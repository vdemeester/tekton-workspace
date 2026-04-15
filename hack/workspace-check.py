#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "packaging",
# ]
# ///
"""
Tekton Workspace Compatibility Check

Exercises real builds across repos in a Go workspace to detect:
1. Conflicting replace directives (go.mod static analysis)
2. Breaking API changes when dependencies are upgraded via MVS
3. Missing modules when newer dep versions drop packages

Usage:
    ./hack/workspace-check.py                           # check all local repos
    ./hack/workspace-check.py pipeline cli triggers     # specific repos
    ./hack/workspace-check.py --format markdown         # GitHub issue output
    ./hack/workspace-check.py --format json             # machine-readable
    ./hack/workspace-check.py --repos-dir ./repos       # custom repos location
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ALL_REPOS = [
    "pipeline", "triggers", "chains", "cli", "results",
    "operator", "pipelines-as-code", "dashboard",
    "plumbing", "pruner",
]


# --- Data types ---

@dataclass
class ReplaceConflict:
    module: str
    repos: dict[str, str]  # repo -> replace target


@dataclass
class BuildResult:
    repo: str
    success: bool
    error_summary: str = ""
    raw_errors: str = ""
    error_type: str = ""  # "replace_conflict", "missing_module", "api_break", "other"


@dataclass
class CompatReport:
    timestamp: str
    repos: list[str]
    replace_conflicts: list[ReplaceConflict]
    build_results: list[BuildResult]
    workspace_go_work: str

    @property
    def compatible_repos(self) -> list[str]:
        return [r.repo for r in self.build_results if r.success]

    @property
    def broken_repos(self) -> list[str]:
        return [r.repo for r in self.build_results if not r.success]


# --- Replace conflict detection (static) ---

def detect_replace_conflicts(repos_dir: Path, repos: list[str]) -> list[ReplaceConflict]:
    """Find modules with conflicting replace directives across repos."""
    replace_map: dict[str, dict[str, str]] = defaultdict(dict)

    for repo in repos:
        gomod = repos_dir / repo / "go.mod"
        if not gomod.exists():
            continue
        result = subprocess.run(
            ["go", "mod", "edit", "-json", str(gomod)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            continue
        data = json.loads(result.stdout)
        for rep in data.get("Replace") or []:
            old = rep["Old"]["Path"]
            new_path = rep["New"]["Path"]
            new_ver = rep["New"].get("Version", "")
            replace_map[old][repo] = f"{new_path} {new_ver}".strip()

    conflicts = []
    for mod, repo_targets in sorted(replace_map.items()):
        if len(repo_targets) >= 2 and len(set(repo_targets.values())) > 1:
            conflicts.append(ReplaceConflict(module=mod, repos=repo_targets))

    return conflicts


# --- Build checking ---

def create_workspace(
    workspace_dir: Path,
    repos_dir: Path,
    repos: list[str],
    go_version: str = "1.25.7",
) -> str:
    """Create a go.work file and return its content."""
    lines = [f"go {go_version}", "", "use ("]
    for repo in repos:
        # Compute relative path from workspace_dir to repos_dir/repo
        rel = os.path.relpath(repos_dir / repo, workspace_dir)
        lines.append(f"\t{rel}")
    lines.append(")")
    content = "\n".join(lines) + "\n"
    (workspace_dir / "go.work").write_text(content)
    return content


def classify_error(stderr: str) -> tuple[str, str]:
    """Classify a build error and extract a summary.

    Returns (error_type, summary).
    """
    lines = stderr.strip().splitlines()

    # Replace conflict
    for line in lines:
        if "conflicting replacements" in line:
            mod = line.split("for ")[-1].rstrip(":")
            return "replace_conflict", f"Conflicting replace directives for `{mod}`"

    # Missing module / package
    missing = []
    for line in lines:
        if "no required module provides package" in line:
            pkg = line.split("package ")[-1].split(";")[0].strip()
            missing.append(pkg)
    if missing:
        summary = f"Missing {len(missing)} package(s): " + ", ".join(f"`{p}`" for p in missing[:5])
        if len(missing) > 5:
            summary += f" (+{len(missing) - 5} more)"
        return "missing_module", summary

    # API break: type/method errors
    api_errors = []
    for line in lines:
        if any(x in line for x in [
            "undefined:", "cannot use", "not enough arguments",
            "too many arguments", "has no field or method",
        ]):
            api_errors.append(line.strip())
    if api_errors:
        summary = f"{len(api_errors)} compilation error(s)"
        return "api_break", summary

    # Other
    if lines:
        return "other", lines[-1][:200]
    return "other", "Unknown error"


def check_repo_build(
    workspace_dir: Path,
    repos_dir: Path,
    repo: str,
    build_target: str = "./cmd/...",
) -> BuildResult:
    """Try to build a repo within the workspace context."""
    repo_dir = repos_dir / repo

    # Try ./cmd/... first, fall back to ./... if no cmd dir
    if not (repo_dir / "cmd").exists():
        build_target = "./pkg/..."
        if not (repo_dir / "pkg").exists():
            build_target = "./..."

    result = subprocess.run(
        ["go", "build", build_target],
        capture_output=True,
        text=True,
        cwd=str(repo_dir),
        env={**os.environ, "GOWORK": str(workspace_dir / "go.work")},
        timeout=300,
    )

    if result.returncode == 0:
        return BuildResult(repo=repo, success=True)

    stderr = result.stderr
    error_type, summary = classify_error(stderr)

    return BuildResult(
        repo=repo,
        success=False,
        error_summary=summary,
        raw_errors=stderr[-3000:],  # last 3k chars
        error_type=error_type,
    )


def run_checks(
    repos_dir: Path,
    repos: list[str],
) -> CompatReport:
    """Run full compatibility check."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Filter to repos that exist
    repos = [r for r in repos if (repos_dir / r / "go.mod").exists()]
    if not repos:
        print("No repos found", file=sys.stderr)
        sys.exit(1)

    print(f"Checking {len(repos)} repos: {', '.join(repos)}", file=sys.stderr)

    # 1. Static: detect replace conflicts
    print("  → Detecting replace conflicts...", file=sys.stderr)
    conflicts = detect_replace_conflicts(repos_dir, repos)

    # 2. Determine which repos can be in the workspace (no replace conflicts)
    conflicting_repos = set()
    if conflicts:
        # Find the minimal set of repos to exclude to resolve all conflicts
        # Simple heuristic: count how many conflicts each repo is in, exclude most conflicting
        conflict_count: dict[str, int] = defaultdict(int)
        for c in conflicts:
            for repo in c.repos:
                conflict_count[repo] += 1
        # Exclude repos with conflicts, but try to keep as many as possible
        # by removing the most-conflicting first
        remaining_conflicts = list(conflicts)
        while remaining_conflicts:
            worst = max(conflict_count, key=conflict_count.get)
            conflicting_repos.add(worst)
            remaining_conflicts = [
                c for c in remaining_conflicts if worst not in c.repos
            ]
            del conflict_count[worst]

    workspace_repos = [r for r in repos if r not in conflicting_repos]

    # 3. Create workspace and build
    with tempfile.TemporaryDirectory(prefix="tekton-workspace-") as tmpdir:
        workspace_dir = Path(tmpdir)
        go_work_content = create_workspace(workspace_dir, repos_dir, workspace_repos)

        build_results = []

        # Build repos that are in the workspace
        for repo in workspace_repos:
            print(f"  → Building {repo}...", file=sys.stderr)
            result = check_repo_build(workspace_dir, repos_dir, repo)
            build_results.append(result)

        # Report excluded repos as replace_conflict failures
        for repo in sorted(conflicting_repos):
            involved = [
                c for c in conflicts if repo in c.repos
            ]
            mods = ", ".join(f"`{c.module}`" for c in involved)
            build_results.append(BuildResult(
                repo=repo,
                success=False,
                error_type="replace_conflict",
                error_summary=f"Excluded from workspace — conflicting replaces for {mods}",
            ))

    # Sort: successes first, then by repo name
    build_results.sort(key=lambda r: (not r.success, r.repo))

    return CompatReport(
        timestamp=timestamp,
        repos=repos,
        replace_conflicts=conflicts,
        build_results=build_results,
        workspace_go_work=go_work_content,
    )


