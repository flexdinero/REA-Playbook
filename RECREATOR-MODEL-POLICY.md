# Agent-neutral quality and cost policy

Use the cheapest available model that has passed the task's measured quality gates. Capability, price and account availability change. There is no permanent named-model ranking in this repository. Grok, Claude, Gemini, ChatGPT, local models and coding agents can all participate through the same evidence and candidate-file contracts. The current host agent can perform the whole workflow without an API gateway.

| Work | Default economic approach | Escalation trigger | Required evidence |
|---|---|---|---|
| Parse captures, classify files, normalize catalogs | Deterministic code first; small model only for ambiguous extraction | Missing fields, inconsistent classification, schema rejection | Exact source spans, schema validation, sampled recall audit |
| Research retrieval and reference triage | Cheap retrieval plus a qualified small model | Contradictory primary sources or material uncertainty | Dated primary links, relevance and evidence classification |
| Architecture and hidden behavior | Strongest qualified reasoning model within the authorized budget | A material unknown survives controlled experiments | Competing hypotheses, discriminating tests, explicit uncertainty |
| Implementation | Cheapest coding agent that passes the project's acceptance benchmark | Repeated failure, tenancy/data-loss issue, concurrency ambiguity | Real patch, baseline failure, regression and holdout receipts |
| Visual reconstruction | Qualified vision model for analysis; code for measurements | Unexplained layout/state differences | Paired screenshots at fixed viewport/state plus interaction tests |
| Security, money and migration review | Strong qualified reviewer and deterministic checks | Any unresolved high-impact failure | Negative authorization matrix, ledger invariants, restore proof |
| Documentation and summaries | Small model or current agent | Claims exceed evidence or source attribution is wrong | Link/field preservation and claim-level review |

Before choosing models, define a small representative target-specific evaluation set: extraction errors, hidden-state reasoning, patch acceptance, abstention, tool-call failures, latency, tokens and cost. Keep a separate holdout. Reject candidates that fail mandatory correctness, schema, privacy or capability gates, regardless of price. Pick the cheapest remaining candidate using measured total task cost, including retries, tool calls and review. Re-evaluate after model, prompt, tool or product changes. Do not equate a vendor's benchmark with this project's results.

Bound each role's attempts and token/cost allowance before provider calls. Reserve estimated maximum cost, reconcile actual usage, stop on budget exhaustion, and never silently downgrade a critical review. If no candidate qualifies within budget, hand off the exact unresolved question and required capability. Cache only immutable, non-sensitive results keyed by source, prompt, model, tool and policy versions. Never reuse another tenant's private context as a cheap cache hit.

The suite's `select-model` helper ranks supplied qualified candidates only. It intentionally makes no provider requests and incurs no model API cost. Quality labels and price inputs need external evidence. API accounting, gateways, credential brokers, inference hosting and training are separate integrations, not implemented billing guarantees. Current development uses the host agent and deterministic local checks; it has not run a cross-vendor model benchmark or purchased API calls.

Structured-output support reduces formatting errors but does not establish factual correctness or safe tool use. Check the selected provider's current contracts: [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [Claude structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output), and [xAI documentation](https://docs.x.ai/). Treat these as integration references; verify the exact model/account before adoption.
