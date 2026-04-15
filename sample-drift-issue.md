## 📊 Tekton Dependency Drift Report

**Generated:** 2026-04-15 09:13 UTC  
**Repos scanned:** 10

| Metric | Count |
|--------|-------|
| Drifted modules | 🔴 37 |
| Replace conflicts | 🟢 0 |
| Go versions in use | 🔴 5 |

<details>
<summary><b>Go Versions</b></summary>

| Repo | Go Version |
|------|-----------|
| chains | `1.25.7` ⬅️ |
| cli | `1.25.8` |
| dashboard | `1.25.0` ⬅️ |
| operator | `1.25.5` ⬅️ |
| pipeline | `1.25.7` ⬅️ |
| pipelines-as-code | `1.25.7` ⬅️ |
| plumbing | `1.25.7` ⬅️ |
| pruner | `1.25.7` ⬅️ |
| results | `1.25.6` ⬅️ |
| triggers | `1.25.7` ⬅️ |

</details>

### Drifted Dependencies

<details>
<summary><b><code>k8s.io/api</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.35.3` | ✅ latest |
| cli | `v0.35.3` | ✅ latest |
| dashboard | `v0.35.3` | ✅ latest |
| operator | `v0.35.0` | 🔴 behind |
| pipeline | `v0.35.3` | ✅ latest |
| pipelines-as-code | `v0.35.3` | ✅ latest |
| pruner | `v0.35.3` | ✅ latest |
| results | `v0.34.6` | 🔴 behind |
| triggers | `v0.35.3` | ✅ latest |

**Alignment commands:**
```bash
cd operator && go get k8s.io/api@v0.35.3
cd results && go get k8s.io/api@v0.35.3
```
</details>

<details>
<summary><b><code>k8s.io/apiextensions-apiserver</code></b> — 4 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.35.2` | 🔴 behind |
| cli | `v0.35.3` | ✅ latest |
| operator | `v0.35.0` | 🔴 behind |
| pipeline | `v0.35.2` | 🔴 behind |
| pipelines-as-code | `v0.35.3` | ✅ latest |
| pruner | `v0.35.2` | 🔴 behind |
| results | `v0.32.11` | 🔴 behind |
| triggers | `v0.35.3` | ✅ latest |

**Alignment commands:**
```bash
cd chains && go get k8s.io/apiextensions-apiserver@v0.35.3
cd operator && go get k8s.io/apiextensions-apiserver@v0.35.3
cd pipeline && go get k8s.io/apiextensions-apiserver@v0.35.3
cd pruner && go get k8s.io/apiextensions-apiserver@v0.35.3
cd results && go get k8s.io/apiextensions-apiserver@v0.35.3
```
</details>

<details>
<summary><b><code>k8s.io/apimachinery</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.35.3` | ✅ latest |
| cli | `v0.35.3` | ✅ latest |
| dashboard | `v0.35.3` | ✅ latest |
| operator | `v0.35.0` | 🔴 behind |
| pipeline | `v0.35.3` | ✅ latest |
| pipelines-as-code | `v0.35.3` | ✅ latest |
| pruner | `v0.35.3` | ✅ latest |
| results | `v0.34.6` | 🔴 behind |
| triggers | `v0.35.3` | ✅ latest |

**Alignment commands:**
```bash
cd operator && go get k8s.io/apimachinery@v0.35.3
cd results && go get k8s.io/apimachinery@v0.35.3
```
</details>

<details>
<summary><b><code>k8s.io/apiserver</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| operator | `v0.34.1` | ✅ latest |
| results | `v0.32.13` | 🔴 behind |

**Alignment commands:**
```bash
cd results && go get k8s.io/apiserver@v0.34.1
```
</details>

<details>
<summary><b><code>k8s.io/client-go</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.35.3` | 🔴 behind |
| cli | `v0.35.3` | 🔴 behind |
| dashboard | `v0.35.3` | 🔴 behind |
| operator | `v1.5.2` | ✅ latest |
| pipeline | `v0.35.3` | 🔴 behind |
| pipelines-as-code | `v0.35.3` | 🔴 behind |
| pruner | `v0.35.3` | 🔴 behind |
| results | `v0.34.6` | 🔴 behind |
| triggers | `v0.35.3` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get k8s.io/client-go@v1.5.2
cd cli && go get k8s.io/client-go@v1.5.2
cd dashboard && go get k8s.io/client-go@v1.5.2
cd pipeline && go get k8s.io/client-go@v1.5.2
cd pipelines-as-code && go get k8s.io/client-go@v1.5.2
cd pruner && go get k8s.io/client-go@v1.5.2
cd results && go get k8s.io/client-go@v1.5.2
cd triggers && go get k8s.io/client-go@v1.5.2
```
</details>

<details>
<summary><b><code>k8s.io/code-generator</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.35.3` | ✅ latest |
| operator | `v0.34.1` | 🔴 behind |
| pipeline | `v0.35.2` | 🔴 behind |
| pruner | `v0.35.3` | ✅ latest |
| triggers | `v0.35.3` | ✅ latest |

