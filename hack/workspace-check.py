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
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

def parse_go_version(v: str) -> tuple:
    """Parse a Go module version into a sortable key."""
    v = v.lstrip("v")
    # Pseudo-version: use timestamp
    m = re.match(r"0\.0\.0-(\d{14})-", v)
    if m:
        return (0, 0, 0, 1, m.group(1))
    try:
        from packaging.version import Version
        pv = Version(v)
        return (pv.major, pv.minor, pv.micro, 0 if pv.pre else 1, str(pv))
    except Exception:
        pass
    m = re.match(r"(\d+)\.(\d+)\.(\d+)", v)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)), 1, "")
    return (0, 0, 0, 0, v)


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
class DowngradingReplace:
    repo: str
    module: str
    pinned_version: str
    needed_version: str


@dataclass
class BuildResult:
    repo: str
    success: bool
    error_summary: str = ""
    raw_errors: str = ""
    error_type: str = ""  # "replace_conflict", "missing_module", "api_break", "downgrading_replace", "other"


@dataclass
class CompatReport:
    timestamp: str
    repos: list[str]
    replace_conflicts: list[ReplaceConflict]
    downgrading_replaces: list[DowngradingReplace]
    # Pass 1: all repos in workspace (shows real breakage)
    full_build_results: list[BuildResult]
    # Pass 2: without problematic repos (shows what works today)
    clean_build_results: list[BuildResult]
    clean_repos: list[str]  # repos in the clean workspace
    excluded_repos: list[str]  # repos excluded due to replace issues
    workspace_go_work: str  # the clean go.work

    @property
    def compatible_repos(self) -> list[str]:
        return [r.repo for r in self.clean_build_results if r.success]

    @property
    def broken_repos(self) -> list[str]:
        return (
            [r.repo for r in self.clean_build_results if not r.success]
            + self.excluded_repos
        )


# --- Replace conflict detection (static) ---

def detect_replace_issues(
    repos_dir: Path,
    repos: list[str],
) -> tuple[list[ReplaceConflict], list[DowngradingReplace]]:
    """Find replace directive issues across repos.

    Detects:
    1. Multi-repo conflicts: 2+ repos replace same module to different targets
    2. Downgrading replaces: a repo replaces a shared dep to an older version
       than other repos require (breaks the workspace even if only one repo does it)

    Returns (conflicts, downgrading_replaces).
    """
    replace_map: dict[str, dict[str, str]] = defaultdict(dict)
    replace_versions: dict[str, dict[str, str]] = defaultdict(dict)
    require_versions: dict[str, dict[str, str]] = defaultdict(dict)

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
        for req in data.get("Require") or []:
            require_versions[req["Path"]][repo] = req["Version"]
        for rep in data.get("Replace") or []:
            old = rep["Old"]["Path"]
            new_path = rep["New"]["Path"]
            new_ver = rep["New"].get("Version", "")
            replace_map[old][repo] = f"{new_path} {new_ver}".strip()
            if new_ver and old == new_path:  # same-module version pin
                replace_versions[old][repo] = new_ver

    conflicts = []
    for mod, repo_targets in sorted(replace_map.items()):
        if len(repo_targets) >= 2 and len(set(repo_targets.values())) > 1:
            conflicts.append(ReplaceConflict(module=mod, repos=repo_targets))

    downgrades = []
    for mod, repo_ver in replace_versions.items():
        required = require_versions.get(mod, {})
        if len(required) < 2:
            continue
        max_required = max(required.values(), key=parse_go_version)
        for repo, pinned_ver in repo_ver.items():
            if parse_go_version(pinned_ver) < parse_go_version(max_required):
                downgrades.append(DowngradingReplace(
                    repo=repo, module=mod,
                    pinned_version=pinned_ver, needed_version=max_required,
                ))

    return conflicts, downgrades


# --- Build checking ---

