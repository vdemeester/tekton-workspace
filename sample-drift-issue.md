## 📊 Tekton Dependency Drift Report

**Generated:** 2026-04-15 08:26 UTC  
**Repos scanned:** 10

| Metric | Count |
|--------|-------|
| Drifted modules | 🔴 36 |
| Replace conflicts | 🟡 5 |
| Go versions in use | 🔴 5 |

<details>
<summary><b>Go Versions</b></summary>

| Repo | Go Version |
|------|-----------|
| chains | `1.25.7` |
| cli | `1.25.6` ⬅️ |
| dashboard | `1.25.0` ⬅️ |
| operator | `1.25.5` ⬅️ |
| pipeline | `1.25.7` |
| pipelines-as-code | `1.25.7` |
| plumbing | `1.25.7` |
| pruner | `1.24.0` ⬅️ |
| results | `1.25.6` ⬅️ |
| triggers | `1.25.6` ⬅️ |

</details>

### Drifted Dependencies

<details>
<summary><b><code>k8s.io/api</code></b> — 6 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.35.3` | ✅ latest |
| cli | `v0.34.5` | 🔴 behind |
| dashboard | `v0.35.3` | ✅ latest |
| operator | `v0.35.2` | 🔴 behind |
| pipeline | `v0.35.3` | ✅ latest |
| pipelines-as-code | `v0.35.3` | ✅ latest |
| pruner | `v0.33.1` | 🔴 behind |
| results | `v0.34.6` | 🔴 behind |
| triggers | `v0.32.13` | 🔴 behind |

**Alignment commands:**
```bash
cd cli && go get k8s.io/api@v0.35.3
cd operator && go get k8s.io/api@v0.35.3
cd pruner && go get k8s.io/api@v0.35.3
cd results && go get k8s.io/api@v0.35.3
cd triggers && go get k8s.io/api@v0.35.3
```
</details>

<details>
<summary><b><code>k8s.io/apiextensions-apiserver</code></b> — 5 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.35.2` | 🔴 behind |
| cli | `v0.32.11` | 🔴 behind |
| operator | `v0.35.2` | 🔴 behind |
| pipeline | `v0.35.2` | 🔴 behind |
| pipelines-as-code | `v0.35.3` | ✅ latest |
| pruner | `v0.33.1` | 🔴 behind |
| results | `v0.32.11` | 🔴 behind |
| triggers | `v0.32.13` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get k8s.io/apiextensions-apiserver@v0.35.3
cd cli && go get k8s.io/apiextensions-apiserver@v0.35.3
cd operator && go get k8s.io/apiextensions-apiserver@v0.35.3
cd pipeline && go get k8s.io/apiextensions-apiserver@v0.35.3
cd pruner && go get k8s.io/apiextensions-apiserver@v0.35.3
cd results && go get k8s.io/apiextensions-apiserver@v0.35.3
cd triggers && go get k8s.io/apiextensions-apiserver@v0.35.3
```
</details>

<details>
<summary><b><code>k8s.io/apimachinery</code></b> — 6 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.35.3` | ✅ latest |
| cli | `v0.34.5` | 🔴 behind |
| dashboard | `v0.35.3` | ✅ latest |
| operator | `v0.35.2` | 🔴 behind |
| pipeline | `v0.35.3` | ✅ latest |
| pipelines-as-code | `v0.35.3` | ✅ latest |
| pruner | `v0.33.1` | 🔴 behind |
| results | `v0.34.6` | 🔴 behind |
| triggers | `v0.33.9` | 🔴 behind |

**Alignment commands:**
```bash
cd cli && go get k8s.io/apimachinery@v0.35.3
cd operator && go get k8s.io/apimachinery@v0.35.3
cd pruner && go get k8s.io/apimachinery@v0.35.3
cd results && go get k8s.io/apimachinery@v0.35.3
cd triggers && go get k8s.io/apimachinery@v0.35.3
```
</details>