**Alignment commands:**
```bash
cd operator && go get k8s.io/code-generator@v0.35.3
cd pipeline && go get k8s.io/code-generator@v0.35.3
```
</details>

<details>
<summary><b><code>k8s.io/gengo/v2</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v2.0.0-20250922181213-ec3ebc5fd46b` | ✅ latest |
| operator | `v2.0.0-20250820003526-c297c0c1eb9d` | 🔴 behind |
| pipeline | `v2.0.0-20250922181213-ec3ebc5fd46b` | ✅ latest |
| pruner | `v2.0.0-20250922181213-ec3ebc5fd46b` | ✅ latest |
| triggers | `v2.0.0-20250922181213-ec3ebc5fd46b` | ✅ latest |

**Alignment commands:**
```bash
cd operator && go get k8s.io/gengo/v2@v2.0.0-20250922181213-ec3ebc5fd46b
```
</details>

<details>
<summary><b><code>k8s.io/klog/v2</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v2.130.1` | 🔴 behind |
| cli | `v2.130.1` | 🔴 behind |
| dashboard | `v2.130.1` | 🔴 behind |
| operator | `v2.130.1` | 🔴 behind |
| pipeline | `v2.130.1` | 🔴 behind |
| pipelines-as-code | `v2.140.0` | ✅ latest |
| pruner | `v2.130.1` | 🔴 behind |
| results | `v2.130.1` | 🔴 behind |
| triggers | `v2.130.1` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get k8s.io/klog/v2@v2.140.0
cd cli && go get k8s.io/klog/v2@v2.140.0
cd dashboard && go get k8s.io/klog/v2@v2.140.0
cd operator && go get k8s.io/klog/v2@v2.140.0
cd pipeline && go get k8s.io/klog/v2@v2.140.0
cd pruner && go get k8s.io/klog/v2@v2.140.0
cd results && go get k8s.io/klog/v2@v2.140.0
cd triggers && go get k8s.io/klog/v2@v2.140.0
```
</details>

<details>
<summary><b><code>k8s.io/kube-openapi</code></b> — 4 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.0.0-20250910181357-589584f1c912` | 🔴 behind |
| cli | `v0.0.0-20250910181357-589584f1c912` | 🔴 behind |
| dashboard | `v0.0.0-20250910181357-589584f1c912` | 🔴 behind |
| operator | `v0.0.0-20251125145642-4e65d59e963e` | 🔴 behind |
| pipeline | `v0.0.0-20250910181357-589584f1c912` | 🔴 behind |
| pipelines-as-code | `v0.0.0-20260330154417-16be699c7b31` | ✅ latest |
| pruner | `v0.0.0-20250910181357-589584f1c912` | 🔴 behind |
| results | `v0.0.0-20250710124328-f3f2b991d03b` | 🔴 behind |
| triggers | `v0.0.0-20250910181357-589584f1c912` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get k8s.io/kube-openapi@v0.0.0-20260330154417-16be699c7b31
cd cli && go get k8s.io/kube-openapi@v0.0.0-20260330154417-16be699c7b31
cd dashboard && go get k8s.io/kube-openapi@v0.0.0-20260330154417-16be699c7b31
cd operator && go get k8s.io/kube-openapi@v0.0.0-20260330154417-16be699c7b31
cd pipeline && go get k8s.io/kube-openapi@v0.0.0-20260330154417-16be699c7b31
cd pruner && go get k8s.io/kube-openapi@v0.0.0-20260330154417-16be699c7b31
cd results && go get k8s.io/kube-openapi@v0.0.0-20260330154417-16be699c7b31
cd triggers && go get k8s.io/kube-openapi@v0.0.0-20260330154417-16be699c7b31
```
</details>

<details>
<summary><b><code>k8s.io/utils</code></b> — 4 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.0.0-20251002143259-bc988d571ff4` | 🔴 behind |
| cli | `v0.0.0-20251002143259-bc988d571ff4` | 🔴 behind |
| dashboard | `v0.0.0-20251002143259-bc988d571ff4` | 🔴 behind |
| operator | `v0.0.0-20260108192941-914a6e750570` | 🔴 behind |
| pipeline | `v0.0.0-20251002143259-bc988d571ff4` | 🔴 behind |
| pipelines-as-code | `v0.0.0-20260319190234-28399d86e0b5` | ✅ latest |
| pruner | `v0.0.0-20251002143259-bc988d571ff4` | 🔴 behind |
| results | `v0.0.0-20250820121507-0af2bda4dd1d` | 🔴 behind |
| triggers | `v0.0.0-20251002143259-bc988d571ff4` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get k8s.io/utils@v0.0.0-20260319190234-28399d86e0b5
cd cli && go get k8s.io/utils@v0.0.0-20260319190234-28399d86e0b5
cd dashboard && go get k8s.io/utils@v0.0.0-20260319190234-28399d86e0b5
cd operator && go get k8s.io/utils@v0.0.0-20260319190234-28399d86e0b5
cd pipeline && go get k8s.io/utils@v0.0.0-20260319190234-28399d86e0b5
cd pruner && go get k8s.io/utils@v0.0.0-20260319190234-28399d86e0b5
cd results && go get k8s.io/utils@v0.0.0-20260319190234-28399d86e0b5
cd triggers && go get k8s.io/utils@v0.0.0-20260319190234-28399d86e0b5
```
</details>

<details>
<summary><b><code>knative.dev/eventing</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| cli | `v0.48.1` | 🔴 behind |
| pipelines-as-code | `v0.48.2` | ✅ latest |
| triggers | `v0.0.0-20260209140146-9e76da08faaa` | 🔴 behind |

**Alignment commands:**
```bash
cd cli && go get knative.dev/eventing@v0.48.2
cd triggers && go get knative.dev/eventing@v0.48.2
```
</details>

<details>
<summary><b><code>knative.dev/hack</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| operator | `v0.0.0-20250331013814-c577ed9f7775` | 🔴 behind |
| pipeline | `v0.0.0-20260212092700-0126b283bf20` | ✅ latest |

**Alignment commands:**
```bash
cd operator && go get knative.dev/hack@v0.0.0-20260212092700-0126b283bf20
```
</details>

<details>
<summary><b><code>knative.dev/pkg</code></b> — 5 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.0.0-20260318013857-98d5a706d4fd` | 🔴 behind |
| cli | `v0.0.0-20260329160701-396dbaacd652` | 🔴 behind |
| operator | `v0.0.0-20260114161248-8c840449eed2` | 🔴 behind |
| pipeline | `v0.0.0-20260318013857-98d5a706d4fd` | 🔴 behind |
| pipelines-as-code | `v0.0.0-20260406140200-cb58ae50e894` | ✅ latest |
| pruner | `v0.0.0-20260318013857-98d5a706d4fd` | 🔴 behind |
| results | `v0.0.0-20250415155312-ed3e2158b883` | 🔴 behind |
| triggers | `v0.0.0-20260318013857-98d5a706d4fd` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get knative.dev/pkg@v0.0.0-20260406140200-cb58ae50e894
cd cli && go get knative.dev/pkg@v0.0.0-20260406140200-cb58ae50e894
cd operator && go get knative.dev/pkg@v0.0.0-20260406140200-cb58ae50e894
cd pipeline && go get knative.dev/pkg@v0.0.0-20260406140200-cb58ae50e894
cd pruner && go get knative.dev/pkg@v0.0.0-20260406140200-cb58ae50e894
cd results && go get knative.dev/pkg@v0.0.0-20260406140200-cb58ae50e894
cd triggers && go get knative.dev/pkg@v0.0.0-20260406140200-cb58ae50e894
```
</details>

<details>
<summary><b><code>github.com/tektoncd/pipeline</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.11.0` | ✅ latest |
| cli | `v1.11.0` | ✅ latest |
| operator | `v1.9.1` | 🔴 behind |
| pipelines-as-code | `v1.11.0` | ✅ latest |
| pruner | `v1.11.0` | ✅ latest |
| results | `v1.9.2` | 🔴 behind |
| triggers | `v1.11.0` | ✅ latest |

