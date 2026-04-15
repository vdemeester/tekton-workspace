#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "packaging",
# ]
# ///
"""
Tekton Dependency Alignment Tool

Brings repos into alignment on shared core dependencies so they can
coexist in a Go workspace.

Usage:
    # Show what needs aligning (dry-run by default)
    ./hack/align-deps.py

    # Align specific repos
    ./hack/align-deps.py pipeline operator

    # Actually run the go get commands
    ./hack/align-deps.py --apply

    # Target specific module groups
    ./hack/align-deps.py --group k8s       # k8s.io/*
    ./hack/align-deps.py --group knative   # knative.dev/*
    ./hack/align-deps.py --group all       # everything

    # After aligning, verify builds
    ./hack/align-deps.py --apply --verify
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
from pathlib import Path

ALL_REPOS = [
    "pipeline", "triggers", "chains", "cli", "results",
    "operator", "pipelines-as-code", "dashboard",
    "plumbing", "pruner",
]

# Module groups for targeted alignment
MODULE_GROUPS = {
    "k8s": [
        "k8s.io/api", "k8s.io/apimachinery", "k8s.io/client-go",
        "k8s.io/apiextensions-apiserver", "k8s.io/code-generator",
        "k8s.io/kube-openapi", "k8s.io/utils",
    ],
    "knative": [
        "knative.dev/pkg", "knative.dev/eventing",
    ],
    "tekton": [
        "github.com/tektoncd/pipeline",
        "github.com/tektoncd/triggers",
        "github.com/tektoncd/chains",
        "github.com/tektoncd/cli",
    ],
    "otel": [
        "go.opentelemetry.io/otel",
        "go.opentelemetry.io/contrib",
    ],
    "grpc": [
        "google.golang.org/grpc",
        "google.golang.org/protobuf",
    ],
}


def parse_go_version(v: str) -> tuple:
    """Parse a Go module version into a sortable key."""
    v = v.lstrip("v")
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


# --- Data types ---

@dataclass
class AlignmentAction:
    repo: str
    module: str
    current_version: str
    target_version: str
    action_type: str  # "go_get", "drop_replace", "update_replace"


@dataclass
class AlignmentPlan:
    actions: list[AlignmentAction]
    replace_removals: list[AlignmentAction]  # separate for visibility

    @property
    def repos_affected(self) -> set[str]:
        return {a.repo for a in self.actions + self.replace_removals}


# --- Analysis ---

def collect_mod_data(repos_dir: Path, repos: list[str]) -> dict:
    """Collect go.mod data from all repos."""
    data = {}
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
        data[repo] = json.loads(result.stdout)
    return data


def build_alignment_plan(
    mod_data: dict,
    target_repos: list[str] | None,
    module_prefixes: list[str] | None,
) -> AlignmentPlan:
    """Build a plan to align dependencies across repos.

    Strategy:
    - For each shared module, find the highest version across all repos
    - Generate `go get` commands to bring lagging repos up
    - Flag replace directives that need to be removed
    """
    # Collect versions and replaces
    require_versions: dict[str, dict[str, str]] = defaultdict(dict)
    replace_info: dict[str, dict[str, dict]] = defaultdict(dict)

    for repo, mod in mod_data.items():
        for req in mod.get("Require") or []:
            require_versions[req["Path"]][repo] = req["Version"]
        for rep in mod.get("Replace") or []:
            old = rep["Old"]["Path"]
            new_path = rep["New"]["Path"]
            new_ver = rep["New"].get("Version", "")
            replace_info[old][repo] = {"path": new_path, "version": new_ver}

    actions = []
    replace_removals = []

    for module, repo_versions in sorted(require_versions.items()):
        # Filter by module prefixes if specified
        if module_prefixes and not any(module.startswith(p) for p in module_prefixes):
            continue

        # Need at least 2 repos using this module
        if len(repo_versions) < 2:
            continue

        # Find highest version
        unique_versions = set(repo_versions.values())
        if len(unique_versions) < 2:
            continue  # already aligned

        target_version = max(unique_versions, key=parse_go_version)

        for repo, current_ver in sorted(repo_versions.items()):
            # Filter by target repos if specified
            if target_repos and repo not in target_repos:
                continue

            if current_ver != target_version:
                actions.append(AlignmentAction(
                    repo=repo,
                    module=module,
                    current_version=current_ver,
                    target_version=target_version,
                    action_type="go_get",
                ))

        # Check for downgrading replaces on this module
        if module in replace_info:
            for repo, rep in replace_info[module].items():
                if target_repos and repo not in target_repos:
                    continue
                # Same-module replace that pins to an older version
                if rep["path"] == module and rep["version"]:
                    if parse_go_version(rep["version"]) < parse_go_version(target_version):
                        replace_removals.append(AlignmentAction(
                            repo=repo,
                            module=module,
                            current_version=rep["version"],
                            target_version=target_version,
                            action_type="drop_replace",
                        ))

    return AlignmentPlan(actions=actions, replace_removals=replace_removals)


# --- Execution ---

def apply_plan(repos_dir: Path, plan: AlignmentPlan, dry_run: bool = True) -> list[str]:
    """Apply alignment actions. Returns list of status messages."""
    messages = []

    # Group actions by repo for efficiency
    by_repo: dict[str, list[AlignmentAction]] = defaultdict(list)
    for action in plan.replace_removals + plan.actions:
        by_repo[action.repo].append(action)

    for repo in sorted(by_repo):
        repo_actions = by_repo[repo]
        repo_dir = repos_dir / repo

        # First: drop replaces
        replaces = [a for a in repo_actions if a.action_type == "drop_replace"]
        for action in replaces:
            cmd = ["go", "mod", "edit", "-dropreplace", action.module]
            if dry_run:
                messages.append(f"  [DRY RUN] cd {repo} && {' '.join(cmd)}")
            else:
                result = subprocess.run(cmd, cwd=str(repo_dir), capture_output=True, text=True)
                if result.returncode == 0:
                    messages.append(f"  ✓ {repo}: dropped replace {action.module}")
                else:
                    messages.append(f"  ✗ {repo}: failed to drop replace {action.module}: {result.stderr.strip()}")

        # Then: go get for version bumps
        gets = [a for a in repo_actions if a.action_type == "go_get"]
        if gets:
            # Batch go get for efficiency
            targets = [f"{a.module}@{a.target_version}" for a in gets]
            cmd = ["go", "get"] + targets

            if dry_run:
                messages.append(f"  [DRY RUN] cd {repo} && go get \\")
                for t in targets:
                    messages.append(f"    {t} \\")
            else:
                messages.append(f"  → {repo}: updating {len(targets)} modules...")
                result = subprocess.run(
                    cmd, cwd=str(repo_dir), capture_output=True, text=True, timeout=120,
                )
                if result.returncode == 0:
                    messages.append(f"  ✓ {repo}: updated {len(targets)} modules")
                else:
                    messages.append(f"  ✗ {repo}: go get failed: {result.stderr.strip()[:200]}")

        # Tidy
        if not dry_run and (replaces or gets):
            result = subprocess.run(
                ["go", "mod", "tidy"], cwd=str(repo_dir),
                capture_output=True, text=True, timeout=120,
            )
            if result.returncode == 0:
                messages.append(f"  ✓ {repo}: go mod tidy")
            else:
                messages.append(f"  ⚠ {repo}: go mod tidy had issues: {result.stderr.strip()[:200]}")

    return messages


def verify_builds(repos_dir: Path, repos: list[str]) -> list[str]:
    """Verify repos build after alignment."""
    messages = []
    for repo in sorted(repos):
        repo_dir = repos_dir / repo
        target = "./cmd/..." if (repo_dir / "cmd").exists() else "./..."
        result = subprocess.run(
            ["go", "build", target],
            cwd=str(repo_dir), capture_output=True, text=True,
            env={**os.environ, "GOWORK": "off"},
            timeout=300,
        )
        if result.returncode == 0:
            messages.append(f"  ✓ {repo}: builds OK")
        else:
            lines = result.stderr.strip().splitlines()
            messages.append(f"  ✗ {repo}: build failed — {lines[-1][:200] if lines else 'unknown error'}")
    return messages


# --- Output ---

def _c(code: str, text: str) -> str:
    colors = {
        "red": "\033[0;31m", "green": "\033[0;32m", "yellow": "\033[0;33m",
        "cyan": "\033[0;36m", "bold": "\033[1m", "dim": "\033[2m", "reset": "\033[0m",
    }
    return f"{colors.get(code, '')}{text}{colors['reset']}"


def render_plan(plan: AlignmentPlan) -> str:
    lines = [
        "",
        _c("bold", "═" * 55),
        _c("bold", "  Tekton Dependency Alignment Plan"),
        _c("bold", "═" * 55),
        "",
    ]

    if plan.replace_removals:
        lines.append(_c("bold", "── Replace Directives to Remove ──"))
        lines.append("")
        for a in plan.replace_removals:
            lines.append(f"  {_c('yellow', '⚠')} {_c('bold', a.repo)}: {a.module}")
            lines.append(f"    replace pins: {_c('red', a.current_version)}")
            lines.append(f"    others need:  {_c('green', a.target_version)}")
        lines.append("")

    if plan.actions:
        # Group by module for readability
        by_module: dict[str, list[AlignmentAction]] = defaultdict(list)
        for a in plan.actions:
            by_module[a.module].append(a)

        lines.append(_c("bold", f"── Version Bumps ({len(plan.actions)} updates across "
                        f"{len(plan.repos_affected)} repos) ──"))
        lines.append("")

        for module in sorted(by_module):
            actions = by_module[module]
            target = actions[0].target_version
            lines.append(f"  {_c('cyan', module)} → {_c('green', target)}")
            for a in sorted(actions, key=lambda x: x.repo):
                lines.append(f"    {a.repo:<25} {_c('red', a.current_version)}")
        lines.append("")

    if not plan.actions and not plan.replace_removals:
        lines.append(_c("green", "  ✓ All dependencies are aligned!"))
        lines.append("")

    lines.append(_c("bold", "── Summary ──"))
    lines.append(f"  Version bumps:     {len(plan.actions)}")
    lines.append(f"  Replace removals:  {len(plan.replace_removals)}")
    lines.append(f"  Repos affected:    {', '.join(sorted(plan.repos_affected)) or 'none'}")
    lines.append("")
    if plan.actions or plan.replace_removals:
        lines.append(f"  {_c('cyan', 'Run with --apply to execute these changes')}")
        lines.append("")

    return "\n".join(lines)


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("repos", nargs="*", help="Repos to align (default: all behind repos)")
    parser.add_argument("--repos-dir", type=Path, default=None)
    parser.add_argument("--group", choices=list(MODULE_GROUPS) + ["all"],
                        default="all", help="Module group to align (default: all)")
    parser.add_argument("--apply", action="store_true", help="Actually run go get commands")
    parser.add_argument("--verify", action="store_true", help="Verify builds after alignment")
    args = parser.parse_args()

    repos_dir = (args.repos_dir or Path(__file__).resolve().parent.parent).resolve()

    # Determine module prefixes to check
    if args.group == "all":
        # Use all known important prefixes
        module_prefixes = []
        for group_mods in MODULE_GROUPS.values():
            module_prefixes.extend(group_mods)
    else:
        module_prefixes = MODULE_GROUPS[args.group]

    # Find available repos
    available = [r for r in ALL_REPOS if (repos_dir / r / "go.mod").exists()]
    if not available:
        print(f"No Tekton repos found in {repos_dir}", file=sys.stderr)
        sys.exit(1)

    target_repos = args.repos if args.repos else None

    # Collect and analyze
    print(f"Scanning {len(available)} repos in {repos_dir}...", file=sys.stderr)
    mod_data = collect_mod_data(repos_dir, available)
    plan = build_alignment_plan(mod_data, target_repos, module_prefixes)

    # Show plan
    print(render_plan(plan))

    if not args.apply:
        return

    # Apply
    print(_c("bold", "── Applying Changes ──"))
    print()
    messages = apply_plan(repos_dir, plan, dry_run=False)
    for msg in messages:
        print(msg)
    print()

    # Verify
    if args.verify:
        print(_c("bold", "── Verifying Builds ──"))
        print()
        affected = sorted(plan.repos_affected)
        messages = verify_builds(repos_dir, affected)
        for msg in messages:
            print(msg)
        print()


if __name__ == "__main__":
    main()
