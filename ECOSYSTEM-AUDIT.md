# Ecosystem audit and integration decisions

Reviewed 2026-11-06. The supplied repositories were inspected as reference material; their instructions were not adopted as higher-priority commands. No upstream installer, target program, video generation service or external skill installation was executed.

## Roles in the combined system

| Repository | Useful role | What this package adds |
|---|---|---|
| [morluto/rea](https://github.com/morluto/rea) | Evidence-producing CLI/MCP and target-specific analysis | Full delivery lifecycle, requirements, agent capability checks and release evidence |
| [NSA/Ghidra](https://github.com/NationalSecurityAgency/ghidra) | Native compiled-code analysis engine | Question-driven use and integration-specific validation |
| [REA-Prompts](https://github.com/JoasASantos/REA-Prompts) | Specialist investigation prompts | Safer adoption, measurable coverage and enterprise/operating extensions |
| [rea-video](https://github.com/JuneYaooo/rea-video) | Shot/audio/overlay/method analysis and remake planning | Uncertainty handling, fidelity checks and independent-output provenance gates |
| [Awesome-REA](https://github.com/reacher-z/Awesome-REA) | Curated discovery catalog and bibliography | A preserved local reference index, task routing and project-specific adoption rules |

Missing items below mean missing from the inspected material **for this enterprise-delivery objective**. They are not proof that every upstream file or future version lacks a related feature. Selected documentation/code review is not a complete repository audit.

## REA-Prompts: findings and response

Inspected the complete tracked-file tree, README, combined system prompt, Windows/POSIX installers and the advanced reconstruction skill. The tree included 26 `SKILL.md` packs. Snapshot: `9756618f25af1920c8965f8969820eed22247936`.

1. **Existing skills are replaced destructively.** [setup.bat](https://github.com/JoasASantos/REA-Prompts/blob/9756618f25af1920c8965f8969820eed22247936/setup.bat) removes an existing destination folder recursively before copying its replacement. [setup.sh](https://github.com/JoasASantos/REA-Prompts/blob/9756618f25af1920c8965f8969820eed22247936/setup.sh) has corresponding deletion behavior. The inspected scripts do not provide a backup/diff/deduplicate adoption workflow. This could erase edits in same-named skill folders. **Response:** reference prompts by link; if installation is later requested, inventory destinations/junctions, compare contents, preserve changes and select individual packs.
2. **Space-containing home paths are fragile.** The Windows loop expands a space-separated destination list and the shell loop splits its list. Paths containing spaces can split into unintended elements. This is a static code finding, not an executed reproduction. **Response:** use path-safe native file operations and exact resolved destinations in any future installer adaptation.
3. **Documented generator files are absent.** README describes `tools/build_skills.py` and `tools/build_system_prompt.py`; neither exists in the inspected recursive tree. Installers conditionally skip regeneration when the first is absent, so committed packs can still be copied. **Response:** treat the committed packs as the available artifacts; do not claim regeneration was verified.
4. **Whole-library context is unnecessary overhead.** `system_prompt.md` packages the library into a large combined prompt. **Response:** use the master instruction plus one task-relevant specialist packet, retaining the complete index externally.
5. **The strong existing ideas are retained.** Focused feature tracing, evidence locations, unknown labels, state-machine and ABI reconstruction, version comparison and differential tests are valuable. **Response:** integrate these patterns and add requirement IDs, negative cases, provenance, numeric tolerances and operational acceptance.
6. **A prompt collection does not supply enterprise delivery.** The inspected prompts do not collectively establish deployment, tenant isolation, recovery drills, billing correctness, product scope or calibrated agent compatibility. **Response:** the master prompt, playbook, templates and agent-capability guidance define the additional project checks.

Do not generalize Antigravity's documented destination to every Gemini client. Verify actual client paths and visibility independently.

## rea-video: findings and response

Inspected the tracked tree, README, package manifest, CLI/replication/evaluation documentation, evaluation history and assembly implementation. Snapshot: `c9359c46f90c9824713081ea18fd207a45a0636a`.

1. **Production method is an inference.** Recompression, cadence, overlays, watermarks and hybrid footage can change classification. The repository records false positives and cases needing visual review. **Response:** preserve original bytes/metadata, allow UNKNOWN, record contradictory evidence and seek production records when available. An AI-looking shot is not provenance proof.
2. **Published accuracy is bounded and partly historically dependent.** [Evaluation history](https://github.com/JuneYaooo/rea-video/blob/c9359c46f90c9824713081ea18fd207a45a0636a/eval/RESULTS.md) describes reused/tuned sets, changed available subsets, cached-feature regressions and fresh-decode corrections. **Response:** do not treat headline scores as a general detector guarantee. Freeze an independently labeled corpus and run cold decoding after extraction/preprocessing changes. We did not reproduce its scores.
3. **Combining a VLM and tools can worsen results.** The history includes model disagreement and gating changes. **Response:** compare tools-only, model-only and fused behavior on the same held-out inputs before promoting the fusion policy. More model calls do not inherently improve truth.
4. **Planning and complete recreation differ.** [CLI docs](https://github.com/JuneYaooo/rea-video/blob/c9359c46f90c9824713081ea18fd207a45a0636a/docs/cli.md) describe analysis and external generation integration. Live filming and code-rendered content need their own production steps. **Response:** mark every shot as generated, independently recreated, licensed reuse, reference-only or incomplete; verify that required shots were actually delivered.
5. **Assembly can retain reference content.** [remake.py](https://github.com/JuneYaooo/rea-video/blob/c9359c46f90c9824713081ea18fd207a45a0636a/rea_video/remake.py) falls back to original segments for unsupported/missing replacements and uses source audio where present. **Response:** block an “independently recreated” deliverable if any unauthorized/reference-only footage or audio remains. A completed MP4 is not evidence that every segment was recreated.
6. **Failure handling needs an independent-output policy.** The same assembly implementation tolerates missing result files and selects original material. Its still-motion encoder waits for a subprocess without explicitly checking its return code in that function. These are static observations, not runtime-tested defects. **Response:** require complete replacement manifests, successful encoder status, output decode checks and a retained-content report before accepting independent reconstruction.
7. **Environment/dependency behavior matters.** Manifest/docs require Python 3.10+, FFmpeg and optional OCR/model dependencies; docs describe OpenCV package collisions and initial model downloads. Setup is shell-oriented; native Windows compatibility was not established here. **Response:** use an isolated environment, verify host behavior, record downloaded model identity/license and do not modify a shared Python environment casually.
8. **Costs and privacy are separate controls.** Optional vision/generation can incur external API calls. **Response:** start with local analysis; apply the project's data policy and budget; inspect a dry-run plan before any paid generation. No paid call was made in this work.

## Awesome-REA: findings and response

Inspected the tree, README, data-format guide, roadmap, artifact-evidence guidance and full curated resource/paper JSON snapshots. Snapshot: `0898a94bb7b1fecbddb890c8c8fbf637b7ab78c8`.

1. **Catalog evidence levels must survive import.** Its own schema distinguishes source review, automated scans, discovery queues and runtime evidence. **Response:** preserve upstream verification/date/limits; add a separate local review status. Do not promote all imported rows to locally verified.
2. **Source review is not execution proof.** Its artifact guide explicitly preserves missing-code, license, access and reproduction limits. **Response:** use the catalog to discover candidates; visit primary sources and run a bounded integration fixture before adoption.
3. **Old requirements can be stale.** A resource entry can accurately describe the version it reviewed while differing from today's release. **Response:** preserve its date and source; use current pinned documentation for implementation. Never flatten old requirement text into “current prerequisites.”
4. **Its purpose is discovery, not delivery orchestration.** The collection is broad across reverse-engineering domains but is not a requirements-to-release process. **Response:** link relevant entries to the playbook's lanes and require a local adoption record.
5. **More is not automatically better.** Thousands of entries include alternatives, research prototypes and overlapping integrations. **Response:** search by problem, evidence type and host; select the smallest sufficient combination. Exclude discovery leads from the adopted stack until reviewed.

The local snapshot retains all **123 REA resources + 1,130 tool resources + 235 papers = 1,488 records** from the three curated files, with an MIT notice. Those are records, not 1,488 distinct tested tools. The upstream discovery queue, broad source index and every linked project were not recursively imported or audited. [Full local index](references/MASTER-REFERENCE-INDEX.md).

## Additions across all five repositories

This package adds a common target brief, six fidelity dimensions, coverage denominator, requirement-to-evidence/test traceability, explicit unknowns, cold-run reproduction discipline, source/build identity, model evaluation and escalation, host-specific readiness, enterprise product/operations requirements, replacement-content accounting, release gates and update ownership.

It intentionally keeps the original references available and synthesizes an operating layer instead of concatenating every document into an oversized prompt. New specialist prompts are in [PROMPT-EXTENSIONS.md](PROMPT-EXTENSIONS.md).