**Alignment commands:**
```bash
cd operator && go get github.com/tektoncd/pipeline@v1.11.0
cd results && go get github.com/tektoncd/pipeline@v1.11.0
```
</details>

<details>
<summary><b><code>github.com/tektoncd/plumbing</code></b> — 5 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.0.0-20250115133002-f515628dffea` | 🔴 behind |
| cli | `v0.0.0-20250430145243-3b7cd59879c1` | 🔴 behind |
| dashboard | `v0.0.0-20221005125931-631bdcbca245` | 🔴 behind |
| operator | `v0.0.0-20250805154627-25448098dea2` | ✅ latest |
| pipeline | `v0.0.0-20220817140952-3da8ce01aeeb` | 🔴 behind |
| pruner | `v0.0.0-20250805154627-25448098dea2` | ✅ latest |
| triggers | `v0.0.0-20250430145243-3b7cd59879c1` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get github.com/tektoncd/plumbing@v0.0.0-20250805154627-25448098dea2
cd cli && go get github.com/tektoncd/plumbing@v0.0.0-20250805154627-25448098dea2
cd dashboard && go get github.com/tektoncd/plumbing@v0.0.0-20250805154627-25448098dea2
cd pipeline && go get github.com/tektoncd/plumbing@v0.0.0-20250805154627-25448098dea2
cd triggers && go get github.com/tektoncd/plumbing@v0.0.0-20250805154627-25448098dea2
```
</details>