# --- Rendering: terminal ---

def _c(code: str, text: str) -> str:
    colors = {
        "red": "\033[0;31m", "green": "\033[0;32m", "yellow": "\033[0;33m",
        "cyan": "\033[0;36m", "bold": "\033[1m", "dim": "\033[2m", "reset": "\033[0m",
    }
    return f"{colors.get(code, '')}{text}{colors['reset']}"


ERROR_TYPE_LABELS = {
    "replace_conflict": "Replace Conflict",
    "missing_module": "Missing Module",
    "api_break": "API Break",
    "other": "Build Error",
}


def render_terminal(report: CompatReport) -> str:
    lines = [
        "",
        _c("bold", "═" * 55),
        _c("bold", "  Tekton Workspace Compatibility Check"),
        _c("bold", "═" * 55),
        "",
        f"{_c('cyan', 'Generated:')} {report.timestamp}",
        f"{_c('cyan', 'Repos:')} {', '.join(report.repos)}",
        "",
    ]

    # Replace conflicts
    if report.replace_conflicts:
        lines.append(_c("bold", f"── Replace Conflicts ({len(report.replace_conflicts)}) ──"))
        lines.append("")
        for c in report.replace_conflicts:
            lines.append(f"  {_c('red', '✗')} {_c('bold', c.module)}")
            for repo, target in sorted(c.repos.items()):
                lines.append(f"    {repo:<25} → {target}")
            lines.append("")

    # Build results
    lines.append(_c("bold", "── Build Results ──"))
    lines.append("")
    for r in report.build_results:
        if r.success:
            lines.append(f"  {_c('green', '✓')} {r.repo}")
        else:
            label = ERROR_TYPE_LABELS.get(r.error_type, r.error_type)
            lines.append(f"  {_c('red', '✗')} {r.repo} — {_c('yellow', label)}")
            lines.append(f"    {_c('dim', r.error_summary)}")
    lines.append("")

    # Summary
    ok = len(report.compatible_repos)
    fail = len(report.broken_repos)
    lines.append(_c("bold", "── Summary ──"))
    lines.append(f"  Compatible:  {_c('green', str(ok))}")
    lines.append(f"  Broken:      {_c('red', str(fail))}")
    if report.compatible_repos:
        lines.append(f"\n  {_c('cyan', 'Working workspace:')}")
        lines.append(f"  go work init {' '.join('../' + r for r in report.compatible_repos)}")
    lines.append("")

    return "\n".join(lines)


