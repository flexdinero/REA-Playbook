"""Audit declared graph frontiers without inventing missing product behavior."""
import re
from pathlib import Path

from .storage import canonical, check, inside, parse, sha


BASES = {'observed', 'inferred', 'proposed', 'unknown'}


def text(value):
    return isinstance(value, str) and bool(value.strip())


def inventory(items, label, limit):
    check(isinstance(items, list) and len(items) <= limit, label + ' inventory exceeds its limit or is not an array')
    result = {}
    for item in items:
        check(isinstance(item, dict) and text(item.get('id')), label + ' requires stable IDs')
        check(item['id'] not in result, label + ' repeats an ID')
        result[item['id']] = item
    return result


def audit_graph(graph, evidence_root):
    check(isinstance(graph, dict) and type(graph.get('schema_version')) is int and graph['schema_version'] == 1,
          'unsupported discovery graph schema')
    check(text(graph.get('scope')), 'graph requires an explicit scope')
    nodes = inventory(graph['nodes'], 'nodes', 5000)
    check(nodes and any(n.get('mandatory') is True for n in nodes.values()), 'graph needs a nonempty mandatory scope')
    edges = inventory(graph['edges'], 'edges', 10000)
    evidence = inventory(graph['evidence'], 'evidence', 1000)
    root = Path(evidence_root).resolve(strict=True)
    check(root.is_dir(), 'evidence root must be a directory')
    files = {}
    remaining = 64 * 1024 * 1024

    def read(path, expected):
        nonlocal remaining
        check(isinstance(expected, str) and re.fullmatch('[0-9a-f]{64}', expected), 'invalid evidence hash')
        path = Path(path)
        if path not in files:
            with path.open('rb') as handle:
                raw = handle.read(min(remaining, 32 * 1024 * 1024) + 1)
            check(len(raw) <= min(remaining, 32 * 1024 * 1024), 'graph evidence exceeds bounded read budget')
            remaining -= len(raw)
            files[path] = raw
        raw = files[path]
        check(sha(raw) == expected, 'evidence artifact hash mismatch: ' + str(path))
        return raw

    def refs(ids):
        check(isinstance(ids, list) and all(text(i) and i in evidence for i in ids), 'unknown evidence reference')
        check(len(ids) == len(set(ids)), 'duplicate evidence reference')
        return ids

    receipts = {}
    for identity, item in evidence.items():
        check(item.get('kind') in {'source', 'observation', 'execution_receipt'}, 'unknown evidence kind')
        check(all(text(item.get(key)) for key in ('source', 'recorded_at', 'scope')), 'evidence provenance fields required')
        path = inside(root, item['path'])
        raw = read(path, item['sha256'])
        if item['kind'] != 'execution_receipt':
            continue
        receipt = parse(raw)
        check(isinstance(receipt, dict) and text(receipt.get('id')), 'execution receipt requires run identity')
        results = receipt['results']
        check(isinstance(results, list) and results, 'empty execution receipt')
        profiles, passes = {}, []
        for result in results:
            name = result['profile']
            check(text(name) and name not in profiles, 'duplicate or missing execution profile')
            artifact = result['artifact']
            check(isinstance(artifact, str) and re.fullmatch('[0-9a-f]{64}', artifact), 'invalid execution artifact ID')
            output = parse(read(inside(root, (path.parent / 'artifacts' / artifact).relative_to(root)), artifact))
            check(type(output['timed_out']) is bool and type(output['output_truncated']) is bool, 'invalid execution flags')
            passed = type(output['exit_code']) is int and output['exit_code'] == 0 and not output['timed_out']
            check(output['passed'] is passed and result['passed'] is passed, 'execution pass flag contradicts actual result')
            profiles[name] = passed and not output['output_truncated']
            passes.append(passed)
        check(receipt['passed'] is all(passes), 'receipt aggregate contradicts execution results')
        receipts[identity] = profiles

    findings = []
    def finding(code, identity, detail):
        findings.append({'code': code, 'id': identity, 'detail': detail})

    def observed(item):
        mode = item.get('observation_kind', 'runtime')
        check(mode in {'runtime', 'source'}, 'unknown observation kind')
        allowed = {'source'} if mode == 'source' else {'observation', 'execution_receipt'}
        return item['basis'] == 'observed' and any(evidence[i]['kind'] in allowed for i in item['evidence_ids'])

    adjacency = {identity: [] for identity in nodes}
    for identity, edge in edges.items():
        check(edge['from'] in nodes and edge['to'] in nodes, 'edge refers to an unknown node')
        check(text(edge.get('relation')) and edge.get('basis') in BASES, 'invalid edge relation/basis')
        ids = refs(edge['evidence_ids'])
        if edge['basis'] == 'observed' and not observed(edge):
            finding('unsupported_observed_claim', identity, 'Observed edge lacks evidence of its declared observation kind')
        adjacency[edge['from']].append(('out', nodes[edge['to']], edge))
        adjacency[edge['to']].append(('in', nodes[edge['from']], edge))
        if edge['relation'] == 'contradicts' and not refs(edge.get('resolution_evidence_ids', [])):
            finding('unresolved_contradiction', identity, 'Contradictory evidence requires investigation')

    for identity, node in nodes.items():
        check(text(node.get('type')) and text(node.get('title')) and node.get('basis') in BASES, 'invalid node type/title/basis')
        check(type(node.get('mandatory')) is bool, 'mandatory must be boolean')
        check(node.get('discovery') in {'unexplored', 'partial', 'mapped'}, 'invalid discovery state')
        check(node.get('implementation') in {'not_started', 'partial', 'implemented'}, 'invalid implementation state')
        check(node.get('verification') in {'unverified', 'verified'}, 'invalid verification state')
        ids = refs(node['evidence_ids'])
        if node['basis'] == 'observed' and not observed(node):
            finding('unsupported_observed_claim', identity, 'Observed node lacks evidence of its declared observation kind')
        if node['mandatory']:
            for field, expected, code in [('discovery', 'mapped', 'discovery_frontier'),
                                          ('implementation', 'implemented', 'implementation_incomplete'),
                                          ('verification', 'verified', 'verification_incomplete')]:
                if node[field] != expected:
                    finding(code, identity, field + ': ' + node[field])
        requirements = node['required_links']
        check(isinstance(requirements, list), 'required_links must be an array')
        if node['mandatory'] and not requirements and not text(node.get('boundary')):
            finding('undeclared_boundary', identity, 'Declare leaf scope or investigate additional dependencies')
        for required in requirements:
            check(isinstance(required, dict), 'required-link entries must be objects')
            check(required.get('direction') in {'in', 'out'} and required.get('minimum_basis') in {'observed', 'any'}, 'invalid required-link direction/basis')
            check(text(required.get('relation')) and text(required.get('target_type')), 'invalid required-link relation/type')
            mode = required.get('observation_kind', 'runtime')
            check(mode in {'source', 'runtime'}, 'invalid required-link observation kind')
            matched = any(direction == required['direction'] and target['type'] == required['target_type']
                          and edge['relation'] == required['relation']
                          and (required['minimum_basis'] == 'any' or observed(edge) and edge.get('observation_kind', 'runtime') == mode)
                          for direction, target, edge in adjacency[identity])
            if not matched:
                finding('missing_required_link', identity, dict(required))
        checks = node['verification_checks']
        check(isinstance(checks, list), 'verification_checks must be an array')
        successes = []
        for item in checks:
            check(isinstance(item, dict), 'verification-check entries must be objects')
            refs([item['evidence_id']])
            check(text(item.get('profile')), 'verification check requires a profile')
            successes.append(receipts.get(item['evidence_id'], {}).get(item['profile']) is True)
        if node['verification'] == 'verified' and (not successes or not all(successes)):
            finding('verification_not_passed', identity, 'Claim lacks successful nontruncated execution for every named check')
        questions = node.get('questions', [])
        check(isinstance(questions, list), 'questions must be an array')
        for question in questions:
            check(isinstance(question, dict), 'question entries must be objects')
            check(text(question.get('id')) and text(question.get('question')) and question.get('status') in {'open', 'blocked', 'resolved'}, 'invalid discovery question')
            if question['status'] != 'resolved' or not refs(question.get('resolution_evidence_ids', [])):
                finding('open_question', identity, question)

    return {'schema_version': 1, 'graph_sha256': sha(canonical(graph).encode()), 'scope': graph['scope'],
            'declared_scope_satisfied': not findings, 'nodes': len(nodes), 'edges': len(edges),
            'evidence_records': len(evidence), 'findings': findings,
            'limits': ['Only the supplied graph and declared dependencies are audited.',
                       'Hashes and successful receipts do not prove truthful sources or sufficient test coverage.',
                       'No target discovery, model reasoning or whole-product completeness proof occurs.']}
