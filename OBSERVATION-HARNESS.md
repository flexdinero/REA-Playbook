# Offline deterministic observation comparison

[scripts/compare_observations.py](scripts/compare_observations.py) compares recorded reference and candidate observations against a frozen corpus using Python 3.10+ and its standard library. It never launches the target, runs an adapter, opens a browser, calls a model or contacts a service. You must collect the evidence first.

## Run

```text
python scripts/compare_observations.py --corpus CORPUS.json --reference REFERENCE.json --candidate CANDIDATE.json --evidence-root EVIDENCE_DIRECTORY
```

The command prints a JSON report. Exit 0 means all supplied required cases pass this exact comparator; exit 1 means a difference, missing/extra case, unobserved result or input/context mismatch; exit 2 means invalid input, mismatched baseline or invalid evidence provenance. Preserve the report alongside the capture records.

The CLI report includes SHA-256 identities for the exact corpus/reference/candidate file bytes parsed, so later edits can be distinguished from the inputs that produced the report. This binds the report to supplied files; it does not authenticate the capture process.

## Frozen corpus

Create this structure using real requirement IDs and lowercase SHA-256 values. Hashes in this illustration are placeholders and must be replaced. Hash inputs/context using a recorded serialization method; do not hash differently redacted or differently ordered inputs on each side and assume they match.

```json
{
  "schema_version": 1,
  "baseline_id": "contract-v1",
  "cases": [{
    "case_id": "create-contact-01",
    "requirement_ids": ["R-CONTACT-001"],
    "input_sha256": "REPLACE_WITH_64_LOWERCASE_HEX_CHARACTERS",
    "context_sha256": "REPLACE_WITH_64_LOWERCASE_HEX_CHARACTERS"
  }]
}
```

The shared context identifies equivalent fixture data, semantic role/tenant aliases, flags, time conditions, viewport/device and other contract-relevant state. Record the reference and candidate build separately; they need not have identical build IDs. A digest asserts alignment of the supplied context; the harness cannot independently verify that a live system actually had that state.

## Reference and candidate capture files

Each file has `schema_version`, the same `baseline_id`, and a `cases` list. An observed case contains:

```json
{
  "case_id": "create-contact-01",
  "input_sha256": "REPLACE_WITH_64_LOWERCASE_HEX_CHARACTERS",
  "context_sha256": "REPLACE_WITH_64_LOWERCASE_HEX_CHARACTERS",
  "status": "observed",
  "source": {
    "build_id": "actual-build-identity",
    "run_id": "actual-capture-run",
    "artifact_path": "reference/create-contact-01.txt",
    "artifact_sha256": "REPLACE_WITH_REAL_ARTIFACT_SHA256"
  },
  "observation": {
    "output": {"created": true},
    "effects": [{"contact_count_delta": 1}],
    "error": null
  }
}
```

`artifact_path` must resolve to a file within the explicit evidence root. The script verifies its bytes against the supplied hash. `output`, `effects` and `error` must all be present, including explicit null/empty values where appropriate. A case that was not executed uses `not_observed` or `blocked`; neither can pass. Duplicate case IDs/JSON keys and non-finite JSON values are rejected.

Define the adapter that extracts these observations, document how it accounts for durable effects and test it independently. An unchanged raw artifact hash does not prove that an adapter's hand-written JSON faithfully represents that artifact. The collector, adapter, fixture and oracle all remain part of the assurance case.

## Comparison semantics

The oracle `exact-json-observation-v1` ignores object-key order, preserves array order and uses strict JSON serialization for values. Boolean true differs from integer 1; integer 1 differs from floating representation 1.0. No fields are masked or normalized automatically. Fields outside the three observation members are metadata and are not behaviorally compared; their existence must not imply coverage of unrecorded behavior.

Empty corpora cannot pass. Missing observations cannot pass even if missing on both sides. Unexpected cases prevent complete match so a changed suite cannot silently alter the denominator. Only cases listed in the frozen corpus contribute required-case coverage. A passing case links to requirement IDs; it does not prove that those cases exhaust every requirement.

## Select another oracle when needed

Use dedicated tolerance/units checks for numerical contracts; image/time-series metrics plus interaction tests for visuals/media; repeated-trial statistical evaluation for AI; and consistency/history checking for concurrent systems. Preserve raw evidence and explicitly justify any transformation. Do not weaken this comparator or drop meaningful fields to force an inappropriate test to pass.

## Verify the harness

```text
python -m unittest discover -s tests -v
```

The failure-oriented tests use synthetic temporary fixtures. They verify match/difference/invalid exit behavior, missing/extra cases, wrong input context, unexecuted records, evidence changes, path confinement, strict value comparison and event order. Their results are evidence about this harness, not about GoHighLevel or any other target.
