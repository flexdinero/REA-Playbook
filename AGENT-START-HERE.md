# REA + Ghidra: reconstruction and enterprise engineering system

Prepared 2026-11-06. This is an operating design and research package, not a completed installation or a tested product.

The objective is to reconstruct authorized software faithfully, build new systems from explicit requirements, and expose omissions before release. No prompt, model, or reverse-engineering tool can guarantee universal cloning or perfection. The useful standard is complete coverage of a declared scope, supported by independently checkable evidence.

## Start here

For hidden behavior, start with [hypothesis-driven reconstruction](HYPOTHESIS-DRIVEN-RECONSTRUCTION.md), [limitation closure](LIMITATIONS-AND-CLOSURE.md), and the [limitation register](templates/LIMITATION-REGISTER.csv). The [GoHighLevel assessment](GHL-RECONSTRUCTION.md) provides a large-SaaS discovery example.

1. Fill in [the target brief](templates/TARGET-BRIEF.md).
2. Paste [MASTER-PROMPT.md](MASTER-PROMPT.md) into your coding agent, with the completed brief.
3. Follow [PLAYBOOK.md](PLAYBOOK.md) for discovery, investigation, implementation, verification, and operations.
4. Consult [CAPABILITY-AUDIT.md](CAPABILITY-AUDIT.md) before assuming an artifact reveals a whole system.
5. Select the smallest sufficient stack using [TOOLCHAIN.md](TOOLCHAIN.md).
6. Apply [AGENT-COMPATIBILITY.md](AGENT-COMPATIBILITY.md) to use the playbook with your existing agent and available tools, without prescribed model routing.
7. Maintain [traceability](templates/TRACEABILITY.csv) and [release evidence](templates/RELEASE-CHECKLIST.md).

8. Use [REFERENCE-INDEX.md](REFERENCE-INDEX.md) to navigate the five-repository ecosystem, [ECOSYSTEM-AUDIT.md](ECOSYSTEM-AUDIT.md) for adoption findings, and [PROMPT-EXTENSIONS.md](PROMPT-EXTENSIONS.md) for focused follow-up work.

For a manageable first pilot, follow [WORKED-EXAMPLE.md](WORKED-EXAMPLE.md). Additional templates cover [task packets](templates/TASK-PACKET.md), [evidence records](templates/EVIDENCE-RECORD.json), [gaps](templates/GAP-REGISTER.csv), and [tool adoption](templates/TOOL-ADOPTION.md).

[RESEARCH-SOURCES.md](RESEARCH-SOURCES.md) records sources, versions, and verification limits.

The [complete local reference index](references/MASTER-REFERENCE-INDEX.md) preserves all 1,488 curated Awesome-REA records and links all 26 REAP skill packs plus the five core repositories. Imported source-review labels remain upstream assertions; they do not mean the tools or papers were all independently audited or executed here.

## What was actually checked

- You confirmed REA means [morluto/rea](https://github.com/morluto/rea).
- The workspace initially contained only `.git`, with no commits or configured remote reported by Git. No local REA source was available for a code audit.
- Research inspected upstream README files, installation and provider documentation, native and browser workflows, model-artifact limitations, package metadata, release metadata, and official documentation/repository descriptions for complementary tools.
- npm reported `rea-agents` 6.8.0. The REA source snapshot inspected included commit `f8356f3d713d707b4a6d9eb5ab3941787f546ccc`. Different reads of a moving branch can span commits; these are research observations, not a reproducible whole-repository audit.
- Ghidra's latest-release API reported 12.2. The published REA guide describes verification with Ghidra 12.1.4/JDK 21 and separately describes newer Java requirements.
- Nothing in this package proves installation, a live MCP connection, provider compatibility on this machine, a successful target reconstruction, production readiness, or model benchmark superiority.

## Immediate operating decisions

- Use REA as an evidence interface; use Ghidra when native compiled code is relevant.
- Start from available source and observed behavior before decompiling native code.
- Agent-neutral operation: use your existing Grok, Claude, Gemini, ChatGPT/Codex or other capable agent. Check actual tools, access and context limits; no vendor/model routing is prescribed.
- Start new enterprise systems with a modular architecture and explicit contracts. Add distributed infrastructure only when requirements justify it.
- Preserve originals, retain evidence, and distinguish observed, inferred, proposed, and unknown facts.
- Measure visual, behavioral, API, data, operational, and model fidelity separately.
- Treat requested enhancements as a separate backlog after establishing the reference baseline.

## First session instruction

> Read AGENT-START-HERE.md and MASTER-PROMPT.md. Use my completed TARGET-BRIEF. Inventory the workspace and available tools without changing my agent configuration. Produce a capability report, evidence plan, and the first high-risk vertical slice. Continue through authorized work; report missing access and evidence precisely. Do not claim that writing this plan implements or verifies the target.

For a new product, set `mode: greenfield`: REA and Ghidra become optional tools for specific compatibility questions rather than mandatory development dependencies.
