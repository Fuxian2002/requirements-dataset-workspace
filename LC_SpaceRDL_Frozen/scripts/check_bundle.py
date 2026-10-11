#!/usr/bin/env python3
"""Independent organization/freeze checks, not a language or LC runtime test."""
import collections
import hashlib
import json
from pathlib import Path
import re


def check(root):
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)
    def read(name):
        return json.loads((root / name).read_text(encoding='utf-8'))
    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()
    req = read('requirements.json')['requirements']
    atoms = read('data_fragment_statements.json')
    audit = read('strict_audit.json')
    require(len(req) == 82, 'Requirements count differs from 82')
    require(len({r['id'] for r in req}) == 82, 'Duplicate requirement IDs')
    counts = dict(collections.Counter(s['operator'] for s in atoms))
    require(counts == {'Compute': 248, 'Set': 34}, 'Frozen operator counts differ')
    require(len(atoms) == 282, 'Distinct atom count differs')
    require(sum(len(s['projection_lines']) for s in atoms) == 423, 'Occurrence count differs')
    require(len(audit['rejected_statements']) == 44, 'Rejected candidate count differs')
    require(not audit['strict_full_conversion_complete'], 'False full completion claim')
    require((root / 'code.rdl').read_bytes() == (root / 'data_fragments.rdl').read_bytes(), 'Code alias differs')
    code = (root / 'code.rdl').read_text(encoding='utf-8').splitlines()
    positions = []
    for s in atoms:
        for line in s['projection_lines']:
            require(0 < line <= len(code) and code[line - 1].strip() == s['source_excerpt'], f"Wrong current line: {s['id']} L{line}")
            positions.append(line)
    require(len(set(positions)) == 423, 'Overlapping tracked positions')
    active = {s['id'] for s in atoms}
    require(not active.intersection(s['id'] for s in audit['rejected_statements']), 'Rejected candidate is active')
    require(not any(re.match(r'\s*(Init|GetData|SendData|ProTM|ProTC)\s', line) for line in code), 'Unconfirmed action in code')
    for name, expected in read('freeze_manifest.json').items():
        require((root / name).is_file() and sha(root / name) == expected, f'Frozen input changed: {name}')
    evidence_count = 0
    lc_count = 0
    for entry in read('source_manifest.json')['files']:
        if not entry.get('included') or entry.get('missing'):
            continue
        path = root / entry['bundle_path']
        require(path.is_file() and sha(path) == entry['sha256'], f"Evidence changed/missing: {entry['bundle_path']}")
        evidence_count += 1
        lc_count += entry['bundle_path'].startswith('evidence/LC/')
    require(lc_count == 97, 'Source snapshot count differs from 97')
    for entry in read('local_source_manifest.json')['files']:
        path = root / 'evidence/LC' / entry['path']
        require(path.is_file() and sha(path) == entry['sha256'], 'Local frozen comparison mismatch: ' + entry['path'])
    requirements_md = (root / 'requirements.md').read_text(encoding='utf-8')
    trace_md = (root / 'traceability.md').read_text(encoding='utf-8')
    statements_md = (root / 'statements.md').read_text(encoding='utf-8')
    require(set(re.findall(r'^## (REQ-LC-\d+)', requirements_md, re.M)) == {r['id'] for r in req}, 'Readable requirements inventory differs')
    require(set(re.findall(r'^## (REQ-LC-\d+)', trace_md, re.M)) == {r['id'] for r in req}, 'Traceability inventory differs')
    require(set(re.findall(r'^## (ST-LC-\d+)', statements_md, re.M)) == active, 'Statement inventory differs')
    for md in sorted(root.glob('*.md')):
        for link in re.findall(r'\]\(([^\n]+?)\)', md.read_text(encoding='utf-8')):
            destination = link.strip('<>')
            if '://' in destination:
                continue
            filename, _, fragment = destination.partition('#')
            target = root / filename if filename else md
            require(target.exists(), f'Broken local link in {md.name}: {destination}')
            if fragment and target.is_file() and target.suffix == '.md':
                require('id="' + fragment + '"' in target.read_text(encoding='utf-8'), f'Broken explicit anchor: {destination}')
    report = {'result': 'pass' if not errors else 'fail', 'errors': errors,
              'requirements': len(req), 'distinct_data_atoms': len(atoms), 'atom_occurrences': len(positions),
              'operator_definitions': counts, 'frozen_evidence_files_checked': evidence_count,
              'frozen_LC_source_files_checked': lc_count, 'rejected_candidates': 44,
              'full_conversion_result': 'blocked',
              'scope': 'freeze hashes, evidence, code alias, current locations, inventory and local links; not official parsing, LC execution or full semantic equivalence'}
    (root / 'logs').mkdir(exist_ok=True)
    (root / 'logs/bundle_check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


if __name__ == '__main__':
    report = check(Path(__file__).resolve().parents[1])
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['result'] == 'pass' else 1)
