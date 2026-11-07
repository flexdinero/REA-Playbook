"""python -m recreator --workspace PRIVATE_PATH COMMAND ..."""

import argparse
import json
from pathlib import Path
import sys

from .engine import Suite
from .experiments import execute_experiment
from .models import select_model
from .storage import Workspace, parse


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True)
    commands = parser.add_subparsers(dest='command', required=True)
    init = commands.add_parser('init')
    init.add_argument('--manifest', required=True)
    init.add_argument('--corpus', required=True)
    run = commands.add_parser('run')
    run.add_argument('--profiles', nargs='+')
    experiment = commands.add_parser('experiment')
    experiment.add_argument('--packet', required=True)
    experiment.add_argument('--reference', required=True)
    experiment.add_argument('--evidence-root', required=True)
    repair = commands.add_parser('repair')
    repair.add_argument('--path', required=True)
    repair.add_argument('--expected-sha256', required=True)
    repair.add_argument('--candidate', required=True)
    repair.add_argument('--profiles', nargs='+')
    for command in (run, repair, experiment):
        mode = command.add_mutually_exclusive_group(required=True)
        mode.add_argument('--trusted-local', action='store_true')
        mode.add_argument('--sandbox-image')
    commands.add_parser('recover')
    commands.add_parser('status')
    commands.add_parser('handoff')
    lesson = commands.add_parser('propose-lesson')
    lesson.add_argument('--document', required=True)
    promote = commands.add_parser('promote-lesson')
    promote.add_argument('--id', required=True)
    promote.add_argument('--reviewer', required=True)
    promote.add_argument('--runs', nargs='+', required=True)
    revoke = commands.add_parser('revoke-lesson')
    revoke.add_argument('--id', required=True)
    revoke.add_argument('--reason', required=True)
    choose = commands.add_parser('select-model')
    choose.add_argument('--candidates', required=True)
    choose.add_argument('--capabilities', nargs='+', required=True)
    choose.add_argument('--budget', type=float, required=True)
    evidence = commands.add_parser('evidence')
    evidence.add_argument('--file', required=True)
    evidence.add_argument('--kind', choices=['observed', 'inferred', 'proposed', 'unknown'], required=True)
    evidence.add_argument('--source', required=True)
    evidence.add_argument('--claim', required=True)
    hypothesis = commands.add_parser('hypothesis')
    hypothesis.add_argument('--document', required=True)
    resolve = commands.add_parser('resolve-hypothesis')
    resolve.add_argument('--id', required=True)
    resolve.add_argument('--explanation', type=int, required=True)
    resolve.add_argument('--evidence', nargs='+', required=True)
    resolve.add_argument('--status', choices=['supported', 'contradicted', 'inconclusive'], required=True)
    args = parser.parse_args(argv)
    try:
        workspace = Workspace(args.workspace)
        suite = Suite(workspace)
        if args.command == 'init':
            Suite.initialize(workspace, parse(Path(args.manifest).read_bytes()), Path(args.corpus).read_bytes())
            result = suite.handoff()
        elif args.command == 'run':
            result = suite.run(args.profiles, trusted_local=args.trusted_local, sandbox_image=args.sandbox_image)
        elif args.command == 'experiment':
            result = execute_experiment(suite, parse(Path(args.packet).read_bytes()),
                                        parse(Path(args.reference).read_bytes()), Path(args.evidence_root),
                                        trusted_local=args.trusted_local, sandbox_image=args.sandbox_image)
        elif args.command == 'repair':
            result = suite.repair(args.path, args.expected_sha256, Path(args.candidate).read_bytes(), args.profiles,
                                  trusted_local=args.trusted_local, sandbox_image=args.sandbox_image)
        elif args.command == 'recover':
            result = suite.recover()
        elif args.command == 'status':
            state = workspace.read()
            result = {'revision': state['revision'], 'project_id': state['manifest']['project_id'],
                      'runs': len(state['runs']), 'repairs': state['repairs'], 'pending_repair': state.get('pending_repair'),
                      'budget_spent': state['budget_spent'], 'lessons': state['lessons'],
                      'experiments': state.get('experiments', {})}
        elif args.command == 'handoff':
            result = suite.handoff()
        elif args.command == 'propose-lesson':
            item = parse(Path(args.document).read_bytes())
            result = suite.propose_lesson(item['title'], item['procedure'], item['evidence'])
        elif args.command == 'promote-lesson':
            result = suite.promote_lesson(args.id, args.reviewer, args.runs)
        elif args.command == 'revoke-lesson':
            result = suite.revoke_lesson(args.id, args.reason)
        elif args.command == 'evidence':
            result = suite.record_evidence(Path(args.file).read_bytes(), args.kind, args.source, args.claim)
        elif args.command == 'hypothesis':
            item = parse(Path(args.document).read_bytes())
            result = suite.hypothesis(item['question'], item['explanations'], item['experiment'], item['evidence'])
        elif args.command == 'resolve-hypothesis':
            result = suite.resolve_hypothesis(args.id, args.explanation, args.evidence, args.status)
        else:
            result = select_model(parse(Path(args.candidates).read_bytes()), args.capabilities, args.budget)
        print(json.dumps(result, indent=2, allow_nan=False))
        if result.get('status') == 'reconciliation_required':
            return 2
        return 1 if result.get('passed') is False or result.get('status') == 'reverted' else 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({'error': str(error), 'type': type(error).__name__}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