<details>
<summary><b><code>github.com/tektoncd/triggers</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| cli | `v0.35.1-0.20260401091813-1aad8a1898ec` | ✅ latest |
| operator | `v0.35.0` | 🔴 behind |
| results | `v0.35.0` | 🔴 behind |

**Alignment commands:**
```bash
cd operator && go get github.com/tektoncd/triggers@v0.35.1-0.20260401091813-1aad8a1898ec
cd results && go get github.com/tektoncd/triggers@v0.35.1-0.20260401091813-1aad8a1898ec
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.63.0` | 🔴 behind |
| cli | `v0.63.0` | 🔴 behind |
| pipeline | `v0.63.0` | 🔴 behind |
| results | `v0.67.0` | ✅ latest |
| triggers | `v0.63.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc@v0.67.0
cd cli && go get go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc@v0.67.0
cd pipeline && go get go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc@v0.67.0
cd triggers && go get go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc@v0.67.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.67.0` | 🔴 behind |
| cli | `v0.67.0` | 🔴 behind |
| operator | `v0.63.0` | 🔴 behind |
| pipeline | `v0.67.0` | 🔴 behind |
| pipelines-as-code | `v0.68.0` | ✅ latest |
| pruner | `v0.67.0` | 🔴 behind |
| results | `v0.67.0` | 🔴 behind |
| triggers | `v0.67.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp@v0.68.0
cd cli && go get go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp@v0.68.0
cd operator && go get go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp@v0.68.0
cd pipeline && go get go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp@v0.68.0
cd pruner && go get go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp@v0.68.0
cd results && go get go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp@v0.68.0
cd triggers && go get go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp@v0.68.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/contrib/instrumentation/runtime</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.67.0` | 🔴 behind |
| pipeline | `v0.67.0` | 🔴 behind |
| pipelines-as-code | `v0.68.0` | ✅ latest |
| pruner | `v0.67.0` | 🔴 behind |
| triggers | `v0.67.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get go.opentelemetry.io/contrib/instrumentation/runtime@v0.68.0
cd pipeline && go get go.opentelemetry.io/contrib/instrumentation/runtime@v0.68.0
cd pruner && go get go.opentelemetry.io/contrib/instrumentation/runtime@v0.68.0
cd triggers && go get go.opentelemetry.io/contrib/instrumentation/runtime@v0.68.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.43.0` | ✅ latest |
| cli | `v1.43.0` | ✅ latest |
| operator | `v1.40.0` | 🔴 behind |
| pipeline | `v1.43.0` | ✅ latest |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.43.0` | ✅ latest |
| results | `v1.43.0` | ✅ latest |
| triggers | `v1.43.0` | ✅ latest |

**Alignment commands:**
```bash
cd operator && go get go.opentelemetry.io/otel@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.42.0` | 🔴 behind |
| cli | `v1.42.0` | 🔴 behind |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.42.0` | 🔴 behind |
| triggers | `v1.42.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc@v1.43.0
cd cli && go get go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc@v1.43.0
cd pipeline && go get go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc@v1.43.0
cd pruner && go get go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc@v1.43.0
cd triggers && go get go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.43.0` | ✅ latest |
| cli | `v1.42.0` | 🔴 behind |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.43.0` | ✅ latest |
| triggers | `v1.43.0` | ✅ latest |

**Alignment commands:**
```bash
cd cli && go get go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp@v1.43.0
cd pipeline && go get go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/exporters/otlp/otlptrace</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.43.0` | ✅ latest |
| cli | `v1.43.0` | ✅ latest |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.43.0` | ✅ latest |
| triggers | `v1.43.0` | ✅ latest |

