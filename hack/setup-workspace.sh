#!/usr/bin/env bash
# setup-workspace.sh — Set up a Go workspace for Tekton multi-repo development
#
# Usage:
#   ./hack/setup-workspace.sh [options] [repo1 repo2 ...]
#
# Options:
#   --dir DIR         Directory for repo checkouts (default: repository root)
#   --all             Include all known Tekton repos
#   -h, --help        Show this help
#
# Examples:
#   ./hack/setup-workspace.sh --all                     # clone & set up everything
#   ./hack/setup-workspace.sh pipeline triggers cli      # specific repos
#   ./hack/setup-workspace.sh                            # auto-detect existing clones

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

ALL_REPOS=(
    plumbing
    pipeline
    triggers
    chains
    cli
    results
    operator
    pipelines-as-code
    dashboard
    pruner
)

GITHUB_ORG="https://github.com/tektoncd"

usage() {
    sed -n '2,/^$/s/^# //p' "$0"
    exit "${1:-0}"
}

clone_if_missing() {
    local repo="$1"
    local target="$REPOS_DIR/$repo"
    if [[ -d "$target" ]]; then
        echo "  ✓ $repo (exists)"
    else
        echo "  ⬇ Cloning $repo..."
        git clone --quiet "$GITHUB_ORG/$repo.git" "$target"
        echo "  ✓ $repo (cloned)"
    fi
}

generate_go_work() {
    local repos=("$@")
    local go_work="$REPOS_DIR/go.work"
    local go_version

    # Use the highest Go version found across repos
    go_version=$(for r in "${repos[@]}"; do
        grep '^go ' "$REPOS_DIR/$r/go.mod" 2>/dev/null | awk '{print $2}'
    done | sort -V | tail -1)

    cat > "$go_work" <<EOF
go ${go_version}

use (
EOF
    for repo in "${repos[@]}"; do
        echo "	./$repo" >> "$go_work"
    done
    echo ")" >> "$go_work"

    echo ""
    echo "Generated $go_work"
}

# --- Parse args ---

REPOS_DIR="$REPO_ROOT"
selected_repos=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dir)
            REPOS_DIR="$(cd "$2" 2>/dev/null && pwd || echo "$2")"
            shift 2 ;;
        --all)
            selected_repos=("${ALL_REPOS[@]}")
            shift ;;
        -h|--help)
            usage 0 ;;
        -*)
            echo "Unknown option: $1" >&2
            usage 1 ;;
        *)
            selected_repos+=("$1")
            shift ;;
    esac
done

# Auto-detect if no repos specified
if [[ ${#selected_repos[@]} -eq 0 ]]; then
    echo "Auto-detecting Tekton repos in $REPOS_DIR..."
    for repo in "${ALL_REPOS[@]}"; do
        if [[ -f "$REPOS_DIR/$repo/go.mod" ]]; then
            selected_repos+=("$repo")
        fi
    done
    if [[ ${#selected_repos[@]} -eq 0 ]]; then
        echo "No Tekton repos found in $REPOS_DIR."
        echo "Use --all to clone them, or specify repos."
        exit 1
    fi
    echo "Found ${#selected_repos[@]} repos: ${selected_repos[*]}"
fi

# --- Main ---

mkdir -p "$REPOS_DIR"
echo ""
echo "Setting up workspace in: $REPOS_DIR"
echo "Repos: ${selected_repos[*]}"
echo ""

# Clone missing repos
for repo in "${selected_repos[@]}"; do
    clone_if_missing "$repo"
done

# Generate go.work
generate_go_work "${selected_repos[@]}"

echo ""
echo "Done! You can now:"
echo "  cd $REPOS_DIR"
echo "  go build ./pipeline/...            # build pipeline with local deps"
echo "  go test ./triggers/...             # test triggers against local pipeline"
echo "  go work sync                       # sync dependency versions"
echo ""
echo "Your IDE will resolve cross-repo imports automatically."
