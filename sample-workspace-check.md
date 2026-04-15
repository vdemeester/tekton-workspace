## 🔨 Tekton Workspace Compatibility Check

**Generated:** 2026-04-15 09:12 UTC  
**Repos checked:** 10

| Metric | Result |
|--------|--------|
| Compatible repos | 🟡 6/10 |
| Replace conflicts | 🟢 0 |
| Downgrading replaces | 🟡 10 |

### ⚠️ Downgrading Replace Directives

These repos have `replace` directives that pin shared dependencies to **older versions** 
than other repos require. In a Go workspace, replaces apply globally — one repo's 
downgrade breaks everyone else.

| Repo | Module | Pinned To | Others Need |
|------|--------|-----------|-------------|
| pipeline | `github.com/aws/aws-sdk-go-v2/service/ecr` | `v1.27.3` | `v1.51.2` |
| pipeline | `github.com/aws/aws-sdk-go-v2/service/ecrpublic` | `v1.23.3` | `v1.38.2` |
| operator | `k8s.io/api` | `v0.32.4` | `v0.35.3` |
| operator | `k8s.io/apiextensions-apiserver` | `v0.32.9` | `v0.35.3` |
| operator | `k8s.io/apimachinery` | `v0.32.4` | `v0.35.3` |
| operator | `k8s.io/client-go` | `v0.32.4` | `v1.5.2` |
| operator | `k8s.io/code-generator` | `v0.32.4` | `v0.35.3` |
| operator | `k8s.io/kube-openapi` | `v0.0.0-20250627150254-e9823e99808e` | `v0.0.0-20260330154417-16be699c7b31` |
| operator | `knative.dev/eventing` | `v0.30.3` | `v0.48.2` |
| operator | `knative.dev/pkg` | `v0.0.0-20250415155312-ed3e2158b883` | `v0.0.0-20260406140200-cb58ae50e894` |

**Fix:** Remove these replace directives and update the code to work with the newer versions.

### Full Workspace Build (2/10)

All repos in a single `go.work` (except hard conflicts):

| Repo | Status | Issue |
|------|--------|-------|
| dashboard | ✅ builds | — |
| plumbing | ✅ builds | — |
| chains | ❌ Missing Module | Missing 2 package(s): `knative.dev/pkg/observability/configmap`, `gocloud.dev/docstore/awsdynamodb` |
| cli | ❌ Missing Module | Missing 1 package(s): `knative.dev/pkg/observability/configmap` |
| operator | ❌ Missing Module | Missing 1 package(s): `knative.dev/pkg/observability/configmap` |
| pipeline | ❌ Missing Module | Missing 1 package(s): `knative.dev/pkg/observability/configmap` |
| pipelines-as-code | ❌ Missing Module | Missing 1 package(s): `knative.dev/pkg/observability/configmap` |
| pruner | ❌ Missing Module | Missing 1 package(s): `knative.dev/pkg/observability/configmap` |
| results | ❌ Missing Module | Missing 1 package(s): `knative.dev/pkg/observability/configmap` |
| triggers | ❌ Missing Module | Missing 1 package(s): `knative.dev/pkg/observability/configmap` |

<details>
<summary><b>Build error details</b></summary>

**chains** — Missing 2 package(s): `knative.dev/pkg/observability/configmap`, `gocloud.dev/docstore/awsdynamodb`
```
../pipeline/pkg/apis/config/metrics_tls.go:9:2: no required module provides package knative.dev/pkg/observability/configmap; to add it:
pkg/chains/storage/docdb/docdb.go:30:2: no required module provides package gocloud.dev/docstore/awsdynamodb; to add it:
```

**cli** — Missing 1 package(s): `knative.dev/pkg/observability/configmap`
```
../pipeline/pkg/apis/config/metrics_tls.go:9:2: no required module provides package knative.dev/pkg/observability/configmap; to add it:
```

**operator** — Missing 1 package(s): `knative.dev/pkg/observability/configmap`
```
../pipeline/pkg/apis/config/metrics_tls.go:9:2: no required module provides package knative.dev/pkg/observability/configmap; to add it:
```

**pipeline** — Missing 1 package(s): `knative.dev/pkg/observability/configmap`
```
pkg/apis/config/metrics_tls.go:9:2: no required module provides package knative.dev/pkg/observability/configmap; to add it:
```

**pipelines-as-code** — Missing 1 package(s): `knative.dev/pkg/observability/configmap`
```
../pipeline/pkg/apis/config/metrics_tls.go:9:2: no required module provides package knative.dev/pkg/observability/configmap; to add it:
```

**pruner** — Missing 1 package(s): `knative.dev/pkg/observability/configmap`
```
../pipeline/pkg/apis/config/metrics_tls.go:9:2: no required module provides package knative.dev/pkg/observability/configmap; to add it:
```

**results** — Missing 1 package(s): `knative.dev/pkg/observability/configmap`
```
../pipeline/pkg/apis/config/metrics_tls.go:9:2: no required module provides package knative.dev/pkg/observability/configmap; to add it:
```

**triggers** — Missing 1 package(s): `knative.dev/pkg/observability/configmap`
```
../pipeline/pkg/apis/config/metrics_tls.go:9:2: no required module provides package knative.dev/pkg/observability/configmap; to add it:
```

</details>

### Clean Workspace Build (6/8)

Without repos that have problematic replaces (operator, pipeline):

| Repo | Status | Issue |
|------|--------|-------|
| cli | ✅ builds | — |
| dashboard | ✅ builds | — |
| pipelines-as-code | ✅ builds | — |
| plumbing | ✅ builds | — |
| pruner | ✅ builds | — |
| triggers | ✅ builds | — |
| chains | ❌ Missing Module | Missing 1 package(s): `gocloud.dev/docstore/awsdynamodb` |
| results | ❌ Missing Module | Missing 1 package(s): `knative.dev/pkg/metrics` |

### ✅ Working Workspace

These repos can be used together in a `go.work` today:

```go
go 1.25.8

use (
	./triggers
	./chains
	./cli
	./results
	./pipelines-as-code
	./dashboard
	./plumbing
	./pruner
)
```

---
*Generated by [`workspace-check.py`](../blob/main/hack/workspace-check.py) — run locally or via [weekly CI](../blob/main/.github/workflows/workspace-check.yaml)*