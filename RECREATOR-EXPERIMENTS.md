# Executable reconstruction experiments

The `experiment` command connects frozen experiment definitions, actual target
adapter execution, retained receipts and deterministic comparison. It uses the
existing private workspace and protected manifest. It does not discover an
unknown feature automatically or turn an implementation choice into a capture.

Each packet declares `schema_version: 1`, `baseline_id`, `oracle_basis` and
`cases`. The oracle basis is `captured-reference`, `explicit-contract` or
`derived-invariant`. Every case supplies `case_id`, nonempty `requirement_ids`,
`input_sha256`, `context_sha256`, `prepare_profile` and `observe_profile`.
The last two names must identify separate commands in the frozen manifest.
The packet permits 1â€“20 cases and at most 600 seconds of declared command time.

The reference uses the recorded-observation format described in
[the comparator instructions](OBSERVATION-HARNESS.md). It must cover every case
with the same input/context identities, explicit output/effects/error and valid
raw evidence hashes. It is validated before commands run and copied into the
private artifact store. The packet and reference are retained by content hash.

```text
python -m recreator --workspace C:/private/target-runtime experiment --packet C:/private/experiment/packet.json --reference C:/private/experiment/reference.json --evidence-root C:/private/experiment --trusted-local
```

Preparation must reset/establish the case's actual starting conditions, verify
their postconditions and emit one JSON object with `ready: true`, `input_sha256`
and `context_sha256`. A fresh owned fixture can implement reset. An adapter which
merely prints `ready` without checking its conditions is an invalid experiment.
The observation command emits one JSON object with those same digests and
`observation: {"output": ..., "effects": ..., "error": ...}`. Put diagnostic
logs on stderr. Each command must exit zero; truncated output is rejected.
Expected product errors belong in the observation's error field, with the
adapter itself still exiting zero after successfully collecting the evidence.

Reset failure prevents the observation command for that case. Missing/malformed
observations cannot pass. Candidate source and protected dependencies must remain
stable across stages. The final report includes real run IDs, candidate artifact,
comparison, failures and oracle basis. Exit zero means a match over these supplied
cases; exit one means an executed mismatch/failure; invalid setup exits two.
Experimental diagnostics never replace the manifest's mandatory acceptance gates.

Review adapters independently: digests identify declared inputs, not proof that a
command used them faithfully. Raw artifacts establish byte identity, not truth.
For GHL, a round-trip invariant is useful evidence about the candidate; it is not
equivalent to observing HighLevel execute that round trip. Preserve hypothesis
alternatives and distinguish contradiction from insufficient observation.

The runner persists each stage attempt, captured output and receipt linkage.
Captured output is indexed before source-integrity checks, so an integrity failure
does not orphan that evidence. A run ID and attempt context let an interrupted
caller locate a committed receipt even before the caller updates its stage status.
A crash before output capture can still leave an uncertain attempted action.
The runner is single-controller and does not automatically resume interrupted
experiments. A retained `started` record requires inspection of stage records,
actual run receipts and possible external outcomes before another run. There is no automatic
rollback of reset commands or provider effects. Use owned fixtures or separately
authorized sandboxes. Trusted-local execution retains the host-access limitations
in [operations](RECREATOR-OPERATIONS.md); Docker still requires deployment proof.
This release does not automatically choose hypotheses, schedule experiments,
perform statistical tests or promote lessons from an experimental match.
