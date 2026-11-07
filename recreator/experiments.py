"""Run frozen adapter experiments against recorded, independently supplied oracles."""
from copy import deepcopy
from uuid import uuid4

from scripts.compare_observations import compare
from .storage import canonical, check, inside, now, parse, sha


def execute_experiment(suite, packet, reference, evidence_root, **options):
    check(bool(options.get('trusted_local')) != bool(options.get('sandbox_image')),
          'choose explicit trusted-local or pinned sandbox execution')
    workspace = suite.workspace
    state = workspace.read()
    check(not state.get('pending_repair'), 'recover pending repair before experiments')
    repo = suite._frozen(state)
    check(isinstance(packet, dict) and type(packet.get('schema_version')) is int and packet['schema_version'] == 1,
          'unsupported experiment schema')
    check(packet.get('oracle_basis') in {'captured-reference', 'explicit-contract', 'derived-invariant'},
          'declare the oracle basis; a contract is not a vendor capture')
    cases = packet['cases']
    check(isinstance(cases, list) and 1 <= len(cases) <= 20, 'experiment requires 1..20 cases')
    corpus = {'schema_version': 1, 'baseline_id': packet['baseline_id'], 'cases': [
        {key: case[key] for key in ('case_id', 'requirement_ids', 'input_sha256', 'context_sha256')} for case in cases]}
    # Validate the entire reference, including its raw artifacts, before any command.
    check(compare(corpus, reference, reference, evidence_root)['complete_match'], 'reference must cover every frozen case')
    total_timeout = 0
    for case in cases:
        check(case['prepare_profile'] != case['observe_profile'], 'preparation and observation must be separate profiles')
        for key in ('prepare_profile', 'observe_profile'):
            profile = state['manifest']['profiles'][case[key]]
            timeout = profile['timeout_seconds']
            check(type(timeout) is int and 1 <= timeout <= 300, 'invalid profile timeout')
            total_timeout += timeout
    check(total_timeout <= 600, 'experiment declared timeout budget exceeds 600 seconds')
    source = {name: sha(inside(repo, name).read_bytes()) for name in state['manifest']['editable']}
    source_identity = sha(canonical({'source': source, 'protected': state['protected']}).encode())
    frozen_reference = deepcopy(reference)
    for row in frozen_reference['cases']:
        with inside(evidence_root, row['source']['artifact_path']).open('rb') as handle:
            artifact = handle.read(32 * 1024 * 1024 + 1)
        identity = workspace.put(artifact)
        check(identity == row['source']['artifact_sha256'], 'reference changed during import')
        row['source']['artifact_path'] = 'artifacts/' + identity
    report = {'id': str(uuid4()), 'at': now(), 'status': 'started', 'oracle_basis': packet['oracle_basis'],
              'packet_artifact': workspace.put(canonical(packet).encode()),
              'reference_artifact': workspace.put(canonical(frozen_reference).encode()),
              'source_identity': source_identity, 'run_ids': [], 'stages': [], 'failures': [], 'passed': False}
    workspace.update('experiment_started', {'experiment_id': report['id']},
                     lambda s: s.setdefault('experiments', {}).update({report['id']: deepcopy(report)}), state['revision'])
    candidate = {'schema_version': 1, 'baseline_id': packet['baseline_id'], 'cases': []}
    def checkpoint(event):
        current = workspace.read()
        workspace.update(event, {'experiment_id': report['id']},
                         lambda s: s['experiments'].update({report['id']: deepcopy(report)}), current['revision'])
    for case, spec in zip(cases, corpus['cases']):
        row = dict(spec, status='not_observed')
        candidate['cases'].append(row)
        stage = 'prepare'
        try:
            for stage, profile_key in (('prepare', 'prepare_profile'), ('observe', 'observe_profile')):
                check({name: sha(inside(repo, name).read_bytes()) for name in source} == source,
                      'experiment source changed between stages')
                attempt = {'id': str(uuid4()), 'case_id': case['case_id'], 'stage': stage,
                           'profile': case[profile_key], 'status': 'attempted', 'receipt_committed': False}
                report['stages'].append(attempt)
                checkpoint('experiment_stage_attempted')
                def captured(result, actual_source, run_id):
                    attempt.update(status='output_captured', run_id=run_id,
                                   execution_artifact=result['artifact'], source=actual_source)
                    checkpoint('experiment_stage_output_captured')
                receipt = suite.run([case[profile_key]], on_result=captured,
                                    run_context={'experiment_id': report['id'], 'attempt_id': attempt['id']}, **options)
                report['run_ids'].append(receipt['id'])
                attempt.update(status='receipt_committed', receipt_committed=True)
                checkpoint('experiment_stage_receipt_committed')
                execution = parse(workspace.get(receipt['results'][0]['artifact']))
                check(receipt['source'] == source, 'experiment source changed')
                check(execution['passed'] and not execution['output_truncated'], 'adapter failed, timed out or output was truncated')
                payload = parse(execution['stdout'].encode('utf-8'))
                check(isinstance(payload, dict) and all(payload.get(key) == spec[key] for key in ('input_sha256', 'context_sha256')),
                      'adapter input/context does not match the frozen experiment')
                if stage == 'prepare':
                    check(payload.get('ready') is True, 'adapter did not confirm reset/preconditions')
                else:
                    observation = payload.get('observation')
                    check(isinstance(observation, dict) and set(observation) == {'output', 'effects', 'error'},
                          'adapter must report output, effects and error')
                    row.update(status='observed', observation=observation, source={
                        'build_id': source_identity, 'run_id': receipt['id'],
                        'artifact_path': 'artifacts/' + receipt['results'][0]['artifact'],
                        'artifact_sha256': receipt['results'][0]['artifact']})
                attempt['status'] = 'validated'
                checkpoint('experiment_stage_validated')
        except (ValueError, OSError, KeyError, TypeError) as error:
            report['failures'].append({'case_id': case['case_id'], 'stage': stage,
                                       'error': type(error).__name__ + ': ' + str(error)})
            checkpoint('experiment_stage_failed')
    report['candidate_artifact'] = workspace.put(canonical(candidate).encode())
    report['comparison'] = compare(corpus, frozen_reference, candidate, workspace.root)
    report['passed'] = report['comparison']['complete_match'] and not report['failures']
    report['status'] = 'finished'
    current = workspace.read()
    workspace.update('experiment_finished', {'experiment_id': report['id'], 'passed': report['passed']},
                     lambda s: s['experiments'].update({report['id']: report}), current['revision'])
    return report