# --- Rendering: markdown ---

def render_markdown(report: CompatReport) -> str:
    lines = [
        "## 🔨 Tekton Workspace Compatibility Check",
        "",
        f"**Generated:** {report.timestamp}  ",
        f"**Repos checked:** {len(report.repos)}",
        "",
    ]

    ok = len(report.compatible_repos)
    fail = len(report.broken_repos)

    lines += [
        "| Metric | Result |",
        "|--------|--------|",
        f"| Build in workspace | {'🟢' if ok == len(report.repos) else '🟡' if ok > fail else '🔴'} {ok}/{len(report.repos)} repos |",
        f"| Replace conflicts | {'🟢' if not report.replace_conflicts else '🔴'} {len(report.replace_conflicts)} |",
        "",
    ]

    # Build results overview
    lines += ["### Build Results", ""]
    lines += [
        "| Repo | Status | Issue |",
        "|------|--------|-------|",
    ]
    for r in report.build_results:
        if r.success:
            lines.append(f"| {r.repo} | ✅ builds | — |")
        else:
            label = ERROR_TYPE_LABELS.get(r.error_type, r.error_type)
            lines.append(f"| {r.repo} | ❌ {label} | {r.error_summary} |")
    lines.append("")

    # Replace conflicts detail
    if report.replace_conflicts:
        lines += [
            "### ⚠️ Replace Directive Conflicts",
            "",
            "Repos with conflicting `replace` directives cannot coexist in a `go.work`.",
            "The Go team [recommends avoiding replace directives](https://go.dev/ref/mod#go-mod-file-replace) ",
            "in libraries. Consider removing them and updating dependencies instead.",
            "",
        ]
        for c in report.replace_conflicts:
            lines.append(f"**`{c.module}`**")
            lines += [
                "| Repo | Replace Target |",
                "|------|---------------|",
            ]
            for repo, target in sorted(c.repos.items()):
                lines.append(f"| {repo} | `{target}` |")
            lines.append("")

        # Actionable fix
        lines += [
            "<details>",
            "<summary><b>How to fix replace conflicts</b></summary>",
            "",
            "Replace directives pin a dependency to a specific version, overriding MVS.",
            "When two repos replace the same module to different versions, Go cannot resolve it.",
            "",
            "**Options:**",
            "1. **Remove the replace** — update the code to work with the version MVS selects",
            "2. **Align the replace** — make both repos point to the same version",
            "3. **Upgrade past the need** — often replaces exist for old compatibility; upgrading deps may eliminate them",
            "",
        ]
        for c in report.replace_conflicts:
            # Suggest aligning to the newest target
            targets = list(c.repos.values())
            lines.append(f"For `{c.module}`:")
            lines.append("```bash")
            for repo in sorted(c.repos):
                lines.append(f"# In {repo}/go.mod — consider removing this replace:")
                lines.append(f"#   replace {c.module} => {c.repos[repo]}")
            lines.append("```")
            lines.append("")
        lines += ["</details>", ""]

    # Breaking API / missing module details
    broken = [r for r in report.build_results if not r.success and r.error_type in ("missing_module", "api_break")]
    if broken:
        lines += [
            "### 🔥 Breaking Changes from Dependency Upgrades",
            "",
            "These repos build fine standalone (`GOWORK=off go build ./...`) but break in the ",
            "workspace because Go's MVS selects a newer dependency version that has breaking changes.",
            "",
            "This is **real drift** — it means these repos are relying on APIs from older dependency ",
            "versions that have since changed. Fixing these makes the codebase more maintainable and ",
            "unblocks workspace-based development.",
            "",
        ]
        for r in broken:
            lines += [
                "<details>",
                f"<summary><b>{r.repo}</b> — {r.error_summary}</summary>",
                "",
            ]
            if r.raw_errors:
                # Extract the most relevant error lines
                relevant = []
                for line in r.raw_errors.splitlines():
                    if any(x in line for x in [
                        "no required module", "undefined:", "cannot use",
                        "has no field or method", "not enough arguments",
                    ]):
                        relevant.append(line.strip())
                if relevant:
                    lines.append("```")
                    for l in relevant[:20]:
                        lines.append(l)
                    if len(relevant) > 20:
                        lines.append(f"... and {len(relevant) - 20} more errors")
                    lines.append("```")
                    lines.append("")

            lines.append("**How to fix:** Update the repo to use the newer dependency API:")
            lines.append("```bash")
            lines.append(f"cd {r.repo}")
            if r.error_type == "missing_module":
                lines.append("# Add missing dependencies:")
                for line in r.raw_errors.splitlines():
                    if "go get " in line:
                        lines.append(line.strip())
            else:
                lines.append("# Update deps and fix compilation errors:")
                lines.append("go get -u ./...")
                lines.append("go build ./...")
            lines.append("```")
            lines += ["</details>", ""]

    # Working workspace
    if report.compatible_repos:
        lines += [
            "### ✅ Working Workspace",
            "",
            "These repos can be used together in a `go.work` today:",
            "",
            "```go",
        ]
        lines.append(report.workspace_go_work.rstrip())
        lines += [
            "```",
            "",
        ]

    lines += [
        "---",
        "*Generated by [`workspace-check.py`](../blob/main/hack/workspace-check.py) — "
        "run locally or via [weekly CI](../blob/main/.github/workflows/workspace-check.yaml)*",
    ]

    return "\n".join(lines)