**Alignment commands:**
```bash
cd pipeline && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.42.0` | 🔴 behind |
| cli | `v1.42.0` | 🔴 behind |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.42.0` | 🔴 behind |
| triggers | `v1.42.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc@v1.43.0
cd cli && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc@v1.43.0
cd pipeline && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc@v1.43.0
cd pruner && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc@v1.43.0
cd triggers && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.43.0` | ✅ latest |
| cli | `v1.43.0` | ✅ latest |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.43.0` | ✅ latest |
| triggers | `v1.43.0` | ✅ latest |

**Alignment commands:**
```bash
cd pipeline && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/exporters/prometheus</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.64.0` | 🔴 behind |
| cli | `v0.64.0` | 🔴 behind |
| pipeline | `v0.64.0` | 🔴 behind |
| pipelines-as-code | `v0.65.0` | ✅ latest |
| pruner | `v0.64.0` | 🔴 behind |
| triggers | `v0.64.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get go.opentelemetry.io/otel/exporters/prometheus@v0.65.0
cd cli && go get go.opentelemetry.io/otel/exporters/prometheus@v0.65.0
cd pipeline && go get go.opentelemetry.io/otel/exporters/prometheus@v0.65.0
cd pruner && go get go.opentelemetry.io/otel/exporters/prometheus@v0.65.0
cd triggers && go get go.opentelemetry.io/otel/exporters/prometheus@v0.65.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/exporters/stdout/stdouttrace</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.42.0` | 🔴 behind |
| cli | `v1.42.0` | 🔴 behind |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.42.0` | 🔴 behind |
| triggers | `v1.42.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get go.opentelemetry.io/otel/exporters/stdout/stdouttrace@v1.43.0
cd cli && go get go.opentelemetry.io/otel/exporters/stdout/stdouttrace@v1.43.0
cd pipeline && go get go.opentelemetry.io/otel/exporters/stdout/stdouttrace@v1.43.0
cd pruner && go get go.opentelemetry.io/otel/exporters/stdout/stdouttrace@v1.43.0
cd triggers && go get go.opentelemetry.io/otel/exporters/stdout/stdouttrace@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/metric</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.43.0` | ✅ latest |
| cli | `v1.43.0` | ✅ latest |
| operator | `v1.40.0` | 🔴 behind |
| pipeline | `v1.43.0` | ✅ latest |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.43.0` | ✅ latest |
| results | `v1.43.0` | ✅ latest |
| triggers | `v1.43.0` | ✅ latest |

**Alignment commands:**
```bash
cd operator && go get go.opentelemetry.io/otel/metric@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/sdk</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.43.0` | ✅ latest |
| cli | `v1.43.0` | ✅ latest |
| operator | `v1.40.0` | 🔴 behind |
| pipeline | `v1.43.0` | ✅ latest |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.43.0` | ✅ latest |
| results | `v1.43.0` | ✅ latest |
| triggers | `v1.43.0` | ✅ latest |

**Alignment commands:**
```bash
cd operator && go get go.opentelemetry.io/otel/sdk@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/trace</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.43.0` | ✅ latest |
| cli | `v1.43.0` | ✅ latest |
| operator | `v1.40.0` | 🔴 behind |
| pipeline | `v1.43.0` | ✅ latest |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.43.0` | ✅ latest |
| results | `v1.43.0` | ✅ latest |
| triggers | `v1.43.0` | ✅ latest |

**Alignment commands:**
```bash
cd operator && go get go.opentelemetry.io/otel/trace@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/proto/otlp</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.10.0` | ✅ latest |
| cli | `v1.10.0` | ✅ latest |
| pipeline | `v1.9.0` | 🔴 behind |
| pipelines-as-code | `v1.10.0` | ✅ latest |
| pruner | `v1.10.0` | ✅ latest |
| triggers | `v1.10.0` | ✅ latest |

**Alignment commands:**
```bash
cd pipeline && go get go.opentelemetry.io/proto/otlp@v1.10.0
```
</details>

