#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "packaging",
# ]
# ///
"""
Generate a Dependency Alignment Report.

Applies alignment in a workspace, collects per-repo go.mod diffs,
and outputs a markdown report suitable for a GitHub issue.

Usage:
    ./hack/alignment-report.py                        # all repos except operator
    ./hack/alignment-report.py --repos-dir ./repos    # custom location
    ./hack/alignment-report.py --include-operator      # include operator too
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ALL_REPOS = [
    "pipeline", "triggers", "chains", "cli", "results",
    "pipelines-as-code", "dashboard", "plumbing", "pruner",
]

SKIP_REPOS = ["operator"]  # excluded by default due to replace issues

GITHUB_ORG = "tektoncd"


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)


# --- Existing PR detection ---

def find_existing_prs(repos: list[str], modules_by_repo: dict[str, list[str]]) -> dict[str, list[dict]]:
    """Find open PRs that already bump needed modules.

    Returns {repo: [{title, url, modules_bumped}]}.
    """
    results: dict[str, list[dict]] = {}

    for repo in repos:
        needed_modules = set(modules_by_repo.get(repo, []))
        if not needed_modules:
            continue

        # Search for open dependency PRs
        r = run([
            "gh", "pr", "list",
            "-R", f"{GITHUB_ORG}/{repo}",
            "--json", "title,url,body,labels",
            "--search", "bump is:open",
            "--limit", "30",
        ])
        if r.returncode != 0:
            continue

        try:
            prs = json.loads(r.stdout)
        except json.JSONDecodeError:
            continue

        matching = []
        for pr in prs:
            title = pr.get("title", "")
            body = pr.get("body", "") or ""
            text = f"{title} {body}"

            # Check which needed modules this PR bumps
            bumped = [m for m in needed_modules if m in text]
            if bumped:
                matching.append({
                    "title": title,
                    "url": pr.get("url", ""),
                    "modules": bumped,
                })

        if matching:
            results[repo] = matching

    return results


def get_go_mod_diff(repos_dir: Path, repo: str) -> str | None:
    """Get go.mod diff for a repo."""
    r = run(["git", "diff", "go.mod"], cwd=str(repos_dir / repo))
    return r.stdout.strip() if r.stdout.strip() else None


def get_diff_stat(repos_dir: Path, repo: str) -> str:
    """Get diff stat for a repo."""
    r = run(["git", "diff", "--stat"], cwd=str(repos_dir / repo))
    lines = r.stdout.strip().splitlines()
    return lines[-1].strip() if lines else "no changes"


def count_direct_changes(repos_dir: Path, repo: str) -> int:
    """Count direct dependency version changes in go.mod."""
    r = run(["git", "diff", "go.mod"], cwd=str(repos_dir / repo))
    # Count lines that change a version and aren't indirect
    count = 0
    for line in r.stdout.splitlines():
        if line.startswith(("+\t", "-\t")) and "// indirect" not in line:
            count += 1
    return count // 2  # +/- pairs


def reset_repo(repos_dir: Path, repo: str) -> None:
    run(["git", "checkout", "."], cwd=str(repos_dir / repo))
    run(["git", "clean", "-fd"], cwd=str(repos_dir / repo))


def apply_alignment(repos_dir: Path, repos: list[str]) -> dict[str, dict]:
    """Run align-deps and collect results per repo."""
    script = Path(__file__).resolve().parent / "align-deps.py"

    # Run alignment
    r = run(
        [sys.executable, str(script), "--repos-dir", str(repos_dir), "--apply"] + repos,
        timeout=300,
    )
    print(r.stdout, file=sys.stderr)
    if r.stderr:
        print(r.stderr, file=sys.stderr)

    # Collect diffs and extract changed modules
    results = {}
    for repo in repos:
        diff = get_go_mod_diff(repos_dir, repo)
        changed_modules = []
        if diff:
            # Extract module paths from +/- lines in go.mod diff
            for line in diff.splitlines():
                if line.startswith(("+\t", "-\t")) and not line.startswith(("+++", "---")):
                    m = re.match(r"[+-]\t(\S+)\s+v", line)
                    if m:
                        changed_modules.append(m.group(1))
            changed_modules = sorted(set(changed_modules))

        results[repo] = {
            "has_changes": diff is not None,
            "diff": diff,
            "stat": get_diff_stat(repos_dir, repo) if diff else "no changes",
            "direct_count": count_direct_changes(repos_dir, repo) if diff else 0,
            "changed_modules": changed_modules,
        }
    return results


def verify_builds(repos_dir: Path, repos: list[str]) -> dict[str, dict]:
    """Build each repo standalone and report results."""
    results = {}
    for repo in repos:
        repo_dir = repos_dir / repo

        # Vendor if needed
        if (repo_dir / "vendor").exists():
            vr = run(["go", "mod", "vendor"], cwd=str(repo_dir), timeout=300)
            if vr.returncode != 0:
                results[repo] = {"success": False, "error": f"vendor failed: {vr.stderr.strip().splitlines()[-1][:200]}"}
                continue

        target = "./cmd/..." if (repo_dir / "cmd").exists() else "./..."
        r = run(
            ["go", "build", target],
            cwd=str(repo_dir), timeout=300,
            env={**__import__("os").environ, "GOWORK": "off"},
        )
        if r.returncode == 0:
            results[repo] = {"success": True}
        else:
            last = r.stderr.strip().splitlines()[-1][:200] if r.stderr.strip() else "unknown"
            results[repo] = {"success": False, "error": last}

    return results


def render_report(
    repos: list[str],
    alignment: dict[str, dict],
    build_results: dict[str, dict],
    existing_prs: dict[str, list[dict]],
    skipped: list[str],
) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "## 🔧 Dependency Alignment — go.mod changes needed per repo",
        "",
        f"**Generated:** {ts}",
        "",
        "After running `align-deps.py --apply`, here's what changed in each repo. "
        "These are purely `go.mod` + `go.sum` updates — **no source code changes needed** "
        "(unless a repo has upstream API breaks).",
        "",
        "### Summary",
        "",
        "| Repo | Direct Deps Changed | Stat | Build | Status |",
        "|------|-------------------|------|-------|--------|",
    ]

    for repo in repos:
        a = alignment.get(repo, {})
        b = build_results.get(repo, {})
        if not a.get("has_changes"):
            lines.append(f"| {repo} | 0 | no changes | — | ✅ already aligned |")
        else:
            build_icon = "✅" if b.get("success") else "❌"
            build_text = "builds" if b.get("success") else b.get("error", "failed")[:60]
            lines.append(f"| {repo} | {a['direct_count']} | {a['stat']} | {build_icon} {build_text} | 🔧 needs update |")

    if skipped:
        for repo in skipped:
            lines.append(f"| {repo} | — | — | — | ⏳ skipped ([PR #3332](https://github.com/tektoncd/operator/pull/3332)) |")

    lines += ["", "### Per-Repo Diffs (`go.mod`)", ""]

    for repo in repos:
        a = alignment.get(repo, {})
        if a.get("diff"):
            lines += [
                "<details>",
                f"<summary><b>{repo}</b> — {a['direct_count']} direct deps, {a['stat']}</summary>",
                "",
                "```diff",
                a["diff"],
                "```",
                "</details>",
                "",
            ]

    # Existing PRs that already address some of these bumps
    if existing_prs:
        lines += [
            "### 🔄 Existing PRs Already In Flight",
            "",
            "These open PRs already bump some of the needed dependencies:",
            "",
        ]
        for repo in sorted(existing_prs):
            lines.append(f"**{repo}**")
            for pr in existing_prs[repo]:
                mods = ", ".join(f"`{m}`" for m in pr["modules"][:5])
                extra = f" (+{len(pr['modules']) - 5} more)" if len(pr["modules"]) > 5 else ""
                lines.append(f"- [{pr['title']}]({pr['url']}) — bumps {mods}{extra}")
            lines.append("")

    # Build failures
    failed = {r: b for r, b in build_results.items() if not b.get("success")}
    if failed:
        lines += [
            "### ❌ Build Failures After Alignment",
            "",
            "These repos need code changes beyond `go.mod` updates:",
            "",
        ]
        for repo, b in sorted(failed.items()):
            lines.append(f"- **{repo}**: `{b.get('error', 'unknown')}`")
        lines.append("")

    lines += [
        "### How to Reproduce",
        "",
        "```bash",
        "git clone https://github.com/vdemeester/tekton-workspace.git",
        "cd tekton-workspace",
        "./hack/setup-workspace.sh --all",
        "",
        "# Dry-run (see plan)",
        f"./hack/align-deps.py {' '.join(repos)}",
        "",
        "# Apply and verify",
        f"./hack/align-deps.py {' '.join(repos)} --apply --verify",
        "```",
        "",
        "---",
        "*Generated by [`alignment-report.py`](../blob/main/hack/alignment-report.py) — "
        "run locally or via [weekly CI](../blob/main/.github/workflows/alignment-report.yaml)*",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repos-dir", type=Path, default=None)
    parser.add_argument("--include-operator", action="store_true")
    parser.add_argument("--output", "-o", type=Path)
    parser.add_argument("--verify", action="store_true", default=True,
                        help="Verify builds after alignment (default: true)")
    parser.add_argument("--no-verify", action="store_false", dest="verify")
    args = parser.parse_args()

    repos_dir = (args.repos_dir or Path(__file__).resolve().parent.parent).resolve()

    repos = list(ALL_REPOS)
    skipped = list(SKIP_REPOS)
    if args.include_operator:
        repos.append("operator")
        skipped = []

    # Filter to repos that exist
    repos = [r for r in repos if (repos_dir / r / "go.mod").exists()]
    if not repos:
        print(f"No repos found in {repos_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Aligning {len(repos)} repos (skipping: {', '.join(skipped) or 'none'})...", file=sys.stderr)

    # 1. Apply alignment
    alignment = apply_alignment(repos_dir, repos)

    # 2. Verify builds
    build_results = {}
    if args.verify:
        changed_repos = [r for r in repos if alignment.get(r, {}).get("has_changes")]
        if changed_repos:
            print(f"Verifying builds for {len(changed_repos)} changed repos...", file=sys.stderr)
            build_results = verify_builds(repos_dir, changed_repos)

    # 3. Find existing PRs that already bump needed modules
    modules_by_repo = {
        r: a.get("changed_modules", [])
        for r, a in alignment.items()
        if a.get("has_changes")
    }
    print(f"Checking for existing PRs in {len(modules_by_repo)} repos...", file=sys.stderr)
    existing_prs = find_existing_prs(list(modules_by_repo.keys()), modules_by_repo)
    if existing_prs:
        total = sum(len(prs) for prs in existing_prs.values())
        print(f"Found {total} existing PRs across {len(existing_prs)} repos", file=sys.stderr)

    # 4. Generate report
    report = render_report(repos, alignment, build_results, existing_prs, skipped)

    if args.output:
        args.output.write_text(report)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(report)

    # 5. Reset repos to clean state
    print("Resetting repos...", file=sys.stderr)
    for repo in repos:
        reset_repo(repos_dir, repo)


if __name__ == "__main__":
    main()