<details>
<summary><b><code>k8s.io/client-go</code></b> — 6 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.35.3` | 🔴 behind |
| cli | `v0.34.5` | 🔴 behind |
| dashboard | `v0.35.3` | 🔴 behind |
| operator | `v1.5.2` | ✅ latest |
| pipeline | `v0.35.3` | 🔴 behind |
| pipelines-as-code | `v0.35.3` | 🔴 behind |
| pruner | `v0.33.1` | 🔴 behind |
| results | `v0.34.6` | 🔴 behind |
| triggers | `v0.32.13` | 🔴 behind |

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
<summary><b><code>k8s.io/code-generator</code></b> — 5 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.35.3` | ✅ latest |
| operator | `v0.34.1` | 🔴 behind |
| pipeline | `v0.35.2` | 🔴 behind |
| pruner | `v0.33.1` | 🔴 behind |
| triggers | `v0.32.13` | 🔴 behind |

**Alignment commands:**
```bash
cd operator && go get k8s.io/code-generator@v0.35.3
cd pipeline && go get k8s.io/code-generator@v0.35.3
cd pruner && go get k8s.io/code-generator@v0.35.3
cd triggers && go get k8s.io/code-generator@v0.35.3
```
</details>

<details>
<summary><b><code>k8s.io/gengo/v2</code></b> — 4 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v2.0.0-20250922181213-ec3ebc5fd46b` | ✅ latest |
| operator | `v2.0.0-20250820003526-c297c0c1eb9d` | 🔴 behind |
| pipeline | `v2.0.0-20250922181213-ec3ebc5fd46b` | ✅ latest |
| pruner | `v2.0.0-20250207200755-1244d31929d7` | 🔴 behind |
| triggers | `v2.0.0-20240911193312-2b36238f13e9` | 🔴 behind |

**Alignment commands:**
```bash
cd operator && go get k8s.io/gengo/v2@v2.0.0-20250922181213-ec3ebc5fd46b
cd pruner && go get k8s.io/gengo/v2@v2.0.0-20250922181213-ec3ebc5fd46b
cd triggers && go get k8s.io/gengo/v2@v2.0.0-20250922181213-ec3ebc5fd46b
```
</details>

<details>
<summary><b><code>k8s.io/klog/v2</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v2.130.1` | 🔴 behind |
| cli | `v2.130.1` | 🔴 behind |
| dashboard | `v2.130.1` | 🔴 behind |
| operator | `v2.140.0` | ✅ latest |
| pipeline | `v2.130.1` | 🔴 behind |
| pipelines-as-code | `v2.140.0` | ✅ latest |
| plumbing | `v2.80.1` | 🔴 behind |
| pruner | `v2.130.1` | 🔴 behind |
| results | `v2.130.1` | 🔴 behind |
| triggers | `v2.130.1` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get k8s.io/klog/v2@v2.140.0
cd cli && go get k8s.io/klog/v2@v2.140.0
cd dashboard && go get k8s.io/klog/v2@v2.140.0
cd pipeline && go get k8s.io/klog/v2@v2.140.0
cd plumbing && go get k8s.io/klog/v2@v2.140.0
cd pruner && go get k8s.io/klog/v2@v2.140.0
cd results && go get k8s.io/klog/v2@v2.140.0
cd triggers && go get k8s.io/klog/v2@v2.140.0
```
</details>

<details>
<summary><b><code>k8s.io/kube-openapi</code></b> — 5 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.0.0-20250910181357-589584f1c912` | 🔴 behind |
| cli | `v0.0.0-20250710124328-f3f2b991d03b` | 🔴 behind |
| dashboard | `v0.0.0-20250910181357-589584f1c912` | 🔴 behind |
| operator | `v0.0.0-20260127142750-a19766b6e2d4` | 🔴 behind |
| pipeline | `v0.0.0-20250910181357-589584f1c912` | 🔴 behind |
| pipelines-as-code | `v0.0.0-20260330154417-16be699c7b31` | ✅ latest |
| pruner | `v0.0.0-20250318190949-c8a335a9a2ff` | 🔴 behind |
| results | `v0.0.0-20250710124328-f3f2b991d03b` | 🔴 behind |
| triggers | `v0.0.0-20250318190949-c8a335a9a2ff` | 🔴 behind |

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
<summary><b><code>k8s.io/utils</code></b> — 5 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.0.0-20251002143259-bc988d571ff4` | 🔴 behind |
| cli | `v0.0.0-20250820121507-0af2bda4dd1d` | 🔴 behind |
| dashboard | `v0.0.0-20251002143259-bc988d571ff4` | 🔴 behind |
| operator | `v0.0.0-20260210185600-b8788abfbbc2` | 🔴 behind |
| pipeline | `v0.0.0-20251002143259-bc988d571ff4` | 🔴 behind |
| pipelines-as-code | `v0.0.0-20260319190234-28399d86e0b5` | ✅ latest |
| pruner | `v0.0.0-20241210054802-24370beab758` | 🔴 behind |
| results | `v0.0.0-20250820121507-0af2bda4dd1d` | 🔴 behind |
| triggers | `v0.0.0-20241210054802-24370beab758` | 🔴 behind |

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
<summary><b><code>knative.dev/eventing</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| cli | `v0.30.3` | 🔴 behind |
| pipelines-as-code | `v0.48.2` | ✅ latest |
| triggers | `v0.30.3` | 🔴 behind |

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
| cli | `v0.0.0-20250415155312-ed3e2158b883` | 🔴 behind |
| operator | `v0.0.0-20260114161248-8c840449eed2` | 🔴 behind |
| pipeline | `v0.0.0-20260318013857-98d5a706d4fd` | 🔴 behind |
| pipelines-as-code | `v0.0.0-20260406140200-cb58ae50e894` | ✅ latest |
| pruner | `v0.0.0-20250811181739-e06d4c9af190` | 🔴 behind |
| results | `v0.0.0-20250415155312-ed3e2158b883` | 🔴 behind |
| triggers | `v0.0.0-20250415155312-ed3e2158b883` | 🔴 behind |

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
<summary><b><code>github.com/tektoncd/pipeline</code></b> — 4 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.11.0` | ✅ latest |
| cli | `v1.9.2` | 🔴 behind |
| operator | `v1.9.2` | 🔴 behind |
| pipelines-as-code | `v1.11.0` | ✅ latest |
| pruner | `v1.7.0` | 🔴 behind |
| results | `v1.9.2` | 🔴 behind |
| triggers | `v1.9.0` | 🔴 behind |