def detect_max_go_version(repos_dir: Path, repos: list[str]) -> str:
    """Find the highest Go version across all repos' go.mod files."""
    versions = []
    for repo in repos:
        gomod = repos_dir / repo / "go.mod"
        if not gomod.exists():
            continue
        result = subprocess.run(
            ["go", "mod", "edit", "-json", str(gomod)],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if go_ver := data.get("Go"):
                versions.append(go_ver)
    if not versions:
        return "1.25.8"
    # Sort as tuples for proper version comparison
    return max(versions, key=lambda v: tuple(int(x) for x in v.split(".") if x.isdigit()))


def create_workspace(
    repos_dir: Path,
    repos: list[str],
    go_version: str | None = None,
) -> str:
    """Create a go.work file in repos_dir and return its content."""
    if go_version is None:
        go_version = detect_max_go_version(repos_dir, repos)
    lines = [f"go {go_version}", "", "use ("]
    for repo in repos:
        lines.append(f"\t./{repo}")
    lines.append(")")
    content = "\n".join(lines) + "\n"
    (repos_dir / "go.work").write_text(content)
    return content


def classify_error(stderr: str) -> tuple[str, str]:
    """Classify a build error and extract a summary.

    Returns (error_type, summary).
    """
    lines = stderr.strip().splitlines()

    # Go version mismatch in go.work
    for line in lines:
        if "requires go >=" in line and "go.work lists" in line:
            return "go_version", line.strip()

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
    repos_dir: Path,
    repo: str,
    build_target: str = "./cmd/...",
) -> BuildResult:
    """Try to build a repo within the workspace context.

    Expects a go.work file in repos_dir.
    """
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
        env={**os.environ, "GOWORK": str(repos_dir / "go.work")},
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

    # 1. Static analysis: detect replace issues
    print("  → Detecting replace issues...", file=sys.stderr)
    conflicts, downgrades = detect_replace_issues(repos_dir, repos)

    for d in downgrades:
        print(
            f"  ⚠ {d.repo} replaces {d.module} → {d.pinned_version} "
            f"(other repos need {d.needed_version})",
            file=sys.stderr,
        )

    # 2. Determine repos to exclude for multi-repo conflicts only
    #    (can't even create a go.work with conflicting replaces)
    conflict_excluded = set()
    if conflicts:
        conflict_count: dict[str, int] = defaultdict(int)
        for c in conflicts:
            for repo in c.repos:
                conflict_count[repo] += 1
        remaining = list(conflicts)
        while remaining:
            worst = max(conflict_count, key=conflict_count.get)
            conflict_excluded.add(worst)
            remaining = [c for c in remaining if worst not in c.repos]
            del conflict_count[worst]

    # --- Pass 1: Full workspace (all repos except hard conflicts) ---
    pass1_repos = [r for r in repos if r not in conflict_excluded]
    print(f"\n  ══ Pass 1: Full workspace ({len(pass1_repos)} repos) ══", file=sys.stderr)

    full_build_results = []
    try:
        create_workspace(repos_dir, pass1_repos)
        for repo in pass1_repos:
            print(f"  → Building {repo}...", file=sys.stderr)
            result = check_repo_build(repos_dir, repo)
            full_build_results.append(result)
    finally:
        _cleanup_gowork(repos_dir)

    # Add conflict-excluded repos
    for repo in sorted(conflict_excluded):
        involved = [c for c in conflicts if repo in c.repos]
        mods = ", ".join(f"`{c.module}`" for c in involved)
        full_build_results.append(BuildResult(
            repo=repo, success=False,
            error_type="replace_conflict",
            error_summary=f"Excluded — conflicting replace directives for {mods}",
        ))

    full_build_results.sort(key=lambda r: (not r.success, r.repo))

    # --- Pass 2: Clean workspace (exclude downgrading replaces too) ---
    downgrade_repos = {d.repo for d in downgrades}
    clean_excluded = conflict_excluded | downgrade_repos
    clean_repos = [r for r in repos if r not in clean_excluded]

    clean_build_results = []
    go_work_content = ""

    if clean_repos != pass1_repos:
        print(f"\n  ══ Pass 2: Clean workspace ({len(clean_repos)} repos, "
              f"excluding {', '.join(sorted(clean_excluded))}) ══", file=sys.stderr)
        try:
            go_work_content = create_workspace(repos_dir, clean_repos)
            for repo in clean_repos:
                print(f"  → Building {repo}...", file=sys.stderr)
                result = check_repo_build(repos_dir, repo)
                clean_build_results.append(result)
        finally:
            _cleanup_gowork(repos_dir)
    else:
        # No downgrading replaces — pass 2 is same as pass 1
        clean_build_results = [r for r in full_build_results if r.repo in clean_repos]
        go_work_content = f"go 1.25.8\n\nuse (\n" + "".join(f"\t./{r}\n" for r in clean_repos) + ")\n"

    clean_build_results.sort(key=lambda r: (not r.success, r.repo))

    return CompatReport(
        timestamp=timestamp,
        repos=repos,
        replace_conflicts=conflicts,
        downgrading_replaces=downgrades,
        full_build_results=full_build_results,
        clean_build_results=clean_build_results,
        clean_repos=clean_repos,
        excluded_repos=sorted(clean_excluded),
        workspace_go_work=go_work_content,
    )


