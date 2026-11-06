# Capability audit: what REA and Ghidra can establish

Assessment date: 2026-11-06. REA identification confirmed by the user. This is a documentation-based capability assessment with selected metadata inspection, not a source-wide security audit or runtime benchmark.

## Their actual relationship

REA connects an agent to target-specific inspection workflows. Native work can use Ghidra or another supported engine. Ghidra supplies compiled-code analysis. The coding agent interprets evidence and builds an implementation. They are complementary parts of a larger process; neither supplies an enterprise product delivery system. See the [REA README](https://github.com/morluto/rea) and [Ghidra README](https://github.com/NationalSecurityAgency/ghidra).

## Capability and missing-proof matrix

The limits below are engineering conclusions about what the available evidence can establish. They do not mean a tool has no relevant partial capability.

| Area | Useful evidence from REA/Ghidra | What remains missing or limited | Necessary complement |
|---|---|---|---|
| Native executable | Assembly, pseudocode, references, imports, recovered types and control flow | Optimizations erase structure; stripped symbols, dynamic dispatch and obfuscation complicate analysis; recovered C-like text is not original source | Runtime debugging, test inputs, symbols/source where available, expert review |
| Web interface | DOM/script/package/network observations and selected screenshots | Observation covers selected pages and windows; hidden roles/states/features remain unseen | Playwright journeys, role matrix, visual and accessibility testing |
| SaaS backend | Client-visible calls, payloads in permitted captures, shipped client logic | Remote source, database constraints, queues, fraud rules and infrastructure may never reach the client | Source/docs/logs when available; independent service implementation and contract tests |
| JavaScript/Electron | Modules, imports, source maps where present, IPC and native boundaries | Missing maps, minification, lazy chunks, server modules and conditional code leave gaps | Full authorized journey capture, source-level investigation, integration tests |
| .NET | Metadata and CIL; native dependencies and selected build comparisons | Static managed inspection is not complete high-level recovery or proof of NativeAOT behavior | ILSpy/source where available; managed debugger and native tooling as applicable |
| Android | APK manifest/classes/resources through applicable workflows and external tools | Decompilation can fail; native libraries, obfuscation, server dependencies and device state remain separate | JADX, Apktool, adb, Appium, native analysis and real-device tests |
| iOS/macOS | Permitted local package/native artifacts can be inspected on supported hosts | Signing, entitlements, Keychain, background execution and platform services need native validation | macOS, Xcode, simulators/devices, signing and test accounts |
| Flutter/Unity | Package provenance/metadata and relevant native artifacts | Metadata does not recreate Dart source, game logic, scenes, assets or runtime behavior | SDK-specific investigation, permitted assets/source, runtime tests |
| Firmware/embedded | Extraction, image structure and native-analysis handoffs | Peripherals, timing, boot state, secure hardware and undocumented buses may be essential | Binwalk/Unblob, emulation where valid, debug hardware and test rig |
| Protocols | Recorded traffic and selected parsing/analysis | Encryption, missing session keys, unobserved versions, stateful timing and private services constrain reconstruction | Authorized test capture, protocol spec, contract/fuzz testing |
| AI/model artifacts | Declared tensors, dimensions and metadata for supported files | Does not load/interpret weights or run inference; a hosted API does not expose its weights/training process | Licensed weights/data or an explicitly evaluated substitute |
| Automation | Existing code/process/capture evidence can inform a workflow | Business permissions, durable state, replay, exactly-once effects and external limits need design | Workflow engine, idempotency, integration contracts and recovery tests |
| Enterprise SaaS/AaaS | Technical evidence can reveal pieces of an existing service | Product management, tenant isolation, support, billing, service obligations and operational readiness are not supplied | Application architecture, identity/authorization, observability, runbooks and ownership |
| Scale/security | Header flags and static candidates can inform questions | Header hardening is not proof of runtime safety; “enterprise scale” cannot be inferred from framework choice | Threat model, negative tests, capacity measurements and recovery drills |

REA's specialized surfaces change quickly. Use the exact release's catalog and documentation to decide which workflow is available. The table is not an exhaustive inventory of all REA tools.

## Especially important documented boundaries

### Browser observation is not the active test harness

REA's [browser guide](https://github.com/morluto/rea/blob/main/docs/browser-observation.md) describes passive CDP observation with bounded coverage. It complements active browser automation; it does not replace it. Candidate routes/endpoints found in bundles are leads to investigate, not proof that every route is usable.

### Standalone Ghidra and REA's provider are different surfaces

Ghidra's own UI, scripting, extensions and debugger ecosystem are broader than the selected REA adapter. REA's [native guide](https://github.com/morluto/rea/blob/main/docs/native-investigation.md) documents provider-specific operations and limits. A static reference is not proof that a call executes, and pseudocode should be checked against instructions and observed behavior where consequential.

### Native Windows support is bounded

The [Windows P0 guide](https://github.com/morluto/rea/blob/main/docs/windows-ghidra-p0.md) describes experimental Windows x64 read-only support. It admits selected native PE architectures, DOS MZ and a bounded raw 6502 lane on fixed local NTFS volumes. It does not establish general Windows parity, Ghidra GUI control, annotation support, every binary format, or Windows-on-Arm support. Reparse-point and path restrictions matter on a Windows workstation. Do not generalize this adapter boundary to standalone Ghidra.

### Model metadata is a narrow evidence class

The [model-artifact guide](https://github.com/morluto/rea/blob/main/docs/model-artifacts.md) distinguishes header inspection from full-file hashing. Equal metadata does not establish equal weights. Training data, hyperparameters, tokenizer, preprocessing, retrieval, tool use and serving behavior can all affect outputs independently of tensor declarations.

### Installation is not verification

The [installation guide](https://github.com/morluto/rea/blob/main/docs/installation.md) separates setup, host prerequisites and live use. npm package acquisition, agent registration, provider readiness and successful analysis are distinct milestones. A terminal's environment may differ from the desktop client's environment.

## Six meanings of “clone”

| Claim | What would substantiate it | Typical access limit |
|---|---|---|
| Visual fidelity | Matched screens/states/viewports/fonts/assets plus documented diff tolerance | Screenshots do not expose hidden interaction or all responsive behavior |
| Behavioral fidelity | Same outputs and side effects for a declared state/input corpus | Finite tests do not exhaust all possible inputs |
| Contract fidelity | API/protocol schemas, auth/errors/versioning and interoperability tests | Undocumented consumers or private endpoints may remain unknown |
| Operational fidelity | Measured load, resilience, recovery and security objectives | Reference production internals may be unavailable |
| Source/build identity | Original source/dependencies/toolchain or byte-identical reproducible artifacts | Decompilation does not invert compilation uniquely |
| Model fidelity | Exact accessible artifacts/configuration or a bounded statistical evaluation | Black-box API behavior underdetermines training and weights |

For finite black-box observations, many different implementations can agree on every observed case. This is the fundamental reason a universal “nothing missing” claim is unsupported. More tools improve evidence coverage; they do not remove this information limit.

## What an authorized artifact does not automatically include

Access to software is separate from permission to redistribute its source, images, fonts, trademarks, datasets, or model weights. Track provenance and the permissions relevant to the intended use. This package assumes authorized analysis and appropriately licensed implementation inputs; it does not provide license circumvention or third-party access.

## Practical decision rule

Use source when available. Use observed contracts and journeys to establish behavior. Use REA to inspect relevant artifacts. Use Ghidra for native questions. Use a debugger or instrumentation only when execution answers a concrete unresolved question. Build and verify the product with an ordinary engineering stack. Record every remaining gap.