**Alignment commands:**
```bash
cd cli && go get github.com/tektoncd/pipeline@v1.11.0
cd operator && go get github.com/tektoncd/pipeline@v1.11.0
cd pruner && go get github.com/tektoncd/pipeline@v1.11.0
cd results && go get github.com/tektoncd/pipeline@v1.11.0
cd triggers && go get github.com/tektoncd/pipeline@v1.11.0
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
<summary><b><code>go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.63.0` | ✅ latest |
| cli | `v0.63.0` | ✅ latest |
| pipeline | `v0.63.0` | ✅ latest |
| results | `v0.63.0` | ✅ latest |
| triggers | `v0.60.0` | 🔴 behind |

**Alignment commands:**
```bash
cd triggers && go get go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc@v0.63.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp</code></b> — 5 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.67.0` | 🔴 behind |
| cli | `v0.63.0` | 🔴 behind |
| operator | `v0.63.0` | 🔴 behind |
| pipeline | `v0.67.0` | 🔴 behind |
| pipelines-as-code | `v0.68.0` | ✅ latest |
| pruner | `v0.62.0` | 🔴 behind |
| results | `v0.63.0` | 🔴 behind |
| triggers | `v0.61.0` | 🔴 behind |

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
<summary><b><code>go.opentelemetry.io/contrib/instrumentation/runtime</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.67.0` | 🔴 behind |
| pipeline | `v0.67.0` | 🔴 behind |
| pipelines-as-code | `v0.68.0` | ✅ latest |
| pruner | `v0.62.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get go.opentelemetry.io/contrib/instrumentation/runtime@v0.68.0
cd pipeline && go get go.opentelemetry.io/contrib/instrumentation/runtime@v0.68.0
cd pruner && go get go.opentelemetry.io/contrib/instrumentation/runtime@v0.68.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.43.0` | ✅ latest |
| cli | `v1.40.0` | 🔴 behind |
| operator | `v1.40.0` | 🔴 behind |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.40.0` | 🔴 behind |
| results | `v1.40.0` | 🔴 behind |
| triggers | `v1.40.0` | 🔴 behind |

