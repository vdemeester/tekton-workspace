## 🔨 Tekton Workspace Compatibility Check

**Generated:** 2026-04-15 08:37 UTC  
**Repos checked:** 10

| Metric | Result |
|--------|--------|
| Build in workspace | 🔴 1/10 repos |
| Replace conflicts | 🔴 5 |

### Build Results

| Repo | Status | Issue |
|------|--------|-------|
| plumbing | ✅ builds | — |
| chains | ❌ Missing Module | Missing 1 package(s): `gocloud.dev/docstore/awsdynamodb` |
| cli | ❌ API Break | 2 compilation error(s) |
| dashboard | ❌ API Break | 1 compilation error(s) |
| operator | ❌ Replace Conflict | Excluded from workspace — conflicting replaces for `k8s.io/api`, `k8s.io/apimachinery`, `k8s.io/client-go`, `k8s.io/code-generator`, `k8s.io/kube-openapi` |
| pipeline | ❌ API Break | 2 compilation error(s) |
| pipelines-as-code | ❌ API Break | 2 compilation error(s) |
| pruner | ❌ API Break | 2 compilation error(s) |
| results | ❌ Missing Module | Missing 1 package(s): `knative.dev/pkg/metrics` |
| triggers | ❌ Missing Module | Missing 1 package(s): `knative.dev/pkg/metrics` |

### ⚠️ Replace Directive Conflicts