<details>
<summary><b><code>google.golang.org/grpc</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.80.0` | ✅ latest |
| cli | `v1.80.0` | ✅ latest |
| operator | `v1.78.0` | 🔴 behind |
| pipeline | `v1.80.0` | ✅ latest |
| pipelines-as-code | `v1.80.0` | ✅ latest |
| pruner | `v1.80.0` | ✅ latest |
| results | `v1.80.0` | ✅ latest |
| triggers | `v1.80.0` | ✅ latest |

**Alignment commands:**
```bash
cd operator && go get google.golang.org/grpc@v1.80.0
```
</details>

<details>
<summary><b><code>google.golang.org/protobuf</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.36.11` | ✅ latest |
| cli | `v1.36.11` | ✅ latest |
| dashboard | `v1.36.8` | 🔴 behind |
| operator | `v1.36.11` | ✅ latest |
| pipeline | `v1.36.11` | ✅ latest |
| pipelines-as-code | `v1.36.11` | ✅ latest |
| pruner | `v1.36.11` | ✅ latest |
| results | `v1.36.11` | ✅ latest |
| triggers | `v1.36.11` | ✅ latest |

**Alignment commands:**
```bash
cd dashboard && go get google.golang.org/protobuf@v1.36.11
```
</details>

<details>
<summary><b><code>sigs.k8s.io/gateway-api</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| operator | `v1.4.1` | 🔴 behind |
| pipelines-as-code | `v1.5.1` | ✅ latest |
| triggers | `v1.1.0` | 🔴 behind |

**Alignment commands:**
```bash
cd operator && go get sigs.k8s.io/gateway-api@v1.5.1
cd triggers && go get sigs.k8s.io/gateway-api@v1.5.1
```
</details>

<details>
<summary><b><code>sigs.k8s.io/json</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.0.0-20250730193827-2d320260d730` | ✅ latest |
| cli | `v0.0.0-20250730193827-2d320260d730` | ✅ latest |
| dashboard | `v0.0.0-20250730193827-2d320260d730` | ✅ latest |
| operator | `v0.0.0-20250730193827-2d320260d730` | ✅ latest |
| pipeline | `v0.0.0-20250730193827-2d320260d730` | ✅ latest |
| pipelines-as-code | `v0.0.0-20250730193827-2d320260d730` | ✅ latest |
| pruner | `v0.0.0-20250730193827-2d320260d730` | ✅ latest |
| results | `v0.0.0-20241014173422-cfa47c3a1cc8` | 🔴 behind |
| triggers | `v0.0.0-20250730193827-2d320260d730` | ✅ latest |

**Alignment commands:**
```bash
cd results && go get sigs.k8s.io/json@v0.0.0-20250730193827-2d320260d730
```
</details>

<details>
<summary><b><code>sigs.k8s.io/release-utils</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.12.4` | ✅ latest |
| operator | `v0.12.3` | 🔴 behind |

**Alignment commands:**
```bash
cd operator && go get sigs.k8s.io/release-utils@v0.12.4
```
</details>

<details>
<summary><b><code>sigs.k8s.io/structured-merge-diff/v6</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v6.3.0` | 🔴 behind |
| cli | `v6.3.0` | 🔴 behind |
| dashboard | `v6.3.0` | 🔴 behind |
| pipeline | `v6.3.0` | 🔴 behind |
| pipelines-as-code | `v6.3.2` | ✅ latest |
| pruner | `v6.3.0` | 🔴 behind |
| results | `v6.3.0` | 🔴 behind |
| triggers | `v6.3.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get sigs.k8s.io/structured-merge-diff/v6@v6.3.2
cd cli && go get sigs.k8s.io/structured-merge-diff/v6@v6.3.2
cd dashboard && go get sigs.k8s.io/structured-merge-diff/v6@v6.3.2
cd pipeline && go get sigs.k8s.io/structured-merge-diff/v6@v6.3.2
cd pruner && go get sigs.k8s.io/structured-merge-diff/v6@v6.3.2
cd results && go get sigs.k8s.io/structured-merge-diff/v6@v6.3.2
cd triggers && go get sigs.k8s.io/structured-merge-diff/v6@v6.3.2
```
</details>

### 🧩 Workspace Compatibility

Repos grouped by `k8s.io/api` minor version (repos in the same row can share a `go.work`):

| k8s.io/api | Repos |
|-----------|-------|
| `0.35` | chains, cli, dashboard, operator, pipeline, pipelines-as-code, pruner, triggers |
| `0.34` | results |

---
*Generated by [`dependency-drift.py`](../blob/main/hack/dependency-drift.py) — run locally or via [weekly CI](../blob/main/.github/workflows/dependency-drift.yaml)*