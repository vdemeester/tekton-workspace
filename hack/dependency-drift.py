#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "packaging",
# ]
# ///
"""
Tekton Dependency Drift Report

Scans go.mod files across Tekton repos and reports version skew on shared
dependencies, replace directive conflicts, and workspace compatibility.

Usage:
    ./hack/dependency-drift.py                              # scan all local repos
    ./hack/dependency-drift.py pipeline triggers cli         # specific repos
    ./hack/dependency-drift.py --modules k8s.io/api         # filter modules
    ./hack/dependency-drift.py --fix                        # show alignment commands
    ./hack/dependency-drift.py --format markdown            # GitHub-flavored markdown
    ./hack/dependency-drift.py --format json                # machine-readable
    ./hack/dependency-drift.py --repos-dir /path/to/repos   # custom repos location
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from packaging.version import Version

ALL_REPOS = [
    "pipeline", "triggers", "chains", "cli", "results",
    "operator", "pipelines-as-code", "dashboard",
    "plumbing", "pruner",
]

IMPORTANT_PREFIXES = [
    "k8s.io/", "knative.dev/", "github.com/tektoncd/",
    "sigs.k8s.io/", "go.opentelemetry.io/",
    "google.golang.org/grpc", "google.golang.org/protobuf",
]


# --- Version sorting ---

def parse_go_version(v: str) -> tuple:
    """Parse a Go module version into a sortable key.

    Handles:
    - Standard semver: v0.35.3, v1.43.0
    - Pseudo-versions: v0.0.0-20260406140200-cb58ae50e894
    - Pre-release: v1.2.3-rc1
    """
    v = v.lstrip("v")

    # Pseudo-version: use timestamp for ordering
    m = re.match(r"0\.0\.0-(\d{14})-", v)
    if m:
        return (0, 0, 0, 1, m.group(1))

    # Standard semver with packaging (handles rc, beta, etc.)
    try:
        pv = Version(v)
        return (pv.major, pv.minor, pv.micro, 0 if pv.pre else 1, str(pv))
    except Exception:
        pass

    # Fallback: extract numeric parts
    m = re.match(r"(\d+)\.(\d+)\.(\d+)", v)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)), 1, "")

    return (0, 0, 0, 0, v)


def latest_version(versions: list[str]) -> str:
    """Return the highest version from a list."""
    return max(versions, key=parse_go_version)


# --- Data collection ---

@dataclass
class RepoData:
    go_version: str = ""
    requires: dict[str, str] = field(default_factory=dict)
    replaces: dict[str, str] = field(default_factory=dict)


def collect_repo(repos_dir: Path, repo: str) -> RepoData | None:
    """Parse a single repo's go.mod."""
    gomod = repos_dir / repo / "go.mod"
    if not gomod.exists():
        return None

    result = subprocess.run(
        ["go", "mod", "edit", "-json", str(gomod)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"warning: failed to parse {repo}/go.mod", file=sys.stderr)
        return None

    mod = json.loads(result.stdout)
    data = RepoData(go_version=mod.get("Go", ""))

    for req in mod.get("Require") or []:
        data.requires[req["Path"]] = req["Version"]

    for rep in mod.get("Replace") or []:
        old = rep["Old"]["Path"]
        new_path = rep["New"]["Path"]
        new_ver = rep["New"].get("Version", "")
        data.replaces[old] = f"{new_path} {new_ver}".strip()

    return data


def collect_all(repos_dir: Path, repos: list[str]) -> dict[str, RepoData]:
    """Collect data from all repos."""
    result = {}
    for repo in repos:
        data = collect_repo(repos_dir, repo)
        if data:
            result[repo] = data
    return result


# --- Analysis ---

@dataclass
class DriftedModule:
    versions: dict[str, str]  # repo -> version
    latest: str


@dataclass
class DriftReport:
    timestamp: str
    repos: dict[str, RepoData]
    drifted: dict[str, DriftedModule]
    replace_conflicts: dict[str, dict[str, str]]
    go_versions: dict[str, str]

    @property
    def drift_count(self) -> int:
        return len(self.drifted)

    @property
    def conflict_count(self) -> int:
        return len(self.replace_conflicts)

    @property
    def go_version_count(self) -> int:
        return len(set(self.go_versions.values()))


def analyze(
    repos_data: dict[str, RepoData],
    module_filters: list[str] | None = None,
) -> DriftReport:
    """Analyze dependency drift across repos."""
    # Collect all deps
    dep_versions: dict[str, dict[str, str]] = defaultdict(dict)
    replace_map: dict[str, dict[str, str]] = defaultdict(dict)

    for repo, data in repos_data.items():
        for mod, ver in data.requires.items():
            dep_versions[mod][repo] = ver
        for mod, target in data.replaces.items():
            replace_map[mod][repo] = target

    # Find drifted modules
    drifted = {}
    for mod, ver_map in dep_versions.items():
        if len(ver_map) < 2 or len(set(ver_map.values())) < 2:
            continue
        if not any(mod.startswith(p) for p in IMPORTANT_PREFIXES):
            continue
        if module_filters and not any(f in mod for f in module_filters):
            continue
        best = latest_version(list(ver_map.values()))
        drifted[mod] = DriftedModule(versions=ver_map, latest=best)

    # Find replace conflicts
    conflicts = {}
    for mod, repo_targets in replace_map.items():
        if len(repo_targets) >= 2 and len(set(repo_targets.values())) > 1:
            conflicts[mod] = repo_targets

    go_versions = {r: d.go_version for r, d in repos_data.items()}

    return DriftReport(
        timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        repos=repos_data,
        drifted=dict(sorted(drifted.items(), key=lambda kv: _mod_sort_key(kv[0]))),
        replace_conflicts=dict(sorted(conflicts.items())),
        go_versions=go_versions,
    )


def _mod_sort_key(mod: str) -> tuple:
    if mod.startswith("k8s.io"):
        return (0, mod)
    if mod.startswith("knative"):
        return (1, mod)
    if "tektoncd" in mod:
        return (2, mod)
    return (9, mod)


# --- Output: terminal ---

def _c(code: str, text: str) -> str:
    """Colorize text for terminal."""
    colors = {
        "red": "\033[0;31m", "green": "\033[0;32m", "yellow": "\033[0;33m",
        "cyan": "\033[0;36m", "bold": "\033[1m", "reset": "\033[0m",
    }
    return f"{colors.get(code, '')}{text}{colors['reset']}"


def render_terminal(report: DriftReport, fix: bool = False, repos_dir: Path = Path(".")) -> str:
    """Render drift report for terminal output."""
    lines = [
        "",
        _c("bold", "═" * 55),
        _c("bold", "  Tekton Dependency Drift Report"),
        _c("bold", "═" * 55),
        "",
        f"{_c('cyan', 'Generated:')} {report.timestamp}",
        f"{_c('cyan', 'Repos scanned:')} {', '.join(sorted(report.repos))}",
        "",
    ]

    # Go versions
    lines.append(_c("bold", "── Go Versions ──"))
    latest_go = latest_version(list(report.go_versions.values()))
    for repo in sorted(report.go_versions):
        ver = report.go_versions[repo]
        marker = "" if ver == latest_go else f"  {_c('yellow', '⬅')}"
        lines.append(f"  {repo:<25} {ver}{marker}")
    if report.go_version_count > 1:
        lines.append(f"  {_c('yellow', f'⚠ {report.go_version_count} different Go versions')}")
    else:
        lines.append(f"  {_c('green', '✓ All repos on the same Go version')}")
    lines.append("")

    # Drifted deps
    if not report.drifted:
        lines.append(_c("green", "✓ No dependency drift detected"))
    else:
        lines.append(_c("bold", f"── Drifted Dependencies ({report.drift_count} modules) ──"))
        lines.append("")
        for mod, info in report.drifted.items():
            lines.append(f"  {_c('yellow', '⚠')} {_c('bold', mod)}")
            for repo in sorted(info.versions):
                ver = info.versions[repo]
                if ver == info.latest:
                    lines.append(f"    {_c('green', f'{repo:<25} {ver} (latest)')}")
                else:
                    lines.append(f"    {_c('red', f'{repo:<25} {ver}')}")
            if fix:
                lines.append(f"    {_c('cyan', 'Fix:')}")
                for repo in sorted(info.versions):
                    if info.versions[repo] != info.latest:
                        lines.append(f"      cd {repos_dir / repo} && go get {mod}@{info.latest}")
            lines.append("")

    # Replace conflicts
    if report.replace_conflicts:
        lines.append(_c("bold", f"── Replace Directive Conflicts ({report.conflict_count}) ──"))
        lines.append("")
        for mod, repo_targets in report.replace_conflicts.items():
            lines.append(f"  {_c('red', '✗')} {_c('bold', mod)}")
            for repo, target in sorted(repo_targets.items()):
                lines.append(f"    {repo:<25} → {target}")
            lines.append("")
        lines.append(f"  {_c('yellow', 'These prevent repos from coexisting in a go.work workspace.')}")
        lines.append("")

    # Summary
    lines.append(_c("bold", "── Summary ──"))
    lines.append(f"  Repos:              {len(report.repos)}")
    lines.append(f"  Drifted modules:    {report.drift_count}")
    lines.append(f"  Replace conflicts:  {report.conflict_count}")
    if report.drift_count > 0 and not fix:
        lines.append(f"\n  {_c('cyan', 'Run with --fix to generate alignment commands')}")
    lines.append("")

    return "\n".join(lines)


# --- Output: markdown ---

def render_markdown(report: DriftReport, fix: bool = True) -> str:
    """Render drift report as GitHub-flavored markdown."""
    lines = [
        "## 📊 Tekton Dependency Drift Report",
        "",
        f"**Generated:** {report.timestamp}  ",
        f"**Repos scanned:** {len(report.repos)}",
        "",
    ]

    # Summary table
    def badge(val: int, green_max: int = 0, yellow_max: int = 5) -> str:
        if val <= green_max:
            return "🟢"
        return "🟡" if val <= yellow_max else "🔴"

    lines += [
        "| Metric | Count |",
        "|--------|-------|",
        f"| Drifted modules | {badge(report.drift_count)} {report.drift_count} |",
        f"| Replace conflicts | {badge(report.conflict_count)} {report.conflict_count} |",
        f"| Go versions in use | {badge(report.go_version_count, 1, 3)} {report.go_version_count} |",
        "",
    ]

    # Go versions
    latest_go = latest_version(list(report.go_versions.values()))
    lines += [
        "<details>",
        "<summary><b>Go Versions</b></summary>",
        "",
        "| Repo | Go Version |",
        "|------|-----------|",
    ]
    for repo in sorted(report.go_versions):
        ver = report.go_versions[repo]
        marker = "" if ver == latest_go else " ⬅️"
        lines.append(f"| {repo} | `{ver}`{marker} |")
    lines += ["", "</details>", ""]

    # Drifted modules
    if report.drifted:
        lines += ["### Drifted Dependencies", ""]
        for mod, info in report.drifted.items():
            n_versions = len(set(info.versions.values()))
            lines += [
                "<details>",
                f"<summary><b><code>{mod}</code></b> — {n_versions} versions</summary>",
                "",
                "| Repo | Version | Status |",
                "|------|---------|--------|",
            ]
            for repo in sorted(info.versions):
                ver = info.versions[repo]
                status = "✅ latest" if ver == info.latest else "🔴 behind"
                lines.append(f"| {repo} | `{ver}` | {status} |")
            lines.append("")

            if fix:
                behind = [r for r in sorted(info.versions) if info.versions[r] != info.latest]
                if behind:
                    lines += ["**Alignment commands:**", "```bash"]
                    for repo in behind:
                        lines.append(f"cd {repo} && go get {mod}@{info.latest}")
                    lines += ["```"]
            lines += ["</details>", ""]

    # Replace conflicts
    if report.replace_conflicts:
        lines += [
            "### ⚠️ Replace Directive Conflicts",
            "",
            "These prevent repos from coexisting in a `go.work` workspace:",
            "",
        ]
        for mod, repo_targets in report.replace_conflicts.items():
            lines += [
                f"**`{mod}`**",
                "| Repo | Replace Target |",
                "|------|---------------|",
            ]
            for repo, target in sorted(repo_targets.items()):
                lines.append(f"| {repo} | `{target}` |")
            lines.append("")

    # Workspace compatibility matrix
    dep_versions: dict[str, dict[str, str]] = defaultdict(dict)
    for repo, data in report.repos.items():
        for mod, ver in data.requires.items():
            dep_versions[mod][repo] = ver

    k8s_groups: dict[str, list[str]] = defaultdict(list)
    if "k8s.io/api" in dep_versions:
        for repo, ver in dep_versions["k8s.io/api"].items():
            minor = ".".join(ver.lstrip("v").split(".")[:2])
            k8s_groups[minor].append(repo)

    if k8s_groups:
        lines += [
            "### 🧩 Workspace Compatibility",
            "",
            "Repos grouped by `k8s.io/api` minor version (repos in the same row can share a `go.work`):",
            "",
            "| k8s.io/api | Repos |",
            "|-----------|-------|",
        ]
        for minor in sorted(k8s_groups, reverse=True):
            repos_list = ", ".join(sorted(k8s_groups[minor]))
            lines.append(f"| `{minor}` | {repos_list} |")
        lines.append("")

    lines += [
        "---",
        "*Generated by [`dependency-drift.py`](../blob/main/hack/dependency-drift.py) — "
        "run locally or via [weekly CI](../blob/main/.github/workflows/dependency-drift.yaml)*",
    ]

    return "\n".join(lines)


# --- Output: JSON ---

def render_json(report: DriftReport) -> str:
    """Render drift report as JSON."""
    return json.dumps({
        "timestamp": report.timestamp,
        "go_versions": report.go_versions,
        "drifted_modules": {
            mod: {"versions": info.versions, "latest": info.latest}
            for mod, info in report.drifted.items()
        },
        "replace_conflicts": report.replace_conflicts,
        "summary": {
            "repos": len(report.repos),
            "drifted": report.drift_count,
            "conflicts": report.conflict_count,
            "go_versions": report.go_version_count,
        },
    }, indent=2)


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repos", nargs="*", help="Repos to scan (default: auto-detect local)")
    parser.add_argument("--repos-dir", type=Path, default=None, help="Directory containing repo checkouts")
    parser.add_argument("--modules", help="Comma-separated module name filters")
    parser.add_argument("--fix", action="store_true", help="Show alignment commands")
    parser.add_argument("--format", choices=["terminal", "markdown", "json"], default="terminal")
    parser.add_argument("--output", "-o", type=Path, help="Write output to file")
    args = parser.parse_args()

    # Resolve repos directory
    if args.repos_dir:
        repos_dir = args.repos_dir.resolve()
    else:
        # Default: repository root (script is in hack/)
        repos_dir = Path(__file__).resolve().parent.parent

    # Select repos
    if args.repos:
        repos = args.repos
    else:
        # Auto-detect: use repos that exist locally
        repos = [r for r in ALL_REPOS if (repos_dir / r / "go.mod").exists()]
        if not repos:
            print(f"No Tekton repos found in {repos_dir}", file=sys.stderr)
            print("Use --repos-dir or specify repos explicitly", file=sys.stderr)
            sys.exit(1)

    # Collect
    module_filters = args.modules.split(",") if args.modules else None
    repos_data = collect_all(repos_dir, repos)

    if not repos_data:
        print("No repos could be parsed", file=sys.stderr)
        sys.exit(1)

    # Analyze
    report = analyze(repos_data, module_filters)

    # Render
    if args.format == "json":
        output = render_json(report)
    elif args.format == "markdown":
        output = render_markdown(report, fix=args.fix)
    else:
        output = render_terminal(report, fix=args.fix, repos_dir=repos_dir)

    if args.output:
        args.output.write_text(output)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(output)

    # Exit code: non-zero if drift detected (useful for CI)
    sys.exit(1 if report.drift_count > 0 or report.conflict_count > 0 else 0)


if __name__ == "__main__":
    main()