**Alignment commands:**
```bash
cd cli && go get go.opentelemetry.io/otel@v1.43.0
cd operator && go get go.opentelemetry.io/otel@v1.43.0
cd pipeline && go get go.opentelemetry.io/otel@v1.43.0
cd pruner && go get go.opentelemetry.io/otel@v1.43.0
cd results && go get go.opentelemetry.io/otel@v1.43.0
cd triggers && go get go.opentelemetry.io/otel@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.42.0` | 🔴 behind |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.37.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc@v1.43.0
cd pipeline && go get go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc@v1.43.0
cd pruner && go get go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.43.0` | ✅ latest |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.37.0` | 🔴 behind |

**Alignment commands:**
```bash
cd pipeline && go get go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp@v1.43.0
cd pruner && go get go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/exporters/otlp/otlptrace</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.42.0` | 🔴 behind |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.37.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace@v1.43.0
cd pipeline && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace@v1.43.0
cd pruner && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.42.0` | 🔴 behind |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.37.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc@v1.43.0
cd pipeline && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc@v1.43.0
cd pruner && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.42.0` | 🔴 behind |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.37.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp@v1.43.0
cd pipeline && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp@v1.43.0
cd pruner && go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/exporters/prometheus</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.64.0` | 🔴 behind |
| pipeline | `v0.64.0` | 🔴 behind |
| pipelines-as-code | `v0.65.0` | ✅ latest |
| pruner | `v0.59.1` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get go.opentelemetry.io/otel/exporters/prometheus@v0.65.0
cd pipeline && go get go.opentelemetry.io/otel/exporters/prometheus@v0.65.0
cd pruner && go get go.opentelemetry.io/otel/exporters/prometheus@v0.65.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/exporters/stdout/stdouttrace</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.42.0` | 🔴 behind |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.37.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get go.opentelemetry.io/otel/exporters/stdout/stdouttrace@v1.43.0
cd pipeline && go get go.opentelemetry.io/otel/exporters/stdout/stdouttrace@v1.43.0
cd pruner && go get go.opentelemetry.io/otel/exporters/stdout/stdouttrace@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/metric</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.43.0` | ✅ latest |
| cli | `v1.40.0` | 🔴 behind |
| operator | `v1.40.0` | 🔴 behind |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.40.0` | 🔴 behind |
| results | `v1.40.0` | 🔴 behind |
| triggers | `v1.40.0` | 🔴 behind |