def _cleanup_gowork(repos_dir: Path) -> None:
    for name in ("go.work", "go.work.sum"):
        f = repos_dir / name
        if f.exists():
            f.unlink()


# --- Rendering: terminal ---

def _c(code: str, text: str) -> str:
    colors = {
        "red": "\033[0;31m", "green": "\033[0;32m", "yellow": "\033[0;33m",
        "cyan": "\033[0;36m", "bold": "\033[1m", "dim": "\033[2m", "reset": "\033[0m",
    }
    return f"{colors.get(code, '')}{text}{colors['reset']}"


ERROR_TYPE_LABELS = {
    "go_version": "Go Version Mismatch",
    "replace_conflict": "Replace Conflict",
    "missing_module": "Missing Module",
    "api_break": "API Break",
    "other": "Build Error",
}


def _render_build_list(lines: list[str], results: list[BuildResult]) -> None:
    for r in results:
        if r.success:
            lines.append(f"  {_c('green', '✓')} {r.repo}")
        else:
            label = ERROR_TYPE_LABELS.get(r.error_type, r.error_type)
            lines.append(f"  {_c('red', '✗')} {r.repo} — {_c('yellow', label)}")
            lines.append(f"    {_c('dim', r.error_summary)}")


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

    # Downgrading replaces
    if report.downgrading_replaces:
        lines.append(_c("bold", f"── Downgrading Replace Directives ({len(report.downgrading_replaces)}) ──"))
        lines.append("")
        by_repo: dict[str, list[DowngradingReplace]] = defaultdict(list)
        for d in report.downgrading_replaces:
            by_repo[d.repo].append(d)
        for repo in sorted(by_repo):
            lines.append(f"  {_c('yellow', '⚠')} {_c('bold', repo)}")
            for d in by_repo[repo]:
                lines.append(f"    {d.module}")
                lines.append(f"      pinned: {_c('red', d.pinned_version)}  needed: {_c('green', d.needed_version)}")
            lines.append("")
        lines.append(f"  {_c('dim', 'These replace directives downgrade shared deps, breaking other repos in the workspace.')}")
        lines.append("")

    # Pass 1: Full workspace
    full_ok = sum(1 for r in report.full_build_results if r.success)
    full_total = len(report.full_build_results)
    lines.append(_c("bold", f"── Full Workspace ({full_ok}/{full_total} build) ──"))
    lines.append("")
    _render_build_list(lines, report.full_build_results)
    lines.append("")

    # Pass 2: Clean workspace (only if different)
    if report.excluded_repos:
        clean_ok = sum(1 for r in report.clean_build_results if r.success)
        clean_total = len(report.clean_build_results)
        lines.append(_c("bold", f"── Clean Workspace ({clean_ok}/{clean_total} build, "
                        f"without {', '.join(report.excluded_repos)}) ──"))
        lines.append("")
        _render_build_list(lines, report.clean_build_results)
        lines.append("")

    # Summary
    ok = len(report.compatible_repos)
    fail = len(report.broken_repos)
    lines.append(_c("bold", "── Summary ──"))
    lines.append(f"  Compatible:  {_c('green', str(ok))}")
    lines.append(f"  Broken:      {_c('red', str(fail))}")
    if report.excluded_repos:
        lines.append(f"  Excluded:    {_c('yellow', ', '.join(report.excluded_repos))} (downgrading replaces)")
    if report.compatible_repos:
        lines.append(f"\n  {_c('cyan', 'Working workspace:')}") 
        lines.append(f"  go work init {' '.join('./' + r for r in report.compatible_repos)}")
    lines.append("")

    return "\n".join(lines)


# --- Rendering: markdown ---

def _md_build_table(lines: list[str], results: list[BuildResult]) -> None:
    lines += [
        "| Repo | Status | Issue |",
        "|------|--------|-------|",
    ]
    for r in results:
        if r.success:
            lines.append(f"| {r.repo} | ✅ builds | — |")
        else:
            label = ERROR_TYPE_LABELS.get(r.error_type, r.error_type)
            lines.append(f"| {r.repo} | ❌ {label} | {r.error_summary} |")
    lines.append("")


