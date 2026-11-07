# Audit a product's discovery graph

This extension turns the [discovery process](RECREATOR-DISCOVERY.md) into a
deterministic audit over an explicitly supplied graph. It does not automatically
discover every feature, collect account data or infer architecture from names.

The version-one graph contains `schema_version`, `scope`, `nodes`, `edges` and
`evidence`. Node IDs and edge IDs are unique. Nodes declare `type`, `title`,
`basis` (observed/inferred/proposed/unknown), `mandatory`, `discovery`
(unexplored/partial/mapped), `implementation` (not_started/partial/implemented),
`verification` (unverified/verified), `evidence_ids`, `required_links` and
`verification_checks`. An explicitly declared boundary may explain why a leaf
has no further required relationships. Optional open questions remain visible.

Each required link declares `relation`, `direction` (in/out), `target_type` and
`minimum_basis` (observed/any). An edge declares `from`, `to`, `relation`, `basis`
and `evidence_ids`. Inferred links cannot satisfy an observed-link requirement.
Observed claims default to `observation_kind: runtime`, requiring observation or
execution-receipt evidence. Explicit `observation_kind: source` permits source
inspection claims but cannot satisfy a runtime-link requirement. Required links
may explicitly request source observation; their default is runtime. A source
summary is not promoted to runtime observation merely because it describes one.
An unresolved `contradicts` edge remains a finding until resolution evidence is
provided. Cycles are allowed: feedback and iterative workflows are legitimate.

Evidence records declare `id`, relative `path`, `sha256`, `kind` (source,
observation or execution_receipt), `source`, `recorded_at` and `scope`. Every raw
file hash is checked and paths must stay inside the evidence root. Execution
receipts use the existing Suite.run format and retain their sibling `artifacts/`
directory. Verification checks name `evidence_id` and `profile`. A verified node
requires at least one actual successful, nontruncated check; contradictory exit
or timeout flags are rejected. The reviewer remains responsible for whether that
check actually proves the node's claimed behavior. Hashes do not prove provenance.

The audit reports unexplored mandatory nodes, incomplete implementation or
verification, unsupported observation claims, missing required links, unresolved
questions/contradictions and undeclared leaf boundaries. Its result is
`declared_scope_satisfied`, never a whole-product completeness percentage.
The graph's scope and denominator are supplied inventory, not independently
discovered truth. A graph can be structurally coherent and omit a real feature.

Read-only command (no target code execution):

```text
python -m recreator --workspace C:/private/runtime audit-graph --document C:/private/graph.json --evidence-root C:/private/project
```

Exit zero means the supplied declared scope has no reported findings. Exit one
means open findings; exit two means malformed or corrupt inputs. Retain the graph
digest and report with the reviewed target revision. Update the graph when new
clues appear; do not delete unknown nodes or weaken required links to manufacture
completion. This is a discovery/traceability diagnostic, not a replacement for
independent product tests, live comparisons or production acceptance.

Input bounds: 8 MiB graph document through the CLI, 5,000 nodes, 10,000 edges,
1,000 evidence records, 32 MiB per evidence file and 64 MiB total distinct evidence
bytes including execution artifacts. Large captures need a separately reviewed
external evidence adapter; this command does not silently skip them.
