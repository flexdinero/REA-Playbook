# Agent-neutral use

Use this repository with Grok, Claude, Gemini, ChatGPT/Codex or another capable agent. No particular vendor, model, model router, effort setting or multi-agent framework is required. Compatibility is a capability check, not a tested certification of every client/version.

## Capability contract

| Capability | Needed for | If unavailable |
|---|---|---|
| Read repository/files | Follow the playbook and inspect source | Provide a clone, attached files or focused excerpts |
| Edit files | Implement the target and maintain evidence | Produce a concrete patch for a connected executor |
| Run shell/programs | Build, analyze artifacts and execute tests | Hand off exact commands; results remain UNTESTED until returned |
| Browser automation | Active reference/implementation journeys | Use another authorized test harness/operator and retain evidence |
| Image/visual inspection | Screenshots, diagrams and video frames | Supply deterministic comparisons plus a human/visual-capable review |
| MCP or equivalent tool bridge | Call REA through the agent | Use REA CLI in an authorized runtime and retain raw output |
| Suitable host/device | Native analysis, mobile builds, hardware tests | Use a verified external host/device lane; record transfer/data limits |
| External service access | Real integrations and production checks | Use an identified sandbox; block production claims until access exists |

## Client-specific adoption

Grok, Claude, Gemini and OpenAI products each have different chat, IDE/CLI and API surfaces. A chat session may have fewer execution capabilities than a coding agent with a connected runtime. Discover the actual surface rather than assuming tool availability from the brand. Follow current official REA installation documentation for supported client IDs, registration and restart behavior.

This package does not claim that every named chat client supports MCP directly. Where direct integration is absent, an authorized operator or coding runtime can execute CLI commands and pass evidence back. That is a handoff, not an automatic tool call.

## Bootstrap

1. Read README.md, AGENT-START-HERE.md and MASTER-PROMPT.md.
2. Create the target brief and inventory actual access, tools and limitations.
3. Establish a harmless live analysis/build/test fixture for the needed capabilities.
4. Execute bounded tasks with evidence and acceptance criteria.
5. If a capability is absent, prepare an exact handoff or mark the dependency BLOCKED; continue independent work.

Record agent/client/version, connected tools, host, target identity, data-handling constraints and actual outputs. Do not fabricate execution, switch models automatically or treat self-confidence as proof.

## Context, cost and reliability

Keep raw evidence on disk and pass relevant slices. Use deterministic code for parsing, hashes, accounting, comparisons, authorization and release gates. Limit repeated failed attempts; collect new evidence or change approach rather than repeating prompts. Track actual cost where relevant without prescribing model routing.

Single-agent sequential work is the default. Delegation and paid services follow the user's actual authorization. An optional independent reviewer can challenge consequential conclusions, but a different model is not a substitute for an independent oracle or test.

## Acceptance

The same requirement matrix, evidence rules and release gates apply to every agent. A less capable client can participate in specification and review; it cannot truthfully claim execution that requires tools it lacks. Report the verified capability surface and handoffs in the final project report.
