"""Compare a frozen deterministic corpus; never execute target or adapter code."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError(f"Non-finite JSON constant: {value}")


def load_with_digest(path):
    raw = Path(path).read_bytes()
    document = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                          parse_constant=invalid_constant)
    canonical(document)  # Also reject numeric overflow such as 1e999 in metadata.
    return document, hashlib.sha256(raw).hexdigest()


def load(path):
    return load_with_digest(path)[0]


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def digest(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def rows(document, kind):
    require(isinstance(document, dict), f"{kind}: expected object")
    require(type(document.get("schema_version")) is int and document["schema_version"] == 1,
            f"{kind}: unsupported schema_version")
    require(text(document.get("baseline_id")), f"{kind}: missing baseline_id")
    require(isinstance(document.get("cases"), list), f"{kind}: cases must be a list")
    result = {}
    for row in document["cases"]:
        require(isinstance(row, dict) and text(row.get("case_id")), f"{kind}: missing case_id")
        key = row["case_id"]
        require(key not in result, f"{kind}: duplicate case_id {key}")
        result[key] = row
    return result


def validate_evidence(row, root):
    source = row.get("source")
    require(isinstance(source, dict), "Observed case lacks source")
    require(text(source.get("build_id")) and text(source.get("run_id")),
            "Observed case lacks build/run identity")
    require(text(source.get("artifact_path")) and digest(source.get("artifact_sha256")),
            "Observed case lacks artifact path/hash")
    path = Path(source["artifact_path"])
    require(not path.is_absolute() and not path.drive, "Artifact must use a relative path")
    resolved = (root / path).resolve()
    require(resolved.is_relative_to(root), "Artifact escapes evidence root")
    require(resolved.is_file(), "Evidence artifact missing")
    with resolved.open("rb") as handle:
        hasher = hashlib.sha256()
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    require(hasher.hexdigest() == source["artifact_sha256"], "Evidence artifact hash mismatch")
    observation = row.get("observation")
    require(isinstance(observation, dict) and set(observation) == {"output", "effects", "error"},
            "Observation must explicitly contain output, effects and error")
    canonical(observation)


def compare(corpus, reference, candidate, evidence_root):
    expected = rows(corpus, "corpus")
    require(expected, "Empty corpus cannot establish a pass")
    left = rows(reference, "reference")
    right = rows(candidate, "candidate")
    require(corpus["baseline_id"] == reference["baseline_id"] == candidate["baseline_id"],
            "Baseline identity mismatch")
    root = Path(evidence_root).resolve()
    require(root.is_dir(), "Evidence root is not a directory")
    for key, spec in expected.items():
        require(digest(spec.get("input_sha256")) and digest(spec.get("context_sha256")),
                f"Corpus {key}: input/context digest required")
        ids = spec.get("requirement_ids")
        require(isinstance(ids, list) and ids and all(text(item) for item in ids),
                f"Corpus {key}: nonempty requirement_ids required")
        require(len(ids) == len(set(ids)), f"Corpus {key}: repeated requirement ID")
    for side in (left, right):
        for row in side.values():
            require(row.get("status") in {"observed", "not_observed", "blocked"},
                    "Unknown observation status")
            require(digest(row.get("input_sha256")) and digest(row.get("context_sha256")),
                    "Observation lacks input/context digests")
            if row["status"] == "observed":
                validate_evidence(row, root)

    results = []
    for key in sorted(set(expected) | set(left) | set(right)):
        spec = expected.get(key)
        a, b = left.get(key), right.get(key)
        different = []
        if spec is None:
            status = "UNEXPECTED_CASE"
        elif a is None or b is None:
            status = "MISSING_OBSERVATION"
        elif any(row[field] != spec[field] for row in (a, b)
                 for field in ("input_sha256", "context_sha256")):
            status = "INPUT_OR_CONTEXT_MISMATCH"
        elif a["status"] != "observed" or b["status"] != "observed":
            status = "NOT_OBSERVED"
        else:
            different = [field for field in ("output", "effects", "error")
                         if canonical(a["observation"][field]) != canonical(b["observation"][field])]
            status = "DIFFERENT" if different else "PASS"
        results.append({"case_id": key, "requirement_ids": spec["requirement_ids"] if spec else [],
                        "status": status, "different_fields": different})
    passed = sum(row["status"] == "PASS" for row in results)
    return {"schema_version": 1, "baseline_id": corpus["baseline_id"],
            "oracle": "exact-json-observation-v1", "required_cases": len(expected),
            "passing_cases": passed, "complete_match": all(row["status"] == "PASS" for row in results),
            "limits": ["Only the frozen supplied cases and recorded observation fields are compared.",
                       "Artifact hashes establish byte integrity, not truthful capture or oracle correctness.",
                       "No target execution, statistical testing, normalization or universal equivalence proof occurs."],
            "cases": results}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--reference", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--evidence-root", required=True)
    args = parser.parse_args(argv)
    try:
        inputs = {name: load_with_digest(getattr(args, name))
                  for name in ("corpus", "reference", "candidate")}
        report = compare(*(inputs[name][0] for name in ("corpus", "reference", "candidate")),
                         args.evidence_root)
        report["input_files_sha256"] = {name: value[1] for name, value in inputs.items()}
    except (ValueError, OSError, TypeError, KeyError) as error:
        print(json.dumps({"complete_match": False, "error": str(error)}), file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if report["complete_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
