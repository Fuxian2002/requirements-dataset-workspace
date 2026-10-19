#!/usr/bin/env python3
"""Generate readable views from existing frozen inputs; never initialize/replace reviews."""
import argparse
import json
from pathlib import Path


def read(root, name):
    return json.loads((root / name).read_text(encoding='utf-8'))


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2)


def evidence(records):
    result = []
    for e in records:
        path = e.get('path', '')
        locator = (f" L{e['start_line']}–{e.get('end_line', e['start_line'])}"
                   if 'start_line' in e else f" p{e.get('page', '')}")
        result.append(f"[{path}](<{path}>) {locator} {e.get('symbol', '')}")
    return '\n\n'.join(result)


def render(root):
    req = read(root, 'requirements.json')['requirements']
    res = read(root, 'resources.json')
    atoms = sorted(read(root, 'data_fragment_statements.json'), key=lambda x: x['id'])
    audit = read(root, 'strict_audit.json')
    issues = read(root, 'data/issues.json')['issues']
    lines = (root / 'code.rdl').read_text(encoding='utf-8').splitlines()
    by_req = {r['id']: [s for s in atoms if r['id'] in s['requirements']] for r in req}
    rejected = sorted(audit['rejected_statements'], key=lambda x: x['id'])
    def write(name, parts):
        (root / name).write_text('\n\n'.join(parts) + '\n', encoding='utf-8')

    parts = ['# LC 完整需求整理与补全（82 条）',
             '保留63条正式需求及19条补充需求的原文、规则、证据和人工审查字段。'
             '“完整”指需求清单，不表示全量严格转换已完成。JSON内原ST、obligations、native_interface_statements和syntax字段含历史审查记录；'
             '本轮有效片段及位置以 [追踪表](traceability.md) 和 projection_lines 为准。'
             'expressed/checked 不是官方解析或真实运行通过。']
    for r in sorted(req, key=lambda x: x['id']):
        parts += [f"## {r['id']}", f"原编号：{r.get('original_id', '')}；来源：{r.get('source', '')}",
                  r.get('description', ''), f"原文：{r.get('original_text', '')}",
                  '当前保留片段：' + ', '.join(s['id'] for s in by_req[r['id']]),
                  evidence(r.get('evidence', [])),
                  '完整审查记录（原值保留，历史候选不算当前完成）：\n\n```json\n' + dump(r) + '\n```']
    write('requirements.md', parts)

    parts = ['# LC 资源与数据字典',
             '来源权威输入为 resources.json；保留原始资源规则和人工结论，不重置状态。'
             '资源是本项目的来源/计算合同记录，不冒称论文已确认的全部资源序列化格式。'
             '软件服务、软件端点及其历史候选独立标识，不能当作已获确认的硬件Device/Port。',
             f"共{len(res['resources'])}项资源记录、{len(res['data_elements'])}项数据定义。"]
    software = {'software-interface', 'source-backed-software-endpoint', 'source-interface-contract', 'external-application', 'protocol'}
    for group, selected in [('数据处理/状态/配置/环境记录', False), ('软件接口及历史候选资源（非已确认设备绑定）', True)]:
        parts.append('## ' + group)
        for r in sorted(res['resources'], key=lambda x: x['id']):
            if (r.get('kind') in software) != selected:
                continue
            parts += [f"### {r['id']} — {r.get('name', '')}",
                      f"类别：{r.get('kind', '')}；当前保留片段引用：" + ', '.join(s['id'] for s in atoms if r['id'] in s.get('resources', [])),
                      '```json\n' + dump(r) + '\n```']
    parts.append('## 数据定义（聚合/别名的官方序列化仍有缺口）')
    for d in sorted(res['data_elements'], key=lambda x: x['name']):
        parts += [f"### {d['name']}", '```json\n' + dump(d) + '\n```']
    for key in ('serialization_note', 'flow_contract', 'expanded_flow_links'):
        if key in res:
            parts += ['## ' + key + '（保留原审查值）', '```json\n' + dump(res[key]) + '\n```']
    write('resources.md', parts)

    parts = ['# 当前保留的282个数据处理片段定义',
             'Compute 248、Set 34；共423个出现位置。以下只用当前code.rdl的projection_lines定位；'
             '原JSON的start_line/occurrences属于旧版位置，不得用于本轮验收。'
             '所有片段均不证明完整消息入口、软件副作用或全量语义等价。']
    for s in atoms:
        parts += [f"<a id=\"{s['id'].lower()}\"></a>", f"## {s['id']} — {s['title']}",
                  f"操作：{s['operator']}；需求：" + ', '.join(s['requirements']),
                  '资源：' + ', '.join(s.get('resources', [])),
                  '当前位置：' + ', '.join(f"[code.rdl L{n}](code.rdl)" for n in s['projection_lines']),
                  '```spacerdl\n' + lines[s['projection_lines'][0] - 1].strip() + '\n```',
                  '输入绑定：' + s.get('input_binding', ''), '输出绑定：' + s.get('output_binding', ''),
                  '规则：\n\n' + '\n'.join('- ' + rule for rule in s.get('rules', [])),
                  evidence(s.get('evidence', [])),
                  '检查边界：' + s.get('note', '')]
    write('statements.md', parts)

    parts = ['# 82条需求的当前追踪表',
             '各条需求均列出当前保留片段、已剔除候选与剩余义务。不以有片段等同于全需求完成；'
             'requirements.json旧链接原样留作历史审查。当前全量状态blocked。']
    for r in sorted(req, key=lambda x: x['id']):
        parts += [f"## {r['id']} — {r.get('original_id', '')}", r.get('description', '')]
        parts.append('当前保留数据片段：\n\n' + ('\n'.join(
            f"- [{s['id']}](statements.md#{s['id'].lower()}) {s['operator']}；code.rdl L" + ', L'.join(map(str, s['projection_lines']))
            for s in by_req[r['id']]) or '无'))
        rejected_for_req = [s for s in rejected if r['id'] in s['requirements']]
        parts.append('已剔除的软件接口候选：' + (', '.join(f"{s['id']} ({s['operator']})" for s in rejected_for_req) or '无直接关联；仍有系统入口/资源绑定缺口'))
        parts.append('剩余义务（保留原审查）：\n\n```json\n' + dump(r.get('remaining', [])) + '\n```')
        parts.append('最终范围：仅数据处理片段；非完整系统转换。')
    write('traceability.md', parts)

    parts = ['# 当前阻塞与已保留问题清单',
             '[当前严格转换阻塞结论](STRICT_CONVERSION_BLOCKER.md)优先于旧候选审查。'
             '下面的问题状态、人工结论及证据均从已有issues.json读取，不重新初始化。'
             '资源/需求中的旧候选字段是历史记录，不会因保留而重新进入code.rdl。',
             '## 44个剔除候选（逐项）']
    for s in rejected:
        parts += [f"### {s['id']} — {s['operator']} / {s['endpoint']}",
                  '关联需求：' + ', '.join(s['requirements']), '拒绝原因：' + s['reason'], evidence(s['evidence'])]
    parts.append('## 原有问题审查记录')
    for issue in sorted(issues, key=lambda x: x['id']):
        parts += [f"### {issue['id']} — {issue.get('title', '')}", '```json\n' + dump(issue) + '\n```']
    write('issues.md', parts)

    write('grammar_profile.md', ['# 本轮冻结的语法核定与检查边界',
        '论文表7的数据操作形状：',
        '```spacerdl\nCompute outputName inputName ReqCapByFormTable FormulaTable.formulaName;\nSet outputName inputName;\n```',
        '表8采用Composite、If/Else、While结构。FormulaTable的本项目具体函数合同、聚合数据序列化与变量别名不能仅因形状吻合就称为完整论文语义获确认。',
        '论文中的Init/GetData/SendData/ProTM/ProTC未被删除；本轮仅排除了44个未建立论文设备/硬件端口/数管对应依据的软件候选。五类目前为0，不表示LC没有收发或后续最终只能使用Compute/Set。',
        '不引入自造Device、软件适配语法、固定ControlPeriod或消息中断绑定；不把Compute中的请求描述当成真实发送。',
        '本地检查覆盖操作形状、符号、公式输入输出合同、布尔条件符号与括号结构。未执行官方解析器，未证明全量语义等价。',
        '[原论文](<evidence/reference/reference_materials/定稿ra012-20260721.pdf>)；具体阻塞见STRICT_CONVERSION_BLOCKER.md。'])

    flow_ids = ['ST-LC-0200', 'ST-LC-0201', 'ST-LC-0207', 'ST-LC-0230', 'ST-LC-0234', 'ST-LC-0300', 'ST-LC-0309', 'ST-LC-0340', 'ST-LC-0341', 'ST-LC-0342', 'ST-LC-0343', 'ST-LC-0346', 'ST-LC-0365']
    parts = ['# 需求—资源—片段—结果的贯通讲解',
             '这是源码行为与当前表达范围的贯通说明，不是已可运行的全系统SpaceRDL例程。监测消息和独立Sample Request是两个入口，不能合成一个虚构周期。',
             '## 1. 监测消息更新持久结果',
             'lc_app.c接收软件消息，lc_dispatch.c按MID路由到监测处理；这个接收/触发过程未获得论文任务绑定。输入已到达后，片段检查LC状态，选中WP，按源码原类型计算偏移、解码和比较，再提交WP结果、统计与age，最后提交整包监测次数。',
             '极端偏移可能整数回绕：必须保留代码实际算术及风险记录，不能把片段解释为“所有越界必然拒绝”。NaN、STALE/ERROR及统计更新以各片段规则和证据为准，不凭其他版本审查推定错误。',
             '## 2. 独立评估请求读取此前的监测结果',
             '只有另一个Sample Request到达才进入AP评估，读取已经持久化的WRT/ART和状态。DISABLED、NOT_USED、PERMOFF不请求RTS；其他路径按RPN结果、连续失败阈值和LC ACTIVE/PASSIVE条件继续。不能让一个监测Compute暗中调用评估。',
             '## 3. 正常动作和禁止动作',
             '允许路径保留源码AP先变PASSIVE、准备RTS、提交位置、请求尝试计数、事件及结果的相对顺序；禁止路径不生成RTS效果并按规则更新抑制统计。请求描述和提交位置仅是数据，实际CFE_SB_TransmitMsg及事件发送尚未表达；因此不能将这些片段称为已发出请求的运行证明。',
             '## 4. 精确映射实例（完整规则可顺着链接审阅）']
    by_id = {s['id']: s for s in atoms}
    for sid in flow_ids:
        s = by_id[sid]
        parts += [f"### {sid} — {s['title']}", '需求：' + ', '.join(s['requirements']),
                  '资源合同：' + ', '.join(s.get('resources', [])) + '（resources.md / resources.json）',
                  '```spacerdl\n' + lines[s['projection_lines'][0] - 1].strip() + '\n```',
                  '产生/保持的结果：' + s.get('output_binding', ''),
                  '[完整规则](statements.md#' + sid.lower() + ')；code.rdl L' + ', L'.join(map(str, s['projection_lines']))]
    parts += ['## 审查结论', '可贯通查阅需求、资源、源码定位、片段和数据结果；真实软件消息入口/提交仍blocked。不存在全需求已严格转换完成的贯通运行例子。']
    write('walkthrough.md', parts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    render(parser.parse_args().root)
