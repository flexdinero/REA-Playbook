"""Counterexamples for graph omissions and unsupported closure claims."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

from recreator.discovery import audit_graph
from recreator.storage import sha


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / 'notes.txt').write_bytes(b'owned synthetic source')
        (self.root / 'artifacts').mkdir()
        self.execution = {'exit_code': 0, 'timed_out': False, 'passed': True,
                          'output_truncated': False, 'stdout': 'actual fixture output', 'stderr': ''}
        self.write_receipt()
        self.graph = {'schema_version': 1, 'scope': 'synthetic two-node declared scope',
                      'evidence': [self.evidence('notes', 'notes.txt', 'observation'),
                                   self.evidence('run', 'receipt.json', 'execution_receipt')],
                      'nodes': [self.node('action', 'ui'), self.node('api', 'api')],
                      'edges': [{'id': 'call', 'from': 'action', 'to': 'api', 'relation': 'invokes',
                                 'basis': 'observed', 'evidence_ids': ['notes']}]}
        self.graph['nodes'][0]['required_links'] = [{'relation': 'invokes', 'direction': 'out',
                                                   'target_type': 'api', 'minimum_basis': 'observed'}]

    def evidence(self, identity, path, kind):
        return {'id': identity, 'path': path, 'sha256': sha((self.root / path).read_bytes()),
                'kind': kind, 'source': 'synthetic fixture', 'recorded_at': '2026-11-06', 'scope': 'fixture only'}

    def node(self, identity, kind):
        return {'id': identity, 'type': kind, 'title': identity, 'basis': 'observed', 'mandatory': True,
                'discovery': 'mapped', 'implementation': 'implemented', 'verification': 'verified',
                'evidence_ids': ['notes'], 'required_links': [], 'boundary': 'synthetic fixture leaf',
                'verification_checks': [{'evidence_id': 'run', 'profile': 'acceptance'}]}

    def write_receipt(self):
        raw = json.dumps(self.execution).encode()
        identity = sha(raw)
        (self.root / 'artifacts' / identity).write_bytes(raw)
        self.receipt = {'id': 'fixture-run', 'passed': self.execution['passed'],
                        'results': [{'profile': 'acceptance', 'passed': self.execution['passed'], 'artifact': identity}]}
        (self.root / 'receipt.json').write_text(json.dumps(self.receipt), encoding='utf-8')

    def audit(self):
        return audit_graph(self.graph, self.root)

    def codes(self):
        return {f['code'] for f in self.audit()['findings']}

    def test_consistent_declared_fixture_scope(self):
        report = self.audit()
        self.assertTrue(report['declared_scope_satisfied'])
        self.assertNotIn('completion_percentage', report)

    def test_missing_relationship_is_an_actionable_frontier(self):
        self.graph['edges'] = []
        report = self.audit()
        self.assertFalse(report['declared_scope_satisfied'])
        self.assertIn('missing_required_link', self.codes())

    def test_inferred_edge_cannot_close_observed_requirement(self):
        self.graph['edges'][0]['basis'] = 'inferred'
        self.assertIn('missing_required_link', self.codes())

    def test_unexplored_and_unimplemented_remain_open(self):
        self.graph['nodes'][1].update(discovery='unexplored', implementation='not_started', verification='unverified')
        self.assertTrue({'discovery_frontier', 'implementation_incomplete', 'verification_incomplete'} <= self.codes())

    def test_observed_claim_needs_evidence(self):
        self.graph['edges'][0]['evidence_ids'] = []
        self.assertIn('unsupported_observed_claim', self.codes())

    def test_source_only_evidence_does_not_close_runtime_observation(self):
        self.graph['evidence'][0]['kind'] = 'source'
        self.assertTrue({'unsupported_observed_claim', 'missing_required_link'} <= self.codes())

    def test_explicit_source_observation_still_does_not_close_runtime_link(self):
        self.graph['evidence'][0]['kind'] = 'source'
        for item in self.graph['nodes'] + self.graph['edges']:
            item['observation_kind'] = 'source'
        self.assertNotIn('unsupported_observed_claim', self.codes())
        self.assertIn('missing_required_link', self.codes())

    def test_fake_pass_flag_rejected(self):
        self.execution['exit_code'] = 1
        self.write_receipt()
        self.graph['evidence'][1] = self.evidence('run', 'receipt.json', 'execution_receipt')
        with self.assertRaises(ValueError):
            self.audit()

    def test_modified_raw_execution_rejected(self):
        identity = self.receipt['results'][0]['artifact']
        (self.root / 'artifacts' / identity).write_bytes(b'changed')
        with self.assertRaises(ValueError):
            self.audit()

    def test_wrong_profile_cannot_close_verified_claim(self):
        self.graph['nodes'][0]['verification_checks'][0]['profile'] = 'not-executed'
        self.assertIn('verification_not_passed', self.codes())

    def test_unknown_node_and_duplicate_ids_rejected(self):
        self.graph['edges'][0]['to'] = 'missing'
        with self.assertRaises(ValueError):
            self.audit()

    def test_duplicate_node_ids_rejected(self):
        self.graph['nodes'].append(deepcopy(self.graph['nodes'][0]))
        with self.assertRaises(ValueError):
            self.audit()

    def test_valid_failed_execution_does_not_verify_a_node(self):
        self.execution.update(exit_code=1, passed=False)
        self.write_receipt()
        self.graph['evidence'][1] = self.evidence('run', 'receipt.json', 'execution_receipt')
        self.assertIn('verification_not_passed', self.codes())

    def test_truncated_execution_is_insufficient(self):
        self.execution['output_truncated'] = True
        self.write_receipt()
        self.graph['evidence'][1] = self.evidence('run', 'receipt.json', 'execution_receipt')
        self.assertIn('verification_not_passed', self.codes())

    def test_cycles_are_not_assumed_to_be_defects(self):
        self.graph['edges'].append({'id': 'feedback', 'from': 'api', 'to': 'action',
                                   'relation': 'displays', 'basis': 'observed', 'evidence_ids': ['notes']})
        self.assertTrue(self.audit()['declared_scope_satisfied'])

    def test_cli_reports_frontiers_without_creating_runtime(self):
        self.graph['nodes'][0]['discovery'] = 'partial'
        path = self.root / 'graph.json'
        path.write_text(json.dumps(self.graph), encoding='utf-8')
        runtime = self.root / 'unused-private-runtime'
        result = subprocess.run([sys.executable, '-m', 'recreator', '--workspace', str(runtime),
                                 'audit-graph', '--document', str(path), '--evidence-root', str(self.root)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(json.loads(result.stdout)['declared_scope_satisfied'])
        self.assertFalse(runtime.exists())

    def test_cli_malformed_nested_entries_return_json_error(self):
        for field in ['required_links', 'questions']:
            with self.subTest(field=field):
                graph = deepcopy(self.graph)
                graph['nodes'][0][field] = ['not an object']
                path = self.root / 'bad-graph.json'
                path.write_text(json.dumps(graph), encoding='utf-8')
                result = subprocess.run([sys.executable, '-m', 'recreator', '--workspace', str(self.root / 'unused'),
                                         'audit-graph', '--document', str(path), '--evidence-root', str(self.root)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertIn('error', json.loads(result.stderr))

    def test_open_question_and_contradiction_remain_visible(self):
        self.graph['nodes'][0]['questions'] = [{'id': 'q1', 'status': 'open', 'question': 'What is missing?'}]
        self.graph['edges'].append({'id': 'conflict', 'from': 'action', 'to': 'api',
                                   'relation': 'contradicts', 'basis': 'observed', 'evidence_ids': ['notes']})
        self.assertTrue({'open_question', 'unresolved_contradiction'} <= self.codes())

    def test_path_escape_rejected(self):
        self.graph['evidence'][0]['path'] = '../outside.txt'
        with self.assertRaises(ValueError):
            self.audit()

    def test_undeclared_boundary_remains_open(self):
        del self.graph['nodes'][1]['boundary']
        self.assertIn('undeclared_boundary', self.codes())


if __name__ == '__main__':
    unittest.main()
