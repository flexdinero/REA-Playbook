"""Executed adapter experiments; synthetic fixtures are not vendor observations."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest import mock

from recreator.engine import Suite
from recreator.storage import Workspace, canonical, sha
from recreator.experiments import execute_experiment


class ExperimentTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = self.root / 'target'
        self.repo.mkdir()
        self.workspace = Workspace(self.root / 'private')
        self.case = {'case_id': 'save', 'requirement_ids': ['save-roundtrip'],
                     'input_sha256': sha(b'input'), 'context_sha256': sha(b'context')}
        self.observation = {'output': {'saved': True}, 'effects': ['persisted'], 'error': None}
        self.ready = dict(ready=True, input_sha256=self.case['input_sha256'], context_sha256=self.case['context_sha256'])
        self.payload = dict(input_sha256=self.case['input_sha256'], context_sha256=self.case['context_sha256'], observation=self.observation)
        self.packet = {'schema_version': 1, 'baseline_id': 'owned-fixture-v1',
                       'oracle_basis': 'explicit-contract', 'cases': [dict(self.case, prepare_profile='prepare', observe_profile='observe')]}
        self.raw = self.root / 'reference.txt'
        self.raw.write_bytes(b'independent synthetic expected contract')
        self.reference = {'schema_version': 1, 'baseline_id': 'owned-fixture-v1', 'cases': [dict(
            self.case, status='observed', observation=deepcopy(self.observation), source={
                'build_id': 'fixture-contract-v1', 'run_id': 'fixture-reference',
                'artifact_path': 'reference.txt', 'artifact_sha256': sha(self.raw.read_bytes())})]}

    def initialize(self, prepare=None, observe=None):
        scripts = {'prepare': prepare or 'print(' + repr(json.dumps(self.ready)) + ')',
                   'observe': observe or 'print(' + repr(json.dumps(self.payload)) + ')'}
        profiles = {}
        for name, source in scripts.items():
            (self.repo / (name + '.py')).write_text(source, encoding='utf-8')
            profiles[name] = {'cwd': '.', 'argv': [sys.executable, name + '.py'], 'timeout_seconds': 5}
        (self.repo / 'app.txt').write_text('candidate', encoding='utf-8')
        profiles['acceptance'] = deepcopy(profiles['observe'])
        profiles['holdout'] = deepcopy(profiles['observe'])
        manifest = {'project_id': 'experiment-fixture', 'repo': str(self.repo), 'repair_budget': 1,
                    'editable': ['app.txt'], 'protected': ['prepare.py', 'observe.py'], 'profiles': profiles}
        self.suite = Suite.initialize(self.workspace, manifest, canonical(self.packet).encode())

    def execute(self):
        return execute_experiment(self.suite, self.packet, self.reference, self.root, trusted_local=True)

    def test_real_adapter_output_matches_and_is_retained(self):
        self.initialize()
        report = self.execute()
        self.assertTrue(report['passed'])
        self.assertEqual(report['oracle_basis'], 'explicit-contract')
        self.assertEqual(len(report['run_ids']), 2)
        self.assertIn(report['id'], self.workspace.read()['experiments'])
        candidate = json.loads(self.workspace.get(report['candidate_artifact']))
        self.assertEqual(candidate['cases'][0]['observation'], self.observation)

    def test_wrong_effect_is_a_counterexample(self):
        self.payload['observation']['effects'] = ['lost']
        self.initialize()
        report = self.execute()
        self.assertFalse(report['passed'])
        self.assertEqual(report['comparison']['cases'][0]['different_fields'], ['effects'])

    def test_failed_preparation_does_not_execute_observer(self):
        self.initialize(prepare='raise SystemExit(1)')
        report = self.execute()
        self.assertFalse(report['passed'])
        self.assertEqual(len(report['run_ids']), 1)
        self.assertEqual(report['failures'][0]['stage'], 'prepare')

    def test_reset_claim_requires_bound_context_and_exact_true(self):
        self.ready['ready'] = 1
        self.initialize()
        report = self.execute()
        self.assertFalse(report['passed'])
        self.assertEqual(len(report['run_ids']), 1)

    def test_malformed_or_mismatched_observation_cannot_pass(self):
        self.payload['context_sha256'] = '0' * 64
        self.initialize()
        report = self.execute()
        self.assertFalse(report['passed'])
        self.assertEqual(report['comparison']['cases'][0]['status'], 'NOT_OBSERVED')

    def test_bad_reference_stops_before_execution(self):
        self.initialize()
        self.raw.write_bytes(b'changed')
        with self.assertRaises(ValueError):
            self.execute()
        self.assertFalse(self.workspace.read()['runs'])

    def test_implicit_execution_refused_before_recording_start(self):
        self.initialize()
        with self.assertRaises(ValueError):
            execute_experiment(self.suite, self.packet, self.reference, self.root)
        self.assertFalse(self.workspace.read()['runs'])

    def test_json_log_noise_is_not_an_observation(self):
        self.initialize(observe='print("adapter log without JSON")')
        report = self.execute()
        self.assertFalse(report['passed'])
        self.assertEqual(report['failures'][0]['stage'], 'observe')

    def test_output_truncation_cannot_produce_a_pass(self):
        self.initialize(observe='print("x" * (2 * 1024 * 1024 + 1))')
        report = self.execute()
        self.assertFalse(report['passed'])
        self.assertIn('truncated', report['failures'][0]['error'])

    def test_source_mutation_during_reset_blocks_observer(self):
        self.initialize(prepare="from pathlib import Path; Path('app.txt').write_text('changed'); print('mutation evidence')")
        report = self.execute()
        self.assertFalse(report['passed'])
        self.assertEqual(len(report['run_ids']), 0)
        self.assertEqual(report['failures'][0]['stage'], 'prepare')
        attempt = report['stages'][0]
        self.assertIn('mutation evidence', json.loads(self.workspace.get(attempt['execution_artifact']))['stdout'])
        self.assertFalse(attempt['receipt_committed'])

    def test_interruption_preserves_completed_stage_identity(self):
        self.initialize()
        original = self.suite.run
        def interrupted(*args, **kwargs):
            original(*args, **kwargs)
            raise KeyboardInterrupt('after receipt commit, before caller linkage')
        with mock.patch.object(self.suite, 'run', side_effect=interrupted):
            with self.assertRaises(KeyboardInterrupt):
                self.execute()
        state = self.workspace.read()
        experiment = next(iter(state['experiments'].values()))
        attempt = experiment['stages'][0]
        self.assertEqual(attempt['case_id'], 'save')
        self.assertEqual(attempt['stage'], 'prepare')
        receipt = state['runs'][attempt['run_id']]
        self.assertEqual(receipt['context']['attempt_id'], attempt['id'])
        self.assertEqual(attempt['execution_artifact'], receipt['results'][0]['artifact'])

    def test_cli_executes_the_same_evidence_path(self):
        self.initialize()
        for name, value in [('packet.json', self.packet), ('reference.json', self.reference)]:
            (self.root / name).write_text(json.dumps(value), encoding='utf-8')
        result = subprocess.run([sys.executable, '-m', 'recreator', '--workspace', str(self.workspace.root),
                                 'experiment', '--packet', str(self.root / 'packet.json'),
                                 '--reference', str(self.root / 'reference.json'), '--evidence-root', str(self.root),
                                 '--trusted-local'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['passed'])


if __name__ == '__main__':
    unittest.main()