Repos with conflicting `replace` directives cannot coexist in a `go.work`.
The Go team [recommends avoiding replace directives](https://go.dev/ref/mod#go-mod-file-replace) 
in libraries. Consider removing them and updating dependencies instead.

**`k8s.io/api`**
| Repo | Replace Target |
|------|---------------|
| operator | `k8s.io/api v0.32.4` |
| pruner | `k8s.io/api v0.33.1` |

**`k8s.io/apimachinery`**
| Repo | Replace Target |
|------|---------------|
| operator | `k8s.io/apimachinery v0.32.4` |
| pruner | `k8s.io/apimachinery v0.33.1` |

**`k8s.io/client-go`**
| Repo | Replace Target |
|------|---------------|
| operator | `k8s.io/client-go v0.32.4` |
| pruner | `k8s.io/client-go v0.33.1` |

**`k8s.io/code-generator`**
| Repo | Replace Target |
|------|---------------|
| operator | `k8s.io/code-generator v0.32.4` |
| pruner | `k8s.io/code-generator v0.33.1` |

**`k8s.io/kube-openapi`**
| Repo | Replace Target |
|------|---------------|
| operator | `k8s.io/kube-openapi v0.0.0-20250627150254-e9823e99808e` |
| pruner | `k8s.io/kube-openapi v0.0.0-20250318190949-c8a335a9a2ff` |

<details>
<summary><b>How to fix replace conflicts</b></summary>

Replace directives pin a dependency to a specific version, overriding MVS.
When two repos replace the same module to different versions, Go cannot resolve it.

**Options:**
1. **Remove the replace** — update the code to work with the version MVS selects
2. **Align the replace** — make both repos point to the same version
3. **Upgrade past the need** — often replaces exist for old compatibility; upgrading deps may eliminate them

For `k8s.io/api`:
```bash
# In operator/go.mod — consider removing this replace:
#   replace k8s.io/api => k8s.io/api v0.32.4
# In pruner/go.mod — consider removing this replace:
#   replace k8s.io/api => k8s.io/api v0.33.1
```

For `k8s.io/apimachinery`:
```bash
# In operator/go.mod — consider removing this replace:
#   replace k8s.io/apimachinery => k8s.io/apimachinery v0.32.4
# In pruner/go.mod — consider removing this replace:
#   replace k8s.io/apimachinery => k8s.io/apimachinery v0.33.1
```

For `k8s.io/client-go`:
```bash
# In operator/go.mod — consider removing this replace:
#   replace k8s.io/client-go => k8s.io/client-go v0.32.4
# In pruner/go.mod — consider removing this replace:
#   replace k8s.io/client-go => k8s.io/client-go v0.33.1
```

For `k8s.io/code-generator`:
```bash
# In operator/go.mod — consider removing this replace:
#   replace k8s.io/code-generator => k8s.io/code-generator v0.32.4
# In pruner/go.mod — consider removing this replace:
#   replace k8s.io/code-generator => k8s.io/code-generator v0.33.1
```

For `k8s.io/kube-openapi`:
```bash
# In operator/go.mod — consider removing this replace:
#   replace k8s.io/kube-openapi => k8s.io/kube-openapi v0.0.0-20250627150254-e9823e99808e
# In pruner/go.mod — consider removing this replace:
#   replace k8s.io/kube-openapi => k8s.io/kube-openapi v0.0.0-20250318190949-c8a335a9a2ff
```

</details>

### 🔥 Breaking Changes from Dependency Upgrades

These repos build fine standalone (`GOWORK=off go build ./...`) but break in the 
workspace because Go's MVS selects a newer dependency version that has breaking changes.

This is **real drift** — it means these repos are relying on APIs from older dependency 
versions that have since changed. Fixing these makes the codebase more maintainable and 
unblocks workspace-based development.

<details>
<summary><b>chains</b> — Missing 1 package(s): `gocloud.dev/docstore/awsdynamodb`</summary>

```
pkg/chains/storage/docdb/docdb.go:30:2: no required module provides package gocloud.dev/docstore/awsdynamodb; to add it:
```

**How to fix:** Update the repo to use the newer dependency API:
```bash
cd chains
# Add missing dependencies:
go get gocloud.dev/docstore/awsdynamodb
```
</details>

<details>
<summary><b>cli</b> — 2 compilation error(s)</summary>

```
../../../.local/share/go/pkg/mod/k8s.io/kube-openapi@v0.0.0-20250318190949-c8a335a9a2ff/pkg/util/proto/document_v3.go:291:31: cannot use s.GetDefault().ToRawInfo() (value of type *"go.yaml.in/yaml/v3".Node) as *"gopkg.in/yaml.v3".Node value in argument to parseV3Interface
../../../.local/share/go/pkg/mod/knative.dev/pkg@v0.0.0-20260406140200-cb58ae50e894/apis/duck/typed.go:62:14: undefined: cache.ToListWatcherWithWatchListSemantics
```

**How to fix:** Update the repo to use the newer dependency API:
```bash
cd cli
# Update deps and fix compilation errors:
go get -u ./...
go build ./...
```
</details>

<details>
<summary><b>dashboard</b> — 1 compilation error(s)</summary>

```
../../../.local/share/go/pkg/mod/k8s.io/kube-openapi@v0.0.0-20250318190949-c8a335a9a2ff/pkg/util/proto/document_v3.go:291:31: cannot use s.GetDefault().ToRawInfo() (value of type *"go.yaml.in/yaml/v3".Node) as *"gopkg.in/yaml.v3".Node value in argument to parseV3Interface
```

**How to fix:** Update the repo to use the newer dependency API:
```bash
cd dashboard
# Update deps and fix compilation errors:
go get -u ./...
go build ./...
```
</details>

<details>
<summary><b>pipeline</b> — 2 compilation error(s)</summary>

```
../../../.local/share/go/pkg/mod/k8s.io/kube-openapi@v0.0.0-20250318190949-c8a335a9a2ff/pkg/util/proto/document_v3.go:291:31: cannot use s.GetDefault().ToRawInfo() (value of type *"go.yaml.in/yaml/v3".Node) as *"gopkg.in/yaml.v3".Node value in argument to parseV3Interface
../../../.local/share/go/pkg/mod/knative.dev/pkg@v0.0.0-20260406140200-cb58ae50e894/apis/duck/typed.go:62:14: undefined: cache.ToListWatcherWithWatchListSemantics
```

**How to fix:** Update the repo to use the newer dependency API:
```bash
cd pipeline
# Update deps and fix compilation errors:
go get -u ./...
go build ./...
```
</details>

<details>
<summary><b>pipelines-as-code</b> — 2 compilation error(s)</summary>

```
../../../.local/share/go/pkg/mod/k8s.io/kube-openapi@v0.0.0-20250318190949-c8a335a9a2ff/pkg/util/proto/document_v3.go:291:31: cannot use s.GetDefault().ToRawInfo() (value of type *"go.yaml.in/yaml/v3".Node) as *"gopkg.in/yaml.v3".Node value in argument to parseV3Interface
../../../.local/share/go/pkg/mod/knative.dev/pkg@v0.0.0-20260406140200-cb58ae50e894/apis/duck/typed.go:62:14: undefined: cache.ToListWatcherWithWatchListSemantics
```

**How to fix:** Update the repo to use the newer dependency API:
```bash
cd pipelines-as-code
# Update deps and fix compilation errors:
go get -u ./...
go build ./...
```
</details>

<details>
<summary><b>pruner</b> — 2 compilation error(s)</summary>

```
../../../.local/share/go/pkg/mod/k8s.io/kube-openapi@v0.0.0-20250318190949-c8a335a9a2ff/pkg/util/proto/document_v3.go:291:31: cannot use s.GetDefault().ToRawInfo() (value of type *"go.yaml.in/yaml/v3".Node) as *"gopkg.in/yaml.v3".Node value in argument to parseV3Interface
../../../.local/share/go/pkg/mod/knative.dev/pkg@v0.0.0-20260406140200-cb58ae50e894/apis/duck/typed.go:62:14: undefined: cache.ToListWatcherWithWatchListSemantics
```

**How to fix:** Update the repo to use the newer dependency API:
```bash
cd pruner
# Update deps and fix compilation errors:
go get -u ./...
go build ./...
```
</details>

<details>
<summary><b>results</b> — Missing 1 package(s): `knative.dev/pkg/metrics`</summary>

```
pkg/apis/config/metrics.go:6:2: no required module provides package knative.dev/pkg/metrics; to add it:
```

**How to fix:** Update the repo to use the newer dependency API:
```bash
cd results
# Add missing dependencies:
go get knative.dev/pkg/metrics
```
</details>

<details>
<summary><b>triggers</b> — Missing 1 package(s): `knative.dev/pkg/metrics`</summary>

```
pkg/reconciler/metrics/metrics.go:31:2: no required module provides package knative.dev/pkg/metrics; to add it:
```

**How to fix:** Update the repo to use the newer dependency API:
```bash
cd triggers
# Add missing dependencies:
go get knative.dev/pkg/metrics
```
</details>

### ✅ Working Workspace

These repos can be used together in a `go.work` today:

```go
go 1.25.7

use (
	../../home/vincent/src/tektoncd/pipeline
	../../home/vincent/src/tektoncd/triggers
	../../home/vincent/src/tektoncd/chains
	../../home/vincent/src/tektoncd/cli
	../../home/vincent/src/tektoncd/results
	../../home/vincent/src/tektoncd/pipelines-as-code
	../../home/vincent/src/tektoncd/dashboard
	../../home/vincent/src/tektoncd/plumbing
	../../home/vincent/src/tektoncd/pruner
)
```

---
*Generated by [`workspace-check.py`](../blob/main/hack/workspace-check.py) — run locally or via [weekly CI](../blob/main/.github/workflows/workspace-check.yaml)*