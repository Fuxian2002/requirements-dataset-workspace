#!/usr/bin/env python3
"""Shape/resource check of PARTIAL data fragments; no full-coverage claim."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re

IDENT = r'[A-Za-z_][A-Za-z0-9_]*'


def check(root):
    resources=json.loads((root/'resources.json').read_text())
    names={d['name']:d for d in resources['data_elements']}
    formulas={r['formula']:r for r in resources['resources'] if r.get('formula')}
    statements=json.loads((root/'data_fragment_statements.json').read_text())
    by_line={n:s for s in statements for n in s['projection_lines']}
    lines=(root/'data_fragments.rdl').read_text().splitlines()
    stack=[]
    errors=[]
    parsed=0
    occurrences=collections.Counter()
    for number,line in enumerate(lines,1):
        text=line.split('//',1)[0].strip()
        if not text:
            continue
        if text=='Composite {':
            stack.append(('Composite',False))
            continue
        condition=re.fullmatch(r'(If|While)\s*\(('+IDENT+r')\)\s*\{',text)
        if condition:
            op,guard=condition.groups()
            if guard not in names or names[guard]['type']!='boolean':
                errors.append((number,'undefined/nonboolean guard',guard))
            stack.append((op,False))
            continue
        if text=='} Else {':
            if not stack or stack[-1] != ('If',False):
                errors.append((number,'Else without matching unused If'))
            else:
                stack[-1]=('If',True)
            continue
        if text=='}':
            if not stack:
                errors.append((number,'extra closing brace'))
            else:
                stack.pop()
            continue
        compute=re.fullmatch(r'Compute ('+IDENT+r') ('+IDENT+r') ReqCapByFormTable (FormulaTable\.'+IDENT+r');',text)
        assign=re.fullmatch(r'Set ('+IDENT+r') ('+IDENT+r');',text)
        if not compute and not assign:
            errors.append((number,'unsupported or unconfirmed operation',text))
            continue
        output,inp=(compute or assign).groups()[:2]
        if inp not in names or output not in names:
            errors.append((number,'undefined operand',text))
        if compute:
            formula=compute.group(3)
            contract=formulas.get(formula)
            if not contract or inp not in contract['inputs'] or output not in contract['outputs']:
                errors.append((number,'missing/wrong formula contract',text))
        s=by_line.get(number)
        if not s or s['source_excerpt']!=text:
            errors.append((number,'missing or inconsistent tracked operation',text))
        else:
            occurrences[s['id']]+=1
        parsed+=1
    if stack:
        errors.append(('EOF','unclosed structures'))
    if set(occurrences)!={s['id'] for s in statements}:
        errors.append(('catalog','unlocated statement definitions'))
    report={'result':'pass' if not errors else 'fail', 'errors':errors,
            'distinct_data_atoms':len(occurrences),'atom_occurrences':parsed,
            'unconfirmed_device_operations_in_projection':0,
            'artifact_sha256':hashlib.sha256((root/'data_fragments.rdl').read_bytes()).hexdigest(),
            'full_LC_conversion':'blocked, not checked as complete',
            'scope':'exact Compute/Set shapes, symbols, formula contracts, boolean symbols and block structure; not semantic equivalence or execution'}
    (root/'data_projection_check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    audit_path=root/'strict_audit.json'
    if audit_path.is_file():
        audit=json.loads(audit_path.read_text())
        audit['data_fragment_shape_check']=report['result']
        audit['strict_full_conversion_complete']=False
        audit_path.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args()
    report=check(args.root)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    raise SystemExit(0 if report['result']=='pass' else 1)
