# 当前保留的282个数据处理片段定义

Compute 248、Set 34；共423个出现位置。以下只用当前code.rdl的projection_lines定位；原JSON的start_line/occurrences属于旧版位置，不得用于本轮验收。所有片段均不证明完整消息入口、软件副作用或全量语义等价。

<a id="st-lc-0100"></a>

## ST-LC-0100 — 验证命令头长度而不执行负载

操作：Compute；需求：REQ-LC-0003, REQ-LC-0005, REQ-LC-0035, REQ-LC-0036, REQ-LC-0037

资源：RES-LC-0100

当前位置：[code.rdl L165](code.rdl), [code.rdl L188](code.rdl), [code.rdl L347](code.rdl), [code.rdl L384](code.rdl), [code.rdl L455](code.rdl), [code.rdl L486](code.rdl), [code.rdl L547](code.rdl), [code.rdl L845](code.rdl), [code.rdl L928](code.rdl)

```spacerdl
Compute CommandLengthMatches CommandContext ReqCapByFormTable FormulaTable.VerifyCommandLength;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：CommandLengthMatches 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- 从 route 对应的原命令结构取得 ExpectedLength=sizeof(对应 LC_*Cmd_t)，ActualLength 为消息头声明长度；仅比较这两者。
- 输出 TRUE 当且仅当 ExpectedLength 等于 ActualLength；FALSE时命令负载不得执行。未取得有效消息头/部署ABI则输入待确认，不能把外部缺数据当长度匹配。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L10–10 LC1002

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L40–114 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L121–256 *VerifyDispatch

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0101"></a>

## ST-LC-0101 — 区分地面命令与内部请求的计数范围

操作：Compute；需求：REQ-LC-0003, REQ-LC-0004, REQ-LC-0005, REQ-LC-0080

资源：RES-LC-0101

当前位置：[code.rdl L163](code.rdl), [code.rdl L186](code.rdl), [code.rdl L345](code.rdl), [code.rdl L382](code.rdl), [code.rdl L453](code.rdl), [code.rdl L484](code.rdl), [code.rdl L545](code.rdl), [code.rdl L843](code.rdl), [code.rdl L926](code.rdl)

```spacerdl
Compute CommandIsGround CommandContext ReqCapByFormTable FormulaTable.IsGroundCommandMessage;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：CommandIsGround 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- MID=LC_CMD_MID 为地面命令；LC_SEND_HK_MID 和 LC_SAMPLE_AP_MID 为内部请求，不计普通地面CmdCount/CmdErrCount。
- 仅输出boolean，不合并WP接收和AP采样入口，不变任何状态。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L10–10 LC1002

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L40–114 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L121–256 *VerifyDispatch

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L11–11 LC1003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L267–293 LC_NoopCmd / LC_ResetCountersCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L317–345 LC_SetLCStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L460–468 LC_SetAPStateCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

[evidence/LC/docs/dox_src/cfs_lc.dox](<evidence/LC/docs/dox_src/cfs_lc.dox>)  L125–139 Design Overview

[evidence/LC/docs/dox_src/cfs_lc.dox](<evidence/LC/docs/dox_src/cfs_lc.dox>)  L644–652 scheduler FAQ

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L91–126 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0102"></a>

## ST-LC-0102 — 停止被拒绝命令的负载执行

操作：Compute；需求：REQ-LC-0003, REQ-LC-0005, REQ-LC-0035, REQ-LC-0036, REQ-LC-0037, REQ-LC-0045, REQ-LC-0046, REQ-LC-0047, REQ-LC-0048, REQ-LC-0049, REQ-LC-0073

资源：RES-LC-0102