**Alignment commands:**
```bash
cd cli && go get go.opentelemetry.io/otel/metric@v1.43.0
cd operator && go get go.opentelemetry.io/otel/metric@v1.43.0
cd pipeline && go get go.opentelemetry.io/otel/metric@v1.43.0
cd pruner && go get go.opentelemetry.io/otel/metric@v1.43.0
cd results && go get go.opentelemetry.io/otel/metric@v1.43.0
cd triggers && go get go.opentelemetry.io/otel/metric@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/sdk</code></b> — 4 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.43.0` | ✅ latest |
| cli | `v1.40.0` | 🔴 behind |
| operator | `v1.40.0` | 🔴 behind |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.37.0` | 🔴 behind |
| results | `v1.40.0` | 🔴 behind |
| triggers | `v1.40.0` | 🔴 behind |

**Alignment commands:**
```bash
cd cli && go get go.opentelemetry.io/otel/sdk@v1.43.0
cd operator && go get go.opentelemetry.io/otel/sdk@v1.43.0
cd pipeline && go get go.opentelemetry.io/otel/sdk@v1.43.0
cd pruner && go get go.opentelemetry.io/otel/sdk@v1.43.0
cd results && go get go.opentelemetry.io/otel/sdk@v1.43.0
cd triggers && go get go.opentelemetry.io/otel/sdk@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/sdk/metric</code></b> — 4 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.43.0` | ✅ latest |
| cli | `v1.40.0` | 🔴 behind |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.37.0` | 🔴 behind |
| results | `v1.40.0` | 🔴 behind |
| triggers | `v1.40.0` | 🔴 behind |

**Alignment commands:**
```bash
cd cli && go get go.opentelemetry.io/otel/sdk/metric@v1.43.0
cd pipeline && go get go.opentelemetry.io/otel/sdk/metric@v1.43.0
cd pruner && go get go.opentelemetry.io/otel/sdk/metric@v1.43.0
cd results && go get go.opentelemetry.io/otel/sdk/metric@v1.43.0
cd triggers && go get go.opentelemetry.io/otel/sdk/metric@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/otel/trace</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.43.0` | ✅ latest |
| cli | `v1.40.0` | 🔴 behind |
| operator | `v1.40.0` | 🔴 behind |
| pipeline | `v1.42.0` | 🔴 behind |
| pipelines-as-code | `v1.43.0` | ✅ latest |
| pruner | `v1.40.0` | 🔴 behind |
| results | `v1.40.0` | 🔴 behind |
| triggers | `v1.40.0` | 🔴 behind |

**Alignment commands:**
```bash
cd cli && go get go.opentelemetry.io/otel/trace@v1.43.0
cd operator && go get go.opentelemetry.io/otel/trace@v1.43.0
cd pipeline && go get go.opentelemetry.io/otel/trace@v1.43.0
cd pruner && go get go.opentelemetry.io/otel/trace@v1.43.0
cd results && go get go.opentelemetry.io/otel/trace@v1.43.0
cd triggers && go get go.opentelemetry.io/otel/trace@v1.43.0
```
</details>

<details>
<summary><b><code>go.opentelemetry.io/proto/otlp</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.10.0` | ✅ latest |
| pipeline | `v1.9.0` | 🔴 behind |
| pipelines-as-code | `v1.10.0` | ✅ latest |
| pruner | `v1.7.0` | 🔴 behind |

**Alignment commands:**
```bash
cd pipeline && go get go.opentelemetry.io/proto/otlp@v1.10.0
cd pruner && go get go.opentelemetry.io/proto/otlp@v1.10.0
```
</details>

<details>
<summary><b><code>google.golang.org/grpc</code></b> — 4 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.80.0` | ✅ latest |
| cli | `v1.79.3` | 🔴 behind |
| operator | `v1.79.3` | 🔴 behind |
| pipeline | `v1.79.3` | 🔴 behind |
| pipelines-as-code | `v1.80.0` | ✅ latest |
| pruner | `v1.75.0` | 🔴 behind |
| results | `v1.79.3` | 🔴 behind |
| triggers | `v1.79.1` | 🔴 behind |

**Alignment commands:**
```bash
cd cli && go get google.golang.org/grpc@v1.80.0
cd operator && go get google.golang.org/grpc@v1.80.0
cd pipeline && go get google.golang.org/grpc@v1.80.0
cd pruner && go get google.golang.org/grpc@v1.80.0
cd results && go get google.golang.org/grpc@v1.80.0
cd triggers && go get google.golang.org/grpc@v1.80.0
```
</details>

