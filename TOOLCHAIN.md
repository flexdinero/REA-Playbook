# Toolchain: fill the actual gaps

This is a selection map, not an instruction to install everything. Links are official repositories or documentation. A checked description proves relevance, not compatibility, security or successful integration. Review current release, license, dependencies, advisories and platform prerequisites before adoption.

## Smallest useful starting set

For an authorized web/SaaS reconstruction start with the existing coding environment, REA for relevant client inspection, Playwright for active journeys, the selected application framework and hosted PostgreSQL, an identity solution, contract tests, CI and observability. Add Ghidra only for a native-code question. Add workflow/model/video tools only when the target requires them.

## Investigation and fidelity

| Gap | Candidate | Use and boundary |
|---|---|---|
| Compiled-code analysis | [Ghidra](https://github.com/NationalSecurityAgency/ghidra) | Native analysis; provider integration must be tested independently |
| Runtime native behavior | [Frida](https://github.com/frida/frida), platform debugger | Instrument owned/authorized test processes; static recovery and execution answer different questions |
| Android DEX | [JADX](https://github.com/skylot/jadx) | Decompiled classes/methods; incomplete recovery remains possible |
| Android resources | [Apktool](https://github.com/iBotPeaches/Apktool) | Resource/manifest analysis; not proof of reconstructed behavior |
| .NET high-level exploration | [ILSpy](https://github.com/icsharpcode/ILSpy) | Managed decompilation; NativeAOT needs separate treatment |
| Active browser journeys | [Playwright](https://github.com/microsoft/playwright) | Chromium/Firefox/WebKit tests; mobile browser emulation is not native-device QA |
| Mobile UI automation | [Appium](https://github.com/appium/appium) | Platform-driver/device automation; verify driver and host requirements |
| Authorized HTTP traffic | [mitmproxy](https://github.com/mitmproxy/mitmproxy) | Test-client traffic capture/debugging; encrypted or pinned traffic may remain unavailable |
| Firmware extraction | [Binwalk](https://github.com/ReFirmLabs/binwalk), [Unblob](https://github.com/onekey-sec/unblob) | Extract supported content; does not emulate hardware/peripherals |
| Difficult path constraints | [angr](https://github.com/angr/angr), [Z3](https://github.com/Z3Prover/z3) | Bounded symbolic/constraint reasoning; state explosion and environmental models matter |
| Shot/motion/media reference | [rea-video](https://github.com/JuneYaooo/rea-video) | Evidence-led timeline analysis; uncertain classification and partial remake support |

A second commercial decompiler can be useful when an architecture or interpretation warrants independent analysis. Do not buy Hopper/IDA/JEB merely because REA lists them; tool licenses and platform compatibility remain separate.

## Engineering the product

The following combinations are proposed defaults, not a claim that any framework guarantees enterprise scale.

| Product class | Reasonable starting choice | Change when |
|---|---|---|
| TypeScript web/SaaS | [Next.js](https://github.com/vercel/next.js), optional [NestJS](https://github.com/nestjs/nest) service layer, hosted PostgreSQL | Separate service needed for workers/API ownership; existing stack has stronger constraints |
| Python/AI API | [FastAPI](https://github.com/fastapi/fastapi) with durable workers | Native/compiled bottlenecks, team conventions or workload needs another runtime |
| Enterprise .NET/Java | [ASP.NET Core](https://github.com/dotnet/aspnetcore) or [Spring Boot](https://github.com/spring-projects/spring-boot) | Prefer the organization's established language/platform ecosystem |
| Cross-platform mobile | [React Native](https://github.com/react/react-native) or [Flutter](https://github.com/flutter/flutter) | Native platform APIs, fidelity, accessibility or performance justify native modules/apps |
| Desktop | [Tauri](https://github.com/tauri-apps/tauri) or an existing native stack | Required native APIs, packaging or integration dictate another choice |
| Durable business automation | [Temporal](https://github.com/temporalio/temporal) | Simpler tasks fit existing jobs; visual connector automation is the primary need |
| Connector-oriented internal automation | [n8n](https://github.com/n8n-io/n8n) | Its licensing/deployment model fits the intended use; custom workflows need stronger code control |

n8n describes itself as fair-code; its [license](https://github.com/n8n-io/n8n/blob/master/LICENSE.md) has use and enterprise-file restrictions. Do not assume its source is freely embeddable in a competing paid service. Check the exact license and intended use before adopting any candidate.

Data: choose hosted PostgreSQL; [Supabase](https://github.com/supabase/supabase) is one possible hosted provider. Database migrations, roles, grants, tenant isolation, backups and restore still require design and proof. Do not create a local database merely to make a demo pass. Auth: [Keycloak](https://github.com/keycloak/keycloak) is a candidate IAM system, while [OpenFGA](https://github.com/openfga/openfga) addresses authorization relationships. They solve different parts of the problem; add an external authorization engine only if requirements justify it.

## Quality, security and operations

| Gap | Candidate | Acceptance use |
|---|---|---|
| Consumer/provider contracts | [Pact](https://github.com/pact-foundation/pact-js) | Verify actual contract versions between services |
| Schema-derived API testing | [Schemathesis](https://github.com/schemathesis/schemathesis) | Exercise edge cases using accurate API schemas |
| Accessibility | [axe-core](https://github.com/dequelabs/axe-core) | Automated checks plus keyboard/screen-reader/manual testing |
| Load/capacity | [k6](https://github.com/grafana/k6) | Measured percentiles, error rates and saturation under named conditions |
| Secrets | [Gitleaks](https://github.com/gitleaks/gitleaks) | Scan repository/history/artifacts; handle findings without printing secrets |
| Static security patterns | [Semgrep](https://github.com/semgrep/semgrep) | Review actionable findings; clean scans are not a security guarantee |
| Vulnerabilities/config | [Trivy](https://github.com/aquasecurity/trivy) | Scan relevant images/dependencies/config; adjudicate findings |
| Bill of materials | [Syft](https://github.com/anchore/syft) | Record shipped dependency identities/licenses |
| Telemetry | [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) | Correlate logs/metrics/traces, redact sensitive data, test alerts |
| Infrastructure as code | [OpenTofu](https://github.com/opentofu/opentofu) | Reproducible environment plans with reviewed changes and state protection |

Source scanning, runtime security testing, authorization tests and operational controls complement one another. Do not buy tools to substitute for defining and testing security boundaries.

## ML/AI systems

Use [PyTorch](https://github.com/pytorch/pytorch) for suitable training/research, [Transformers](https://github.com/huggingface/transformers) for supported model implementations, [PEFT](https://github.com/huggingface/peft) for appropriate parameter-efficient adaptation, [vLLM](https://github.com/vllm-project/vllm) for supported LLM serving, and [ONNX Runtime](https://github.com/microsoft/onnxruntime) for suitable inference targets. [MLflow](https://github.com/mlflow/mlflow) can track runs/evaluations/artifacts.

These are optional lanes. Establish model/data rights, accessible weights, tokenizer/preprocessing, representative evals, hardware, throughput, memory, latency and cost before choosing. A hosted chatbot replica can reproduce an interface and build an evaluated behavior substitute; that does not recreate the provider's model or training process.

## Specialized extensions

For additional evidence/testing gaps, use [the final research audit](FINAL-RESEARCH-AUDIT.md): rr for suitable native replay, Jepsen for relevant distributed histories, Stryker for mutation testing, AFL++ for instrumentable fuzzing, CBMC/Alive2 for scoped formal evidence, and reproducible-build/provenance guidance. Each has assumptions and platform limits; use the audit's primary links and adoption checks. The [offline observation comparator](OBSERVATION-HARNESS.md) is bundled and tested locally; the external tools were researched rather than installed.

For structured inference of hidden behavior, see [hypothesis-driven reconstruction](HYPOTHESIS-DRIVEN-RECONSTRUCTION.md). It maps optional automata learning, property-based testing, HTTP simulation, network fault injection, formal models and contract standards to specific experiments. These close selected investigation/design gaps when prerequisites hold; they are not mandatory installations or universal recovery tools.

Use [Awesome-REA's domain indexes](REFERENCE-INDEX.md) for JVM, WASM, games, protocol tooling, firmware and specialized native analysis rather than stacking overlapping tools in advance. Game reconstruction additionally needs simulation rules, input/timing, physics/RNG, asset provenance, save compatibility and target-platform tests. A WASM port also needs platform dependency, threading, memory and I/O design; compilation alone does not establish portability.

Each chosen dependency gets an adoption record: problem solved, canonical URL, exact version/SHA, license, host support, trust/data boundary, minimal verification, maintenance owner, failure/fallback behavior and removal path.
