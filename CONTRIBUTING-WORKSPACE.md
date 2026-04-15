# Working with Go Workspaces for Tekton Development

Go workspaces (`go.work`, Go 1.18+) let you work on multiple Tekton
repositories simultaneously without `replace` directives in `go.mod`. This is
especially useful when a change spans multiple repos (e.g., adding an API in
`pipeline` and consuming it in `triggers` and `cli`).

## Quick Start

```bash
# From within the workspace-exp directory (or wherever you keep your workspace)
./hack/setup-workspace.sh pipeline triggers cli
```

This clones any missing repos and generates a `go.work` file. That's it — Go
and your IDE will now resolve cross-repo imports from your local checkouts.

## How It Works

A `go.work` file tells the Go toolchain to prefer local module directories over
downloaded versions:

```go
go 1.25.7

use (
    ../pipeline
    ../triggers
    ../cli
)
```

When you `go build` or `go test` any of these modules, imports like
`github.com/tektoncd/pipeline` resolve to `../pipeline` instead of fetching a
tagged release. This means:

- **No `replace` directives needed** — edit code in `pipeline`, and `triggers`
  picks it up instantly
- **Full IDE support** — go-to-definition, find-references, and refactoring work
  across all repos in the workspace
- **Local integration testing** — catch breakage before pushing

## Common Workflows

### Cross-repo API change

You need to change a type in `pipeline` and update `chains` + `cli`:

```bash
# Set up workspace with the repos you need
./hack/setup-workspace.sh pipeline chains cli

# Make your changes in pipeline
$EDITOR ../pipeline/pkg/apis/pipeline/v1/types.go

# Verify chains still builds
go build ../chains/...

# Fix chains, then verify cli
$EDITOR ../chains/pkg/...
go build ../cli/...

# Run tests across everything
go test ../pipeline/... ../chains/... ../cli/...
```

Submit PRs to each repo. The `pipeline` PR merges first, gets tagged, then
`chains` and `cli` PRs update their `go.mod` to point at the new tag.

### "Does my change break downstream?"

```bash
# Edit pipeline
$EDITOR ../pipeline/pkg/reconciler/...

# Quick check across all downstream consumers
go build ../triggers/... ../chains/... ../cli/... ../operator/...
```

### Sync dependency versions

```bash
# See if repos have drifted on shared dependency versions
go work sync
```

This updates each module's `go.mod` to use consistent dependency versions. Use
with care — review the diff before committing.

### Adding/removing repos from your workspace

```bash
# Add a repo
go work use ../results

# Remove a repo (edit go.work or)
go work edit -dropuse ../results
```

## Tekton Dependency Graph

Understanding the dependency order helps plan multi-repo changes:

```
plumbing (shared build/test utilities)
    ↑
pipeline (core — most repos depend on this)
    ↑
  ┌─┴──────────┬────────────┬──────────────────┐
triggers    chains    pipelines-as-code    dashboard
    ↑         ↑
  ┌─┴─────────┘
 cli
  ↑
results
  ↑
operator (depends on pipeline, triggers, results, pruner)
```

## Setup Options

```bash
# Auto-detect: use whatever Tekton repos you already have cloned
./hack/setup-workspace.sh

# Specific repos only
./hack/setup-workspace.sh pipeline triggers

# Everything
./hack/setup-workspace.sh --all
```

## Important Notes

| Topic | Details |
|-------|---------|
| **Local only** | `go.work` and `go.work.sum` are for your machine. Never commit them to Tekton repos. Each repo's `.gitignore` should include `go.work*`. |
| **CI is unaffected** | CI builds each repo independently using `go.mod`. The workspace doesn't change CI behavior. |
| **`go.mod` is still source of truth** | When submitting PRs, each repo's `go.mod` must reference real published versions/tags, not local paths. |
| **Version mismatches** | Your local pipeline code may be ahead of what `triggers` expects. Build errors are expected and useful — they tell you what to update. |
| **`GOWORK=off`** | To temporarily disable the workspace: `GOWORK=off go build ./...` |

## IDE Setup

### VS Code
Open the workspace-exp directory (or the parent `tektoncd/` directory). The Go
extension auto-detects `go.work` and provides cross-repo navigation.

### GoLand
Open the directory containing `go.work`. GoLand natively supports workspaces
since 2022.1.

### Emacs (lsp-mode / eglot)
Point your project root at the directory containing `go.work`. `gopls`
auto-detects it.

## Known Dependency Conflicts

Not all Tekton repos can coexist in the same workspace today due to version
skew on shared dependencies. The main culprits:

| Dependency | Repos on latest | Repos lagging |
|---|---|---|
| `k8s.io/api` | pipeline, chains, pac, dashboard (0.35.x) | triggers, hub (0.32.x), cli, results (0.34.x) |
| `knative.dev/pkg` | pipeline, chains, pac | operator (has `replace` pinning older version) |

**Working combinations** (tested):
- `pipeline` + `chains` + `pipelines-as-code` + `dashboard` ✅
- Adding `operator` → knative.dev/pkg replace conflict ❌
- Adding `triggers` → k8s.io/api version conflict ❌

As repos update their dependencies, more combinations become possible. This is
actually a **feature** of workspaces — it makes dependency drift visible and
creates pressure to keep versions aligned.

To work around conflicts temporarily:
```bash
# Drop the conflicting repo
go work edit -dropuse ../operator

# Or work with just two repos
go work edit -dropuse ../dashboard -dropuse ../chains
```

## Detecting & Fixing Dependency Drift

The `hack/dependency-drift.py` script scans all local Tekton repos and reports
version skew on shared dependencies. It uses a
[uv script shebang](https://docs.astral.sh/uv/guides/scripts/) so it
self-installs its dependencies — just run it directly:

```bash
# Full report across all repos (terminal output with colors)
./hack/dependency-drift.py

# Focus on k8s deps
./hack/dependency-drift.py --modules k8s.io/api,k8s.io/client-go

# Generate `go get` commands to align everything to latest
./hack/dependency-drift.py --fix

# GitHub-flavored markdown (what the CI issue looks like)
./hack/dependency-drift.py --format markdown --fix

# Machine-readable output (for automation)
./hack/dependency-drift.py --format json
```

The report shows:
- **Go version skew** across repos
- **Drifted dependencies** — same module at different versions
- **Replace directive conflicts** — repos with incompatible `replace` in `go.mod`
- **Fix commands** — exact `go get` commands to align lagging repos

This is useful both for local development (understanding why a workspace
combination fails) and for project-wide maintenance (coordinating dependency
bumps across repos instead of letting Dependabot drift them apart).

## Troubleshooting

**"conflicting replacements" errors**
- Two repos have `replace` directives pointing the same module to different
  versions. Remove one repo from the workspace, or add a workspace-level
  replace: `go work edit -replace k8s.io/api=k8s.io/api@v0.35.3`

**"module not found" errors**
- Verify the repo is cloned and the path in `go.work` is correct
- Run `go work sync` to refresh

**Unexpected version of a dependency**
- `GOWORK=off go list -m all` shows what CI would use (go.mod only)
- `go list -m all` shows what the workspace resolves

**Want to test with the released version, not local**
- Remove the repo from `go.work`: `go work edit -dropuse ../pipeline`
- Or disable entirely: `GOWORK=off go test ./...`