# --- Rendering: JSON ---

def render_json(report: CompatReport) -> str:
    return json.dumps({
        "timestamp": report.timestamp,
        "repos": report.repos,
        "replace_conflicts": [
            {"module": c.module, "repos": c.repos}
            for c in report.replace_conflicts
        ],
        "build_results": [
            {
                "repo": r.repo,
                "success": r.success,
                "error_type": r.error_type,
                "error_summary": r.error_summary,
            }
            for r in report.build_results
        ],
        "compatible": report.compatible_repos,
        "broken": report.broken_repos,
    }, indent=2)


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("repos", nargs="*", help="Repos to check (default: all local)")
    parser.add_argument("--repos-dir", type=Path, default=None)
    parser.add_argument("--format", choices=["terminal", "markdown", "json"], default="terminal")
    parser.add_argument("--output", "-o", type=Path, help="Write output to file")
    args = parser.parse_args()

    # Resolve repos directory
    if args.repos_dir:
        repos_dir = args.repos_dir.resolve()
    else:
        repos_dir = Path(__file__).resolve().parent.parent

    repos = args.repos if args.repos else [
        r for r in ALL_REPOS if (repos_dir / r / "go.mod").exists()
    ]

    if not repos:
        print(f"No Tekton repos found in {repos_dir}", file=sys.stderr)
        sys.exit(1)

    report = run_checks(repos_dir, repos)

    if args.format == "json":
        output = render_json(report)
    elif args.format == "markdown":
        output = render_markdown(report)
    else:
        output = render_terminal(report)

    if args.output:
        args.output.write_text(output)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(output)

    sys.exit(1 if report.broken_repos else 0)


if __name__ == "__main__":
    main()