当前位置：[code.rdl L171](code.rdl), [code.rdl L194](code.rdl), [code.rdl L353](code.rdl), [code.rdl L390](code.rdl), [code.rdl L413](code.rdl), [code.rdl L421](code.rdl), [code.rdl L461](code.rdl), [code.rdl L492](code.rdl), [code.rdl L529](code.rdl), [code.rdl L553](code.rdl), [code.rdl L851](code.rdl), [code.rdl L894](code.rdl), [code.rdl L902](code.rdl), [code.rdl L910](code.rdl), [code.rdl L934](code.rdl), [code.rdl L954](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.AbortRejectedCommand;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅把 outcome 标为 rejected、handlerEnabled=false，保存实际拒绝原因（长度、未知FcnCode、非法状态/索引）。
- AppData/WRT/ART与负载操作均保持不变；后续唯一允许的命令业务是拒绝计数与错误事件描述。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L10–10 LC1002

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L40–114 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L121–256 *VerifyDispatch

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0103"></a>

## ST-LC-0103 — 地面拒绝计数加一

操作：Compute；需求：REQ-LC-0003, REQ-LC-0005, REQ-LC-0035, REQ-LC-0036, REQ-LC-0037, REQ-LC-0045, REQ-LC-0046, REQ-LC-0047, REQ-LC-0048, REQ-LC-0049, REQ-LC-0073

资源：RES-LC-0103

当前位置：[code.rdl L174](code.rdl), [code.rdl L197](code.rdl), [code.rdl L356](code.rdl), [code.rdl L393](code.rdl), [code.rdl L415](code.rdl), [code.rdl L423](code.rdl), [code.rdl L464](code.rdl), [code.rdl L495](code.rdl), [code.rdl L531](code.rdl), [code.rdl L556](code.rdl), [code.rdl L854](code.rdl), [code.rdl L896](code.rdl), [code.rdl L904](code.rdl), [code.rdl L912](code.rdl), [code.rdl L937](code.rdl), [code.rdl L956](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.IncrementRejectedGroundCommand;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只将 AppData.CmdErrCount 工作副本按原成员类型加一；保留 CmdCount、其他HK计数、AP/WP状态与统计不变。
- 长度错误内部HK/AP请求不经过本步；不把错误计数扩展至所有内部消息。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L10–10 LC1002

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L40–114 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L121–256 *VerifyDispatch

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0104"></a>

## ST-LC-0104 — 形成原拒绝原因的错误事件描述

操作：Compute；需求：REQ-LC-0003, REQ-LC-0005, REQ-LC-0035, REQ-LC-0036, REQ-LC-0037, REQ-LC-0045, REQ-LC-0046, REQ-LC-0047, REQ-LC-0048, REQ-LC-0049, REQ-LC-0073

资源：RES-LC-0104

当前位置：[code.rdl L169](code.rdl), [code.rdl L192](code.rdl), [code.rdl L351](code.rdl), [code.rdl L388](code.rdl), [code.rdl L417](code.rdl), [code.rdl L425](code.rdl), [code.rdl L459](code.rdl), [code.rdl L490](code.rdl), [code.rdl L533](code.rdl), [code.rdl L551](code.rdl), [code.rdl L849](code.rdl), [code.rdl L898](code.rdl), [code.rdl L906](code.rdl), [code.rdl L914](code.rdl), [code.rdl L932](code.rdl), [code.rdl L958](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.PrepareRejectedCommandEvent;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅在 plannedEvents 末尾追加 ERROR 描述；长度错地面/HK/AP分别为 LC_CMD_LEN_ERR_EID / LC_HKREQ_LEN_ERR_EID / LC_APSAMPLE_LEN_ERR_EID，包含 MID/FcnCode/ActualLength/ExpectedLength。
- 参数错按明确命令和失败前置匹配：LC状态非法用LC_LCSTATE_ERR_EID；AP新状态非法/索引越界/当前NOT_USED或PERMOFF分别LC_APSTATE_NEW_ERR_EID/LC_APSTATE_APNUM_ERR_EID/LC_APSTATE_CURR_ERR_EID；永久关闭ALL或索引错/原状态非DISABLED分别LC_APOFF_APNUM_ERR_EID/LC_APOFF_CURR_ERR_EID；AP/WP统计索引错分别LC_APSTATS_APNUM_ERR_EID/LC_WPSTATS_WPNUM_ERR_EID，均ERROR且参数来自当前原payload。
- 未知FcnCode用 LC_CC_ERR_EID；参数错误沿当前handler对应LC_*ERR_EID。事件文本和参数来自源码，不表示 CFE_EVS_SendEvent 已执行。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L10–10 LC1002

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L40–114 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L121–256 *VerifyDispatch

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0105"></a>

## ST-LC-0105 — 普通有效地面命令计数加一

操作：Compute；需求：REQ-LC-0001, REQ-LC-0004, REQ-LC-0035, REQ-LC-0036, REQ-LC-0037, REQ-LC-0038, REQ-LC-0039, REQ-LC-0040, REQ-LC-0041, REQ-LC-0042, REQ-LC-0043, REQ-LC-0044, REQ-LC-0046, REQ-LC-0047, REQ-LC-0048, REQ-LC-0049

资源：RES-LC-0105

当前位置：[code.rdl L363](code.rdl), [code.rdl L408](code.rdl), [code.rdl L524](code.rdl), [code.rdl L889](code.rdl), [code.rdl L949](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.IncrementAcceptedGroundCommand;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 对Noop、有效状态命令、有效统计复位命令，仅将 AppData.CmdCount 工作副本按原类型加一，保持其他成员不变。
- ResetCounters 不得套用本步到实现流程：源码reset命令直接清六项计数且不加一；LC1003与LC1001冲突另登记。内部HK/AP请求不经过本步。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L2–2 LC1000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L267–279 LC_NoopCmd

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L157–165 LC_NoopVerifyDispatch

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L11–11 LC1003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L267–293 LC_NoopCmd / LC_ResetCountersCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L317–345 LC_SetLCStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L460–468 LC_SetAPStateCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L90–90 LC4000

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L280–281 LC_CheckMsgForWPs

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L52–55 LC_SampleAPReq

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L150–197 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L91–91 LC4001

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L92–92 LC4002

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L102–102 LC4009

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L481–537 LC_SetAPPermOffCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L104–110 LC4010

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L544–611 LC_ResetAPStatsCmd / LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L111–117 LC4011

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L118–126 LC4012

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L619–691 LC_ResetWPStatsCmd / LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L127–135 LC4013

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0106"></a>

## ST-LC-0106 — 形成命令成功事件描述

操作：Compute；需求：REQ-LC-0001, REQ-LC-0002, REQ-LC-0004, REQ-LC-0035, REQ-LC-0036, REQ-LC-0037, REQ-LC-0038, REQ-LC-0039, REQ-LC-0040, REQ-LC-0041, REQ-LC-0042, REQ-LC-0043, REQ-LC-0044, REQ-LC-0046, REQ-LC-0047, REQ-LC-0048, REQ-LC-0049

资源：RES-LC-0106

当前位置：[code.rdl L365](code.rdl), [code.rdl L410](code.rdl), [code.rdl L473](code.rdl), [code.rdl L526](code.rdl), [code.rdl L891](code.rdl), [code.rdl L951](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.PrepareAcceptedCommandEvent;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅按被接受命令分支追加 INFORMATION 描述：Noop LC_NOOP_INF_EID含版本；reset LC_RESET_INF_EID；LC state LC_LCSTATE_INF_EID含new state；AP state LC_APSTATE_INF_EID含APNumber/new state；PermOff LC_APOFF_INF_EID；AP/WP stats LC_APSTATS_INF_EID / LC_WPSTATS_INF_EID。
- 保持计数、表、模式不变；不生成RTS请求；事件实际提交仍待确认。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L2–2 LC1000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L267–279 LC_NoopCmd

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L157–165 LC_NoopVerifyDispatch

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L3–9 LC1001

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L287–310 LC_ResetCountersCmd / LC_ResetCounters

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L11–11 LC1003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L267–293 LC_NoopCmd / LC_ResetCountersCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L317–345 LC_SetLCStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L460–468 LC_SetAPStateCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L90–90 LC4000

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L280–281 LC_CheckMsgForWPs

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L52–55 LC_SampleAPReq

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L150–197 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L91–91 LC4001

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L92–92 LC4002

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L102–102 LC4009

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L481–537 LC_SetAPPermOffCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L104–110 LC4010

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L544–611 LC_ResetAPStatsCmd / LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L111–117 LC4011

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L118–126 LC4012

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L619–691 LC_ResetWPStatsCmd / LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L127–135 LC4013

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0107"></a>

## ST-LC-0107 — 提交命令工作副本的实际状态变更

操作：Set；需求：REQ-LC-0001, REQ-LC-0002, REQ-LC-0003, REQ-LC-0004, REQ-LC-0005, REQ-LC-0035, REQ-LC-0036, REQ-LC-0037, REQ-LC-0038, REQ-LC-0039, REQ-LC-0040, REQ-LC-0041, REQ-LC-0042, REQ-LC-0043, REQ-LC-0044, REQ-LC-0045, REQ-LC-0046, REQ-LC-0047, REQ-LC-0048, REQ-LC-0049, REQ-LC-0072, REQ-LC-0073

资源：RES-LC-0107

当前位置：[code.rdl L177](code.rdl), [code.rdl L200](code.rdl), [code.rdl L359](code.rdl), [code.rdl L367](code.rdl), [code.rdl L396](code.rdl), [code.rdl L428](code.rdl), [code.rdl L467](code.rdl), [code.rdl L475](code.rdl), [code.rdl L498](code.rdl), [code.rdl L536](code.rdl), [code.rdl L559](code.rdl), [code.rdl L857](code.rdl), [code.rdl L917](code.rdl), [code.rdl L940](code.rdl), [code.rdl L961](code.rdl)

```spacerdl
Set LCCommandPersistentState CommandContext;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：持久绑定：LCCommandPersistentState。仅将 rules 指定的原 LC 内存成员从 CommandContext 操作后工作快照写入；不是 cFE服务提交，不修改其他存储。

规则：

- 将本入口明确改动的 LC_AppData.CmdCount/CmdErrCount/其他六项HK计数、CurrentLCState，选定 ART.CurrentState/AP统计及WRT统计写回各原存储。
- 未改动成员和未选定条目保持不变。plannedEvents 只作为输出，不由 Set 发送；不得把派生拒绝outcome写入原不存在的LC成员。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L2–2 LC1000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L267–279 LC_NoopCmd

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L157–165 LC_NoopVerifyDispatch

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L3–9 LC1001

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L287–310 LC_ResetCountersCmd / LC_ResetCounters

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L10–10 LC1002

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L40–114 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L121–256 *VerifyDispatch

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L11–11 LC1003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L267–293 LC_NoopCmd / LC_ResetCountersCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L317–345 LC_SetLCStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L460–468 LC_SetAPStateCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L90–90 LC4000

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L280–281 LC_CheckMsgForWPs

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L52–55 LC_SampleAPReq

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L150–197 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L91–91 LC4001

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L92–92 LC4002

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L102–102 LC4009

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L481–537 LC_SetAPPermOffCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L103–103 LC4009.1

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L389–439 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L104–110 LC4010

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L544–611 LC_ResetAPStatsCmd / LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L111–117 LC4011

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L118–126 LC4012

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L619–691 LC_ResetWPStatsCmd / LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L127–135 LC4013

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0108"></a>

## ST-LC-0108 — 复位六项housekeeping计数

操作：Compute；需求：REQ-LC-0002, REQ-LC-0004, REQ-LC-0051, REQ-LC-0054, REQ-LC-0058, REQ-LC-0074

资源：RES-LC-0108

当前位置：[code.rdl L443](code.rdl), [code.rdl L471](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.ResetHousekeepingCounters;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅清零 AppData.CmdCount、CmdErrCount、APSampleCount、MonitoredMsgCount、RTSExecCount、PassiveRTSExecCount 六个工作副本成员。
- 不改 CurrentLCState、WRT/ART、CDSSavedOnExit；reset命令实现没有随后CmdCount++。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L3–9 LC1001

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L287–310 LC_ResetCountersCmd / LC_ResetCounters

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L11–11 LC1003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L267–293 LC_NoopCmd / LC_ResetCountersCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L317–345 LC_SetLCStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L460–468 LC_SetAPStateCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L146–155 LC9000

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L187–216 LC_AppInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L991–1011 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L301–310 LC_ResetCounters

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L173–173 LC9003

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L386–478 LC_TableInit

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L88–102 LC_SAVE_TO_CDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L182–182 LC9004.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–881 LC_CreateTaskCDS

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0109"></a>

## ST-LC-0109 — 记录Reset的一般有效命令规则冲突

操作：Compute；需求：REQ-LC-0002, REQ-LC-0004

资源：RES-LC-0109

当前位置：[code.rdl L445](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.ApplyDocumentaryResetAcceptance;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- documentary义务视图：在六计数已归零的工作副本上，对LC1003的通用有效地面命令规则计算CmdCount=1。
- 该结果不提交原持久存储，不冒充源码行为；它与LC1001要求最终ValidCommandCounter=0及源码未递增并存，等待需求解释。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L3–9 LC1001

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L287–310 LC_ResetCountersCmd / LC_ResetCounters

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L11–11 LC1003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L267–293 LC_NoopCmd / LC_ResetCountersCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L317–345 LC_SetLCStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L460–468 LC_SetAPStateCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0110"></a>

## ST-LC-0110 — 核验新LC应用状态

操作：Compute；需求：REQ-LC-0005, REQ-LC-0035, REQ-LC-0036, REQ-LC-0037

资源：RES-LC-0110

当前位置：[code.rdl L944](code.rdl)

```spacerdl
Compute RequestedLCStateValid CommandContext ReqCapByFormTable FormulaTable.ValidateRequestedLCState;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：RequestedLCStateValid 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE仅当NewLCState为LC_STATE_ACTIVE/PASSIVE/DISABLED三者之一；否则FALSE。
- 不改变CurrentLCState，不执行事件服务。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L90–90 LC4000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L317–345 LC_SetLCStateCmd

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L280–281 LC_CheckMsgForWPs

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L52–55 LC_SampleAPReq

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L150–197 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L91–91 LC4001

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L92–92 LC4002

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0111"></a>

## ST-LC-0111 — 计算新的应用工作模式

操作：Compute；需求：REQ-LC-0035, REQ-LC-0036, REQ-LC-0037

资源：RES-LC-0111

当前位置：[code.rdl L947](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.AssignRequestedLCState;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 长度和参数有效后，仅将 AppData.CurrentLCState 工作副本改为命令NewLCState；其具体值由命令明示，不默认ACTIVE。
- ACTIVE允许后续WP/AP处理及动作条件判断；PASSIVE允许处理但动作抑制；DISABLED禁止WP/AP处理。这些后续入口由各自流程读取持久状态，不在本操作执行采样或RTS。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L90–90 LC4000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L317–345 LC_SetLCStateCmd

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L280–281 LC_CheckMsgForWPs

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L52–55 LC_SampleAPReq

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L150–197 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L91–91 LC4001

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L92–92 LC4002

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0112"></a>

## ST-LC-0112 — 核验新AP状态枚举

操作：Compute；需求：REQ-LC-0005, REQ-LC-0038, REQ-LC-0039, REQ-LC-0040, REQ-LC-0041, REQ-LC-0042, REQ-LC-0043, REQ-LC-0072

资源：RES-LC-0112

当前位置：[code.rdl L861](code.rdl)

```spacerdl
Compute RequestedAPStateValid CommandContext ReqCapByFormTable FormulaTable.ValidateRequestedAPState;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：RequestedAPStateValid 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE仅当NewAPState为LC_APSTATE_ACTIVE/PASSIVE/DISABLED；PERMOFF须独立命令，NOT_USED不是允许目标。
- FALSE保留所有ART条目不变并用LC_APSTATE_NEW_ERR_EID拒绝描述。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0113"></a>

## ST-LC-0113 — 解析AP单选或ALL目标范围

操作：Compute；需求：REQ-LC-0005, REQ-LC-0038, REQ-LC-0039, REQ-LC-0040, REQ-LC-0041, REQ-LC-0042, REQ-LC-0043, REQ-LC-0072

资源：RES-LC-0113

当前位置：[code.rdl L833](code.rdl), [code.rdl L864](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.ResolveCommandAPSelection;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- APNumber=LC_ALL_ACTIONPOINTS时range=[0,LC_MAX_ACTIONPOINTS-1]、selectionAll=true；单选APNumber<LC_MAX_ACTIONPOINTS时range=[APNumber,APNumber]。
- 其他APNumber令selectionValid=false且错误LC_APSTATE_APNUM_ERR_EID。合法时cursor=range.start、commandSuccess=(ALL时true，单选时false)；仅改range/cursor/选择旗标，不改ART。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0114"></a>

## ST-LC-0114 — 取得AP选择合法性

操作：Compute；需求：REQ-LC-0005, REQ-LC-0038, REQ-LC-0039, REQ-LC-0040, REQ-LC-0041, REQ-LC-0042, REQ-LC-0043, REQ-LC-0072

资源：RES-LC-0114

当前位置：[code.rdl L866](code.rdl)

```spacerdl
Compute CommandAPSelectionValid CommandContext ReqCapByFormTable FormulaTable.CommandAPSelectionIsValid;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：CommandAPSelectionValid 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- 直接输出上一步selectionValid，不在本步重新改变或猜测目标索引。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0115"></a>

## ST-LC-0115 — 检查AP目标游标是否结束

操作：Compute；需求：REQ-LC-0038, REQ-LC-0039, REQ-LC-0040, REQ-LC-0041, REQ-LC-0042, REQ-LC-0043, REQ-LC-0072

资源：RES-LC-0115

当前位置：[code.rdl L869](code.rdl), [code.rdl L883](code.rdl)

```spacerdl
Compute CommandAPTargetsRemain CommandContext ReqCapByFormTable FormulaTable.HasMoreCommandAPTargets;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：CommandAPTargetsRemain 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当selectionValid且cursor<=range.end；FALSE表示有限范围遍历终止；范围来自已验证平台容量。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0116"></a>

## ST-LC-0116 — 检查当前AP是否允许状态切换

操作：Compute；需求：REQ-LC-0038, REQ-LC-0039, REQ-LC-0040, REQ-LC-0041, REQ-LC-0042, REQ-LC-0043, REQ-LC-0045, REQ-LC-0072

资源：RES-LC-0116

当前位置：[code.rdl L872](code.rdl)

```spacerdl
Compute CommandAPTargetMutable CommandContext ReqCapByFormTable FormulaTable.CommandAPTargetIsMutable;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：CommandAPTargetMutable 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- 读取ART[cursor].CurrentState；TRUE仅当不是LC_APSTATE_NOT_USED且不是LC_APSTATE_PERMOFF。
- FALSE时ALL模式只跳过该条目，单选模式拒绝命令；禁止被跳过AP产生结果/RTS/事件。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L103–103 LC4009.1

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L389–439 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0117"></a>

## ST-LC-0117 — 计算一个可变AP的新状态

操作：Compute；需求：REQ-LC-0038, REQ-LC-0039, REQ-LC-0040, REQ-LC-0041, REQ-LC-0042, REQ-LC-0043, REQ-LC-0072

资源：RES-LC-0117

当前位置：[code.rdl L875](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.AssignOneRequestedAPState;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅将ART[cursor].CurrentState工作副本改为NewAPState并把commandSuccess=true。
- 保留该AP的ActionResult及全部统计，保留其他AP及AppData；实际状态由末尾Set提交。DISABLED目标禁止该AP后续评估/动作/评估事件，不禁止该状态命令自己的成功事件。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0118"></a>

## ST-LC-0118 — 处理不可变AP的全选跳过或单选拒绝

操作：Compute；需求：REQ-LC-0005, REQ-LC-0038, REQ-LC-0039, REQ-LC-0040, REQ-LC-0041, REQ-LC-0042, REQ-LC-0043, REQ-LC-0045, REQ-LC-0072

资源：RES-LC-0118

当前位置：[code.rdl L878](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.RejectOrSkipImmutableAPTarget;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- selectionAll=true：只记录该目标为skipped，保持ART且不改地面命令计数，整个ALL命令可成功。
- selectionAll=false：outcome=rejected、handlerEnabled=false、rejectionEvent=LC_APSTATE_CURR_ERR_EID，保持ART；若原PERMOFF且请求ACTIVE同时实现LC4009.1拒绝义务。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L103–103 LC4009.1

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L389–439 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0119"></a>

## ST-LC-0119 — 推进AP状态命令游标

操作：Compute；需求：REQ-LC-0038, REQ-LC-0039, REQ-LC-0040, REQ-LC-0041, REQ-LC-0042, REQ-LC-0043, REQ-LC-0072

资源：RES-LC-0119

当前位置：[code.rdl L881](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.AdvanceCommandAPCursor;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅cursor加一（已验证有限range内），其他成员保持不变；后继必须重新计算CommandAPTargetsRemain。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0120"></a>

## ST-LC-0120 — 读取AP状态命令最终成功标志

操作：Compute；需求：REQ-LC-0004, REQ-LC-0005, REQ-LC-0038, REQ-LC-0039, REQ-LC-0040, REQ-LC-0041, REQ-LC-0042, REQ-LC-0043, REQ-LC-0072

资源：RES-LC-0120

当前位置：[code.rdl L886](code.rdl)

```spacerdl
Compute CommandAPStateSuccess CommandContext ReqCapByFormTable FormulaTable.CommandAPStateSucceeded;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：CommandAPStateSuccess 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE=commandSuccess。ALL模式合法时即使无可变条目仍TRUE；单选只有实际允许赋值后TRUE。
- FALSE仅在合法选择的不可变单项，末尾走拒绝计数/事件而不是成功路径。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L11–11 LC1003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L267–293 LC_NoopCmd / LC_ResetCountersCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L317–345 LC_SetLCStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L460–468 LC_SetAPStateCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0121"></a>

## ST-LC-0121 — 保留单项/ALL对指定AP的原文状态赋值义务

操作：Compute；需求：REQ-LC-0038, REQ-LC-0039, REQ-LC-0040, REQ-LC-0041, REQ-LC-0042, REQ-LC-0043, REQ-LC-0045

资源：RES-LC-0121

当前位置：[code.rdl L835](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.ApplyLiteralSelectedAPStateObligation;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- documentary视图只把已合法选择的range内各ART.CurrentState工作副本改为NewAPState：单项只改该条目，ALL改全部条目；不擅自加入原文未声明的NOT_USED/PERMOFF例外。
- 此变化不进行持久Set，不冒充源码行为。PERMOFF激活与LC4009.1、代码单项拒绝/ALL跳过，以及NOT_USED例外分别登记，等待正式需求解释。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L103–103 LC4009.1

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L389–439 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0122"></a>

## ST-LC-0122 — 永久关闭仅允许单个有效AP索引

操作：Compute；需求：REQ-LC-0005, REQ-LC-0044, REQ-LC-0073

资源：RES-LC-0122

当前位置：[code.rdl L400](code.rdl)

```spacerdl
Compute PermOffSingleAPIndexValid CommandContext ReqCapByFormTable FormulaTable.ValidatePermOffSingleAPIndex;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：PermOffSingleAPIndexValid 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当APNumber不是LC_ALL_ACTIONPOINTS且小于LC_MAX_ACTIONPOINTS；否则FALSE，错误LC_APOFF_APNUM_ERR_EID。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L102–102 LC4009

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L481–537 LC_SetAPPermOffCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0123"></a>

## ST-LC-0123 — 永久关闭的原状态门控

操作：Compute；需求：REQ-LC-0005, REQ-LC-0044, REQ-LC-0073

资源：RES-LC-0123

当前位置：[code.rdl L403](code.rdl)

```spacerdl
Compute PermOffAPDisabled CommandContext ReqCapByFormTable FormulaTable.PermOffAPWasDisabled;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：PermOffAPDisabled 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- 读取ART[APNumber].CurrentState；TRUE仅为LC_APSTATE_DISABLED。FALSE不改ART，错误LC_APOFF_CURR_ERR_EID。
- 这一前置是代码事实，LC4009原文未给出，需要独立列冲突。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L102–102 LC4009

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L481–537 LC_SetAPPermOffCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0124"></a>

## ST-LC-0124 — 计算单AP永久关闭状态

操作：Compute；需求：REQ-LC-0044, REQ-LC-0045, REQ-LC-0073

资源：RES-LC-0124

当前位置：[code.rdl L406](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.AssignAPPermanentOff;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只将有效已DISABLED AP的CurrentState工作副本改为LC_APSTATE_PERMOFF；保留ActionResult和统计。
- 后续普通状态命令不得再激活该条目；表替换或不保存CDS的初始化可采用ADT默认状态，不把永久性夸大为硬件永久锁定。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L102–102 LC4009

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L481–537 LC_SetAPPermOffCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L103–103 LC4009.1

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L389–439 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0125"></a>

## ST-LC-0125 — 保留永久关闭命令的无前置原文义务

操作：Compute；需求：REQ-LC-0044, REQ-LC-0073

资源：RES-LC-0125

当前位置：[code.rdl L374](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.ApplyDocumentaryPermanentOff;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- documentary视图：对有效单个命令指定AP，仅计算CurrentState=PERMOFF，不加入原文未声明的必须先Disabled限制。
- 该快照不进行持久Set，记录与实现前置的差异待确认；不补造允许重启外的再激活规则。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L102–102 LC4009

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L481–537 LC_SetAPPermOffCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0126"></a>

## ST-LC-0126 — 解析统计复位的AP/WP单选或ALL范围

操作：Compute；需求：REQ-LC-0005, REQ-LC-0046, REQ-LC-0047, REQ-LC-0048, REQ-LC-0049, REQ-LC-0074

资源：RES-LC-0126

当前位置：[code.rdl L502](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.ResolveStatsResetRange;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 根据真实命令route选APNumber/LC_ALL_ACTIONPOINTS/LC_MAX_ACTIONPOINTS，或WPNumber/LC_ALL_WATCHPOINTS/LC_MAX_WATCHPOINTS；ALL=[0,max-1]、有效单项=[number,number]。
- 越界令statsSelectionValid=false并保存LC_APSTATS_APNUM_ERR_EID或LC_WPSTATS_WPNUM_ERR_EID；合法cursor=start。只改选择阶段字段，不改表或计数。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L104–110 LC4010

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L544–611 LC_ResetAPStatsCmd / LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L111–117 LC4011

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L118–126 LC4012

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L619–691 LC_ResetWPStatsCmd / LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L127–135 LC4013

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0127"></a>

## ST-LC-0127 — 读取统计复位范围合法性

操作：Compute；需求：REQ-LC-0005, REQ-LC-0046, REQ-LC-0047, REQ-LC-0048, REQ-LC-0049

资源：RES-LC-0127

当前位置：[code.rdl L504](code.rdl)

```spacerdl
Compute StatsResetSelectionValid CommandContext ReqCapByFormTable FormulaTable.StatsResetSelectionIsValid;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：StatsResetSelectionValid 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- 输出上一阶段statsSelectionValid，FALSE禁止统计清零；不假设非法范围能剪裁执行。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L104–110 LC4010

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L544–611 LC_ResetAPStatsCmd / LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L111–117 LC4011

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L118–126 LC4012

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L619–691 LC_ResetWPStatsCmd / LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L127–135 LC4013

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0128"></a>

## ST-LC-0128 — 检查统计复位游标终止条件

操作：Compute；需求：REQ-LC-0046, REQ-LC-0047, REQ-LC-0048, REQ-LC-0049, REQ-LC-0074

资源：RES-LC-0128

当前位置：[code.rdl L509](code.rdl), [code.rdl L521](code.rdl)

```spacerdl
Compute StatsResetTargetsRemain CommandContext ReqCapByFormTable FormulaTable.HasMoreStatsResetTargets;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：StatsResetTargetsRemain 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当statsSelectionValid且cursor<=range.end；有限范围由实际最大数提供。FALSE无动作结束循环。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L104–110 LC4010

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L544–611 LC_ResetAPStatsCmd / LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L111–117 LC4011

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L118–126 LC4012

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L619–691 LC_ResetWPStatsCmd / LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L127–135 LC4013

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0129"></a>

## ST-LC-0129 — 区分AP与WP统计复位负载

操作：Compute；需求：REQ-LC-0046, REQ-LC-0047, REQ-LC-0048, REQ-LC-0049, REQ-LC-0074

资源：RES-LC-0129

当前位置：[code.rdl L507](code.rdl)

```spacerdl
Compute StatsResetTargetsAP CommandContext ReqCapByFormTable FormulaTable.StatsResetTargetsAP;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：StatsResetTargetsAP 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当route是ResetAPStats，FALSE当route是已核验ResetWPStats；不能把任意其他命令当WP复位。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L104–110 LC4010

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L544–611 LC_ResetAPStatsCmd / LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L111–117 LC4011

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L118–126 LC4012

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L619–691 LC_ResetWPStatsCmd / LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L127–135 LC4013

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0130"></a>

## ST-LC-0130 — 复位一个AP的统计且保留状态和结果

操作：Compute；需求：REQ-LC-0046, REQ-LC-0047, REQ-LC-0074

资源：RES-LC-0130

当前位置：[code.rdl L513](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.ResetSelectedAPStatistics;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只将ART[cursor]六项正式统计FailToPassCount、PassToFailCount、ConsecutiveFailCount、CumulativeFailCount、CumulativeRTSExecCount、CumulativeEventMsgsSent归零；实现另外PassiveAPCount也归零。
- ResetStatsCmd=true：CurrentState、ActionResult严格保持原值；保留其他条目、WRT、AppData。不是初始化，不把结果改为STALE。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L104–110 LC4010

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L544–611 LC_ResetAPStatsCmd / LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L111–117 LC4011

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0131"></a>

## ST-LC-0131 — 复位一个WP的统计且保留结果和年龄

操作：Compute；需求：REQ-LC-0048, REQ-LC-0049, REQ-LC-0074

资源：RES-LC-0131

当前位置：[code.rdl L516](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.ResetSelectedWPStatistics;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只将WRT[cursor]的EvaluationCount、FalseToTrueCount、ConsecutiveTrueCount、CumulativeTrueCount归零；LastFalseToTrue.Value及Timestamp.Seconds/Subseconds、LastTrueToFalse.Value及Timestamp.Seconds/Subseconds归零。
- ResetStatsCmd=true：WatchResult和CountdownToStale严格保持原值；保留其他条目、ART、AppData。正式八类统计含两个时间戳，但实现时间戳各含Seconds和Subseconds，均清零。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L118–126 LC4012

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L619–691 LC_ResetWPStatsCmd / LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L127–135 LC4013

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0132"></a>

## ST-LC-0132 — 推进统计复位游标

操作：Compute；需求：REQ-LC-0046, REQ-LC-0047, REQ-LC-0048, REQ-LC-0049, REQ-LC-0074

资源：RES-LC-0132

当前位置：[code.rdl L519](code.rdl)

```spacerdl
Compute CommandContext CommandContext ReqCapByFormTable FormulaTable.AdvanceStatsResetCursor;
```

输入绑定：独立已接收地面命令入口：原 CFE_SB_Buffer_t 的 MID、FcnCode、声明长度及各命令 payload，编译分支配置、sizeof 命令结构的期待长度，入口时 LC_AppData、ART、WRT 的完整工作副本；阶段字段含 route、lengthValid、outcome、AP/WP cursor/range、selectedOldState、plannedEvents。每项 Compute 读取该平坦符号操作前快照并写同一平坦符号操作后快照；字段仅按当前 rules 改动，其他字段保持。接收及聚合序列化 pending。

输出绑定：前一操作写出的 CommandContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅cursor加一；保持刚复位的工作表和其他状态；后续必须重新计算StatsResetTargetsRemain。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L104–110 LC4010

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L544–611 LC_ResetAPStatsCmd / LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L111–117 LC4011

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L118–126 LC4012

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L619–691 LC_ResetWPStatsCmd / LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L127–135 LC4013

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0133"></a>

## ST-LC-0133 — 构造HK基本字段快照

操作：Compute；需求：REQ-LC-0050, REQ-LC-0077

资源：RES-LC-0133

当前位置：[code.rdl L204](code.rdl)

```spacerdl
Compute HKContext HKContext ReqCapByFormTable FormulaTable.CopyHousekeepingBaseFields;
```

输入绑定：独立 LC_SEND_HK_MID 有效长度请求入口：复制请求及入口时 LC_AppData、WRT、ART、WatchpointCount 与 HkPacket；工作字段包括 tableIndex、packByte、activeCount、payload、effects。各 Compute 读前值写后值，不自动执行服务。

输出绑定：前一操作写出的 HKContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 从入口AppData读取CmdCount、CmdErrCount、APSampleCount、MonitoredMsgCount、RTSExecCount、PassiveRTSExecCount、CurrentLCState复制到payload；WatchpointCount复制payload.WPsInUse。
- 只把payload.ActiveAPs清零、wpTableIndex=0、apTableIndex=0；不清持久CmdCount，不更新任何AP/WP统计；WP/AP位图由随后打包步骤填。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L136–145 LC8000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L114–260 LC_SendHkCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L140–253 LC_SendHkCmd

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L89–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0134"></a>

## ST-LC-0134 — HK的WP打包组终止条件

操作：Compute；需求：REQ-LC-0050, REQ-LC-0077, REQ-LC-0082

资源：RES-LC-0134

当前位置：[code.rdl L206](code.rdl), [code.rdl L213](code.rdl)

```spacerdl
Compute HKWatchpointGroupsRemain HKContext ReqCapByFormTable FormulaTable.HasMoreHKWatchpointGroups;
```

输入绑定：独立 LC_SEND_HK_MID 有效长度请求入口：复制请求及入口时 LC_AppData、WRT、ART、WatchpointCount 与 HkPacket；工作字段包括 tableIndex、packByte、activeCount、payload、effects。各 Compute 读前值写后值，不自动执行服务。

输出绑定：HKWatchpointGroupsRemain 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当wpTableIndex<LC_MAX_WATCHPOINTS，且容量前置已确认4整除；FALSE结束。未确认容量约束不得执行越界前取。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L136–145 LC8000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L114–260 LC_SendHkCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L140–253 LC_SendHkCmd

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L89–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L86–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0135"></a>

## ST-LC-0135 — 把四个WP结果打包为一字节

操作：Compute；需求：REQ-LC-0050, REQ-LC-0077, REQ-LC-0082

资源：RES-LC-0135

当前位置：[code.rdl L209](code.rdl)

```spacerdl
Compute HKContext HKContext ReqCapByFormTable FormulaTable.PackFourHKWatchResults;
```

输入绑定：独立 LC_SEND_HK_MID 有效长度请求入口：复制请求及入口时 LC_AppData、WRT、ART、WatchpointCount 与 HkPacket；工作字段包括 tableIndex、packByte、activeCount、payload、effects。各 Compute 读前值写后值，不自动执行服务。

输出绑定：前一操作写出的 HKContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 在wpTableIndex当前组按源码次序访问wpTableIndex+3-i (i=0..3)，Shift=6-2*i，映射STALE/FALSE/TRUE/ERROR到LC_HKWR_*码；未知结果按ERROR。
- 首项直接赋ByteData，后3项OR合并；仅写payload.WPResults[wpTableIndex/4]。不修改WRT.WatchResult、年龄或任何统计。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L136–145 LC8000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L114–260 LC_SendHkCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L140–253 LC_SendHkCmd

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L89–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L86–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0136"></a>

## ST-LC-0136 — 推进HK WP打包组游标

操作：Compute；需求：REQ-LC-0050, REQ-LC-0082

资源：RES-LC-0136

当前位置：[code.rdl L211](code.rdl)

```spacerdl
Compute HKContext HKContext ReqCapByFormTable FormulaTable.AdvanceHKWatchpointGroup;
```

输入绑定：独立 LC_SEND_HK_MID 有效长度请求入口：复制请求及入口时 LC_AppData、WRT、ART、WatchpointCount 与 HkPacket；工作字段包括 tableIndex、packByte、activeCount、payload、effects。各 Compute 读前值写后值，不自动执行服务。

输出绑定：前一操作写出的 HKContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅wpTableIndex加4，保持payload已填字节和所有持久LC状态；重算HKWatchpointGroupsRemain。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L136–145 LC8000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L114–260 LC_SendHkCmd

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L86–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L140–253 LC_SendHkCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0137"></a>

## ST-LC-0137 — HK的AP打包组终止条件

操作：Compute；需求：REQ-LC-0050, REQ-LC-0077, REQ-LC-0082

资源：RES-LC-0137

当前位置：[code.rdl L216](code.rdl), [code.rdl L225](code.rdl)

```spacerdl
Compute HKActionpointGroupsRemain HKContext ReqCapByFormTable FormulaTable.HasMoreHKActionpointGroups;
```

输入绑定：独立 LC_SEND_HK_MID 有效长度请求入口：复制请求及入口时 LC_AppData、WRT、ART、WatchpointCount 与 HkPacket；工作字段包括 tableIndex、packByte、activeCount、payload、effects。各 Compute 读前值写后值，不自动执行服务。

输出绑定：HKActionpointGroupsRemain 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当apTableIndex<LC_MAX_ACTIONPOINTS，且容量前置已确认2整除；FALSE结束。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L136–145 LC8000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L114–260 LC_SendHkCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L140–253 LC_SendHkCmd

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L89–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L86–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0138"></a>

## ST-LC-0138 — 打包两个AP状态并统计ActiveAPs

操作：Compute；需求：REQ-LC-0050, REQ-LC-0077, REQ-LC-0082

资源：RES-LC-0138

当前位置：[code.rdl L219](code.rdl)

```spacerdl
Compute HKContext HKContext ReqCapByFormTable FormulaTable.PackTwoHKActionStates;
```

输入绑定：独立 LC_SEND_HK_MID 有效长度请求入口：复制请求及入口时 LC_AppData、WRT、ART、WatchpointCount 与 HkPacket；工作字段包括 tableIndex、packByte、activeCount、payload、effects。各 Compute 读前值写后值，不自动执行服务。

输出绑定：前一操作写出的 HKContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 当前组按apTableIndex+1-i (i=0,1)，Shift=6-4*i，把ART.CurrentState映射LC_HKAR_STATE_*。ACTIVE/PASSIVE/DISABLED/NOT_USED各为原编码；PERMOFF和未知都映射NOT_USED。
- 首项赋apPackByte，第二项OR；仅对每个实际ACTIVE条目把payload.ActiveAPs加一，不把PERMOFF当Active，不改变ART状态或计数。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L136–145 LC8000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L114–260 LC_SendHkCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L140–253 LC_SendHkCmd

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L89–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L86–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0139"></a>

## ST-LC-0139 — 把两个AP结果合入状态字节

操作：Compute；需求：REQ-LC-0050, REQ-LC-0077, REQ-LC-0082

资源：RES-LC-0139

当前位置：[code.rdl L221](code.rdl)

```spacerdl
Compute HKContext HKContext ReqCapByFormTable FormulaTable.PackTwoHKActionResults;
```

输入绑定：独立 LC_SEND_HK_MID 有效长度请求入口：复制请求及入口时 LC_AppData、WRT、ART、WatchpointCount 与 HkPacket；工作字段包括 tableIndex、packByte、activeCount、payload、effects。各 Compute 读前值写后值，不自动执行服务。

输出绑定：前一操作写出的 HKContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 读取上一步apPackByte（已有状态位），按apTableIndex+1-i访问ActionResult，Shift=4-4*i；STALE/PASS/FAIL/ERROR映射LC_HKAR_*结果码，未知按ERROR。
- 只将结果位OR到已有状态位后写payload.APResults[apTableIndex/2]，不覆盖状态位，不修改ART完整状态/结果/统计。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L136–145 LC8000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L114–260 LC_SendHkCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L140–253 LC_SendHkCmd

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L89–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L86–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0140"></a>

## ST-LC-0140 — 推进HK AP打包组游标

操作：Compute；需求：REQ-LC-0050, REQ-LC-0082

资源：RES-LC-0140

当前位置：[code.rdl L223](code.rdl)

```spacerdl
Compute HKContext HKContext ReqCapByFormTable FormulaTable.AdvanceHKActionpointGroup;
```

输入绑定：独立 LC_SEND_HK_MID 有效长度请求入口：复制请求及入口时 LC_AppData、WRT、ART、WatchpointCount 与 HkPacket；工作字段包括 tableIndex、packByte、activeCount、payload、effects。各 Compute 读前值写后值，不自动执行服务。

输出绑定：前一操作写出的 HKContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅apTableIndex加2，保持payload已填字节和ActiveAPs；重算HKActionpointGroupsRemain。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L136–145 LC8000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L114–260 LC_SendHkCmd

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L86–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L140–253 LC_SendHkCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0141"></a>

## ST-LC-0141 — 提交完整HK负载到原HkPacket

操作：Set；需求：REQ-LC-0050, REQ-LC-0077

资源：RES-LC-0141

当前位置：[code.rdl L228](code.rdl)

```spacerdl
Set LC_HKPayload HKContext;
```

输入绑定：独立 LC_SEND_HK_MID 有效长度请求入口：复制请求及入口时 LC_AppData、WRT、ART、WatchpointCount 与 HkPacket；工作字段包括 tableIndex、packByte、activeCount、payload、effects。各 Compute 读前值写后值，不自动执行服务。

输出绑定：持久绑定：LC_HKPayload。仅将 rules 指定的原 LC 内存成员从 HKContext 操作后工作快照写入；不是 cFE服务提交，不修改其他存储。

规则：

- 仅将已形成payload写回LC_OperData.HkPacket.Payload：八项基础字段、WPResults、APResults及ActiveAPs；不写AppData/WRT/ART。
- payload形成不等于发送；时间戳和SB发送需独立服务绑定。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L136–145 LC8000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L114–260 LC_SendHkCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L140–253 LC_SendHkCmd

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L89–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0142"></a>

## ST-LC-0142 — 形成HK时间戳服务意图

操作：Compute；需求：REQ-LC-0050

资源：RES-LC-0142

当前位置：[code.rdl L230](code.rdl)

```spacerdl
Compute HKContext HKContext ReqCapByFormTable FormulaTable.PrepareHKTimestampRequest;
```

输入绑定：独立 LC_SEND_HK_MID 有效长度请求入口：复制请求及入口时 LC_AppData、WRT、ART、WatchpointCount 与 HkPacket；工作字段包括 tableIndex、packByte、activeCount、payload、effects。各 Compute 读前值写后值，不自动执行服务。

输出绑定：前一操作写出的 HKContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅向effects追加CFE_SB_TimeStampMsg(HkPacket.TelemetryHeader)的请求描述；时间必须来自真实框架服务，不补造now或固定时间。
- 不修改payload统计，不宣称完成实际时间戳。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L136–145 LC8000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L114–260 LC_SendHkCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0143"></a>

## ST-LC-0143 — 形成HK发送服务意图

操作：Compute；需求：REQ-LC-0050

资源：RES-LC-0143

当前位置：[code.rdl L232](code.rdl)

```spacerdl
Compute HKContext HKContext ReqCapByFormTable FormulaTable.PrepareHKTransmissionRequest;
```

输入绑定：独立 LC_SEND_HK_MID 有效长度请求入口：复制请求及入口时 LC_AppData、WRT、ART、WatchpointCount 与 HkPacket；工作字段包括 tableIndex、packByte、activeCount、payload、effects。各 Compute 读前值写后值，不自动执行服务。

输出绑定：前一操作写出的 HKContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 在已形成完整payload后向effects追加CFE_SB_TransmitMsg(HkPacket.TelemetryHeader,true)的请求描述，明确它依赖真实时间戳服务阶段。
- 原源码未检查timestamp/transmit返回值；本模型不虚构成功回执或重试。实际发送尚无严格论文软件服务绑定。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L136–145 LC8000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L114–260 LC_SendHkCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0144"></a>

## ST-LC-0144 — 区分上电和保存CriticalData的复位策略

操作：Compute；需求：REQ-LC-0051, REQ-LC-0052, REQ-LC-0053, REQ-LC-0054, REQ-LC-0055, REQ-LC-0058

资源：RES-LC-0144

当前位置：[code.rdl L241](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.SelectInitializationStrategy;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 根据原resetCause和已确认SaveCriticalData配置计算coldRequired：PowerOn为TRUE；ProcessorReset/LCAppReset且SaveCriticalData=NO为TRUE；二者且YES进入CDS恢复可用性核对。
- 设置tableSource尚未选定、fatalStatus保持原值、effects不变；不通过一个Initialize算法同时完成所有表/状态/订阅。仓库默认LC_SAVE_TO_CDS未定义不等于所有部署关闭。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L146–155 LC9000

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L187–216 LC_AppInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L991–1011 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L301–310 LC_ResetCounters

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L156–163 LC9001

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L994–997 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L164–172 LC9002

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L999–1000 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L173–173 LC9003

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L386–478 LC_TableInit

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L88–102 LC_SAVE_TO_CDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L174–179 LC9004

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–521 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L613–769 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L777–902 LC_CreateTaskCDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L182–182 LC9004.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–881 LC_CreateTaskCDS

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0145"></a>

## ST-LC-0145 — 读取等价上电初始化条件

操作：Compute；需求：REQ-LC-0051, REQ-LC-0054, REQ-LC-0058

资源：RES-LC-0145

当前位置：[code.rdl L243](code.rdl)

```spacerdl
Compute InitializationRequiresColdData InitContext ReqCapByFormTable FormulaTable.InitializationRequiresColdData;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：InitializationRequiresColdData 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- 输出上一步coldRequired；不把任何初始化原因合并成固定周期。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L146–155 LC9000

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L187–216 LC_AppInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L991–1011 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L301–310 LC_ResetCounters

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L173–173 LC9003

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L386–478 LC_TableInit

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L88–102 LC_SAVE_TO_CDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L182–182 LC9004.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–881 LC_CreateTaskCDS

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0146"></a>

## ST-LC-0146 — 核对五对象全部恢复成功与APP保存标志

操作：Compute；需求：REQ-LC-0055, REQ-LC-0058, REQ-LC-0076

资源：RES-LC-0146

当前位置：[code.rdl L262](code.rdl)

```spacerdl
Compute CriticalRestoreComplete InitContext ReqCapByFormTable FormulaTable.AllFiveCriticalObjectsRestored;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：CriticalRestoreComplete 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE要求外部真实 TableResults 同时含WRT_CDS_RESTORED、ART_CDS_RESTORED、APP_CDS_RESTORED、WDT_TBL_RESTORED、ADT_TBL_RESTORED。
- APP恢复标志仅在RestoreFromCDS返回CFE_SUCCESS且恢复AppData.CDSSavedOnExit=LC_CDS_SAVED时成立；否则FALSE并进行完整cold fallback。
- 这只是源码全或无的状态核对，不额外证明语义有效性；服务结果未取得则输入pending，不推断FALSE/TRUE。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L174–179 LC9004

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–521 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L613–769 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L777–902 LC_CreateTaskCDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L182–182 LC9004.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–881 LC_CreateTaskCDS

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0147"></a>

## ST-LC-0147 — 接收恢复的LC AppData/HK计数工作副本

操作：Compute；需求：REQ-LC-0055, REQ-LC-0056, REQ-LC-0057, REQ-LC-0076

资源：RES-LC-0147

当前位置：[code.rdl L265](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.UseRestoredCriticalAppData;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅将外部真实RestoreFromCDS返回的完整LC_AppData复制到工作AppData（六计数、CurrentLCState、CDSSavedOnExit等原成员），保持WRT/ART/WDT/ADT不变。
- 只有CriticalRestoreComplete=TRUE路径可将它作为最终恢复状态；HK负载是LC_OperData未保存成员，实际下次HK从恢复AppData/WRT/ART重建，不称恢复HkPacket内存。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L174–179 LC9004

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–521 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L613–769 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L777–902 LC_CreateTaskCDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L180–180 LC9004.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–889 LC_CreateTaskCDS

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L105–127 LC_STATE_WHEN_CDS_RESTORED

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L181–181 LC9004.1.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0148"></a>

## ST-LC-0148 — 接收恢复WRT统计和结果工作副本

操作：Compute；需求：REQ-LC-0055, REQ-LC-0076

资源：RES-LC-0148

当前位置：[code.rdl L267](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.UseRestoredCriticalWatchResults;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只将真实CDS返回WRT全表复制到工作WRT，包括WatchResult、CountdownToStale、所有计数和两向值/时间；其他四对象保持不变。
- 不把部分成功数据用作完成初始化。真实CDS读取服务仍pending。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L174–179 LC9004

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–521 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L613–769 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L777–902 LC_CreateTaskCDS

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0149"></a>

## ST-LC-0149 — 接收恢复ART统计和状态工作副本

操作：Compute；需求：REQ-LC-0055, REQ-LC-0076, REQ-LC-0077

资源：RES-LC-0149

当前位置：[code.rdl L269](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.UseRestoredCriticalActionResults;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只将真实CDS返回ART全表复制到工作ART，包括ActionResult、CurrentState、全部计数；其他四对象保持不变。
- 不把PERMOFF重写为NOT_USED（那仅是HK打包视图）。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L174–179 LC9004

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–521 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L613–769 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L777–902 LC_CreateTaskCDS

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L140–253 LC_SendHkCmd

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L89–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0150"></a>

## ST-LC-0150 — 选择全部恢复成功的WDT

操作：Compute；需求：REQ-LC-0055, REQ-LC-0061, REQ-LC-0062, REQ-LC-0063, REQ-LC-0076

资源：RES-LC-0150

当前位置：[code.rdl L271](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.UseRestoredWatchDefinitionTable;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只将真实cFE critical table恢复的WDT放入工作WDT并设置wdtSource=CDS；该表随后成为验证和订阅的实际输入。
- 保留其MID/DataType/Operator/Offset/BitMask/ComparisonValue/age；不偷偷改用default WDT。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L174–179 LC9004

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–521 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L613–769 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L777–902 LC_CreateTaskCDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L195–196 LC9007.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L126–153 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L222–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L197–198 LC9007.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0151"></a>

## ST-LC-0151 — 选择全部恢复成功的ADT

操作：Compute；需求：REQ-LC-0055, REQ-LC-0076

资源：RES-LC-0151

当前位置：[code.rdl L273](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.UseRestoredActionDefinitionTable;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只将真实cFE critical table恢复的ADT放入工作ADT并设置adtSource=CDS、tableSource=CDS；保留DefaultState/RTS/FailCount/EventType/RPN原值。
- 成功恢复路径不把ART.CurrentState重设为ADT.DefaultState；保留恢复ART状态。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L174–179 LC9004

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–521 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L613–769 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L777–902 LC_CreateTaskCDS

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0152"></a>

## ST-LC-0152 — 判定复位模式是否保留CDS前态

操作：Compute；需求：REQ-LC-0056, REQ-LC-0057

资源：RES-LC-0152

当前位置：[code.rdl L275](code.rdl)

```spacerdl
Compute ResetApplicationStateUsesCDS InitContext ReqCapByFormTable FormulaTable.ResetApplicationStateUsesCDS;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：ResetApplicationStateUsesCDS 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当已确认LC_STATE_WHEN_CDS_RESTORED等于LC_STATE_FROM_CDS；其他合法Active/Passive/Disabled为FALSE。
- 非法/未配置值不能当作合法default；部署值待确认。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L180–180 LC9004.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–889 LC_CreateTaskCDS

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L105–127 LC_STATE_WHEN_CDS_RESTORED

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L181–181 LC9004.1.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0153"></a>

## ST-LC-0153 — 保留CDS恢复的复位前LC模式

操作：Compute；需求：REQ-LC-0056, REQ-LC-0057

资源：RES-LC-0153

当前位置：[code.rdl L278](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.RetainCriticalApplicationState;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅将selectedAppState=已恢复AppData.CurrentLCState，并保持该CurrentLCState不变；所有其他AppData/表成员保持。
- 只在成功五对象恢复且ResetApplicationStateUsesCDS=TRUE路径适用，不把FROM_CDS当持久LC模式枚举。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L180–180 LC9004.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–889 LC_CreateTaskCDS

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L105–127 LC_STATE_WHEN_CDS_RESTORED

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L181–181 LC9004.1.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0154"></a>

## ST-LC-0154 — 用平台DefaultResetState覆盖恢复模式

操作：Compute；需求：REQ-LC-0056, REQ-LC-0057

资源：RES-LC-0154

当前位置：[code.rdl L281](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.OverrideCriticalApplicationState;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅将AppData.CurrentLCState改为确认的LC_STATE_WHEN_CDS_RESTORED（ACTIVE/PASSIVE/DISABLED三者之一）；其他恢复数据不变。
- 不使用仓库默认FROM_CDS来猜当前部署选择；源码仅在编译配置不等于FROM_CDS时做此覆盖。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L180–180 LC9004.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–889 LC_CreateTaskCDS

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L105–127 LC_STATE_WHEN_CDS_RESTORED

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L181–181 LC9004.1.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0155"></a>

## ST-LC-0155 — 选择真实默认WDT和ADT返回数据

操作：Compute；需求：REQ-LC-0051, REQ-LC-0052, REQ-LC-0053, REQ-LC-0054, REQ-LC-0058, REQ-LC-0059, REQ-LC-0060, REQ-LC-0076

资源：RES-LC-0155

当前位置：[code.rdl L246](code.rdl), [code.rdl L287](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.UseDefaultDefinitionTables;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅在外部CFE_TBL_Load及GetAddress真实返回Success或允许INFO_UPDATED时，将LC_WDT_FILENAME和LC_ADT_FILENAME加载所得表放入工作WDT/ADT并设置各source=default、tableSource=default。
- 默认文件名来自LC_INTERNAL_CFGVAL，仓库默认/cf/lc_def_wdt.tbl、/cf/lc_def_adt.tbl仅证据。任一加载/地址失败置fatalStatus为真实错误，不能构造默认表成功。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L146–155 LC9000

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L187–216 LC_AppInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L991–1011 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L301–310 LC_ResetCounters

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L156–163 LC9001

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L994–997 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L164–172 LC9002

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L999–1000 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L173–173 LC9003

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L386–478 LC_TableInit

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L88–102 LC_SAVE_TO_CDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L182–182 LC9004.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–881 LC_CreateTaskCDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L183–186 LC9005

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L631–654 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L917–940 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L988–1134 LC_ValidateWDT

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L187–192 LC9006

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L684–706 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L956–987 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L494–728 LC_ValidateADT / LC_ValidateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0156"></a>

## ST-LC-0156 — 检查默认或恢复表是否实际可用

操作：Compute；需求：REQ-LC-0051, REQ-LC-0052, REQ-LC-0053, REQ-LC-0054, REQ-LC-0058, REQ-LC-0059, REQ-LC-0060

资源：RES-LC-0156

当前位置：[code.rdl L248](code.rdl), [code.rdl L284](code.rdl), [code.rdl L289](code.rdl)

```spacerdl
Compute InitializationTablesAvailable InitContext ReqCapByFormTable FormulaTable.InitializationDefinitionTablesAvailable;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：InitializationTablesAvailable 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当本路径两张实际表已取得且fatalStatus为CFE_SUCCESS或被规范为SUCCESS的INFO_UPDATED；FALSE不继续结果初始化或订阅，保留真实失败状态。
- 缺外部结果为pending，不当FALSE来制造受控失败证据。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L146–155 LC9000

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L187–216 LC_AppInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L991–1011 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L301–310 LC_ResetCounters

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L156–163 LC9001

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L994–997 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L164–172 LC9002

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L999–1000 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L173–173 LC9003

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L386–478 LC_TableInit

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L88–102 LC_SAVE_TO_CDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L182–182 LC9004.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–881 LC_CreateTaskCDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L183–186 LC9005

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L631–654 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L917–940 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L988–1134 LC_ValidateWDT

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L187–192 LC9006

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L684–706 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L956–987 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L494–728 LC_ValidateADT / LC_ValidateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0157"></a>

## ST-LC-0157 — 上电等价初始化所有WP结果和统计

操作：Compute；需求：REQ-LC-0052, REQ-LC-0054, REQ-LC-0058, REQ-LC-0074, REQ-LC-0076

资源：RES-LC-0157

当前位置：[code.rdl L251](code.rdl), [code.rdl L292](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.InitializeColdWatchResults;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 对全部工作WRT：WatchResult=LC_WATCH_STALE、CountdownToStale=0；EvaluationCount/FalseToTrueCount/ConsecutiveTrueCount/CumulativeTrueCount=0；两向LastTransition.Value、Seconds/Subseconds全部0。
- 仅改WRT，保持AppData/ART/WDT/ADT。与统计复位保留WatchResult/Countdown不同；不额外执行WP比较，不增加转换统计。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L156–163 LC9001

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L994–997 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L173–173 LC9003

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L386–478 LC_TableInit

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L88–102 LC_SAVE_TO_CDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L182–182 LC9004.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–881 LC_CreateTaskCDS

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0158"></a>

## ST-LC-0158 — 上电等价初始化所有AP结果和统计

操作：Compute；需求：REQ-LC-0053, REQ-LC-0054, REQ-LC-0058, REQ-LC-0074, REQ-LC-0076

资源：RES-LC-0158

当前位置：[code.rdl L253](code.rdl), [code.rdl L294](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.InitializeColdActionResults;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 对全部工作ART：ActionResult=LC_ACTION_STALE；CurrentState取当前真实工作ADT对应条目的DefaultState；PassiveAPCount和六项正式统计全0。
- 仅改ART，保持WRT/AppData/WDT/ADT；不是把所有AP默认置ACTIVE，不保留旧PERMOFF（除非ADT默认本身如此且合法）。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L164–172 LC9002

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L999–1000 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L173–173 LC9003

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L386–478 LC_TableInit

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L88–102 LC_SAVE_TO_CDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L182–182 LC9004.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–881 LC_CreateTaskCDS

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0159"></a>

## ST-LC-0159 — 上电等价初始化应用计数与HK位图

操作：Compute；需求：REQ-LC-0051, REQ-LC-0054, REQ-LC-0058, REQ-LC-0076

资源：RES-LC-0159

当前位置：[code.rdl L255](code.rdl), [code.rdl L296](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.InitializeColdHousekeepingState;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅将工作AppData六计数CmdCount/CmdErrCount/APSampleCount/MonitoredMsgCount/RTSExecCount/PassiveRTSExecCount清0，CurrentLCState=已确认LC_STATE_POWER_ON_RESET。
- 按原LC_AppInit的memset初始LC_OperData.HkPacket.Payload.WPResults/APResults清0；正式LC9000规定bitmapped初值0。当前WRT/ART实际STALE由上述两步建立，下次HK再打包相应STALE码，不能误认为0位图就是STALE。
- 保留当前工作表内容；默认POWER_ON=DISABLED只作为仓库默认不是部署承诺。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L146–155 LC9000

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L187–216 LC_AppInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L991–1011 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L301–310 LC_ResetCounters

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L173–173 LC9003

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L386–478 LC_TableInit

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L88–102 LC_SAVE_TO_CDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L182–182 LC9004.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–881 LC_CreateTaskCDS

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0160"></a>

## ST-LC-0160 — 提交选定初始化结果到原状态对象

操作：Set；需求：REQ-LC-0051, REQ-LC-0052, REQ-LC-0053, REQ-LC-0054, REQ-LC-0055, REQ-LC-0056, REQ-LC-0057, REQ-LC-0058, REQ-LC-0076

资源：RES-LC-0160

当前位置：[code.rdl L307](code.rdl)

```spacerdl
Set LCInitializedPersistentState InitContext;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：持久绑定：LCInitializedPersistentState。仅将 rules 指定的原 LC 内存成员从 InitContext 操作后工作快照写入；不是 cFE服务提交，不修改其他存储。

规则：

- 将确定路径中的工作AppData/WRT/ART，以及实际已取得WDT/ADT内容绑定至原AppData、WRTPtr、ARTPtr、WDTPtr、ADTPtr；cold路径只另清原HK位图。
- 只在InitializationTablesAvailable和真实初始化服务成功条件满足的路径提交，其他对象/阶段字段/effects不写原工程；既不注册表，也不实际Load/Restore/Subscribe。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L146–155 LC9000

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L187–216 LC_AppInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L991–1011 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L301–310 LC_ResetCounters

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L156–163 LC9001

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L994–997 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L164–172 LC9002

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L999–1000 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L173–173 LC9003

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L386–478 LC_TableInit

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L88–102 LC_SAVE_TO_CDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L174–179 LC9004

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–521 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L613–769 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L777–902 LC_CreateTaskCDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L180–180 LC9004.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–889 LC_CreateTaskCDS

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L105–127 LC_STATE_WHEN_CDS_RESTORED

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L181–181 LC9004.1.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L182–182 LC9004.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–881 LC_CreateTaskCDS

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0161"></a>

## ST-LC-0161 — 提供任何初始化的实际WDT/ADT验证输入

操作：Compute；需求：REQ-LC-0055, REQ-LC-0058, REQ-LC-0059, REQ-LC-0060

资源：RES-LC-0161

当前位置：[code.rdl L305](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.PrepareInitializationTableValidationInputs;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只设置validationInputs.WDT=本路径实际工作WDT、validationInputs.ADT=本路径实际工作ADT，以及initializationCause/tableSource。
- 每种初始化都保留正式LC9005/LC9006验证义务；具体验证计算复用FLOW-WP-WDT-VALIDATION及FLOW-ADT-VALIDATE，不把此准备步骤当验证完成。
- 源码默认Load依赖cFE的registered callback；恢复路径是否调用全部验证依赖外部cFE保证，不能仅看pure报告宣称强制回调已执行。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L183–186 LC9005

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L631–654 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L917–940 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L988–1134 LC_ValidateWDT

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L187–192 LC9006

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L684–706 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L956–987 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L494–728 LC_ValidateADT / LC_ValidateRPN

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L174–179 LC9004

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–521 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L613–769 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L777–902 LC_CreateTaskCDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L182–182 LC9004.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–881 LC_CreateTaskCDS

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0162"></a>

## ST-LC-0162 — 提供初始化成功后的实际订阅WDT

操作：Compute；需求：REQ-LC-0061, REQ-LC-0062, REQ-LC-0063, REQ-LC-0076

资源：RES-LC-0162

当前位置：[code.rdl L309](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.PrepareInitializationSubscriptionInput;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只设置subscriptionInput=当前已选工作WDT、subscriptionPipe=原CmdPipe、subscriptionCause=resetCause，保留wdtSource。
- 若ProcessorReset/LCAppReset且SaveCriticalData=YES并全部恢复成功必须用CDS WDT；若恢复无效采用整套cold初始化和实际default WDT。
- 只输出交接快照，随后FLOW-WATCH-SUBSCRIPTIONS构造独立消息订阅意图；不宣称实际SB订阅成功。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L195–196 LC9007.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L126–153 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L222–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L197–198 LC9007.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0163"></a>

## ST-LC-0163 — 保持初始化失败并禁止进入监测运行

操作：Compute；需求：REQ-LC-0051, REQ-LC-0052, REQ-LC-0053, REQ-LC-0054, REQ-LC-0055, REQ-LC-0058, REQ-LC-0059, REQ-LC-0060

资源：RES-LC-0163

当前位置：[code.rdl L258](code.rdl), [code.rdl L299](code.rdl)

```spacerdl
Compute InitContext InitContext ReqCapByFormTable FormulaTable.PreserveFatalInitializationStatus;
```

输入绑定：独立 cFE Power-On / ProcessorReset / LCAppReset 入口：resetCause，任务确认的 SaveCriticalData / powerOnState / resetState 配置符号，当前工作 AppData/WRT/ART/WDT/ADT，外部 cFE Table/CDS 服务结果和返回数据；restore flags、fatalStatus、tableSource、validationInputs、effects。未知服务结果保持未绑定，不能猜成成功或失败。Compute 仅按明确 rules 改当前成员。

输出绑定：前一操作写出的 InitContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只记录真实fatalStatus对应启动失败、Initialized=false和CFE_ES_RunStatus_APP_ERROR的结果描述；不把错误改为正常。
- 不提交伪造状态、不形成新的监测/订阅成功；LC原主循环按框架RunStatus退出属于接口待确认。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L146–155 LC9000

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L187–216 LC_AppInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L991–1011 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L301–310 LC_ResetCounters

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L156–163 LC9001

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L994–997 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L164–172 LC9002

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L999–1000 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L173–173 LC9003

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L386–478 LC_TableInit

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L88–102 LC_SAVE_TO_CDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L174–179 LC9004

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–521 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L613–769 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L777–902 LC_CreateTaskCDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L182–182 LC9004.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–881 LC_CreateTaskCDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L183–186 LC9005

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L631–654 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L917–940 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L988–1134 LC_ValidateWDT

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L187–192 LC9006

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L684–706 LC_CreateDefinitionTables

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L956–987 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L494–728 LC_ValidateADT / LC_ValidateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0164"></a>

## ST-LC-0164 — 初始化订阅重建的旧列表游标

操作：Compute；需求：REQ-LC-0061, REQ-LC-0062, REQ-LC-0063, REQ-LC-0075

资源：RES-LC-0164

当前位置：[code.rdl L994](code.rdl)

```spacerdl
Compute SubscriptionContext SubscriptionContext ReqCapByFormTable FormulaTable.BeginWatchSubscriptionRebuild;
```

输入绑定：独立初始化成功或 WDT 更新入口：实际被选中的 WDT（default 或全部恢复的 CDS WDT）、旧 MessageLinks 列表、CmdPipe、HashTable/MessageLinks/WatchPtLinks 工作副本、cursor 和已知服务返回值、effects。各 Compute 只改变列明成员；不得把订阅意图当作实际订阅成功。

输出绑定：前一操作写出的 SubscriptionContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅设置oldMessageCursor=0、watchCursor=0，保留实际已选WDT和oldMessageLinks/MessageIDsCount以及effects。
- WDT来源必须来自成功初始化/更新交接；SaveCriticalData成功恢复路径不得换成默认表。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L195–196 LC9007.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L126–153 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L222–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L197–198 LC9007.2

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0165"></a>

## ST-LC-0165 — 旧订阅取消列表的有限终止条件

操作：Compute；需求：REQ-LC-0061, REQ-LC-0075

资源：RES-LC-0165

当前位置：[code.rdl L996](code.rdl), [code.rdl L1003](code.rdl)

```spacerdl
Compute OldWatchSubscriptionsRemain SubscriptionContext ReqCapByFormTable FormulaTable.HasMoreOldWatchSubscriptions;
```

输入绑定：独立初始化成功或 WDT 更新入口：实际被选中的 WDT（default 或全部恢复的 CDS WDT）、旧 MessageLinks 列表、CmdPipe、HashTable/MessageLinks/WatchPtLinks 工作副本、cursor 和已知服务返回值、effects。各 Compute 只改变列明成员；不得把订阅意图当作实际订阅成功。

输出绑定：OldWatchSubscriptionsRemain 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当oldMessageCursor<原旧MessageIDsCount；FALSE结束取消请求描述扫描。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0166"></a>

## ST-LC-0166 — 形成一个旧MID取消订阅请求

操作：Compute；需求：REQ-LC-0061, REQ-LC-0075

资源：RES-LC-0166

当前位置：[code.rdl L999](code.rdl)

```spacerdl
Compute SubscriptionContext SubscriptionContext ReqCapByFormTable FormulaTable.PrepareOldWatchUnsubscribeRequest;
```

输入绑定：独立初始化成功或 WDT 更新入口：实际被选中的 WDT（default 或全部恢复的 CDS WDT）、旧 MessageLinks 列表、CmdPipe、HashTable/MessageLinks/WatchPtLinks 工作副本、cursor 和已知服务返回值、effects。各 Compute 只改变列明成员；不得把订阅意图当作实际订阅成功。

输出绑定：前一操作写出的 SubscriptionContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只向effects追加CFE_SB_Unsubscribe(oldMessageLinks[oldMessageCursor].MessageID,CmdPipe)描述，使用实际旧列表MID。
- 原代码取消失败发LC_UNSUB_WP_ERR_EID后继续；这里不猜测服务结果，实际失败事件由真实结果记录另处理。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0167"></a>

## ST-LC-0167 — 推进旧订阅游标

操作：Compute；需求：REQ-LC-0061, REQ-LC-0075

资源：RES-LC-0167

当前位置：[code.rdl L1001](code.rdl)

```spacerdl
Compute SubscriptionContext SubscriptionContext ReqCapByFormTable FormulaTable.AdvanceOldWatchSubscriptionCursor;
```

输入绑定：独立初始化成功或 WDT 更新入口：实际被选中的 WDT（default 或全部恢复的 CDS WDT）、旧 MessageLinks 列表、CmdPipe、HashTable/MessageLinks/WatchPtLinks 工作副本、cursor 和已知服务返回值、effects。各 Compute 只改变列明成员；不得把订阅意图当作实际订阅成功。

输出绑定：前一操作写出的 SubscriptionContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅oldMessageCursor加一，保持effects及当前实际WDT；重算OldWatchSubscriptionsRemain。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0168"></a>

## ST-LC-0168 — 清空工作哈希和MID/WP链接统计

操作：Compute；需求：REQ-LC-0061, REQ-LC-0062, REQ-LC-0063, REQ-LC-0075

资源：RES-LC-0168

当前位置：[code.rdl L1006](code.rdl)

```spacerdl
Compute SubscriptionContext SubscriptionContext ReqCapByFormTable FormulaTable.ClearWatchHashWorkingStructures;
```

输入绑定：独立初始化成功或 WDT 更新入口：实际被选中的 WDT（default 或全部恢复的 CDS WDT）、旧 MessageLinks 列表、CmdPipe、HashTable/MessageLinks/WatchPtLinks 工作副本、cursor 和已知服务返回值、effects。各 Compute 只改变列明成员；不得把订阅意图当作实际订阅成功。

输出绑定：前一操作写出的 SubscriptionContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只把工作HashTable、MessageLinks、WatchPtLinks清零，MessageIDsCount=0、WatchpointCount=0、LastMessageID=CFE_SB_INVALID_MSG_ID，watchCursor=0。
- 不清WDT、WRT或旧取消请求effects；旧列表已经保留在单独oldMessageLinks输入快照，不被本清空覆盖。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L195–196 LC9007.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L126–153 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L222–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L197–198 LC9007.2

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0169"></a>

## ST-LC-0169 — 检查WDT订阅重建游标

操作：Compute；需求：REQ-LC-0061, REQ-LC-0062, REQ-LC-0063, REQ-LC-0075

资源：RES-LC-0169

当前位置：[code.rdl L1008](code.rdl), [code.rdl L1027](code.rdl)

```spacerdl
Compute WatchDefinitionSubscriptionsRemain SubscriptionContext ReqCapByFormTable FormulaTable.HasMoreWatchDefinitionSubscriptions;
```

输入绑定：独立初始化成功或 WDT 更新入口：实际被选中的 WDT（default 或全部恢复的 CDS WDT）、旧 MessageLinks 列表、CmdPipe、HashTable/MessageLinks/WatchPtLinks 工作副本、cursor 和已知服务返回值、effects。各 Compute 只改变列明成员；不得把订阅意图当作实际订阅成功。

输出绑定：WatchDefinitionSubscriptionsRemain 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当watchCursor<LC_MAX_WATCHPOINTS；FALSE终止有限扫描。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L195–196 LC9007.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L126–153 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L222–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L197–198 LC9007.2

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0170"></a>

## ST-LC-0170 — 过滤未使用WDT条目

操作：Compute；需求：REQ-LC-0061, REQ-LC-0062, REQ-LC-0063, REQ-LC-0075

资源：RES-LC-0170

当前位置：[code.rdl L1011](code.rdl)

```spacerdl
Compute WatchSubscriptionEntryUsed SubscriptionContext ReqCapByFormTable FormulaTable.WatchSubscriptionEntryIsUsed;
```

输入绑定：独立初始化成功或 WDT 更新入口：实际被选中的 WDT（default 或全部恢复的 CDS WDT）、旧 MessageLinks 列表、CmdPipe、HashTable/MessageLinks/WatchPtLinks 工作副本、cursor 和已知服务返回值、effects。各 Compute 只改变列明成员；不得把订阅意图当作实际订阅成功。

输出绑定：WatchSubscriptionEntryUsed 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当当前WDT[watchCursor].DataType不是LC_DATA_WATCH_NOT_USED；FALSE只推进游标，不创建链接或订阅意图。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L195–196 LC9007.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L126–153 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L222–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L197–198 LC9007.2

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0171"></a>

## ST-LC-0171 — 检查当前WDT MID是否需要新订阅

操作：Compute；需求：REQ-LC-0061, REQ-LC-0062, REQ-LC-0063, REQ-LC-0075

资源：RES-LC-0171

当前位置：[code.rdl L1014](code.rdl)

```spacerdl
Compute WatchSubscriptionMIDNew SubscriptionContext ReqCapByFormTable FormulaTable.WatchSubscriptionMIDIsNew;
```

输入绑定：独立初始化成功或 WDT 更新入口：实际被选中的 WDT（default 或全部恢复的 CDS WDT）、旧 MessageLinks 列表、CmdPipe、HashTable/MessageLinks/WatchPtLinks 工作副本、cursor 和已知服务返回值、effects。各 Compute 只改变列明成员；不得把订阅意图当作实际订阅成功。

输出绑定：WatchSubscriptionMIDNew 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- 对工作MessageLinks按实际CFE_SB_MsgId_Equal语义比较当前MID；TRUE当未出现，FALSE当已建该MID链。
- hash=MessageID数值 & LC_HASH_TABLE_MASK，256个桶/0x00FF为源码固定值；相同哈希不同MID不能合并成同一个消息。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L195–196 LC9007.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L126–153 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L222–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L197–198 LC9007.2

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0172"></a>

## ST-LC-0172 — 为首次引用MID建立工作链

操作：Compute；需求：REQ-LC-0061, REQ-LC-0062, REQ-LC-0063, REQ-LC-0075

资源：RES-LC-0172

当前位置：[code.rdl L1017](code.rdl)

```spacerdl
Compute SubscriptionContext SubscriptionContext ReqCapByFormTable FormulaTable.AddUniqueWatchMessageLink;
```

输入绑定：独立初始化成功或 WDT 更新入口：实际被选中的 WDT（default 或全部恢复的 CDS WDT）、旧 MessageLinks 列表、CmdPipe、HashTable/MessageLinks/WatchPtLinks 工作副本、cursor 和已知服务返回值、effects。各 Compute 只改变列明成员；不得把订阅意图当作实际订阅成功。

输出绑定：前一操作写出的 SubscriptionContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 当前MID新出现时仅创建一个MessageLinks节点，加入其hash冲突链并MessageIDsCount加一；保存currentMessageLink。
- 原同MID重复不经此步；不在本步提交订阅服务。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L195–196 LC9007.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L126–153 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L222–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L197–198 LC9007.2

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0173"></a>

## ST-LC-0173 — 形成一个新MID订阅请求

操作：Compute；需求：REQ-LC-0061, REQ-LC-0062, REQ-LC-0063, REQ-LC-0075

资源：RES-LC-0173

当前位置：[code.rdl L1019](code.rdl)

```spacerdl
Compute SubscriptionContext SubscriptionContext ReqCapByFormTable FormulaTable.PrepareUniqueWatchSubscribeRequest;
```

输入绑定：独立初始化成功或 WDT 更新入口：实际被选中的 WDT（default 或全部恢复的 CDS WDT）、旧 MessageLinks 列表、CmdPipe、HashTable/MessageLinks/WatchPtLinks 工作副本、cursor 和已知服务返回值、effects。各 Compute 只改变列明成员；不得把订阅意图当作实际订阅成功。

输出绑定：前一操作写出的 SubscriptionContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅向effects追加CFE_SB_Subscribe(当前MID,CmdPipe)描述；同MID只有第一次引用追加，多个WP只挂同一MID链。
- 服务调用失败原代码发LC_SUB_WP_ERR_EID并继续建立WP链接；描述不等于真实成功，也不补造ACK/retry。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L195–196 LC9007.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L126–153 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L222–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L197–198 LC9007.2

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0174"></a>

## ST-LC-0174 — 把当前WP索引挂到对应MID链

操作：Compute；需求：REQ-LC-0061, REQ-LC-0062, REQ-LC-0063, REQ-LC-0075

资源：RES-LC-0174

当前位置：[code.rdl L1022](code.rdl)

```spacerdl
Compute SubscriptionContext SubscriptionContext ReqCapByFormTable FormulaTable.AddWatchpointToMessageLink;
```

输入绑定：独立初始化成功或 WDT 更新入口：实际被选中的 WDT（default 或全部恢复的 CDS WDT）、旧 MessageLinks 列表、CmdPipe、HashTable/MessageLinks/WatchPtLinks 工作副本、cursor 和已知服务返回值、effects。各 Compute 只改变列明成员；不得把订阅意图当作实际订阅成功。

输出绑定：前一操作写出的 SubscriptionContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅创建一个WatchPtLinks节点，WatchIndex=watchCursor，挂到已存在/新创建的currentMID消息WP列表，WatchpointCount加一，LastMessageID=当前MID。
- 对已有MID路径先根据MID查得currentMessageLink再挂接；不复用未定义指针，不修改WDT/WRT或任何AP状态。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L195–196 LC9007.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L126–153 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L222–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L197–198 LC9007.2

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0175"></a>

## ST-LC-0175 — 推进WDT订阅重建游标

操作：Compute；需求：REQ-LC-0061, REQ-LC-0062, REQ-LC-0063, REQ-LC-0075

资源：RES-LC-0175

当前位置：[code.rdl L1025](code.rdl)

```spacerdl
Compute SubscriptionContext SubscriptionContext ReqCapByFormTable FormulaTable.AdvanceWatchSubscriptionCursor;
```

输入绑定：独立初始化成功或 WDT 更新入口：实际被选中的 WDT（default 或全部恢复的 CDS WDT）、旧 MessageLinks 列表、CmdPipe、HashTable/MessageLinks/WatchPtLinks 工作副本、cursor 和已知服务返回值、effects。各 Compute 只改变列明成员；不得把订阅意图当作实际订阅成功。

输出绑定：前一操作写出的 SubscriptionContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅watchCursor加一，保持工作hash/链接/effects；每圈必须重算WatchDefinitionSubscriptionsRemain。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L195–196 LC9007.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L126–153 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L222–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L197–198 LC9007.2

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0176"></a>

## ST-LC-0176 — 提交工作哈希和MID/WP链接表

操作：Set；需求：REQ-LC-0061, REQ-LC-0062, REQ-LC-0063, REQ-LC-0075

资源：RES-LC-0176

当前位置：[code.rdl L1030](code.rdl)

```spacerdl
Set LCWatchSubscriptionIndex SubscriptionContext;
```

输入绑定：独立初始化成功或 WDT 更新入口：实际被选中的 WDT（default 或全部恢复的 CDS WDT）、旧 MessageLinks 列表、CmdPipe、HashTable/MessageLinks/WatchPtLinks 工作副本、cursor 和已知服务返回值、effects。各 Compute 只改变列明成员；不得把订阅意图当作实际订阅成功。

输出绑定：持久绑定：LCWatchSubscriptionIndex。仅将 rules 指定的原 LC 内存成员从 SubscriptionContext 操作后工作快照写入；不是 cFE服务提交，不修改其他存储。

规则：

- 只将工作HashTable/MessageLinks/WatchPtLinks、MessageIDsCount、WatchpointCount写回LC_OperData对应存储；不把effects当真实SB状态。
- 订阅/取消失败是否发生必须来自真实外部服务结果；源码即使其失败仍建立索引，不能称索引存在即订阅成功。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L195–196 LC9007.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L126–153 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L222–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L197–198 LC9007.2

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0177"></a>

## ST-LC-0177 — 记录真实订阅或取消失败事件而不阻断重建

操作：Compute；需求：REQ-LC-0061, REQ-LC-0062, REQ-LC-0063, REQ-LC-0075

资源：RES-LC-0177

当前位置：[code.rdl L988](code.rdl)

```spacerdl
Compute SubscriptionContext SubscriptionContext ReqCapByFormTable FormulaTable.RecordWatchSubscriptionServiceFailure;
```

输入绑定：独立初始化成功或 WDT 更新入口：实际被选中的 WDT（default 或全部恢复的 CDS WDT）、旧 MessageLinks 列表、CmdPipe、HashTable/MessageLinks/WatchPtLinks 工作副本、cursor 和已知服务返回值、effects。各 Compute 只改变列明成员；不得把订阅意图当作实际订阅成功。

输出绑定：前一操作写出的 SubscriptionContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅消耗明确绑定的真实外部SB返回：成功保持plannedEvents；取消失败追加LC_UNSUB_WP_ERR_EID ERROR，新订阅失败追加LC_SUB_WP_ERR_EID ERROR，含MID和真实RC。
- 失败不回滚工作hash/链接，不擅自把原代码改为启动失败；该服务结果入口本身pending。
- 本次新增事件时输出LCEvent0177Ready=true；无新增事件false。NaN/类型错误、首错资格、EDS/SB实际失败分别依原规则，不因写出SendData而扩大触发条件。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L193–194 LC9007

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L486–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L91–157 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L165–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L195–196 LC9007.1

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–491 LC_TableInit

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L126–153 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L222–233 LC_AddWatchpoint

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L197–198 LC9007.2

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0178"></a>

## ST-LC-0178 — 判定维护返回是否为WDT更新

操作：Compute；需求：REQ-LC-0075

资源：RES-LC-0178

当前位置：[code.rdl L970](code.rdl)

```spacerdl
Compute MaintenanceWDTUpdated MaintenanceContext ReqCapByFormTable FormulaTable.MaintenanceWDTWasUpdated;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：MaintenanceWDTUpdated 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当外部真实CFE_TBL_GetAddress(WDT)返回CFE_TBL_INFO_UPDATED；CFE_SUCCESS为FALSE；其他错误保留fatalStatus，不能当合法未更新。

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0179"></a>

## ST-LC-0179 — 新WDT替换后重置旧WRT

操作：Compute；需求：REQ-LC-0074, REQ-LC-0075

资源：RES-LC-0179

当前位置：[code.rdl L973](code.rdl)

```spacerdl
Compute MaintenanceContext MaintenanceContext ReqCapByFormTable FormulaTable.ResetWatchResultsAfterTableReplacement;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：前一操作写出的 MaintenanceContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只将工作WRT全部WatchResult置STALE、CountdownToStale=0、统计及两向记录全0，使用真实新WDT但不尝试在本步比较数据。
- 设置subscriptionInput=newWDT以及旧MID列表，用于FLOW-WATCH-SUBSCRIPTIONS；其他ART/AppData不变。

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0180"></a>

## ST-LC-0180 — 判定维护返回是否为ADT更新

操作：Compute；需求：REQ-LC-0075

资源：RES-LC-0180

当前位置：[code.rdl L976](code.rdl)

```spacerdl
Compute MaintenanceADTUpdated MaintenanceContext ReqCapByFormTable FormulaTable.MaintenanceADTWasUpdated;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：MaintenanceADTUpdated 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当外部真实CFE_TBL_GetAddress(ADT)返回CFE_TBL_INFO_UPDATED；CFE_SUCCESS为FALSE；其他错误保留fatalStatus。

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0181"></a>

## ST-LC-0181 — 新ADT替换后重置旧ART

操作：Compute；需求：REQ-LC-0074, REQ-LC-0075

资源：RES-LC-0181

当前位置：[code.rdl L979](code.rdl)

```spacerdl
Compute MaintenanceContext MaintenanceContext ReqCapByFormTable FormulaTable.ResetActionResultsAfterTableReplacement;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：前一操作写出的 MaintenanceContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只将工作ART全部ActionResult置STALE、CurrentState取真实新ADT.DefaultState；PassiveAPCount及六项统计全0。
- 不保留旧PERMOFF，不更改AppData/WRT；这与统计命令保留状态/结果不同。

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0182"></a>

## ST-LC-0182 — 提交实际表更新后的结果初始化

操作：Set；需求：REQ-LC-0074, REQ-LC-0075

资源：RES-LC-0182

当前位置：[code.rdl L982](code.rdl)

```spacerdl
Set LCTableReplacementResults MaintenanceContext;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：持久绑定：LCTableReplacementResults。仅将 rules 指定的原 LC 内存成员从 MaintenanceContext 操作后工作快照写入；不是 cFE服务提交，不修改其他存储。

规则：

- WDT真实更新时仅写WRT；ADT真实更新时仅写ART；依赖真实newWDT/newADT绑定。未更新的结果表保持不变。
- 实际ReleaseAddress/Manage/GetAddress及订阅重建服务不是此Set的动作，待独立接口绑定。

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L43–108 LC_ManageTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L255–259 LC_SendHkCmd

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L111–117 LC_AppMain

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0183"></a>

## ST-LC-0183 — 检查CDS是否仍处活动

操作：Compute；需求：REQ-LC-0076

资源：RES-LC-0183

当前位置：[code.rdl L118](code.rdl)

```spacerdl
Compute MaintenanceCDSActive MaintenanceContext ReqCapByFormTable FormulaTable.MaintenanceCDSIsActive;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：MaintenanceCDSActive 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当已绑定LC_OperData.HaveActiveCDS=true且前序表维护无fatal错误；FALSE不做任何CDS保存请求。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0184"></a>

## ST-LC-0184 — 形成WRT CDS保存请求

操作：Compute；需求：REQ-LC-0076

资源：RES-LC-0184

当前位置：[code.rdl L121](code.rdl)

```spacerdl
Compute MaintenanceContext MaintenanceContext ReqCapByFormTable FormulaTable.PrepareWatchResultCDSSave;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：前一操作写出的 MaintenanceContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只向effects追加CFE_ES_CopyToCDS(WRTDataCDSHandle,工作WRT)描述，保留AppData/ART；先WRT再ART再APP。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0185"></a>

## ST-LC-0185 — 核对真实WRT保存返回

操作：Compute；需求：REQ-LC-0076

资源：RES-LC-0185

当前位置：[code.rdl L123](code.rdl)

```spacerdl
Compute WatchResultCDSSaveSucceeded MaintenanceContext ReqCapByFormTable FormulaTable.WatchResultCDSSaveSucceeded;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：WatchResultCDSSaveSucceeded 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当真实外部WRT CopyToCDS返回CFE_SUCCESS，FALSE为真实错误；无返回保持pending，不能猜测。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0186"></a>

## ST-LC-0186 — 形成ART CDS保存请求

操作：Compute；需求：REQ-LC-0076

资源：RES-LC-0186

当前位置：[code.rdl L126](code.rdl)

```spacerdl
Compute MaintenanceContext MaintenanceContext ReqCapByFormTable FormulaTable.PrepareActionResultCDSSave;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：前一操作写出的 MaintenanceContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅在WRT真实保存成功路径向effects追加CFE_ES_CopyToCDS(ARTDataCDSHandle,工作ART)描述；其他状态保持。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0187"></a>

## ST-LC-0187 — 核对真实ART保存返回

操作：Compute；需求：REQ-LC-0076

资源：RES-LC-0187

当前位置：[code.rdl L128](code.rdl)

```spacerdl
Compute ActionResultCDSSaveSucceeded MaintenanceContext ReqCapByFormTable FormulaTable.ActionResultCDSSaveSucceeded;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：ActionResultCDSSaveSucceeded 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当真实外部ART CopyToCDS返回CFE_SUCCESS；FALSE停止APP保存阶段。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0188"></a>

## ST-LC-0188 — 在保存APP之前设置CDS已保存标记

操作：Compute；需求：REQ-LC-0076

资源：RES-LC-0188

当前位置：[code.rdl L131](code.rdl)

```spacerdl
Compute MaintenanceContext MaintenanceContext ReqCapByFormTable FormulaTable.SetCriticalDataSavedMarker;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：前一操作写出的 MaintenanceContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅将工作AppData.CDSSavedOnExit=LC_CDS_SAVED；原代码在ART保存成功后、APP保存调用之前设置，即使后续APP复制失败该内存标记也已改变。
- 不据标记断言APP持久保存成功。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0189"></a>

## ST-LC-0189 — 提交原APP保存标记

操作：Set；需求：REQ-LC-0076

资源：RES-LC-0189

当前位置：[code.rdl L133](code.rdl)

```spacerdl
Set LCCriticalDataSavedMarker MaintenanceContext;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：持久绑定：LCCriticalDataSavedMarker。仅将 rules 指定的原 LC 内存成员从 MaintenanceContext 操作后工作快照写入；不是 cFE服务提交，不修改其他存储。

规则：

- 仅将工作AppData.CDSSavedOnExit写回原LC_AppData对应成员；不写其他计数/模式，不执行CopyToCDS。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0190"></a>

## ST-LC-0190 — 形成APP CDS保存请求

操作：Compute；需求：REQ-LC-0076

资源：RES-LC-0190

当前位置：[code.rdl L135](code.rdl)

```spacerdl
Compute MaintenanceContext MaintenanceContext ReqCapByFormTable FormulaTable.PrepareApplicationCDSSave;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：前一操作写出的 MaintenanceContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 仅在markerCommit后向effects追加CFE_ES_CopyToCDS(AppDataCDSHandle,工作AppData)描述，包含已设置CDSSavedOnExit标记。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0191"></a>

## ST-LC-0191 — 核对真实APP保存返回

操作：Compute；需求：REQ-LC-0076

资源：RES-LC-0191

当前位置：[code.rdl L137](code.rdl)

```spacerdl
Compute ApplicationCDSSaveSucceeded MaintenanceContext ReqCapByFormTable FormulaTable.ApplicationCDSSaveSucceeded;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：ApplicationCDSSaveSucceeded 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当真实外部APP CopyToCDS返回CFE_SUCCESS；FALSE为真实错误，不额外判断WDT/ADT本次保存（定义表CDS归cFE Table Services）。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0192"></a>

## ST-LC-0192 — 保存失败时禁用后续LC CDS使用

操作：Compute；需求：REQ-LC-0076

资源：RES-LC-0192

当前位置：[code.rdl L141](code.rdl), [code.rdl L147](code.rdl), [code.rdl L153](code.rdl)

```spacerdl
Compute MaintenanceContext MaintenanceContext ReqCapByFormTable FormulaTable.DisableCDSAfterSaveFailure;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：前一操作写出的 MaintenanceContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 只将HaveActiveCDS工作值=false，按当前真实失败阶段形成LC_WRT_NO_SAVE_ERR_EID / LC_ART_NO_SAVE_ERR_EID / LC_APP_NO_SAVE_START_ERR_EID ERROR事件描述。
- 原LC_PerformMaintenance在保存失败后继续应用而非fatal；不回滚已保存前几个对象，不虚构跨三对象事务原子性。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0193"></a>

## ST-LC-0193 — 提交CDS活动禁用标志

操作：Set；需求：REQ-LC-0076

资源：RES-LC-0193

当前位置：[code.rdl L143](code.rdl), [code.rdl L149](code.rdl), [code.rdl L155](code.rdl)

```spacerdl
Set LCHaveActiveCDS MaintenanceContext;
```

输入绑定：有效 HK 发送后或原主循环 ReceiveBuffer 超时维护入口：当前 WDT/ADT/WRT/ART/AppData，HaveActiveCDS，外部 TBL Manage/GetAddress 与 CDS CopyToCDS 的真实结果、effects。每一步只读自己的服务结果，不虚构 cFE 返回。

输出绑定：持久绑定：LCHaveActiveCDS。仅将 rules 指定的原 LC 内存成员从 MaintenanceContext 操作后工作快照写入；不是 cFE服务提交，不修改其他存储。

规则：

- 仅把工作HaveActiveCDS=false写回LC_OperData.HaveActiveCDS；保留TableResults/AppData/表，不终止正常应用。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–478 LC_TableInit

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0194"></a>

## ST-LC-0194 — 核定消息分发的编译分支

操作：Compute；需求：REQ-LC-0078, REQ-LC-0080

资源：RES-LC-0194

当前位置：[code.rdl L330](code.rdl)

```spacerdl
Compute RoutingBuildUsesEDS RouteContext ReqCapByFormTable FormulaTable.RoutingBuildUsesEDS;
```

输入绑定：独立已收到消息入口：原消息 MID/FcnCode/长度及 CFE_EDS_ENABLED 编译配置；ordinary 和 EDS 独立分支、route、dispatchStatus 与 effects。EDS外部字典/分发结果未提供则保持待确认；不创造周期。

输出绑定：RoutingBuildUsesEDS 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- TRUE当本任务实际构建CFE_EDS_ENABLED，FALSE为普通lc_dispatch.c；仓库存在两个源分支不表示同一实例同时运行。
- 构建配置未确认则输入待确认，不默认普通分支已部署。

[evidence/LC/CMakeLists.txt](<evidence/LC/CMakeLists.txt>)  L16–33 APP_SRC_FILES

[evidence/LC/fsw/src/lc_eds_dispatch.c](<evidence/LC/fsw/src/lc_eds_dispatch.c>)  L42–106 LC_TC_DISPATCH_TABLE / LC_AppPipe

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L314–362 LC_AppPipe

[evidence/LC/docs/dox_src/cfs_lc.dox](<evidence/LC/docs/dox_src/cfs_lc.dox>)  L125–139 Design Overview

[evidence/LC/docs/dox_src/cfs_lc.dox](<evidence/LC/docs/dox_src/cfs_lc.dox>)  L644–652 scheduler FAQ

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L91–126 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0195"></a>

## ST-LC-0195 — 普通分支保留四类独立消息入口

操作：Compute；需求：REQ-LC-0078, REQ-LC-0080

资源：RES-LC-0195

当前位置：[code.rdl L336](code.rdl)

```spacerdl
Compute RouteContext RouteContext ReqCapByFormTable FormulaTable.ClassifyOrdinaryLCMessageRoute;
```

输入绑定：独立已收到消息入口：原消息 MID/FcnCode/长度及 CFE_EDS_ENABLED 编译配置；ordinary 和 EDS 独立分支、route、dispatchStatus 与 effects。EDS外部字典/分发结果未提供则保持待确认；不创造周期。

输出绑定：前一操作写出的 RouteContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- 按照原LC_AppPipe次序：MID=LC_SAMPLE_AP_MID路由SampleAP；MID=LC_SEND_HK_MID路由HK；MID=LC_CMD_MID路由地面命令；其他MID交LC_CheckMsgForWPs。
- 只改route/nextEntry描述，并把实际原message作为对应入口输入交接；不执行下游算法、不增加任何计数/年龄，不合成WP+AP固定周期。

[evidence/LC/CMakeLists.txt](<evidence/LC/CMakeLists.txt>)  L16–33 APP_SRC_FILES

[evidence/LC/fsw/src/lc_eds_dispatch.c](<evidence/LC/fsw/src/lc_eds_dispatch.c>)  L42–106 LC_TC_DISPATCH_TABLE / LC_AppPipe

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L314–362 LC_AppPipe

[evidence/LC/docs/dox_src/cfs_lc.dox](<evidence/LC/docs/dox_src/cfs_lc.dox>)  L125–139 Design Overview

[evidence/LC/docs/dox_src/cfs_lc.dox](<evidence/LC/docs/dox_src/cfs_lc.dox>)  L644–652 scheduler FAQ

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L91–126 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0196"></a>

## ST-LC-0196 — 记录EDS表的真实路由集合和失败行为

操作：Compute；需求：REQ-LC-0078, REQ-LC-0080

资源：RES-LC-0196

当前位置：[code.rdl L333](code.rdl)

```spacerdl
Compute RouteContext RouteContext ReqCapByFormTable FormulaTable.ClassifyEDSLCMessageRoute;
```

输入绑定：独立已收到消息入口：原消息 MID/FcnCode/长度及 CFE_EDS_ENABLED 编译配置；ordinary 和 EDS 独立分支、route、dispatchStatus 与 effects。EDS外部字典/分发结果未提供则保持待确认；不创造周期。

输出绑定：前一操作写出的 RouteContext 为本步输入；本步将新工作快照赋回同一平坦符号。这里只修改 rules 明确列出的成员，其余成员和值完整保持，不隐含全局服务调用。

规则：

- EDS LC_TC_DISPATCH_TABLE只提供CMD七个地面handler和SEND_HK handler，未提供SampleAP/WP监测handler；仅记录其表定义，实际EdsDispatch调用结果必须外部绑定。
- dispatchStatus为真实非CFE_SUCCESS时工作CmdErrCount加一；UNKNOWN_MSG_ID用LC_CC_ERR_EID、WRONG_MSG_LENGTH用LC_CMD_LEN_ERR_EID、其他用LC_CC_ERR_EID错误描述；成功则route为真实选中handler。
- 不凭普通分支为EDS补造SampleAP或WP handler，不把未绑定dispatcher状态当成功；并不实际发送EVS。
- 本次新增事件时输出LCEvent0196Ready=true；无新增事件false。NaN/类型错误、首错资格、EDS/SB实际失败分别依原规则，不因写出SendData而扩大触发条件。

[evidence/LC/CMakeLists.txt](<evidence/LC/CMakeLists.txt>)  L16–33 APP_SRC_FILES

[evidence/LC/fsw/src/lc_eds_dispatch.c](<evidence/LC/fsw/src/lc_eds_dispatch.c>)  L42–106 LC_TC_DISPATCH_TABLE / LC_AppPipe

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L314–362 LC_AppPipe

[evidence/LC/docs/dox_src/cfs_lc.dox](<evidence/LC/docs/dox_src/cfs_lc.dox>)  L125–139 Design Overview

[evidence/LC/docs/dox_src/cfs_lc.dox](<evidence/LC/docs/dox_src/cfs_lc.dox>)  L644–652 scheduler FAQ

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L91–126 LC_AppMain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0197"></a>

## ST-LC-0197 — 核验WP容量的上界、打包粒度和表尺寸

操作：Compute；需求：REQ-LC-0082

资源：RES-LC-0197

当前位置：[code.rdl L435](code.rdl)

```spacerdl
Compute WatchCapacityContractSatisfied CapacityContext ReqCapByFormTable FormulaTable.ValidateConfiguredWatchCapacity;
```

输入绑定：只读任务配置检查入口：实际确认的 LC_MAX_WATCHPOINTS、LC_MAX_ACTIONPOINTS、sizeof(WDTEntry/ADTEntry)、CFE_PLATFORM_TBL_MAX_SNGL_TABLE_SIZE；仓库默认 176 仅作为默认值证据，不等于部署值。未绑定部署字段不能推成检查通过。

输出绑定：WatchCapacityContractSatisfied 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- 要求实际LC_MAX_WATCHPOINTS<=65520，且是4倍数；实际WDT size=LC_MAX_WATCHPOINTS*sizeof(LC_WDTEntry_t)<=实际CFE_PLATFORM_TBL_MAX_SNGL_TABLE_SIZE。
- 仓库默认176满足数字粒度但sizeof和cFE表上限依赖任务ABI/配置；任一未绑定时结果不得标为部署验证通过。
- 这是源码配置文档约束检查，不声称LC运行时代码本来有这些完整拒绝门控。

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L86–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L140–253 LC_SendHkCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0198"></a>

## ST-LC-0198 — 核验AP容量的上界、打包粒度和表尺寸

操作：Compute；需求：REQ-LC-0082

资源：RES-LC-0198

当前位置：[code.rdl L437](code.rdl)

```spacerdl
Compute ActionCapacityContractSatisfied CapacityContext ReqCapByFormTable FormulaTable.ValidateConfiguredActionCapacity;
```

输入绑定：只读任务配置检查入口：实际确认的 LC_MAX_WATCHPOINTS、LC_MAX_ACTIONPOINTS、sizeof(WDTEntry/ADTEntry)、CFE_PLATFORM_TBL_MAX_SNGL_TABLE_SIZE；仓库默认 176 仅作为默认值证据，不等于部署值。未绑定部署字段不能推成检查通过。

输出绑定：ActionCapacityContractSatisfied 是本步计算的派生值，绑定 rules 的具体结果；不改变输入工作快照。

规则：

- 要求实际LC_MAX_ACTIONPOINTS<=65535，且是2倍数；实际ADT size=LC_MAX_ACTIONPOINTS*sizeof(LC_ADTEntry_t)<=实际CFE_PLATFORM_TBL_MAX_SNGL_TABLE_SIZE。
- 不得把默认176当部署参数；本检查是配置契约义务，不替LC源码补造运行期纠错/索引剪裁。

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L86–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L140–253 LC_SendHkCmd

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0200"></a>

## ST-LC-0200 — 读取独立监测入口快照

操作：Set；需求：REQ-LC-0006, REQ-LC-0007, REQ-LC-0008, REQ-LC-0009, REQ-LC-0010, REQ-LC-0011, REQ-LC-0012, REQ-LC-0013, REQ-LC-0014, REQ-LC-0016, REQ-LC-0065, REQ-LC-0066, REQ-LC-0067, REQ-LC-0079

资源：RES-LC-0200

当前位置：[code.rdl L1112](code.rdl)

```spacerdl
Set WMonitorWorking WMonitorEntry;
```

输入绑定：WMonitorEntry来自被LC_AppPipe分类为监测消息的真实LCMessage、LC_AppData及WRT/ADT/WDT活动表、RuntimeContext hash链、LCConfig、当前cFE时刻及明确目标算术ABI观察值。

输出绑定：M是本次监测工作快照；仅复制已有输入，不创建周期、不接入采样入口。

规则：

- 拷贝入口message、tables、state、runtime、config和已观测时间/ABI；建立本次empty eventPlan与orderedSteps，但不改变持久WRT/ART。
- 真实软件总线接收与消息入口绑定尚待确认；不把Set当成CFE_SB_ReceiveBuffer。

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L314–361 LC_AppPipe

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L270–454 LC_CheckMsgForWPs / LC_ProcessWP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0201"></a>

## ST-LC-0201 — 实现监测入口应用状态门

操作：Compute；需求：REQ-LC-0009

资源：RES-LC-0201

当前位置：[code.rdl L1114](code.rdl)

```spacerdl
Compute WMonitorEnabled WMonitorWorking ReqCapByFormTable FormulaTable.WMonitorEnabled;
```

输入绑定：WMonitorWorking是上一阶段输出的最新工作快照。

输出绑定：WMonitorEnabled是下一If/While使用的已定义boolean；不提交持久状态。

规则：

- 按冻结代码：CurrentLCState不等于LC_STATE_DISABLED时true；DISABLED时false，false分支不解析WP、不更新任何计数，不评估AP。
- 正常配置枚举ACTIVE/PASSIVE/DISABLED与正式要求一致；不能把非法枚举自动当正常ACTIVE。正式仅ACTIVE/PASSIVE资格在独立documentary视图表达。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L280–282 LC_CheckMsgForWPs application gate

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0202"></a>

## ST-LC-0202 — 选择消息时间戳或当前时刻

操作：Compute；需求：REQ-LC-0009, REQ-LC-0014

资源：RES-LC-0202

当前位置：[code.rdl L1117](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WMonitorTimestamp;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- 更新comparisonTimestamp：采用CFE_MSG_GetMsgTime已观察的Seconds/Subseconds；仅两者均0时用输入now。
- 无真实时间观察时不能编造时间戳；此操作不改变WRT统计、不减age。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L283–289 LC_CheckMsgForWPs timestamp

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0203"></a>

## ST-LC-0203 — 查找完整MID及保留关联WP顺序

操作：Compute；需求：REQ-LC-0006, REQ-LC-0009

资源：RES-LC-0203

当前位置：[code.rdl L1119](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WMonitorMatchWPChain;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- 从完整MessageID的hash桶依Next查完整MID相等项，选其WatchPtList；将该链原顺序写matchedWPIndices、cursor=0、matchedAny、stateKnown=true。
- 合法RuntimeContext由LC_CreateHashTable建立，WP条目索引来自0..LC_MAX_WATCHPOINTS-1且链有限；不擅自按索引排序、不合并相同hash不同MID。
- 不存在MID或WP链为空时matchedAny=false；不增加任何WRT/AP/MonitoredMsgCount。破损链/未知实际运行配置不能冒充正常有效目录。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L126–153 LC_CreateHashTable

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L294–331 LC_CheckMsgForWPs hash / WP chain

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0204"></a>

## ST-LC-0204 — 区分有WP与无WP消息

操作：Compute；需求：REQ-LC-0009

资源：RES-LC-0204

当前位置：[code.rdl L1121](code.rdl)

```spacerdl
Compute WMonitorHasMatchedWP WMonitorWorking ReqCapByFormTable FormulaTable.WMonitorHasMatchedWP;
```

输入绑定：WMonitorWorking是上一阶段输出的最新工作快照。

输出绑定：WMonitorHasMatchedWP是下一If/While使用的已定义boolean；不提交持久状态。

规则：

- 仅matchedWPIndices非空时true；empty为false，不表示消息处理错误，也不把未定义MID的包计算进MonitoredMsgCount。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L336–347 LC_CheckMsgForWPs message accounting

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0205"></a>

## ST-LC-0205 — 构造无关联WP事件计划

操作：Compute；需求：REQ-LC-0009

资源：RES-LC-0205

当前位置：[code.rdl L1217](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WMonitorNoMIDEvent;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- 只向eventPlan追加LC_MID_INF_EID/INFORMATION及原MID，并在orderedSteps记此调用位置；status=ignored。
- submitted=false，实际EVS发送pending；state、WRT、ART、全局计数均不变。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L340–347 LC_CheckMsgForWPs unreferenced MID

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0206"></a>

## ST-LC-0206 — WP链循环条件与不可推导停点

操作：Compute；需求：REQ-LC-0006, REQ-LC-0009, REQ-LC-0065

资源：RES-LC-0206

当前位置：[code.rdl L1124](code.rdl), [code.rdl L1203](code.rdl)

```spacerdl
Compute WMonitorHasNextWP WMonitorWorking ReqCapByFormTable FormulaTable.WMonitorHasNextWP;
```

输入绑定：WMonitorWorking是上一阶段输出的最新工作快照。

输出绑定：WMonitorHasNextWP是下一If/While使用的已定义boolean；不提交持久状态。

规则：

- stateKnown=true且cursor小于matchedWPIndices长度时true；链末或不可推导标志为false。
- 该循环边界是已有有限hash WP链，不补造处理周期。每轮WMonitorAdvanceWP递增cursor，且不改链；所以合法输入最多执行关联WP数量轮。
- 风险路径停止的是规约审查模型，不声称原LC在同位置安全停止。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L318–329 LC_CheckMsgForWPs WatchPtList iteration

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0207"></a>

## ST-LC-0207 — 按原C算术判断偏移并单独识别回绕风险

操作：Compute；需求：REQ-LC-0009, REQ-LC-0013, REQ-LC-0065

资源：RES-LC-0207

当前位置：[code.rdl L1127](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPOffsetArithmetic;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- 设置selectedWP、oldWRT、currentWDT与offsetDiagnosis；DataType对应sizeof(uint8/uint16/uint32/float)，未知类型令codeAccepted=false、detectedError=DATATYPE。
- 已明确目标C算术模型时，忠实算(Offset + NumOfDataBytes) > MsgLength；true为detected OFFSET错误，false为codeAccepted=true。Offset从消息开头含消息头起算。
- 不将size_t宽度当作uint32加法自动变宽。显式32位无符号模型中0xFFFFFFFF+2回绕成1，对length186可放行。
- 另用无回绕跨度分析区分safe-accepted与unsafe-accepted，只作审查分类、不修正codeAccepted。ABI未确定或通过却实际跨度非法令actualAccessKnown=false。
- 只产生诊断、width/codeAccepted/actualAccessKnown/detectedError；此步骤尚不读取风险指针、不写结果、计数或事件。
- 在选择当前WP时statisticsCandidate从oldWRT完整复制，后续只修改明确字段；设置comparisonPerformed=false，避免前一WP结果泄漏。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L784–865 LC_WPOffsetValid

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0208"></a>

## ST-LC-0208 — 原检查允许取数的分支

操作：Compute；需求：REQ-LC-0009, REQ-LC-0013, REQ-LC-0065

资源：RES-LC-0208

当前位置：[code.rdl L1129](code.rdl)

```spacerdl
Compute WPOffsetAccepted WMonitorWorking ReqCapByFormTable FormulaTable.WPOffsetAccepted;
```

输入绑定：WMonitorWorking是上一阶段输出的最新工作快照。

输出绑定：WPOffsetAccepted是下一If/While使用的已定义boolean；不提交持久状态。

规则：

- 取offsetDiagnosis.codeAccepted；未知类型或源码长度拒绝false；已核定算术模型的普通放行与回绕放行均true。
- 无法求原表达式时不得填写false来声称原LC拒绝；此流程的输入要求已提供算术模型，未提供则整段pending-interpretation而非执行。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L801–865 LC_WPOffsetValid return

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0209"></a>

## ST-LC-0209 — 区分安全可推导读取与原码回绕放行

操作：Compute；需求：REQ-LC-0009, REQ-LC-0013, REQ-LC-0065

资源：RES-LC-0209

当前位置：[code.rdl L1132](code.rdl)

```spacerdl
Compute WPAccessKnown WMonitorWorking ReqCapByFormTable FormulaTable.WPAccessKnown;
```

输入绑定：WMonitorWorking是上一阶段输出的最新工作快照。

输出绑定：WPAccessKnown是下一If/While使用的已定义boolean；不提交持久状态。

规则：

- 取offsetDiagnosis.actualAccessKnown：只有codeAccepted=true且明确合法跨度/ABI时true；回绕放行大偏移false。
- false不是LC的拒绝条件，只防止候选规约捏造未知指针之后的值/结果。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L837–865 LC_WPOffsetValid offset addition

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L369–374 LC_ProcessWP raw pointer

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0210"></a>

## ST-LC-0210 — 保留回绕访问的已知前缀并停止结果推导

操作：Compute；需求：REQ-LC-0009, REQ-LC-0013, REQ-LC-0065

资源：RES-LC-0210

当前位置：[code.rdl L1190](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPIndeterminateAccess;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- 设置stateKnown=false、actualResultKnown=false、status=indeterminate、publicState=null，仅保留已知执行前缀orderedSteps。
- 不生成该WP的ERROR、正常结果、统计、事件、MonitoredMsgCount或后续AP动作；已知此前WP写入不得回滚或猜成整体未变。
- 不能宣称此审查停止等于LC已拒绝风险输入；实际未知指针读取和后续行为仍ISSUE-LC-0021/0004。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L837–865 LC_WPOffsetValid wraparound

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L369–374 LC_ProcessWP pointer

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0211"></a>

## ST-LC-0211 — 被检测偏移/类型错误事件的顺序点

操作：Compute；需求：REQ-LC-0008, REQ-LC-0013, REQ-LC-0065, REQ-LC-0067

资源：RES-LC-0211

当前位置：[code.rdl L1182](code.rdl), [code.rdl L1194](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPDetectedErrorEvent;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- 依据detectedError只追加原DATATYPE或OFFSET EVS事件计划，携带当前WP、类型或MID/offset/width/length；记在结果ERROR和age清零的Set之前。
- 不增EvaluationCount、不做比较；计划submitted=false，服务发送未执行。若数据抽取器捕获未知类型，使用DATATYPE事件同一处理点。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L822–836 LC_WPOffsetValid bad datatype

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L846–862 LC_WPOffsetValid offset rejection

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L957–973 LC_GetSizedWPData bad datatype

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0212"></a>

## ST-LC-0212 — 提交被检测错误的四值ERROR

操作：Set；需求：REQ-LC-0008, REQ-LC-0013, REQ-LC-0014, REQ-LC-0065, REQ-LC-0067

资源：RES-LC-0212

当前位置：[code.rdl L1184](code.rdl), [code.rdl L1196](code.rdl)

```spacerdl
Set WPResultPersistent WWatchErrorValue;
```

输入绑定：WWatchErrorValue为冻结枚举LC_WATCH_ERROR。

输出绑定：绑定LC_OperData.WRTPtr[selectedWP].WatchResult；Set只在被检测错误分支执行，同时更新工作快照对此字段的镜像。

规则：

- 写ERROR，不写FALSE；此前错误事件仅计划不声称真实发送。
- EvaluationCount及连续/累计TRUE和两向历史保持。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L834–835 LC_WPOffsetValid datatype correction

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L861–862 LC_WPOffsetValid offset correction

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0213"></a>

## ST-LC-0213 — 被检测错误时清当前WP倒计数

操作：Set；需求：REQ-LC-0007, REQ-LC-0008, REQ-LC-0013, REQ-LC-0065, REQ-LC-0067

资源：RES-LC-0213

当前位置：[code.rdl L1186](code.rdl), [code.rdl L1198](code.rdl)

```spacerdl
Set WPCountdownPersistent WAgeZero;
```

输入绑定：WAgeZero为已有C常量0。

输出绑定：绑定当前WP的WRT.CountdownToStale；同步工作镜像，其余字段不变。

规则：

- 只清CountdownToStale，不清连续TRUE；此拒绝路径不增加EvaluationCount。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L834–835 LC_WPOffsetValid correction

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L861–862 LC_WPOffsetValid correction

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L968–969 LC_GetSizedWPData correction

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0214"></a>

## ST-LC-0214 — 按BE/LE逐字节取数并扩展

操作：Compute；需求：REQ-LC-0009, REQ-LC-0016, REQ-LC-0065

资源：RES-LC-0214

当前位置：[code.rdl L1135](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPExtractNativeData;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- 仅WPAccessKnown=true执行：currentWDT.DataType选择1/2/4字节，采用LC_CopyBytesWithSwap的swap map复制不对齐源字节到本机表示，设置SizedWPData/extractSucceeded。
- 有符号8/16位符号扩展到32位，unsigned补零；DWORD及float保留位表示。偏移仍含消息头。
- 未知DataType设置extractSucceeded=false、detectedError=DATATYPE；不继续掩码/比较；风险指针路径不会进入此操作。
- 不更新WRT/计数/history，也不把AP输入变成原始字节；AP后续读取归一化WP结果。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L873–981 LC_CopyBytesWithSwap / LC_GetSizedWPData

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0215"></a>

## ST-LC-0215 — 数据取出成功后才进入比较

操作：Compute；需求：REQ-LC-0013, REQ-LC-0016, REQ-LC-0065, REQ-LC-0067

资源：RES-LC-0215

当前位置：[code.rdl L1137](code.rdl)

```spacerdl
Compute WPExtractSucceeded WMonitorWorking ReqCapByFormTable FormulaTable.WPExtractSucceeded;
```

输入绑定：WMonitorWorking是上一阶段输出的最新工作快照。

输出绑定：WPExtractSucceeded是下一If/While使用的已定义boolean；不提交持久状态。

规则：

- 只读取extractSucceeded；false进入检测错误事件、ERROR和Countdown=0修正，跳过EvaluationCount。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L373–395 LC_ProcessWP SizedDataValid

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0216"></a>

## ST-LC-0216 — 按WDT掩码形成比较数据

操作：Compute；需求：REQ-LC-0009, REQ-LC-0010, REQ-LC-0011, REQ-LC-0016, REQ-LC-0065

资源：RES-LC-0216

当前位置：[code.rdl L1140](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPApplyMask;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- MaskedWPData=已归一化SizedWPData按位与currentWDT.BitMask，按32位位模式保留；仅改MaskedWPData。
- 旧WatchResult在任何结果Set之前已保存在oldWRT；不从后来已修改WRT读取PreviousResult。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L379–386 LC_ProcessWP PreviousResult / BitMask

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0217"></a>

## ST-LC-0217 — 自定义算子选择分支

操作：Compute；需求：REQ-LC-0009, REQ-LC-0011, REQ-LC-0079

资源：RES-LC-0217

当前位置：[code.rdl L1142](code.rdl)

```spacerdl
Compute WPIsCustomOperator WMonitorWorking ReqCapByFormTable FormulaTable.WPIsCustomOperator;
```

输入绑定：WMonitorWorking是上一阶段输出的最新工作快照。

输出绑定：WPIsCustomOperator是下一If/While使用的已定义boolean；不提交持久状态。

规则：

- currentWDT.OperatorID为LC_OPER_CUSTOM时true，否则false走标准关系比较；数据条件与参数使用活动WDT，不能硬编码。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L388–395 LC_ProcessWP custom branch

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0218"></a>

## ST-LC-0218 — 冻结默认custom钩子的真实FALSE与事件

操作：Compute；需求：REQ-LC-0009, REQ-LC-0011, REQ-LC-0079

资源：RES-LC-0218

当前位置：[code.rdl L1145](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPDefaultCustomHook;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- 形成customCallInputs：WatchIndex、MaskedWPData、完整消息和CustomFuncArgument；针对冻结lc_custom.c所有case/default均构造LC_CFCALL_ERR_EID/ERROR Unexpected事件计划。
- 设置newWPResult=LC_WATCH_FALSE、comparisonPerformed=true；该stub不做任务计算，实际忽略值/参数，不能替换成ERROR。
- 只改customCallInputs、newWPResult、comparisonPerformed和eventPlan/orderedSteps；实际EVS及真实任务custom替换仍待确认。

[evidence/LC/fsw/src/lc_custom.c](<evidence/LC/fsw/src/lc_custom.c>)  L65–96 LC_CustomFunction default stub

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L388–395 LC_ProcessWP custom dispatch

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0219"></a>

## ST-LC-0219 — 按数据类型和活动算子执行六种关系比较

操作：Compute；需求：REQ-LC-0009, REQ-LC-0010, REQ-LC-0013, REQ-LC-0016, REQ-LC-0065, REQ-LC-0067

资源：RES-LC-0219

当前位置：[code.rdl L1148](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPRelationalCompare;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- 将MaskedWPData截回对应8/16/32位类型，与WDT.ComparisonValue相同LC_MultiType表示比较：data operator tableValue，signed/unsigned/float不得混用。
- 支持LE/LT/EQ/NE/GT/GE；整数直接相应关系。float EQ使用Diff<=LC_FLOAT_TOLERANCE、NE使用Diff>容差；容差来自config，不猜数值。GT/GE/LT/LE直接关系。
- 收到WPFloat为NaN时构造LC_WP_NAN_ERR_EID并newWPResult=ERROR；收到无穷继续原关系比较。WDT阈值有限性属于WDT验证，不替该运行操作编造新门。
- 未知算子/类型构造原错误事件并newWPResult=ERROR。合法取数后即便NaN/算子错误仍comparisonPerformed=true，后续结果Set及EvaluationCount必须执行。
- 只改newWPResult、comparisonPerformed、comparisonDiagnostics、eventPlan/orderedSteps；持久结果尚不提交。
- 本次新增事件时输出LCEvent0219Ready=true；无新增事件false。NaN/类型错误、首错资格、EDS/SB实际失败分别依原规则，不因写出SendData而扩大触发条件。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L464–778 LC_OperatorCompare / LC_SignedCompare / LC_UnsignedCompare / LC_FloatCompare

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0220"></a>

## ST-LC-0220 — 独立提交本次比较结果

操作：Set；需求：REQ-LC-0009, REQ-LC-0011, REQ-LC-0013, REQ-LC-0014, REQ-LC-0016, REQ-LC-0067, REQ-LC-0079

资源：RES-LC-0220

当前位置：[code.rdl L1151](code.rdl)

```spacerdl
Set WPResultPersistent WComparedResult;
```

输入绑定：WComparedResult取最新WMonitorWorking.newWPResult，由标准比较或冻结default custom输出，保留FALSE/TRUE/ERROR/STALE枚举。

输出绑定：绑定当前WP WRT.WatchResult，同步工作state镜像；PreviousResult仍为oldWRT.WatchResult。

规则：

- 在取数/比较完成后、EvaluationCount更新之前写本次四值结果。
- NaN比较错误也写ERROR并继续比较次数；offset/抽取失败不走此Set而走拒绝修正。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L398–407 LC_ProcessWP result before statistics

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0221"></a>

## ST-LC-0221 — 比较次数独立计算

操作：Compute；需求：REQ-LC-0013, REQ-LC-0014, REQ-LC-0067

资源：RES-LC-0221

当前位置：[code.rdl L1153](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPIncrementEvaluationCount;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- newEvaluationCount=oldWRT.EvaluationCount+1，按原uint32目标算术处理；所有已成功取数并进入比较的TRUE/FALSE/ERROR/STALE均计一次。
- NaN属于此路径；offset/类型检查拒绝和取数失败不进入。不改其他计数或结果。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L401–407 LC_ProcessWP EvaluationCount

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0222"></a>

## ST-LC-0222 — 提交比较次数

操作：Set；需求：REQ-LC-0013, REQ-LC-0014, REQ-LC-0067

资源：RES-LC-0222

当前位置：[code.rdl L1155](code.rdl)

```spacerdl
Set WPEvaluationCountPersistent WNewEvaluationCount;
```

输入绑定：WNewEvaluationCount取WMonitorWorking.newEvaluationCount。

输出绑定：绑定当前WP WRT.EvaluationCount并同步镜像。

规则：

- 只提交当前WP EvaluationCount；不额外增加全包MonitoredMsgCount。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L407–407 LC_ProcessWP EvaluationCount

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0223"></a>

## ST-LC-0223 — TRUE统计分支条件

操作：Compute；需求：REQ-LC-0014, REQ-LC-0066

资源：RES-LC-0223

当前位置：[code.rdl L1157](code.rdl)

```spacerdl
Compute WPResultTrue WMonitorWorking ReqCapByFormTable FormulaTable.WPResultTrue;
```

输入绑定：WMonitorWorking是上一阶段输出的最新工作快照。

输出绑定：WPResultTrue是下一If/While使用的已定义boolean；不提交持久状态。

规则：

- 仅newWPResult为LC_WATCH_TRUE时true，不把ERROR/STALE当TRUE。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L409–428 LC_ProcessWP TRUE branch

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0224"></a>

## ST-LC-0224 — TRUE累计、连续次数与age重装

操作：Compute；需求：REQ-LC-0007, REQ-LC-0008, REQ-LC-0014

资源：RES-LC-0224

当前位置：[code.rdl L1160](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPTrueStatistics;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- 当前WP CumulativeTrueCount与ConsecutiveTrueCount各在旧值上加1；拟提交CountdownToStale=currentWDT.ResultAgeWhenStale。
- 更新statisticsCandidate的这三字段；不改两向历史、FalseToTrueCount、EvaluationCount、WatchResult或其他WP。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L411–414 LC_ProcessWP TRUE counters and age

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0225"></a>

## ST-LC-0225 — FALSE统计分支条件

操作：Compute；需求：REQ-LC-0012, REQ-LC-0014, REQ-LC-0067

资源：RES-LC-0225

当前位置：[code.rdl L1163](code.rdl)

```spacerdl
Compute WPResultFalse WMonitorWorking ReqCapByFormTable FormulaTable.WPResultFalse;
```

输入绑定：WMonitorWorking是上一阶段输出的最新工作快照。

输出绑定：WPResultFalse是下一If/While使用的已定义boolean；不提交持久状态。

规则：

- 仅newWPResult为LC_WATCH_FALSE时true；false意味着ERROR/STALE或custom其他结果，不误作正常FALSE。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L429–452 LC_ProcessWP FALSE / other

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0226"></a>

## ST-LC-0226 — FALSE连续TRUE清零和age重装

操作：Compute；需求：REQ-LC-0007, REQ-LC-0008, REQ-LC-0011, REQ-LC-0012, REQ-LC-0014, REQ-LC-0079

资源：RES-LC-0226

当前位置：[code.rdl L1166](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPFalseStatistics;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- 拟提交ConsecutiveTrueCount=0、CountdownToStale=currentWDT.ResultAgeWhenStale；CumulativeTrueCount保持旧值。
- 当前default custom返回FALSE也遵守此分支；两向历史、FalseToTrueCount尚保持。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L429–444 LC_ProcessWP FALSE branch

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0227"></a>

## ST-LC-0227 — ERROR/STALE清age而保留连续TRUE

操作：Compute；需求：REQ-LC-0007, REQ-LC-0008, REQ-LC-0013, REQ-LC-0014, REQ-LC-0067

资源：RES-LC-0227

当前位置：[code.rdl L1169](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPErrorStaleStatistics;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- newWPResult不是TRUE/FALSE时，拟提交CountdownToStale=0，源码此分支包含ERROR/STALE及其他返回。
- ConsecutiveTrueCount、CumulativeTrueCount、FalseToTrueCount、两向历史均保持；EvaluationCount已计一次，不再次计数。
- 不把ERROR/STALE改为FALSE/TRUE。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L446–452 LC_ProcessWP ERROR / STALE

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0228"></a>

## ST-LC-0228 — 实现口径的两向跨越门

操作：Compute；需求：REQ-LC-0014, REQ-LC-0066

资源：RES-LC-0228

当前位置：[code.rdl L1173](code.rdl)

```spacerdl
Compute WPCodeTransitionEligible WMonitorWorking ReqCapByFormTable FormulaTable.WPCodeTransitionEligible;
```

输入绑定：取上一阶段最新WMonitorWorking快照的新newWPResult及取数前oldWRT.WatchResult。

输出绑定：WPCodeTransitionEligible为下一If的boolean，不改state。

规则：

- 新TRUE且旧FALSE或STALE为true；新FALSE且旧TRUE或STALE为true；其余false。
- 这是冻结实现口径，不等同LC2004字面FALSE↔TRUE；独立documentary视图禁止把STALE计作FALSE/TRUE。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L416–444 LC_ProcessWP transition checks

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0229"></a>

## ST-LC-0229 — 实现的跨越计数、值和时间戳

操作：Compute；需求：REQ-LC-0014, REQ-LC-0066

资源：RES-LC-0229

当前位置：[code.rdl L1176](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPCodeTransitionRecord;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- 门为新TRUE时拟增FalseToTrueCount并写LastFalseToTrue.DataType=currentWDT.DataType、Value=MaskedWPData、Timestamp=comparisonTimestamp。
- 门为新FALSE时写LastTrueToFalse相同DataType/Value/Timestamp，不造不存在的TrueToFalseCount。
- 仅改对应转变字段；旧STALE被实现纳入门控，与正式要求的literal视图分别追踪。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L416–444 LC_ProcessWP transition records

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0230"></a>

## ST-LC-0230 — 提交当前WP统计与age候选

操作：Set；需求：REQ-LC-0007, REQ-LC-0008, REQ-LC-0009, REQ-LC-0012, REQ-LC-0014, REQ-LC-0066, REQ-LC-0067, REQ-LC-0079

资源：RES-LC-0230

当前位置：[code.rdl L1179](code.rdl)

```spacerdl
Set WPStatisticsPersistent WStatisticsCandidate;
```

输入绑定：WStatisticsCandidate是WMonitorWorking.statisticsCandidate与选定WP绑定的字段子快照，来源为TRUE/FALSE/ERROR统计及可选跨越记录。

输出绑定：仅提交当前WP CumulativeTrueCount、ConsecutiveTrueCount、CountdownToStale、FalseToTrueCount与两向记录中候选改变的字段；不覆盖已经提交WatchResult/EvaluationCount和其他WP。

规则：

- 保留工作快照中未改变字段；在本轮结果和EvaluationCount提交之后按同一无服务交错的统计块提交。
- 这是候选规约中的状态赋值，不声称实际LC程序/SpaceRDL解释器已执行；持久符号与聚合类型绑定pending。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L409–452 LC_ProcessWP statistics

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0231"></a>

## ST-LC-0231 — 推进关联WP游标

操作：Compute；需求：REQ-LC-0006, REQ-LC-0009

资源：RES-LC-0231

当前位置：[code.rdl L1201](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WMonitorAdvanceWP;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- cursor增加1，重新读取刚提交当前WP对应state镜像，下一WP取最新工作状态。
- matchedWPIndices与entry快照不改；风险stateKnown=false时即便cursor推进也不推断额外状态。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L328–329 LC_CheckMsgForWPs Next

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0232"></a>

## ST-LC-0232 — 完整关联WP处理后能否计算包计数

操作：Compute；需求：REQ-LC-0009, REQ-LC-0065

资源：RES-LC-0232

当前位置：[code.rdl L1206](code.rdl)

```spacerdl
Compute WMonitorStateKnown WMonitorWorking ReqCapByFormTable FormulaTable.WMonitorStateKnown;
```

输入绑定：WMonitorWorking是上一阶段输出的最新工作快照。

输出绑定：WMonitorStateKnown是下一If/While使用的已定义boolean；不提交持久状态。

规则：

- 仅stateKnown=true时true；false路径不增加MonitoredMsgCount，不伪断言原代码不会增加。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L336–338 LC_CheckMsgForWPs final count

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L371–374 LC_ProcessWP unsafe pointer

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0233"></a>

## ST-LC-0233 — 整包监测次数只计算一次

操作：Compute；需求：REQ-LC-0009

资源：RES-LC-0233

当前位置：[code.rdl L1209](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WMonitorIncrementMessageCount;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- 关联WP链至少一项且完整可推导时newMonitoredMsgCount=最新working.app.MonitoredMsgCount+1。
- 即使每项都普通offset拒绝仍增包次数；不是每WP加一次。只改该候选值。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L320–338 LC_CheckMsgForWPs found/count

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0234"></a>

## ST-LC-0234 — 提交一次整包监测计数

操作：Set；需求：REQ-LC-0009

资源：RES-LC-0234

当前位置：[code.rdl L1211](code.rdl)

```spacerdl
Set WMonitoredMsgCountPersistent WNewMonitoredMsgCount;
```

输入绑定：WNewMonitoredMsgCount取WMonitorWorking.newMonitoredMsgCount。

输出绑定：绑定LC_AppData.MonitoredMsgCount并更新工作镜像。

规则：

- 不改APSampleCount、RTS计数、ART，不发RTS，不减WP年龄。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L336–338 LC_CheckMsgForWPs MonitoredMsgCount

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0235"></a>

## ST-LC-0235 — 形成监测出口的可推导性与状态连接

操作：Compute；需求：REQ-LC-0009, REQ-LC-0013, REQ-LC-0016, REQ-LC-0065

资源：RES-LC-0235

当前位置：[code.rdl L1214](code.rdl), [code.rdl L1219](code.rdl)

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WMonitorFinalize;
```

输入绑定：WMonitorWorking为本操作前工作快照：取前一个上下文操作的输出，并读独立Set已经提交的对应持久字段；boolean条件操作不会取代工作快照。

输出绑定：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

规则：

- stateKnown=true且matchedAny=true时status=snapshot-only、actualResultKnown=true、publicState为本入口结果；matchedAny=false保留ignored与未变state；stateKnown=false时status=indeterminate、actualResultKnown=false、publicState=null。
- processedWPIndices保留已完成的原hash顺序；events均submitted=false，不宣称服务成功。
- 新持久WRT/AppData由独立后续SampleAP/HK入口读取，不自动触发AP，不虚构两个入口间隔；不重执行旧整入口Compute。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L270–454 LC_CheckMsgForWPs / LC_ProcessWP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0236"></a>

## ST-LC-0236 — 读取待验证WDT回调输入

操作：Set；需求：REQ-LC-0006, REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0236

当前位置：[code.rdl L1229](code.rdl)

```spacerdl
Set WWDTValidationWorking WWDTValidationEntry;
```

输入绑定：来自cFE TBL验证回调的TableData和LC_MAX_WATCHPOINTS；附当前API对各MID的已观测CFE_SB_IsValidMsgId boolean结果、活动ABI/config，不伪造软件服务调用。

输出绑定：V是仅用于本次回调的局部工作快照，包含pendingWDT；不更新当前活动WDT/WRT。

规则：

- 只复制候选WDT/config/接口观察；真实表更新通知、验证回调和更新提交为pending-interface。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L988–1009 LC_ValidateWDT callback

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0237"></a>

## ST-LC-0237 — 建立校验累加器与有界游标

操作：Compute；需求：REQ-LC-0006, REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0237

当前位置：[code.rdl L1231](code.rdl)

```spacerdl
Compute WWDTValidationWorking WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationInitialize;
```

输入绑定：WWDTValidationWorking读取前一上下文操作输出的最新快照及已提交对应持久字段镜像；boolean输出不替代工作快照。

输出绑定：WWDTValidationWorking为操作后快照；仅rules列明成员改变，其他message/table/state/config/中间量保持，下一操作右参数读取此输出。

规则：

- 设置TableIndex=0、TableResult=CFE_SUCCESS、EntryResult=LC_WDTVAL_ERR_NONE、GoodCount=0、BadCount=0、UnusedCount=0、empty eventPlan/orderedSteps。
- 只清本次回调局部量，不复位活动WRT统计。N_WP取平台LC_MAX_WATCHPOINTS而非固定例子值。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L992–1009 LC_ValidateWDT local initialization

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0238"></a>

## ST-LC-0238 — 校验循环容量条件

操作：Compute；需求：REQ-LC-0006, REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0238

当前位置：[code.rdl L1233](code.rdl), [code.rdl L1271](code.rdl)

```spacerdl
Compute WWDTValidationHasNext WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationHasNext;
```

输入绑定：WWDTValidationWorking为最新工作快照。

输出绑定：WWDTValidationHasNext为下一If/While使用的已定义boolean，不提交状态。

规则：

- 仅TableIndex小于config.LC_MAX_WATCHPOINTS时true；否则false。WWDTValidationAdvance每轮加1，平台有限容量保证终止。
- 不将验证回调频率虚构为周期。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1009–1009 LC_ValidateWDT bound

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0239"></a>

## ST-LC-0239 — 读取当前候选条目且保留首错状态

操作：Compute；需求：REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0239

当前位置：[code.rdl L1236](code.rdl)

```spacerdl
Compute WWDTValidationWorking WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationSelectEntry;
```

输入绑定：WWDTValidationWorking读取前一上下文操作输出的最新快照及已提交对应持久字段镜像；boolean输出不替代工作快照。

输出绑定：WWDTValidationWorking为操作后快照；仅rules列明成员改变，其他message/table/state/config/中间量保持，下一操作右参数读取此输出。

规则：

- 读取pendingWDT[TableIndex]的DataType/OperatorID/MessageID/ComparisonValue，设置currentEntryKind=unclassified。
- 保留EntryResult及TableResult；源码EntryResult初始化在循环外，不能擅自声称每项清零。后续good/bad统计按本项实际分类而不是残留EntryResult。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L992–1015 LC_ValidateWDT entry read

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0240"></a>

## ST-LC-0240 — 未使用WDT条目的跳过门

操作：Compute；需求：REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0240

当前位置：[code.rdl L1238](code.rdl)

```spacerdl
Compute WWDTValidationUnused WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationUnused;
```

输入绑定：WWDTValidationWorking为最新工作快照。

输出绑定：WWDTValidationUnused为下一If/While使用的已定义boolean，不提交状态。

规则：

- DataType为LC_DATA_WATCH_NOT_USED时true，否则false；unused分支跳过类型/算子/MID/float校验。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1015–1021 LC_ValidateWDT unused

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0241"></a>

## ST-LC-0241 — 单独累计未使用条目

操作：Compute；需求：REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0241

当前位置：[code.rdl L1241](code.rdl)

```spacerdl
Compute WWDTValidationWorking WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationCountUnused;
```

输入绑定：WWDTValidationWorking读取前一上下文操作输出的最新快照及已提交对应持久字段镜像；boolean输出不替代工作快照。

输出绑定：WWDTValidationWorking为操作后快照；仅rules列明成员改变，其他message/table/state/config/中间量保持，下一操作右参数读取此输出。

规则：

- UnusedCount加1，currentEntryKind=unused；GoodCount/BadCount/EntryResult/TableResult保持。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1015–1021 LC_ValidateWDT UnusedCount

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0242"></a>

## ST-LC-0242 — 核验数据类型决定的数据大小

操作：Compute；需求：REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0242

当前位置：[code.rdl L1244](code.rdl)

```spacerdl
Compute WWDTValidationWorking WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationDataType;
```

输入绑定：WWDTValidationWorking读取前一上下文操作输出的最新快照及已提交对应持久字段镜像；boolean输出不替代工作快照。

输出绑定：WWDTValidationWorking为操作后快照；仅rules列明成员改变，其他message/table/state/config/中间量保持，下一操作右参数读取此输出。

规则：

- DataType必须为BYTE/UBYTE、WORD/UWORD_BE/LE、DWORD/UDWORD_BE/LE、FLOAT_BE/LE清单。
- 合格设置dataTypeValid=true；不合格设置false、currentEntryKind=bad、EntryResult=LC_WDTVAL_ERR_DATATYPE。
- 不验证WatchpointOffset或加法安全、不验证age单位/任务custom算法；不能把此类型验证概括成全跨度安全。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1022–1034 LC_ValidateWDT datatype

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0243"></a>

## ST-LC-0243 — 类型合法后才核验算子

操作：Compute；需求：REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0243

当前位置：[code.rdl L1246](code.rdl)

```spacerdl
Compute WWDTValidationDataTypeOK WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationDataTypeOK;
```

输入绑定：WWDTValidationWorking为最新工作快照。

输出绑定：WWDTValidationDataTypeOK为下一If/While使用的已定义boolean，不提交状态。

规则：

- 读取本项dataTypeValid；false跳过后续算子/MID/float，确保每项最多计一个bad类别。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1022–1035 LC_ValidateWDT else-if order

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0244"></a>

## ST-LC-0244 — 核验六关系与custom算子

操作：Compute；需求：REQ-LC-0010, REQ-LC-0011, REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0244

当前位置：[code.rdl L1249](code.rdl)

```spacerdl
Compute WWDTValidationWorking WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationOperator;
```

输入绑定：WWDTValidationWorking读取前一上下文操作输出的最新快照及已提交对应持久字段镜像；boolean输出不替代工作快照。

输出绑定：WWDTValidationWorking为操作后快照；仅rules列明成员改变，其他message/table/state/config/中间量保持，下一操作右参数读取此输出。

规则：

- 仅合法DataType条目执行；OperatorID必须为LT/LE/NE/EQ/GE/GT/CUSTOM。
- 合格operatorValid=true；非法operatorValid=false、currentEntryKind=bad、EntryResult=LC_WDTVAL_ERR_OPER；不改类型判定或计数。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1035–1044 LC_ValidateWDT operator

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0245"></a>

## ST-LC-0245 — 算子合法后才核验MID

操作：Compute；需求：REQ-LC-0010, REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0245

当前位置：[code.rdl L1251](code.rdl)

```spacerdl
Compute WWDTValidationOperatorOK WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationOperatorOK;
```

输入绑定：WWDTValidationWorking为最新工作快照。

输出绑定：WWDTValidationOperatorOK为下一If/While使用的已定义boolean，不提交状态。

规则：

- 读取operatorValid；false跳过MID/float以保留首错误分类。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1035–1045 LC_ValidateWDT order

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0246"></a>

## ST-LC-0246 — 忠实采用cFE MID合法性谓词观察

操作：Compute；需求：REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0246

当前位置：[code.rdl L1254](code.rdl)

```spacerdl
Compute WWDTValidationWorking WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationMID;
```

输入绑定：WWDTValidationWorking读取前一上下文操作输出的最新快照及已提交对应持久字段镜像；boolean输出不替代工作快照。

输出绑定：WWDTValidationWorking为操作后快照；仅rules列明成员改变，其他message/table/state/config/中间量保持，下一操作右参数读取此输出。

规则：

- 只在类型与算子合格时，midValid=入口所附当前条目CFE_SB_IsValidMsgId(MessageID)真实boolean观察。
- false则currentEntryKind=bad、EntryResult=LC_WDTVAL_ERR_MID；true留待浮点阈值判定。
- 没有服务观察或未冻结cFE定义时本步骤及后续结论pending-interface，不自己用数值范围代替cFE谓词、不默认true。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1045–1052 LC_ValidateWDT MID validation

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0247"></a>

## ST-LC-0247 — MID合格后才核验浮点阈值

操作：Compute；需求：REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0247

当前位置：[code.rdl L1256](code.rdl)

```spacerdl
Compute WWDTValidationMIDOK WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationMIDOK;
```

输入绑定：WWDTValidationWorking为最新工作快照。

输出绑定：WWDTValidationMIDOK为下一If/While使用的已定义boolean，不提交状态。

规则：

- 读取已观测的midValid；false跳过float。谓词观察缺失时不能执行此boolean分支为正常。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1045–1053 LC_ValidateWDT MID/float order

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0248"></a>

## ST-LC-0248 — 浮点阈值排除NaN与无穷

操作：Compute；需求：REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0248

当前位置：[code.rdl L1259](code.rdl)

```spacerdl
Compute WWDTValidationWorking WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationFloatThreshold;
```

输入绑定：WWDTValidationWorking读取前一上下文操作输出的最新快照及已提交对应持久字段镜像；boolean输出不替代工作快照。

输出绑定：WWDTValidationWorking为操作后快照；仅rules列明成员改变，其他message/table/state/config/中间量保持，下一操作右参数读取此输出。

规则：

- 仅通过类型/算子/MID的条目执行；FLOAT_BE/LE按LC_MultiType位复制为float：NaN优先为FPNAN错误，其次非finite为FPINF错误，其余good。
- 非float直接currentEntryKind=good；float错误设置本项bad及对应EntryResult，合法不改残留EntryResult。
- 运行中收到的WP无穷值并不因此变ERROR，本步骤只约束WDT ComparisonValue。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1053–1087 LC_ValidateWDT float threshold

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0249"></a>

## ST-LC-0249 — 每使用中条目累计一次good或bad

操作：Compute；需求：REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0249

当前位置：[code.rdl L1264](code.rdl)

```spacerdl
Compute WWDTValidationWorking WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationCountResult;
```

输入绑定：WWDTValidationWorking读取前一上下文操作输出的最新快照及已提交对应持久字段镜像；boolean输出不替代工作快照。

输出绑定：WWDTValidationWorking为操作后快照；仅rules列明成员改变，其他message/table/state/config/中间量保持，下一操作右参数读取此输出。

规则：

- 本项currentEntryKind=bad时BadCount加1，good时GoodCount加1；unused由独立操作已计，不重复。
- 不按旧EntryResult判定本项bad；源码else-if保证每项只落一个分类。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1032–1087 LC_ValidateWDT good/bad accounting

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0250"></a>

## ST-LC-0250 — 保留首错返回码与详细事件位置

操作：Compute；需求：REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0250

当前位置：[code.rdl L1267](code.rdl)

```spacerdl
Compute WWDTValidationWorking WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationFirstError;
```

输入绑定：WWDTValidationWorking读取前一上下文操作输出的最新快照及已提交对应持久字段镜像；boolean输出不替代工作快照。

输出绑定：WWDTValidationWorking为操作后快照；仅rules列明成员改变，其他message/table/state/config/中间量保持，下一操作右参数读取此输出。

规则：

- 只有EntryResult非NONE且TableResult仍CFE_SUCCESS，才按float错误或普通错误构造首错EVS事件并设置TableResult=EntryResult。
- float事件携阈值原uint32位模式；普通事件携WP index、Err/DataType/OperatorID/MID。之后条目错误不再发明细，但仍逐项计good/bad/unused。
- 事件submitted=false，不声称EVS发送成功；不改变活动WDT/WRT。
- 本次新增事件时输出LCEvent0250Ready=true；无新增事件false。NaN/类型错误、首错资格、EDS/SB实际失败分别依原规则，不因写出SendData而扩大触发条件。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1092–1119 LC_ValidateWDT first error

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0251"></a>

## ST-LC-0251 — 推进候选WDT校验游标

操作：Compute；需求：REQ-LC-0006, REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0251

当前位置：[code.rdl L1269](code.rdl)

```spacerdl
Compute WWDTValidationWorking WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationAdvance;
```

输入绑定：WWDTValidationWorking读取前一上下文操作输出的最新快照及已提交对应持久字段镜像；boolean输出不替代工作快照。

输出绑定：WWDTValidationWorking为操作后快照；仅rules列明成员改变，其他message/table/state/config/中间量保持，下一操作右参数读取此输出。

规则：

- TableIndex加1，不改pendingWDT、所有活动state与已有首错；循环条件随后重算。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1009–1009 LC_ValidateWDT for increment

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1121–1121 LC_ValidateWDT iteration end

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0252"></a>

## ST-LC-0252 — 构造全表统计报告与回调返回值

操作：Compute；需求：REQ-LC-0006, REQ-LC-0015, REQ-LC-0059

资源：RES-LC-0252

当前位置：[code.rdl L1274](code.rdl)

```spacerdl
Compute WWDTValidationWorking WWDTValidationWorking ReqCapByFormTable FormulaTable.WWDTValidationReport;
```

输入绑定：WWDTValidationWorking读取前一上下文操作输出的最新快照及已提交对应持久字段镜像；boolean输出不替代工作快照。

输出绑定：WWDTValidationWorking为操作后快照；仅rules列明成员改变，其他message/table/state/config/中间量保持，下一操作右参数读取此输出。

规则：

- 全部N_WP项完成后构造LC_WDTVAL_INF_EID/INFORMATION的good/bad/unused事件计划，validationReturnCode=TableResult。
- 无bad为CFE_SUCCESS；有bad返回首错，统计和返回值不表示cFE已接受/提交表更新。
- 没有验证offset、Event/单位/custom任务语义，不补造更强保证。

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L1123–1133 LC_ValidateWDT report/return

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0253"></a>

## ST-LC-0253 — 读取同一次采样末尾age维护输入

操作：Set；需求：REQ-LC-0007, REQ-LC-0008, REQ-LC-0064

资源：RES-LC-0253

当前位置：[code.rdl L788](code.rdl), [code.rdl L1042](code.rdl)

```spacerdl
Set WAgeWorking ActionWorking;
```

输入绑定：ST0368刚输出的ActionWorking：同次AP处理后的最新持久WRT、ART、AppData、ValidSampleCmd及原UpdateAge；不是初始请求快照。

输出绑定：A只复制请求续段工作快照；AP求值已完成，不重新执行RPN或消费监测完成信号。

规则：

- 采样长度错误/应用DISABLED/索引非法不得伪造此合法续段；ValidSampleCmd=true但首AP NOT_USED/PERMOFF拒绝仍可维护age，须保留源码行为。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L60–104 LC_SampleAPReq sample before age

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0254"></a>

## ST-LC-0254 — 有效采样且UpdateAge非零的维护门

操作：Compute；需求：REQ-LC-0007, REQ-LC-0008, REQ-LC-0064

资源：RES-LC-0254

当前位置：[code.rdl L790](code.rdl), [code.rdl L1044](code.rdl)

```spacerdl
Compute WAgeUpdateRequested WAgeWorking ReqCapByFormTable FormulaTable.WAgeUpdateRequested;
```

输入绑定：WAgeWorking为最新工作快照。

输出绑定：WAgeUpdateRequested为下一If/While使用的已定义boolean，不提交状态。

规则：

- 仅入口ValidSampleCmd=true且UpdateAge非零时true；false分支无WRT写入、无老化。
- 不把非零当固定数值1的增量或时间周期；每个这样的请求令所有正倒计数恰减一次。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L91–104 LC_SampleAPReq age gate

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0255"></a>

## ST-LC-0255 — 初始化全WRT维护游标

操作：Compute；需求：REQ-LC-0006, REQ-LC-0007, REQ-LC-0008, REQ-LC-0064

资源：RES-LC-0255

当前位置：[code.rdl L793](code.rdl), [code.rdl L1047](code.rdl)

```spacerdl
Compute WAgeWorking WAgeWorking ReqCapByFormTable FormulaTable.WAgeInitializeCursor;
```

输入绑定：WAgeWorking读取前一上下文操作输出的最新快照及已提交对应持久字段镜像；boolean输出不替代工作快照。

输出绑定：WAgeWorking为操作后快照；仅rules列明成员改变，其他message/table/state/config/中间量保持，下一操作右参数读取此输出。

规则：

- 设置WatchIndex=0，维护容量为平台LC_MAX_WATCHPOINTS；不变更任何WRT。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L93–94 LC_SampleAPReq WatchIndex for

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0256"></a>

## ST-LC-0256 — 全WRT age循环条件

操作：Compute；需求：REQ-LC-0006, REQ-LC-0007, REQ-LC-0008, REQ-LC-0064

资源：RES-LC-0256

当前位置：[code.rdl L795](code.rdl), [code.rdl L814](code.rdl), [code.rdl L1049](code.rdl), [code.rdl L1068](code.rdl)

```spacerdl
Compute WAgeHasNext WAgeWorking ReqCapByFormTable FormulaTable.WAgeHasNext;
```

输入绑定：WAgeWorking为最新工作快照。

输出绑定：WAgeHasNext为下一If/While使用的已定义boolean，不提交状态。

规则：

- WatchIndex小于LC_MAX_WATCHPOINTS为true；否则false。WAgeAdvance每轮加1且容量固定有限，不造时限。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L93–104 LC_SampleAPReq age loop

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0257"></a>

## ST-LC-0257 — 计算当前WP倒计数一次维护结果

操作：Compute；需求：REQ-LC-0007, REQ-LC-0008, REQ-LC-0014, REQ-LC-0064

资源：RES-LC-0257

当前位置：[code.rdl L798](code.rdl), [code.rdl L1052](code.rdl)

```spacerdl
Compute WAgeWorking WAgeWorking ReqCapByFormTable FormulaTable.WAgeComputeNextCountdown;
```

输入绑定：WAgeWorking读取前一上下文操作输出的最新快照及已提交对应持久字段镜像；boolean输出不替代工作快照。

输出绑定：WAgeWorking为操作后快照；仅rules列明成员改变，其他message/table/state/config/中间量保持，下一操作右参数读取此输出。

规则：

- 取当前WRT.CountdownToStale为oldCountdown；oldCountdown>0时newCountdown=oldCountdown-1，否则newCountdown=oldCountdown不做下溢。
- 设置countdownWasPositive和selectedWP；结果/其他统计不变。
- 仅当前请求末尾执行，本次AP使用老化前结果，下次请求才见维护结果。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L95–97 LC_SampleAPReq Countdown decrement

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0258"></a>

## ST-LC-0258 — 零倒计数保持而非下溢

操作：Compute；需求：REQ-LC-0007, REQ-LC-0008, REQ-LC-0064

资源：RES-LC-0258

当前位置：[code.rdl L800](code.rdl), [code.rdl L1054](code.rdl)

```spacerdl
Compute WAgeWasPositive WAgeWorking ReqCapByFormTable FormulaTable.WAgeWasPositive;
```

输入绑定：WAgeWorking为最新工作快照。

输出绑定：WAgeWasPositive为下一If/While使用的已定义boolean，不提交状态。

规则：

- 仅countdownWasPositive时true；old=0时false且不写STALE，保留原结果。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L95–104 LC_SampleAPReq positive countdown

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0259"></a>

## ST-LC-0259 — 提交正倒计数的减一结果

操作：Set；需求：REQ-LC-0007, REQ-LC-0008, REQ-LC-0014, REQ-LC-0064

资源：RES-LC-0259

当前位置：[code.rdl L803](code.rdl), [code.rdl L1057](code.rdl)

```spacerdl
Set WAgeCountdownPersistent WAgeNewCountdown;
```

输入绑定：WAgeNewCountdown取WAgeWorking.newCountdown。

输出绑定：绑定当前WatchIndex的WRT.CountdownToStale并同步续段工作镜像。

规则：

- 只在oldCountdown>0分支执行；不增/清其他统计、不先把ResultAgeWhenStale0写STALE。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L95–99 LC_SampleAPReq decrement then zero

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0260"></a>

## ST-LC-0260 — 减一后恰到零的过期门

操作：Compute；需求：REQ-LC-0007, REQ-LC-0008, REQ-LC-0064

资源：RES-LC-0260

当前位置：[code.rdl L805](code.rdl), [code.rdl L1059](code.rdl)

```spacerdl
Compute WAgeBecameZero WAgeWorking ReqCapByFormTable FormulaTable.WAgeBecameZero;
```

输入绑定：WAgeWorking为最新工作快照。

输出绑定：WAgeBecameZero为下一If/While使用的已定义boolean，不提交状态。

规则：

- 只有本轮已经old>0并提交newCountdown后，newCountdown为0才true；否则false。
- 旧Countdown=0不走此门，不把其当前结果自动改STALE。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L99–102 LC_SampleAPReq zero test

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0261"></a>

## ST-LC-0261 — 到零才提交四值STALE

操作：Set；需求：REQ-LC-0007, REQ-LC-0008, REQ-LC-0014, REQ-LC-0064

资源：RES-LC-0261

当前位置：[code.rdl L808](code.rdl), [code.rdl L1062](code.rdl)

```spacerdl
Set WAgeResultPersistent WWatchStaleValue;
```

输入绑定：WWatchStaleValue为原LC_WATCH_STALE枚举。

输出绑定：绑定当前WRT.WatchResult并同步最新state镜像，供下一Sample/HK入口读取。

规则：

- 只在正倒计数递减到0后执行；保留ConsecutiveTrueCount、EvaluationCount、历史等统计。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L99–102 LC_SampleAPReq WatchResult stale

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0262"></a>

## ST-LC-0262 — 推进age维护游标

操作：Compute；需求：REQ-LC-0006, REQ-LC-0007, REQ-LC-0008, REQ-LC-0064

资源：RES-LC-0262

当前位置：[code.rdl L812](code.rdl), [code.rdl L1066](code.rdl)

```spacerdl
Compute WAgeWorking WAgeWorking ReqCapByFormTable FormulaTable.WAgeAdvance;
```

输入绑定：WAgeWorking读取前一上下文操作输出的最新快照及已提交对应持久字段镜像；boolean输出不替代工作快照。

输出绑定：WAgeWorking为操作后快照；仅rules列明成员改变，其他message/table/state/config/中间量保持，下一操作右参数读取此输出。

规则：

- WatchIndex加1并保持刚提交倒计数/结果的工作镜像；下一条件重算。
- 全表维护只执行一轮，不发RTS/事件，不重跑AP。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L93–104 LC_SampleAPReq WatchIndex increment

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0263"></a>

## ST-LC-0263 — 正式要求的ACTIVE/PASSIVE资格

操作：Compute；需求：REQ-LC-0009

资源：RES-LC-0263

当前位置：[code.rdl L1092](code.rdl)

```spacerdl
Compute WDocMonitorPermitted WDocumentaryMonitorEntry ReqCapByFormTable FormulaTable.WPDocumentaryApplicationGate;
```

输入绑定：来自LC2003正式义务视图的原消息/WDT与应用状态，不作为实现状态修正。

输出绑定：WDocMonitorPermitted仅在ACTIVE/PASSIVE为true；独立documentary If条件。

规则：

- 按LC2003字面仅ACTIVE或PASSIVE允许相关数据比较；DISABLED及未定义枚举不纳入此许可。
- 该documentary门与code-derived CurrentLCState!=DISABLED门分别报告；正常三枚举一致，非法枚举部署语义尚待确认。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L16–18 LC2003

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0264"></a>

## ST-LC-0264 — 正式跨越统计只承认字面FALSE与TRUE

操作：Compute；需求：REQ-LC-0014, REQ-LC-0066

资源：RES-LC-0264

当前位置：[code.rdl L1098](code.rdl)

```spacerdl
Compute WDocLiteralTransition WDocumentaryStatisticsEntry ReqCapByFormTable FormulaTable.WPDocumentaryLiteralTransitionGate;
```

输入绑定：包含旧result、新result、掩码数据/时间戳及旧统计的独立LC2004正式义务输入。

输出绑定：WDocLiteralTransition为字面FALSE→TRUE或TRUE→FALSE时true，其他false。

规则：

- 旧FALSE且新TRUE、或旧TRUE且新FALSE才true；旧STALE/ERROR不自动转换成FALSE/TRUE。
- 不是改原LC的实现门；本视图隔离ISSUE-LC-0006统计口径冲突。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L29–39 LC2004 literal transitions

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0265"></a>

## ST-LC-0265 — 表达正式要求两向跨越值及时间

操作：Compute；需求：REQ-LC-0014, REQ-LC-0066

资源：RES-LC-0265

当前位置：[code.rdl L1101](code.rdl)

```spacerdl
Compute WDocumentaryStatisticsCandidate WDocumentaryStatisticsEntry ReqCapByFormTable FormulaTable.WPDocumentaryLiteralTransition;
```

输入绑定：来自WDocLiteralTransition=true的同一正式义务输入；oldStatistics不来自实现已计STALE的累计值重解释。

输出绑定：WDocumentaryStatisticsCandidate是独立documentary候选，不写当前LC WRT。

规则：

- 旧FALSE→新TRUE时FalseToTrueCount增1并写LastFalseToTrue.Value/Timestamp；旧TRUE→新FALSE时写LastTrueToFalse.Value/Timestamp；其余全部保持。
- 不虚构TrueToFalseCount；不在此候选计算中混入STALE跨越。DataType保留原数据记录类型，语义口径与实现分别。
- 全量一致性需要用户裁定是否保留字面或采用实现STALE视同另一侧；不得据此声称原代码实现正式统计完全一致。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L29–39 LC2004

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L416–444 implementation contrast

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0266"></a>

## ST-LC-0266 — 保留正式跨越义务视图结果

操作：Set；需求：REQ-LC-0014, REQ-LC-0066

资源：RES-LC-0266

当前位置：[code.rdl L1103](code.rdl)

```spacerdl
Set WDocumentaryStatisticsView WDocumentaryStatisticsCandidate;
```

输入绑定：来自独立WPDocumentaryLiteralTransition的候选，不与code-derived工作state合并。

输出绑定：WDocumentaryStatisticsView为审查用正式需求状态视图，不绑定当前LC_OperData.WRTPtr。

规则：

- 只记录正式义务候选；不改LC原工程或用此候选覆盖冻结实现WRT。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L29–39 LC2004

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0267"></a>

## ST-LC-0267 — 正式无法评估ERROR义务的条件

操作：Compute；需求：REQ-LC-0013

资源：RES-LC-0267

当前位置：[code.rdl L1082](code.rdl)

```spacerdl
Compute WDocCannotEvaluate WDocumentaryEvaluationEntry ReqCapByFormTable FormulaTable.WPDocumentaryUnevaluableGate;
```

输入绑定：正式义务输入提供knownEvaluationUnavailable，与源码detectedError、unsafeAccepted/unknownAfterAccess分别列出。

输出绑定：WDocCannotEvaluate仅对有确认无法评估事实时true；未知指针后行为不填成true或正常false。

规则：

- 原LC2003.4要求无法评估时结果为ERROR。条件仅对确认无法评估事实建模，未知访问后的实际结果保持pending-interpretation。
- 提出安全拒绝跨度算法不是自动将其加入原要求或认定源码已有；回绕漏检安全要求仍待确认。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L28–28 LC2003.4

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L784–865 implementation limitations

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0268"></a>

## ST-LC-0268 — 独立表达正式ERROR结果义务

操作：Set；需求：REQ-LC-0013

资源：RES-LC-0268

当前位置：[code.rdl L1085](code.rdl)

```spacerdl
Set WDocumentaryRequiredWatchResult WWatchErrorValue;
```

输入绑定：WWatchErrorValue是已定义LC_WATCH_ERROR；前置是WDocCannotEvaluate=true的确认无法评估事实。

输出绑定：绑定独立documentary WRT结果变量，而非真实code-derived WRT；保存规范要求的目标值。

规则：

- 不能用FALSE替代ERROR；不宣称风险访问原码实际返回ERROR。
- 真实实现错误检出能力冲突与接口/ABI缺口分别保留；此正式要求视图不是源码修复。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L28–28 LC2003.4

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0269"></a>

## ST-LC-0269 — 保留正式custom要求的真实调用数据

操作：Compute；需求：REQ-LC-0011, REQ-LC-0079

资源：RES-LC-0269

当前位置：[code.rdl L1076](code.rdl)

```spacerdl
Compute WDocumentaryCustomRequest WDocumentaryCustomEntry ReqCapByFormTable FormulaTable.WPDocumentaryCustomInputs;
```

输入绑定：正式义务入口提供选定WatchIndex、已转换并掩码数据、原完整消息、活动WDT.CustomFuncArgument及OperatorID。

输出绑定：WDocumentaryCustomRequest为完整任务custom调用输入/输出义务描述，不产生虚构任务计算结果。

规则：

- 只有CUSTOM选择时建立WatchIndex/ProcessedWPData/BufPtr/WDTCustomFuncArg四项调用参数及调用请求计划；其他成员与旧状态不变。
- 真实任务custom处理规则/期望结果缺失，输出标calculationDefinition=pending而不赋正常值；不把冻结stub的FALSE当实际任务算法。
- 冻结stub视图与正式支持任务custom的义务同时保留；软件调用适配与任务算法定义分别pending-interface/pending-interpretation。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L26–26 LC2003.2

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L388–395 LC_ProcessWP custom inputs

[evidence/LC/fsw/src/lc_custom.c](<evidence/LC/fsw/src/lc_custom.c>)  L65–96 default stub boundary

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0300"></a>

## ST-LC-0300 — 取得独立采样请求与已持久化监测结果快照

操作：Compute；需求：REQ-LC-0017, REQ-LC-0018, REQ-LC-0022, REQ-LC-0064, REQ-LC-0069

资源：RES-LC-0300

当前位置：[code.rdl L563](code.rdl)

```spacerdl
Compute ActionWorking ActionInput0300 ReqCapByFormTable FormulaTable.SampleEntrySnapshot;
```

输入绑定：待绑定的 LC_SAMPLE_AP_MID 消息入口，须先通过 LC_SampleAPVerifyDispatch 长度校验；读取该消息载荷 StartIndex/EndIndex/UpdateAge，当前 AppData/WRT/ART/ADT/配置。不是定时任务，不与监测数据入口合并。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 工作成员 request、appState、AppData、WRT、ART、ADT、config 取已确认来源；初始 effects 空，ValidSampleCmd=false；保留原消息及unknown配置边界。
- 后续串行 AP 求值读取该请求到达时最新持久 WRT；监测数据处理完成不自动触发采样。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L44–55 LC_SampleAPReq

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L332–337 LC_AppPipe

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0301"></a>

## ST-LC-0301 — 核对应用是否允许采样

操作：Compute；需求：REQ-LC-0018, REQ-LC-0064

资源：RES-LC-0301

当前位置：[code.rdl L565](code.rdl)

```spacerdl
Compute SampleAppEnabled ActionWorking ReqCapByFormTable FormulaTable.SampleAppEnabled;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 SampleAppEnabled，供后继条件或 Set 使用；不替换工作快照。

规则：

- 源码谓词 CurrentLCState != LC_STATE_DISABLED；正常状态 ACTIVE/PASSIVE 为TRUE，DISABLED为FALSE；不扩展为未知应用状态的安全证明。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L55–55 LC_SampleAPReq

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0302"></a>

## ST-LC-0302 — 独立核对 ALL 或有界 inclusive AP 范围

操作：Compute；需求：REQ-LC-0017, REQ-LC-0018, REQ-LC-0064, REQ-LC-0069

资源：RES-LC-0302

当前位置：[code.rdl L568](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.NormalizeSampleRange;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 仅当 StartIndex 与 EndIndex 均等于 LC_ALL_ACTIONPOINTS 时归一为0..LC_MAX_ACTIONPOINTS-1。
- 否则仅 StartIndex<=EndIndex 且 EndIndex<LC_MAX_ACTIONPOINTS 合法；单边ALL不作为全选。
- 写rangeStart/rangeEnd/rangeValid；ValidSampleCmd保持false，LC_SampleAPs路径返回后才独立标为true，匹配源码赋值位置。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L60–85 LC_SampleAPReq

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0303"></a>

## ST-LC-0303 — 登记非法采样范围的错误事件，不采样不减龄

操作：Compute；需求：REQ-LC-0018, REQ-LC-0064, REQ-LC-0069

资源：RES-LC-0303

当前位置：[code.rdl L821](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.InvalidSampleRangeEffect;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- rangeValid=false时仅追加 LC_APSAMPLE_APNUM_ERR_EID ERROR待提交描述，含原StartIndex/EndIndex。
- ValidSampleCmd=false；ART/AppData采样及RTS统计/WRT倒数保持，无任何RTS请求；真实EVS提交pending-interface。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L76–85 LC_SampleAPReq

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0304"></a>

## ST-LC-0304 — 核对实现中的范围首项门控

操作：Compute；需求：REQ-LC-0018, REQ-LC-0031, REQ-LC-0032, REQ-LC-0069

资源：RES-LC-0304

当前位置：[code.rdl L571](code.rdl)

```spacerdl
Compute StartingAPOperational ActionWorking ReqCapByFormTable FormulaTable.StartingAPOperational;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 StartingAPOperational，供后继条件或 Set 使用；不替换工作快照。

规则：

- 读取合法rangeStart的 ART.CurrentState；非 LC_ACTION_NOT_USED 且非LC_APSTATE_PERMOFF为TRUE。首项DISABLED通过此范围门控，但单项仍跳过。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L50–71 LC_SampleAPs

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0305"></a>

## ST-LC-0305 — 登记首项不可操作导致整个范围被拒绝

操作：Compute；需求：REQ-LC-0018, REQ-LC-0031, REQ-LC-0032, REQ-LC-0064, REQ-LC-0069

资源：RES-LC-0305

当前位置：[code.rdl L777](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.StartingAPRejectedEffect;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 首项NOT_USED/PERMOFF时追加 LC_APSAMPLE_CURR_ERR_EID ERROR待提交描述，整个range内AP均不采样，包括后续ACTIVE/PASSIVE项。
- 首项拒绝不改变索引合法的rangeValid；返回后ValidSampleCmd仍将被标true并可能UpdateAge，不能偷偷修复成仅跳过首项。ART/AppData采样统计均不改。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L62–71 LC_SampleAPs

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L65–74 LC_SampleAPReq

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0306"></a>

## ST-LC-0306 — 初始化本请求 AP 游标

操作：Compute；需求：REQ-LC-0017, REQ-LC-0018, REQ-LC-0069

资源：RES-LC-0306

当前位置：[code.rdl L574](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.BeginAPIteration;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- apIndex=rangeStart，rangeEnd维持inclusive上界；AP遍历variant为rangeEnd-apIndex+1，AP容量以平台符号而非猜测飞行值绑定。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L57–59 LC_SampleAPs

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0307"></a>

## ST-LC-0307 — 判断 inclusive 范围内是否还有 AP

操作：Compute；需求：REQ-LC-0017, REQ-LC-0018, REQ-LC-0069

资源：RES-LC-0307

当前位置：[code.rdl L576](code.rdl), [code.rdl L773](code.rdl)

```spacerdl
Compute HasSelectedAP ActionWorking ReqCapByFormTable FormulaTable.HasSelectedAP;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 HasSelectedAP，供后继条件或 Set 使用；不替换工作快照。

规则：

- TRUE当apIndex<=rangeEnd且apIndex在冻结配置的AP容量内；初始化范围已核定，每轮推进后重新计算，FALSE结束AP循环。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L57–59 LC_SampleAPs

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0308"></a>

## ST-LC-0308 — 取得当前 AP 原状态、旧结果与ADT定义

操作：Compute；需求：REQ-LC-0018, REQ-LC-0022, REQ-LC-0030, REQ-LC-0031, REQ-LC-0032, REQ-LC-0033, REQ-LC-0069

资源：RES-LC-0308

当前位置：[code.rdl L579](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.LoadSelectedAP;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 绑定当前apIndex，保存 originalAPState=ART.CurrentState、previousResult=ART.ActionResult 与本ADT配置；该 originalAPState 本次分支保持，即使后继CurrentState改变。
- 保留前一AP已写回的全局计数；WRT不减龄，RPN不得读下次年龄快照。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L94–108 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0309"></a>

## ST-LC-0309 — 保留 DISABLED、NOT_USED、PERMOFF AP 且禁止其RTS

操作：Compute；需求：REQ-LC-0018, REQ-LC-0022, REQ-LC-0030, REQ-LC-0031, REQ-LC-0032, REQ-LC-0033, REQ-LC-0069

资源：RES-LC-0309

当前位置：[code.rdl L768](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.PreserveSkippedAP;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 不可评估状态不增加APSampleCount、不执行RPN、不更新该ART结果/统计、无该AP的RTS或动作事件；其余合法AP继续循环。
- 源码首项拒绝整范围的差异只在外层门控，不改变单项规则。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0310"></a>

## ST-LC-0310 — 在 RPN 前计算全局AP采样计数

操作：Compute；需求：REQ-LC-0018, REQ-LC-0022, REQ-LC-0033

资源：RES-LC-0310

当前位置：[code.rdl L582](code.rdl)

```spacerdl
Compute APSampleCountNext ActionWorking ReqCapByFormTable FormulaTable.IncrementAPSample;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 uint32 数据 APSampleCountNext，供后继条件或 Set 使用；不替换工作快照。

规则：

- 读前驱当前快照/已写回 LC_AppData.APSampleCount，按源码声明的计数整数类型执行加一；输出新计数，不假定无溢出或饱和；其余状态不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L102–106 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0311"></a>

## ST-LC-0311 — 在 RPN 前写回全局AP采样计数

操作：Set；需求：REQ-LC-0018, REQ-LC-0022, REQ-LC-0033

资源：RES-LC-0311

当前位置：[code.rdl L584](code.rdl)

```spacerdl
Set PersistentAPSampleCount APSampleCountNext;
```

输入绑定：输入为已定义 APSampleCountNext；常量由 declared_values 定义，计算值必须由本次已执行的前驱操作生成。

输出绑定：持久绑定 LC_AppData.APSampleCount，仅此成员写回；后续工作快照读取此新值，不重置同AP其他统计或应用/WP状态。 ActionWorking中的对应成员是该持久目标的别名：本Set写回同时刷新该别名，供下一Compute使用；别名绑定是项目数据合同、官方格式仍待确认。

规则：

- 在流程出现的位置赋 APSampleCountNext 至 LC_AppData.APSampleCount；保留其他成员。
- 这是状态赋值，不是服务成功证据；同一 Set 可在互斥分支复用，不重复执行。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L102–106 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0312"></a>

## ST-LC-0312 — 为当前 AP 初始化有界RPN求值栈

操作：Compute；需求：REQ-LC-0018, REQ-LC-0019, REQ-LC-0021, REQ-LC-0022

资源：RES-LC-0312

当前位置：[code.rdl L586](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.BeginRPN;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。 本次输出明确包含IllegalRPN=false及同步RPNIllegal=false，作为ST0313/While及其后ST8052条件的已初始化来源；ST0321仅刷新而非首次定义此boolean。

规则：

- 清本AP临时RPN栈/StackPtr=0、RPNEquationPtr=0、IllegalRPN=false、IllegalOperand=false、Done=false、EvalResult=LC_ACTION_ERROR。
- ST0312按lc_action.c L310–314在每AP求值开始把工作成员IllegalRPN=false，并同步平坦boolean别名RPNIllegal=false；此初值在While之前已产生。即使While零次执行，后继If RPNIllegal仍有明确值；ST0321每token末尾再从最新IllegalRPN刷新该别名。
- 持久ART.ActionResult仍为前次值；先完成RPN再写本次结果；最大token数来自 LC_MAX_RPN_EQU_SIZE。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L297–319 LC_EvaluateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0313"></a>

## ST-LC-0313 — 计算RPN循环继续条件

操作：Compute；需求：REQ-LC-0019, REQ-LC-0021

资源：RES-LC-0313

当前位置：[code.rdl L588](code.rdl), [code.rdl L622](code.rdl)

```spacerdl
Compute RPNContinue ActionWorking ReqCapByFormTable FormulaTable.RPNContinue;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 RPNContinue，供后继条件或 Set 使用；不替换工作快照。

规则：

- Done=false且IllegalRPN=false且IllegalOperand=false时TRUE；初始与每个token末尾重算。token游标每轮增加，最多LC_MAX_RPN_EQU_SIZE轮。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L319–325 LC_EvaluateRPN

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L448–454 LC_EvaluateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0314"></a>

## ST-LC-0314 — 取一个RPN token并前进token游标

操作：Compute；需求：REQ-LC-0019, REQ-LC-0021

资源：RES-LC-0314

当前位置：[code.rdl L591](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.FetchRPNToken;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 读取ADTPtr[apIndex].RPNEquation[RPNEquationPtr]，随后RPNEquationPtr递增1；不读取超过冻结方程buffer。
- 仅分类为AND/OR/XOR/NOT/EQUAL或WP索引候选；flat boolean从当前token派生，非扩展语言表达式。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L325–337 LC_EvaluateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0315"></a>

## ST-LC-0315 — 独立执行四值AND与栈效果

操作：Compute；需求：REQ-LC-0019, REQ-LC-0021

资源：RES-LC-0315

当前位置：[code.rdl L594](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.EvaluateRPNAnd;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 按POP_RPN_DATA先弹Operand2再Operand1；任一空栈置IllegalRPN，不把无效操作数当正常。
- 合法操作数优先级为FALSE、ERROR、STALE、TRUE；依此产生一个WP结果压栈，其他状态不变。
- IllegalRPN标记保留至终结；最终ERROR不能被本算子遮蔽。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L337–356 LC_EvaluateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0316"></a>

## ST-LC-0316 — 独立执行四值OR与栈效果

操作：Compute；需求：REQ-LC-0019, REQ-LC-0021

资源：RES-LC-0316

当前位置：[code.rdl L598](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.EvaluateRPNOr;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 先弹Operand2再Operand1，空栈标记IllegalRPN；合法输入优先级TRUE、ERROR、STALE、FALSE。
- 产一个WP结果压栈；ERROR可被合法TRUE遮蔽，但非法栈结构不能被遮蔽。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L358–377 LC_EvaluateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0317"></a>

## ST-LC-0317 — 独立执行四值XOR与栈效果

操作：Compute；需求：REQ-LC-0019, REQ-LC-0021

资源：RES-LC-0317

当前位置：[code.rdl L602](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.EvaluateRPNXor;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 弹两个操作数，空栈标记IllegalRPN；ERROR优先，其次STALE，否则两布尔操作数不等为TRUE、相等为FALSE。
- 压一个结果；未定义输入不能伪装TRUE/FALSE。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L379–394 LC_EvaluateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0318"></a>

## ST-LC-0318 — 独立执行四值NOT与栈效果

操作：Compute；需求：REQ-LC-0019, REQ-LC-0021

资源：RES-LC-0318

当前位置：[code.rdl L606](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.EvaluateRPNNot;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 弹一个操作数，空栈标记IllegalRPN；ERROR原样ERROR、STALE原样STALE，FALSE变TRUE、TRUE变FALSE。
- 压一个结果，未改变持久WRT/ART。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L396–410 LC_EvaluateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0319"></a>

## ST-LC-0319 — 核对EQUAL终结而非二元相等比较

操作：Compute；需求：REQ-LC-0019, REQ-LC-0021

资源：RES-LC-0319

当前位置：[code.rdl L610](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.TerminateRPNEqual;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- EQUAL弹一个最终WP结果到EvalResult；空栈置IllegalRPN。
- 最终结果ERROR或STALE时置IllegalOperand停止；否则弹出后StackPtr==0才Done=true，不空则IllegalRPN=true。
- EQUAL不是两个值相等比较；遇EQUAL终止后不读其后填充token。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L412–426 LC_EvaluateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0320"></a>

## ST-LC-0320 — 取当前WRT结果作为WP操作数或标记非法token

操作：Compute；需求：REQ-LC-0019, REQ-LC-0021, REQ-LC-0081

资源：RES-LC-0320

当前位置：[code.rdl L613](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.PushRPNWatchOperand;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 非五种算子的token若<LC_MAX_WATCHPOINTS则取当前持久WRT对应WatchResult入栈；保持ERROR/STALE四值。
- 超出WP容量的token置IllegalRPN；容量合法不等于另一WDT已定义该WP，不增造跨表有效性检查。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L428–441 LC_EvaluateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0321"></a>

## ST-LC-0321 — 在token后检查方程buffer界限

操作：Compute；需求：REQ-LC-0019, REQ-LC-0021

资源：RES-LC-0321

当前位置：[code.rdl L620](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.CheckRPNBufferEnd;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 仅Done/IllegalRPN/IllegalOperand均false时，若RPNEquationPtr>=LC_MAX_RPN_EQU_SIZE置IllegalRPN；否则允许下轮。
- 循环内Fetch严格推进游标，每轮到有限上界或EQUAL/错误结束；不虚构周期限制。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L445–454 LC_EvaluateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0322"></a>

## ST-LC-0322 — 登记非法RPN详细错误事件

操作：Compute；需求：REQ-LC-0019, REQ-LC-0021, REQ-LC-0033, REQ-LC-0068

资源：RES-LC-0322

当前位置：[code.rdl L626](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.InvalidRPNEvent;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- IllegalRPN=true时追加LC_INVALID_RPN_ERR_EID ERROR待提交描述，含AP、RPNEquationPtr-1、StackPtr。
- 此事件位于ART结果写回与AP ERROR事件之前；不会增加ART.CumulativeEventMsgsSent。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L458–467 LC_EvaluateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0323"></a>

## ST-LC-0323 — 将最终WP四值映射成AP结果

操作：Compute；需求：REQ-LC-0019, REQ-LC-0021, REQ-LC-0022, REQ-LC-0033, REQ-LC-0068

资源：RES-LC-0323

当前位置：[code.rdl L629](code.rdl)

```spacerdl
Compute SelectedAPResult ActionWorking ReqCapByFormTable FormulaTable.MapRPNResult;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 AP result 数据 SelectedAPResult，供后继条件或 Set 使用；不替换工作快照。

规则：

- IllegalRPN优先映射AP ERROR；否则最终WP ERROR->AP ERROR，STALE->AP STALE，FALSE->AP PASS，TRUE->AP FAIL。
- WRT ERROR可在合法AND FALSE/OR TRUE中被遮蔽；只看最终式结果，不能遇一个ERROR就直接判整AP ERROR。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L458–484 LC_EvaluateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0324"></a>

## ST-LC-0324 — 在分支判断前持久保存本次AP结果

操作：Set；需求：REQ-LC-0018, REQ-LC-0021, REQ-LC-0022, REQ-LC-0033, REQ-LC-0068

资源：RES-LC-0324

当前位置：[code.rdl L631](code.rdl)

```spacerdl
Set PersistentAPResult SelectedAPResult;
```

输入绑定：输入为已定义 SelectedAPResult；常量由 declared_values 定义，计算值必须由本次已执行的前驱操作生成。

输出绑定：持久绑定 LC_OperData.ARTPtr[apIndex].ActionResult，仅此成员写回；后续工作快照读取此新值，不重置同AP其他统计或应用/WP状态。 ActionWorking中的对应成员是该持久目标的别名：本Set写回同时刷新该别名，供下一Compute使用；别名绑定是项目数据合同、官方格式仍待确认。

规则：

- 在流程出现的位置赋 SelectedAPResult 至 LC_OperData.ARTPtr[apIndex].ActionResult；保留其他成员。
- 这是状态赋值，不是服务成功证据；同一 Set 可在互斥分支复用，不重复执行。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L106–108 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0325"></a>

## ST-LC-0325 — 判定本AP是否FAIL

操作：Compute；需求：REQ-LC-0023, REQ-LC-0027, REQ-LC-0029, REQ-LC-0033

资源：RES-LC-0325

当前位置：[code.rdl L633](code.rdl)

```spacerdl
Compute APResultFail ActionWorking ReqCapByFormTable FormulaTable.APResultFail;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 APResultFail，供后继条件或 Set 使用；不替换工作快照。

规则：

- SelectedAPResult==LC_ACTION_FAIL；取已生成并写回本次结果，不读previousResult。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L113–116 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0326"></a>

## ST-LC-0326 — 计算当前AP连续FAIL计数

操作：Compute；需求：REQ-LC-0027, REQ-LC-0029, REQ-LC-0033, REQ-LC-0068

资源：RES-LC-0326

当前位置：[code.rdl L636](code.rdl)

```spacerdl
Compute ConsecutiveFailNext ActionWorking ReqCapByFormTable FormulaTable.IncrementConsecutiveFail;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 uint32 数据 ConsecutiveFailNext，供后继条件或 Set 使用；不替换工作快照。

规则：

- 读前驱当前快照/已写回 LC_OperData.ARTPtr[apIndex].ConsecutiveFailCount，按源码声明的计数整数类型执行加一；输出新计数，不假定无溢出或饱和；其余状态不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L115–115 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0327"></a>

## ST-LC-0327 — 写回当前AP连续FAIL计数

操作：Set；需求：REQ-LC-0027, REQ-LC-0029, REQ-LC-0033, REQ-LC-0068

资源：RES-LC-0327

当前位置：[code.rdl L638](code.rdl)

```spacerdl
Set PersistentConsecutiveFail ConsecutiveFailNext;
```

输入绑定：输入为已定义 ConsecutiveFailNext；常量由 declared_values 定义，计算值必须由本次已执行的前驱操作生成。

输出绑定：持久绑定 LC_OperData.ARTPtr[apIndex].ConsecutiveFailCount，仅此成员写回；后续工作快照读取此新值，不重置同AP其他统计或应用/WP状态。 ActionWorking中的对应成员是该持久目标的别名：本Set写回同时刷新该别名，供下一Compute使用；别名绑定是项目数据合同、官方格式仍待确认。

规则：

- 在流程出现的位置赋 ConsecutiveFailNext 至 LC_OperData.ARTPtr[apIndex].ConsecutiveFailCount；保留其他成员。
- 这是状态赋值，不是服务成功证据；同一 Set 可在互斥分支复用，不重复执行。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L115–115 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0328"></a>

## ST-LC-0328 — 计算当前AP累计FAIL计数

操作：Compute；需求：REQ-LC-0027, REQ-LC-0033

资源：RES-LC-0328

当前位置：[code.rdl L640](code.rdl)

```spacerdl
Compute CumulativeFailNext ActionWorking ReqCapByFormTable FormulaTable.IncrementCumulativeFail;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 uint32 数据 CumulativeFailNext，供后继条件或 Set 使用；不替换工作快照。

规则：

- 读前驱当前快照/已写回 LC_OperData.ARTPtr[apIndex].CumulativeFailCount，按源码声明的计数整数类型执行加一；输出新计数，不假定无溢出或饱和；其余状态不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L116–116 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0329"></a>

## ST-LC-0329 — 写回当前AP累计FAIL计数

操作：Set；需求：REQ-LC-0027, REQ-LC-0033

资源：RES-LC-0329

当前位置：[code.rdl L642](code.rdl)

```spacerdl
Set PersistentCumulativeFail CumulativeFailNext;
```

输入绑定：输入为已定义 CumulativeFailNext；常量由 declared_values 定义，计算值必须由本次已执行的前驱操作生成。

输出绑定：持久绑定 LC_OperData.ARTPtr[apIndex].CumulativeFailCount，仅此成员写回；后续工作快照读取此新值，不重置同AP其他统计或应用/WP状态。 ActionWorking中的对应成员是该持久目标的别名：本Set写回同时刷新该别名，供下一Compute使用；别名绑定是项目数据合同、官方格式仍待确认。

规则：

- 在流程出现的位置赋 CumulativeFailNext 至 LC_OperData.ARTPtr[apIndex].CumulativeFailCount；保留其他成员。
- 这是状态赋值，不是服务成功证据；同一 Set 可在互斥分支复用，不重复执行。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L116–116 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0330"></a>

## ST-LC-0330 — 判定PASS到FAIL转换

操作：Compute；需求：REQ-LC-0023, REQ-LC-0024, REQ-LC-0033

资源：RES-LC-0330

当前位置：[code.rdl L644](code.rdl)

```spacerdl
Compute PreviousAPPass ActionWorking ReqCapByFormTable FormulaTable.PreviousAPPass;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 PreviousAPPass，供后继条件或 Set 使用；不替换工作快照。

规则：

- 本次FAIL分支内，previousResult==LC_ACTION_PASS时TRUE；STALE/ERROR到FAIL不算该转换。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L118–128 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0331"></a>

## ST-LC-0331 — 计算PASS到FAIL转换数

操作：Compute；需求：REQ-LC-0023, REQ-LC-0024, REQ-LC-0033

资源：RES-LC-0331

当前位置：[code.rdl L647](code.rdl)

```spacerdl
Compute PassToFailNext ActionWorking ReqCapByFormTable FormulaTable.IncrementPassToFail;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 uint32 数据 PassToFailNext，供后继条件或 Set 使用；不替换工作快照。

规则：

- 读前驱当前快照/已写回 LC_OperData.ARTPtr[apIndex].PassToFailCount，按源码声明的计数整数类型执行加一；输出新计数，不假定无溢出或饱和；其余状态不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L123–128 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0332"></a>

## ST-LC-0332 — 写回PASS到FAIL转换数

操作：Set；需求：REQ-LC-0023, REQ-LC-0024, REQ-LC-0033

资源：RES-LC-0332

当前位置：[code.rdl L649](code.rdl)

```spacerdl
Set PersistentPassToFail PassToFailNext;
```

输入绑定：输入为已定义 PassToFailNext；常量由 declared_values 定义，计算值必须由本次已执行的前驱操作生成。

输出绑定：持久绑定 LC_OperData.ARTPtr[apIndex].PassToFailCount，仅此成员写回；后续工作快照读取此新值，不重置同AP其他统计或应用/WP状态。 ActionWorking中的对应成员是该持久目标的别名：本Set写回同时刷新该别名，供下一Compute使用；别名绑定是项目数据合同、官方格式仍待确认。

规则：

- 在流程出现的位置赋 PassToFailNext 至 LC_OperData.ARTPtr[apIndex].PassToFailCount；保留其他成员。
- 这是状态赋值，不是服务成功证据；同一 Set 可在互斥分支复用，不重复执行。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L123–128 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0333"></a>

## ST-LC-0333 — 核定PASS到FAIL事件限额

操作：Compute；需求：REQ-LC-0023, REQ-LC-0024, REQ-LC-0033

资源：RES-LC-0333

当前位置：[code.rdl L651](code.rdl)

```spacerdl
Compute PassFailEventAllowed ActionWorking ReqCapByFormTable FormulaTable.PassFailEventAllowed;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 PassFailEventAllowed，供后继条件或 Set 使用；不替换工作快照。

规则：

- 刚写回的PassToFailCount<=ADT.MaxPassFailEvents时TRUE；最大值0禁止首个转换事件，转换计数依然增加。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L128–135 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0334"></a>

## ST-LC-0334 — 登记限额内PASS到FAIL事件

操作：Compute；需求：REQ-LC-0023, REQ-LC-0024, REQ-LC-0033

资源：RES-LC-0334

当前位置：[code.rdl L654](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.PassToFailEvent;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 仅许可分支追加LC_AP_PASSTOFAIL_INF_EID INFORMATION效果，含AP；下个独立操作再计算/写回事件计数。
- 真实EVS调用pending-interface，不声明EVS发送成功。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L130–134 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0335"></a>

## ST-LC-0335 — 在计数口径内事件效果之后计算ART事件计数

操作：Compute；需求：REQ-LC-0023, REQ-LC-0024, REQ-LC-0025, REQ-LC-0026, REQ-LC-0027, REQ-LC-0029, REQ-LC-0033

资源：RES-LC-0335

当前位置：[code.rdl L656](code.rdl), [code.rdl L689](code.rdl), [code.rdl L715](code.rdl), [code.rdl L741](code.rdl)

```spacerdl
Compute CountedEventNext ActionWorking ReqCapByFormTable FormulaTable.IncrementCountedEvent;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 uint32 数据 CountedEventNext，供后继条件或 Set 使用；不替换工作快照。

规则：

- 读前驱当前快照/已写回 LC_OperData.ARTPtr[apIndex].CumulativeEventMsgsSent，按源码声明的计数整数类型执行加一；输出新计数，不假定无溢出或饱和；其余状态不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L130–135 LC_SampleSingleAP

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L173–180 LC_SampleSingleAP

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L212–218 LC_SampleSingleAP

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L243–247 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0336"></a>

## ST-LC-0336 — 写回计数口径内ART事件计数

操作：Set；需求：REQ-LC-0023, REQ-LC-0024, REQ-LC-0025, REQ-LC-0026, REQ-LC-0027, REQ-LC-0029, REQ-LC-0033

资源：RES-LC-0336

当前位置：[code.rdl L658](code.rdl), [code.rdl L691](code.rdl), [code.rdl L717](code.rdl), [code.rdl L743](code.rdl)

```spacerdl
Set PersistentCountedEvent CountedEventNext;
```

输入绑定：输入为已定义 CountedEventNext；常量由 declared_values 定义，计算值必须由本次已执行的前驱操作生成。

输出绑定：持久绑定 LC_OperData.ARTPtr[apIndex].CumulativeEventMsgsSent，仅此成员写回；后续工作快照读取此新值，不重置同AP其他统计或应用/WP状态。 ActionWorking中的对应成员是该持久目标的别名：本Set写回同时刷新该别名，供下一Compute使用；别名绑定是项目数据合同、官方格式仍待确认。

规则：

- 在流程出现的位置赋 CountedEventNext 至 LC_OperData.ARTPtr[apIndex].CumulativeEventMsgsSent；保留其他成员。
- 这是状态赋值，不是服务成功证据；同一 Set 可在互斥分支复用，不重复执行。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L134–134 LC_SampleSingleAP

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L180–180 LC_SampleSingleAP

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L218–218 LC_SampleSingleAP

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L247–247 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0337"></a>

## ST-LC-0337 — 用本次新增后的连续FAIL核定阈值

操作：Compute；需求：REQ-LC-0027, REQ-LC-0028, REQ-LC-0029, REQ-LC-0033, REQ-LC-0070

资源：RES-LC-0337

当前位置：[code.rdl L662](code.rdl)

```spacerdl
Compute FailThresholdReached ActionWorking ReqCapByFormTable FormulaTable.FailThresholdReached;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 FailThresholdReached，供后继条件或 Set 使用；不替换工作快照。

规则：

- 刚写回ConsecutiveFailCount>=ADT.MaxFailsBeforeRTS时TRUE；不是大于号、不是累计FAIL阈值；FALSE不生成RTS或被动动作事件。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L138–143 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0338"></a>

## ST-LC-0338 — 区分达到阈值时AP原ACTIVE或PASSIVE

操作：Compute；需求：REQ-LC-0027, REQ-LC-0028, REQ-LC-0029, REQ-LC-0070

资源：RES-LC-0338

当前位置：[code.rdl L665](code.rdl)

```spacerdl
Compute OriginalAPActive ActionWorking ReqCapByFormTable FormulaTable.OriginalAPActive;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 OriginalAPActive，供后继条件或 Set 使用；不替换工作快照。

规则：

- 取LoadSelectedAP保存originalAPState==LC_APSTATE_ACTIVE；该值不因后续ART状态转PASSIVE而改写。FALSE在合法求值分支意味着原AP PASSIVE。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L143–148 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0339"></a>

## ST-LC-0339 — 实现视图在请求许可判断前将ACTIVE AP转PASSIVE

操作：Set；需求：REQ-LC-0022, REQ-LC-0027, REQ-LC-0028, REQ-LC-0033, REQ-LC-0070

资源：RES-LC-0339

当前位置：[code.rdl L668](code.rdl)

```spacerdl
Set PersistentAPState ActionPassiveValue;
```

输入绑定：输入为已定义 ActionPassiveValue；常量由 declared_values 定义，计算值必须由本次已执行的前驱操作生成。

输出绑定：持久绑定 LC_OperData.ARTPtr[apIndex].CurrentState，仅此成员写回；后续工作快照读取此新值，不重置同AP其他统计或应用/WP状态。 ActionWorking中的对应成员是该持久目标的别名：本Set写回同时刷新该别名，供下一Compute使用；别名绑定是项目数据合同、官方格式仍待确认。

规则：

- 在流程出现的位置赋 ActionPassiveValue 至 LC_OperData.ARTPtr[apIndex].CurrentState；保留其他成员。
- 这是状态赋值，不是服务成功证据；同一 Set 可在互斥分支复用，不重复执行。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L143–150 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0340"></a>

## ST-LC-0340 — 核定应用ACTIVE才许可RTS请求

操作：Compute；需求：REQ-LC-0027, REQ-LC-0028, REQ-LC-0070, REQ-LC-0071

资源：RES-LC-0340

当前位置：[code.rdl L670](code.rdl)

```spacerdl
Compute ApplicationActiveForRTS ActionWorking ReqCapByFormTable FormulaTable.ApplicationActiveForRTS;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 ApplicationActiveForRTS，供后继条件或 Set 使用；不替换工作快照。

规则：

- 达到阈值且原AP ACTIVE且其状态已写PASSIVE之后，CurrentLCState==LC_STATE_ACTIVE为TRUE；合法PASSIVE为FALSE，DISABLED已在外入口阻止。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L148–160 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0341"></a>

## ST-LC-0341 — 按现有任务配置组装RTS请求描述

操作：Compute；需求：REQ-LC-0027, REQ-LC-0071

资源：RES-LC-0341

当前位置：[code.rdl L673](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.PrepareRTSRequest;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 本地请求快照按源码清零，MID=LC_RTS_REQ_MID、size=sizeof(LC_RTSRequestCmd_t)、FC=LC_RTS_REQ_CC、Payload.RTSId=当前ADT.RTSId。
- 这里只记录真实宏/API来源与字段意图，不猜实际MID数字、线格式大小、外部SC版本或成功回执。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_custom.c](<evidence/LC/fsw/src/lc_custom.c>)  L42–51 LC_ExecuteRTS

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0342"></a>

## ST-LC-0342 — 在允许路径登记RTS请求提交位置

操作：Compute；需求：REQ-LC-0027, REQ-LC-0028, REQ-LC-0033, REQ-LC-0071

资源：RES-LC-0342

当前位置：[code.rdl L675](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.AppendRTSRequestEffect;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 追加按PrepareRTSRequest产生包的 CFE_SB_TransmitMsg(...,true) 待提交描述；位置在AP转PASSIVE之后、请求计数之前。
- LC_ExecuteRTS返回void，忽略Transmit返回；本规约不将effects当实际发送/SC接收/执行成功，真实提交pending-interface。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_custom.c](<evidence/LC/fsw/src/lc_custom.c>)  L53–55 LC_ExecuteRTS

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L156–160 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0343"></a>

## ST-LC-0343 — 在RTS效果位置之后计算AP请求尝试数

操作：Compute；需求：REQ-LC-0027, REQ-LC-0033, REQ-LC-0071

资源：RES-LC-0343

当前位置：[code.rdl L677](code.rdl)

```spacerdl
Compute APRTSAttemptNext ActionWorking ReqCapByFormTable FormulaTable.IncrementAPRTSAttempt;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 uint32 数据 APRTSAttemptNext，供后继条件或 Set 使用；不替换工作快照。

规则：

- 读前驱当前快照/已写回 LC_OperData.ARTPtr[apIndex].CumulativeRTSExecCount，按源码声明的计数整数类型执行加一；输出新计数，不假定无溢出或饱和；其余状态不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L156–158 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0344"></a>

## ST-LC-0344 — 写回AP请求尝试数

操作：Set；需求：REQ-LC-0027, REQ-LC-0033, REQ-LC-0071

资源：RES-LC-0344

当前位置：[code.rdl L679](code.rdl)

```spacerdl
Set PersistentAPRTSAttempt APRTSAttemptNext;
```

输入绑定：输入为已定义 APRTSAttemptNext；常量由 declared_values 定义，计算值必须由本次已执行的前驱操作生成。

输出绑定：持久绑定 LC_OperData.ARTPtr[apIndex].CumulativeRTSExecCount，仅此成员写回；后续工作快照读取此新值，不重置同AP其他统计或应用/WP状态。 ActionWorking中的对应成员是该持久目标的别名：本Set写回同时刷新该别名，供下一Compute使用；别名绑定是项目数据合同、官方格式仍待确认。

规则：

- 在流程出现的位置赋 APRTSAttemptNext 至 LC_OperData.ARTPtr[apIndex].CumulativeRTSExecCount；保留其他成员。
- 这是状态赋值，不是服务成功证据；同一 Set 可在互斥分支复用，不重复执行。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L158–158 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0345"></a>

## ST-LC-0345 — 计算全局RTS请求尝试数

操作：Compute；需求：REQ-LC-0027, REQ-LC-0033, REQ-LC-0071

资源：RES-LC-0345

当前位置：[code.rdl L681](code.rdl)

```spacerdl
Compute GlobalRTSAttemptNext ActionWorking ReqCapByFormTable FormulaTable.IncrementGlobalRTSAttempt;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 uint32 数据 GlobalRTSAttemptNext，供后继条件或 Set 使用；不替换工作快照。

规则：

- 读前驱当前快照/已写回 LC_AppData.RTSExecCount，按源码声明的计数整数类型执行加一；输出新计数，不假定无溢出或饱和；其余状态不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L158–160 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0346"></a>

## ST-LC-0346 — 写回全局RTS请求尝试数

操作：Set；需求：REQ-LC-0027, REQ-LC-0033, REQ-LC-0071

资源：RES-LC-0346

当前位置：[code.rdl L683](code.rdl)

```spacerdl
Set PersistentGlobalRTSAttempt GlobalRTSAttemptNext;
```

输入绑定：输入为已定义 GlobalRTSAttemptNext；常量由 declared_values 定义，计算值必须由本次已执行的前驱操作生成。

输出绑定：持久绑定 LC_AppData.RTSExecCount，仅此成员写回；后续工作快照读取此新值，不重置同AP其他统计或应用/WP状态。 ActionWorking中的对应成员是该持久目标的别名：本Set写回同时刷新该别名，供下一Compute使用；别名绑定是项目数据合同、官方格式仍待确认。

规则：

- 在流程出现的位置赋 GlobalRTSAttemptNext 至 LC_AppData.RTSExecCount；保留其他成员。
- 这是状态赋值，不是服务成功证据；同一 Set 可在互斥分支复用，不重复执行。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L160–160 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0347"></a>

## ST-LC-0347 — 按源代码缓冲区构造表定义动作事件文本

操作：Compute；需求：REQ-LC-0027, REQ-LC-0033

资源：RES-LC-0347

当前位置：[code.rdl L685](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.PrepareActionEventText;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 按snprintf(EventText,CFE_MISSION_EVS_MAX_MESSAGE_LENGTH,"%s %s",ADT.EventText,LC_AP_EVENT_TAIL_STR)记录文本构造/截断规则。
- 事件格式绑定AP、当前连续FAIL数、RTSId；缓冲区大小用依赖宏，不捏造字符数或重写源代码格式语义。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L162–171 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0348"></a>

## ST-LC-0348 — 登记表定义RTS触发事件

操作：Compute；需求：REQ-LC-0027, REQ-LC-0033

资源：RES-LC-0348

当前位置：[code.rdl L687](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.ActionThresholdEvent;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 在两项RTS请求计数写回之后追加ADT.EventID、ADT.EventType与构造EventText的EVS效果，实参AP/连续FAIL数/RTSId。
- 后继IncrementCountedEvent/StoreCountedEvent才更新ART事件数；真实EVS发送pending-interface。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L173–180 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0349"></a>

## ST-LC-0349 — 计算全局被动RTS抑制次数

操作：Compute；需求：REQ-LC-0029, REQ-LC-0033, REQ-LC-0070

资源：RES-LC-0349

当前位置：[code.rdl L694](code.rdl), [code.rdl L706](code.rdl)

```spacerdl
Compute GlobalPassiveNext ActionWorking ReqCapByFormTable FormulaTable.IncrementGlobalPassive;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 uint32 数据 GlobalPassiveNext，供后继条件或 Set 使用；不替换工作快照。

规则：

- 读前驱当前快照/已写回 LC_AppData.PassiveRTSExecCount，按源码声明的计数整数类型执行加一；输出新计数，不假定无溢出或饱和；其余状态不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L189–196 LC_SampleSingleAP

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L204–205 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0350"></a>

## ST-LC-0350 — 写回全局被动RTS抑制次数

操作：Set；需求：REQ-LC-0029, REQ-LC-0033, REQ-LC-0070

资源：RES-LC-0350

当前位置：[code.rdl L696](code.rdl), [code.rdl L708](code.rdl)

```spacerdl
Set PersistentGlobalPassive GlobalPassiveNext;
```

输入绑定：输入为已定义 GlobalPassiveNext；常量由 declared_values 定义，计算值必须由本次已执行的前驱操作生成。

输出绑定：持久绑定 LC_AppData.PassiveRTSExecCount，仅此成员写回；后续工作快照读取此新值，不重置同AP其他统计或应用/WP状态。 ActionWorking中的对应成员是该持久目标的别名：本Set写回同时刷新该别名，供下一Compute使用；别名绑定是项目数据合同、官方格式仍待确认。

规则：

- 在流程出现的位置赋 GlobalPassiveNext 至 LC_AppData.PassiveRTSExecCount；保留其他成员。
- 这是状态赋值，不是服务成功证据；同一 Set 可在互斥分支复用，不重复执行。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L189–189 LC_SampleSingleAP

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L205–205 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0351"></a>

## ST-LC-0351 — 登记应用PASSIVE的DEBUG抑制事件

操作：Compute；需求：REQ-LC-0027, REQ-LC-0028, REQ-LC-0033, REQ-LC-0070

资源：RES-LC-0351

当前位置：[code.rdl L698](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.ApplicationPassiveEvent;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 应用非ACTIVE的合法PASSIVE分支中，原ACTIVE AP已改PASSIVE，全局PassiveRTSExecCount已增，追加LC_PASSIVE_FAIL_DBG_EID DEBUG效果。
- 本路径无RTS请求、无CumulativeRTSExecCount/RTSExecCount增长，也不增加该ART.CumulativeEventMsgsSent；不能用错误的总事件口径补修原代码。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L182–197 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0352"></a>

## ST-LC-0352 — 计算原PASSIVE AP的阈值失败抑制次数

操作：Compute；需求：REQ-LC-0029, REQ-LC-0033

资源：RES-LC-0352

当前位置：[code.rdl L702](code.rdl)

```spacerdl
Compute PassiveAPNext ActionWorking ReqCapByFormTable FormulaTable.IncrementPassiveAP;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 uint32 数据 PassiveAPNext，供后继条件或 Set 使用；不替换工作快照。

规则：

- 读前驱当前快照/已写回 LC_OperData.ARTPtr[apIndex].PassiveAPCount，按源码声明的计数整数类型执行加一；输出新计数，不假定无溢出或饱和；其余状态不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L199–210 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0353"></a>

## ST-LC-0353 — 写回原PASSIVE AP阈值抑制次数

操作：Set；需求：REQ-LC-0029, REQ-LC-0033

资源：RES-LC-0353

当前位置：[code.rdl L704](code.rdl)

```spacerdl
Set PersistentPassiveAP PassiveAPNext;
```

输入绑定：输入为已定义 PassiveAPNext；常量由 declared_values 定义，计算值必须由本次已执行的前驱操作生成。

输出绑定：持久绑定 LC_OperData.ARTPtr[apIndex].PassiveAPCount，仅此成员写回；后续工作快照读取此新值，不重置同AP其他统计或应用/WP状态。 ActionWorking中的对应成员是该持久目标的别名：本Set写回同时刷新该别名，供下一Compute使用；别名绑定是项目数据合同、官方格式仍待确认。

规则：

- 在流程出现的位置赋 PassiveAPNext 至 LC_OperData.ARTPtr[apIndex].PassiveAPCount；保留其他成员。
- 这是状态赋值，不是服务成功证据；同一 Set 可在互斥分支复用，不重复执行。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L204–204 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0354"></a>

## ST-LC-0354 — 核定实现中的被动AP事件限额

操作：Compute；需求：REQ-LC-0029, REQ-LC-0033

资源：RES-LC-0354

当前位置：[code.rdl L710](code.rdl)

```spacerdl
Compute PassiveAPEventAllowed ActionWorking ReqCapByFormTable FormulaTable.PassiveAPEventAllowed;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 PassiveAPEventAllowed，供后继条件或 Set 使用；不替换工作快照。

规则：

- 本次新PassiveAPCount<=ADT.MaxPassiveEvents时TRUE；FALSE仅禁止被动AP事件，PassiveAPCount和全局PassiveRTSExecCount仍增长。原LC3002.4未列该限额，保留差异。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L204–218 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0355"></a>

## ST-LC-0355 — 登记限额内原PASSIVE AP抑制事件

操作：Compute；需求：REQ-LC-0027, REQ-LC-0029, REQ-LC-0033

资源：RES-LC-0355

当前位置：[code.rdl L713](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.PassiveAPEvent;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 追加LC_AP_PASSIVE_FAIL_INF_EID INFORMATION待提交效果，含AP/连续FAIL数/RTSId；后继才更新ART事件计数。
- 本分支无RTS请求，AP原状态保持PASSIVE，无AP/global RTS请求计数增长。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L212–218 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0356"></a>

## ST-LC-0356 — 判定本AP是否PASS

操作：Compute；需求：REQ-LC-0020, REQ-LC-0025, REQ-LC-0026, REQ-LC-0033, REQ-LC-0068

资源：RES-LC-0356

当前位置：[code.rdl L726](code.rdl)

```spacerdl
Compute APResultPass ActionWorking ReqCapByFormTable FormulaTable.APResultPass;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 APResultPass，供后继条件或 Set 使用；不替换工作快照。

规则：

- SelectedAPResult==LC_ACTION_PASS；FAIL分支之后的互斥分支，ERROR/STALE不得当PASS。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L229–254 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0357"></a>

## ST-LC-0357 — 判定FAIL到PASS转换

操作：Compute；需求：REQ-LC-0025, REQ-LC-0026, REQ-LC-0033

资源：RES-LC-0357

当前位置：[code.rdl L729](code.rdl)

```spacerdl
Compute PreviousAPFail ActionWorking ReqCapByFormTable FormulaTable.PreviousAPFail;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 PreviousAPFail，供后继条件或 Set 使用；不替换工作快照。

规则：

- 本次PASS分支内previousResult==LC_ACTION_FAIL为TRUE；ERROR/STALE到PASS不算本转换。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L231–241 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0358"></a>

## ST-LC-0358 — 计算FAIL到PASS转换数

操作：Compute；需求：REQ-LC-0025, REQ-LC-0026, REQ-LC-0033

资源：RES-LC-0358

当前位置：[code.rdl L732](code.rdl)

```spacerdl
Compute FailToPassNext ActionWorking ReqCapByFormTable FormulaTable.IncrementFailToPass;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 uint32 数据 FailToPassNext，供后继条件或 Set 使用；不替换工作快照。

规则：

- 读前驱当前快照/已写回 LC_OperData.ARTPtr[apIndex].FailToPassCount，按源码声明的计数整数类型执行加一；输出新计数，不假定无溢出或饱和；其余状态不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L236–241 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0359"></a>

## ST-LC-0359 — 写回FAIL到PASS转换数

操作：Set；需求：REQ-LC-0025, REQ-LC-0026, REQ-LC-0033

资源：RES-LC-0359

当前位置：[code.rdl L734](code.rdl)

```spacerdl
Set PersistentFailToPass FailToPassNext;
```

输入绑定：输入为已定义 FailToPassNext；常量由 declared_values 定义，计算值必须由本次已执行的前驱操作生成。

输出绑定：持久绑定 LC_OperData.ARTPtr[apIndex].FailToPassCount，仅此成员写回；后续工作快照读取此新值，不重置同AP其他统计或应用/WP状态。 ActionWorking中的对应成员是该持久目标的别名：本Set写回同时刷新该别名，供下一Compute使用；别名绑定是项目数据合同、官方格式仍待确认。

规则：

- 在流程出现的位置赋 FailToPassNext 至 LC_OperData.ARTPtr[apIndex].FailToPassCount；保留其他成员。
- 这是状态赋值，不是服务成功证据；同一 Set 可在互斥分支复用，不重复执行。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L236–236 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0360"></a>

## ST-LC-0360 — 核定FAIL到PASS事件限额

操作：Compute；需求：REQ-LC-0025, REQ-LC-0026, REQ-LC-0033

资源：RES-LC-0360

当前位置：[code.rdl L736](code.rdl)

```spacerdl
Compute FailPassEventAllowed ActionWorking ReqCapByFormTable FormulaTable.FailPassEventAllowed;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 FailPassEventAllowed，供后继条件或 Set 使用；不替换工作快照。

规则：

- 新FailToPassCount<=ADT.MaxFailPassEvents为TRUE；最大值0无该事件，统计仍增。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L241–248 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0361"></a>

## ST-LC-0361 — 登记限额内FAIL到PASS恢复事件

操作：Compute；需求：REQ-LC-0025, REQ-LC-0026, REQ-LC-0033

资源：RES-LC-0361

当前位置：[code.rdl L739](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.FailToPassEvent;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 追加LC_AP_FAILTOPASS_INF_EID INFORMATION效果，随后独立计算/写回事件计数。
- 真实发送pending-interface；转换是否发事件不影响后继连续FAIL归零义务。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L243–247 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0362"></a>

## ST-LC-0362 — PASS或STALE分支独立清零连续FAIL

操作：Set；需求：REQ-LC-0020, REQ-LC-0025, REQ-LC-0033, REQ-LC-0068

资源：RES-LC-0362

当前位置：[code.rdl L747](code.rdl), [code.rdl L755](code.rdl)

```spacerdl
Set PersistentConsecutiveFail ActionZeroCount;
```

输入绑定：输入为已定义 ActionZeroCount；常量由 declared_values 定义，计算值必须由本次已执行的前驱操作生成。

输出绑定：持久绑定 LC_OperData.ARTPtr[apIndex].ConsecutiveFailCount，仅此成员写回；后续工作快照读取此新值，不重置同AP其他统计或应用/WP状态。 ActionWorking中的对应成员是该持久目标的别名：本Set写回同时刷新该别名，供下一Compute使用；别名绑定是项目数据合同、官方格式仍待确认。

规则：

- 在流程出现的位置赋 ActionZeroCount 至 LC_OperData.ARTPtr[apIndex].ConsecutiveFailCount；保留其他成员。
- 这是状态赋值，不是服务成功证据；同一 Set 可在互斥分支复用，不重复执行。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L250–264 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0363"></a>

## ST-LC-0363 — 判定本AP是否STALE

操作：Compute；需求：REQ-LC-0021, REQ-LC-0033, REQ-LC-0068

资源：RES-LC-0363

当前位置：[code.rdl L752](code.rdl)

```spacerdl
Compute APResultStale ActionWorking ReqCapByFormTable FormulaTable.APResultStale;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 APResultStale，供后继条件或 Set 使用；不替换工作快照。

规则：

- SelectedAPResult==LC_ACTION_STALE为TRUE；在非FAIL非PASS分支内，FALSE表示最终ERROR。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L259–276 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0364"></a>

## ST-LC-0364 — ERROR分支保留连续FAIL并登记AP错误事件

操作：Compute；需求：REQ-LC-0021, REQ-LC-0033, REQ-LC-0068

资源：RES-LC-0364

当前位置：[code.rdl L760](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.APErrorEvent;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 当前ART.ActionResult已写ERROR；连续FAIL、累计FAIL、转换、RTS统计保持；追加LC_ACTION_ERROR_ERR_EID ERROR待提交效果。
- 无RTS请求；不增加ART.CumulativeEventMsgsSent。若IllegalRPN先已产生详细非法方程效果，此AP ERROR效果在其后。
- ERROR后再FAIL可能继续前次连续计数；这一实现不证明业务连续性满足正式需求，保留ISSUE-LC-0017。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L266–276 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0365"></a>

## ST-LC-0365 — 记录本AP不满足动作条件时RTS禁止不变量

操作：Compute；需求：REQ-LC-0020, REQ-LC-0021, REQ-LC-0025, REQ-LC-0027, REQ-LC-0029, REQ-LC-0030, REQ-LC-0031, REQ-LC-0032, REQ-LC-0068

资源：RES-LC-0365

当前位置：[code.rdl L722](code.rdl), [code.rdl L749](code.rdl), [code.rdl L757](code.rdl), [code.rdl L762](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.NoRTSForCurrentResult;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 当前结果不是FAIL或本次新连续数未达阈值时，不追加RTS请求、不追加阈值触发/被动AP动作事件、不增加AP/global RTS计数或被动抑制计数。
- PASS/FAIL转换事件已按自己的限额处理；本无动作说明不取消已记录的转换或错误事件，也不虚构发送动作。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L113–138 LC_SampleSingleAP

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L229–276 LC_SampleSingleAP

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0366"></a>

## ST-LC-0366 — 完成当前AP后推进范围游标

操作：Compute；需求：REQ-LC-0018, REQ-LC-0022, REQ-LC-0030, REQ-LC-0069

资源：RES-LC-0366

当前位置：[code.rdl L771](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.AdvanceAPIndex;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 当前AP所有Set及effects顺序已完成后apIndex+=1；下轮重新HasSelectedAP并读取最新AppData/ART，保留其他AP统计。
- 有限合法inclusive范围，每轮严格推进，必在rangeEnd后结束；索引用足以表示容量末尾+1的项目工作游标，不声称改写原uint16循环的极端配置行为。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L57–59 LC_SampleAPs

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0367"></a>

## ST-LC-0367 — AP范围结束后独立核定减龄交接条件

操作：Compute；需求：REQ-LC-0018, REQ-LC-0064, REQ-LC-0069

资源：RES-LC-0367

当前位置：[code.rdl L782](code.rdl)

```spacerdl
Compute AgeHandoffAllowed ActionWorking ReqCapByFormTable FormulaTable.AgeHandoffAllowed;
```

输入绑定：显式读取当前ActionWorking及前驱已执行Set目标对应成员；输出本操作独立boolean/计数/AP结果，不改变工作快照。

输出绑定：定义平坦的 boolean 数据 AgeHandoffAllowed，供后继条件或 Set 使用；不替换工作快照。

规则：

- 源码入口未DISABLED且索引合法ValidSampleCmd=true且UpdateAge!=0为TRUE；首项拒绝整范围也可能TRUE。FALSE不推进任何WP年龄。
- TRUE/FALSE 均有后继，保持持久状态与工作快照不变。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L88–104 LC_SampleAPReq

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0368"></a>

## ST-LC-0368 — 在全部AP处理之后输出WP减龄交接快照

操作：Compute；需求：REQ-LC-0018, REQ-LC-0064, REQ-LC-0069

资源：RES-LC-0368

当前位置：[code.rdl L785](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.HandoffPostAPAge;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 仅AgeHandoffAllowed的TRUE分支产生待交接快照：包含原UpdateAge、ValidSampleCmd、最新持久ART/AppData和本次AP读取的WRT。
- 本操作不执行减龄、不把它合并进RPN或伪造时间单位；后继WP贡献负责全体CountdownToStale正值减一/到0置STALE及Set持久写回，必须在本AP范围之后接入。
- 这不是另一独立周期入口；准确交接仍需在总成中引用已定义WP操作，因此本组REQ0064保留明确remaining。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。
- 本轮总成已在本操作之后内联ST0253–0262续段；0253直接读取ActionWorking，不新增消息入口。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L88–104 LC_SampleAPReq

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0369"></a>

## ST-LC-0369 — 应用DISABLED时整个采样请求无业务动作

操作：Compute；需求：REQ-LC-0018, REQ-LC-0064

资源：RES-LC-0369

当前位置：[code.rdl L825](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.DisabledSamplePreserve;
```

输入绑定：显式读定义好的 ActionWorking 旧值：本入口上一已执行ProjectFlowContext操作同符号输出；从前驱Set实际持久目标绑定刷新其对应成员，If/While选择已执行路径后继续，不读取互斥分支未执行值。

输出绑定：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

规则：

- 保持AP/WP结果与全部计数，不检查范围、不发送范围/首项错误事件、不进行RPN、不请求RTS、不推进WP年龄。
- 只保留请求被忽略的工作诊断；不增加有效/错误地面命令计数或虚构错误事件。
- 除所列变更成员及有序待提交 effects 外，其余消息、ADT、WRT、ART、AppData、配置和阶段变量保持；unknown 标志原样传播，effects 不执行 cFE 服务。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L53–55 LC_SampleAPReq

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0370"></a>

## ST-LC-0370 — 从待验证ADT创建验证快照与平台上界

操作：Compute；需求：REQ-LC-0017, REQ-LC-0034, REQ-LC-0060, REQ-LC-0081

资源：RES-LC-0370

当前位置：[code.rdl L12](code.rdl)

```spacerdl
Compute ADTWorking PendingADTValidationInput ReqCapByFormTable FormulaTable.BeginADTValidation;
```

输入绑定：独立的cFE TBL表更新验证回调LC_ValidateADT(TableData)入口待绑定；输入为候选ADT而非已生效ADT；取LC_MAX_ACTIONPOINTS/LC_MAX_WATCHPOINTS/LC_MAX_RPN_EQU_SIZE/LC_MAX_VALID_ADT_RTSID符号配置。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- adtIndex=0，GoodCount/BadCount/UnusedCount=0，EntryResult=LC_ADTVAL_ERR_NONE，TableResult=CFE_SUCCESS，RPNIndex/StackDepthValue=0；effects空。
- 不更新活动ADT/WRT/ART，不确认加载生效或跨WDT一致性；entry状态pending-interface。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L494–628 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0371"></a>

## ST-LC-0371 — 判断ADT验证循环是否还有条目

操作：Compute；需求：REQ-LC-0017, REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0371

当前位置：[code.rdl L14](code.rdl), [code.rdl L83](code.rdl)

```spacerdl
Compute HasADTEntry ADTWorking ReqCapByFormTable FormulaTable.HasADTEntry;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：定义平坦boolean供后继If/While使用，持久状态与工作快照不变。

规则：

- adtIndex<LC_MAX_ACTIONPOINTS为TRUE；每轮末尾推进并重新计算，达到上界FALSE结束。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L518–518 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0372"></a>

## ST-LC-0372 — 读取一项ADT待验证字段

操作：Compute；需求：REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0372

当前位置：[code.rdl L17](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.LoadADTValidationEntry;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 取得当前DefaultState/RTSId/MaxFailsBeforeRTS/EventType/RPNEquation；保留上一步TableResult及三类计数。
- 源码EntryResult只在函数开始初始化，没有每轮归零；NOT_USED条目未赋新EntryResult，保留原值，不能隐藏原代码行为。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L520–526 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0373"></a>

## ST-LC-0373 — 单独记录ADT空闲定义项

操作：Compute；需求：REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0373

当前位置：[code.rdl L20](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.CountUnusedADTEntry;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 仅NOT_USED定义项UnusedCount++，GoodCount/BadCount不改；RTS/事件/阈值/RPN字段不检查。
- EntryResult保持源码原值，TableResult保留首错误；不使候选ADT生效。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L526–531 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0374"></a>

## ST-LC-0374 — 独立验证ADT默认状态

操作：Compute；需求：REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0374

当前位置：[code.rdl L23](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.ValidateADTDefaultState;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 使用项默认状态仅ACTIVE/PASSIVE/DISABLED/PERMOFF合法；不把LC应用状态枚举当AP状态。
- 非法时EntryResult=LC_ADTVAL_ERR_DEFSTATE，后继只计BadCount不检查更后字段；合法保持EntryResult等待后继检查。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L533–541 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0375"></a>

## ST-LC-0375 — 独立验证ADT RTS标识上界

操作：Compute；需求：REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0375

当前位置：[code.rdl L26](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.ValidateADTRTSId;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 仅RTSId>LC_MAX_VALID_ADT_RTSID拒绝并EntryResult=LC_ADTVAL_ERR_RTSID；RTSId==0没有额外源码拒绝，不能擅加下界1。
- 本检查仅在默认状态有效后执行；上界取平台宏，不猜实际任务SC容量。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L542–550 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0376"></a>

## ST-LC-0376 — 独立验证ADT连续失败阈值

操作：Compute；需求：REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0376

当前位置：[code.rdl L29](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.ValidateADTFailureLimit;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 仅MaxFailsBeforeRTS==0拒绝并EntryResult=LC_ADTVAL_ERR_FAILCNT；非0的uint16字段通过，未加虚构额外上限。
- 本检查仅在状态和RTS号通过后执行。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L551–558 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0377"></a>

## ST-LC-0377 — 独立验证ADT事件类型

操作：Compute；需求：REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0377

当前位置：[code.rdl L32](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.ValidateADTEventType;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 仅CFE_EVS_EventType_DEBUG/INFORMATION/ERROR/CRITICAL合法；非法EntryResult=LC_ADTVAL_ERR_EVTTYPE。
- 本检查仅在前3项通过后执行；有效后才进入RPN结构验证。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L559–567 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0378"></a>

## ST-LC-0378 — 初始化本ADT项的RPN结构验证

操作：Compute；需求：REQ-LC-0019, REQ-LC-0034, REQ-LC-0060, REQ-LC-0081

资源：RES-LC-0378

当前位置：[code.rdl L35](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.BeginRPNValidation;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- rpnValidationIndex=0、StackDepth=0、BufferItem=0、rpnValidationStop=false；本阶段只核对语法/索引容量，不计算WRT真值。
- 保留先前RPNIndex/StackDepthValue输出，只有本次失败才更新二者；不检查另表WDT是否已定义WP。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L635–660 LC_ValidateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0379"></a>

## ST-LC-0379 — 计算有界RPN结构循环条件

操作：Compute；需求：REQ-LC-0019, REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0379

当前位置：[code.rdl L37](code.rdl), [code.rdl L44](code.rdl)

```spacerdl
Compute RPNValidationContinue ADTWorking ReqCapByFormTable FormulaTable.RPNValidationContinue;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：定义平坦boolean供后继If/While使用，持久状态与工作快照不变。

规则：

- rpnValidationIndex<LC_MAX_RPN_EQU_SIZE且rpnValidationStop=false为TRUE；初始化及每次推进后重新计算。
- TRUE每轮仅读当前token，索引推进或明确停止；FALSE进入最终EQUAL/depth校验。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L660–707 LC_ValidateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0380"></a>

## ST-LC-0380 — 核定一个token的结构栈深效果

操作：Compute；需求：REQ-LC-0019, REQ-LC-0034, REQ-LC-0060, REQ-LC-0081

资源：RES-LC-0380

当前位置：[code.rdl L40](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.ValidateOneRPNToken;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 读取当前RPNPtr[rpnValidationIndex]为BufferItem；AND/OR/XOR使StackDepth减1，NOT深度不变；合法WP索引<LC_MAX_WATCHPOINTS使深度增1。
- EQUAL设置rpnValidationStop=true并立即停止，不检查尾随buffer；未知且超WP上界token立即停止。
- 非终结合法token处理后若StackDepth<=0则停止并最终失败；因此二元算子之前必须已有至少2栈项，NOT之前必须已有至少1项。
- 保留当前Index与Depth作为错误诊断；不声称跨表一致性由本容量检查保证。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L662–705 LC_ValidateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0381"></a>

## ST-LC-0381 — 推进RPN结构验证游标或保留停止位置

操作：Compute；需求：REQ-LC-0019, REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0381

当前位置：[code.rdl L42](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.AdvanceRPNValidationIndex;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 只有rpnValidationStop=false才rpnValidationIndex+=1；token导致break/EQUAL时保留当前索引，匹配源码诊断位置。
- 有限LC_MAX_RPN_EQU_SIZE上界，每轮增加索引或停止，循环必终止。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L660–707 LC_ValidateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0382"></a>

## ST-LC-0382 — 独立核定EQUAL及最终单项栈

操作：Compute；需求：REQ-LC-0019, REQ-LC-0034, REQ-LC-0060, REQ-LC-0081

资源：RES-LC-0382

当前位置：[code.rdl L47](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.FinalizeRPNValidation;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 仅BufferItem==LC_RPN_EQUAL且StackDepth==1成功：EntryResult=LC_ADTVAL_ERR_NONE。
- 其他情况EntryResult=LC_ADTVAL_ERR_RPN，并把RPNIndex/rpnValidationIndex及StackDepthValue/StackDepth写入错误诊断快照。
- 一个在有效WP容量内但WDT未定义的WP索引仍可能通过此校验；不擅加业务一致性保证。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L709–725 LC_ValidateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0383"></a>

## ST-LC-0383 — 单独累计有效ADT定义项

操作：Compute；需求：REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0383

当前位置：[code.rdl L50](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.CountGoodADTEntry;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 所有五项校验通过时GoodCount++；BadCount/UnusedCount不改；EntryResult已由RPN成功设为NONE。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L579–582 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0384"></a>

## ST-LC-0384 — 单独累计本条首个校验错误

操作：Compute；需求：REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0384

当前位置：[code.rdl L53](code.rdl), [code.rdl L57](code.rdl), [code.rdl L61](code.rdl), [code.rdl L65](code.rdl), [code.rdl L69](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.CountBadADTEntry;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 状态/RTS/非0失败阈值/事件类型/RPN任一按源码短路检查首次失败时BadCount++一次；不把一条多错项计成多个BadCount。
- 保留相应EntryResult及诊断字段，其他两类计数不改。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L533–583 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0385"></a>

## ST-LC-0385 — 判断是否需要本表唯一首错误详细事件

操作：Compute；需求：REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0385

当前位置：[code.rdl L73](code.rdl)

```spacerdl
Compute FirstADTError ADTWorking ReqCapByFormTable FormulaTable.FirstADTError;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：定义平坦boolean供后继If/While使用，持久状态与工作快照不变。

规则：

- EntryResult!=LC_ADTVAL_ERR_NONE且TableResult==CFE_SUCCESS时TRUE；FALSE不追加详细错误。
- NOT_USED之后可能保留前项EntryResult，但TableResult已锁存首错，因此不重复首错事件。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L588–612 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0386"></a>

## ST-LC-0386 — 登记ADT首错误详细事件

操作：Compute；需求：REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0386

当前位置：[code.rdl L76](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.ADTFirstErrorEvent;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- EntryResult==LC_ADTVAL_ERR_RPN时追加LC_ADTVAL_RPNERR_EID ERROR，含AP/index/depth。
- 其他错误追加LC_ADTVAL_ERR_EID ERROR，含AP/错误码/默认状态/RTS/失败阈值/事件类型。
- 全表最多一次详细首错效果；EVS实际提交pending-interface。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L590–610 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0387"></a>

## ST-LC-0387 — 锁存候选ADT表的首个错误返回码

操作：Compute；需求：REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0387

当前位置：[code.rdl L78](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.LatchADTFirstError;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 在首错误事件效果之后TableResult=EntryResult；后继条目不能覆盖首错误，即使后继通过或空闲。
- 此结果是验证返回意图，不是TBL已拒绝/激活/提交成功证明。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L612–612 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0388"></a>

## ST-LC-0388 — 推进候选ADT条目游标

操作：Compute；需求：REQ-LC-0017, REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0388

当前位置：[code.rdl L81](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.AdvanceADTIndex;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 完成本项短路校验/计数/首错处理后adtIndex+=1；重新HasADTEntry。
- variant=LC_MAX_ACTIONPOINTS-adtIndex，有限上界与严格推进保证终止；持久原工程定义表不改变。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L518–615 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0389"></a>

## ST-LC-0389 — 登记ADT验证三类计数汇总事件

操作：Compute；需求：REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0389

当前位置：[code.rdl L86](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.ADTSummaryEvent;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 循环结束无论表成功/失败均追加LC_ADTVAL_INF_EID INFORMATION效果，含GoodCount/BadCount/UnusedCount。
- 不能把“验证通过”汇总等同候选ADT激活，实际EVS/TBL仍pending-interface。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L620–625 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0390"></a>

## ST-LC-0390 — 输出候选ADT验证返回决定

操作：Compute；需求：REQ-LC-0034, REQ-LC-0060

资源：RES-LC-0390

当前位置：[code.rdl L88](code.rdl)

```spacerdl
Compute ADTWorking ADTWorking ReqCapByFormTable FormulaTable.ReturnADTValidationDecision;
```

输入绑定：显式读取并更新定义好的 ADTWorking；为本入口上一已执行步骤同符号输出，标量计算不替换快照。

输出绑定：显式读旧写新 ADTWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 保留TableResult=CFE_SUCCESS或锁存首错误，Good/Bad/Unused计数及有序effects作为验证输出快照。
- TableData回调返回/软件资源提交的官方语言绑定pending；本操作不替LC_ManageTables提交候选表。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L627–627 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0391"></a>

## ST-LC-0391 — 正式要求视图按请求逐项跳过不可采样AP

操作：Compute；需求：REQ-LC-0018, REQ-LC-0022, REQ-LC-0030, REQ-LC-0031, REQ-LC-0032, REQ-LC-0069

资源：RES-LC-0391

当前位置：[code.rdl L106](code.rdl)

```spacerdl
Compute DocumentaryWorking DocumentaryAPSelectionInput ReqCapByFormTable FormulaTable.DocumentaryRequestedAPs;
```

输入绑定：documentary-only独立义务视图，输入合法请求指定的AP集合及应用状态；不是替换code-derived运行流程。

输出绑定：显式输出DocumentaryWorking，保存正式请求选择义务与源码差异；不读取或改变ADTWorking/ActionWorking运行快照。

规则：

- 正式要求应用ACTIVE/PASSIVE处理请求指定AP；每项ACTIVE/PASSIVE可采样，DISABLED/UNUSED/PERMOFF仅跳过该项。
- 输出逐项 expectedSelection 与源码实际selection差异：首项NOT_USED/PERMOFF时原实现拒整范围，不能以实现流程证明LC3001/3004/3005全部覆盖；差异需ISSUE-LC-0015裁定。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L46–48 LC3001

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L57–59 LC3002

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L72–74 LC3003/4/5

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L41–75 LC_SampleAPs

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0392"></a>

## ST-LC-0392 — 正式要求视图在RTS已initiated条件下AP应转PASSIVE

操作：Set；需求：REQ-LC-0028, REQ-LC-0070

资源：RES-LC-0392

当前位置：[code.rdl L94](code.rdl)

```spacerdl
Set DocumentaryAPState DocumentaryAPPassive;
```

输入绑定：仅documentary义务入口已经给出RTS initiated成立的前提，输入由声明常量LC_APSTATE_PASSIVE编码提供；该前提的真实外部边界未定义，不绑定虚构回执。

输出绑定：documentary视图目标AP状态，表达原始条件性状态赋值义务；不是对原代码流程再执行一次状态修改。

规则：

- 原文Once an RTS is initiated后关联AP状态应PASSIVE；本Set只表达满足此前提的应然赋值。
- 原实现先转PASSIVE再按应用状态决定发送，应用PASSIVE未发送也转PASSIVE；真实initiated语义和发送失败策略仍pending-interpretation，不能与本Set合并成一致结论。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L68–68 LC3002.3.1

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L138–197 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0393"></a>

## ST-LC-0393 — 正式要求视图保留被动阈值失败事件义务

操作：Compute；需求：REQ-LC-0029

资源：RES-LC-0393

当前位置：[code.rdl L100](code.rdl)

```spacerdl
Compute DocumentaryWorking DocumentaryPassiveFailInput ReqCapByFormTable FormulaTable.DocumentaryPassiveFailureEvent;
```

输入绑定：documentary-only输入为AP PASSIVE且连续FAIL达到定义次数的案例；与实现限额分支独立，不额外执行。

输出绑定：显式读旧写新 DocumentaryWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 原LC3002.4要求生成动作未采取事件并增加Passive RTS Execution Counter；原文未写MaxPassiveEvents限额，输出原文应有事件义务描述。
- 实现分支即使超事件限额仍增两项抑制计数但不生成事件；原要求应受此限额还是实现需要修改必须裁定，不能把no-op false分支当原文全覆盖。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L69–71 LC3002.4

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L204–218 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0394"></a>

## ST-LC-0394 — 正式要求视图逐项保留ART统计口径

操作：Compute；需求：REQ-LC-0033, REQ-LC-0068, REQ-LC-0070, REQ-LC-0071

资源：RES-LC-0394

当前位置：[code.rdl L112](code.rdl)

```spacerdl
Compute DocumentaryWorking DocumentaryARTInput ReqCapByFormTable FormulaTable.DocumentaryARTStatistics;
```

输入绑定：正式统计义务与实现快照供只读对照；不执行原工程状态变更。

输出绑定：显式读旧写新 DocumentaryWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 输出八类义务对照：最近PASS/FAIL/ERROR/STALE结果、当前五值AP状态、FAIL->PASS数、PASS->FAIL数、连续FAIL数、累计FAIL数、RTS executions累计、total event messages sent。
- 实现的RTS累计为请求尝试，events不含应用PASSIVE DEBUG及AP ERROR/非法RPN事件；将这些actual口径明确列为差异，不擅补增真实计数。
- ERROR保留连续FAIL使下一FAIL接续此前计数；原“consecutive”对错误间隔与RTS executions/Total events含义pending-interpretation，不自行规定新的飞行算法。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L75–83 LC3006

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L82–281 LC_ValidateADT

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0395"></a>

## ST-LC-0395 — 保留WDT/ADT一致性的任务责任与边界

操作：Compute；需求：REQ-LC-0019, REQ-LC-0034, REQ-LC-0081

资源：RES-LC-0395

当前位置：[code.rdl L1036](code.rdl)

```spacerdl
Compute DocumentaryWorking CrossTableReviewInput ReqCapByFormTable FormulaTable.CrossTableConsistencyBoundary;
```

输入绑定：任务配置、WDT/ADT更新顺序与当前LC状态的审查快照；完整表更新生命周期由其他贡献负责。

输出绑定：显式读旧写新 DocumentaryWorking，后继If/While/Compute读取其新值；项目聚合格式非官方序列化，绑定待确认。

规则：

- 记录ADT方程WP索引容量检查不等于该WP在另一WDT已定义；两个表更新并非原子事务，LC不自动保证业务一致性。
- 文档任务可选择DISABLED后更新两表再启用，但这是候选任务策略，不是代码强制事务，本操作不生成禁用/更新命令或默认采用该策略。
- 要求实际任务提供一致表集合/更新策略；无法确认则pending-interpretation，现有独立校验与未受影响求值继续。
- 除所列变更成员及有序待提交 effects 外，其余输入表、持久ART/WRT/AppData及配置保持；unknown 标志传播；effects不执行TBL/EVS/SB软件服务。

[evidence/LC/docs/dox_src/cfs_lc.dox](<evidence/LC/docs/dox_src/cfs_lc.dox>)  L200–209 table update operation

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L685–697 LC_ValidateRPN

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0396"></a>

## ST-LC-0396 — 在AP范围调用返回后标记合法采样请求

操作：Compute；需求：REQ-LC-0018, REQ-LC-0064, REQ-LC-0069

资源：RES-LC-0396

当前位置：[code.rdl L780](code.rdl)

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.MarkValidSampleAfterAP;
```

输入绑定：显式读取完成AP循环或首项拒绝分支后的ActionWorking；仅rangeValid=true的分支调用。

输出绑定：显式就地写新ActionWorking，下一AgeHandoffAllowed读取此最新标志与UpdateAge。

规则：

- 在原LC_SampleAPs调用对应范围路径返回后ValidSampleCmd=true；包括首项NOT_USED/PERMOFF拒绝整范围的情况。
- 这是请求索引合法标志，不是AP均成功求值/RTS发送成功标志；其余ART/WRT/AppData/请求/配置/effects保持。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L65–74 LC_SampleAPReq

检查边界：独立业务义务；已选论文模板checked，不代表官方解析器或服务执行。完整规则见对应RES。

<a id="st-lc-0529"></a>

## ST-LC-0529 — 将相关监测数据接到状态与配置快照

操作：Compute；需求：REQ-LC-0009, REQ-LC-0080

资源：RES-LC-0529

当前位置：[code.rdl L1110](code.rdl)

```spacerdl
Compute LCIngressWorking529 LCMonitorEnvelope ReqCapByFormTable FormulaTable.BindIngress529;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 入参为刚接收的本条消息；读取当时实际LC_AppData、WRT、ART、定义表及配置，输出工作快照。状态是独立持久来源，不伪装成消息协议的payload。
- 将接收结果的BufPtr/MID/FcnCode/length/payload绑定WMonitorEntry；CommandContext.route及ExpectedLength对应当前实际结构sizeof，内部请求CommandIsGround=false。
- snapshot数据未取得时保持pending/unknown，不猜初值；该桥接是已有真实数据的组装，不新增业务行为。
- 桥接在长度门前只绑定原始消息头、payload字节及独立持久状态；不解引用typed payload。只有CommandLengthMatches=true后的原handler步骤才按源结构读取参数。

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L314–361 LC_AppPipe

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L270–454 LC_CheckMsgForWPs / LC_ProcessWP

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0531"></a>

## ST-LC-0531 — 将内部AP采样请求接到状态与配置快照

操作：Compute；需求：REQ-LC-0017, REQ-LC-0018, REQ-LC-0080

资源：RES-LC-0531

当前位置：[code.rdl L543](code.rdl)

```spacerdl
Compute LCIngressWorking531 LCSampleEnvelope ReqCapByFormTable FormulaTable.BindIngress531;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 入参为刚接收的本条消息；读取当时实际LC_AppData、WRT、ART、定义表及配置，输出工作快照。状态是独立持久来源，不伪装成消息协议的payload。
- 将接收结果的BufPtr/MID/FcnCode/length/payload绑定ActionInput0300；CommandContext.route及ExpectedLength对应当前实际结构sizeof，内部请求CommandIsGround=false。
- snapshot数据未取得时保持pending/unknown，不猜初值；该桥接是已有真实数据的组装，不新增业务行为。
- 桥接在长度门前只绑定原始消息头、payload字节及独立持久状态；不解引用typed payload。只有CommandLengthMatches=true后的原handler步骤才按源结构读取参数。

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L44–55 LC_SampleAPReq

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L332–337 LC_AppPipe

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0533"></a>

## ST-LC-0533 — 将内部HK请求接到状态与配置快照

操作：Compute；需求：REQ-LC-0050

资源：RES-LC-0533

当前位置：[code.rdl L184](code.rdl)

```spacerdl
Compute LCIngressWorking533 LCHKRequestEnvelope ReqCapByFormTable FormulaTable.BindIngress533;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 入参为刚接收的本条消息；读取当时实际LC_AppData、WRT、ART、定义表及配置，输出工作快照。状态是独立持久来源，不伪装成消息协议的payload。
- 将接收结果的BufPtr/MID/FcnCode/length/payload绑定HKContext；CommandContext.route及ExpectedLength对应当前实际结构sizeof，内部请求CommandIsGround=false。
- snapshot数据未取得时保持pending/unknown，不猜初值；该桥接是已有真实数据的组装，不新增业务行为。
- 桥接在长度门前只绑定原始消息头、payload字节及独立持久状态；不解引用typed payload。只有CommandLengthMatches=true后的原handler步骤才按源结构读取参数。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L136–145 LC8000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L114–260 LC_SendHkCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L140–253 LC_SendHkCmd

[evidence/LC/fsw/inc/lc_interface_cfg.h](<evidence/LC/fsw/inc/lc_interface_cfg.h>)  L89–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0535"></a>

## ST-LC-0535 — 将Noop地面命令接到状态与配置快照

操作：Compute；需求：REQ-LC-0001

资源：RES-LC-0535

当前位置：[code.rdl L343](code.rdl)

```spacerdl
Compute LCIngressWorking535 LCNoopEnvelope ReqCapByFormTable FormulaTable.BindIngress535;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 入参为刚接收的本条消息；读取当时实际LC_AppData、WRT、ART、定义表及配置，输出工作快照。状态是独立持久来源，不伪装成消息协议的payload。
- 将接收结果的BufPtr/MID/FcnCode/length/payload绑定CommandContext；CommandContext.route及ExpectedLength对应当前实际结构sizeof，内部请求CommandIsGround=false。
- snapshot数据未取得时保持pending/unknown，不猜初值；该桥接是已有真实数据的组装，不新增业务行为。
- 桥接在长度门前只绑定原始消息头、payload字节及独立持久状态；不解引用typed payload。只有CommandLengthMatches=true后的原handler步骤才按源结构读取参数。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L2–2 LC1000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L267–279 LC_NoopCmd

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L157–165 LC_NoopVerifyDispatch

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L11–11 LC1003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L267–293 LC_NoopCmd / LC_ResetCountersCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L317–345 LC_SetLCStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L460–468 LC_SetAPStateCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L90–90 LC4000

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L280–281 LC_CheckMsgForWPs

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L52–55 LC_SampleAPReq

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L150–197 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L91–91 LC4001

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L92–92 LC4002

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L102–102 LC4009

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L481–537 LC_SetAPPermOffCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L104–110 LC4010

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L544–611 LC_ResetAPStatsCmd / LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L111–117 LC4011

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L118–126 LC4012

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L619–691 LC_ResetWPStatsCmd / LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L127–135 LC4013

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0537"></a>

## ST-LC-0537 — 将ResetCounters地面命令接到状态与配置快照

操作：Compute；需求：REQ-LC-0002

资源：RES-LC-0537

当前位置：[code.rdl L451](code.rdl)

```spacerdl
Compute LCIngressWorking537 LCResetCountersEnvelope ReqCapByFormTable FormulaTable.BindIngress537;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 入参为刚接收的本条消息；读取当时实际LC_AppData、WRT、ART、定义表及配置，输出工作快照。状态是独立持久来源，不伪装成消息协议的payload。
- 将接收结果的BufPtr/MID/FcnCode/length/payload绑定CommandContext；CommandContext.route及ExpectedLength对应当前实际结构sizeof，内部请求CommandIsGround=false。
- snapshot数据未取得时保持pending/unknown，不猜初值；该桥接是已有真实数据的组装，不新增业务行为。
- 桥接在长度门前只绑定原始消息头、payload字节及独立持久状态；不解引用typed payload。只有CommandLengthMatches=true后的原handler步骤才按源结构读取参数。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L3–9 LC1001

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L287–310 LC_ResetCountersCmd / LC_ResetCounters

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L11–11 LC1003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L267–293 LC_NoopCmd / LC_ResetCountersCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L317–345 LC_SetLCStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L460–468 LC_SetAPStateCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L146–155 LC9000

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L187–216 LC_AppInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L991–1011 LC_LoadDefaultTables

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L301–310 LC_ResetCounters

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L173–173 LC9003

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L386–478 LC_TableInit

[evidence/LC/fsw/inc/lc_internal_cfg.h](<evidence/LC/fsw/inc/lc_internal_cfg.h>)  L88–102 LC_SAVE_TO_CDS

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L182–182 LC9004.2

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L438–478 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L874–881 LC_CreateTaskCDS

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0539"></a>

## ST-LC-0539 — 将SetLCState地面命令接到状态与配置快照

操作：Compute；需求：REQ-LC-0035, REQ-LC-0036, REQ-LC-0037

资源：RES-LC-0539

当前位置：[code.rdl L924](code.rdl)

```spacerdl
Compute LCIngressWorking539 LCSetStateEnvelope ReqCapByFormTable FormulaTable.BindIngress539;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 入参为刚接收的本条消息；读取当时实际LC_AppData、WRT、ART、定义表及配置，输出工作快照。状态是独立持久来源，不伪装成消息协议的payload。
- 将接收结果的BufPtr/MID/FcnCode/length/payload绑定CommandContext；CommandContext.route及ExpectedLength对应当前实际结构sizeof，内部请求CommandIsGround=false。
- snapshot数据未取得时保持pending/unknown，不猜初值；该桥接是已有真实数据的组装，不新增业务行为。
- 桥接在长度门前只绑定原始消息头、payload字节及独立持久状态；不解引用typed payload。只有CommandLengthMatches=true后的原handler步骤才按源结构读取参数。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L90–90 LC4000

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L317–345 LC_SetLCStateCmd

[evidence/LC/fsw/src/lc_watch.c](<evidence/LC/fsw/src/lc_watch.c>)  L280–281 LC_CheckMsgForWPs

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L52–55 LC_SampleAPReq

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L150–197 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L91–91 LC4001

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L92–92 LC4002

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0541"></a>

## ST-LC-0541 — 将SetAPState地面命令接到状态与配置快照

操作：Compute；需求：REQ-LC-0038, REQ-LC-0039, REQ-LC-0040, REQ-LC-0041, REQ-LC-0042, REQ-LC-0043

资源：RES-LC-0541

当前位置：[code.rdl L841](code.rdl)

```spacerdl
Compute LCIngressWorking541 LCSetAPStateEnvelope ReqCapByFormTable FormulaTable.BindIngress541;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 入参为刚接收的本条消息；读取当时实际LC_AppData、WRT、ART、定义表及配置，输出工作快照。状态是独立持久来源，不伪装成消息协议的payload。
- 将接收结果的BufPtr/MID/FcnCode/length/payload绑定CommandContext；CommandContext.route及ExpectedLength对应当前实际结构sizeof，内部请求CommandIsGround=false。
- snapshot数据未取得时保持pending/unknown，不猜初值；该桥接是已有真实数据的组装，不新增业务行为。
- 桥接在长度门前只绑定原始消息头、payload字节及独立持久状态；不解引用typed payload。只有CommandLengthMatches=true后的原handler步骤才按源结构读取参数。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L93–93 LC4003

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L353–474 LC_SetAPStateCmd

[evidence/LC/fsw/src/lc_action.c](<evidence/LC/fsw/src/lc_action.c>)  L89–108 LC_SampleSingleAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L94–94 LC4004

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L95–95 LC4005

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L96–96 LC4006

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L97–97 LC4007

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L98–101 LC4008

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0543"></a>

## ST-LC-0543 — 将SetAPPermOff地面命令接到状态与配置快照

操作：Compute；需求：REQ-LC-0044, REQ-LC-0045

资源：RES-LC-0543

当前位置：[code.rdl L380](code.rdl)

```spacerdl
Compute LCIngressWorking543 LCPermOffEnvelope ReqCapByFormTable FormulaTable.BindIngress543;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 入参为刚接收的本条消息；读取当时实际LC_AppData、WRT、ART、定义表及配置，输出工作快照。状态是独立持久来源，不伪装成消息协议的payload。
- 将接收结果的BufPtr/MID/FcnCode/length/payload绑定CommandContext；CommandContext.route及ExpectedLength对应当前实际结构sizeof，内部请求CommandIsGround=false。
- snapshot数据未取得时保持pending/unknown，不猜初值；该桥接是已有真实数据的组装，不新增业务行为。
- 桥接在长度门前只绑定原始消息头、payload字节及独立持久状态；不解引用typed payload。只有CommandLengthMatches=true后的原handler步骤才按源结构读取参数。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L102–102 LC4009

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L481–537 LC_SetAPPermOffCmd

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0545"></a>

## ST-LC-0545 — 将ResetAPStats或ResetWPStats地面命令接到状态与配置快照

操作：Compute；需求：REQ-LC-0046, REQ-LC-0047, REQ-LC-0048, REQ-LC-0049

资源：RES-LC-0545

当前位置：[code.rdl L482](code.rdl)

```spacerdl
Compute LCIngressWorking545 LCResetStatsEnvelope ReqCapByFormTable FormulaTable.BindIngress545;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 入参为刚接收的本条消息；读取当时实际LC_AppData、WRT、ART、定义表及配置，输出工作快照。状态是独立持久来源，不伪装成消息协议的payload。
- 将接收结果的BufPtr/MID/FcnCode/length/payload绑定CommandContext；CommandContext.route及ExpectedLength对应当前实际结构sizeof，内部请求CommandIsGround=false。
- snapshot数据未取得时保持pending/unknown，不猜初值；该桥接是已有真实数据的组装，不新增业务行为。
- 桥接在长度门前只绑定原始消息头、payload字节及独立持久状态；不解引用typed payload。只有CommandLengthMatches=true后的原handler步骤才按源结构读取参数。

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L104–110 LC4010

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L544–611 LC_ResetAPStatsCmd / LC_ResetResultsAP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L111–117 LC4011

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L118–126 LC4012

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L619–691 LC_ResetWPStatsCmd / LC_ResetResultsWP

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L127–135 LC4013

[evidence/LC/docs/lc_FunctionalRequirements.csv](<evidence/LC/docs/lc_FunctionalRequirements.csv>)  L12–12 LC1004

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L95–110 LC_VerifyMsgLength

[evidence/LC/fsw/src/lc_dispatch.c](<evidence/LC/fsw/src/lc_dispatch.c>)  L298–306 LC_AppProcessCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L335–342 LC_SetLCStateCmd

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L589–611 LC_ResetResultsAP

[evidence/LC/fsw/src/lc_cmds.c](<evidence/LC/fsw/src/lc_cmds.c>)  L664–691 LC_ResetResultsWP

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0547"></a>

## ST-LC-0547 — 检查注册LC事件服务实际返回

操作：Compute；需求：REQ-LC-0061, REQ-LC-0072

资源：RES-LC-0547

当前位置：[code.rdl L316](code.rdl)

```spacerdl
Compute LCInit547Succeeded LCInitializationResults ReqCapByFormTable FormulaTable.CheckInit547;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 仅当前阶段真实返回为CFE_SUCCESS时true；失败为false；结果未知不当作成功或已证实失败。FALSE不执行后续初始化。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L241–264 注册LC事件服务

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0549"></a>

## ST-LC-0549 — 检查建立LC共享消息管道及必需订阅实际返回

操作：Compute；需求：REQ-LC-0061, REQ-LC-0072, REQ-LC-0080

资源：RES-LC-0549

当前位置：[code.rdl L319](code.rdl)

```spacerdl
Compute LCInit549Succeeded LCInitializationResults ReqCapByFormTable FormulaTable.CheckInit549;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 仅当前阶段真实返回为CFE_SUCCESS时true；失败为false；结果未知不当作成功或已证实失败。FALSE不执行后续初始化。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L270–344 建立LC共享消息管道及必需订阅

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0551"></a>

## ST-LC-0551 — 检查注册LC定义表和结果表接口实际返回

操作：Compute；需求：REQ-LC-0055, REQ-LC-0056, REQ-LC-0061, REQ-LC-0072

资源：RES-LC-0551

当前位置：[code.rdl L322](code.rdl)

```spacerdl
Compute LCInit551Succeeded LCInitializationResults ReqCapByFormTable FormulaTable.CheckInit551;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 仅当前阶段真实返回为CFE_SUCCESS时true；失败为false；结果未知不当作成功或已证实失败。FALSE不执行后续初始化。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L528–771 注册LC定义表和结果表接口

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0553"></a>

## ST-LC-0553 — 将取得数据接入WWDTValidationEntry

操作：Compute；需求：REQ-LC-0006, REQ-LC-0010, REQ-LC-0011, REQ-LC-0015

资源：RES-LC-0553

当前位置：[code.rdl L1227](code.rdl)

```spacerdl
Compute WWDTValidationEntry LCWDTCallbackData ReqCapByFormTable FormulaTable.BindAcquisition553;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 读取刚取得的原TableData或服务结果；按照既有WWDTValidationEntry数据字典组装实际输入及当时持久状态，保留所有失败标志。
- 已有后继逐项验证/恢复/换表规则不改变；官方数据聚合格式仍pending，不凭组装结果覆盖未知状态。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L632–647 LC_ValidateWDT callback

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0555"></a>

## ST-LC-0555 — 将取得数据接入PendingADTValidationInput

操作：Compute；需求：REQ-LC-0017, REQ-LC-0019, REQ-LC-0034, REQ-LC-0081

资源：RES-LC-0555

当前位置：[code.rdl L10](code.rdl)

```spacerdl
Compute PendingADTValidationInput LCADTCallbackData ReqCapByFormTable FormulaTable.BindAcquisition555;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 读取刚取得的原TableData或服务结果；按照既有PendingADTValidationInput数据字典组装实际输入及当时持久状态，保留所有失败标志。
- 已有后继逐项验证/恢复/换表规则不改变；官方数据聚合格式仍pending，不凭组装结果覆盖未知状态。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L685–700 LC_ValidateADT callback

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0557"></a>

## ST-LC-0557 — 将取得数据接入MaintenanceContext

操作：Compute；需求：REQ-LC-0074, REQ-LC-0075

资源：RES-LC-0557

当前位置：[code.rdl L968](code.rdl)

```spacerdl
Compute MaintenanceContext LCTableMaintenanceResults ReqCapByFormTable FormulaTable.BindAcquisition557;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 读取刚取得的原TableData或服务结果；按照既有MaintenanceContext数据字典组装实际输入及当时持久状态，保留所有失败标志。
- 已有后继逐项验证/恢复/换表规则不改变；官方数据聚合格式仍pending，不凭组装结果覆盖未知状态。

[evidence/LC/fsw/src/lc_utils.c](<evidence/LC/fsw/src/lc_utils.c>)  L40–109 LC_ManageTables

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。

<a id="st-lc-0559"></a>

## ST-LC-0559 — 将取得数据接入InitContext

操作：Compute；需求：REQ-LC-0051, REQ-LC-0052, REQ-LC-0053, REQ-LC-0054, REQ-LC-0055, REQ-LC-0056, REQ-LC-0057, REQ-LC-0058, REQ-LC-0059, REQ-LC-0060, REQ-LC-0061, REQ-LC-0062, REQ-LC-0063, REQ-LC-0074, REQ-LC-0076

资源：RES-LC-0559

当前位置：[code.rdl L239](code.rdl)

```spacerdl
Compute InitContext LCResetRestorationResults ReqCapByFormTable FormulaTable.BindAcquisition559;
```

输入绑定：按下述规则读取原消息/状态/配置/实际返回，不推定部署未知值

输出绑定：按资源规则产生当前阶段值或提交行为；发送不等于交付/执行完成

规则：

- 读取刚取得的原TableData或服务结果；按照既有InitContext数据字典组装实际输入及当时持久状态，保留所有失败标志。
- 已有后继逐项验证/恢复/换表规则不改变；官方数据聚合格式仍pending，不凭组装结果覆盖未知状态。

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L350–524 LC_TableInit

[evidence/LC/fsw/src/lc_app.c](<evidence/LC/fsw/src/lc_app.c>)  L776–903 LC_InitCDSData

检查边界：论文表7语句形状；LC/cFE资源绑定pending，不声称物理端口/设备/官方执行。
