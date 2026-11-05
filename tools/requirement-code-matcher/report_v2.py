"""Standalone, inspectable HTML report for step-wise requirement matching."""
from __future__ import annotations

import html
from collections import defaultdict
from pathlib import Path
from typing import Any


LABELS = {"matched": "匹配", "partial": "部分匹配", "unmatched": "未匹配",
          "counterexample": "发现反例", "not_found": "未找到完整证据",
          "incomplete_evidence": "证据不完整", "outside_code_scope": "需代码外证据"}


def requirement_kind(requirement_id: str) -> tuple[str, str]:
    if "-PREQ" in requirement_id:
        return "nonfunctional", "性能需求"
    if "-SREQ" in requirement_id:
        return "nonfunctional", "安全需求"
    if "-FREQ" in requirement_id:
        return "functional", "功能需求"
    return "other", "其他需求"


def render_report(path: Path, requirements: list[dict[str, Any]],
                  steps: list[dict[str, Any]], units: list[dict[str, Any]],
                  batch_size: int = 12, scope_note: str = "",
                  json_name: str = "matches_v2.json",
                  metadata: dict[str, Any] | None = None) -> None:
    esc = lambda value: html.escape(str(value), quote=True)
    by_step = {step["step_id"]: step for step in steps}
    unit_steps: dict[str, set[str]] = defaultdict(set)
    for step in steps:
        for evidence in step.get("evidence", []):
            unit_steps[evidence["unit_id"]].add(step["step_id"])
    cards = []
    for req in requirements:
        sections = []
        for sid in req["step_ids"]:
            step = by_step[sid]
            state = step["verdict"]
            reason_kind = step.get("reason_kind") or (
                "matched" if state == "matched" else
                "counterexample" if (step.get("verification") or {}).get("counterexample_found") is True
                else "not_found")
            cited = {e["unit_id"] for e in step.get("evidence", [])}
            evidence_html = "".join(
                f"<details class='evidence'><summary><span class='mono'>{esc(e['file'])}:"
                f"{e['line_start']}-{e['line_end']}</span><span>{esc(e['observation'])}</span></summary>"
                f"<pre>{esc(e['snippet'])}</pre></details>"
                for e in step.get("evidence", []))
            inspected_ids = ", ".join(step.get("inspected_ids", []))
            missing = step.get("missing", "")
            sections.append(
                f"<section class='step {esc(state)}'><div class='stephead'>"
                f"<span class='mono'>{esc(sid)}</span><span class='tag {esc(state)}'>"
                f"{esc('有实现证据' if state == 'matched' else LABELS['partial'] if state == 'partial' else LABELS.get(reason_kind, LABELS['unmatched']))}</span></div>"
                f"<p class='steptext'>{esc(step['text'])}</p>"
                f"<div class='stepmeta'>已检查 <b>{step['inspected_count']}</b> / {step['candidate_count']} "
                f"个候选代码单元 · 引用 <b>{len(cited)}</b> 个代码单元 · "
                f"{esc('匹配后停止' if state == 'matched' else '反例后停止' if reason_kind == 'counterexample' else '候选检查完毕')}</div>"
                f"{f'<p class="reason">{esc(missing)}</p>' if missing else ''}"
                f"<details class='inspected'><summary>查看已检查的函数 ID</summary>"
                f"<p class='mono'>{esc(inspected_ids)}</p></details>"
                f"<div class='evidence-list'>{evidence_html or '<p class="empty">没有可引用的源码行</p>'}</div>"
                f"</section>")
        search_text = req["requirement_id"] + " " + req["title"] + " " + " ".join(
            by_step[sid]["text"] for sid in req["step_ids"])
        kind, kind_label = requirement_kind(req["requirement_id"])
        requirement_label = (LABELS["outside_code_scope"] if all(
            by_step[sid].get("reason_kind") == "outside_code_scope" for sid in req["step_ids"])
                             else LABELS[req["verdict"]])
        cards.append(
            f"<article class='requirement {esc(req['verdict'])}' data-state='{esc(req['verdict'])}' "
            f"data-kind='{kind}' data-search='{esc(search_text.lower())}'><header><div><span class='mono rid'>"
            f"{esc(req['requirement_id'])}</span> <span class='kindbadge {kind}'>{kind_label}</span>"
            f"<h2>{esc(req['title'])}</h2></div>"
            f"<div class='result'><span class='tag {esc(req['verdict'])}'>"
            f"{esc(requirement_label)}</span><strong>{req['matched_steps']}/{req['total_steps']}</strong>"
            f"<small>步骤匹配</small></div></header><div class='steps'>{''.join(sections)}</div></article>")
    reverse_rows = []
    for unit in sorted(units, key=lambda u: (-bool(unit_steps[u["id"]]),
                                             u.get("file", ""), u.get("line_start") or 0)):
        linked = sorted(unit_steps[unit["id"]])
        location = f"{unit.get('file', '')}:{unit.get('line_start', '')}-{unit.get('line_end', '')}"
        reverse_rows.append(
            f"<tr data-search='{esc((unit.get('name', '')+' '+location+' '+' '.join(linked)).lower())}'>"
            f"<td class='mono'>{esc(unit.get('name') or unit['id'])}</td>"
            f"<td class='mono'>{esc(location)}</td><td>{esc(', '.join(linked)) if linked else '—'}</td></tr>")
    counts = {label: sum(req["verdict"] == label for req in requirements)
              for label in ("matched", "partial", "unmatched")}
    matched_steps = sum(step["verdict"] == "matched" for step in steps)
    cited_units = sum(bool(unit_steps[unit["id"]]) for unit in units)
    metadata = metadata or {}
    metadata_html = " · ".join(f"{esc(label)}：{esc(metadata[key])}" for key, label in
                              (("model", "模型"), ("document", "需求文档"), ("graph", "代码理解图"))
                              if metadata.get(key))
    document = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>需求—代码匹配审查</title>