def render_markdown(report: CompatReport) -> str:
    lines = [
        "## 🔨 Tekton Workspace Compatibility Check",
        "",
        f"**Generated:** {report.timestamp}  ",
        f"**Repos checked:** {len(report.repos)}",
        "",
    ]

    ok = len(report.compatible_repos)

    lines += [
        "| Metric | Result |",
        "|--------|--------|",
        f"| Compatible repos | {'🟢' if ok == len(report.repos) else '🟡' if ok > len(report.repos)//2 else '🔴'} {ok}/{len(report.repos)} |",
        f"| Replace conflicts | {'🟢' if not report.replace_conflicts else '🔴'} {len(report.replace_conflicts)} |",
        f"| Downgrading replaces | {'🟢' if not report.downgrading_replaces else '🟡'} {len(report.downgrading_replaces)} |",
        "",
    ]

    # --- Downgrading replaces ---
    if report.downgrading_replaces:
        lines += [
            "### ⚠️ Downgrading Replace Directives",
            "",
            "These repos have `replace` directives that pin shared dependencies to **older versions** ",
            "than other repos require. In a Go workspace, replaces apply globally — one repo's ",
            "downgrade breaks everyone else.",
            "",
            "| Repo | Module | Pinned To | Others Need |",
            "|------|--------|-----------|-------------|",
        ]
        for d in report.downgrading_replaces:
            lines.append(f"| {d.repo} | `{d.module}` | `{d.pinned_version}` | `{d.needed_version}` |")
        lines += [
            "",
            "**Fix:** Remove these replace directives and update the code to work with the newer versions.",
            "",
        ]

    # --- Replace conflicts ---
    if report.replace_conflicts:
        lines += [
            "### ❌ Replace Directive Conflicts",
            "",
            "These modules have conflicting `replace` directives across repos (can't even create a `go.work`):",
            "",
        ]
        for c in report.replace_conflicts:
            lines.append(f"**`{c.module}`**")
            lines += ["| Repo | Replace Target |", "|------|---|"]
            for repo, target in sorted(c.repos.items()):
                lines.append(f"| {repo} | `{target}` |")
            lines.append("")

    # --- Pass 1: Full workspace ---
    full_ok = sum(1 for r in report.full_build_results if r.success)
    full_total = len(report.full_build_results)
    lines += [
        f"### Full Workspace Build ({full_ok}/{full_total})",
        "",
        "All repos in a single `go.work` (except hard conflicts):",
        "",
    ]
    _md_build_table(lines, report.full_build_results)

    # Breaking change details
    broken = [r for r in report.full_build_results if not r.success and r.error_type in ("missing_module", "api_break")]
    if broken:
        lines += [
            "<details>",
            "<summary><b>Build error details</b></summary>",
            "",
        ]
        for r in broken:
            lines.append(f"**{r.repo}** — {r.error_summary}")
            if r.raw_errors:
                relevant = [l.strip() for l in r.raw_errors.splitlines()
                           if any(x in l for x in ["no required module", "undefined:", "cannot use",
                                                    "has no field or method", "not enough arguments"])]
                if relevant:
                    lines.append("```")
                    lines.extend(relevant[:15])
                    if len(relevant) > 15:
                        lines.append(f"... and {len(relevant) - 15} more")
                    lines.append("```")
            lines.append("")
        lines += ["</details>", ""]

    # --- Pass 2: Clean workspace ---
    if report.excluded_repos:
        clean_ok = sum(1 for r in report.clean_build_results if r.success)
        clean_total = len(report.clean_build_results)
        lines += [
            f"### Clean Workspace Build ({clean_ok}/{clean_total})",
            "",
            f"Without repos that have problematic replaces ({', '.join(report.excluded_repos)}):",
            "",
        ]
        _md_build_table(lines, report.clean_build_results)

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
        lines += ["```", ""]

    lines += [
        "---",
        "*Generated by [`workspace-check.py`](../blob/main/hack/workspace-check.py) — "
        "run locally or via [weekly CI](../blob/main/.github/workflows/workspace-check.yaml)*",
    ]

    return "\n".join(lines)


# --- Rendering: JSON ---

def _build_results_json(results: list[BuildResult]) -> list[dict]:
    return [
        {"repo": r.repo, "success": r.success,
         "error_type": r.error_type, "error_summary": r.error_summary}
        for r in results
    ]


def render_json(report: CompatReport) -> str:
    return json.dumps({
        "timestamp": report.timestamp,
        "repos": report.repos,
        "replace_conflicts": [
            {"module": c.module, "repos": c.repos}
            for c in report.replace_conflicts
        ],
        "downgrading_replaces": [
            {"repo": d.repo, "module": d.module,
             "pinned": d.pinned_version, "needed": d.needed_version}
            for d in report.downgrading_replaces
        ],
        "full_build": _build_results_json(report.full_build_results),
        "clean_build": _build_results_json(report.clean_build_results),
        "excluded": report.excluded_repos,
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