<details>
<summary><b><code>google.golang.org/protobuf</code></b> — 3 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v1.36.11` | ✅ latest |
| cli | `v1.36.11` | ✅ latest |
| dashboard | `v1.36.8` | 🔴 behind |
| operator | `v1.36.11` | ✅ latest |
| pipeline | `v1.36.11` | ✅ latest |
| pipelines-as-code | `v1.36.11` | ✅ latest |
| pruner | `v1.36.10` | 🔴 behind |
| results | `v1.36.11` | ✅ latest |
| triggers | `v1.36.11` | ✅ latest |

**Alignment commands:**
```bash
cd dashboard && go get google.golang.org/protobuf@v1.36.11
cd pruner && go get google.golang.org/protobuf@v1.36.11
```
</details>

<details>
<summary><b><code>sigs.k8s.io/gateway-api</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| operator | `v1.5.0` | 🔴 behind |
| pipelines-as-code | `v1.5.1` | ✅ latest |

**Alignment commands:**
```bash
cd operator && go get sigs.k8s.io/gateway-api@v1.5.1
```
</details>

<details>
<summary><b><code>sigs.k8s.io/json</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| chains | `v0.0.0-20250730193827-2d320260d730` | ✅ latest |
| cli | `v0.0.0-20241014173422-cfa47c3a1cc8` | 🔴 behind |
| dashboard | `v0.0.0-20250730193827-2d320260d730` | ✅ latest |
| operator | `v0.0.0-20250730193827-2d320260d730` | ✅ latest |
| pipeline | `v0.0.0-20250730193827-2d320260d730` | ✅ latest |
| pipelines-as-code | `v0.0.0-20250730193827-2d320260d730` | ✅ latest |
| pruner | `v0.0.0-20250730193827-2d320260d730` | ✅ latest |
| results | `v0.0.0-20241014173422-cfa47c3a1cc8` | 🔴 behind |
| triggers | `v0.0.0-20241014173422-cfa47c3a1cc8` | 🔴 behind |

**Alignment commands:**
```bash
cd cli && go get sigs.k8s.io/json@v0.0.0-20250730193827-2d320260d730
cd results && go get sigs.k8s.io/json@v0.0.0-20250730193827-2d320260d730
cd triggers && go get sigs.k8s.io/json@v0.0.0-20250730193827-2d320260d730
```
</details>

<details>
<summary><b><code>sigs.k8s.io/structured-merge-diff/v4</code></b> — 2 versions</summary>

| Repo | Version | Status |
|------|---------|--------|
| operator | `v4.7.0` | ✅ latest |
| pruner | `v4.6.0` | 🔴 behind |
| triggers | `v4.6.0` | 🔴 behind |

**Alignment commands:**
```bash
cd pruner && go get sigs.k8s.io/structured-merge-diff/v4@v4.7.0
cd triggers && go get sigs.k8s.io/structured-merge-diff/v4@v4.7.0
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
| results | `v6.3.0` | 🔴 behind |

**Alignment commands:**
```bash
cd chains && go get sigs.k8s.io/structured-merge-diff/v6@v6.3.2
cd cli && go get sigs.k8s.io/structured-merge-diff/v6@v6.3.2
cd dashboard && go get sigs.k8s.io/structured-merge-diff/v6@v6.3.2
cd pipeline && go get sigs.k8s.io/structured-merge-diff/v6@v6.3.2
cd results && go get sigs.k8s.io/structured-merge-diff/v6@v6.3.2
```
</details>

### ⚠️ Replace Directive Conflicts

These prevent repos from coexisting in a `go.work` workspace:

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

### 🧩 Workspace Compatibility

Repos grouped by `k8s.io/api` minor version (repos in the same row can share a `go.work`):

| k8s.io/api | Repos |
|-----------|-------|
| `0.35` | chains, dashboard, operator, pipeline, pipelines-as-code |
| `0.34` | cli, results |
| `0.33` | pruner |
| `0.32` | triggers |

---
*Generated by [`dependency-drift.py`](../blob/main/hack/dependency-drift.py) — run locally or via [weekly CI](../blob/main/.github/workflows/dependency-drift.yaml)*