<style>
:root{{--ink:#19334a;--muted:#637789;--line:#dce5ee;--blue:#174c75;--green:#2f8061;--amber:#a76b00;--red:#b54440}}
*{{box-sizing:border-box}}body{{margin:0;background:#f4f7fa;color:var(--ink);font:14px/1.55 system-ui,'Microsoft YaHei',sans-serif}}
main{{max-width:1180px;margin:auto;padding:22px}}h1{{font-size:27px;margin:4px 0}}h2{{font-size:17px;margin:4px 0}}
.lead{{color:var(--muted);margin:5px 0 16px}}.mono{{font-family:ui-monospace,Consolas,monospace;overflow-wrap:anywhere}}
.provenance{{color:var(--muted);background:white;border:1px solid var(--line);border-radius:7px;padding:9px 12px;overflow-wrap:anywhere}}
.overview{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin:18px 0}}
.metric{{background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 16px}}
.metric b{{display:block;font-size:25px;line-height:1.2}}.metric span{{color:var(--muted)}}
.toolbar{{display:flex;align-items:center;gap:7px;flex-wrap:wrap;position:sticky;top:0;background:#f4f7fa;padding:10px 0;z-index:5}}
button,input,select{{font:inherit;border:1px solid #b8cad9;border-radius:7px;background:white;padding:8px 12px}}
button{{cursor:pointer}}button.active{{background:var(--blue);border-color:var(--blue);color:white}}
input{{min-width:260px;flex:1}}.count{{color:var(--muted);margin-left:auto}}
.requirement{{background:white;border:1px solid var(--line);border-radius:10px;margin:12px 0;overflow:hidden}}
.requirement>header{{display:flex;justify-content:space-between;gap:20px;align-items:center;padding:15px 18px;background:#fbfdff}}
.requirement.partial{{border-left:5px solid #d5a246}}.requirement.unmatched{{border-left:5px solid #cb6864}}
.requirement.matched{{border-left:5px solid #58a587}}.rid{{font-weight:700;color:var(--blue)}}
.kindbadge{{font-size:11px;padding:2px 7px;border-radius:5px;font-weight:650;background:#e8f1f9;color:#225778}}
.kindbadge.nonfunctional{{background:#f2eafa;color:#704b85}}.kindbadge.other{{background:#edf0f2;color:#52616a}}
.result{{display:flex;align-items:center;gap:8px;white-space:nowrap}}.result strong{{font-size:19px}}small{{color:var(--muted)}}
.tag{{font-size:12px;font-weight:650;padding:3px 8px;border-radius:99px;white-space:nowrap}}
.tag.matched{{color:#126747;background:#e6f5ed}}.tag.partial{{color:#875700;background:#fff3d6}}
.tag.unmatched,.tag.counterexample,.tag.not_matched{{color:#9a3434;background:#ffeded}}
.steps{{padding:0 18px 10px}}.step{{border-top:1px solid var(--line);padding:12px 0}}
.stephead{{display:flex;align-items:center;gap:8px}}.steptext{{font-size:15px;margin:7px 0}}
.stepmeta{{color:var(--muted);font-size:13px}}.reason{{color:#8d3d26;background:#fff6ee;padding:8px 10px;border-radius:5px}}
details{{margin:7px 0}}summary{{cursor:pointer}}.inspected{{font-size:12px;color:var(--muted)}}
.evidence{{border:1px solid var(--line);border-radius:6px;margin:8px 0;background:#fbfdff}}
.evidence summary{{padding:8px 10px;display:flex;gap:12px;align-items:baseline}}
.evidence summary span:first-child{{min-width:240px;color:var(--blue)}}.evidence pre{{margin:0;border-top:1px solid var(--line)}}
pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f5f9;padding:10px;font:12px/1.45 Consolas,monospace}}
.empty{{color:var(--muted)}}.coverage{{background:white;border:1px solid var(--line);border-radius:10px;padding:16px;margin:25px 0}}
.coverage h2{{font-size:20px}}.tablewrap{{max-height:600px;overflow:auto}}table{{width:100%;border-collapse:collapse}}
th,td{{padding:8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}th{{position:sticky;top:0;background:#eaf1f7}}
footer{{color:var(--muted);padding:16px 0 30px}}@media(max-width:700px){{.overview{{grid-template-columns:repeat(2,1fr)}}.requirement>header{{align-items:flex-start;flex-direction:column}}.evidence summary{{display:block}}}}
</style></head><body><main>
<h1>需求—代码匹配审查</h1><p class="lead">{esc(scope_note) if scope_note else '逐步骤源码证据'} · <a href="{esc(json_name)}">下载本页 JSON</a></p>
<p class="provenance">{metadata_html} · 展示代码单元：{len(units)} · {'附有源码目录' if metadata.get('source') else '仅有代码理解图'}{' · <a href="requirements_review.html">查看需求与步骤入模审查</a>' if metadata.get('reviewed_input') else ''}</p>
<div class="overview"><div class="metric"><b>{len(requirements)}</b><span>需求</span></div>
<div class="metric"><b>{counts['matched']}</b><span>匹配</span></div>
<div class="metric"><b>{counts['partial']}</b><span>部分匹配</span></div>
<div class="metric"><b>{counts['unmatched']}</b><span>未匹配</span></div>
<div class="metric"><b>{matched_steps}/{len(steps)}</b><span>步骤匹配</span></div></div>
<div class="toolbar"><button data-filter="all" class="active">全部</button><button data-filter="matched">匹配</button>
<button data-filter="partial">部分匹配</button><button data-filter="unmatched">未匹配</button>
<select id="kind-filter" aria-label="需求类型"><option value="all">全部类型</option><option value="functional">功能需求</option><option value="nonfunctional">非功能需求</option></select>
<input id="req-search" type="search" placeholder="搜索需求编号、标题或步骤"><span class="count" id="visible-count"></span></div>
<div id="requirement-list">{''.join(cards)}</div>
<section class="coverage"><h2>代码反向覆盖</h2><p>{cited_units}/{len(units)} 个展示代码单元在本次步骤证据中被引用。
未被引用仅表示本次匹配没有用到，不能据此断言需求缺失。</p>
<input id="unit-search" type="search" placeholder="搜索代码单元、源码位置或步骤 ID">
<details><summary>展开全部 {len(units)} 个代码单元</summary><div class="tablewrap"><table><thead>
<tr><th>代码单元</th><th>位置</th><th>引用该单元的步骤</th></tr></thead><tbody>{''.join(reverse_rows)}</tbody></table></div></details></section>
<footer>匹配规则：全部处理步骤有证据为匹配，部分有证据为部分匹配，零步骤有证据为未匹配。
源码行号经过范围校验；语义判断仍可能出错。</footer></main>
<script>
let active='all';const search=document.getElementById('req-search'),kindFilter=document.getElementById('kind-filter');
function refresh(){{let n=0;document.querySelectorAll('.requirement').forEach(card=>{{
 const show=(active==='all'||card.dataset.state===active)&&(kindFilter.value==='all'||card.dataset.kind===kindFilter.value)&&card.dataset.search.includes(search.value.trim().toLowerCase());
 card.hidden=!show;if(show)n++;}});document.getElementById('visible-count').textContent=`显示 ${{n}}/{len(requirements)} 条`;}}
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{{
 active=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(b=>b.classList.toggle('active',b===button));refresh();}}));
search.addEventListener('input',refresh);kindFilter.addEventListener('change',refresh);refresh();
document.getElementById('unit-search').addEventListener('input',e=>{{const q=e.target.value.trim().toLowerCase();
 document.querySelectorAll('.tablewrap tbody tr').forEach(row=>row.hidden=!row.dataset.search.includes(q));}});
</script></body></html>"""
    path.write_text(document, encoding="utf-8")
