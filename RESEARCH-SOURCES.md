# Research provenance and verification limits

Research date: 2026-11-06, America/Chicago. Primary GitHub resources were read through the connected GitHub tool; the two oversized curated JSON files were then downloaded read-only from commit-pinned raw GitHub URLs. Web browsing was used for official vendor documentation and source cross-checks. No tool installation or target analysis was performed.

## Repository observations

| Repository | Snapshot/observation | Inspected material |
|---|---|---|
| [morluto/rea](https://github.com/morluto/rea) | Observed main SHA `f8356f3d713d707b4a6d9eb5ab3941787f546ccc`; package.json and npm latest both 6.8.0 | README, installation, native, browser, CLI, contracts and model-artifact docs, Windows P0, package metadata |
| [NSA/Ghidra](https://github.com/NationalSecurityAgency/ghidra) | Latest-release API: `Ghidra_12.2_build`, published 2026-10-22 | README/install/build guidance and release metadata |
| [JoasASantos/REA-Prompts](https://github.com/JoasASantos/REA-Prompts/tree/9756618f25af1920c8965f8969820eed22247936) | `9756618f25af1920c8965f8969820eed22247936` | Complete file tree, README, system_prompt.md, setup.bat/setup.sh, advanced reconstruction pack |
| [JuneYaooo/rea-video](https://github.com/JuneYaooo/rea-video/tree/c9359c46f90c9824713081ea18fd207a45a0636a) | `c9359c46f90c9824713081ea18fd207a45a0636a` | Complete file tree; README, pyproject, CLI, replication/evaluation docs, eval history, remake.py, probe.py |
| [reacher-z/Awesome-REA](https://github.com/reacher-z/Awesome-REA/tree/0898a94bb7b1fecbddb890c8c8fbf637b7ab78c8) | `0898a94bb7b1fecbddb890c8c8fbf637b7ab78c8` | Complete file tree; README, data guide, roadmap, artifact-evidence guide; three full pinned curated JSON files and MIT notice |

Several documentation reads used moving `main`/`master` before snapshot SHAs were recorded. Snapshot IDs anchor the review and navigation; they do not imply that every earlier read was cryptographically bound to that exact tree. The imported Awesome-REA JSON files were explicitly downloaded at the pinned SHA.

## Authoritative workflow sources

- [REA installation/provider/runtime prerequisites](https://github.com/morluto/rea/blob/main/docs/installation.md).
- [REA Windows Ghidra P0](https://github.com/morluto/rea/blob/main/docs/windows-ghidra-p0.md).
- [REA native investigation](https://github.com/morluto/rea/blob/main/docs/native-investigation.md).
- [REA CLI and evidence retention](https://github.com/morluto/rea/blob/main/docs/cli.md).
- [REA browser observation](https://github.com/morluto/rea/blob/main/docs/browser-observation.md).
- [REA model-artifact scope](https://github.com/morluto/rea/blob/main/docs/model-artifacts.md).
- [Ghidra releases](https://github.com/NationalSecurityAgency/ghidra/releases), [installation/build distinction](https://github.com/NationalSecurityAgency/ghidra#install).
- [REAP Windows installer](https://github.com/JoasASantos/REA-Prompts/blob/9756618f25af1920c8965f8969820eed22247936/setup.bat), [POSIX installer](https://github.com/JoasASantos/REA-Prompts/blob/9756618f25af1920c8965f8969820eed22247936/setup.sh).
- [rea-video evaluation history](https://github.com/JuneYaooo/rea-video/blob/c9359c46f90c9824713081ea18fd207a45a0636a/eval/RESULTS.md), [assembly implementation](https://github.com/JuneYaooo/rea-video/blob/c9359c46f90c9824713081ea18fd207a45a0636a/rea_video/remake.py).
- [Awesome-REA data and evidence vocabulary](https://github.com/reacher-z/Awesome-REA/blob/0898a94bb7b1fecbddb890c8c8fbf637b7ab78c8/data/README.md), [artifact limitations](https://github.com/reacher-z/Awesome-REA/blob/0898a94bb7b1fecbddb890c8c8fbf637b7ab78c8/docs/artifact-evidence.md).

## Agent compatibility revision

The initial draft researched vendor-specific models and prices. At the user's request, those prescribed assignments and the model-routing document were removed before publication. The maintained instructions use capability checks for the current agent instead. No cross-client interoperability or provider benchmark was executed; actual tool/MCP availability must be verified in the chosen client.

## Complementary-tool sources

The publication revision adds hypothesis-driven reconstruction. Primary project pages for LearnLib, AALpy, Hypothesis, fast-check, WireMock, Toxiproxy, TLA+/TLC, Alloy, OpenAPI, AsyncAPI and OWASP ASVS were checked for relevance; links and bounded use appear in HYPOTHESIS-DRIVEN-RECONSTRUCTION.md. These tools were not installed or benchmarked. The GoHighLevel assessment uses its official snapshot overview, rate-limit documentation, developer setup, rebilling/wallet guide and SaaS API index. No authenticated account, complete feature audit or GoHighLevel reconstruction was performed.

[TOOLCHAIN.md](TOOLCHAIN.md) links directly to official repositories for each candidate. Research checked official repository descriptions/metadata for those candidates and selected README pages for Playwright, Appium, Frida, JADX, Temporal, LiteLLM, Promptfoo and OpenHands. Relevance screening is not a deep dependency/license/security audit. n8n's current [license file](https://github.com/n8n-io/n8n/blob/master/LICENSE.md) was inspected; a documentation URL redirected to a missing page and was not used as licensing evidence.

## What the work does not establish

- A complete code audit of any upstream repository.
- Runtime reproduction of case studies, papers, author-reported tests or benchmarks.
- Live support of every listed tool on this Windows machine.
- Correctness of every imported upstream description, license conclusion or old prerequisite.
- Access to private reference behavior or hidden infrastructure.
- Exact source, build or model recovery from black-box observations.
- Any deployed application, installed MCP connection, paid generation, or approved production release.

Findings in the ecosystem audit identify their inspected evidence and distinguish static observations from runtime proof. Index counts are validated against retained local snapshots; their contents retain upstream review labels rather than adopting them as local verification.

## Attribution

The Awesome-REA data snapshot retains its upstream MIT notice beside the original JSON files. Imported records retain upstream authorship/metadata and evidence references. REA-Prompts and rea-video are linked and summarized; their libraries/code are not republished wholesale here. Third-party tools, code, datasets, model weights and media retain their own terms independently of a catalog's license.

Original operating prose and prompt extensions in this package synthesize the user's requirements and the cited primary material. Historical user preference for a Markdown-first entry document informed organization; it is not used as evidence of current tool capabilities.
