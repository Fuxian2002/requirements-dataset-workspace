#!/usr/bin/env python3
"""Extract supported DATA FRAGMENTS, not a full strict LC conversion.

The input ZIP is immutable. Five device-related operators used with software
services are rejected rather than legitimized by pending annotations. No new
hardware, task period, adapter grammar or external execution is synthesized.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import zipfile

DEVICE_ATOMS = ('Init', 'GetData', 'SendData', 'ProTM', 'ProTC')
ALL_ATOMS = DEVICE_ATOMS + ('Set', 'Compute')


def make_projection(archive_path, output):
    with zipfile.ZipFile(archive_path) as archive:
        requirements = json.loads(archive.read('lc_spacerdl/data/requirements.json'))
        source = json.loads(archive.read('lc_spacerdl/data/statements.json'))
        resources = json.loads(archive.read('lc_spacerdl/data/resources.json'))
        local_manifest = json.loads(archive.read('lc_spacerdl/local_source_manifest.json'))
        requirements_md = archive.read('lc_spacerdl/requirements.md')
    statements = {s['id']:s for s in source['statements']}
    resource_by_id = {r['id']:r for r in resources['resources']}
    rejected = []
    for s in statements.values():
        if s['kind'] != 'atomic' or s.get('operator') not in DEVICE_ATOMS:
            continue
        endpoints = [resource_by_id[r] for r in s['resources']
                     if resource_by_id[r].get('name') == s.get('endpoint')]
        if (s.get('paper_binding') != 'confirmed' or not endpoints or
            any(r.get('kind') == 'source-backed-software-endpoint' for r in endpoints)):
            rejected.append({'id':s['id'], 'operator':s['operator'],
                'endpoint':s.get('endpoint'), 'requirements':s['requirements'],
                'evidence':s['evidence'],
                'reason':'paper Table 7/10 requires hardware port/device or OBDH computer; this record is an unconfirmed software-service binding'})
    rejected_ids = {s['id'] for s in rejected}
    # A projection is deliberately narrower than a complete flow. Do not leave
    # rejected calls in code, replace them with Compute/Set, or count comments.
    lines = ['// PARTIAL DATA FRAGMENTS ONLY. NOT a complete LC SpaceRDL system.',
             '// Paper Table 7 Compute/Set; Table 8 Composite/If/Else/While.',
             '// Device/service actions and message-trigger bindings are NOT represented.',
             '// Every block assumes its inputs have already been provided; no implicit receive.',
             '// Formal requirement variants and implementation variants are separate views.', '']
    locations = collections.defaultdict(list)

    def supported(nodes):
        return any((n.get('op') not in rejected_ids if 'op' in n else
                    any(supported(n.get(k, [])) for k in ('then','else','body','sequence')))
                   for n in nodes)

    def emit(nodes, indent):
        for node in nodes:
            if 'op' in node:
                sid = node['op']
                if sid in rejected_ids:
                    continue
                s = statements[sid]
                if s['operator'] not in ('Compute','Set'):
                    raise ValueError('Unreviewed atom in data projection: '+sid)
                lines.append(indent+'// '+sid+' REQ: '+', '.join(s['requirements']))
                lines.append(indent+s['source_excerpt'])
                locations[sid].append(len(lines))
            elif not supported([node]):
                continue
            elif 'if' in node:
                lines.append(indent+'If ('+node['if']+') {')
                emit(node['then'],indent+'    ')
                if supported(node.get('else', [])):
                    lines.append(indent+'} Else {')
                    emit(node['else'],indent+'    ')
                lines.append(indent+'}')
            elif 'while' in node:
                lines.append(indent+'While ('+node['while']+') {')
                emit(node['body'],indent+'    ')
                lines.append(indent+'}')
            elif 'sequence' in node:
                lines.append(indent+'Composite {')
                emit(node['sequence'],indent+'    ')
                lines.append(indent+'}')
            else:
                raise ValueError('Unknown source AST node')
    for flow in sorted(source['workflows'], key=lambda f:f['id']):
        lines += ['// DATA PROJECTION of '+flow['id']+'; incomplete external behavior.', 'Composite {']
        emit(flow['nodes'],'    ')
        lines += ['}', '']
    for s in sorted(statements.values(),key=lambda s:s['id']):
        if s.get('expanded') and s['kind']=='atomic' and s['id'] not in rejected_ids and s['id'] not in locations:
            emit([{'op':s['id']}],'')
            lines.append('')
    selected = [dict(statements[sid], projection_lines=locations[sid]) for sid in sorted(locations)]
    counts = collections.Counter(s['operator'] for s in selected)
    report = {'result':'blocked-full-conversion', 'data_fragment_shape_check':'not-yet-run',
        'baseline_archive_sha256':hashlib.sha256(archive_path.read_bytes()).hexdigest(),
        'requirements_total':len(requirements['requirements']),
        'strict_full_conversion_complete':False,
        'rejected_unconfirmed_device_actions':len(rejected),
        'rejected_operator_counts':dict(collections.Counter(s['operator'] for s in rejected)),
        'data_fragment_operators':{op:counts[op] for op in ALL_ATOMS},
        'remaining_requirements_must_not_be_counted_complete':True,
        'required_external_information':['authoritative SpaceRDL definition for cFE software services and nonperiodic message-triggered tasks, or an evidence-backed deployment/system boundary supported by the paper'],
        'rejected_statements':rejected,
        'scope':'source-backed data projection only, NOT a proof of full paper semantic compliance or LC execution'}
    output.mkdir(parents=True,exist_ok=True)
    (output/'data_fragments.rdl').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (output/'data_fragment_statements.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (output/'strict_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # Complete reviewed requirements preserved byte for byte, not reinitialized.
    (output/'requirements.md').write_bytes(requirements_md)
    for name,doc in [('requirements.json',requirements),('resources.json',resources),('local_source_manifest.json',local_manifest)]:
        (output/name).write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    report=make_projection(args.archive,args.output)
    print(json.dumps({k:v for k,v in report.items() if k!='rejected_statements'},ensure_ascii=False,indent=2))
