"""Failure-oriented checks for the offline comparison harness, not a target clone."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import compare_observations as harness


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        evidence = b"synthetic fixture evidence; not a captured target"
        (self.root / "raw.txt").write_bytes(evidence)
        self.spec = {"case_id": "create-1", "requirement_ids": ["R1"],
                     "input_sha256": "a" * 64, "context_sha256": "b" * 64}
        self.corpus = {"schema_version": 1, "baseline_id": "B1", "cases": [self.spec]}
        row = {"case_id": "create-1", "input_sha256": "a" * 64, "context_sha256": "b" * 64,
               "status": "observed", "source": {"build_id": "reference-v1", "run_id": "run-1",
               "artifact_path": "raw.txt", "artifact_sha256": hashlib.sha256(evidence).hexdigest()},
               "observation": {"output": {"ok": True}, "effects": [{"record_count": 1}], "error": None}}
        self.reference = {"schema_version": 1, "baseline_id": "B1", "cases": [row]}
        self.candidate = deepcopy(self.reference)
        self.candidate["cases"][0]["source"]["build_id"] = "candidate-v1"

    def result(self):
        return harness.compare(self.corpus, self.reference, self.candidate, self.root)

    def status(self):
        result = self.result()
        self.assertFalse(result["complete_match"])
        return result["cases"][0]["status"]

    def test_equal_complete_corpus_passes(self):
        self.assertTrue(self.result()["complete_match"])

    def test_wrong_durable_effect_fails(self):
        self.candidate["cases"][0]["observation"]["effects"][0]["record_count"] = 2
        self.assertEqual(self.status(), "DIFFERENT")

    def test_bool_and_integer_are_not_equal(self):
        self.candidate["cases"][0]["observation"]["output"]["ok"] = 1
        self.assertEqual(self.status(), "DIFFERENT")

    def test_event_order_is_not_ignored(self):
        self.reference["cases"][0]["observation"]["effects"] = [1, 2]
        self.candidate["cases"][0]["observation"]["effects"] = [2, 1]
        self.assertEqual(self.status(), "DIFFERENT")

    def test_missing_both_sides_does_not_pass(self):
        self.reference["cases"] = []
        self.candidate["cases"] = []
        self.assertEqual(self.status(), "MISSING_OBSERVATION")

    def test_extra_case_does_not_pass(self):
        extra = deepcopy(self.candidate["cases"][0])
        extra["case_id"] = "unexpected"
        self.candidate["cases"].append(extra)
        self.assertFalse(self.result()["complete_match"])
        self.assertEqual(self.result()["cases"][-1]["status"], "UNEXPECTED_CASE")

    def test_matching_wrong_context_does_not_pass(self):
        for side in (self.reference, self.candidate):
            side["cases"][0]["context_sha256"] = "c" * 64
        self.assertEqual(self.status(), "INPUT_OR_CONTEXT_MISMATCH")

    def test_unexecuted_record_does_not_pass(self):
        self.candidate["cases"][0]["status"] = "not_observed"
        self.assertEqual(self.status(), "NOT_OBSERVED")

    def test_changed_artifact_is_rejected(self):
        (self.root / "raw.txt").write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            self.result()

    def test_artifact_cannot_escape_root(self):
        self.candidate["cases"][0]["source"]["artifact_path"] = "../outside.txt"
        with self.assertRaisesRegex(ValueError, "escapes"):
            self.result()

    def test_observation_cannot_omit_effects(self):
        del self.candidate["cases"][0]["observation"]["effects"]
        with self.assertRaisesRegex(ValueError, "output, effects and error"):
            self.result()

    def test_empty_corpus_rejected(self):
        self.corpus["cases"] = []
        with self.assertRaisesRegex(ValueError, "Empty corpus"):
            self.result()

    def test_duplicate_case_ids_rejected(self):
        self.candidate["cases"].append(deepcopy(self.candidate["cases"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate case_id"):
            self.result()

    def test_baseline_mismatch_rejected(self):
        self.candidate["baseline_id"] = "B2"
        with self.assertRaisesRegex(ValueError, "Baseline"):
            self.result()

    def test_duplicate_json_keys_and_nan_rejected(self):
        for value in ('{"schema_version":1,"schema_version":2}', '{"value":NaN}', '{"value":1e999}'):
            file = self.root / "bad.json"
            file.write_text(value, encoding="utf-8")
            with self.assertRaises(ValueError):
                harness.load(file)

    def test_cli_exit_codes_match_pass_difference_and_invalid(self):
        paths = {name: self.root / f"{name}.json" for name in ("corpus", "reference", "candidate")}
        def run():
            for name, path in paths.items():
                path.write_text(json.dumps(getattr(self, name)), encoding="utf-8")
            return subprocess.run([sys.executable, str(ROOT / "scripts/compare_observations.py"),
                                   "--corpus", str(paths["corpus"]), "--reference", str(paths["reference"]),
                                   "--candidate", str(paths["candidate"]), "--evidence-root", str(self.root)],
                                  capture_output=True, text=True, check=False)
        passed = run()
        self.assertEqual(passed.returncode, 0)
        self.assertEqual(json.loads(passed.stdout)["input_files_sha256"],
                         {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()})
        self.candidate["cases"][0]["observation"]["error"] = "unexpected error"
        self.assertEqual(run().returncode, 1)
        self.candidate["baseline_id"] = "wrong"
        self.assertEqual(run().returncode, 2)


if __name__ == "__main__":
    unittest.main()
