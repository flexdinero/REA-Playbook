# Master reference index: choose by task

Use this navigation layer first. The [complete generated index](references/MASTER-REFERENCE-INDEX.md) includes all curated records imported from Awesome-REA plus the 26 REAP packs and five core repositories. The [JSON index](references/master-reference-index.json) retains original upstream records and separate local review status. Repeated URLs may represent distinct resource/paper/case records; they are preserved rather than silently dropped.

## Core ecosystem

| Need | Canonical reference | Local operating guidance |
|---|---|---|
| Evidence tooling | [REA](https://github.com/morluto/rea) | [Playbook](PLAYBOOK.md), [capability audit](CAPABILITY-AUDIT.md) |
| Native-code engine | [Ghidra](https://github.com/NationalSecurityAgency/ghidra) | [Toolchain](TOOLCHAIN.md) |
| Investigation templates | [REA-Prompts](https://github.com/JoasASantos/REA-Prompts) | [Extensions](PROMPT-EXTENSIONS.md), [installer findings](ECOSYSTEM-AUDIT.md) |
| Video decomposition | [rea-video](https://github.com/JuneYaooo/rea-video) | [Media findings](ECOSYSTEM-AUDIT.md), extension 10 |
| Broad tools/cases/papers | [Awesome-REA](https://github.com/reacher-z/Awesome-REA) | [Local full index](references/MASTER-REFERENCE-INDEX.md) |

## Pick a specialist packet

| Task | Upstream sections or domain files | Added local controls |
|---|---|---|
| First feature/trace | REAP 01–02 | Evidence IDs, state/role coverage, counterexamples |
| Native executable or algorithm | REAP 03, 18, 22; Awesome native-analysis | ABI/numerical correctness, dynamic confirmation, bounded claims |
| Reconstruction | REAP 04, 20 | Six fidelity dimensions and release traceability |
| Website/Electron/extension/PWA | REAP 11; Awesome web-analysis | Active Playwright journeys, tenant/role matrix, service contracts |
| Android | REAP 08; Awesome android | Real-device/lifecycle, signing and integration evidence |
| Managed/JVM/WASM | Awesome managed-code and native/domain entries | Runtime-specific source/ABI and interoperability tests |
| Firmware/protocols | REAP 07, 20; Awesome firmware/protocol-analysis | Hardware/host prerequisites, bounded emulation and compatibility |
| Game/portability | REAP 05–06; Awesome game-analysis | Timing/RNG/physics, platform I/O and asset provenance |
| Crash/version comparison | REAP 15–16 | Build identity, regression corpus and resume packet |
| Authorized defensive security | REAP 09–10, 12–14, 17, 19, 21 | Isolated scope, threat model, evidence and verified fixes |
| Video/motion | rea-video CLI/evaluation/capability docs | Cold-run holdout, uncertain provenance, complete replacement manifest |
| Enterprise web/mobile/automation/AI | Local extensions 1–15 | Identity, billing, recovery, cost, support and measured release |

Exact REAP pack URLs are listed in the generated full index. For Awesome domain browsing use its [repository directory](https://github.com/reacher-z/Awesome-REA/tree/main/docs/repositories), [cases](https://github.com/reacher-z/Awesome-REA/blob/main/docs/cases.md), and [papers](https://github.com/reacher-z/Awesome-REA/blob/main/docs/papers.md). Follow primary sources for implementation decisions.

## Local data and provenance

- [Original REA-resource records](references/awesome-rea/rea-resources.json): 123.
- [Original tool-resource records](references/awesome-rea/tool-resources.json): 1,130.
- [Original bibliography records](references/awesome-rea/papers.json): 235.
- [Upstream MIT notice](references/awesome-rea/LICENSE).
- [Full tracked-file navigation for the three added repos](references/upstream-file-index.json): paths, blob IDs, sizes and commit-pinned URLs; not local copies or audits of every file.
- [Index builder](scripts/build_reference_index.py): rebuilds navigation from the preserved inputs without installing tools or calling models.
- [Research sources and limits](RESEARCH-SOURCES.md).

Rebuild from the repository root with `python scripts/build_reference_index.py`. This regenerates derived index files from the local snapshots only. Refreshing upstream content is a separate action requiring new source identity, licenses, drift review and validation.

## Adoption policy

The [final research source ledger](references/final-research-index.json) adds fifteen separately scoped source records beyond the preserved imported/navigation index. See [the audit](FINAL-RESEARCH-AUDIT.md) for actionable methods and [the observation harness](OBSERVATION-HARNESS.md) for locally tested comparison tooling.

For the investigation methods added beyond the imported catalog, use [hypothesis-driven reconstruction](HYPOTHESIS-DRIVEN-RECONSTRUCTION.md), [limitation closure](LIMITATIONS-AND-CLOSURE.md), [the register](templates/LIMITATION-REGISTER.csv), [agent compatibility](AGENT-COMPATIBILITY.md) and [the GoHighLevel plan](GHL-RECONSTRUCTION.md).

Search by concrete missing capability. Shortlist candidates whose host, runtime, license and data boundary fit. Confirm current primary documentation and a pinned release. Run a harmless fixture that exercises the intended integration. Mark local status as candidate, trial, adopted, rejected, blocked or retired with dated evidence. An imported row is initially `imported-not-independently-validated`.

Preserve upstream names, record IDs, descriptions, evidence URLs, review dates, limitations and licenses. Keep local measurements separate. Do not add counts across overlapping discovery/source-scan datasets and call the result unique verified projects. This snapshot deliberately excludes unreviewed discovery queues from the curated total.
