import json
import os
import stat
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest

from recreator.storage import Workspace, SuiteError, sha
from recreator.engine import Suite
from recreator.models import select_model


class SuiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'target'
        self.repo.mkdir()
        (self.repo / 'app.txt').write_text('broken', encoding='utf-8')
        (self.repo / 'check.py').write_text("from pathlib import Path\nassert Path('app.txt').read_text() == 'fixed'\n", encoding='utf-8')
        self.manifest = {'project_id': 'owned-fixture', 'repo': str(self.repo),
                         'repair_budget': 2, 'editable': ['app.txt'], 'protected': ['check.py'],
                         'profiles': {'acceptance': {'cwd': '.', 'argv': [sys.executable, 'check.py'], 'timeout_seconds': 5},
                                      'holdout': {'cwd': '.', 'argv': [sys.executable, '-c', "from pathlib import Path; assert len(Path('app.txt').read_text()) == 5"], 'timeout_seconds': 5}}}
        self.workspace = Workspace(self.root / 'private')
        self.suite = Suite.initialize(self.workspace, self.manifest, b'{"cases":["fixture"]}')

    def test_refuses_implicit_execution(self):
        with self.assertRaises(SuiteError):
            self.suite.run(['acceptance'])

    def test_receipt_is_real_and_protected_inputs_are_frozen(self):
        receipt = self.suite.run(['acceptance'], trusted_local=True)
        self.assertFalse(receipt['passed'])
        self.assertIn('AssertionError', self.workspace.get(receipt['results'][0]['artifact']).decode())
        (self.repo / 'check.py').write_text('pass', encoding='utf-8')
        with self.assertRaises(SuiteError):
            self.suite.run(['acceptance'], trusted_local=True)

    def test_repair_accepts_only_after_baseline_failure_and_holdout(self):
        repair = self.suite.repair('app.txt', sha(b'broken'), b'fixed', ['acceptance', 'holdout'], trusted_local=True)
        self.assertEqual(repair['status'], 'accepted')
        self.assertEqual((self.repo / 'app.txt').read_bytes(), b'fixed')
        self.assertFalse(self.workspace.read().get('pending_repair'))

    def test_rejected_candidate_rolls_back_and_budget_is_enforced(self):
        for _ in range(2):
            repair = self.suite.repair('app.txt', sha(b'broken'), b'wrong', ['acceptance', 'holdout'], trusted_local=True)
            self.assertEqual(repair['status'], 'reverted')
            self.assertEqual((self.repo / 'app.txt').read_bytes(), b'broken')
        with self.assertRaises(SuiteError):
            self.suite.repair('app.txt', sha(b'broken'), b'fixed', ['acceptance', 'holdout'], trusted_local=True)

    def test_no_passing_baseline_repair_or_protected_edit(self):
        (self.repo / 'app.txt').write_bytes(b'fixed')
        with self.assertRaises(SuiteError):
            self.suite.repair('app.txt', sha(b'fixed'), b'wrong', ['acceptance', 'holdout'], trusted_local=True)
        with self.assertRaises(SuiteError):
            self.suite.repair('check.py', sha((self.repo / 'check.py').read_bytes()), b'pass', ['acceptance'], trusted_local=True)

    def test_pending_repair_recovery_checks_current_file(self):
        original = self.workspace.put(b'broken')
        self.workspace.update('fixture_interruption', {}, lambda s: s.update(pending_repair={'id': 'interrupted', 'path': 'app.txt', 'before': original, 'candidate': sha(b'fixed')}))
        (self.repo / 'app.txt').write_bytes(b'fixed')
        result = self.suite.recover()
        self.assertEqual(result['status'], 'recovered')
        self.assertEqual((self.repo / 'app.txt').read_bytes(), b'broken')

    def test_lessons_cannot_promote_from_reflection_alone(self):
        lesson = self.suite.propose_lesson('Check restart continuity', 'restore state before retry', [])
        with self.assertRaises(SuiteError):
            self.suite.promote_lesson(lesson['id'], 'reviewer', [])

    def test_workspace_detects_corruption_and_writer_collision(self):
        with self.workspace.locked():
            with self.assertRaises(SuiteError):
                self.workspace.update('collision', {}, lambda s: None)
        raw = json.loads(self.workspace.state_path.read_text())
        raw['phase'] = 'forged'
        self.workspace.state_path.write_text(json.dumps(raw))
        with self.assertRaises(SuiteError):
            self.workspace.read()

    def test_learning_promotes_disjoint_holdouts_and_revokes(self):
        # Separate scenario identities must be frozen before evaluation.
        with tempfile.TemporaryDirectory() as directory:
            manifest = dict(self.manifest)
            manifest['profiles'] = dict(self.manifest['profiles'])
            manifest['profiles']['holdout'] = dict(manifest['profiles']['holdout'], kind='holdout', case_ids=['heldout-a'])
            manifest['profiles']['holdout_b'] = dict(manifest['profiles']['holdout'], case_ids=['heldout-b'])
            workspace = Workspace(directory)
            suite = Suite.initialize(workspace, manifest, b'heldout-fixture')
            (self.repo / 'app.txt').write_bytes(b'fixed')
            evidence = workspace.put(b'independent fixture review')
            lesson = suite.propose_lesson('Example fixture', 'Scoped tested procedure', [evidence])
            first = suite.run(['holdout'], trusted_local=True)
            repeated = suite.run(['holdout'], trusted_local=True)
            with self.assertRaises(SuiteError):
                suite.promote_lesson(lesson['id'], 'fixture-reviewer', [first['id'], repeated['id']])
            second = suite.run(['holdout_b'], trusted_local=True)
            self.assertEqual(suite.promote_lesson(lesson['id'], 'fixture-reviewer', [first['id'], second['id']])['status'], 'promoted')
            self.assertEqual(len(suite.handoff()['lessons']), 1)
            suite.revoke_lesson(lesson['id'], 'new contradictory evidence')
            self.assertEqual(suite.handoff()['lessons'], [])

    def test_escape_and_missing_holdout_rejected(self):
        with self.assertRaises(SuiteError):
            self.suite.repair('../elsewhere', sha(b'broken'), b'fixed', ['acceptance', 'holdout'], trusted_local=True)
        with self.assertRaises(SuiteError):
            self.suite.repair('app.txt', sha(b'broken'), b'fixed', ['acceptance'], trusted_local=True)

    def test_cheapest_qualified_model_and_no_silent_fallback(self):
        candidates = [
            {'id': 'cheap-unqualified', 'capabilities': ['code'], 'quality_passed': False, 'cost_per_task': 0.01},
            {'id': 'qualified-small', 'capabilities': ['code'], 'quality_passed': True, 'cost_per_task': 0.04},
            {'id': 'qualified-large', 'capabilities': ['code', 'vision'], 'quality_passed': True, 'cost_per_task': 0.5}]
        self.assertEqual(select_model(candidates, ['code'], 1)['id'], 'qualified-small')
        self.assertEqual(select_model(candidates, ['vision'], 1)['id'], 'qualified-large')
        with self.assertRaises(SuiteError):
            select_model(candidates, ['vision'], 0.1)

    def test_hypotheses_require_real_evidence_and_competing_explanations(self):
        evidence = self.suite.record_evidence(b'observed restart response', 'observed', 'owned fixture', 'state survives restart')
        hypothesis = self.suite.hypothesis('wait continuation', ['persisted cursor', 'volatile timer'], 'restart before due time', [evidence['id']])
        self.assertEqual(hypothesis['status'], 'untested')
        with self.assertRaises(SuiteError):
            self.suite.resolve_hypothesis(hypothesis['id'], 0, [], 'supported')
        resolved = self.suite.resolve_hypothesis(hypothesis['id'], 0, [evidence['id']], 'supported')
        self.assertEqual(resolved['status'], 'supported')

    def test_command_cannot_silently_modify_tracked_source(self):
        manifest = dict(self.manifest)
        manifest['profiles'] = dict(self.manifest['profiles'], acceptance={'cwd':'.', 'argv':[sys.executable, '-c', "from pathlib import Path; Path('app.txt').write_text('fixed')"], 'timeout_seconds':5})
        workspace = Workspace(self.root / 'mutating-private')
        suite = Suite.initialize(workspace, manifest, b'fixture')
        with self.assertRaises(SuiteError):
            suite.run(['acceptance'], trusted_local=True)

    def test_cli_run_reports_failure_then_handoff_resumes_state(self):
        command = [sys.executable, '-m', 'recreator', '--workspace', str(self.workspace.root)]
        failed = subprocess.run([*command, 'run', '--profiles', 'acceptance', '--trusted-local'], capture_output=True, text=True)
        self.assertEqual(failed.returncode, 1, failed.stderr)
        self.assertFalse(json.loads(failed.stdout)['passed'])
        handoff = subprocess.run([*command, 'handoff'], capture_output=True, text=True)
        self.assertEqual(handoff.returncode, 0, handoff.stderr)
        self.assertEqual(json.loads(handoff.stdout)['project_id'], 'owned-fixture')

    def test_recovery_does_not_overwrite_unrelated_user_edit(self):
        original = self.workspace.put(b'broken')
        self.workspace.update('interrupted', {}, lambda s: s.update(pending_repair={'id':'x','path':'app.txt','before':original,'candidate':sha(b'fixed')}))
        (self.repo / 'app.txt').write_bytes(b'user work')
        with self.assertRaises(SuiteError):
            self.suite.recover()
        self.assertEqual((self.repo / 'app.txt').read_bytes(), b'user work')

    @unittest.skipUnless(os.name == 'posix', 'POSIX permission semantics')
    def test_repairs_and_rollback_preserve_executable_mode(self):
        target = self.repo / 'app.txt'
        target.chmod(0o740)
        self.suite.repair('app.txt', sha(b'broken'), b'fixed', ['acceptance', 'holdout'], trusted_local=True)
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o740)
        target.write_bytes(b'broken')
        self.suite.repair('app.txt', sha(b'broken'), b'wrong', ['acceptance', 'holdout'], trusted_local=True)
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o740)


if __name__ == '__main__':
    unittest.main()
