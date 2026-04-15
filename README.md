# Tekton Workspace

> ⚠️ **Experiment** — Exploring Go workspaces and cross-repo tooling for the
> Tekton project.

Tekton is split across many repositories (`pipeline`, `triggers`, `chains`,
`cli`, `results`, `operator`, `pipelines-as-code`, `dashboard`, `plumbing`,
`pruner`) that depend on each other. This makes cross-repo development
painful — changing an API in `pipeline` means juggling `replace` directives,
waiting for tags, and hoping nothing drifts apart.

This repo experiments with [Go workspaces](https://go.dev/doc/tutorial/workspaces)
and tooling to make it easier for contributors to:

- **Work on multiple components simultaneously** — edit `pipeline` and `cli`
  together, with full IDE support and cross-repo go-to-definition
- **Detect dependency drift** — find where repos have diverged on shared
  dependencies like `k8s.io/*`, `knative.dev/pkg`, and each other
- **Catch breaking changes early** — actually build repos together and surface
  API breaks before they become release blockers
- **Automate dependency alignment** — generate the exact `go get` commands to
  bring lagging repos up to date

## Quick Start

```bash
git clone https://github.com/vdemeester/tekton-workspace.git
cd tekton-workspace

# Clone all Tekton repos and generate a go.work
./hack/setup-workspace.sh --all

# Or just the repos you need
./hack/setup-workspace.sh pipeline cli triggers
```

That's it. Go and your IDE will resolve cross-repo imports from local checkouts.

```bash
# Build cli against your local pipeline changes
go build ./cli/cmd/...

# Test triggers with local pipeline
go test ./triggers/...

# Full IDE support — open this directory in VS Code, GoLand, or Emacs
```

## Drift Detection

Find where repos have diverged on shared dependencies:

```bash
# Full report
./hack/dependency-drift.py

# Focus on k8s deps
./hack/dependency-drift.py --modules k8s.io/api,k8s.io/client-go

# Show exact commands to align repos to latest versions
./hack/dependency-drift.py --fix

# GitHub-flavored markdown (what the CI issue looks like)
./hack/dependency-drift.py --format markdown --fix
```

## Workspace Compatibility Check

Actually build repos together and catch real breakage:

```bash
# Build all repos in a workspace, report what breaks
./hack/workspace-check.py

# Specific repos
./hack/workspace-check.py pipeline cli triggers

# Markdown report
./hack/workspace-check.py --format markdown
```

This catches two categories of problems that static analysis misses:

1. **Conflicting `replace` directives** — two repos pin the same module to
   different versions (e.g., `operator` and `pruner` both replace `k8s.io/*`
   but to different targets)
2. **Breaking API changes** — a repo builds fine standalone but breaks when
   Go's MVS selects a newer dependency version from another repo in the
   workspace (e.g., `knative.dev/pkg` removed the `metrics` package)

## CI Workflows

Two GitHub Actions run weekly and create/update issues:

| Workflow | Schedule | Issue Label | What it does |
|----------|----------|-------------|-------------|
| `dependency-drift.yaml` | Monday 8:00 UTC | `dependency-drift` | Version skew report across all repos |
| `workspace-check.yaml` | Monday 9:00 UTC | `workspace-compat` | Build compatibility matrix |

## Sample Reports

See what the CI issues look like:

- [Sample Drift Report](sample-drift-issue.md)
- [Sample Workspace Check](sample-workspace-check.md)
- [Live gist](https://gist.github.com/vdemeester/c98466533851d4239c3b951567caf46c)

## What's Next

- [ ] Automated PRs to align dependencies across repos
- [ ] Integration with Tekton release process
- [ ] Workspace compatibility as a merge gate
- [ ] Reduce/eliminate `replace` directives in repos

## Contributing

See [CONTRIBUTING-WORKSPACE.md](CONTRIBUTING-WORKSPACE.md) for detailed
contributor documentation on using Go workspaces with Tekton.
