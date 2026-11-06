# First pilot: reconstruct a CSV export

This is an illustrative experiment design, not a claim that a target was tested. Choose an application you own or can examine, and select a real CSV export. A small feature exposes the whole evidence-to-implementation loop without pretending a full application was cloned.

## Define the behavior

Record the exact app build and authorized account/role. Observe where export begins, how selection/filters affect records, whether the export reflects current or saved edits, and how progress/errors appear. Inspect the resulting bytes: columns/order, sorting, encoding/BOM, delimiter, quoting, newline, date/timezone, numerical precision, null/empty values and filename.

Ask whether export is synchronous, background or server-generated. Use UI observations and authorized request/response capture first. For Electron use module/IPC evidence; for a native exporter use Ghidra only if a specific formatting/selection rule cannot otherwise be established.

## Create a reference corpus

Use safe test records covering ordinary text, commas, quotes, newlines, Unicode, null/empty values, timestamps and large selections. Include permission denial, no matching rows, failed writes/downloads and duplicate/retried actions where applicable. Capture exact reference outputs and errors before implementation. Record which cases are inaccessible rather than fabricating outputs.

## Trace and specify

Create `R-EXPORT-001` for selection semantics, `R-EXPORT-002` for format, `R-EXPORT-003` for permissions and `R-EXPORT-004` for failure/retry behavior. Link each to evidence, proposed implementation locations and test IDs. If a native function is relevant, retain function identity, instructions/pseudocode, addresses and limitations. Do not infer the complete exporter from a string reference alone.

Write a behavioral specification independently of implementation. State whether exact byte equality or normalized record equality is required. Any normalization, such as a nondeterministic filename timestamp, must be explicit and justified by the acceptance contract.

## Allocate models and build

Use the current agent to inventory evidence, implement the exporter, investigate ambiguity and inspect the UI, within its actual capabilities. If it cannot inspect images or run tests, hand off that step explicitly. Hashes, CSV parsing, byte comparisons and coverage are deterministic code. No model switching is required.

Implement the real path from click to persisted/downloaded result. A hard-coded fixture is not a working exporter. Use the chosen database/provider test environment only if persistence is part of the feature.

## Compare and accept

Run the same corpus through both systems. Compare bytes or parsed records according to the specification, plus permissions, progress, errors and side effects. Emit PASS/FAIL/UNTESTED per requirement, all divergences, tested build/environment and evidence paths. Expand to the next feature only after the initial loop works or the remaining block is understood.

For greenfield work, replace the reference with a user-approved export contract. For AI behavior, replace exact equality with a suitable protected task-quality evaluation. For video, use a representative shot/layer/timeline pilot and complete replacement provenance before scaling generation.
