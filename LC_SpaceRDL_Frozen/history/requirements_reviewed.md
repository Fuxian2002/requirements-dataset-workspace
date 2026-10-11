# LC 需求盘点、规范化与补全

本文件由随包 data/ 目录生成；证据为固定 commit 的完整快照。编号与状态是本项目交付约定。

## REQ-LC-0001

**NASA 原始 ID**：LC1000

**来源类别**：documented

**原始文字/行为**：Upon receipt of a No-Op command, LC shall increment the LC Valid Command Counter and generate an event message.

**原始理由/补充说明**：Debug command to verify application is alive.  Heritage from LRO.

**规范化中文需求**：接受 No-Op 地面命令后，有效命令计数加一并发送说明 LC 存活的事件。

**触发/条件**：已完成长度验证的地面命令到达

**输入**：LC_NoopCmd_t（无业务负载）

**输出**：CmdCount_new、LC_NOOP_INF_EID INFORMATION事件

**状态与历史**：LC_AppData.CmdCount 为历史计数

**处理及约束**：只对有效长度的No-Op执行。<br>CmdCount_new=CmdCount_old+1；事件含编译版本宏。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L2–2 LC1000<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L267–279 LC_NoopCmd<br>[evidence/LC/fsw/src/lc_dispatch.c](evidence/LC/fsw/src/lc_dispatch.c) L157–165 LC_NoopVerifyDispatch

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0020<br>RES-LC-0025<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0501<br>RES-LC-0534<br>RES-LC-0535<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0001<br>ST-LC-0006<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0501<br>ST-LC-0534<br>ST-LC-0535<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0501<br>ST-LC-0534

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "有效No-op的CmdCount递增和提交",
    "operation_ids": [
      "ST-LC-0105",
      "ST-LC-0107"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "No-op版本事件的数据形成",
    "operation_ids": [
      "ST-LC-0106",
      "ST-LC-0501"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0501",
      "ST-LC-0534"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0002

**NASA 原始 ID**：LC1001

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Reset command, LC shall reset the following housekeeping variables to a value of zero:
a)	Valid Command Counter
b)	Command Rejected Counter
c)	Passive RTS Execution Counter
d)	Actionpoint Sample Count
e)	TLM Count
f)	RTS Execution Counter

**原始理由/补充说明**：Important for testing and on-orbit flight operations in order to start with a “clean slate”.  Heritage from LRO, SDO.

**规范化中文需求**：接受 Reset 命令后，把六项 housekeeping 计数清零。

**触发/条件**：已完成长度验证的地面命令到达

**输入**：LC_ResetCountersCmd_t

**输出**：六项新计数和LC_RESET_INF_EID事件

**状态与历史**：CmdCount、CmdErrCount、PassiveRTSExecCount、APSampleCount、MonitoredMsgCount、RTSExecCount

**处理及约束**：六项均设0；不重置应用状态/WRT/ART。<br>此专用重置行为与LC1003的统一有效计数加一义务需裁定优先级，保留两条原始要求。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L3–9 LC1001<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L287–310 LC_ResetCountersCmd / LC_ResetCounters

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0020<br>RES-LC-0026<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0108<br>RES-LC-0109<br>RES-LC-0501<br>RES-LC-0536<br>RES-LC-0537<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0001<br>ST-LC-0007<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0108<br>ST-LC-0109<br>ST-LC-0501<br>ST-LC-0536<br>ST-LC-0537<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8040<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0009

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：LC1001本条清零有直接实现；与LC1003不能通过改写原文消除冲突。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0501<br>ST-LC-0536

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "复位六项HK计数，不改模式和表",
    "operation_ids": [
      "ST-LC-0108",
      "ST-LC-0107"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "复位成功事件描述",
    "operation_ids": [
      "ST-LC-0106",
      "ST-LC-0501"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0501",
      "ST-LC-0536"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "LC1001清零最终ValidCommandCounter与LC1003所有有效命令加一相冲突；实现Reset不加一。",
    "operation_ids": [],
    "status": "pending-interpretation",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。<br>LC1001清零最终ValidCommandCounter与LC1003所有有效命令加一相冲突；实现Reset不加一。

## REQ-LC-0003

**NASA 原始 ID**：LC1002

**来源类别**：documented

**原始文字/行为**：For all LC commands, if the length contained in the message header is not equal to the expected length, LC shall reject the command and issue an event message.

**原始理由/补充说明**：Basic command verification in the event of  SEU or memory corruption.  Heritage from LRO, SDO.

**规范化中文需求**：所有 LC 命令头声明长度与预期长度不等时，拒绝执行并发送错误事件。

**触发/条件**：LC命令/内部请求在分发前长度核验

**输入**：消息头ActualLength、按消息类型/命令码确定ExpectedLength

**输出**：拒绝标志、长度错误事件；地面命令另加CmdErrCount

**状态与历史**：CmdErrCount

**处理及约束**：ActualLength!=ExpectedLength时不得调用业务处理入口。<br>默认分支HK/SampleAP内部请求长度错误仅发事件；其余长度错误加CmdErrCount。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L10–10 LC1002<br>[evidence/LC/fsw/src/lc_dispatch.c](evidence/LC/fsw/src/lc_dispatch.c) L40–114 LC_VerifyMsgLength<br>[evidence/LC/fsw/src/lc_dispatch.c](evidence/LC/fsw/src/lc_dispatch.c) L121–256 *VerifyDispatch

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0020<br>RES-LC-0025<br>RES-LC-0100<br>RES-LC-0101<br>RES-LC-0102<br>RES-LC-0103<br>RES-LC-0104<br>RES-LC-0107<br>RES-LC-0500<br>RES-LC-0702

**ST**：ST-LC-0001<br>ST-LC-0006<br>ST-LC-0100<br>ST-LC-0101<br>ST-LC-0102<br>ST-LC-0103<br>ST-LC-0104<br>ST-LC-0107<br>ST-LC-0500<br>ST-LC-8019<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：默认非 EDS 分发路径；EDS 分支差异见 code-derived 补充。正式长度拒绝义务在非EDS明确，EDS依赖外部EdsDispatch长度服务未运行。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0500

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "按实际结构大小校验长度、FALSE阻止业务负载",
    "operation_ids": [
      "ST-LC-0100",
      "ST-LC-0102"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "区分地面与内部长度拒绝计数并形成错误事件",
    "operation_ids": [
      "ST-LC-0101",
      "ST-LC-0103",
      "ST-LC-0104",
      "ST-LC-0107",
      "ST-LC-0500"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0500"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0004

**NASA 原始 ID**：LC1003

**来源类别**：documented

**原始文字/行为**：If LC accepts any command as valid, LC shall execute the command, increment the LC Valid Command Counter and issue an event message.

**原始理由/补充说明**：Operators require feedback on command execution.  Note that this only applies to “ground commands” (i.e. does not include requests that come from the scheduler).  Heritage from LRO, SDO.

**规范化中文需求**：接受任何有效地面命令，应执行命令、有效命令计数加一并发事件；调度器内部请求不在此计数范围。

**触发/条件**：已完成长度验证的地面命令到达

**输入**：已知命令码、有效参数

**输出**：业务结果、CmdCount_new、确认事件

**状态与历史**：有效命令计数与目标业务状态

**处理及约束**：保留“any command”原始义务。<br>NoOp/状态/统计命令成功分支增计数；ResetCountersCmd仅清零不加一。<br>需要确定Reset是否作为LC1001专门例外；不可在归一化时擅自删去any。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L11–11 LC1003<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L267–293 LC_NoopCmd / LC_ResetCountersCmd<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L317–345 LC_SetLCStateCmd<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L460–468 LC_SetAPStateCmd

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0020<br>RES-LC-0025<br>RES-LC-0101<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0108<br>RES-LC-0109<br>RES-LC-0120<br>RES-LC-0501<br>RES-LC-0702

**ST**：ST-LC-0001<br>ST-LC-0006<br>ST-LC-0101<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0108<br>ST-LC-0109<br>ST-LC-0120<br>ST-LC-0501<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8040<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0009

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：conflict

**检查层次**：static<br>manual

**人工语义核对**：同基线文字的统一加一规则与Reset实现存在例外；可能是专用重置优先级，需独立审查。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0501

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "普通有效地面命令执行后的计数/事件描述/提交",
    "operation_ids": [
      "ST-LC-0105",
      "ST-LC-0106",
      "ST-LC-0107",
      "ST-LC-0501"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "Reset通用接受规则和代码差异被显式形式化",
    "operation_ids": [
      "ST-LC-0109",
      "ST-LC-0108"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0501"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0005

**NASA 原始 ID**：LC1004

**来源类别**：documented

**原始文字/行为**：If LC rejects any command, LC shall abort the command execution, increment the LC Command Rejected Counter and issue an error event message.

**原始理由/补充说明**：Operators require feedback on command execution. Heritage from LRO, SDO.

**规范化中文需求**：拒绝 LC 地面命令时，停止该命令执行、拒绝计数加一并发错误事件。

**触发/条件**：无效长度/未知命令码/无效业务参数的地面命令

**输入**：命令头、负载、当前状态

**输出**：CmdErrCount_new、错误事件、业务状态不提交

**状态与历史**：CmdErrCount及业务状态

**处理及约束**：地面命令拒绝后不得产生所请求业务状态改变。<br>内部HK/SampleAP默认分支错误不加地面拒绝计数；正式原文all与理由中的ground范围需共同阅读。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L12–12 LC1004<br>[evidence/LC/fsw/src/lc_dispatch.c](evidence/LC/fsw/src/lc_dispatch.c) L95–110 LC_VerifyMsgLength<br>[evidence/LC/fsw/src/lc_dispatch.c](evidence/LC/fsw/src/lc_dispatch.c) L298–306 LC_AppProcessCmd<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L335–342 LC_SetLCStateCmd

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0020<br>RES-LC-0025<br>RES-LC-0100<br>RES-LC-0101<br>RES-LC-0102<br>RES-LC-0103<br>RES-LC-0104<br>RES-LC-0107<br>RES-LC-0110<br>RES-LC-0112<br>RES-LC-0113<br>RES-LC-0114<br>RES-LC-0118<br>RES-LC-0120<br>RES-LC-0122<br>RES-LC-0123<br>RES-LC-0126<br>RES-LC-0127<br>RES-LC-0500<br>RES-LC-0702

**ST**：ST-LC-0001<br>ST-LC-0006<br>ST-LC-0100<br>ST-LC-0101<br>ST-LC-0102<br>ST-LC-0103<br>ST-LC-0104<br>ST-LC-0107<br>ST-LC-0110<br>ST-LC-0112<br>ST-LC-0113<br>ST-LC-0114<br>ST-LC-0118<br>ST-LC-0120<br>ST-LC-0122<br>ST-LC-0123<br>ST-LC-0126<br>ST-LC-0127<br>ST-LC-0500<br>ST-LC-8019<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8076<br>ST-LC-8077<br>ST-LC-8078<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：默认非 EDS 分发路径；EDS 分支差异见 code-derived 补充。按正式需求理由的地面命令口径判断。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0500

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "拒绝命令停止执行、地面错误计数和错误事件描述",
    "operation_ids": [
      "ST-LC-0102",
      "ST-LC-0103",
      "ST-LC-0104",
      "ST-LC-0107",
      "ST-LC-0500"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0500"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0006

**NASA 原始 ID**：LC2000

**来源类别**：documented

**原始文字/行为**：The flight software shall monitor a maximum of <PLATFORM_DEFINED> Watchpoints.

**原始理由/补充说明**：Need to define a limit for defining data structures.  Heritage from LRO, SDO.

**规范化中文需求**：最多监测平台定义数量的 Watchpoint；平台值是容量，不是采样周期。

**触发/条件**：配置/构建及WDT使用

**输入**：LC_MAX_WATCHPOINTS、WDT/WRT

**输出**：有界Watchpoint目录/索引

**状态与历史**：WDT/WRT及链接数组容量

**处理及约束**：容量由平台配置定义；默认值与实际部署值分别记录。<br>所有Watchpoint遍历/校验按0..LC_MAX_WATCHPOINTS-1。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L13–13 LC2000<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L126–153 LC_CreateHashTable<br>[evidence/LC/fsw/src/lc_app.h](evidence/LC/fsw/src/lc_app.h) L171–172 LC_OperData_t

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0021<br>RES-LC-0033<br>RES-LC-0200<br>RES-LC-0203<br>RES-LC-0206<br>RES-LC-0231<br>RES-LC-0236<br>RES-LC-0237<br>RES-LC-0238<br>RES-LC-0251<br>RES-LC-0252<br>RES-LC-0255<br>RES-LC-0256<br>RES-LC-0262<br>RES-LC-0510<br>RES-LC-0552<br>RES-LC-0553<br>RES-LC-0702<br>RES-LC-0704

**ST**：ST-LC-0002<br>ST-LC-0014<br>ST-LC-0016<br>ST-LC-0200<br>ST-LC-0203<br>ST-LC-0206<br>ST-LC-0231<br>ST-LC-0236<br>ST-LC-0237<br>ST-LC-0238<br>ST-LC-0251<br>ST-LC-0252<br>ST-LC-0255<br>ST-LC-0256<br>ST-LC-0262<br>ST-LC-0510<br>ST-LC-0552<br>ST-LC-0553<br>ST-LC-8069<br>ST-LC-8070<br>ST-LC-8071<br>ST-LC-8072<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-8097<br>ST-LC-8098<br>ST-LC-8099<br>ST-LC-8113<br>ST-LC-8115<br>ST-LC-8116<br>ST-LC-8117<br>ST-LC-8122<br>ST-LC-8123<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：full

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：该原始条目的全部容量/算子/条件性计数义务已在资源规则及关联数据变换中保留；full仅评价此条语义，不表示完整系统可运行。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0510<br>ST-LC-0552

**附加字段 obligation_mapping**：full

**附加字段 obligations**：

```json
[
  {
    "description": "容量为平台LC_MAX_WATCHPOINTS，合法WP目录和全表循环有限",
    "operation_ids": [
      "ST-LC-0203",
      "ST-LC-0206",
      "ST-LC-0231",
      "ST-LC-0237",
      "ST-LC-0238",
      "ST-LC-0251",
      "ST-LC-0256",
      "ST-LC-0262"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 prior_mapping_scope**：保留旧人工full结论，其口径是局部数据变换；不表示本轮所有义务或完整系统已full

**附加字段 remaining**：部署平台值、活动目录、ABI/cFE资源加载pending-interface；不造固定周期。

## REQ-LC-0007

**NASA 原始 ID**：LC2001

**来源类别**：documented

**原始文字/行为**：For each Watchpoint specified in the Watchpoint Definition Table (WDT) LC shall specify an age value which indicates when the data becomes “stale”.

**原始理由/补充说明**：Need to provide a means of ensuring evaluated data is not stale.  Heritage from MMS.

**规范化中文需求**：WDT 每个 Watchpoint 有一个决定何时变为 STALE 的 age 参数。

**触发/条件**：WDT定义/加载

**输入**：WDT.ResultAgeWhenStale

**输出**：各WP时效阈值

**状态与历史**：WDT定义字段；WRT.CountdownToStale

**处理及约束**：阈值为平台/表指定；不捏造秒或毫秒单位。<br>当前实现以有效SampleAP请求且UpdateAge非零的次数计数；阈值0不递减。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L14–14 LC2001<br>[evidence/LC/config/default_lc_tblstruct.h](evidence/LC/config/default_lc_tblstruct.h) L105–113 LC_WDTEntry_t.ResultAgeWhenStale<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L409–452 LC_ProcessWP<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L88–104 LC_SampleAPReq

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0020<br>RES-LC-0022<br>RES-LC-0033<br>RES-LC-0034<br>RES-LC-0200<br>RES-LC-0213<br>RES-LC-0224<br>RES-LC-0226<br>RES-LC-0227<br>RES-LC-0230<br>RES-LC-0253<br>RES-LC-0254<br>RES-LC-0255<br>RES-LC-0256<br>RES-LC-0257<br>RES-LC-0258<br>RES-LC-0259<br>RES-LC-0260<br>RES-LC-0261<br>RES-LC-0262

**ST**：ST-LC-0001<br>ST-LC-0003<br>ST-LC-0014<br>ST-LC-0016<br>ST-LC-0017<br>ST-LC-0200<br>ST-LC-0213<br>ST-LC-0224<br>ST-LC-0226<br>ST-LC-0227<br>ST-LC-0230<br>ST-LC-0253<br>ST-LC-0254<br>ST-LC-0255<br>ST-LC-0256<br>ST-LC-0257<br>ST-LC-0258<br>ST-LC-0259<br>ST-LC-0260<br>ST-LC-0261<br>ST-LC-0262<br>ST-LC-8067<br>ST-LC-8068<br>ST-LC-8069<br>ST-LC-8070<br>ST-LC-8071<br>ST-LC-8072<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-8095<br>ST-LC-8096<br>ST-LC-8097<br>ST-LC-8098<br>ST-LC-8099<br>ST-LC-8107<br>ST-LC-8108<br>ST-LC-8110<br>ST-LC-8111<br>ST-LC-8112<br>ST-LC-8113<br>ST-LC-8115<br>ST-LC-8116<br>ST-LC-8117<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0005

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：age存在并有活动过期路径；阈值0、更新请求节奏需按字段说明理解，非墙钟计时。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "每WP age参数由活动WDT.ResultAgeWhenStale供TRUE/FALSE装载",
    "operation_ids": [
      "ST-LC-0224",
      "ST-LC-0226",
      "ST-LC-0230"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "次数age在有效UpdateAge请求末尾维护到零STALE",
    "operation_ids": [
      "ST-LC-0254",
      "ST-LC-0257",
      "ST-LC-0259",
      "ST-LC-0260",
      "ST-LC-0261"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "真实采样末尾续段/参数加载绑定",
    "operation_ids": [
      "ST-LC-0253"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：正式未给墙钟单位，不补秒/毫秒；真实UpdateAge节奏、部署值和接口pending。

## REQ-LC-0008

**NASA 原始 ID**：LC2002

**来源类别**：documented

**原始文字/行为**：For each Watchpoint specified in the Watchpoint Definition Table (WDT) LC shall maintain the age of the data.

**原始理由/补充说明**：Need to provide a means of ensuring evaluated data is not stale.  Heritage from MMS.

**规范化中文需求**：每个 WDT Watchpoint 的数据 age 应被维护。

**触发/条件**：TRUE/FALSE WP评估和有效带UpdateAge的SampleAP请求

**输入**：ResultAgeWhenStale、UpdateAge、旧CountdownToStale

**输出**：新CountdownToStale、可能的新STALE结果

**状态与历史**：每个WRT的倒计数；本次AP先取旧WP结果，之后递减

**处理及约束**：TRUE/FALSE评估重装倒计数；ERROR/STALE结果清0。<br>有效UpdateAge请求使所有正倒计数减一，到0设STALE。<br>正式age未指定单位；保存的是剩余有效请求次数，不是已过去时间或自接收起秒数。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L15–15 LC2002<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L409–452 LC_ProcessWP<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L60–104 LC_SampleAPReq

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0020<br>RES-LC-0022<br>RES-LC-0033<br>RES-LC-0034<br>RES-LC-0200<br>RES-LC-0211<br>RES-LC-0212<br>RES-LC-0213<br>RES-LC-0224<br>RES-LC-0226<br>RES-LC-0227<br>RES-LC-0230<br>RES-LC-0253<br>RES-LC-0254<br>RES-LC-0255<br>RES-LC-0256<br>RES-LC-0257<br>RES-LC-0258<br>RES-LC-0259<br>RES-LC-0260<br>RES-LC-0261<br>RES-LC-0262<br>RES-LC-0506<br>RES-LC-0702

**ST**：ST-LC-0001<br>ST-LC-0003<br>ST-LC-0014<br>ST-LC-0016<br>ST-LC-0017<br>ST-LC-0200<br>ST-LC-0211<br>ST-LC-0212<br>ST-LC-0213<br>ST-LC-0224<br>ST-LC-0226<br>ST-LC-0227<br>ST-LC-0230<br>ST-LC-0253<br>ST-LC-0254<br>ST-LC-0255<br>ST-LC-0256<br>ST-LC-0257<br>ST-LC-0258<br>ST-LC-0259<br>ST-LC-0260<br>ST-LC-0261<br>ST-LC-0262<br>ST-LC-0506<br>ST-LC-8067<br>ST-LC-8068<br>ST-LC-8069<br>ST-LC-8070<br>ST-LC-8071<br>ST-LC-8072<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-8095<br>ST-LC-8096<br>ST-LC-8097<br>ST-LC-8098<br>ST-LC-8099<br>ST-LC-8107<br>ST-LC-8108<br>ST-LC-8110<br>ST-LC-8111<br>ST-LC-8112<br>ST-LC-8113<br>ST-LC-8115<br>ST-LC-8116<br>ST-LC-8117<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0005

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：当前表字段提供次数定义，满足可审查的age解释；维护顺序是先AP评估再过期，不能改造成先过期。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0506

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "TRUE/FALSE重装age，ERROR/STALE清零但保持连续TRUE",
    "operation_ids": [
      "ST-LC-0224",
      "ST-LC-0226",
      "ST-LC-0227",
      "ST-LC-0230"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "检测错误ERROR并清age，不计比较次数",
    "operation_ids": [
      "ST-LC-0211",
      "ST-LC-0212",
      "ST-LC-0213",
      "ST-LC-0506"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "先所有AP求值，再所有正Countdown减一，到零STALE；旧0保持",
    "operation_ids": [
      "ST-LC-0253",
      "ST-LC-0254",
      "ST-LC-0256",
      "ST-LC-0257",
      "ST-LC-0258",
      "ST-LC-0259",
      "ST-LC-0260",
      "ST-LC-0261",
      "ST-LC-0262"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "绑定AP处理后的最新持久WRT",
    "operation_ids": [
      "ST-LC-0253"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：age是同次请求续段，不是新入口；原子字段/服务及类型加载pending。

## REQ-LC-0009

**NASA 原始 ID**：LC2003

**来源类别**：documented

**原始文字/行为**：Upon receipt of a message, LC shall compare the data in the message to the table-defined value using the table-defined comparison value and comparison operator for each data point defined in the Watchpoint Definition Table (WDT) if the LC Application State is one of the following:
a)	Active
b)	Passive

**原始理由/补充说明**：Telemetry Watchpoints shall be evaluated whenever the message (packet) containing the data to be examined is received.  If LC App is Disabled, LC does not process WDT or ADT.   Disabled state useful for making updates to LC tables (note that LC does not have to be disabled in order to make WDT or ADT updates, however, care must be taken to ensure the validity of the relationship between the 2 tables during updates). Note that individual Watchpoints can’t be disabled;  Individual Actionpoints can be disabled.  Note also that WDT can have unused entries.  Heritage from LRO (loosely SDO).

**规范化中文需求**：应用 ACTIVE/PASSIVE 时，相关消息到达立即触发 WDT 所列数据点比较。

**触发/条件**：被订阅监测消息到达；与SampleAP请求独立

**输入**：SB消息、MID、WDT偏移/类型/掩码/比较值/算子、应用状态

**输出**：相关WP结果、WRT统计、MonitoredMsgCount

**状态与历史**：CurrentLCState与旧WRT

**处理及约束**：仅处理MID匹配的全部使用中WP。<br>应用DISABLED不监测；不虚构固定周期。<br>先执行LC_WPOffsetValid的实际C长度/类型检查，只有返回true才取数与比较；被检查拒绝时写ERROR。极端偏移可能通过整数回绕绕过检查，不得概括为所有越界均先ERROR；见ISSUE-LC-0021。<br>相关监测消息依当前hash链逐WP更新WRT，整包完成后MonitoredMsgCount加一次；出口状态留给下一个独立采样入口，不自动评估AP。极端回绕不可推导路径见ISSUE0021。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L16–18 LC2003<br>[evidence/LC/fsw/src/lc_dispatch.c](evidence/LC/fsw/src/lc_dispatch.c) L314–361 LC_AppPipe<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L270–348 LC_CheckMsgForWPs<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L358–454 LC_ProcessWP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0021<br>RES-LC-0022<br>RES-LC-0033<br>RES-LC-0200<br>RES-LC-0201<br>RES-LC-0202<br>RES-LC-0203<br>RES-LC-0204<br>RES-LC-0205<br>RES-LC-0206<br>RES-LC-0207<br>RES-LC-0208<br>RES-LC-0209<br>RES-LC-0210<br>RES-LC-0214<br>RES-LC-0216<br>RES-LC-0217<br>RES-LC-0218<br>RES-LC-0219<br>RES-LC-0220<br>RES-LC-0230<br>RES-LC-0231<br>RES-LC-0232<br>RES-LC-0233<br>RES-LC-0234<br>RES-LC-0235<br>RES-LC-0263<br>RES-LC-0505<br>RES-LC-0507<br>RES-LC-0508<br>RES-LC-0528<br>RES-LC-0529<br>RES-LC-0700<br>RES-LC-0702

**ST**：ST-LC-0002<br>ST-LC-0003<br>ST-LC-0014<br>ST-LC-0016<br>ST-LC-0200<br>ST-LC-0201<br>ST-LC-0202<br>ST-LC-0203<br>ST-LC-0204<br>ST-LC-0205<br>ST-LC-0206<br>ST-LC-0207<br>ST-LC-0208<br>ST-LC-0209<br>ST-LC-0210<br>ST-LC-0214<br>ST-LC-0216<br>ST-LC-0217<br>ST-LC-0218<br>ST-LC-0219<br>ST-LC-0220<br>ST-LC-0230<br>ST-LC-0231<br>ST-LC-0232<br>ST-LC-0233<br>ST-LC-0234<br>ST-LC-0235<br>ST-LC-0263<br>ST-LC-0505<br>ST-LC-0507<br>ST-LC-0508<br>ST-LC-0528<br>ST-LC-0529<br>ST-LC-8103<br>ST-LC-8106<br>ST-LC-8110<br>ST-LC-8111<br>ST-LC-8112<br>ST-LC-8113<br>ST-LC-8114<br>ST-LC-8115<br>ST-LC-8116<br>ST-LC-8117<br>ST-LC-9010

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0012<br>ISSUE-LC-0021

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：非EDS活动路径支持；EDS分支无此监测路由，部署选择未知。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。 本轮补全：相关监测消息依当前hash链逐WP更新WRT，整包完成后MonitoredMsgCount加一次；出口状态留给下一个独立采样入口，不自动评估AP。极端回绕不可推导路径见ISSUE0021。 完整行为合同仍不构成官方事件/服务语法验收，mapping保持原评定。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0505<br>ST-LC-0507<br>ST-LC-0508<br>ST-LC-0528

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "正式ACTIVE/PASSIVE资格及独立消息触发",
    "operation_ids": [
      "ST-LC-0263",
      "ST-LC-0200"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "实现非DISABLED门、消息时刻和完整MID/hash关联WP顺序",
    "operation_ids": [
      "ST-LC-0201",
      "ST-LC-0202",
      "ST-LC-0203",
      "ST-LC-0204",
      "ST-LC-0206"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "逐WP偏移检查/风险识别、取数/掩码、标准或custom比较和提交",
    "operation_ids": [
      "ST-LC-0207",
      "ST-LC-0208",
      "ST-LC-0209",
      "ST-LC-0214",
      "ST-LC-0216",
      "ST-LC-0217",
      "ST-LC-0219",
      "ST-LC-0218",
      "ST-LC-0220",
      "ST-LC-0230",
      "ST-LC-0507",
      "ST-LC-0508"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "找到WP整包完成后计数一次，未匹配不计",
    "operation_ids": [
      "ST-LC-0205",
      "ST-LC-0232",
      "ST-LC-0233",
      "ST-LC-0234",
      "ST-LC-0235",
      "ST-LC-0505"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "非法枚举!=DISABLED和正式许可、EDS部署、风险访问不可推导",
    "operation_ids": [
      "ST-LC-0201",
      "ST-LC-0263",
      "ST-LC-0210"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：真实SB/EVS入口与持久资源绑定pending-interface，非EDS路由部署待确认；风险不改成安全拒绝。

## REQ-LC-0010

**NASA 原始 ID**：LC2003.1

**来源类别**：documented

**原始文字/行为**：LC shall support the following comparison values:
a)       =
b)       !=
c)       >
d)      >=
e)      <
f)        <=

**原始理由/补充说明**：Watchdog comparison values

**规范化中文需求**：Watchpoint 支持 =、!=、>、>=、<、<= 六种关系比较。

**触发/条件**：合法WP数据比较

**输入**：经类型/字节序/掩码归一化数据、ComparisonValue、OperatorID

**输出**：TRUE/FALSE或ERROR

**状态与历史**：旧WP状态用于统计，不改变比较定义

**处理及约束**：比较方向保持data operator tableValue。<br>有符号/无符号/浮点分别比较；未知算子为ERROR。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L19–25 LC2003.1<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L464–561 LC_OperatorCompare<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L564–778 LC_SignedCompare / LC_UnsignedCompare / LC_FloatCompare

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0021<br>RES-LC-0022<br>RES-LC-0033<br>RES-LC-0200<br>RES-LC-0216<br>RES-LC-0219<br>RES-LC-0244<br>RES-LC-0245<br>RES-LC-0508<br>RES-LC-0552<br>RES-LC-0553<br>RES-LC-0702<br>RES-LC-0704

**ST**：ST-LC-0002<br>ST-LC-0003<br>ST-LC-0014<br>ST-LC-0016<br>ST-LC-0200<br>ST-LC-0216<br>ST-LC-0219<br>ST-LC-0244<br>ST-LC-0245<br>ST-LC-0508<br>ST-LC-0552<br>ST-LC-0553<br>ST-LC-8106<br>ST-LC-8110<br>ST-LC-8111<br>ST-LC-8112<br>ST-LC-8113<br>ST-LC-8115<br>ST-LC-8116<br>ST-LC-8117<br>ST-LC-8120<br>ST-LC-8121<br>ST-LC-8122<br>ST-LC-8123<br>ST-LC-9010

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0508<br>ST-LC-0552

**附加字段 obligation_mapping**：full

**附加字段 obligations**：

```json
[
  {
    "description": "六关系方向data operator ComparisonValue，signed/unsigned/float分别解释",
    "operation_ids": [
      "ST-LC-0219",
      "ST-LC-0508"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "float EQ/NE实际配置容差，NaN ERROR，收到无穷继续比较",
    "operation_ids": [
      "ST-LC-0219",
      "ST-LC-0508"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "WDT六关系/custom算子范围校验",
    "operation_ids": [
      "ST-LC-0244",
      "ST-LC-0245"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：ABI/浮点容差/活动WDT输入绑定pending-interface，未运行官方解释器/LC。

## REQ-LC-0011

**NASA 原始 ID**：LC2003.2

**来源类别**：documented

**原始文字/行为**：If the WDT comparison operator specifies that a Custom Function shall be performed, LC shall apply the custom function to the data contained in the message.

**原始理由/补充说明**：Provides capability to do a calculation on the data instead of just a comparison.  Heritage from LRO (loosely SDO).

**规范化中文需求**：WDT 选择 Custom operator 时，将消息中的数据送给任务自定义函数。

**触发/条件**：WP已通过偏移和类型检查且OperatorID==LC_OPER_CUSTOM

**输入**：WatchIndex、MaskedWPData、完整消息、CustomFuncArgument

**输出**：自定义WP结果

**状态与历史**：WDT自定义参数及WRT

**处理及约束**：默认自定义钩子是交付示例，真实任务计算未给出。<br>结果参与统一WRT更新；不将default stub补造成飞行算法。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L26–26 LC2003.2<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L386–395 LC_ProcessWP<br>[evidence/LC/fsw/src/lc_custom.c](evidence/LC/fsw/src/lc_custom.c) L65–96 LC_CustomFunction

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0021<br>RES-LC-0022<br>RES-LC-0033<br>RES-LC-0200<br>RES-LC-0216<br>RES-LC-0217<br>RES-LC-0218<br>RES-LC-0220<br>RES-LC-0226<br>RES-LC-0244<br>RES-LC-0269<br>RES-LC-0507<br>RES-LC-0552<br>RES-LC-0553<br>RES-LC-0702<br>RES-LC-0704

**ST**：ST-LC-0002<br>ST-LC-0003<br>ST-LC-0014<br>ST-LC-0016<br>ST-LC-0200<br>ST-LC-0216<br>ST-LC-0217<br>ST-LC-0218<br>ST-LC-0220<br>ST-LC-0226<br>ST-LC-0244<br>ST-LC-0269<br>ST-LC-0507<br>ST-LC-0552<br>ST-LC-0553<br>ST-LC-8100<br>ST-LC-8106<br>ST-LC-8107<br>ST-LC-8108<br>ST-LC-8110<br>ST-LC-8111<br>ST-LC-8112<br>ST-LC-8113<br>ST-LC-8115<br>ST-LC-8116<br>ST-LC-8117<br>ST-LC-8120<br>ST-LC-8121<br>ST-LC-8122<br>ST-LC-8123

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0020

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：unknown

**检查层次**：static<br>manual

**人工语义核对**：调用机制存在；实际任务自定义函数规则取决于部署。默认实现不证明业务自定义计算完整。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0507<br>ST-LC-0552

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "CUSTOM选择后准备WatchIndex/MaskedWPData/完整BufPtr/CustomFuncArgument",
    "operation_ids": [
      "ST-LC-0217",
      "ST-LC-0216",
      "ST-LC-0269"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "冻结默认stub所有case/default发Unexpected且FALSE",
    "operation_ids": [
      "ST-LC-0218",
      "ST-LC-0220",
      "ST-LC-0226",
      "ST-LC-0507"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "任务custom运算规则和实际结果缺失，不能以stub证明完成",
    "operation_ids": [
      "ST-LC-0269"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "真实custom调用及EVS提交",
    "operation_ids": [
      "ST-LC-0218",
      "ST-LC-0269",
      "ST-LC-0507"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：ISSUE0020任务自定义算法待提供；documentary义务与默认stub事实并列，不补造算法。

## REQ-LC-0012

**NASA 原始 ID**：LC2003.3

**来源类别**：documented

**原始文字/行为**：If the comparison result for a Watchpoint results in a False, LC shall set the Number of Consecutive True values to zero.

**原始理由/补充说明**：Restarts the consecutive True values.  Heritage from LRO, SDO.

**规范化中文需求**：WP 比较结果为 FALSE 时，把该 WP 连续 TRUE 次数清零。

**触发/条件**：有效WP比较产生FALSE

**输入**：旧ConsecutiveTrueCount、新WP结果

**输出**：ConsecutiveTrueCount_new=0

**状态与历史**：单个WRT

**处理及约束**：仅FALSE分支此正式义务。<br>ERROR/STALE分支不清连续TRUE计数，另标code-derived补充，勿擅自归零。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L27–27 LC2003.3<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L429–452 LC_ProcessWP

**RES**：RES-LC-0001<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0022<br>RES-LC-0033<br>RES-LC-0200<br>RES-LC-0225<br>RES-LC-0226<br>RES-LC-0230

**ST**：ST-LC-0003<br>ST-LC-0014<br>ST-LC-0016<br>ST-LC-0200<br>ST-LC-0225<br>ST-LC-0226<br>ST-LC-0230<br>ST-LC-8107<br>ST-LC-8108<br>ST-LC-8110<br>ST-LC-8111<br>ST-LC-8112<br>ST-LC-8113<br>ST-LC-8115<br>ST-LC-8116<br>ST-LC-8117

**ISSUE**：ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：full

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：该原始条目的全部容量/算子/条件性计数义务已在资源规则及关联数据变换中保留；full仅评价此条语义，不表示完整系统可运行。

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 obligation_mapping**：full

**附加字段 obligations**：

```json
[
  {
    "description": "仅新FALSE时ConsecutiveTrueCount清零",
    "operation_ids": [
      "ST-LC-0225",
      "ST-LC-0226",
      "ST-LC-0230"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 prior_mapping_scope**：保留旧人工full结论，其口径是局部数据变换；不表示本轮所有义务或完整系统已full

**附加字段 remaining**：真实字段持久绑定与入口pending-interface；ERROR/STALE保持计数另由REQ0067记录。

## REQ-LC-0013

**NASA 原始 ID**：LC2003.4

**来源类别**：documented

**原始文字/行为**：If the Watchpoint cannot be evaluated, LC shall set the Watchpoint Results Table to ERROR for the erroneous Watchpoint.

**原始理由/补充说明**：Want to report that there was an erroneous watchpoint.  Heritage from LRO.

**规范化中文需求**：Watchpoint 无法评估时，将该项 WRT 结果置为 ERROR。

**触发/条件**：被代码检测到的偏移/类型错误、未知算子、数据NaN等评估错误；极端偏移回绕漏检另列问题

**输入**：SB长度、WDT类型/偏移/算子、数据

**输出**：已检测错误路径的WatchResult=ERROR、适用CountdownToStale=0及错误事件；回绕放行后结果不能确定

**状态与历史**：单个WRT及错误前统计

**处理及约束**：不能用FALSE替代错误。<br>数据抽取失败不继续比较；收到的浮点NaN为ERROR，收到的无穷按比较算子处理，不自动判ERROR。WDT中的浮点阈值则须有限且非NaN。<br>运行时实际判定是(Offset + NumOfDataBytes) > MsgLength，宽度来自sizeof(uint8/uint16/uint32/float)。未知类型或该C表达式为true时先调用适用的EVS错误事件服务，再写WatchResult=ERROR、CountdownToStale=0，返回false并跳过LC_ProcessWP；此拒绝路径不增加EvaluationCount。<br>源码将Offset和NumOfDataBytes声明为uint32，MsgLength声明为size_t；以下回绕例按uint32为32位无符号且加法未提升到更宽整数的C算术假设核对。common_types.h及目标编译环境未固定，需由ISSUE-LC-0004核定；size_t较宽不会使已经完成的uint32加法重新变宽。<br>在上述32位无符号算术假设下，offset=0xFFFFFFFF、width=2使和回绕为1；对length=186会放行。LC随后按原始大偏移形成数据指针，不能据此推断ERROR、比较结果、统计更新、事件或后续正常返回。<br>希望满足的安全条件是offset<=length且width<=length-offset，并拒绝所有不满足的跨度；这是待确认/待实现的安全要求，不是本基线已经实现的保护，本包不修改LC源码。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L28–28 LC2003.4<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L784–865 LC_WPOffsetValid<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L957–973 LC_GetSizedWPData<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L693–778 LC_FloatCompare

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0021<br>RES-LC-0022<br>RES-LC-0033<br>RES-LC-0200<br>RES-LC-0207<br>RES-LC-0208<br>RES-LC-0209<br>RES-LC-0210<br>RES-LC-0211<br>RES-LC-0212<br>RES-LC-0213<br>RES-LC-0215<br>RES-LC-0219<br>RES-LC-0220<br>RES-LC-0221<br>RES-LC-0222<br>RES-LC-0227<br>RES-LC-0235<br>RES-LC-0267<br>RES-LC-0268<br>RES-LC-0506<br>RES-LC-0508<br>RES-LC-0702

**ST**：ST-LC-0002<br>ST-LC-0003<br>ST-LC-0014<br>ST-LC-0016<br>ST-LC-0200<br>ST-LC-0207<br>ST-LC-0208<br>ST-LC-0209<br>ST-LC-0210<br>ST-LC-0211<br>ST-LC-0212<br>ST-LC-0213<br>ST-LC-0215<br>ST-LC-0219<br>ST-LC-0220<br>ST-LC-0221<br>ST-LC-0222<br>ST-LC-0227<br>ST-LC-0235<br>ST-LC-0267<br>ST-LC-0268<br>ST-LC-0506<br>ST-LC-0508<br>ST-LC-8101<br>ST-LC-8102<br>ST-LC-8106<br>ST-LC-8107<br>ST-LC-8108<br>ST-LC-8110<br>ST-LC-8111<br>ST-LC-8112<br>ST-LC-8113<br>ST-LC-8115<br>ST-LC-8116<br>ST-LC-8117<br>ST-LC-9010

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0021

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：conflict

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。 偏移专项复查：常规拒绝/比较错误分支支持正式ERROR义务；32位无符号加法回绕条件下存在偏移漏检，不能保证非法访问前进入ERROR分支，故实现证据标conflict。该判断来自静态C表达式与受控算术模型，未运行LC非法指针路径。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0506<br>ST-LC-0508

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "正式确认无法评估时目标ERROR而非FALSE",
    "operation_ids": [
      "ST-LC-0267",
      "ST-LC-0268"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "实现检测偏移/类型/抽取错误，事件位置→ERROR→age0，不计比较次数",
    "operation_ids": [
      "ST-LC-0207",
      "ST-LC-0208",
      "ST-LC-0211",
      "ST-LC-0212",
      "ST-LC-0213",
      "ST-LC-0215",
      "ST-LC-0506"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "提取成功后的NaN/非法算子ERROR仍计EvaluationCount且不清连续TRUE",
    "operation_ids": [
      "ST-LC-0219",
      "ST-LC-0220",
      "ST-LC-0221",
      "ST-LC-0222",
      "ST-LC-0227",
      "ST-LC-0508"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "uint32回绕放行后结果未知，不能声称原代码拒绝",
    "operation_ids": [
      "ST-LC-0209",
      "ST-LC-0210"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "全跨度安全要求待裁定，不静默替代原表达式",
    "operation_ids": [
      "ST-LC-0207",
      "ST-LC-0267"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：ISSUE0021/0004 ABI及风险指针行为待确认；documentaryERROR义务不是现码万能检错保证；接口pending。

## REQ-LC-0014

**NASA 原始 ID**：LC2004

**来源类别**：documented

**原始文字/行为**：For each Watchpoint, the flight software shall maintain the following statistics in the dump-only Watchpoint Results Table:
a)	The result of the last relational comparison (False, True, Error, or Stale)
b)	The number of times this Watchpoint has been compared
c)	The number of times this Watchpoint has crossed from the False to True result
d)	The number of consecutive times the comparison has yielded a True result
e)	The cumulative number of times the comparison has yielded a True result
f)	Most recent FALSE to TRUE transition value
g)	Most recent FALSE to TRUE transition timestamp
h)	Most recent TRUE to FALSE transition value
i)	Most recent TRUE to FALSE transition timestamp
j)	Most recent comparison age

**原始理由/补充说明**：Provides results for each evaluation of the WDT.  Heritage from LRO, SDO.

**规范化中文需求**：每个 WP 在 dump-only WRT 中保存结果及九类比较、连续、累计、跨越和age统计。

**触发/条件**：WP评估/age更新/重置

**输入**：旧WRT、当前结果/数据/时间戳、时效参数

**输出**：WatchResult、EvaluationCount、FalseToTrueCount、ConsecutiveTrueCount、CumulativeTrueCount、LastFalseToTrue、LastTrueToFalse、age

**状态与历史**：单个WRT历史

**处理及约束**：必须保留FALSE/TRUE/ERROR/STALE四值。<br>保存两向跨越值及时间戳；比较age由CountdownToStale表述。<br>正式FalseToTrue仅写FALSE→TRUE；实现也把previous STALE→TRUE算入FalseToTrueCount/最近跨越。<br>错误数据抽取/偏移路径不增加EvaluationCount；age实际是倒计数。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L29–39 LC2004<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L398–452 LC_ProcessWP<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L91–104 LC_SampleAPReq

**RES**：RES-LC-0001<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0022<br>RES-LC-0033<br>RES-LC-0200<br>RES-LC-0202<br>RES-LC-0212<br>RES-LC-0220<br>RES-LC-0221<br>RES-LC-0222<br>RES-LC-0223<br>RES-LC-0224<br>RES-LC-0225<br>RES-LC-0226<br>RES-LC-0227<br>RES-LC-0228<br>RES-LC-0229<br>RES-LC-0230<br>RES-LC-0257<br>RES-LC-0259<br>RES-LC-0261<br>RES-LC-0264<br>RES-LC-0265<br>RES-LC-0266

**ST**：ST-LC-0003<br>ST-LC-0014<br>ST-LC-0016<br>ST-LC-0200<br>ST-LC-0202<br>ST-LC-0212<br>ST-LC-0220<br>ST-LC-0221<br>ST-LC-0222<br>ST-LC-0223<br>ST-LC-0224<br>ST-LC-0225<br>ST-LC-0226<br>ST-LC-0227<br>ST-LC-0228<br>ST-LC-0229<br>ST-LC-0230<br>ST-LC-0257<br>ST-LC-0259<br>ST-LC-0261<br>ST-LC-0264<br>ST-LC-0265<br>ST-LC-0266<br>ST-LC-8067<br>ST-LC-8068<br>ST-LC-8069<br>ST-LC-8070<br>ST-LC-8071<br>ST-LC-8072<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-8095<br>ST-LC-8096<br>ST-LC-8097<br>ST-LC-8098<br>ST-LC-8099<br>ST-LC-8104<br>ST-LC-8105<br>ST-LC-8107<br>ST-LC-8108<br>ST-LC-8109<br>ST-LC-8110<br>ST-LC-8111<br>ST-LC-8112<br>ST-LC-8113<br>ST-LC-8115<br>ST-LC-8116<br>ST-LC-8117<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0006

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：conflict

**检查层次**：static<br>manual

**人工语义核对**：STALE初始化计入FALSE→TRUE与原文字面不同；统计口径需裁定，不能自动改原要求。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "a 保存最近四值FALSE/TRUE/ERROR/STALE",
    "operation_ids": [
      "ST-LC-0220",
      "ST-LC-0212",
      "ST-LC-0261"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "b 比较次数：提取成功的NaN也计，偏移/抽取拒绝不计",
    "operation_ids": [
      "ST-LC-0221",
      "ST-LC-0222"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "c 正式FALSE→TRUE次数与实现STALE→TRUE分别表达",
    "operation_ids": [
      "ST-LC-0264",
      "ST-LC-0265",
      "ST-LC-0266",
      "ST-LC-0228",
      "ST-LC-0229"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "d 连续TRUE：TRUE加1，FALSE清0，ERROR/STALE保持",
    "operation_ids": [
      "ST-LC-0224",
      "ST-LC-0226",
      "ST-LC-0227",
      "ST-LC-0230"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "e 累计TRUE仅TRUE加1",
    "operation_ids": [
      "ST-LC-0224",
      "ST-LC-0230"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "f 最近FALSE→TRUE值：正式字面与实现STALE跨越分离",
    "operation_ids": [
      "ST-LC-0265",
      "ST-LC-0229"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "g 最近FALSE→TRUE时刻：消息时间双0才用now",
    "operation_ids": [
      "ST-LC-0202",
      "ST-LC-0265",
      "ST-LC-0229"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "h 最近TRUE→FALSE值：正式字面与实现STALE跨越分离",
    "operation_ids": [
      "ST-LC-0265",
      "ST-LC-0229"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "i 最近TRUE→FALSE时刻；不造不存在的TrueToFalseCount",
    "operation_ids": [
      "ST-LC-0202",
      "ST-LC-0265",
      "ST-LC-0229"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "j age由表值重装并由有效采样末尾续段维护",
    "operation_ids": [
      "ST-LC-0224",
      "ST-LC-0226",
      "ST-LC-0227",
      "ST-LC-0230",
      "ST-LC-0257",
      "ST-LC-0259",
      "ST-LC-0261"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "dump-only WRT建立/真实提交由生命周期与软件接口适配",
    "operation_ids": [
      "ST-LC-0220",
      "ST-LC-0222",
      "ST-LC-0230"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：ISSUE0006 STALE跨越口径冲突不记全部full；dump-only资源建立与软件提交不是Compute完成。

## REQ-LC-0015

**NASA 原始 ID**：LC2005

**来源类别**：documented

**原始文字/行为**：Upon receipt of a table update indication, LC shall validate the Watchpoint Definition Table for the following:
a)	Valid operator
b)	Data size
c)	Message  ID

**原始理由/补充说明**：Valid the items that can be validated when an table is updated (some items cannot be valued until runtime).  Heritage from LRO.

**规范化中文需求**：WDT 更新时验证算子、数据大小和消息 ID。

**触发/条件**：cFE TBL提供待验证WDT；表更新管理

**输入**：新WDT所有条目

**输出**：校验结果、错误总数/事件、通过后可用表

**状态与历史**：旧活动WDT/WRT，cFE表管理状态

**处理及约束**：跳过DataType NOT_USED条目。<br>类型在支持清单，算子在六比较/custom，MID通过CFE_SB_IsValidMsgId。<br>浮点比较阈值额外排除NaN/无穷；LC_ValidateWDT完全不验证WatchpointOffset。运行时虽另有长度检查，其uint32加法可能回绕，不能认为WDT验证或运行检查保证所有偏移安全。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L40–43 LC2005<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L988–1134 LC_ValidateWDT<br>[evidence/LC/fsw/src/lc_utils.c](evidence/LC/fsw/src/lc_utils.c) L43–79 LC_ManageTables<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L613–688 LC_CreateDefinitionTables

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0027<br>RES-LC-0236<br>RES-LC-0237<br>RES-LC-0238<br>RES-LC-0239<br>RES-LC-0240<br>RES-LC-0241<br>RES-LC-0242<br>RES-LC-0243<br>RES-LC-0244<br>RES-LC-0245<br>RES-LC-0246<br>RES-LC-0247<br>RES-LC-0248<br>RES-LC-0249<br>RES-LC-0250<br>RES-LC-0251<br>RES-LC-0252<br>RES-LC-0509<br>RES-LC-0510<br>RES-LC-0552<br>RES-LC-0553<br>RES-LC-0702<br>RES-LC-0704

**ST**：ST-LC-0008<br>ST-LC-0236<br>ST-LC-0237<br>ST-LC-0238<br>ST-LC-0239<br>ST-LC-0240<br>ST-LC-0241<br>ST-LC-0242<br>ST-LC-0243<br>ST-LC-0244<br>ST-LC-0245<br>ST-LC-0246<br>ST-LC-0247<br>ST-LC-0248<br>ST-LC-0249<br>ST-LC-0250<br>ST-LC-0251<br>ST-LC-0252<br>ST-LC-0509<br>ST-LC-0510<br>ST-LC-0552<br>ST-LC-0553<br>ST-LC-8118<br>ST-LC-8119<br>ST-LC-8120<br>ST-LC-8121<br>ST-LC-8122<br>ST-LC-8123<br>ST-LC-9011

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0021

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：LC登记验证回调并实现内容；回调调用/表更新提交由未冻结cFE负责。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0509<br>ST-LC-0510<br>ST-LC-0552

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "表更新验证回调取得候选TableData并有限遍历、NOT_USED跳过",
    "operation_ids": [
      "ST-LC-0236",
      "ST-LC-0237",
      "ST-LC-0238",
      "ST-LC-0239",
      "ST-LC-0240",
      "ST-LC-0241",
      "ST-LC-0251"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "类型/data size清单检查，不保证offset安全",
    "operation_ids": [
      "ST-LC-0242",
      "ST-LC-0243"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "六关系/custom算子校验，按else-if首类别",
    "operation_ids": [
      "ST-LC-0244",
      "ST-LC-0245"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "MID用真实CFE_SB_IsValidMsgId观察，不编值域",
    "operation_ids": [
      "ST-LC-0246",
      "ST-LC-0247"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "额外float阈值NaN/无穷验证，区别运行输入无穷",
    "operation_ids": [
      "ST-LC-0248"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "逐项good/bad/unused，首错明细/返回，最终INFO",
    "operation_ids": [
      "ST-LC-0249",
      "ST-LC-0250",
      "ST-LC-0252",
      "ST-LC-0509",
      "ST-LC-0510"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "活动表接纳/提交需cFE真实接口",
    "operation_ids": [
      "ST-LC-0252",
      "ST-LC-0510"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：原WDT完全不验WatchpointOffset；未冻结cFE谓词、回调/EVS/更新绑定pending-interface。

## REQ-LC-0016

**NASA 原始 ID**：LC2006

**来源类别**：documented

**原始文字/行为**：LC shall convert telemetry to native byte order prior to evaluating actionpoint or watchpoint equations.

**原始理由/补充说明**：Actionpoint and Watchpoint evaluation need to be evaluated using data in the correct byte order.

**规范化中文需求**：评估 WP/AP 方程前，将遥测数据转换为 CPU 本机字节序。

**触发/条件**：从SB抽取多字节WP数据

**输入**：WDT类型中的BE/LE、源字节

**输出**：归一化SizedWPData

**状态与历史**：单个数据抽取临时值；AP读取已归一化WP结果

**处理及约束**：按类型区分BE/LE，不依赖数据自然对齐。<br>有符号值正确扩展，unsigned正确补零；浮点保留位表示后解释。<br>AP方程输入是WP结果而非原始遥测字节。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L44–44 LC2006<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L873–955 LC_CopyBytesWithSwap / LC_GetSizedWPData<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L464–550 LC_OperatorCompare<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L432–436 LC_EvaluateRPN

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0021<br>RES-LC-0022<br>RES-LC-0033<br>RES-LC-0200<br>RES-LC-0214<br>RES-LC-0215<br>RES-LC-0216<br>RES-LC-0219<br>RES-LC-0220<br>RES-LC-0235<br>RES-LC-0508<br>RES-LC-0702

**ST**：ST-LC-0002<br>ST-LC-0003<br>ST-LC-0014<br>ST-LC-0016<br>ST-LC-0200<br>ST-LC-0214<br>ST-LC-0215<br>ST-LC-0216<br>ST-LC-0219<br>ST-LC-0220<br>ST-LC-0235<br>ST-LC-0508<br>ST-LC-8106<br>ST-LC-8110<br>ST-LC-8111<br>ST-LC-8112<br>ST-LC-8113<br>ST-LC-8115<br>ST-LC-8116<br>ST-LC-8117<br>ST-LC-9010

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0508

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "多字节BE/LE逐字节转换到native，允许不对齐",
    "operation_ids": [
      "ST-LC-0214"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "signed扩展/unsigned补零/float位保留，再掩码比较",
    "operation_ids": [
      "ST-LC-0214",
      "ST-LC-0216",
      "ST-LC-0219",
      "ST-LC-0508"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "AP读取已归一化WP结果而非原始字节",
    "operation_ids": [
      "ST-LC-0220",
      "ST-LC-0235"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：目标swap map/ABI及AP组持久连接待核定；不以静态规则宣称运行通过。

## REQ-LC-0017

**NASA 原始 ID**：LC3000

**来源类别**：documented

**原始文字/行为**：Limit Checker shall support up to a maximum of <PLATFORM_DEFINED> Actionpoints

**原始理由/补充说明**：Used to size the actionpoint table

**规范化中文需求**：支持最多平台定义数量的 Actionpoint。

**触发/条件**：配置/构建及ADT使用

**输入**：LC_MAX_ACTIONPOINTS、ADT/ART

**输出**：有界AP目录/索引

**状态与历史**：ADT/ART容量

**处理及约束**：默认容量与实际部署容量区分。<br>AP数组合法索引为0..LC_MAX_ACTIONPOINTS-1。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L45–45 LC3000<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L518–625 LC_ValidateADT<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L60–74 LC_SampleAPReq

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0300<br>RES-LC-0302<br>RES-LC-0306<br>RES-LC-0307<br>RES-LC-0370<br>RES-LC-0371<br>RES-LC-0388<br>RES-LC-0530<br>RES-LC-0531<br>RES-LC-0554<br>RES-LC-0555<br>RES-LC-0700<br>RES-LC-0704

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0300<br>ST-LC-0302<br>ST-LC-0306<br>ST-LC-0307<br>ST-LC-0370<br>ST-LC-0371<br>ST-LC-0388<br>ST-LC-0530<br>ST-LC-0531<br>ST-LC-0554<br>ST-LC-0555<br>ST-LC-8008<br>ST-LC-8009<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：full

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：该原始条目的全部容量/算子/条件性计数义务已在资源规则及关联数据变换中保留；full仅评价此条语义，不表示完整系统可运行。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0530<br>ST-LC-0554

**附加字段 obligation_mapping**：full

**附加字段 obligations**：

```json
[
  {
    "description": "AP容量以平台定义LC_MAX_ACTIONPOINTS为上界，合法范围和inclusive迭代均受其约束。",
    "operation_ids": [
      "ST-LC-0302",
      "ST-LC-0306",
      "ST-LC-0307",
      "ST-LC-0370",
      "ST-LC-0371"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 prior_mapping_scope**：保留旧人工full结论，其口径是局部数据变换；不表示本轮所有义务或完整系统已full

**附加字段 remaining**：平台默认容量只是冻结源码基线，实际飞行容量与依赖部署尚未固定。

## REQ-LC-0018

**NASA 原始 ID**：LC3001

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Sample Request, LC shall process the request specified Actionpoints defined in the Actionpoint Definition Table (ADT) if the LC Application State is one of the following:
a)	Active
b)	Passive

**原始理由/补充说明**：Processing of the Actionpoint Definition Table is scheduled upon receipt of a  command (usually from the CFS Scheduler Application).  If LC App is Disabled, LC does not process WDT or ADT.   Disabled state useful for making updates to LC tables. Note that individual Watchpoints can’t be disabled;  Individual Actionpoints can be disabled.  Can sample individual or all actionpoints.  Heritage from LRO.

**规范化中文需求**：应用 ACTIVE/PASSIVE 收到 Sample Request 时处理请求指定的 Actionpoint。

**触发/条件**：独立的LC_SAMPLE_AP_MID消息到达

**输入**：StartIndex、EndIndex、UpdateAge、ADT、旧WRT/ART、应用状态

**输出**：所选AP新结果/统计/动作计划，可能过期的WRT

**状态与历史**：应用状态、AP状态及WP历史结果

**处理及约束**：应用DISABLED忽略请求。<br>全选请求要求start/end均等于LC_ALL_ACTIONPOINTS；否则start<=end且end<MAX。<br>先采样AP，再按UpdateAge更新全体WP倒计数。<br>实现LC_SampleAPs对首项NOT_USED/PERMOFF拒绝整范围；这可能阻止后续可采样AP，独立登记。<br>每AP先APSampleCount++再RPN；本AP的ActionInput使用已演进AppData，逐项写回ART/AppData。所有AP后才更新WP年龄；完整状态/效果顺序见RES0034。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L46–48 LC3001<br>[evidence/LC/fsw/src/lc_dispatch.c](evidence/LC/fsw/src/lc_dispatch.c) L332–337 LC_AppPipe<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L44–107 LC_SampleAPReq<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L41–75 LC_SampleAPs

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0300<br>RES-LC-0301<br>RES-LC-0302<br>RES-LC-0303<br>RES-LC-0304<br>RES-LC-0305<br>RES-LC-0306<br>RES-LC-0307<br>RES-LC-0308<br>RES-LC-0309<br>RES-LC-0310<br>RES-LC-0311<br>RES-LC-0312<br>RES-LC-0324<br>RES-LC-0366<br>RES-LC-0367<br>RES-LC-0368<br>RES-LC-0369<br>RES-LC-0391<br>RES-LC-0396<br>RES-LC-0511<br>RES-LC-0512<br>RES-LC-0530<br>RES-LC-0531<br>RES-LC-0700<br>RES-LC-0702

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0300<br>ST-LC-0301<br>ST-LC-0302<br>ST-LC-0303<br>ST-LC-0304<br>ST-LC-0305<br>ST-LC-0306<br>ST-LC-0307<br>ST-LC-0308<br>ST-LC-0309<br>ST-LC-0310<br>ST-LC-0311<br>ST-LC-0312<br>ST-LC-0324<br>ST-LC-0366<br>ST-LC-0367<br>ST-LC-0368<br>ST-LC-0369<br>ST-LC-0391<br>ST-LC-0396<br>ST-LC-0511<br>ST-LC-0512<br>ST-LC-0530<br>ST-LC-0531<br>ST-LC-8012<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8072<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0010<br>ISSUE-LC-0012<br>ISSUE-LC-0015

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：conflict

**检查层次**：static<br>manual

**人工语义核对**：范围首项非操作态时整范围不处理，与逐个跳过要求需审查；EDS分支无SampleAP路由。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。 本轮补全：每AP先APSampleCount++再RPN；本AP的ActionInput使用已演进AppData，逐项写回ART/AppData。所有AP后才更新WP年龄；完整状态/效果顺序见RES0034。 完整行为合同仍不构成官方事件/服务语法验收，mapping保持原评定。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0511<br>ST-LC-0512<br>ST-LC-0530

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "独立Sample Request入口读取请求指定范围及最新持久WRT/ART/AppData，不与监测数据入口合并。",
    "operation_ids": [
      "ST-LC-0300"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "应用ACTIVE/PASSIVE处理，DISABLED忽略且不采样/RTS/减龄；源码门控为非DISABLED。",
    "operation_ids": [
      "ST-LC-0301",
      "ST-LC-0369"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "ALL需两端均为ALL，其他inclusive范围须start<=end且end<MAX；非法范围不采样并登记错误。",
    "operation_ids": [
      "ST-LC-0302",
      "ST-LC-0303",
      "ST-LC-0511"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "合法请求应处理各指定可评估AP并仅跳过各不可采样项；源码首项NOT_USED/PERMOFF拒整范围的差异不得伪装覆盖。",
    "operation_ids": [
      "ST-LC-0304",
      "ST-LC-0305",
      "ST-LC-0306",
      "ST-LC-0307",
      "ST-LC-0308",
      "ST-LC-0309",
      "ST-LC-0366",
      "ST-LC-0391",
      "ST-LC-0512"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "每AP先增加APSampleCount再RPN，串行写回结果/统计，全部AP后ValidSampleCmd才标true并核对UpdateAge。",
    "operation_ids": [
      "ST-LC-0310",
      "ST-LC-0311",
      "ST-LC-0312",
      "ST-LC-0324",
      "ST-LC-0396",
      "ST-LC-0367",
      "ST-LC-0368"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：真实独立消息/软件回调入口、项目聚合数据与持久成员别名仍待官方接口绑定；不以注释或effects冒充执行。<br>首项拒绝整范围与请求指定AP的正式义务待ISSUE-LC-0015裁定；EDS路径不默认视为非EDS等价。<br>同次AP后age续段已由ST0368内联ST0253–0262；ActionWorking到WAgeWorking的官方聚合/别名加载仍待确认，不能把项目资源绑定当官方验收。

## REQ-LC-0019

**NASA 原始 ID**：LC3001.1

**来源类别**：documented

**原始文字/行为**：LC shall support the following Reverse Polish Operators:
a)	And
b)	Or
c)	Xor
d)	Not
e)	equals

**原始理由/补充说明**：Specifies supported operators

**规范化中文需求**：支持 AND、OR、XOR、NOT、EQUAL 五种逆波兰算子。

**触发/条件**：ADT方程求值/校验

**输入**：WP四值结果、RPNEquation

**输出**：AP PASS/FAIL/ERROR/STALE

**状态与历史**：临时RPN栈；无跨请求栈状态

**处理及约束**：AND：FALSE优先，之后ERROR、STALE、TRUE；OR：TRUE优先，之后ERROR、STALE、FALSE。<br>XOR：ERROR优先，其后STALE，否则布尔异或；NOT保留ERROR/STALE，否则反相。<br>EQUAL是方程终结：必须留下一个结果且pop后栈空；不是两值相等比较。<br>最终FALSE→PASS，TRUE→FAIL，ERROR→ERROR，STALE→STALE；非法/无终结/栈下溢为ERROR。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L49–54 LC3001.1<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L296–487 LC_EvaluateRPN<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L635–728 LC_ValidateRPN

**RES**：RES-LC-0001<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0034<br>RES-LC-0312<br>RES-LC-0313<br>RES-LC-0314<br>RES-LC-0315<br>RES-LC-0316<br>RES-LC-0317<br>RES-LC-0318<br>RES-LC-0319<br>RES-LC-0320<br>RES-LC-0321<br>RES-LC-0322<br>RES-LC-0323<br>RES-LC-0378<br>RES-LC-0379<br>RES-LC-0380<br>RES-LC-0381<br>RES-LC-0382<br>RES-LC-0395<br>RES-LC-0513<br>RES-LC-0554<br>RES-LC-0555<br>RES-LC-0702<br>RES-LC-0704

**ST**：ST-LC-0004<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0312<br>ST-LC-0313<br>ST-LC-0314<br>ST-LC-0315<br>ST-LC-0316<br>ST-LC-0317<br>ST-LC-0318<br>ST-LC-0319<br>ST-LC-0320<br>ST-LC-0321<br>ST-LC-0322<br>ST-LC-0323<br>ST-LC-0378<br>ST-LC-0379<br>ST-LC-0380<br>ST-LC-0381<br>ST-LC-0382<br>ST-LC-0395<br>ST-LC-0513<br>ST-LC-0554<br>ST-LC-0555<br>ST-LC-8000<br>ST-LC-8002<br>ST-LC-8003<br>ST-LC-8004<br>ST-LC-8005<br>ST-LC-8006<br>ST-LC-8008<br>ST-LC-8009<br>ST-LC-8046<br>ST-LC-8047<br>ST-LC-8048<br>ST-LC-8049<br>ST-LC-8050<br>ST-LC-8051<br>ST-LC-8052<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-8094<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：full

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：该原始条目的全部容量/算子/条件性计数义务已在资源规则及关联数据变换中保留；full仅评价此条语义，不表示完整系统可运行。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0513<br>ST-LC-0554

**附加字段 obligation_mapping**：full

**附加字段 obligations**：

```json
[
  {
    "description": "支持AND：FALSE优先、ERROR、STALE、TRUE，合法二元栈效果与下溢错误分开。",
    "operation_ids": [
      "ST-LC-0315"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "支持OR：TRUE优先、ERROR、STALE、FALSE。",
    "operation_ids": [
      "ST-LC-0316"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "支持XOR：ERROR优先、STALE，其余布尔异或。",
    "operation_ids": [
      "ST-LC-0317"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "支持NOT：ERROR/STALE保持，其余布尔反相。",
    "operation_ids": [
      "ST-LC-0318"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "支持EQUAL作为单结果方程终结，不是二元相等；空栈/额外栈项非法，终结后不读尾随token。",
    "operation_ids": [
      "ST-LC-0319"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "有界逐token求值读当前WRT四值；非法token/栈/无终结为ERROR，最终FALSE->PASS/TRUE->FAIL/ERROR/STALE对应AP四值。",
    "operation_ids": [
      "ST-LC-0312",
      "ST-LC-0313",
      "ST-LC-0314",
      "ST-LC-0320",
      "ST-LC-0321",
      "ST-LC-0322",
      "ST-LC-0323",
      "ST-LC-0513"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "ADT校验独立核对token合法、栈深正值、EQUAL时深1；只校容量不证明另表已定义WP。",
    "operation_ids": [
      "ST-LC-0378",
      "ST-LC-0379",
      "ST-LC-0380",
      "ST-LC-0381",
      "ST-LC-0382"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 prior_mapping_scope**：保留旧人工full结论，其口径是局部数据变换；不表示本轮所有义务或完整系统已full

**附加字段 remaining**：项目公式/聚合/枚举的官方库加载格式与解析器尚待验收；不声称该候选片段是完整可运行系统。

## REQ-LC-0020

**NASA 原始 ID**：LC3001.2

**来源类别**：documented

**原始文字/行为**：If the equation result for an Actionpoint results in a Pass, LC shall set the Number of Consecutive Fail values to zero.

**原始理由/补充说明**：Used to track consecutive failures.  If consecutive failures > max then take action.  Need to reset if Actionpoint doesn’t fail.  Heritage from LRO, SDO.

**规范化中文需求**：AP 方程结果 PASS 时，将该AP连续FAIL次数清零。

**触发/条件**：AP ACTIVE/PASSIVE一次求值产生PASS

**输入**：新AP结果、旧连续FAIL次数

**输出**：ConsecutiveFailCount=0，必要FAIL→PASS记录

**状态与历史**：ART单项历史

**处理及约束**：不能用CumulativeFailCount替代连续计数。<br>通过路径保留累计失败/RTS次数；仅连续计数归零。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L55–55 LC3001.2<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L229–254 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0356<br>RES-LC-0362<br>RES-LC-0365

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0356<br>ST-LC-0362<br>ST-LC-0365<br>ST-LC-8058<br>ST-LC-8061<br>ST-LC-8062<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：full

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：该原始条目的全部容量/算子/条件性计数义务已在资源规则及关联数据变换中保留；full仅评价此条语义，不表示完整系统可运行。

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 obligation_mapping**：full

**附加字段 obligations**：

```json
[
  {
    "description": "当前AP PASS时仅ConsecutiveFailCount清零，累计FAIL与RTS次数保持；FAIL->PASS事件处理完仍必须执行。",
    "operation_ids": [
      "ST-LC-0356",
      "ST-LC-0362",
      "ST-LC-0365"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 prior_mapping_scope**：保留旧人工full结论，其口径是局部数据变换；不表示本轮所有义务或完整系统已full

**附加字段 remaining**：无

## REQ-LC-0021

**NASA 原始 ID**：LC3001.3

**来源类别**：documented

**原始文字/行为**：If the Actionpoint cannot be evaluated, LC shall set the Actionpoint Results Table to ERROR for the erroneous Actionpoint.

**原始理由/补充说明**：Potential problems with the Watchpoint or the equation.  Heritage from LRO.

**规范化中文需求**：AP 无法评估时，ART 中该AP结果置为 ERROR。

**触发/条件**：RPN非法或结果含不可消解ERROR

**输入**：方程/栈、WP四值

**输出**：ActionResult=ERROR、错误事件

**状态与历史**：ART历史连续FAIL次数不自动归零

**处理及约束**：错误不是PASS。<br>WRT ERROR可被AND FALSE或OR TRUE遮蔽，只有方程最终ERROR才AP ERROR。<br>运行时非法表达式先LC_INVALID_RPN_ERR_EID，AP处理随后LC_ACTION_ERROR_ERR_EID。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L56–56 LC3001.3<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L104–108 LC_SampleSingleAP<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L266–275 LC_SampleSingleAP<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L458–484 LC_EvaluateRPN

**RES**：RES-LC-0001<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0034<br>RES-LC-0312<br>RES-LC-0313<br>RES-LC-0314<br>RES-LC-0315<br>RES-LC-0316<br>RES-LC-0317<br>RES-LC-0318<br>RES-LC-0319<br>RES-LC-0320<br>RES-LC-0321<br>RES-LC-0322<br>RES-LC-0323<br>RES-LC-0324<br>RES-LC-0363<br>RES-LC-0364<br>RES-LC-0365<br>RES-LC-0513<br>RES-LC-0519<br>RES-LC-0702

**ST**：ST-LC-0004<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0312<br>ST-LC-0313<br>ST-LC-0314<br>ST-LC-0315<br>ST-LC-0316<br>ST-LC-0317<br>ST-LC-0318<br>ST-LC-0319<br>ST-LC-0320<br>ST-LC-0321<br>ST-LC-0322<br>ST-LC-0323<br>ST-LC-0324<br>ST-LC-0363<br>ST-LC-0364<br>ST-LC-0365<br>ST-LC-0513<br>ST-LC-0519<br>ST-LC-8046<br>ST-LC-8047<br>ST-LC-8048<br>ST-LC-8049<br>ST-LC-8050<br>ST-LC-8051<br>ST-LC-8052<br>ST-LC-8058<br>ST-LC-8061<br>ST-LC-8062<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0513<br>ST-LC-0519

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "最终方程不可评估映射AP ERROR并写该AP ART.ActionResult，不能把ERROR当PASS。",
    "operation_ids": [
      "ST-LC-0323",
      "ST-LC-0324",
      "ST-LC-0363"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "合法AND FALSE/OR TRUE可遮蔽WP ERROR；非法RPN结构优先AP ERROR。",
    "operation_ids": [
      "ST-LC-0315",
      "ST-LC-0316",
      "ST-LC-0323"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "非法RPN详细错误先于ART结果写回和AP错误事件；ERROR保留连续FAIL且禁止RTS。",
    "operation_ids": [
      "ST-LC-0322",
      "ST-LC-0324",
      "ST-LC-0364",
      "ST-LC-0365",
      "ST-LC-0513",
      "ST-LC-0519"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。

## REQ-LC-0022

**NASA 原始 ID**：LC3002

**来源类别**：documented

**原始文字/行为**：For Each table-defined Actionpoint, LC shall store the results in the dump-only Actionpoint Results Table if the Actionpoint state is either:
a)	Active
b)	Passive

**原始理由/补充说明**：Actionpoint is not evaluated if state is unused, disabled or permanently disabled.  Heritage from LRO, (loosely SDO).

**规范化中文需求**：表定义AP状态ACTIVE或PASSIVE时，将其采样结果保存在dump-only ART。

**触发/条件**：合法AP采样请求选中该AP

**输入**：ADT方程、旧ART/WRT、CurrentState

**输出**：ActionResult及统计

**状态与历史**：AP状态五值与AP结果四值分别建模

**处理及约束**：仅ACTIVE/PASSIVE求值及结果更新。<br>NOT_USED、DISABLED、PERMOFF不求值。<br>结果enum不得和CurrentState enum合并。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L57–59 LC3002<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L82–108 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0300<br>RES-LC-0308<br>RES-LC-0309<br>RES-LC-0310<br>RES-LC-0311<br>RES-LC-0312<br>RES-LC-0323<br>RES-LC-0324<br>RES-LC-0339<br>RES-LC-0366<br>RES-LC-0391

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0300<br>ST-LC-0308<br>ST-LC-0309<br>ST-LC-0310<br>ST-LC-0311<br>ST-LC-0312<br>ST-LC-0323<br>ST-LC-0324<br>ST-LC-0339<br>ST-LC-0366<br>ST-LC-0391<br>ST-LC-8012<br>ST-LC-8057<br>ST-LC-8058<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 obligation_mapping**：full

**附加字段 obligations**：

```json
[
  {
    "description": "每AP当前状态ACTIVE/PASSIVE才求值与保存结果；NOT_USED/DISABLED/PERMOFF不求值、不更新该结果/统计。",
    "operation_ids": [
      "ST-LC-0308",
      "ST-LC-0309",
      "ST-LC-0312",
      "ST-LC-0324"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "结果保存于dump-only ART真实ActionResult持久目标，AP state与AP result枚举分开。",
    "operation_ids": [
      "ST-LC-0324",
      "ST-LC-0339"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：真实独立消息/软件回调入口、项目聚合数据与持久成员别名仍待官方接口绑定；不以注释或effects冒充执行。<br>本组只表达ART存储，不虚构表dump服务或将ART当自动HK完整遥测。

## REQ-LC-0023

**NASA 原始 ID**：LC3002.1

**来源类别**：documented

**原始文字/行为**：If the Actionpoint equation results in a transition from PASS to FAIL, LC shall issue an event message indicating the failure.

**原始理由/补充说明**：Want to see when an Actionpoint first exceeds the limit.  Heritage from LRO, SDO.

**规范化中文需求**：AP 求值发生 PASS→FAIL 时发出失败事件。

**触发/条件**：旧ActionResult==PASS且本次结果FAIL

**输入**：旧/新结果、PassToFailCount、MaxPassFailEvents

**输出**：增量PassToFailCount与限额内INFORMATION事件

**状态与历史**：ART历史转换计数

**处理及约束**：新失败累计和连续数分别增加。<br>事件受LC3002.1.1表限额约束，计数超过限额仍记录转换。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L60–60 LC3002.1<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L113–135 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0325<br>RES-LC-0330<br>RES-LC-0331<br>RES-LC-0332<br>RES-LC-0333<br>RES-LC-0334<br>RES-LC-0335<br>RES-LC-0336<br>RES-LC-0514<br>RES-LC-0702

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0325<br>ST-LC-0330<br>ST-LC-0331<br>ST-LC-0332<br>ST-LC-0333<br>ST-LC-0334<br>ST-LC-0335<br>ST-LC-0336<br>ST-LC-0514<br>ST-LC-8053<br>ST-LC-8054<br>ST-LC-8055<br>ST-LC-8056<br>ST-LC-8057<br>ST-LC-8058<br>ST-LC-8059<br>ST-LC-8060<br>ST-LC-8062<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0514

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "本次FAIL且previousResult PASS才增加PASS->FAIL转换数；ERROR/STALE到FAIL不算。",
    "operation_ids": [
      "ST-LC-0325",
      "ST-LC-0330",
      "ST-LC-0331",
      "ST-LC-0332"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "转换事件受LC3002.1.1限额允许时登记失败事件，事件效果之后才增长ART计数；超限仍保留转换计数。",
    "operation_ids": [
      "ST-LC-0333",
      "ST-LC-0334",
      "ST-LC-0335",
      "ST-LC-0336",
      "ST-LC-0514"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。

## REQ-LC-0024

**NASA 原始 ID**：LC3002.1.1

**来源类别**：documented

**原始文字/行为**：LC shall limit the number of generated PASS to FAIL transition event messages to the table-defined maximum.

**原始理由/补充说明**：Event generation limit avoids spamming of event messages.

**规范化中文需求**：PASS→FAIL 转换事件数不得超过表定义最大值。

**触发/条件**：一次PASS→FAIL

**输入**：新增后的PassToFailCount、MaxPassFailEvents

**输出**：允许/抑制转换事件；CumulativeEventMsgsSent

**状态与历史**：每AP自统计重置起转换次数

**处理及约束**：仅PassToFailCount_new<=MaxPassFailEvents时发事件。<br>最大值0使该类事件不发；统计仍增。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L61–61 LC3002.1.1<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L118–135 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0330<br>RES-LC-0331<br>RES-LC-0332<br>RES-LC-0333<br>RES-LC-0334<br>RES-LC-0335<br>RES-LC-0336<br>RES-LC-0514<br>RES-LC-0702

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0330<br>ST-LC-0331<br>ST-LC-0332<br>ST-LC-0333<br>ST-LC-0334<br>ST-LC-0335<br>ST-LC-0336<br>ST-LC-0514<br>ST-LC-8053<br>ST-LC-8054<br>ST-LC-8055<br>ST-LC-8056<br>ST-LC-8057<br>ST-LC-8058<br>ST-LC-8059<br>ST-LC-8060<br>ST-LC-8062<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0010

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0514

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "用新增转换数<=表MaxPassFailEvents控制PASS->FAIL事件，0限额禁止首事件；计数仍记录全部转换。",
    "operation_ids": [
      "ST-LC-0331",
      "ST-LC-0332",
      "ST-LC-0333"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "只在许可分支登记转换事件及其计数，不在超限分支产生该事件。",
    "operation_ids": [
      "ST-LC-0334",
      "ST-LC-0335",
      "ST-LC-0336",
      "ST-LC-0514"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。

## REQ-LC-0025

**NASA 原始 ID**：LC3002.2

**来源类别**：documented

**原始文字/行为**：If the Actionpoint equation results in a transition from FAIL to PASS, LC shall issue an event message indicating that the actionpoint is now within limits.

**原始理由/补充说明**：Want to see if an actionpoint which had fails, go back within limits.  Helps to see if there is data that is “bad” but not so bad that it fails enough times to cause the RTS to be executed.  Heritage from LRO, SDO.

**规范化中文需求**：AP 求值发生 FAIL→PASS 时发出恢复到限值内事件。

**触发/条件**：旧ActionResult==FAIL且本次结果PASS

**输入**：旧/新结果、FailToPassCount、MaxFailPassEvents

**输出**：增量FailToPassCount、限额内INFORMATION事件、连续FAIL归零

**状态与历史**：ART转换历史

**处理及约束**：转换事件受LC3002.2.1限额；PASS总是将连续FAIL归零。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L62–62 LC3002.2<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L229–254 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0335<br>RES-LC-0336<br>RES-LC-0356<br>RES-LC-0357<br>RES-LC-0358<br>RES-LC-0359<br>RES-LC-0360<br>RES-LC-0361<br>RES-LC-0362<br>RES-LC-0365<br>RES-LC-0518<br>RES-LC-0702

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0335<br>ST-LC-0336<br>ST-LC-0356<br>ST-LC-0357<br>ST-LC-0358<br>ST-LC-0359<br>ST-LC-0360<br>ST-LC-0361<br>ST-LC-0362<br>ST-LC-0365<br>ST-LC-0518<br>ST-LC-8053<br>ST-LC-8054<br>ST-LC-8055<br>ST-LC-8056<br>ST-LC-8057<br>ST-LC-8058<br>ST-LC-8059<br>ST-LC-8060<br>ST-LC-8061<br>ST-LC-8062<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0518

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "本次PASS且previousResult FAIL才增加FAIL->PASS转换数。",
    "operation_ids": [
      "ST-LC-0356",
      "ST-LC-0357",
      "ST-LC-0358",
      "ST-LC-0359"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "限额内登记恢复事件及事件数，随后PASS一律清连续FAIL，不增RTS。",
    "operation_ids": [
      "ST-LC-0360",
      "ST-LC-0361",
      "ST-LC-0335",
      "ST-LC-0336",
      "ST-LC-0362",
      "ST-LC-0365",
      "ST-LC-0518"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。

## REQ-LC-0026

**NASA 原始 ID**：LC3002.2.1

**来源类别**：documented

**原始文字/行为**：LC shall limit the number of generated FAIL to PASS transition event messages to the table-defined maximum.

**原始理由/补充说明**：Event generation limit avoids spamming of event messages.

**规范化中文需求**：FAIL→PASS 转换事件数不得超过表定义最大值。

**触发/条件**：一次FAIL→PASS

**输入**：新增后的FailToPassCount、MaxFailPassEvents

**输出**：允许/抑制恢复事件；CumulativeEventMsgsSent

**状态与历史**：每AP自统计重置起转换次数

**处理及约束**：仅FailToPassCount_new<=MaxFailPassEvents时发事件；计数仍记录全部转换。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L63–63 LC3002.2.1<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L231–248 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0335<br>RES-LC-0336<br>RES-LC-0356<br>RES-LC-0357<br>RES-LC-0358<br>RES-LC-0359<br>RES-LC-0360<br>RES-LC-0361<br>RES-LC-0518<br>RES-LC-0702

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0335<br>ST-LC-0336<br>ST-LC-0356<br>ST-LC-0357<br>ST-LC-0358<br>ST-LC-0359<br>ST-LC-0360<br>ST-LC-0361<br>ST-LC-0518<br>ST-LC-8053<br>ST-LC-8054<br>ST-LC-8055<br>ST-LC-8056<br>ST-LC-8057<br>ST-LC-8058<br>ST-LC-8059<br>ST-LC-8060<br>ST-LC-8062<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0010

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0518

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "用新增FailToPassCount<=表MaxFailPassEvents控制恢复事件，0禁止事件且转换统计不受影响。",
    "operation_ids": [
      "ST-LC-0358",
      "ST-LC-0359",
      "ST-LC-0360"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "许可才登记恢复事件和事件累计，超过限额无该事件。",
    "operation_ids": [
      "ST-LC-0361",
      "ST-LC-0335",
      "ST-LC-0336",
      "ST-LC-0518"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。

## REQ-LC-0027

**NASA 原始 ID**：LC3002.3

**来源类别**：documented

**原始文字/行为**：If the equation has yielded a Fail result for the table-defined consecutive number of times limit and the Actionpoint is currently Active, LC shall:
a)	generate an event message
b)	send a command to start the table-defined RTS
c)	Increment the counter indicating Total count of commands sent to SC task to start an RTS

**原始理由/补充说明**：Takes the action defined in the actionpoint definition table.  Heritage from LRO, SDO.

**规范化中文需求**：连续FAIL达到ADT阈值且AP ACTIVE时，生成事件、向SC请求启动表定义RTS，并累计发出请求次数。

**触发/条件**：本次AP FAIL且ConsecutiveFailCount_new>=MaxFailsBeforeRTS

**输入**：AP状态、应用状态、ADT阈值/RTSId/EventID/EventType/EventText

**输出**：RTS启动请求、表定义事件、AP/global请求计数

**状态与历史**：ART连续与累计FAIL；CurrentAPState及CurrentLCState

**处理及约束**：阈值比较为>=，不是>或累计失败达到阈值。<br>结合LC4001应用PASSIVE禁止RTS请求；应用ACTIVE且AP ACTIVE才发送。<br>发送请求边界止于SC接口；不声明RTS已执行成功。<br>当前调用LC_ExecuteRTS返回void，发送失败无返回可供计数条件判断，见补充。<br>先累计本次FAIL再用>=阈值判断；许可时先AP置PASSIVE、再RTS调用位置、再两请求计数、再动作事件和事件计数；应用/AP被动分支禁止RTS但保留各自抑制记录。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L64–67 LC3002.3<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L113–180 LC_SampleSingleAP<br>[evidence/LC/fsw/src/lc_custom.c](evidence/LC/fsw/src/lc_custom.c) L42–56 LC_ExecuteRTS

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0325<br>RES-LC-0326<br>RES-LC-0327<br>RES-LC-0328<br>RES-LC-0329<br>RES-LC-0335<br>RES-LC-0336<br>RES-LC-0337<br>RES-LC-0338<br>RES-LC-0339<br>RES-LC-0340<br>RES-LC-0341<br>RES-LC-0342<br>RES-LC-0343<br>RES-LC-0344<br>RES-LC-0345<br>RES-LC-0346<br>RES-LC-0347<br>RES-LC-0348<br>RES-LC-0351<br>RES-LC-0355<br>RES-LC-0365<br>RES-LC-0515<br>RES-LC-0516<br>RES-LC-0517<br>RES-LC-0523<br>RES-LC-0702<br>RES-LC-0703

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0325<br>ST-LC-0326<br>ST-LC-0327<br>ST-LC-0328<br>ST-LC-0329<br>ST-LC-0335<br>ST-LC-0336<br>ST-LC-0337<br>ST-LC-0338<br>ST-LC-0339<br>ST-LC-0340<br>ST-LC-0341<br>ST-LC-0342<br>ST-LC-0343<br>ST-LC-0344<br>ST-LC-0345<br>ST-LC-0346<br>ST-LC-0347<br>ST-LC-0348<br>ST-LC-0351<br>ST-LC-0355<br>ST-LC-0365<br>ST-LC-0515<br>ST-LC-0516<br>ST-LC-0517<br>ST-LC-0523<br>ST-LC-8053<br>ST-LC-8054<br>ST-LC-8055<br>ST-LC-8056<br>ST-LC-8057<br>ST-LC-8058<br>ST-LC-8059<br>ST-LC-8060<br>ST-LC-8061<br>ST-LC-8062<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0007<br>ISSUE-LC-0011

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：unknown

**检查层次**：static<br>manual

**人工语义核对**：请求/计数代码存在，但原文commands sent是否意味着Transmit成功未确定；cFE发送返回值被忽略，不能把计数叫成功执行。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。 本轮补全：先累计本次FAIL再用>=阈值判断；许可时先AP置PASSIVE、再RTS调用位置、再两请求计数、再动作事件和事件计数；应用/AP被动分支禁止RTS但保留各自抑制记录。 完整行为合同仍不构成官方事件/服务语法验收，mapping保持原评定。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0515<br>ST-LC-0516<br>ST-LC-0517<br>ST-LC-0523

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "本次FAIL先递增连续/累计FAIL，再用连续数>=表阈值判断，未达不请求动作。",
    "operation_ids": [
      "ST-LC-0326",
      "ST-LC-0327",
      "ST-LC-0328",
      "ST-LC-0329",
      "ST-LC-0337",
      "ST-LC-0365"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "原AP ACTIVE且应用ACTIVE许可RTS，应用PASSIVE/AP PASSIVE均独立抑制且不增RTS请求数；AP先置PASSIVE保留源码顺序。",
    "operation_ids": [
      "ST-LC-0338",
      "ST-LC-0339",
      "ST-LC-0340",
      "ST-LC-0351",
      "ST-LC-0355",
      "ST-LC-0516",
      "ST-LC-0517"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "以现有MID/FC/RTSId/包大小宏构造并登记SC RTS请求，真实发送义务待绑定。",
    "operation_ids": [
      "ST-LC-0341",
      "ST-LC-0342",
      "ST-LC-0523"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "请求效果位置后逐项增加AP CumulativeRTSExecCount及全局RTSExecCount；统计是源码尝试数，不证明commands sent成功。",
    "operation_ids": [
      "ST-LC-0343",
      "ST-LC-0344",
      "ST-LC-0345",
      "ST-LC-0346"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "按表EventText与tail构造缓冲区文本，用表EventID/EventType生成动作事件效果，再增加ART事件数。",
    "operation_ids": [
      "ST-LC-0347",
      "ST-LC-0348",
      "ST-LC-0335",
      "ST-LC-0336",
      "ST-LC-0515"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：真实独立消息/软件回调入口、项目聚合数据与持久成员别名仍待官方接口绑定；不以注释或effects冒充执行。<br>EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。<br>commands sent/RTS initiated边界及原代码忽略发送返回策略待ISSUE-LC-0007；错误间隔的“连续”待ISSUE-LC-0011/0017。

## REQ-LC-0028

**NASA 原始 ID**：LC3002.3.1

**来源类别**：documented

**原始文字/行为**：Once an RTS is initiated, LC shall change the current state of the associated Actionpoint to Passive.

**原始理由/补充说明**：Prevents an RTS from getting initiated more than once.  Heritage from LRO, (loosely SDO).

**规范化中文需求**：一旦RTS被发起，应将关联AP当前状态改为PASSIVE防止重复发起。

**触发/条件**：触发RTS启动的AP

**输入**：AP ACTIVE、连续阈值、应用状态

**输出**：AP.CurrentState=PASSIVE

**状态与历史**：独立于应用状态的AP状态

**处理及约束**：原文以RTS initiated为条件。<br>实现先改AP PASSIVE再检查应用状态及发送；即使应用PASSIVE未发送也改AP PASSIVE。<br>发送失败亦无成功反馈；需裁定发起与请求准备的边界。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L68–68 LC3002.3.1<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L138–197 LC_SampleSingleAP<br>[evidence/LC/fsw/src/lc_custom.c](evidence/LC/fsw/src/lc_custom.c) L42–56 LC_ExecuteRTS

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0337<br>RES-LC-0338<br>RES-LC-0339<br>RES-LC-0340<br>RES-LC-0342<br>RES-LC-0351<br>RES-LC-0392<br>RES-LC-0516<br>RES-LC-0523<br>RES-LC-0702<br>RES-LC-0703

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0337<br>ST-LC-0338<br>ST-LC-0339<br>ST-LC-0340<br>ST-LC-0342<br>ST-LC-0351<br>ST-LC-0392<br>ST-LC-0516<br>ST-LC-0523<br>ST-LC-8010<br>ST-LC-8055<br>ST-LC-8057<br>ST-LC-8058<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0007

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：conflict

**检查层次**：static<br>manual

**人工语义核对**：实现改状态条件宽于“RTS initiated”字面。保留原要求，另说明应用PASSIVE下AP ACTIVE仍转PASSIVE。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0516<br>ST-LC-0523

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "正式条件义务是Once an RTS is initiated后AP状态PASSIVE，独立documentary Set保留此条件。",
    "operation_ids": [
      "ST-LC-0392"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "源码实现达到阈值原AP ACTIVE先将状态PASSIVE，然后根据应用是否ACTIVE请求RTS；应用PASSIVE未发送也转PASSIVE。",
    "operation_ids": [
      "ST-LC-0337",
      "ST-LC-0338",
      "ST-LC-0339",
      "ST-LC-0340",
      "ST-LC-0342",
      "ST-LC-0351",
      "ST-LC-0516",
      "ST-LC-0523"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：initiated含义、失败策略与先置PASSIVE差异需裁定；不得把实现视图自动当原文完整覆盖。<br>EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。

## REQ-LC-0029

**NASA 原始 ID**：LC3002.4

**来源类别**：documented

**原始文字/行为**：If the equation has yielded a Fail result for the defined consecutive number of times and the Actionpoint is currently Passive, LC shall:
a)	generate an event message indicating that the Actionpoint Failed but the action was not taken
b)	Increment the Passive RTS Execution Counter

**原始理由/补充说明**：Informs the ground that an actionpoint tripped but that the action was not taken.  Heritage from LRO, SDO.

**规范化中文需求**：连续FAIL达到阈值且AP PASSIVE时，不执行动作，应发抑制事件并加Passive RTS计数。

**触发/条件**：AP PASSIVE且本次FAIL达到ADT连续阈值

**输入**：旧PassiveAPCount、MaxPassiveEvents、应用状态

**输出**：PassiveAPCount_new、PassiveRTSExecCount_new、限额内抑制事件、无RTS请求

**状态与历史**：ART及全局被动抑制计数

**处理及约束**：每次达到阈值的PASSIVE失败增加PassiveAPCount和全局PassiveRTSExecCount。<br>实现抑制事件受MaxPassiveEvents限额；正式本条未写该限额，保留差异。<br>与应用PASSIVE且AP ACTIVE路径分开；后者使用DEBUG事件且AP先转PASSIVE。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L69–71 LC3002.4<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L199–219 LC_SampleSingleAP<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L182–197 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0325<br>RES-LC-0326<br>RES-LC-0327<br>RES-LC-0335<br>RES-LC-0336<br>RES-LC-0337<br>RES-LC-0338<br>RES-LC-0349<br>RES-LC-0350<br>RES-LC-0352<br>RES-LC-0353<br>RES-LC-0354<br>RES-LC-0355<br>RES-LC-0365<br>RES-LC-0393<br>RES-LC-0517<br>RES-LC-0522<br>RES-LC-0702

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0325<br>ST-LC-0326<br>ST-LC-0327<br>ST-LC-0335<br>ST-LC-0336<br>ST-LC-0337<br>ST-LC-0338<br>ST-LC-0349<br>ST-LC-0350<br>ST-LC-0352<br>ST-LC-0353<br>ST-LC-0354<br>ST-LC-0355<br>ST-LC-0365<br>ST-LC-0393<br>ST-LC-0517<br>ST-LC-0522<br>ST-LC-8011<br>ST-LC-8053<br>ST-LC-8054<br>ST-LC-8055<br>ST-LC-8056<br>ST-LC-8057<br>ST-LC-8058<br>ST-LC-8059<br>ST-LC-8060<br>ST-LC-8061<br>ST-LC-8062<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0010

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：conflict

**检查层次**：static<br>manual

**人工语义核对**：正式“generate an event”与代码MaxPassiveEvents抑制分支存在需裁定的范围差异，不认定为运行缺陷。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0517<br>ST-LC-0522

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "本次FAIL达阈值且原AP PASSIVE时独立增加PassiveAPCount与全局PassiveRTSExecCount，禁止RTS。",
    "operation_ids": [
      "ST-LC-0337",
      "ST-LC-0338",
      "ST-LC-0352",
      "ST-LC-0353",
      "ST-LC-0349",
      "ST-LC-0350"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "正式LC3002.4保留动作未采取事件义务，但源码受MaxPassiveEvents限额；是否该限额约束原义务待裁定。",
    "operation_ids": [
      "ST-LC-0354",
      "ST-LC-0355",
      "ST-LC-0393",
      "ST-LC-0517",
      "ST-LC-0522"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "实现许可事件后再增加ART事件数；超限时仅事件被抑制，两项被动计数仍增加。",
    "operation_ids": [
      "ST-LC-0355",
      "ST-LC-0335",
      "ST-LC-0336",
      "ST-LC-0517"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。<br>原文没有MaxPassiveEvents限额，保留ISSUE-LC-0010与documentary对照，不偷偷补修代码。

## REQ-LC-0030

**NASA 原始 ID**：LC3003

**来源类别**：documented

**原始文字/行为**：If the Actionpoint is Disabled, LC shall skip processing that actionpoint.

**原始理由/补充说明**：Actionpoints can be individually enabled/disabled.  If disabled, don’t process the definition.  Heritage from LRO, (loosely SDO).

**规范化中文需求**：AP DISABLED 时跳过该AP处理，不产生该AP的采样动作。

**触发/条件**：请求包含DISABLED AP

**输入**：AP.CurrentState

**输出**：该AP结果/统计不更新、无RTS

**状态与历史**：ART既有值

**处理及约束**：LC_SampleSingleAP仅ACTIVE/PASSIVE进入求值。<br>不影响应用状态或其他可用AP。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L72–72 LC3003<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L89–108 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0308<br>RES-LC-0309<br>RES-LC-0365<br>RES-LC-0366<br>RES-LC-0391

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0308<br>ST-LC-0309<br>ST-LC-0365<br>ST-LC-0366<br>ST-LC-0391<br>ST-LC-8012<br>ST-LC-8058<br>ST-LC-8061<br>ST-LC-8062<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 obligation_mapping**：full

**附加字段 obligations**：

```json
[
  {
    "description": "被选中的DISABLED AP跳过RPN，结果/各统计保持且不发RTS；范围内其他可评估项继续。",
    "operation_ids": [
      "ST-LC-0308",
      "ST-LC-0309",
      "ST-LC-0366",
      "ST-LC-0391"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：无

## REQ-LC-0031

**NASA 原始 ID**：LC3004

**来源类别**：documented

**原始文字/行为**：If the Actionpoint is Unused, LC shall skip processing that actionpoint

**原始理由/补充说明**：Unused Actionpoint entries can’t be processed.  Heritage from LRO, (loosely SDO).

**规范化中文需求**：AP UNUSED 时跳过该AP处理。

**触发/条件**：请求包含NOT_USED AP

**输入**：AP.CurrentState

**输出**：该AP结果/统计不更新

**状态与历史**：ART既有值

**处理及约束**：单项求值入口跳过NOT_USED。<br>当前范围入口若首项NOT_USED则拒绝整范围，而非仅跳过该项。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L73–73 LC3004<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L41–75 LC_SampleAPs<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L89–108 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0304<br>RES-LC-0305<br>RES-LC-0308<br>RES-LC-0309<br>RES-LC-0365<br>RES-LC-0391<br>RES-LC-0512<br>RES-LC-0702

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0304<br>ST-LC-0305<br>ST-LC-0308<br>ST-LC-0309<br>ST-LC-0365<br>ST-LC-0391<br>ST-LC-0512<br>ST-LC-8012<br>ST-LC-8058<br>ST-LC-8061<br>ST-LC-8062<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0015

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：conflict

**检查层次**：static<br>manual

**人工语义核对**：单项禁止行为满足，但范围首项影响其他AP；与LC3001关联审查。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0512

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "单项NOT_USED AP不求值不改ART；正式要求仅跳过该AP。",
    "operation_ids": [
      "ST-LC-0308",
      "ST-LC-0309",
      "ST-LC-0391"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "源码若范围首项NOT_USED会拒绝整范围，可能阻断后续AP；不可把该实现当逐项跳过完整满足。",
    "operation_ids": [
      "ST-LC-0304",
      "ST-LC-0305",
      "ST-LC-0391",
      "ST-LC-0512"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：范围首项NOT_USED整体拒绝与LC3001/LC3004的组合意义待ISSUE-LC-0015。

## REQ-LC-0032

**NASA 原始 ID**：LC3005

**来源类别**：documented

**原始文字/行为**：If the Actionpoint is Permanently Disabled, LC shall skip processing that actionpoint

**原始理由/补充说明**：Useful for separation sequence actionpoints.  Heritage from LRO.

**规范化中文需求**：AP PERMANENTLY DISABLED 时跳过该AP处理。

**触发/条件**：请求包含PERMOFF AP

**输入**：AP.CurrentState

**输出**：该AP结果/统计不更新

**状态与历史**：ART既有值

**处理及约束**：PERMOFF不能通过常规状态命令重启。<br>当前范围入口首项PERMOFF会拒绝整范围，其他AP受影响。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L74–74 LC3005<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L41–75 LC_SampleAPs<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L89–108 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0304<br>RES-LC-0305<br>RES-LC-0308<br>RES-LC-0309<br>RES-LC-0365<br>RES-LC-0391<br>RES-LC-0512<br>RES-LC-0702

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0304<br>ST-LC-0305<br>ST-LC-0308<br>ST-LC-0309<br>ST-LC-0365<br>ST-LC-0391<br>ST-LC-0512<br>ST-LC-8012<br>ST-LC-8058<br>ST-LC-8061<br>ST-LC-8062<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0015

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：conflict

**检查层次**：static<br>manual

**人工语义核对**：单项禁止满足；整范围首项检查的范围效应需裁定。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0512

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "单项PERMOFF AP不求值不改ART；正式要求仅跳过该AP。",
    "operation_ids": [
      "ST-LC-0308",
      "ST-LC-0309",
      "ST-LC-0391"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "源码范围首项PERMOFF整体拒绝而非仅跳过该AP，保留差异。",
    "operation_ids": [
      "ST-LC-0304",
      "ST-LC-0305",
      "ST-LC-0391",
      "ST-LC-0512"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：范围首项PERMOFF组合解释待ISSUE-LC-0015；状态命令不能解除PERMOFF的规则由命令组负责，不在本组捏造解锁。

## REQ-LC-0033

**NASA 原始 ID**：LC3006

**来源类别**：documented

**原始文字/行为**：For each Actionpoint, the flight software shall maintain the following statistics in the dump-only Actionpoint Results Table:
a)	The result of the last Sample (Pass, Fail, Error, or Stale)
b)	The current state (PermOff, Disabled, Active, Passive, Unused)
c)	The number of times this Actionpoint has crossed from the Fail to Pass state
d)	The number of times this Actionpoint has crossed from the Pass to Fail state
e)	The number of consecutive times the equation result = Failed
f)	The cumulative number of times the equation result = Failed
g)	The cumulative count of the RTS executions
h)	Total number of event messages sent

**原始理由/补充说明**：Provides detailed results of the Actionpoint evaluation.  Heritage from LRO.

**规范化中文需求**：每个 AP 在 dump-only ART 保存最近结果、当前状态、两向转换、连续/累计FAIL、RTS请求累计和事件总计。

**触发/条件**：AP采样/状态命令/统计重置

**输入**：旧ART、新方程结果、动作/事件条件

**输出**：ActionResult、CurrentState、FailToPassCount、PassToFailCount、ConsecutiveFailCount、CumulativeFailCount、CumulativeRTSExecCount、CumulativeEventMsgsSent

**状态与历史**：ART每AP历史

**处理及约束**：PASS/FAIL/ERROR/STALE结果与PERMOFF/DISABLED/ACTIVE/PASSIVE/NOT_USED状态分别保留。<br>CumulativeEventMsgsSent对限额内转换事件/RTS触发事件/被动AP事件增加。<br>应用PASSIVE抑制DEBUG事件及AP ERROR事件实际不增加CumulativeEventMsgsSent；正式“Total number”与实现计数口径不同。<br>RTS计数是请求尝试，不是外部执行回执。<br>ART逐AP更新且后继入口读取最新状态；事件数不含应用PASSIVE DEBUG/AP ERROR。不能将统计写回等同外部服务成功。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L75–83 LC3006<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L82–281 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0308<br>RES-LC-0309<br>RES-LC-0310<br>RES-LC-0311<br>RES-LC-0322<br>RES-LC-0323<br>RES-LC-0324<br>RES-LC-0325<br>RES-LC-0326<br>RES-LC-0327<br>RES-LC-0328<br>RES-LC-0329<br>RES-LC-0330<br>RES-LC-0331<br>RES-LC-0332<br>RES-LC-0333<br>RES-LC-0334<br>RES-LC-0335<br>RES-LC-0336<br>RES-LC-0337<br>RES-LC-0339<br>RES-LC-0342<br>RES-LC-0343<br>RES-LC-0344<br>RES-LC-0345<br>RES-LC-0346<br>RES-LC-0347<br>RES-LC-0348<br>RES-LC-0349<br>RES-LC-0350<br>RES-LC-0351<br>RES-LC-0352<br>RES-LC-0353<br>RES-LC-0354<br>RES-LC-0355<br>RES-LC-0356<br>RES-LC-0357<br>RES-LC-0358<br>RES-LC-0359<br>RES-LC-0360<br>RES-LC-0361<br>RES-LC-0362<br>RES-LC-0363<br>RES-LC-0364<br>RES-LC-0394<br>RES-LC-0513<br>RES-LC-0514<br>RES-LC-0515<br>RES-LC-0516<br>RES-LC-0517<br>RES-LC-0518<br>RES-LC-0519<br>RES-LC-0523<br>RES-LC-0702<br>RES-LC-0703

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0308<br>ST-LC-0309<br>ST-LC-0310<br>ST-LC-0311<br>ST-LC-0322<br>ST-LC-0323<br>ST-LC-0324<br>ST-LC-0325<br>ST-LC-0326<br>ST-LC-0327<br>ST-LC-0328<br>ST-LC-0329<br>ST-LC-0330<br>ST-LC-0331<br>ST-LC-0332<br>ST-LC-0333<br>ST-LC-0334<br>ST-LC-0335<br>ST-LC-0336<br>ST-LC-0337<br>ST-LC-0339<br>ST-LC-0342<br>ST-LC-0343<br>ST-LC-0344<br>ST-LC-0345<br>ST-LC-0346<br>ST-LC-0347<br>ST-LC-0348<br>ST-LC-0349<br>ST-LC-0350<br>ST-LC-0351<br>ST-LC-0352<br>ST-LC-0353<br>ST-LC-0354<br>ST-LC-0355<br>ST-LC-0356<br>ST-LC-0357<br>ST-LC-0358<br>ST-LC-0359<br>ST-LC-0360<br>ST-LC-0361<br>ST-LC-0362<br>ST-LC-0363<br>ST-LC-0364<br>ST-LC-0394<br>ST-LC-0513<br>ST-LC-0514<br>ST-LC-0515<br>ST-LC-0516<br>ST-LC-0517<br>ST-LC-0518<br>ST-LC-0519<br>ST-LC-0523<br>ST-LC-8013<br>ST-LC-8052<br>ST-LC-8053<br>ST-LC-8054<br>ST-LC-8055<br>ST-LC-8056<br>ST-LC-8057<br>ST-LC-8058<br>ST-LC-8059<br>ST-LC-8060<br>ST-LC-8061<br>ST-LC-8062<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0011<br>ISSUE-LC-0017

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：conflict

**检查层次**：static<br>manual

**人工语义核对**：事件总数实际漏计两类AP关联事件；无运行测试，需确认统计口径。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。 本轮补全：ART逐AP更新且后继入口读取最新状态；事件数不含应用PASSIVE DEBUG/AP ERROR。不能将统计写回等同外部服务成功。 完整行为合同仍不构成官方事件/服务语法验收，mapping保持原评定。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0513<br>ST-LC-0514<br>ST-LC-0515<br>ST-LC-0516<br>ST-LC-0517<br>ST-LC-0518<br>ST-LC-0519<br>ST-LC-0523

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "a 最近Sample结果四值保存在ART，AP结果与AP状态独立。",
    "operation_ids": [
      "ST-LC-0323",
      "ST-LC-0324"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "b 当前AP状态五值读取/保留，达到阈值原ACTIVE转PASSIVE实现顺序清楚；命令/复位流程由其他组持续维护。",
    "operation_ids": [
      "ST-LC-0308",
      "ST-LC-0309",
      "ST-LC-0339"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "c FAIL->PASS转换次数独立增长且持久存储。",
    "operation_ids": [
      "ST-LC-0357",
      "ST-LC-0358",
      "ST-LC-0359"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "d PASS->FAIL转换次数独立增长且持久存储。",
    "operation_ids": [
      "ST-LC-0330",
      "ST-LC-0331",
      "ST-LC-0332"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "e 连续FAIL：FAIL增、PASS/STALE清、ERROR保持；“consecutive”是否应包含错误间隔待裁定。",
    "operation_ids": [
      "ST-LC-0326",
      "ST-LC-0327",
      "ST-LC-0362",
      "ST-LC-0364",
      "ST-LC-0394",
      "ST-LC-0519"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "f 累计FAIL只在FAIL增长，不因PASS/STALE/ERROR清零。",
    "operation_ids": [
      "ST-LC-0328",
      "ST-LC-0329"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "g 源码RTS累计是请求尝试，原“RTS executions”若指外部执行未实现回执，需裁定。",
    "operation_ids": [
      "ST-LC-0342",
      "ST-LC-0343",
      "ST-LC-0344",
      "ST-LC-0394",
      "ST-LC-0523"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "h 原总事件数义务与实现仅计限额内转换/动作/被动AP事件不同；DEBUG应用被动/AP ERROR/非法RPN不计，需保留差异。",
    "operation_ids": [
      "ST-LC-0335",
      "ST-LC-0336",
      "ST-LC-0351",
      "ST-LC-0364",
      "ST-LC-0322",
      "ST-LC-0394",
      "ST-LC-0513",
      "ST-LC-0516",
      "ST-LC-0519"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "ART真实各目标Set对当前AP持久写回，后继请求/HK读最新值；保持dump-only结果表边界。",
    "operation_ids": [
      "ST-LC-0324",
      "ST-LC-0327",
      "ST-LC-0329",
      "ST-LC-0332",
      "ST-LC-0359",
      "ST-LC-0339",
      "ST-LC-0344",
      "ST-LC-0336"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：原统计口径/错误间隔待ISSUE-LC-0011/0017；真实EVS/SB提交pending-interface，不能从统计增量证明服务成功。

## REQ-LC-0034

**NASA 原始 ID**：LC3007

**来源类别**：documented

**原始文字/行为**：Upon receipt of a table update indication, LC shall validate the Actionpoint Definition Table for the following:
a)	valid default state
b)	RTS number (in range)
c)	Event Type (DEBUG, INFO, ERROR, CRITICAL)
d)	Failure Count (in range)
e)	Action Equation syntax

**原始理由/补充说明**：Not much can be validated since much is at run-time. Heritage from LRO.

**规范化中文需求**：ADT 更新时验证默认状态、RTS号、事件类型、失败阈值、RPN语法。

**触发/条件**：cFE TBL调用ADT验证回调/更新

**输入**：ADT全部条目、平台常量

**输出**：校验返回、首错误详细事件、汇总事件

**状态与历史**：旧ADT/ART与cFE表状态

**处理及约束**：NOT_USED定义项作为空闲跳过。<br>使用项状态在ACTIVE/PASSIVE/DISABLED/PERMOFF；RTSId<=LC_MAX_VALID_ADT_RTSID，失败阈值非0。<br>事件类型仅DEBUG/INFORMATION/ERROR/CRITICAL；RPN需合法WP索引/操作数深度/终止EQUAL。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L84–89 LC3007<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L494–630 LC_ValidateADT<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L635–728 LC_ValidateRPN<br>[evidence/LC/fsw/src/lc_utils.c](evidence/LC/fsw/src/lc_utils.c) L89–97 LC_ManageTables

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0028<br>RES-LC-0370<br>RES-LC-0371<br>RES-LC-0372<br>RES-LC-0373<br>RES-LC-0374<br>RES-LC-0375<br>RES-LC-0376<br>RES-LC-0377<br>RES-LC-0378<br>RES-LC-0379<br>RES-LC-0380<br>RES-LC-0381<br>RES-LC-0382<br>RES-LC-0383<br>RES-LC-0384<br>RES-LC-0385<br>RES-LC-0386<br>RES-LC-0387<br>RES-LC-0388<br>RES-LC-0389<br>RES-LC-0390<br>RES-LC-0395<br>RES-LC-0520<br>RES-LC-0521<br>RES-LC-0554<br>RES-LC-0555<br>RES-LC-0702<br>RES-LC-0704

**ST**：ST-LC-0009<br>ST-LC-0370<br>ST-LC-0371<br>ST-LC-0372<br>ST-LC-0373<br>ST-LC-0374<br>ST-LC-0375<br>ST-LC-0376<br>ST-LC-0377<br>ST-LC-0378<br>ST-LC-0379<br>ST-LC-0380<br>ST-LC-0381<br>ST-LC-0382<br>ST-LC-0383<br>ST-LC-0384<br>ST-LC-0385<br>ST-LC-0386<br>ST-LC-0387<br>ST-LC-0388<br>ST-LC-0389<br>ST-LC-0390<br>ST-LC-0395<br>ST-LC-0520<br>ST-LC-0521<br>ST-LC-0554<br>ST-LC-0555<br>ST-LC-8000<br>ST-LC-8001<br>ST-LC-8002<br>ST-LC-8003<br>ST-LC-8004<br>ST-LC-8005<br>ST-LC-8006<br>ST-LC-8007<br>ST-LC-8008<br>ST-LC-8009<br>ST-LC-8094

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：回调规则明确；cFE提交/调用能力依赖外部框架。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0520<br>ST-LC-0521<br>ST-LC-0554

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "表更新指示触发验证候选ADT，不自动生效。",
    "operation_ids": [
      "ST-LC-0370"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "a 检查使用项默认状态四合法AP值；NOT_USED仅记录空闲。",
    "operation_ids": [
      "ST-LC-0372",
      "ST-LC-0373",
      "ST-LC-0374"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "b 检查RTSId<=平台LC_MAX_VALID_ADT_RTSID，不擅增下界1。",
    "operation_ids": [
      "ST-LC-0375"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "c 检查事件类型DEBUG/INFORMATION/ERROR/CRITICAL。",
    "operation_ids": [
      "ST-LC-0377"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "d 检查失败阈值非0，原字段uint16上界不另造新任务限制。",
    "operation_ids": [
      "ST-LC-0376"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "e 检查有界RPN token、栈深、EQUAL终结且depth1，超WP容量非法但不证明WDT实际定义。",
    "operation_ids": [
      "ST-LC-0378",
      "ST-LC-0379",
      "ST-LC-0380",
      "ST-LC-0381",
      "ST-LC-0382"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "每条短路只计Good/Bad/Unused一类，首错误码锁存，提供唯一首错误详细事件与总计事件。",
    "operation_ids": [
      "ST-LC-0383",
      "ST-LC-0384",
      "ST-LC-0373",
      "ST-LC-0385",
      "ST-LC-0386",
      "ST-LC-0387",
      "ST-LC-0388",
      "ST-LC-0389",
      "ST-LC-0390",
      "ST-LC-0520",
      "ST-LC-0521"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：真实独立消息/软件回调入口、项目聚合数据与持久成员别名仍待官方接口绑定；不以注释或effects冒充执行。<br>EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。<br>TBL回调返回/表激活与跨表一致性不由本校验快照完成。

## REQ-LC-0035

**NASA 原始 ID**：LC4000

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Set LC Application State To Active Command, LC shall set the state of the LC Application to Active.

**原始理由/补充说明**：Nominal mode for LC.  LC performs all limit tests defined in the watchpoint definition table and will invoke stored command sequences if the results of watchpoint evaluations trigger an actionpoint condition as defined in the actionpoint definition table.  Heritage from LRO, SDO.

**规范化中文需求**：将LC应用状态设置为ACTIVE。

**触发/条件**：长度正确的指定地面状态命令到达

**输入**：NewLCState=LC_STATE_ACTIVE

**输出**：CurrentLCState_new、CmdCount_new、状态确认事件

**状态与历史**：LC_AppData.CurrentLCState，区别于ART单AP状态

**处理及约束**：继续WP/AP评估并允许符合AP条件的RTS请求。<br>无效NewLCState被拒绝，CmdErrCount加一并发ERROR事件。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L90–90 LC4000<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L317–345 LC_SetLCStateCmd<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L280–281 LC_CheckMsgForWPs<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L52–55 LC_SampleAPReq<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L150–197 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0025<br>RES-LC-0100<br>RES-LC-0102<br>RES-LC-0103<br>RES-LC-0104<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0110<br>RES-LC-0111<br>RES-LC-0500<br>RES-LC-0501<br>RES-LC-0538<br>RES-LC-0539<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0006<br>ST-LC-0100<br>ST-LC-0102<br>ST-LC-0103<br>ST-LC-0104<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0110<br>ST-LC-0111<br>ST-LC-0500<br>ST-LC-0501<br>ST-LC-0538<br>ST-LC-0539<br>ST-LC-8019<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0500<br>ST-LC-0501<br>ST-LC-0538

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "长度与枚举合法后应用状态改为命令明示值；非法保持原状态并拒绝",
    "operation_ids": [
      "ST-LC-0100",
      "ST-LC-0110",
      "ST-LC-0111",
      "ST-LC-0102",
      "ST-LC-0103",
      "ST-LC-0104",
      "ST-LC-0105",
      "ST-LC-0106",
      "ST-LC-0107",
      "ST-LC-0500",
      "ST-LC-0501"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0500",
      "ST-LC-0501",
      "ST-LC-0538"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0036

**NASA 原始 ID**：LC4001

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Set LC Application State to Passive Command, LC shall set the LC Application State to Passive.

**原始理由/补充说明**：Provides the ability to monitor data but not take actions.  LC still monitors telemetry and report statistics, however, no actions will be taken.  Heritage from LRO, SDO (SDO used the term Watch Mode)

**规范化中文需求**：将LC应用状态设置为PASSIVE。

**触发/条件**：长度正确的指定地面状态命令到达

**输入**：NewLCState=LC_STATE_PASSIVE

**输出**：CurrentLCState_new、CmdCount_new、状态确认事件

**状态与历史**：LC_AppData.CurrentLCState，区别于ART单AP状态

**处理及约束**：继续WP/AP评估与统计/事件，禁止RTS请求。<br>无效NewLCState被拒绝，CmdErrCount加一并发ERROR事件。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L91–91 LC4001<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L317–345 LC_SetLCStateCmd<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L280–281 LC_CheckMsgForWPs<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L52–55 LC_SampleAPReq<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L150–197 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0025<br>RES-LC-0100<br>RES-LC-0102<br>RES-LC-0103<br>RES-LC-0104<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0110<br>RES-LC-0111<br>RES-LC-0500<br>RES-LC-0501<br>RES-LC-0538<br>RES-LC-0539<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0006<br>ST-LC-0100<br>ST-LC-0102<br>ST-LC-0103<br>ST-LC-0104<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0110<br>ST-LC-0111<br>ST-LC-0500<br>ST-LC-0501<br>ST-LC-0538<br>ST-LC-0539<br>ST-LC-8019<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0500<br>ST-LC-0501<br>ST-LC-0538

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "长度与枚举合法后应用状态改为命令明示值；非法保持原状态并拒绝",
    "operation_ids": [
      "ST-LC-0100",
      "ST-LC-0110",
      "ST-LC-0111",
      "ST-LC-0102",
      "ST-LC-0103",
      "ST-LC-0104",
      "ST-LC-0105",
      "ST-LC-0106",
      "ST-LC-0107",
      "ST-LC-0500",
      "ST-LC-0501"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0500",
      "ST-LC-0501",
      "ST-LC-0538"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0037

**NASA 原始 ID**：LC4002

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Set LC Application State to Disable Command, LC shall set the LC Application State to Disabled.

**原始理由/补充说明**：Provides capability to stop all LC monitoring.  Useful when updating watchpoint and/or Actionpoint definition tables.  Heritage from LRO, SDO.

**规范化中文需求**：将LC应用状态设置为DISABLED。

**触发/条件**：长度正确的指定地面状态命令到达

**输入**：NewLCState=LC_STATE_DISABLED

**输出**：CurrentLCState_new、CmdCount_new、状态确认事件

**状态与历史**：LC_AppData.CurrentLCState，区别于ART单AP状态

**处理及约束**：停止WP监测与AP采样；状态/统计/HK命令仍可处理。<br>无效NewLCState被拒绝，CmdErrCount加一并发ERROR事件。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L92–92 LC4002<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L317–345 LC_SetLCStateCmd<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L280–281 LC_CheckMsgForWPs<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L52–55 LC_SampleAPReq<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L150–197 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0025<br>RES-LC-0100<br>RES-LC-0102<br>RES-LC-0103<br>RES-LC-0104<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0110<br>RES-LC-0111<br>RES-LC-0500<br>RES-LC-0501<br>RES-LC-0538<br>RES-LC-0539<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0006<br>ST-LC-0100<br>ST-LC-0102<br>ST-LC-0103<br>ST-LC-0104<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0110<br>ST-LC-0111<br>ST-LC-0500<br>ST-LC-0501<br>ST-LC-0538<br>ST-LC-0539<br>ST-LC-8019<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0500<br>ST-LC-0501<br>ST-LC-0538

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "长度与枚举合法后应用状态改为命令明示值；非法保持原状态并拒绝",
    "operation_ids": [
      "ST-LC-0100",
      "ST-LC-0110",
      "ST-LC-0111",
      "ST-LC-0102",
      "ST-LC-0103",
      "ST-LC-0104",
      "ST-LC-0105",
      "ST-LC-0106",
      "ST-LC-0107",
      "ST-LC-0500",
      "ST-LC-0501"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0500",
      "ST-LC-0501",
      "ST-LC-0538"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0038

**NASA 原始 ID**：LC4003

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Set Actionpoint to Active Command, LC shall set the state for the command-specified Actionpoint to ACTIVE such that the actionpoint is evaluated and the table-defined actions are taken based on the evaluation.

**原始理由/补充说明**：Provides the ability to enable the actionpoint so that appropriate actions are taken on the basis of current watchpoint states.  Heritage from LRO, SDO.

**规范化中文需求**：收到命令后将指定单个AP置为ACTIVE；原文义务与当前例外分别保留。

**触发/条件**：长度正确的指定地面状态命令到达

**输入**：合法APNumber、NewAPState=LC_APSTATE_ACTIVE

**输出**：AP.CurrentState_new、成功/拒绝计数及命令事件

**状态与历史**：ART单项CurrentState；应用状态不变

**处理及约束**：AP可采样并在应用ACTIVE时允许阈值RTS请求。<br>实现仅修改原状态不是NOT_USED/PERMOFF的AP；单个禁止项命令拒绝，全选略过禁止项但命令整体接受。<br>永久禁用保护对应LC4009.1；NOT_USED例外与“all”字面需统一口径。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L93–93 LC4003<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L353–474 LC_SetAPStateCmd<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L89–108 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0025<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0112<br>RES-LC-0113<br>RES-LC-0114<br>RES-LC-0115<br>RES-LC-0116<br>RES-LC-0117<br>RES-LC-0118<br>RES-LC-0119<br>RES-LC-0120<br>RES-LC-0121<br>RES-LC-0501<br>RES-LC-0540<br>RES-LC-0541<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0006<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0112<br>ST-LC-0113<br>ST-LC-0114<br>ST-LC-0115<br>ST-LC-0116<br>ST-LC-0117<br>ST-LC-0118<br>ST-LC-0119<br>ST-LC-0120<br>ST-LC-0121<br>ST-LC-0501<br>ST-LC-0540<br>ST-LC-0541<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8076<br>ST-LC-8077<br>ST-LC-8078<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：单项命令在NOT_USED/PERMOFF拒绝；PERMOFF保护有LC4009.1正式依据，NOT_USED视作不可用条目，另有补充。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0501<br>ST-LC-0540

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "合法状态/索引和当前条目门控，单选或有限ALL遍历赋值，结束成功或拒绝提交",
    "operation_ids": [
      "ST-LC-0112",
      "ST-LC-0113",
      "ST-LC-0114",
      "ST-LC-0115",
      "ST-LC-0116",
      "ST-LC-0117",
      "ST-LC-0118",
      "ST-LC-0119",
      "ST-LC-0120",
      "ST-LC-0107"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0501",
      "ST-LC-0540"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "单项原文按指定AP赋值的义务与NOT_USED/PERMOFF实现拒绝被分离保留",
    "operation_ids": [
      "ST-LC-0121"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "正式单项状态命令未声明NOT_USED/PERMOFF例外，代码单选拒绝；激活PERMOFF另受LC4009.1约束，需需求裁决。",
    "operation_ids": [],
    "status": "pending-interpretation",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。<br>正式单项状态命令未声明NOT_USED/PERMOFF例外，代码单选拒绝；激活PERMOFF另受LC4009.1约束，需需求裁决。

## REQ-LC-0039

**NASA 原始 ID**：LC4004

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Set All Actionpoints to Active Command, LC shall set the state for all Actionpoints to ACTIVE such that the actionpoints are evaluated and the table-defined actions are taken based on the evaluation.

**原始理由/补充说明**：Provide the ability to enable ALL actionpoints.  Heritage from LRO, SDO.

**规范化中文需求**：收到命令后将全部AP置为ACTIVE；原文义务与当前例外分别保留。

**触发/条件**：长度正确的指定地面状态命令到达

**输入**：APNumber=LC_ALL_ACTIONPOINTS、NewAPState=LC_APSTATE_ACTIVE

**输出**：AP.CurrentState_new、成功/拒绝计数及命令事件

**状态与历史**：ART单项CurrentState；应用状态不变

**处理及约束**：AP可采样并在应用ACTIVE时允许阈值RTS请求。<br>实现仅修改原状态不是NOT_USED/PERMOFF的AP；单个禁止项命令拒绝，全选略过禁止项但命令整体接受。<br>永久禁用保护对应LC4009.1；NOT_USED例外与“all”字面需统一口径。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L94–94 LC4004<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L353–474 LC_SetAPStateCmd<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L89–108 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0025<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0112<br>RES-LC-0113<br>RES-LC-0114<br>RES-LC-0115<br>RES-LC-0116<br>RES-LC-0117<br>RES-LC-0118<br>RES-LC-0119<br>RES-LC-0120<br>RES-LC-0121<br>RES-LC-0501<br>RES-LC-0540<br>RES-LC-0541<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0006<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0112<br>ST-LC-0113<br>ST-LC-0114<br>ST-LC-0115<br>ST-LC-0116<br>ST-LC-0117<br>ST-LC-0118<br>ST-LC-0119<br>ST-LC-0120<br>ST-LC-0121<br>ST-LC-0501<br>ST-LC-0540<br>ST-LC-0541<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8076<br>ST-LC-8077<br>ST-LC-8078<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0008

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：conflict

**检查层次**：static<br>manual

**人工语义核对**：“all”源码实际为全部可修改AP，排除NOT_USED/PERMOFF；保留原文，等待确认该量词范围。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0501<br>ST-LC-0540

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "合法状态/索引和当前条目门控，单选或有限ALL遍历赋值，结束成功或拒绝提交",
    "operation_ids": [
      "ST-LC-0112",
      "ST-LC-0113",
      "ST-LC-0114",
      "ST-LC-0115",
      "ST-LC-0116",
      "ST-LC-0117",
      "ST-LC-0118",
      "ST-LC-0119",
      "ST-LC-0120",
      "ST-LC-0107"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "ALL原文对全部条目的要求未被实现例外替换",
    "operation_ids": [
      "ST-LC-0121"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "正式ALL包含NOT_USED/PERMOFF与代码跳过例外、LC4009.1的冲突待裁决；不宣称代码流程全满足ALL原文。",
    "operation_ids": [],
    "status": "pending-interpretation",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0501",
      "ST-LC-0540"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：正式ALL包含NOT_USED/PERMOFF与代码跳过例外、LC4009.1的冲突待裁决；不宣称代码流程全满足ALL原文。<br>已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0040

**NASA 原始 ID**：LC4005

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Set Actionpoint to Passive Command, LC shall set the state for the command-specified Actionpoint to PASSIVE such that the actionpoint is evaluated, however, no actions are taken.

**原始理由/补充说明**：Provides ability to monitor data associated with an action point but not take the action defined for that actionpoint.  Heritage from LRO, SDO.

**规范化中文需求**：收到命令后将指定单个AP置为PASSIVE；原文义务与当前例外分别保留。

**触发/条件**：长度正确的指定地面状态命令到达

**输入**：合法APNumber、NewAPState=LC_APSTATE_PASSIVE

**输出**：AP.CurrentState_new、成功/拒绝计数及命令事件

**状态与历史**：ART单项CurrentState；应用状态不变

**处理及约束**：AP可采样但不发RTS，符合阈值时记录抑制统计。<br>实现仅修改原状态不是NOT_USED/PERMOFF的AP；单个禁止项命令拒绝，全选略过禁止项但命令整体接受。<br>永久禁用保护对应LC4009.1；NOT_USED例外与“all”字面需统一口径。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L95–95 LC4005<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L353–474 LC_SetAPStateCmd<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L89–108 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0025<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0112<br>RES-LC-0113<br>RES-LC-0114<br>RES-LC-0115<br>RES-LC-0116<br>RES-LC-0117<br>RES-LC-0118<br>RES-LC-0119<br>RES-LC-0120<br>RES-LC-0121<br>RES-LC-0501<br>RES-LC-0540<br>RES-LC-0541<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0006<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0112<br>ST-LC-0113<br>ST-LC-0114<br>ST-LC-0115<br>ST-LC-0116<br>ST-LC-0117<br>ST-LC-0118<br>ST-LC-0119<br>ST-LC-0120<br>ST-LC-0121<br>ST-LC-0501<br>ST-LC-0540<br>ST-LC-0541<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8076<br>ST-LC-8077<br>ST-LC-8078<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：单项命令在NOT_USED/PERMOFF拒绝；PERMOFF保护有LC4009.1正式依据，NOT_USED视作不可用条目，另有补充。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0501<br>ST-LC-0540

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "合法状态/索引和当前条目门控，单选或有限ALL遍历赋值，结束成功或拒绝提交",
    "operation_ids": [
      "ST-LC-0112",
      "ST-LC-0113",
      "ST-LC-0114",
      "ST-LC-0115",
      "ST-LC-0116",
      "ST-LC-0117",
      "ST-LC-0118",
      "ST-LC-0119",
      "ST-LC-0120",
      "ST-LC-0107"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0501",
      "ST-LC-0540"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "单项原文按指定AP赋值的义务与NOT_USED/PERMOFF实现拒绝被分离保留",
    "operation_ids": [
      "ST-LC-0121"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "正式单项状态命令未声明NOT_USED/PERMOFF例外，代码单选拒绝；激活PERMOFF另受LC4009.1约束，需需求裁决。",
    "operation_ids": [],
    "status": "pending-interpretation",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。<br>正式单项状态命令未声明NOT_USED/PERMOFF例外，代码单选拒绝；激活PERMOFF另受LC4009.1约束，需需求裁决。

## REQ-LC-0041

**NASA 原始 ID**：LC4006

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Set All Actionpoints to Passive Command, LC shall set the state for the all Actionpoints to PASSIVE such that all actionpoints are evaluated, however, no actions are taken.

**原始理由/补充说明**：Provides ability to quiet all actionpoints.  Heritage from LRO, SDO.

**规范化中文需求**：收到命令后将全部AP置为PASSIVE；原文义务与当前例外分别保留。

**触发/条件**：长度正确的指定地面状态命令到达

**输入**：APNumber=LC_ALL_ACTIONPOINTS、NewAPState=LC_APSTATE_PASSIVE

**输出**：AP.CurrentState_new、成功/拒绝计数及命令事件

**状态与历史**：ART单项CurrentState；应用状态不变

**处理及约束**：AP可采样但不发RTS，符合阈值时记录抑制统计。<br>实现仅修改原状态不是NOT_USED/PERMOFF的AP；单个禁止项命令拒绝，全选略过禁止项但命令整体接受。<br>永久禁用保护对应LC4009.1；NOT_USED例外与“all”字面需统一口径。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L96–96 LC4006<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L353–474 LC_SetAPStateCmd<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L89–108 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0025<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0112<br>RES-LC-0113<br>RES-LC-0114<br>RES-LC-0115<br>RES-LC-0116<br>RES-LC-0117<br>RES-LC-0118<br>RES-LC-0119<br>RES-LC-0120<br>RES-LC-0121<br>RES-LC-0501<br>RES-LC-0540<br>RES-LC-0541<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0006<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0112<br>ST-LC-0113<br>ST-LC-0114<br>ST-LC-0115<br>ST-LC-0116<br>ST-LC-0117<br>ST-LC-0118<br>ST-LC-0119<br>ST-LC-0120<br>ST-LC-0121<br>ST-LC-0501<br>ST-LC-0540<br>ST-LC-0541<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8076<br>ST-LC-8077<br>ST-LC-8078<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0008

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：conflict

**检查层次**：static<br>manual

**人工语义核对**：“all”源码实际为全部可修改AP，排除NOT_USED/PERMOFF；保留原文，等待确认该量词范围。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0501<br>ST-LC-0540

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "合法状态/索引和当前条目门控，单选或有限ALL遍历赋值，结束成功或拒绝提交",
    "operation_ids": [
      "ST-LC-0112",
      "ST-LC-0113",
      "ST-LC-0114",
      "ST-LC-0115",
      "ST-LC-0116",
      "ST-LC-0117",
      "ST-LC-0118",
      "ST-LC-0119",
      "ST-LC-0120",
      "ST-LC-0107"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "ALL原文对全部条目的要求未被实现例外替换",
    "operation_ids": [
      "ST-LC-0121"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "正式ALL包含NOT_USED/PERMOFF与代码跳过例外、LC4009.1的冲突待裁决；不宣称代码流程全满足ALL原文。",
    "operation_ids": [],
    "status": "pending-interpretation",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0501",
      "ST-LC-0540"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：正式ALL包含NOT_USED/PERMOFF与代码跳过例外、LC4009.1的冲突待裁决；不宣称代码流程全满足ALL原文。<br>已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0042

**NASA 原始 ID**：LC4007

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Set Actionpoint to Disabled Command, LC shall set the state for the command-specified Actionpoint to DISABLED such that the actionpoints are not evaluated and no actions are taken.

**原始理由/补充说明**：Disable an action point so that no evaluation is performed for the particular actionpoint.  Heritage from LRO, SDO.

**规范化中文需求**：收到命令后将指定单个AP置为DISABLED；原文义务与当前例外分别保留。

**触发/条件**：长度正确的指定地面状态命令到达

**输入**：合法APNumber、NewAPState=LC_APSTATE_DISABLED

**输出**：AP.CurrentState_new、成功/拒绝计数及命令事件

**状态与历史**：ART单项CurrentState；应用状态不变

**处理及约束**：该AP不采样、不采取动作；原LC4008还禁止AP事件。<br>实现仅修改原状态不是NOT_USED/PERMOFF的AP；单个禁止项命令拒绝，全选略过禁止项但命令整体接受。<br>永久禁用保护对应LC4009.1；NOT_USED例外与“all”字面需统一口径。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L97–97 LC4007<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L353–474 LC_SetAPStateCmd<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L89–108 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0025<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0112<br>RES-LC-0113<br>RES-LC-0114<br>RES-LC-0115<br>RES-LC-0116<br>RES-LC-0117<br>RES-LC-0118<br>RES-LC-0119<br>RES-LC-0120<br>RES-LC-0121<br>RES-LC-0501<br>RES-LC-0540<br>RES-LC-0541<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0006<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0112<br>ST-LC-0113<br>ST-LC-0114<br>ST-LC-0115<br>ST-LC-0116<br>ST-LC-0117<br>ST-LC-0118<br>ST-LC-0119<br>ST-LC-0120<br>ST-LC-0121<br>ST-LC-0501<br>ST-LC-0540<br>ST-LC-0541<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8076<br>ST-LC-8077<br>ST-LC-8078<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：单项命令在NOT_USED/PERMOFF拒绝；PERMOFF保护有LC4009.1正式依据，NOT_USED视作不可用条目，另有补充。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0501<br>ST-LC-0540

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "合法状态/索引和当前条目门控，单选或有限ALL遍历赋值，结束成功或拒绝提交",
    "operation_ids": [
      "ST-LC-0112",
      "ST-LC-0113",
      "ST-LC-0114",
      "ST-LC-0115",
      "ST-LC-0116",
      "ST-LC-0117",
      "ST-LC-0118",
      "ST-LC-0119",
      "ST-LC-0120",
      "ST-LC-0107"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0501",
      "ST-LC-0540"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "单项原文按指定AP赋值的义务与NOT_USED/PERMOFF实现拒绝被分离保留",
    "operation_ids": [
      "ST-LC-0121"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "正式单项状态命令未声明NOT_USED/PERMOFF例外，代码单选拒绝；激活PERMOFF另受LC4009.1约束，需需求裁决。",
    "operation_ids": [],
    "status": "pending-interpretation",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。<br>正式单项状态命令未声明NOT_USED/PERMOFF例外，代码单选拒绝；激活PERMOFF另受LC4009.1约束，需需求裁决。

## REQ-LC-0043

**NASA 原始 ID**：LC4008

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Set All Actionpoints to Disabled Command, LC shall set the state for all Actionpoint to DISABLED such that:
a)	the actionpoints are not evaluated
b)	no actions are taken
c)	no event messages generated.

**原始理由/补充说明**：Provides the ability to “turn off” all actionpoint evaluations.  Heritage from LRO, SDO.

**规范化中文需求**：收到命令后将全部AP置为DISABLED；原文义务与当前例外分别保留。

**触发/条件**：长度正确的指定地面状态命令到达

**输入**：APNumber=LC_ALL_ACTIONPOINTS、NewAPState=LC_APSTATE_DISABLED

**输出**：AP.CurrentState_new、成功/拒绝计数及命令事件

**状态与历史**：ART单项CurrentState；应用状态不变

**处理及约束**：该AP不采样、不采取动作；原LC4008还禁止AP事件。<br>实现仅修改原状态不是NOT_USED/PERMOFF的AP；单个禁止项命令拒绝，全选略过禁止项但命令整体接受。<br>永久禁用保护对应LC4009.1；NOT_USED例外与“all”字面需统一口径。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L98–101 LC4008<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L353–474 LC_SetAPStateCmd<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L89–108 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0025<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0112<br>RES-LC-0113<br>RES-LC-0114<br>RES-LC-0115<br>RES-LC-0116<br>RES-LC-0117<br>RES-LC-0118<br>RES-LC-0119<br>RES-LC-0120<br>RES-LC-0121<br>RES-LC-0501<br>RES-LC-0540<br>RES-LC-0541<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0006<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0112<br>ST-LC-0113<br>ST-LC-0114<br>ST-LC-0115<br>ST-LC-0116<br>ST-LC-0117<br>ST-LC-0118<br>ST-LC-0119<br>ST-LC-0120<br>ST-LC-0121<br>ST-LC-0501<br>ST-LC-0540<br>ST-LC-0541<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8076<br>ST-LC-8077<br>ST-LC-8078<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0008

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：conflict

**检查层次**：static<br>manual

**人工语义核对**：“all”源码实际为全部可修改AP，排除NOT_USED/PERMOFF；保留原文，等待确认该量词范围。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0501<br>ST-LC-0540

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "合法状态/索引和当前条目门控，单选或有限ALL遍历赋值，结束成功或拒绝提交",
    "operation_ids": [
      "ST-LC-0112",
      "ST-LC-0113",
      "ST-LC-0114",
      "ST-LC-0115",
      "ST-LC-0116",
      "ST-LC-0117",
      "ST-LC-0118",
      "ST-LC-0119",
      "ST-LC-0120",
      "ST-LC-0107"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "ALL原文对全部条目的要求未被实现例外替换",
    "operation_ids": [
      "ST-LC-0121"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "正式ALL包含NOT_USED/PERMOFF与代码跳过例外、LC4009.1的冲突待裁决；不宣称代码流程全满足ALL原文。",
    "operation_ids": [],
    "status": "pending-interpretation",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0501",
      "ST-LC-0540"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：正式ALL包含NOT_USED/PERMOFF与代码跳过例外、LC4009.1的冲突待裁决；不宣称代码流程全满足ALL原文。<br>已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0044

**NASA 原始 ID**：LC4009

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Set Actionpoint to Permanent Disable, LC shall mark the command-specified Actionpoint such that the Actionpoint cannot be Activated.

**原始理由/补充说明**：Useful for separation sequences or other actionpoints that should only be active for a limited period of time and never re-enabled by the ground.  Heritage from LRO.

**规范化中文需求**：收到 Permanent Disable 命令后，使指定AP不能再被Activated。

**触发/条件**：长度正确的指定地面状态命令到达

**输入**：APNumber、旧CurrentState

**输出**：CurrentState=PERMOFF或拒绝事件/计数

**状态与历史**：单AP CurrentState

**处理及约束**：不能全选；APNumber必须<MAX。<br>实现要求先DISABLED才允许转PERMOFF；原文未给前置DISABLED条件。<br>仅记录逻辑永久关闭，定义表重新加载/未恢复CDS重启仍可重新初始化。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L102–102 LC4009<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L481–537 LC_SetAPPermOffCmd

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0025<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0122<br>RES-LC-0123<br>RES-LC-0124<br>RES-LC-0125<br>RES-LC-0501<br>RES-LC-0542<br>RES-LC-0543<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0006<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0122<br>ST-LC-0123<br>ST-LC-0124<br>ST-LC-0125<br>ST-LC-0501<br>ST-LC-0542<br>ST-LC-0543<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8035<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0008<br>ISSUE-LC-0016

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：conflict

**检查层次**：static<br>manual

**人工语义核对**：前置DISABLED规则在代码可证，但正式本条无此条件；不得偷偷加进正式原文。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0501<br>ST-LC-0542

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "单AP置PERMOFF的实现及无Disabled前置原文义务分离",
    "operation_ids": [
      "ST-LC-0122",
      "ST-LC-0123",
      "ST-LC-0124",
      "ST-LC-0125",
      "ST-LC-0107"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "LC4009未规定原状态必须Disabled，而代码规定此门控；需需求裁决。",
    "operation_ids": [],
    "status": "pending-interpretation",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0501",
      "ST-LC-0542"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：LC4009未规定原状态必须Disabled，而代码规定此门控；需需求裁决。<br>已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0045

**NASA 原始 ID**：LC4009.1

**来源类别**：documented

**原始文字/行为**：If a command is received to Activate an Actionpoint which has been permanently disabled, the command shall be rejected.

**原始理由/补充说明**：The only way to activate a permanently disabled actionpoint is to restart LC application or load a new Actionpoint table.  Note that the restart of the LC application will only activate this Actionpoint if the Save Critical Data  parameter is set to “No” (see LC9005).  Heritage from LRO.

**规范化中文需求**：对已永久禁用AP的激活命令必须拒绝。

**触发/条件**：单AP激活命令到达，旧状态PERMOFF

**输入**：APNumber、NewAPState=ACTIVE、ART旧状态

**输出**：拒绝事件、CmdErrCount加一；PERMOFF保留

**状态与历史**：单AP CurrentState

**处理及约束**：PERMOFF不能通过常规SetAPState改任何可操作态。<br>全选激活略过PERMOFF且整体接受；原文a command量词是否涵盖全选激活需要裁定。<br>重载ADT或不恢复CDS的重启可按默认状态初始化，非永不可恢复物理状态。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L103–103 LC4009.1<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L389–439 LC_SetAPStateCmd<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L589–611 LC_ResetResultsAP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0025<br>RES-LC-0102<br>RES-LC-0103<br>RES-LC-0104<br>RES-LC-0107<br>RES-LC-0116<br>RES-LC-0118<br>RES-LC-0121<br>RES-LC-0124<br>RES-LC-0500<br>RES-LC-0542<br>RES-LC-0543<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0006<br>ST-LC-0102<br>ST-LC-0103<br>ST-LC-0104<br>ST-LC-0107<br>ST-LC-0116<br>ST-LC-0118<br>ST-LC-0121<br>ST-LC-0124<br>ST-LC-0500<br>ST-LC-0542<br>ST-LC-0543<br>ST-LC-8019<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8076<br>ST-LC-8077<br>ST-LC-8078<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0008

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：conflict

**检查层次**：static<br>manual

**人工语义核对**：单项拒绝支持；全选涉及PERMOFF时不是整体拒绝，是保持该项不变。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0500<br>ST-LC-0542

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "PERMOFF单项激活被拒绝、ALL不改该条目",
    "operation_ids": [
      "ST-LC-0116",
      "ST-LC-0118",
      "ST-LC-0102",
      "ST-LC-0103",
      "ST-LC-0104",
      "ST-LC-0107",
      "ST-LC-0500"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0500",
      "ST-LC-0542"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0046

**NASA 原始 ID**：LC4010

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Reset Actionpoint Statistics Command, LC shall set to zero, all of the following Actionpoint Statistics for the command-specified Actionpoints:
a)	Total number of FAIL to PASS transitions
b)	Total number of PASS to FAIL transitions
c)	Number of consecutive FAIL results
d)	Total number of FAIL results
e)	Total number of RTS executions
f)	Total number of event messages sent  relating to that Actionpoint

**原始理由/补充说明**：Provides ability to start monitoring “from scratch”.  Heritage from LRO, SDO.

**规范化中文需求**：重置指定AP的六类统计，保留AP状态和最近结果。

**触发/条件**：长度正确的Reset AP Statistics命令到达

**输入**：APNumber<LC_MAX_ACTIONPOINTS

**输出**：FailToPassCount、PassToFailCount、ConsecutiveFailCount、CumulativeFailCount、CumulativeRTSExecCount、CumulativeEventMsgsSent全部0，另清PassiveAPCount

**状态与历史**：ART单项或全部；CurrentState和ActionResult不变

**处理及约束**：全选或单项范围均通过LC_ResetResultsAP(...,true)。<br>AP状态/结果仅false初始化模式修改，不因统计重置改变。<br>错误AP号拒绝并增CmdErrCount；成功增CmdCount并发确认事件。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L104–110 LC4010<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L544–611 LC_ResetAPStatsCmd / LC_ResetResultsAP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0026<br>RES-LC-0102<br>RES-LC-0103<br>RES-LC-0104<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0126<br>RES-LC-0127<br>RES-LC-0128<br>RES-LC-0129<br>RES-LC-0130<br>RES-LC-0132<br>RES-LC-0500<br>RES-LC-0501<br>RES-LC-0544<br>RES-LC-0545<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0007<br>ST-LC-0102<br>ST-LC-0103<br>ST-LC-0104<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0126<br>ST-LC-0127<br>ST-LC-0128<br>ST-LC-0129<br>ST-LC-0130<br>ST-LC-0132<br>ST-LC-0500<br>ST-LC-0501<br>ST-LC-0544<br>ST-LC-0545<br>ST-LC-8019<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8042<br>ST-LC-8043<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0500<br>ST-LC-0501<br>ST-LC-0544

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0500",
      "ST-LC-0501",
      "ST-LC-0544"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "解析有效单项/ALL，逐AP复位六项正式统计及PassiveAPCount，保留模式/最近结果，计数/错误路径显式",
    "operation_ids": [
      "ST-LC-0126",
      "ST-LC-0127",
      "ST-LC-0128",
      "ST-LC-0130",
      "ST-LC-0132",
      "ST-LC-0105",
      "ST-LC-0106",
      "ST-LC-0102",
      "ST-LC-0103",
      "ST-LC-0104",
      "ST-LC-0107",
      "ST-LC-0500",
      "ST-LC-0501"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0047

**NASA 原始 ID**：LC4011

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Reset All Actionpoint Statistics Command, LC shall set to zero, all of the following Actionpoint Statistics for all Actionpoints:
a)	Total number of FAIL to PASS transitions
b)	Total number of PASS to FAIL transitions
c)	Number of consecutive FAIL results
d)	Total number of FAIL results
e)	Total number of RTS executions
f)	Total number of event messages sent relating to that Actionpoint

**原始理由/补充说明**：Provides ability to start monitoring “from scratch”.  Heritage from LRO, SDO.

**规范化中文需求**：重置所有AP的六类统计，保留AP状态和最近结果。

**触发/条件**：长度正确的Reset AP Statistics命令到达

**输入**：APNumber=LC_ALL_ACTIONPOINTS

**输出**：FailToPassCount、PassToFailCount、ConsecutiveFailCount、CumulativeFailCount、CumulativeRTSExecCount、CumulativeEventMsgsSent全部0，另清PassiveAPCount

**状态与历史**：ART单项或全部；CurrentState和ActionResult不变

**处理及约束**：全选或单项范围均通过LC_ResetResultsAP(...,true)。<br>AP状态/结果仅false初始化模式修改，不因统计重置改变。<br>错误AP号拒绝并增CmdErrCount；成功增CmdCount并发确认事件。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L111–117 LC4011<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L544–611 LC_ResetAPStatsCmd / LC_ResetResultsAP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0026<br>RES-LC-0102<br>RES-LC-0103<br>RES-LC-0104<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0126<br>RES-LC-0127<br>RES-LC-0128<br>RES-LC-0129<br>RES-LC-0130<br>RES-LC-0132<br>RES-LC-0500<br>RES-LC-0501<br>RES-LC-0544<br>RES-LC-0545<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0007<br>ST-LC-0102<br>ST-LC-0103<br>ST-LC-0104<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0126<br>ST-LC-0127<br>ST-LC-0128<br>ST-LC-0129<br>ST-LC-0130<br>ST-LC-0132<br>ST-LC-0500<br>ST-LC-0501<br>ST-LC-0544<br>ST-LC-0545<br>ST-LC-8019<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8042<br>ST-LC-8043<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0500<br>ST-LC-0501<br>ST-LC-0544

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0500",
      "ST-LC-0501",
      "ST-LC-0544"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "解析有效单项/ALL，逐AP复位六项正式统计及PassiveAPCount，保留模式/最近结果，计数/错误路径显式",
    "operation_ids": [
      "ST-LC-0126",
      "ST-LC-0127",
      "ST-LC-0128",
      "ST-LC-0130",
      "ST-LC-0132",
      "ST-LC-0105",
      "ST-LC-0106",
      "ST-LC-0102",
      "ST-LC-0103",
      "ST-LC-0104",
      "ST-LC-0107",
      "ST-LC-0500",
      "ST-LC-0501"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0048

**NASA 原始 ID**：LC4012

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Reset Watchpoint Statistics Command, LC shall set to zero all of the following Watchpoint Statistics for the command-specified Watchpoints:
a)	Total sample count for this watchpoint
b)	Number of times result transitioned from FALSE to TRUE
c)	Number of consecutive TRUE results
d)	Total number of TRUE results
e)	Most recent FALSE to TRUE transition value
f)	Most recent FALSE to TRUE transition timestamp
g)	Most recent TRUE to FALSE transition value
h)	Most recent TRUE to FALSE transition timestamp

**原始理由/补充说明**：Provides ability to start monitoring “from scratch”.  Heritage from LRO, SDO.

**规范化中文需求**：重置指定WP的八类统计，保留最近结果和age倒计数。

**触发/条件**：长度正确的Reset Watchpoint Statistics命令到达

**输入**：WPNumber<LC_MAX_WATCHPOINTS

**输出**：EvaluationCount、FalseToTrueCount、ConsecutiveTrueCount、CumulativeTrueCount和两向最近跨越值/时间全部0

**状态与历史**：WRT单项或全部；WatchResult/CountdownToStale保持

**处理及约束**：全选或单项调用LC_ResetResultsWP(...,true)。<br>不把最近结果改STALE，也不清倒计数；初始化/表换新才使用false模式。<br>错误WP号拒绝并增CmdErrCount；成功增CmdCount并发确认事件。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L118–126 LC4012<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L619–691 LC_ResetWPStatsCmd / LC_ResetResultsWP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0026<br>RES-LC-0102<br>RES-LC-0103<br>RES-LC-0104<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0126<br>RES-LC-0127<br>RES-LC-0128<br>RES-LC-0129<br>RES-LC-0131<br>RES-LC-0132<br>RES-LC-0500<br>RES-LC-0501<br>RES-LC-0544<br>RES-LC-0545<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0007<br>ST-LC-0102<br>ST-LC-0103<br>ST-LC-0104<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0126<br>ST-LC-0127<br>ST-LC-0128<br>ST-LC-0129<br>ST-LC-0131<br>ST-LC-0132<br>ST-LC-0500<br>ST-LC-0501<br>ST-LC-0544<br>ST-LC-0545<br>ST-LC-8019<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8042<br>ST-LC-8043<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0500<br>ST-LC-0501<br>ST-LC-0544

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0500",
      "ST-LC-0501",
      "ST-LC-0544"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "解析有效单项/ALL，逐WP复位八类统计，保留最近结果/CountdownToStale，计数/错误路径显式",
    "operation_ids": [
      "ST-LC-0126",
      "ST-LC-0127",
      "ST-LC-0128",
      "ST-LC-0131",
      "ST-LC-0132",
      "ST-LC-0105",
      "ST-LC-0106",
      "ST-LC-0102",
      "ST-LC-0103",
      "ST-LC-0104",
      "ST-LC-0107",
      "ST-LC-0500",
      "ST-LC-0501"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0049

**NASA 原始 ID**：LC4013

**来源类别**：documented

**原始文字/行为**：Upon receipt of a Reset All Watchpoint Statistics Command, LC shall set to zero, all of the following Watchpoint Statistics for all Watchpoints:
a)	Total sample count for this watchpoint
b)	Number of times result transitioned from FALSE to TRUE
c)	Number of consecutive TRUE results
d)	Total number of TRUE results
e)	Most recent FALSE to TRUE transition value
f)	Most recent FALSE to TRUE transition timestamp
g)	Most recent TRUE to FALSE transition value
h)	Most recent TRUE to FALSE transition timestamp

**原始理由/补充说明**：Provides ability to start monitoring “from scratch”.  Heritage from LRO, SDO.

**规范化中文需求**：重置所有WP的八类统计，保留最近结果和age倒计数。

**触发/条件**：长度正确的Reset Watchpoint Statistics命令到达

**输入**：WPNumber=LC_ALL_WATCHPOINTS

**输出**：EvaluationCount、FalseToTrueCount、ConsecutiveTrueCount、CumulativeTrueCount和两向最近跨越值/时间全部0

**状态与历史**：WRT单项或全部；WatchResult/CountdownToStale保持

**处理及约束**：全选或单项调用LC_ResetResultsWP(...,true)。<br>不把最近结果改STALE，也不清倒计数；初始化/表换新才使用false模式。<br>错误WP号拒绝并增CmdErrCount；成功增CmdCount并发确认事件。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L127–135 LC4013<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L619–691 LC_ResetWPStatsCmd / LC_ResetResultsWP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0026<br>RES-LC-0102<br>RES-LC-0103<br>RES-LC-0104<br>RES-LC-0105<br>RES-LC-0106<br>RES-LC-0107<br>RES-LC-0126<br>RES-LC-0127<br>RES-LC-0128<br>RES-LC-0129<br>RES-LC-0131<br>RES-LC-0132<br>RES-LC-0500<br>RES-LC-0501<br>RES-LC-0544<br>RES-LC-0545<br>RES-LC-0701<br>RES-LC-0702

**ST**：ST-LC-0007<br>ST-LC-0102<br>ST-LC-0103<br>ST-LC-0104<br>ST-LC-0105<br>ST-LC-0106<br>ST-LC-0107<br>ST-LC-0126<br>ST-LC-0127<br>ST-LC-0128<br>ST-LC-0129<br>ST-LC-0131<br>ST-LC-0132<br>ST-LC-0500<br>ST-LC-0501<br>ST-LC-0544<br>ST-LC-0545<br>ST-LC-8019<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8042<br>ST-LC-8043<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0500<br>ST-LC-0501<br>ST-LC-0544

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0500",
      "ST-LC-0501",
      "ST-LC-0544"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "解析有效单项/ALL，逐WP复位八类统计，保留最近结果/CountdownToStale，计数/错误路径显式",
    "operation_ids": [
      "ST-LC-0126",
      "ST-LC-0127",
      "ST-LC-0128",
      "ST-LC-0131",
      "ST-LC-0132",
      "ST-LC-0105",
      "ST-LC-0106",
      "ST-LC-0102",
      "ST-LC-0103",
      "ST-LC-0104",
      "ST-LC-0107",
      "ST-LC-0500",
      "ST-LC-0501"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0050

**NASA 原始 ID**：LC8000

**来源类别**：documented

**原始文字/行为**：LC shall generate a housekeeping message containing the following:
a)	Valid  Command Counter
b)	Command Rejected Counter
c)	Passive RTS Execution Counter (Total count of RTS sequences not initiated because either the LC application state or the state of the actionpoint that failed is set to Passive) 
d)	Current LC Application State (LC_ACTIVE, LC_PASSIVE, LC_DISABLED)...
e)	Total count of actionpoints sampled while LC_ACTIVE or LC_PASSIVE...
f)	Total count of packets monitored for watchpoints (cmd and tlm)
g)	RTS Execution Counter (Total count of commands sent to SC task to start an RTS)
h)	Selected data from watchpoint results table
i)	Selected data from actionpoint results table

**原始理由/补充说明**：Housekeeping telemetry to indicate basic LC status.  Heritage from LRO, loosely SDO.

**规范化中文需求**：生成包含六项计数、应用状态、WRT和ART选定信息的housekeeping消息。

**触发/条件**：LC_SEND_HK_MID内部请求通过长度验证

**输入**：LC_AppData计数/应用状态、WRT结果、ART状态/结果

**输出**：LC_HkTlm包及框架时间戳；随后维护状态

**状态与历史**：HkPacket及应用/WRT/ART快照

**处理及约束**：复制CmdCount/CmdErrCount/PassiveRTSExecCount/APSampleCount/MonitoredMsgCount/RTSExecCount与CurrentLCState。<br>WP四结果每项2位；AP结果2位+状态2位，每项4位。<br>PERMOFF在HK压缩状态编码为NOT_USED；完整ART dump可区分。<br>另外报告WPsInUse和ActiveAPs；发送后运行LC_PerformMaintenance。<br>独立HK入口读取前一监测/采样完成后的最新持久AppData/WRT/ART；先报告再维护，不能由监测或采样无条件自动触发。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L136–145 LC8000<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L114–260 LC_SendHkCmd

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0030<br>RES-LC-0133<br>RES-LC-0134<br>RES-LC-0135<br>RES-LC-0136<br>RES-LC-0137<br>RES-LC-0138<br>RES-LC-0139<br>RES-LC-0140<br>RES-LC-0141<br>RES-LC-0142<br>RES-LC-0143<br>RES-LC-0524<br>RES-LC-0532<br>RES-LC-0533<br>RES-LC-0700<br>RES-LC-0701

**ST**：ST-LC-0011<br>ST-LC-0133<br>ST-LC-0134<br>ST-LC-0135<br>ST-LC-0136<br>ST-LC-0137<br>ST-LC-0138<br>ST-LC-0139<br>ST-LC-0140<br>ST-LC-0141<br>ST-LC-0142<br>ST-LC-0143<br>ST-LC-0524<br>ST-LC-0532<br>ST-LC-0533<br>ST-LC-8022<br>ST-LC-8023<br>ST-LC-8024<br>ST-LC-9000

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：HK字段和打包明确；CFE_SB_TransmitMsg返回值未检查，不证明外部接收。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。 本轮补全：独立HK入口读取前一监测/采样完成后的最新持久AppData/WRT/ART；先报告再维护，不能由监测或采样无条件自动触发。 完整行为合同仍不构成官方事件/服务语法验收，mapping保持原评定。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0524<br>ST-LC-0532

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "HK六计数、CurrentLCState、WPsInUse快照",
    "operation_ids": [
      "ST-LC-0133",
      "ST-LC-0141"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "WP二位打包、AP四位状态/结果打包和ActiveAPs计算",
    "operation_ids": [
      "ST-LC-0134",
      "ST-LC-0135",
      "ST-LC-0136",
      "ST-LC-0137",
      "ST-LC-0138",
      "ST-LC-0139",
      "ST-LC-0140",
      "ST-LC-0141"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "HK时间戳/发送顺序的描述",
    "operation_ids": [
      "ST-LC-0142",
      "ST-LC-0143",
      "ST-LC-0524"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "独立HK消息入口及CFE_SB_TimeStampMsg/TransmitMsg真实调用的论文资源语法绑定待确认；意图不表示已发送。",
    "operation_ids": [
      "ST-LC-0524",
      "ST-LC-0532"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：独立HK消息入口及CFE_SB_TimeStampMsg/TransmitMsg真实调用的论文资源语法绑定待确认；意图不表示已发送。

## REQ-LC-0051

**NASA 原始 ID**：LC9000

**来源类别**：documented

**原始文字/行为**：Upon cFE Power-On LC shall initialize the following Housekeeping data to Zero (or value specified):
a)	Valid Command Counter
b)	Command Rejected Counter
c)	Passive RTS Execution Counter
d)	Current LC State to <PLATFORM_DEFINED> Default Power-on State
e)	Actionpoint Sample Count
f)	TLM Count
g)	RTS Execution Counter
h)	Watch Results (bitmapped)
i)	Action Results (bitmapped)

**原始理由/补充说明**：Need to initialize values to a default state on cFE Power-on reset.  Derived requirement.

**规范化中文需求**：cFE Power-On 初始化六项计数、平台默认应用状态以及bitmapped WP/AP结果。

**触发/条件**：cFE Power-On/无法完全恢复CDS后的默认初始化

**输入**：平台LC_STATE_POWER_ON_RESET、默认WDT/ADT

**输出**：清零计数、初始应用状态和HK初始化缓冲

**状态与历史**：LC_AppData及HkPacket，运行后从WRT/ART重新打包结果

**处理及约束**：LC_AppInit先清零OperData/AppData；LC_LoadDefaultTables再清计数并设POWER_ON状态。<br>默认WP/AP结果实际STALE，正式bitmapped初值zero与STALE编码需分别表述：HK缓冲初0，首次HK按STALE打包。<br>平台状态为可变配置，不捏造任务实际选值。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L146–155 LC9000<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L187–216 LC_AppInit<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L991–1011 LC_LoadDefaultTables<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L301–310 LC_ResetCounters

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0026<br>RES-LC-0029<br>RES-LC-0032<br>RES-LC-0108<br>RES-LC-0144<br>RES-LC-0145<br>RES-LC-0155<br>RES-LC-0156<br>RES-LC-0159<br>RES-LC-0160<br>RES-LC-0163<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0705

**ST**：ST-LC-0007<br>ST-LC-0010<br>ST-LC-0013<br>ST-LC-0108<br>ST-LC-0144<br>ST-LC-0145<br>ST-LC-0155<br>ST-LC-0156<br>ST-LC-0159<br>ST-LC-0160<br>ST-LC-0163<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8025<br>ST-LC-8027<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8030<br>ST-LC-8031<br>ST-LC-8040<br>ST-LC-8041<br>ST-LC-9004

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0558

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "六计数、平台PowerOn模式和HK位图0初始化",
    "operation_ids": [
      "ST-LC-0144",
      "ST-LC-0145",
      "ST-LC-0155",
      "ST-LC-0156",
      "ST-LC-0159",
      "ST-LC-0160"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
    "operation_ids": [
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。

## REQ-LC-0052

**NASA 原始 ID**：LC9001

**来源类别**：documented

**原始文字/行为**：Upon cFE Power-On LC shall initialize the following Watchpoint data to Zero (or value specified) for all Watchpoints:
a)	The result of the last watchpoint relational comparison to STALE
b)	The number of times this Watchpoint has been compared
c)	The number of times this Watchpoint has crossed from the False to True result
d)	The number of consecutive times the comparison has yielded a True result
e)	The cumulative number of times the comparison has yielded a True result
f)	The value that caused the last False-to-True crossing, and the crossing time stamp
g)	The value that caused the last True-to-False crossing, and the crossing time stamp

**原始理由/补充说明**：Power on reset behavior for watchpoint data

**规范化中文需求**：Power-On 将所有WP结果置STALE，比较/连续/累计统计和两向跨越值/时间清零。

**触发/条件**：默认初始化或WDT换新触发WRT初始化

**输入**：WRT容量

**输出**：WatchResult=STALE、CountdownToStale=0、要求的WP统计全0

**状态与历史**：WRT全部项

**处理及约束**：以LC_ResetResultsWP(0,MAX-1,false)完成初始化。<br>最近跨越类型字段未被本工具显式重置，默认初分配WRT为0；本条要求值/时间而非DataType。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L156–163 LC9001<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L994–997 LC_LoadDefaultTables<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L664–691 LC_ResetResultsWP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0026<br>RES-LC-0029<br>RES-LC-0032<br>RES-LC-0144<br>RES-LC-0155<br>RES-LC-0156<br>RES-LC-0157<br>RES-LC-0160<br>RES-LC-0163<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0705

**ST**：ST-LC-0007<br>ST-LC-0010<br>ST-LC-0013<br>ST-LC-0144<br>ST-LC-0155<br>ST-LC-0156<br>ST-LC-0157<br>ST-LC-0160<br>ST-LC-0163<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8025<br>ST-LC-8027<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8030<br>ST-LC-8031

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0006

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0558

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "所有WP初值STALE、年龄0、统计与两向记录0",
    "operation_ids": [
      "ST-LC-0157",
      "ST-LC-0160"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
    "operation_ids": [
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。

## REQ-LC-0053

**NASA 原始 ID**：LC9002

**来源类别**：documented

**原始文字/行为**：Upon cFE Power-On LC shall initialize the following Actionpoint data to Zero (or value specified) for all Actionpoints:
a)	The result of the last Actionpoint Sample to STALE
b)	The current state as defined in the ADT
c)	The number of times this Actionpoint has crossed from the Fail to Pass state
d)	The number of times this Actionpoint has crossed from the Pass to Fail state
e)	The number of consecutive times the equation result = Failed
f)	The cumulative number of times the equation result = Failed
g)	The cumulative count of the RTS executions
h)	Total number of event messages sent

**原始理由/补充说明**：Power on reset behavior for actionpoint data

**规范化中文需求**：Power-On 将所有AP结果置STALE，状态取ADT.DefaultState，六类统计归零。

**触发/条件**：默认初始化或ADT换新触发ART初始化

**输入**：ADT.DefaultState、ART容量

**输出**：ActionResult=STALE、CurrentState=DefaultState、统计全0

**状态与历史**：ART全部项

**处理及约束**：以LC_ResetResultsAP(0,MAX-1,false)初始化。<br>新表默认PERMOFF也是合法状态；不强行将所有AP激活。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L164–172 LC9002<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L999–1000 LC_LoadDefaultTables<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L589–611 LC_ResetResultsAP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0026<br>RES-LC-0029<br>RES-LC-0032<br>RES-LC-0144<br>RES-LC-0155<br>RES-LC-0156<br>RES-LC-0158<br>RES-LC-0160<br>RES-LC-0163<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0705

**ST**：ST-LC-0007<br>ST-LC-0010<br>ST-LC-0013<br>ST-LC-0144<br>ST-LC-0155<br>ST-LC-0156<br>ST-LC-0158<br>ST-LC-0160<br>ST-LC-0163<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8025<br>ST-LC-8027<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8030<br>ST-LC-8031

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0558

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "所有AP初值STALE、真实ADT默认状态、统计0",
    "operation_ids": [
      "ST-LC-0158",
      "ST-LC-0160"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
    "operation_ids": [
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。

## REQ-LC-0054

**NASA 原始 ID**：LC9003

**来源类别**：documented

**原始文字/行为**：Upon a cFE Processor Reset or LC Application Reset,  if the <PLATFORM_DEFINED> Save Critical Data parameter is set to NO, LC shall perform the same initialization as a cFE Power-on (see LC9000, LC9001, LC9002, and LC9003)

**原始理由/补充说明**：Configuration parameter indicates if data should be saved across a cFE Processor Reset or LC Application Reset.

**规范化中文需求**：Processor Reset/LC App Reset 且不保存Critical Data时，采用Power-On等价初始化。

**触发/条件**：Processor/App reset启动；LC_SAVE_TO_CDS未启用

**输入**：默认WDT/ADT、POWER_ON配置

**输出**：与LC9000/9001/9002相同初值

**状态与历史**：无恢复的AppData/WRT/ART/WDT/ADT

**处理及约束**：LC_SAVE_TO_CDS是编译期开关，以是否defined判断；默认未定义。<br>无完整五对象恢复标志时走默认初始化。<br>原文末尾自引用LC9003保留为原文文档问题，不执行递归初始化。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L173–173 LC9003<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L386–478 LC_TableInit<br>[evidence/LC/fsw/inc/lc_internal_cfg.h](evidence/LC/fsw/inc/lc_internal_cfg.h) L88–102 LC_SAVE_TO_CDS

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0026<br>RES-LC-0029<br>RES-LC-0032<br>RES-LC-0108<br>RES-LC-0144<br>RES-LC-0145<br>RES-LC-0155<br>RES-LC-0156<br>RES-LC-0157<br>RES-LC-0158<br>RES-LC-0159<br>RES-LC-0160<br>RES-LC-0163<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0705

**ST**：ST-LC-0007<br>ST-LC-0010<br>ST-LC-0013<br>ST-LC-0108<br>ST-LC-0144<br>ST-LC-0145<br>ST-LC-0155<br>ST-LC-0156<br>ST-LC-0157<br>ST-LC-0158<br>ST-LC-0159<br>ST-LC-0160<br>ST-LC-0163<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8025<br>ST-LC-8027<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8030<br>ST-LC-8031<br>ST-LC-8040<br>ST-LC-8041<br>ST-LC-9004

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0558

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "保存CriticalData=NO的两种复位选择上电等价初始化",
    "operation_ids": [
      "ST-LC-0144",
      "ST-LC-0145",
      "ST-LC-0155",
      "ST-LC-0156",
      "ST-LC-0157",
      "ST-LC-0158",
      "ST-LC-0159",
      "ST-LC-0160"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
    "operation_ids": [
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。

## REQ-LC-0055

**NASA 原始 ID**：LC9004

**来源类别**：documented

**原始文字/行为**：Upon a cFE Processor Reset or LC Application Reset,  if the <PLATFORM_DEFINED> Save Critical Data parameter is set to YES, LC shall  restore the following data:
a)	LC housekeeping data
b)	WDT
c)	Watchpoint Statistics
d)	ADT
e)	Actionpoint Statistics

**原始理由/补充说明**：Provides ability to “fly thru” a cFE processor reset or LC Application reset.

**规范化中文需求**：Reset 且保存Critical Data开启时，应恢复HK数据、WDT、WP统计、ADT、AP统计。

**触发/条件**：启用CDS的Processor/App reset初始化

**输入**：cFE CDS三LC区和两个critical表

**输出**：恢复AppData/WRT/ART/WDT/ADT，或整套默认初始化

**状态与历史**：五对象恢复标志及HaveActiveCDS

**处理及约束**：必须五项全部恢复才采用恢复数据；部分成功不能混新旧。<br>LC显式管理AppData/WRT/ART；WDT/ADT恢复由cFE critical表服务负责。<br>创建CDS或critical表失败会禁用CDS并继续默认启动，真实持续保存能力不能假定。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L174–179 LC9004<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L350–521 LC_TableInit<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L613–769 LC_CreateDefinitionTables<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L777–902 LC_CreateTaskCDS

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0014<br>RES-LC-0029<br>RES-LC-0032<br>RES-LC-0144<br>RES-LC-0146<br>RES-LC-0147<br>RES-LC-0148<br>RES-LC-0149<br>RES-LC-0150<br>RES-LC-0151<br>RES-LC-0160<br>RES-LC-0161<br>RES-LC-0163<br>RES-LC-0550<br>RES-LC-0551<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0704<br>RES-LC-0705

**ST**：ST-LC-0010<br>ST-LC-0013<br>ST-LC-0144<br>ST-LC-0146<br>ST-LC-0147<br>ST-LC-0148<br>ST-LC-0149<br>ST-LC-0150<br>ST-LC-0151<br>ST-LC-0160<br>ST-LC-0161<br>ST-LC-0163<br>ST-LC-0550<br>ST-LC-0551<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8025<br>ST-LC-8027<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8030<br>ST-LC-8031<br>ST-LC-9013<br>ST-LC-9014<br>ST-LC-9015

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0018

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：LC代码覆盖恢复路径；完整恢复行为依赖未固定cFE且没有运行证明。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0550<br>ST-LC-0558

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "保存开启的复位核对五对象全或无、分别接收恢复数据",
    "operation_ids": [
      "ST-LC-0144",
      "ST-LC-0146",
      "ST-LC-0147",
      "ST-LC-0148",
      "ST-LC-0149",
      "ST-LC-0150",
      "ST-LC-0151",
      "ST-LC-0160"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
    "operation_ids": [
      "ST-LC-0550",
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "源码CriticalData有效性依赖cFE恢复返回及APP保存标志；全部初始化的validation callback保证未由LC源代码单独证明，需核实依赖版本/保证。",
    "operation_ids": [],
    "status": "pending-interpretation",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。<br>源码CriticalData有效性依赖cFE恢复返回及APP保存标志；全部初始化的validation callback保证未由LC源代码单独证明，需核实依赖版本/保证。

## REQ-LC-0056

**NASA 原始 ID**：LC9004.1

**来源类别**：documented

**原始文字/行为**：LC shall initialize the LC Application State to <PLATFORM_DEFINED> Default Reset State

**原始理由/补充说明**：Provides flexibility.  May want to “fly thru” a reset by defaulting to LC ACTIVE or maybe defaulting to PASSIVE so that no actions are taken.  May want to default to LC Disable.

**规范化中文需求**：恢复CDS时，将LC应用状态设置为平台默认Reset State。

**触发/条件**：APP CDS恢复成功并标记CDSSavedOnExit有效

**输入**：LC_STATE_WHEN_CDS_RESTORED、恢复CurrentLCState

**输出**：最终CurrentLCState

**状态与历史**：APP CDS

**处理及约束**：平台值可为ACTIVE/PASSIVE/DISABLED或FROM_CDS。<br>非FROM_CDS时编译分支显式覆盖恢复值；FROM_CDS保留恢复值。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L180–180 LC9004.1<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L874–889 LC_CreateTaskCDS<br>[evidence/LC/fsw/inc/lc_internal_cfg.h](evidence/LC/fsw/inc/lc_internal_cfg.h) L105–127 LC_STATE_WHEN_CDS_RESTORED

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0014<br>RES-LC-0029<br>RES-LC-0032<br>RES-LC-0147<br>RES-LC-0152<br>RES-LC-0153<br>RES-LC-0154<br>RES-LC-0160<br>RES-LC-0550<br>RES-LC-0551<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0704<br>RES-LC-0705

**ST**：ST-LC-0010<br>ST-LC-0013<br>ST-LC-0147<br>ST-LC-0152<br>ST-LC-0153<br>ST-LC-0154<br>ST-LC-0160<br>ST-LC-0550<br>ST-LC-0551<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8026<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8030<br>ST-LC-8031<br>ST-LC-9013<br>ST-LC-9014<br>ST-LC-9015

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0550<br>ST-LC-0558

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "成功恢复后按合法平台resetState选择保留或覆盖模式",
    "operation_ids": [
      "ST-LC-0152",
      "ST-LC-0153",
      "ST-LC-0154",
      "ST-LC-0160"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
    "operation_ids": [
      "ST-LC-0550",
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。

## REQ-LC-0057

**NASA 原始 ID**：LC9004.1.1

**来源类别**：documented

**原始文字/行为**：If the platform defined Default Reset State indicates to use the state of the LC Application prior to the reset, LC shall set the state of the LC Application to the state restored from the CDS

**原始理由/补充说明**：Provides ability to maintain the state of the LC Application prior to the reset instead of using the default value

**规范化中文需求**：Default Reset State 指定FROM_CDS时，使用CDS恢复的复位前LC应用状态。

**触发/条件**：APP CDS恢复并LC_STATE_WHEN_CDS_RESTORED==LC_STATE_FROM_CDS

**输入**：CDS AppData.CurrentLCState

**输出**：恢复状态保持

**状态与历史**：复位前AppData.CurrentLCState

**处理及约束**：FROM_CDS分支不覆盖CurrentLCState。<br>只有完整CDS恢复被接受；部分失败回退默认Power-On状态。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L181–181 LC9004.1.1<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L874–889 LC_CreateTaskCDS<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L438–478 LC_TableInit

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0014<br>RES-LC-0029<br>RES-LC-0032<br>RES-LC-0147<br>RES-LC-0152<br>RES-LC-0153<br>RES-LC-0154<br>RES-LC-0160<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0705

**ST**：ST-LC-0010<br>ST-LC-0013<br>ST-LC-0147<br>ST-LC-0152<br>ST-LC-0153<br>ST-LC-0154<br>ST-LC-0160<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8026<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8030<br>ST-LC-8031

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：逐项与冻结基线活动源码比较；属于静态阅读证据，未运行 LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0558

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "FROM_CDS保留复位前模式，不把sentinel当实际LC模式",
    "operation_ids": [
      "ST-LC-0152",
      "ST-LC-0153",
      "ST-LC-0160"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
    "operation_ids": [
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。

## REQ-LC-0058

**NASA 原始 ID**：LC9004.2

**来源类别**：documented

**原始文字/行为**：If LC determines the Critical Data is invalid, LC shall perform the same initialization as a cFE Power-on (see LC9000, LC9001 and LC9002)

**原始理由/补充说明**：Need to validate critical data to make sure that the data looks reasonable

**规范化中文需求**：Critical Data无效时，全套采用Power-On初始化。

**触发/条件**：恢复任一CDS/critical表失败，或APP保存标记无效

**输入**：框架恢复返回码、CDSSavedOnExit、五对象恢复标志

**输出**：加载默认WDT/ADT并初始化AppData/WRT/ART

**状态与历史**：不允许部分恢复混用

**处理及约束**：AppData只在Restore成功且CDSSavedOnExit==LC_CDS_SAVED时认定恢复。<br>LC不显式校验恢复WRT/ART每字段范围；损坏检测依赖cFE CDS完整性能力。<br>恢复内容语义有效性要求未由冻结依赖证明，不宣称所有Critical Data有效性已核实。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L182–182 LC9004.2<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L438–478 LC_TableInit<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L874–881 LC_CreateTaskCDS

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0014<br>RES-LC-0029<br>RES-LC-0032<br>RES-LC-0108<br>RES-LC-0144<br>RES-LC-0145<br>RES-LC-0146<br>RES-LC-0155<br>RES-LC-0156<br>RES-LC-0157<br>RES-LC-0158<br>RES-LC-0159<br>RES-LC-0160<br>RES-LC-0161<br>RES-LC-0163<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0705

**ST**：ST-LC-0010<br>ST-LC-0013<br>ST-LC-0108<br>ST-LC-0144<br>ST-LC-0145<br>ST-LC-0146<br>ST-LC-0155<br>ST-LC-0156<br>ST-LC-0157<br>ST-LC-0158<br>ST-LC-0159<br>ST-LC-0160<br>ST-LC-0161<br>ST-LC-0163<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8025<br>ST-LC-8027<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8030<br>ST-LC-8031<br>ST-LC-8040<br>ST-LC-8041<br>ST-LC-9004

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0018

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：unknown

**检查层次**：static<br>manual

**人工语义核对**：失效回退路径支持，但完整数据有效性（例如合法恢复状态）是否由cFE判定，缺依赖基线证据。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0558

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "任一Critical对象或APP保存标志缺失时完整cold fallback",
    "operation_ids": [
      "ST-LC-0146",
      "ST-LC-0155",
      "ST-LC-0156",
      "ST-LC-0157",
      "ST-LC-0158",
      "ST-LC-0159",
      "ST-LC-0160"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
    "operation_ids": [
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "源码CriticalData有效性依赖cFE恢复返回及APP保存标志；全部初始化的validation callback保证未由LC源代码单独证明，需核实依赖版本/保证。",
    "operation_ids": [],
    "status": "pending-interpretation",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。<br>源码CriticalData有效性依赖cFE恢复返回及APP保存标志；全部初始化的validation callback保证未由LC源代码单独证明，需核实依赖版本/保证。

## REQ-LC-0059

**NASA 原始 ID**：LC9005

**来源类别**：documented

**原始文字/行为**：Upon any initialization, LC shall validate the Watchpoint Definition Table for the following:
a)	valid operator
b)	data size
c)	Message ID

**原始理由/补充说明**：Valid the items that can be validated when a table is updated (some items cannot be validated until runtime).  Heritage from LRO.

**规范化中文需求**：任何初始化均应验证WDT的有效算子、数据大小和MID。

**触发/条件**：Power-On/Processor Reset/App Reset初始化

**输入**：加载或恢复WDT

**输出**：WDT验证结果/事件

**状态与历史**：cFE TBL及WDT

**处理及约束**：LC登记LC_ValidateWDT回调并在默认表加载时依赖TBL验证。<br>恢复critical表时也必须保留正式“any initialization”义务；当前LC不再显式调用回调，cFE是否调用未知。<br>验证回调只检查所列类型、算子、MID及浮点阈值，不检查WatchpointOffset或其加法溢出；回调发生不构成偏移安全保证。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L183–186 LC9005<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L631–654 LC_CreateDefinitionTables<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L917–940 LC_LoadDefaultTables<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L988–1134 LC_ValidateWDT

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0027<br>RES-LC-0029<br>RES-LC-0155<br>RES-LC-0156<br>RES-LC-0161<br>RES-LC-0163<br>RES-LC-0236<br>RES-LC-0237<br>RES-LC-0238<br>RES-LC-0239<br>RES-LC-0240<br>RES-LC-0241<br>RES-LC-0242<br>RES-LC-0243<br>RES-LC-0244<br>RES-LC-0245<br>RES-LC-0246<br>RES-LC-0247<br>RES-LC-0248<br>RES-LC-0249<br>RES-LC-0250<br>RES-LC-0251<br>RES-LC-0252<br>RES-LC-0509<br>RES-LC-0510<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0702<br>RES-LC-0705

**ST**：ST-LC-0008<br>ST-LC-0010<br>ST-LC-0155<br>ST-LC-0156<br>ST-LC-0161<br>ST-LC-0163<br>ST-LC-0236<br>ST-LC-0237<br>ST-LC-0238<br>ST-LC-0239<br>ST-LC-0240<br>ST-LC-0241<br>ST-LC-0242<br>ST-LC-0243<br>ST-LC-0244<br>ST-LC-0245<br>ST-LC-0246<br>ST-LC-0247<br>ST-LC-0248<br>ST-LC-0249<br>ST-LC-0250<br>ST-LC-0251<br>ST-LC-0252<br>ST-LC-0509<br>ST-LC-0510<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8025<br>ST-LC-8027<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8030<br>ST-LC-8031<br>ST-LC-8118<br>ST-LC-8119<br>ST-LC-8120<br>ST-LC-8121<br>ST-LC-8122<br>ST-LC-8123<br>ST-LC-9011

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0018<br>ISSUE-LC-0021

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：unknown

**检查层次**：static<br>manual

**人工语义核对**：回调存在；在全部恢复初始化路径的调用由cFE决定，未取得对应cFE版本不能断言全覆盖。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0509<br>ST-LC-0510<br>ST-LC-0558

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "任何初始化提供实际选中WDT、保留默认与CDS来源",
    "operation_ids": [
      "ST-LC-0161"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "验证WDT DataType/Operator/MID的计算义务",
    "operation_ids": [
      "ST-LC-0236",
      "ST-LC-0237",
      "ST-LC-0238",
      "ST-LC-0239",
      "ST-LC-0240",
      "ST-LC-0241",
      "ST-LC-0242",
      "ST-LC-0243",
      "ST-LC-0244",
      "ST-LC-0245",
      "ST-LC-0246",
      "ST-LC-0247",
      "ST-LC-0248",
      "ST-LC-0249",
      "ST-LC-0250",
      "ST-LC-0251",
      "ST-LC-0252",
      "ST-LC-0509",
      "ST-LC-0510"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
    "operation_ids": [
      "ST-LC-0509",
      "ST-LC-0510",
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "源码CriticalData有效性依赖cFE恢复返回及APP保存标志；全部初始化的validation callback保证未由LC源代码单独证明，需核实依赖版本/保证。",
    "operation_ids": [],
    "status": "pending-interpretation",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。<br>源码CriticalData有效性依赖cFE恢复返回及APP保存标志；全部初始化的validation callback保证未由LC源代码单独证明，需核实依赖版本/保证。

## REQ-LC-0060

**NASA 原始 ID**：LC9006

**来源类别**：documented

**原始文字/行为**：Upon any initialization, LC shall validate the Actionpoint Definition Table for the following:
a)	valid default state
b)	RTS number (in range)
c)	Event Type (DEBUG, INFO, ERROR, CRITICAL)
d)	Failure Count (in range)
e)	Action Equation syntax

**原始理由/补充说明**：Valid the items that can be validated when a table is updated (some items cannot be validated until runtime).  Heritage from LRO.

**规范化中文需求**：任何初始化均应验证ADT的默认状态、RTS号、事件类型、失败次数和RPN语法。

**触发/条件**：Power-On/Processor Reset/App Reset初始化

**输入**：加载或恢复ADT

**输出**：ADT验证结果/事件

**状态与历史**：cFE TBL及ADT

**处理及约束**：校验规则同LC3007。<br>恢复critical表时保留any initialization要求，LC本地不显式重验；取决于cFE表恢复语义。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L187–192 LC9006<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L684–706 LC_CreateDefinitionTables<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L956–987 LC_LoadDefaultTables<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L494–728 LC_ValidateADT / LC_ValidateRPN

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0028<br>RES-LC-0029<br>RES-LC-0155<br>RES-LC-0156<br>RES-LC-0161<br>RES-LC-0163<br>RES-LC-0370<br>RES-LC-0371<br>RES-LC-0372<br>RES-LC-0373<br>RES-LC-0374<br>RES-LC-0375<br>RES-LC-0376<br>RES-LC-0377<br>RES-LC-0378<br>RES-LC-0379<br>RES-LC-0380<br>RES-LC-0381<br>RES-LC-0382<br>RES-LC-0383<br>RES-LC-0384<br>RES-LC-0385<br>RES-LC-0386<br>RES-LC-0387<br>RES-LC-0388<br>RES-LC-0389<br>RES-LC-0390<br>RES-LC-0520<br>RES-LC-0521<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0702<br>RES-LC-0705

**ST**：ST-LC-0009<br>ST-LC-0010<br>ST-LC-0155<br>ST-LC-0156<br>ST-LC-0161<br>ST-LC-0163<br>ST-LC-0370<br>ST-LC-0371<br>ST-LC-0372<br>ST-LC-0373<br>ST-LC-0374<br>ST-LC-0375<br>ST-LC-0376<br>ST-LC-0377<br>ST-LC-0378<br>ST-LC-0379<br>ST-LC-0380<br>ST-LC-0381<br>ST-LC-0382<br>ST-LC-0383<br>ST-LC-0384<br>ST-LC-0385<br>ST-LC-0386<br>ST-LC-0387<br>ST-LC-0388<br>ST-LC-0389<br>ST-LC-0390<br>ST-LC-0520<br>ST-LC-0521<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8000<br>ST-LC-8001<br>ST-LC-8002<br>ST-LC-8003<br>ST-LC-8004<br>ST-LC-8005<br>ST-LC-8006<br>ST-LC-8007<br>ST-LC-8008<br>ST-LC-8009<br>ST-LC-8025<br>ST-LC-8027<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8030<br>ST-LC-8031

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0018

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：unknown

**检查层次**：static<br>manual

**人工语义核对**：默认表验证有回调；恢复时依赖cFE调用保证，未独立证明。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0520<br>ST-LC-0521<br>ST-LC-0558

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "任何初始化提供实际选中ADT、保留默认与CDS来源",
    "operation_ids": [
      "ST-LC-0161"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "验证ADT DefaultState/RTS/EventType/FailCount/RPN的计算义务",
    "operation_ids": [
      "ST-LC-0370",
      "ST-LC-0371",
      "ST-LC-0372",
      "ST-LC-0373",
      "ST-LC-0374",
      "ST-LC-0375",
      "ST-LC-0376",
      "ST-LC-0377",
      "ST-LC-0378",
      "ST-LC-0379",
      "ST-LC-0380",
      "ST-LC-0381",
      "ST-LC-0382",
      "ST-LC-0383",
      "ST-LC-0384",
      "ST-LC-0385",
      "ST-LC-0386",
      "ST-LC-0387",
      "ST-LC-0388",
      "ST-LC-0389",
      "ST-LC-0390",
      "ST-LC-0520",
      "ST-LC-0521"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
    "operation_ids": [
      "ST-LC-0520",
      "ST-LC-0521",
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "源码CriticalData有效性依赖cFE恢复返回及APP保存标志；全部初始化的validation callback保证未由LC源代码单独证明，需核实依赖版本/保证。",
    "operation_ids": [],
    "status": "pending-interpretation",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。<br>源码CriticalData有效性依赖cFE恢复返回及APP保存标志；全部初始化的validation callback保证未由LC源代码单独证明，需核实依赖版本/保证。

## REQ-LC-0061

**NASA 原始 ID**：LC9007

**来源类别**：documented

**原始文字/行为**：Upon any initialization, LC shall subscribe to the messages defined in the WDT.

**原始理由/补充说明**：Must subscribe to all of the messages defined in the Watchpoint
Definition Table after any reset.  Heritage from LRO.

**规范化中文需求**：任何初始化均订阅WDT中定义的消息。

**触发/条件**：表初始化成功后

**输入**：最终活动WDTPtr（默认或完整CDS恢复）、每项DataType/MID

**输出**：监测消息订阅和MID→WP目录

**状态与历史**：CmdPipe、MessageLinks/WatchPtLinks/HashTable

**处理及约束**：忽略NOT_USED WP；每个唯一MID订阅一次，可关联多个WP。<br>重新建表先取消旧MID订阅；订阅失败发ERROR但继续构建，不能宣称全部订阅已成功。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L193–194 LC9007<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L486–491 LC_TableInit<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L91–157 LC_CreateHashTable<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L165–233 LC_AddWatchpoint

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0029<br>RES-LC-0031<br>RES-LC-0032<br>RES-LC-0150<br>RES-LC-0162<br>RES-LC-0164<br>RES-LC-0165<br>RES-LC-0166<br>RES-LC-0167<br>RES-LC-0168<br>RES-LC-0169<br>RES-LC-0170<br>RES-LC-0171<br>RES-LC-0172<br>RES-LC-0173<br>RES-LC-0174<br>RES-LC-0175<br>RES-LC-0176<br>RES-LC-0177<br>RES-LC-0502<br>RES-LC-0546<br>RES-LC-0547<br>RES-LC-0548<br>RES-LC-0549<br>RES-LC-0550<br>RES-LC-0551<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0702<br>RES-LC-0704<br>RES-LC-0705<br>RES-LC-0706<br>RES-LC-0707

**ST**：ST-LC-0010<br>ST-LC-0012<br>ST-LC-0013<br>ST-LC-0150<br>ST-LC-0162<br>ST-LC-0164<br>ST-LC-0165<br>ST-LC-0166<br>ST-LC-0167<br>ST-LC-0168<br>ST-LC-0169<br>ST-LC-0170<br>ST-LC-0171<br>ST-LC-0172<br>ST-LC-0173<br>ST-LC-0174<br>ST-LC-0175<br>ST-LC-0176<br>ST-LC-0177<br>ST-LC-0502<br>ST-LC-0546<br>ST-LC-0547<br>ST-LC-0548<br>ST-LC-0549<br>ST-LC-0550<br>ST-LC-0551<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8030<br>ST-LC-8031<br>ST-LC-8088<br>ST-LC-8089<br>ST-LC-8090<br>ST-LC-8091<br>ST-LC-8092<br>ST-LC-8093<br>ST-LC-9009<br>ST-LC-9013<br>ST-LC-9014<br>ST-LC-9015

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0019

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：unknown

**检查层次**：static<br>manual

**人工语义核对**：会请求所有所需订阅；失败只事件不阻止启动，无运行订阅成功证据。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0502<br>ST-LC-0546<br>ST-LC-0548<br>ST-LC-0550<br>ST-LC-0558

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "按实际初始化选择的WDT交接订阅输入，Processor/App reset成功恢复用CDS WDT",
    "operation_ids": [
      "ST-LC-0150",
      "ST-LC-0162"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
    "operation_ids": [
      "ST-LC-0502",
      "ST-LC-0546",
      "ST-LC-0548",
      "ST-LC-0550",
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "实际SB Subscribe执行与失败事件提交待论文软件服务资源绑定；只形成数据和意图不能声称完成订阅。",
    "operation_ids": [
      "ST-LC-0502",
      "ST-LC-0546",
      "ST-LC-0548",
      "ST-LC-0550",
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "扫描实际WDT，过滤未用条目、MID去重、hash冲突区分、订阅意图和索引绑定",
    "operation_ids": [
      "ST-LC-0164",
      "ST-LC-0168",
      "ST-LC-0169",
      "ST-LC-0170",
      "ST-LC-0171",
      "ST-LC-0172",
      "ST-LC-0173",
      "ST-LC-0174",
      "ST-LC-0175",
      "ST-LC-0176"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "真实失败返回事件描述且继续重建",
    "operation_ids": [
      "ST-LC-0177",
      "ST-LC-0502"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。<br>实际SB Subscribe执行与失败事件提交待论文软件服务资源绑定；只形成数据和意图不能声称完成订阅。

## REQ-LC-0062

**NASA 原始 ID**：LC9007.1

**来源类别**：documented

**原始文字/行为**：For a cFE Processor Reset, If the Save Critical Data parameter is YES, LC shall subscribe to the messages defined in the WDT restored from the CDS

**原始理由/补充说明**：Need to use the WDT that was being used prior to the cFE Processor Reset instead of the default WDT.


**规范化中文需求**：Processor Reset 且Save Critical Data开启时，订阅CDS恢复WDT中的消息。

**触发/条件**：完整CDS恢复成功后的Processor reset初始化

**输入**：恢复WDTPtr中的使用项MID

**输出**：订阅请求、WP路由目录

**状态与历史**：恢复表与CmdPipe

**处理及约束**：完整五对象恢复才获取恢复WDTPtr后LC_CreateHashTable。<br>CDS开关虽启用但恢复失败则默认表订阅，符合LC9004.2回退；不可伪称恢复表仍生效。<br>订阅失败继续并发错误事件，成功由外部cFE SB返回确定。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L195–196 LC9007.1<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L438–491 LC_TableInit<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L126–153 LC_CreateHashTable<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L222–233 LC_AddWatchpoint

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0029<br>RES-LC-0031<br>RES-LC-0032<br>RES-LC-0150<br>RES-LC-0162<br>RES-LC-0164<br>RES-LC-0168<br>RES-LC-0169<br>RES-LC-0170<br>RES-LC-0171<br>RES-LC-0172<br>RES-LC-0173<br>RES-LC-0174<br>RES-LC-0175<br>RES-LC-0176<br>RES-LC-0177<br>RES-LC-0502<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0702<br>RES-LC-0705

**ST**：ST-LC-0010<br>ST-LC-0012<br>ST-LC-0013<br>ST-LC-0150<br>ST-LC-0162<br>ST-LC-0164<br>ST-LC-0168<br>ST-LC-0169<br>ST-LC-0170<br>ST-LC-0171<br>ST-LC-0172<br>ST-LC-0173<br>ST-LC-0174<br>ST-LC-0175<br>ST-LC-0176<br>ST-LC-0177<br>ST-LC-0502<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8030<br>ST-LC-8031<br>ST-LC-8088<br>ST-LC-8090<br>ST-LC-8091<br>ST-LC-8092<br>ST-LC-8093<br>ST-LC-9009

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0019

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：unknown

**检查层次**：static<br>manual

**人工语义核对**：恢复表来源路径支持；订阅成功未通过执行验证，故保持unknown完成边界。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0502<br>ST-LC-0558

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "按实际初始化选择的WDT交接订阅输入，Processor/App reset成功恢复用CDS WDT",
    "operation_ids": [
      "ST-LC-0150",
      "ST-LC-0162"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
    "operation_ids": [
      "ST-LC-0502",
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "实际SB Subscribe执行与失败事件提交待论文软件服务资源绑定；只形成数据和意图不能声称完成订阅。",
    "operation_ids": [
      "ST-LC-0502",
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "扫描实际WDT，过滤未用条目、MID去重、hash冲突区分、订阅意图和索引绑定",
    "operation_ids": [
      "ST-LC-0164",
      "ST-LC-0168",
      "ST-LC-0169",
      "ST-LC-0170",
      "ST-LC-0171",
      "ST-LC-0172",
      "ST-LC-0173",
      "ST-LC-0174",
      "ST-LC-0175",
      "ST-LC-0176"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "真实失败返回事件描述且继续重建",
    "operation_ids": [
      "ST-LC-0177",
      "ST-LC-0502"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。<br>实际SB Subscribe执行与失败事件提交待论文软件服务资源绑定；只形成数据和意图不能声称完成订阅。

## REQ-LC-0063

**NASA 原始 ID**：LC9007.2

**来源类别**：documented

**原始文字/行为**：For an LC Application Reset, If the Save Critical Data parameter is YES, LC shall subscribe to the messages defined in the WDT restored from the CDS

**原始理由/补充说明**：Need to use the WDT that was being used prior to the LC App reset instead of the default WDT


**规范化中文需求**：Application Reset 且Save Critical Data开启时，订阅CDS恢复WDT中的消息。

**触发/条件**：完整CDS恢复成功后的Application reset初始化

**输入**：恢复WDTPtr中的使用项MID

**输出**：订阅请求、WP路由目录

**状态与历史**：恢复表与CmdPipe

**处理及约束**：完整五对象恢复才获取恢复WDTPtr后LC_CreateHashTable。<br>CDS开关虽启用但恢复失败则默认表订阅，符合LC9004.2回退；不可伪称恢复表仍生效。<br>订阅失败继续并发错误事件，成功由外部cFE SB返回确定。

**证据**：[evidence/LC/docs/lc_FunctionalRequirements.csv](evidence/LC/docs/lc_FunctionalRequirements.csv) L197–198 LC9007.2<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L438–491 LC_TableInit<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L126–153 LC_CreateHashTable<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L222–233 LC_AddWatchpoint

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0029<br>RES-LC-0031<br>RES-LC-0032<br>RES-LC-0150<br>RES-LC-0162<br>RES-LC-0164<br>RES-LC-0168<br>RES-LC-0169<br>RES-LC-0170<br>RES-LC-0171<br>RES-LC-0172<br>RES-LC-0173<br>RES-LC-0174<br>RES-LC-0175<br>RES-LC-0176<br>RES-LC-0177<br>RES-LC-0502<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0702<br>RES-LC-0705

**ST**：ST-LC-0010<br>ST-LC-0012<br>ST-LC-0013<br>ST-LC-0150<br>ST-LC-0162<br>ST-LC-0164<br>ST-LC-0168<br>ST-LC-0169<br>ST-LC-0170<br>ST-LC-0171<br>ST-LC-0172<br>ST-LC-0173<br>ST-LC-0174<br>ST-LC-0175<br>ST-LC-0176<br>ST-LC-0177<br>ST-LC-0502<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8030<br>ST-LC-8031<br>ST-LC-8088<br>ST-LC-8090<br>ST-LC-8091<br>ST-LC-8092<br>ST-LC-8093<br>ST-LC-9009

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0019

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：unknown

**检查层次**：static<br>manual

**人工语义核对**：恢复表来源路径支持；订阅成功未通过执行验证，故保持unknown完成边界。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0502<br>ST-LC-0558

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "按实际初始化选择的WDT交接订阅输入，Processor/App reset成功恢复用CDS WDT",
    "operation_ids": [
      "ST-LC-0150",
      "ST-LC-0162"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
    "operation_ids": [
      "ST-LC-0502",
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "实际SB Subscribe执行与失败事件提交待论文软件服务资源绑定；只形成数据和意图不能声称完成订阅。",
    "operation_ids": [
      "ST-LC-0502",
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "扫描实际WDT，过滤未用条目、MID去重、hash冲突区分、订阅意图和索引绑定",
    "operation_ids": [
      "ST-LC-0164",
      "ST-LC-0168",
      "ST-LC-0169",
      "ST-LC-0170",
      "ST-LC-0171",
      "ST-LC-0172",
      "ST-LC-0173",
      "ST-LC-0174",
      "ST-LC-0175",
      "ST-LC-0176"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "真实失败返回事件描述且继续重建",
    "operation_ids": [
      "ST-LC-0177",
      "ST-LC-0502"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。<br>实际SB Subscribe执行与失败事件提交待论文软件服务资源绑定；只形成数据和意图不能声称完成订阅。

## REQ-LC-0064

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：if ((LC_SampleAP->UpdateAge != 0) && (ValidSampleCmd)) ... CountdownToStale--; ... WatchResult = LC_WATCH_STALE;

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：WP时效由有效带UpdateAge请求推进；先AP求值再推进age，0阈值不自行过期。

**触发/条件**：有效SampleAP处理后且应用不DISABLED、UpdateAge!=0

**输入**：全体WRT.CountdownToStale、UpdateAge

**输出**：剩余次数减一；到0改STALE

**状态与历史**：本次AP已读取更新前WP结果

**处理及约束**：先执行请求AP范围，再循环全部WP推进age。<br>正值才减一，0不减且不额外改结果。<br>TRUE/FALSE WP结果加载ResultAgeWhenStale；ERROR/STALE清倒计数。<br>该次数不是墙钟时间，request频率由外部调度决定。

**证据**：[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L44–107 LC_SampleAPReq<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L409–452 LC_ProcessWP<br>[evidence/LC/config/default_lc_tblstruct.h](evidence/LC/config/default_lc_tblstruct.h) L109–111 ResultAgeWhenStale

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0020<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0253<br>RES-LC-0254<br>RES-LC-0255<br>RES-LC-0256<br>RES-LC-0257<br>RES-LC-0258<br>RES-LC-0259<br>RES-LC-0260<br>RES-LC-0261<br>RES-LC-0262<br>RES-LC-0300<br>RES-LC-0301<br>RES-LC-0302<br>RES-LC-0303<br>RES-LC-0305<br>RES-LC-0367<br>RES-LC-0368<br>RES-LC-0369<br>RES-LC-0396<br>RES-LC-0511<br>RES-LC-0512<br>RES-LC-0702

**ST**：ST-LC-0001<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0253<br>ST-LC-0254<br>ST-LC-0255<br>ST-LC-0256<br>ST-LC-0257<br>ST-LC-0258<br>ST-LC-0259<br>ST-LC-0260<br>ST-LC-0261<br>ST-LC-0262<br>ST-LC-0300<br>ST-LC-0301<br>ST-LC-0302<br>ST-LC-0303<br>ST-LC-0305<br>ST-LC-0367<br>ST-LC-0368<br>ST-LC-0369<br>ST-LC-0396<br>ST-LC-0511<br>ST-LC-0512<br>ST-LC-8066<br>ST-LC-8067<br>ST-LC-8068<br>ST-LC-8069<br>ST-LC-8070<br>ST-LC-8071<br>ST-LC-8072<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-8095<br>ST-LC-8096<br>ST-LC-8097<br>ST-LC-8098<br>ST-LC-8099<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0015

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：补充记录有依据的活动行为；不是NASA正式要求，未运行LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0511<br>ST-LC-0512

**附加字段 obligation_mapping**：full

**附加字段 obligations**：

```json
[
  {
    "description": "源码减龄只能位于AP范围函数返回之后；索引合法后标ValidSampleCmd=true，包括首项拒整范围。",
    "operation_ids": [
      "ST-LC-0396",
      "ST-LC-0305",
      "ST-LC-0367",
      "ST-LC-0512"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "仅非DISABLED、ValidSampleCmd且UpdateAge!=0交接到全WP减龄；AP读取减龄前WRT，无动作/错误请求不自动更新年龄。",
    "operation_ids": [
      "ST-LC-0300",
      "ST-LC-0369",
      "ST-LC-0303",
      "ST-LC-0367",
      "ST-LC-0368",
      "ST-LC-0253",
      "ST-LC-0254",
      "ST-LC-0255",
      "ST-LC-0256",
      "ST-LC-0257",
      "ST-LC-0258",
      "ST-LC-0259",
      "ST-LC-0260",
      "ST-LC-0261",
      "ST-LC-0262",
      "ST-LC-0511"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：正倒数减1/到0置STALE以及FALSE/TRUE加载阈值、ERROR/STALE倒数清0已由WP操作表达，ST0368已在同次采样内联ST0253–0262；聚合/字段别名的官方加载格式仍待确认。<br>次数不是秒/毫秒，真实请求节奏外部未知；不增造周期。

## REQ-LC-0065

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：WPDataPtr = ((uint8 *)BufPtr) + ... WatchpointOffset; MaskedWPData = SizedWPData & ... BitMask;

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：执行源码的偏移/类型门控后按BE/LE取数、扩展和掩码；极端偏移回绕放行时后续值未知。

**触发/条件**：相关监测消息的某个WP候选

**输入**：消息（含头）、长度、WatchpointOffset、DataType、BitMask、ComparisonValue

**输出**：安全跨度下的类型化/掩码输入与WP结果，或已检测错误修正；回绕漏检时后续行为未知

**状态与历史**：无永久临时输入状态

**处理及约束**：WatchpointOffset从消息开头含消息头起算。<br>运行时实际判定是(Offset + NumOfDataBytes) > MsgLength，宽度来自sizeof(uint8/uint16/uint32/float)。未知类型或该C表达式为true时先调用适用的EVS错误事件服务，再写WatchResult=ERROR、CountdownToStale=0，返回false并跳过LC_ProcessWP；此拒绝路径不增加EvaluationCount。<br>未对齐多字节值由字节拷贝转换，不直接解引用。<br>数据类型决定signed/unsigned/float比较；不把所有值视作uint32数学比较。<br>源码将Offset和NumOfDataBytes声明为uint32，MsgLength声明为size_t；以下回绕例按uint32为32位无符号且加法未提升到更宽整数的C算术假设核对。common_types.h及目标编译环境未固定，需由ISSUE-LC-0004核定；size_t较宽不会使已经完成的uint32加法重新变宽。<br>在上述32位无符号算术假设下，offset=0xFFFFFFFF、width=2使和回绕为1；对length=186会放行。LC随后按原始大偏移形成数据指针，不能据此推断ERROR、比较结果、统计更新、事件或后续正常返回。<br>希望满足的安全条件是offset<=length且width<=length-offset，并拒绝所有不满足的跨度；这是待确认/待实现的安全要求，不是本基线已经实现的保护，本包不修改LC源码。

**证据**：[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L358–395 LC_ProcessWP<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L784–981 LC_WPOffsetValid / LC_GetSizedWPData

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0021<br>RES-LC-0022<br>RES-LC-0033<br>RES-LC-0200<br>RES-LC-0206<br>RES-LC-0207<br>RES-LC-0208<br>RES-LC-0209<br>RES-LC-0210<br>RES-LC-0211<br>RES-LC-0212<br>RES-LC-0213<br>RES-LC-0214<br>RES-LC-0215<br>RES-LC-0216<br>RES-LC-0219<br>RES-LC-0232<br>RES-LC-0235<br>RES-LC-0506<br>RES-LC-0508<br>RES-LC-0702

**ST**：ST-LC-0002<br>ST-LC-0003<br>ST-LC-0014<br>ST-LC-0016<br>ST-LC-0200<br>ST-LC-0206<br>ST-LC-0207<br>ST-LC-0208<br>ST-LC-0209<br>ST-LC-0210<br>ST-LC-0211<br>ST-LC-0212<br>ST-LC-0213<br>ST-LC-0214<br>ST-LC-0215<br>ST-LC-0216<br>ST-LC-0219<br>ST-LC-0232<br>ST-LC-0235<br>ST-LC-0506<br>ST-LC-0508<br>ST-LC-8106<br>ST-LC-8110<br>ST-LC-8111<br>ST-LC-8112<br>ST-LC-8113<br>ST-LC-8115<br>ST-LC-8116<br>ST-LC-8117<br>ST-LC-9010

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0020<br>ISSUE-LC-0021

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：补充记录有依据的活动行为；不是NASA正式要求，未运行LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。 偏移专项复查：保留原始C表达式而非数学无限精度加法；unsafe-accepted分支仅登记访问风险，不能生成虚构ERROR或正常统计。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0506<br>ST-LC-0508

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "原类型width与uint32相加长度检查，offset含消息头",
    "operation_ids": [
      "ST-LC-0207",
      "ST-LC-0208"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "安全可推导跨度BE/LE取数、扩展、掩码及类型化关系",
    "operation_ids": [
      "ST-LC-0209",
      "ST-LC-0214",
      "ST-LC-0216",
      "ST-LC-0219",
      "ST-LC-0508"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "检测错误事件→ERROR→age0，跳正常比较次数",
    "operation_ids": [
      "ST-LC-0211",
      "ST-LC-0212",
      "ST-LC-0213",
      "ST-LC-0506"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "回绕放行后值/结果/统计不可推导，不把审查停点当源码安全拒绝",
    "operation_ids": [
      "ST-LC-0210",
      "ST-LC-0232"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：ISSUE0021/0004 C算术/接口与风险指针实际行为未知；希望安全算法不混成已实现要求。

## REQ-LC-0066

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：if ((PreviousResult == LC_WATCH_FALSE) || (PreviousResult == LC_WATCH_STALE)) ... FalseToTrueCount++;

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：当前实现把STALE→TRUE也当FalseToTrue跨越，STALE→FALSE也保存LastTrueToFalse；正式统计含义需确认。

**触发/条件**：WP结果TRUE/FALSE且旧结果STALE

**输入**：旧WP结果、掩码值、时间戳

**输出**：转换统计/值/时间更新

**状态与历史**：WRT最近跨越历史

**处理及约束**：旧STALE、新TRUE时增FalseToTrueCount并记录LastFalseToTrue。<br>旧STALE、新FALSE时记录LastTrueToFalse，不含对称TrueToFalse计数字段。<br>此记录不修改LC2004原义，只解释实现。

**证据**：[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L409–444 LC_ProcessWP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0021<br>RES-LC-0022<br>RES-LC-0033<br>RES-LC-0200<br>RES-LC-0223<br>RES-LC-0228<br>RES-LC-0229<br>RES-LC-0230<br>RES-LC-0264<br>RES-LC-0265<br>RES-LC-0266

**ST**：ST-LC-0002<br>ST-LC-0003<br>ST-LC-0014<br>ST-LC-0016<br>ST-LC-0200<br>ST-LC-0223<br>ST-LC-0228<br>ST-LC-0229<br>ST-LC-0230<br>ST-LC-0264<br>ST-LC-0265<br>ST-LC-0266<br>ST-LC-8104<br>ST-LC-8105<br>ST-LC-8109<br>ST-LC-8110<br>ST-LC-8111<br>ST-LC-8112<br>ST-LC-8113<br>ST-LC-8115<br>ST-LC-8116<br>ST-LC-8117

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：实现事实明确；与正式LC2004存在口径差异。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "实现旧STALE新TRUE也增FalseToTrueCount并记值/时刻",
    "operation_ids": [
      "ST-LC-0228",
      "ST-LC-0229",
      "ST-LC-0230"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "实现旧STALE新FALSE也记LastTrueToFalse，无对称计数字段",
    "operation_ids": [
      "ST-LC-0228",
      "ST-LC-0229",
      "ST-LC-0230"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "正式LC2004字面另有义务视图，口径待裁定",
    "operation_ids": [
      "ST-LC-0264",
      "ST-LC-0265",
      "ST-LC-0266"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：补充事实不改原正式要求；ISSUE0006开放，持久绑定pending-interface。

## REQ-LC-0067

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：else { /* WPEvalResult is STALE or ERROR */ ... CountdownToStale = 0; }

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：WP ERROR/STALE分支清时效倒计数，但保持已有连续TRUE计数；不误补为连续TRUE归零。

**触发/条件**：WP本次标准/custom比较返回ERROR或STALE

**输入**：旧ConsecutiveTrueCount、CountdownToStale、错误结果

**输出**：WatchResult及CountdownToStale=0；连续TRUE旧值保持

**状态与历史**：单WP统计

**处理及约束**：结果保存且EvaluationCount在已成功抽取后加一。<br>该分支不写ConsecutiveTrueCount；FALSE分支才清0。<br>数据抽取失败路径不增加EvaluationCount。

**证据**：[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L398–454 LC_ProcessWP<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L957–973 LC_GetSizedWPData

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0021<br>RES-LC-0022<br>RES-LC-0033<br>RES-LC-0200<br>RES-LC-0211<br>RES-LC-0212<br>RES-LC-0213<br>RES-LC-0215<br>RES-LC-0219<br>RES-LC-0220<br>RES-LC-0221<br>RES-LC-0222<br>RES-LC-0225<br>RES-LC-0227<br>RES-LC-0230<br>RES-LC-0506<br>RES-LC-0508<br>RES-LC-0702

**ST**：ST-LC-0002<br>ST-LC-0003<br>ST-LC-0014<br>ST-LC-0016<br>ST-LC-0200<br>ST-LC-0211<br>ST-LC-0212<br>ST-LC-0213<br>ST-LC-0215<br>ST-LC-0219<br>ST-LC-0220<br>ST-LC-0221<br>ST-LC-0222<br>ST-LC-0225<br>ST-LC-0227<br>ST-LC-0230<br>ST-LC-0506<br>ST-LC-0508<br>ST-LC-8106<br>ST-LC-8107<br>ST-LC-8108<br>ST-LC-8110<br>ST-LC-8111<br>ST-LC-8112<br>ST-LC-8113<br>ST-LC-8115<br>ST-LC-8116<br>ST-LC-8117<br>ST-LC-9010

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：补充记录有依据的活动行为；不是NASA正式要求，未运行LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0506<br>ST-LC-0508

**附加字段 obligation_mapping**：full

**附加字段 obligations**：

```json
[
  {
    "description": "提取成功后ERROR/STALE也提交结果并计EvaluationCount",
    "operation_ids": [
      "ST-LC-0220",
      "ST-LC-0221",
      "ST-LC-0222"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "ERROR/STALE清age但保持连续TRUE和历史",
    "operation_ids": [
      "ST-LC-0227",
      "ST-LC-0230"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "偏移/类型/取数拒绝不计次数，只修正结果/age",
    "operation_ids": [
      "ST-LC-0211",
      "ST-LC-0212",
      "ST-LC-0213",
      "ST-LC-0506"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：真实入口、EVS、持久提交pending-interface；本规则与FALSE清连续TRUE分别走查。

## REQ-LC-0068

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：else if (CurrentResult == LC_ACTION_STALE) ... ConsecutiveFailCount = 0; else ... LC_ACTION_ERROR_ERR_EID

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：AP STALE清连续FAIL；AP ERROR保留连续FAIL并发错误事件，不应推导ERROR中断失败连续性。

**触发/条件**：AP求值产生STALE或ERROR

**输入**：旧连续FAIL计数、新结果

**输出**：STALE→计数0；ERROR→计数保持/ERROR事件

**状态与历史**：ART连续计数历史

**处理及约束**：PASS同样清连续FAIL，FAIL增一。<br>ERROR后下一FAIL可继续此前计数；这描述实现，是否满足业务“连续”应独立裁定。<br>错误结果不能压成PASS。

**证据**：[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L229–276 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0322<br>RES-LC-0323<br>RES-LC-0324<br>RES-LC-0326<br>RES-LC-0327<br>RES-LC-0356<br>RES-LC-0362<br>RES-LC-0363<br>RES-LC-0364<br>RES-LC-0365<br>RES-LC-0394<br>RES-LC-0513<br>RES-LC-0519<br>RES-LC-0702

**ST**：ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0322<br>ST-LC-0323<br>ST-LC-0324<br>ST-LC-0326<br>ST-LC-0327<br>ST-LC-0356<br>ST-LC-0362<br>ST-LC-0363<br>ST-LC-0364<br>ST-LC-0365<br>ST-LC-0394<br>ST-LC-0513<br>ST-LC-0519<br>ST-LC-8013<br>ST-LC-8052<br>ST-LC-8058<br>ST-LC-8061<br>ST-LC-8062<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0017

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：正式只明确PASS归零；ERROR保持是代码补充，潜在连续语义问题需审查。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0513<br>ST-LC-0519

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "AP STALE清连续FAIL；PASS同样清；FAIL增；ERROR保留连续数并登记错误且不发RTS。",
    "operation_ids": [
      "ST-LC-0356",
      "ST-LC-0363",
      "ST-LC-0362",
      "ST-LC-0364",
      "ST-LC-0365",
      "ST-LC-0519"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "ERROR后下一FAIL可能接续旧连续数，明确为实现规则而非业务已认可“连续”定义。",
    "operation_ids": [
      "ST-LC-0326",
      "ST-LC-0327",
      "ST-LC-0394"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：ERROR间隔是否中断业务连续性待ISSUE-LC-0017；真实错误事件提交pending-interface。

## REQ-LC-0069

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：if ((CurrentAPState != LC_ACTION_NOT_USED) && (CurrentAPState != LC_APSTATE_PERMOFF)) ... for (...<=EndIndex...)

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：AP范围采样先检查首项可操作状态；首项NOT_USED/PERMOFF会拒绝整个范围，即使后续AP可用。

**触发/条件**：合法范围SampleAP调用LC_SampleAPs

**输入**：范围start/end、首项CurrentState

**输出**：范围内逐项调用或单错误事件无采样

**状态与历史**：所有范围项旧ART

**处理及约束**：循环inclusive start..end。<br>通过首项检查后，LC_SampleSingleAP单项仅ACTIVE/PASSIVE求值，其他项跳过。<br>请求ValidSampleCmd按索引合法性设true，因此首项拒绝后仍可能推进WP age。

**证据**：[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L41–108 LC_SampleAPs / LC_SampleSingleAP<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L68–104 LC_SampleAPReq

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0300<br>RES-LC-0302<br>RES-LC-0303<br>RES-LC-0304<br>RES-LC-0305<br>RES-LC-0306<br>RES-LC-0307<br>RES-LC-0308<br>RES-LC-0309<br>RES-LC-0366<br>RES-LC-0367<br>RES-LC-0368<br>RES-LC-0391<br>RES-LC-0396<br>RES-LC-0511<br>RES-LC-0512<br>RES-LC-0702

**ST**：ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0300<br>ST-LC-0302<br>ST-LC-0303<br>ST-LC-0304<br>ST-LC-0305<br>ST-LC-0306<br>ST-LC-0307<br>ST-LC-0308<br>ST-LC-0309<br>ST-LC-0366<br>ST-LC-0367<br>ST-LC-0368<br>ST-LC-0391<br>ST-LC-0396<br>ST-LC-0511<br>ST-LC-0512<br>ST-LC-8012<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8072<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0010<br>ISSUE-LC-0015

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：此范围副作用与LC3001/3004/3005关联，不能简单称逐项跳过。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0511<br>ST-LC-0512

**附加字段 obligation_mapping**：full

**附加字段 obligations**：

```json
[
  {
    "description": "源码范围首项NOT_USED/PERMOFF拒整范围，首项其他状态允许inclusive逐项调用。",
    "operation_ids": [
      "ST-LC-0302",
      "ST-LC-0304",
      "ST-LC-0305",
      "ST-LC-0306",
      "ST-LC-0307",
      "ST-LC-0512"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "范围门控通过后仅单项ACTIVE/PASSIVE求值，其余跳过且游标继续。",
    "operation_ids": [
      "ST-LC-0308",
      "ST-LC-0309",
      "ST-LC-0366"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "首项拒绝不影响合法索引ValidSampleCmd标true，因此仍可能后置WP减龄。",
    "operation_ids": [
      "ST-LC-0305",
      "ST-LC-0396",
      "ST-LC-0367",
      "ST-LC-0368",
      "ST-LC-0512"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：该实现与正式请求逐项义务的冲突按ISSUE-LC-0015保留；跨贡献末尾年龄尚需集成。

## REQ-LC-0070

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：LC_OperData.ARTPtr[APNumber].CurrentState = LC_APSTATE_PASSIVE; if (LC_AppData.CurrentLCState == LC_STATE_ACTIVE) ...

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：达到连续FAIL阈值的ACTIVE AP先转PASSIVE，随后由应用状态决定发RTS或只记被动抑制。

**触发/条件**：AP ACTIVE且本次FAIL连续计数>=阈值

**输入**：旧AP状态、应用状态、ADT

**输出**：AP PASSIVE；应用ACTIVE请求RTS或应用PASSIVE增抑制计数/DEBUG事件

**状态与历史**：应用状态不变、AP状态变

**处理及约束**：应用PASSIVE仍使AP转PASSIVE。<br>全局PassiveRTSExecCount加一；该DEBUG事件不加ART.CumulativeEventMsgsSent。<br>请求边界不是脚本执行完成。

**证据**：[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L138–197 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0337<br>RES-LC-0338<br>RES-LC-0339<br>RES-LC-0340<br>RES-LC-0349<br>RES-LC-0350<br>RES-LC-0351<br>RES-LC-0392<br>RES-LC-0394<br>RES-LC-0516<br>RES-LC-0702

**ST**：ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0337<br>ST-LC-0338<br>ST-LC-0339<br>ST-LC-0340<br>ST-LC-0349<br>ST-LC-0350<br>ST-LC-0351<br>ST-LC-0392<br>ST-LC-0394<br>ST-LC-0516<br>ST-LC-8010<br>ST-LC-8013<br>ST-LC-8055<br>ST-LC-8057<br>ST-LC-8058<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0017

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：补充记录有依据的活动行为；不是NASA正式要求，未运行LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0516

**附加字段 obligation_mapping**：full

**附加字段 obligations**：

```json
[
  {
    "description": "达到本次连续FAIL阈值且AP原ACTIVE，先持久AP PASSIVE，再按应用ACTIVE许可RTS。",
    "operation_ids": [
      "ST-LC-0337",
      "ST-LC-0338",
      "ST-LC-0339",
      "ST-LC-0340"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "应用PASSIVE时已改变AP，RTS禁止，只增全局PassiveRTSExecCount并登记DEBUG，不增加ART事件数。",
    "operation_ids": [
      "ST-LC-0349",
      "ST-LC-0350",
      "ST-LC-0351",
      "ST-LC-0516"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。<br>与原Once initiated状态时机及总事件口径差异分别保留ISSUE-LC-0007/0017。

## REQ-LC-0071

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：void LC_ExecuteRTS(uint16 RTSId) ... CFE_SB_TransmitMsg(..., true);

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：RTS适配函数构造任务配置MID/命令码/RTSId的请求包；发送返回码被忽略，计数表示尝试。

**触发/条件**：AP动作条件选择LC_ExecuteRTS

**输入**：RTSId、LC_RTS_REQ_MID、LC_RTS_REQ_CC

**输出**：SB请求尝试；无LC成功/失败返回

**状态与历史**：请求包局部变量；ART和全局计数由调用方更新

**处理及约束**：清零本地包，CFE_MSG_Init长度为sizeof包，设置FC与RTSId后发送。<br>函数void，CFE_SB_TransmitMsg返回值未向调用方提供。<br>不定义RTS执行回执或外部执行成功状态。

**证据**：[evidence/LC/fsw/src/lc_custom.c](evidence/LC/fsw/src/lc_custom.c) L42–56 LC_ExecuteRTS<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L156–160 LC_SampleSingleAP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0340<br>RES-LC-0341<br>RES-LC-0342<br>RES-LC-0343<br>RES-LC-0344<br>RES-LC-0345<br>RES-LC-0346<br>RES-LC-0394<br>RES-LC-0523<br>RES-LC-0703

**ST**：ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0340<br>ST-LC-0341<br>ST-LC-0342<br>ST-LC-0343<br>ST-LC-0344<br>ST-LC-0345<br>ST-LC-0346<br>ST-LC-0394<br>ST-LC-0523<br>ST-LC-8013<br>ST-LC-8055<br>ST-LC-8057<br>ST-LC-8058<br>ST-LC-8063<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：补充记录有依据的活动行为；不是NASA正式要求，未运行LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0523

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "RTS局部包按源码清零并按MID/FC/size宏设置头、RTSId载荷。",
    "operation_ids": [
      "ST-LC-0341"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "只在允许路径记录CFE_SB_TransmitMsg(...,true)提交位置，void/忽略返回不生成飞行成功或失败反馈。",
    "operation_ids": [
      "ST-LC-0342",
      "ST-LC-0523"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "调用位置之后计AP和全局请求尝试，禁止路径两计数不增；不称外部RTS成功执行。",
    "operation_ids": [
      "ST-LC-0343",
      "ST-LC-0344",
      "ST-LC-0345",
      "ST-LC-0346"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。<br>实际软件接口原子语法和依赖线格式未确认；不补造SC回执。

## REQ-LC-0072

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：Set all actionpoints to the new state except those that are not used or set permanently off

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：状态命令不能改变NOT_USED/PERMOFF；全选略过它们，单选拒绝。

**触发/条件**：合法NewAPState的SetAPState地面命令

**输入**：APNumber/ALL、旧状态、NewAPState

**输出**：修改可用项/保持保护项，成功或错误事件/计数

**状态与历史**：ART.CurrentState

**处理及约束**：全选命令整体成功，即使部分或全部项被跳过。<br>单选NOT_USED/PERMOFF发LC_APSTATE_CURR_ERR_EID并CmdErrCount加一。<br>可写新态仅ACTIVE/PASSIVE/DISABLED，不用该命令设PERMOFF。

**证据**：[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L353–474 LC_SetAPStateCmd

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0025<br>RES-LC-0107<br>RES-LC-0112<br>RES-LC-0113<br>RES-LC-0114<br>RES-LC-0115<br>RES-LC-0116<br>RES-LC-0117<br>RES-LC-0118<br>RES-LC-0119<br>RES-LC-0120<br>RES-LC-0546<br>RES-LC-0547<br>RES-LC-0548<br>RES-LC-0549<br>RES-LC-0550<br>RES-LC-0551<br>RES-LC-0704<br>RES-LC-0706<br>RES-LC-0707

**ST**：ST-LC-0006<br>ST-LC-0107<br>ST-LC-0112<br>ST-LC-0113<br>ST-LC-0114<br>ST-LC-0115<br>ST-LC-0116<br>ST-LC-0117<br>ST-LC-0118<br>ST-LC-0119<br>ST-LC-0120<br>ST-LC-0546<br>ST-LC-0547<br>ST-LC-0548<br>ST-LC-0549<br>ST-LC-0550<br>ST-LC-0551<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8076<br>ST-LC-8077<br>ST-LC-8078<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008<br>ST-LC-9013<br>ST-LC-9014<br>ST-LC-9015

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：补充记录有依据的活动行为；不是NASA正式要求，未运行LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0546<br>ST-LC-0548<br>ST-LC-0550

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "NOT_USED/PERMOFF在ALL跳过、单项拒绝",
    "operation_ids": [
      "ST-LC-0116",
      "ST-LC-0118",
      "ST-LC-0117",
      "ST-LC-0120",
      "ST-LC-0107"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0546",
      "ST-LC-0548",
      "ST-LC-0550"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0073

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：Actionpoints can only be turned permanently off if they are currently disabled

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：永久关闭命令仅允许单个已DISABLED AP，拒绝ALL和其他原状态。

**触发/条件**：SetAPPermOff有效长度命令

**输入**：APNumber、旧CurrentState

**输出**：PERMOFF或错误事件/拒绝计数

**状态与历史**：ART.CurrentState

**处理及约束**：APNumber必须合法且不是ALL。<br>必须旧状态DISABLED；失败不改变状态。<br>这个前置条件是代码补充，不覆盖LC4009无此条件的文字。

**证据**：[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L481–537 LC_SetAPPermOffCmd

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0025<br>RES-LC-0102<br>RES-LC-0103<br>RES-LC-0104<br>RES-LC-0107<br>RES-LC-0122<br>RES-LC-0123<br>RES-LC-0124<br>RES-LC-0125<br>RES-LC-0500<br>RES-LC-0702

**ST**：ST-LC-0006<br>ST-LC-0102<br>ST-LC-0103<br>ST-LC-0104<br>ST-LC-0107<br>ST-LC-0122<br>ST-LC-0123<br>ST-LC-0124<br>ST-LC-0125<br>ST-LC-0500<br>ST-LC-8019<br>ST-LC-8020<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8034<br>ST-LC-8035<br>ST-LC-8036<br>ST-LC-8037<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8079<br>ST-LC-8080<br>ST-LC-8081<br>ST-LC-8082<br>ST-LC-8083<br>ST-LC-8084<br>ST-LC-9002<br>ST-LC-9003<br>ST-LC-9004<br>ST-LC-9005<br>ST-LC-9007<br>ST-LC-9008

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0016

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：补充记录有依据的活动行为；不是NASA正式要求，未运行LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0500

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "永久关闭只允许有效单项且原状态Disabled，否则拒绝",
    "operation_ids": [
      "ST-LC-0122",
      "ST-LC-0123",
      "ST-LC-0124",
      "ST-LC-0102",
      "ST-LC-0103",
      "ST-LC-0104",
      "ST-LC-0107",
      "ST-LC-0500"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
    "operation_ids": [
      "ST-LC-0500"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。

## REQ-LC-0074

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：reset AP stats command does not modify AP state or most recent test result; reset WP stats command does not modify most recent test result

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：统计重置和表初始化分离：重置保留结果/状态/age；初始化重置结果为STALE且AP采用ADT默认状态。

**触发/条件**：统计地面命令或初始化/表更新

**输入**：ResetStatsCmd true/false、指定范围、ADT默认状态

**输出**：被选统计清0；条件性初始化状态/结果

**状态与历史**：WRT/ART历史

**处理及约束**：true：AP结果/当前状态保持；WP结果/CountdownToStale保持。<br>false：AP ActionResult STALE且CurrentState DefaultState；WP WatchResult STALE且CountdownToStale0。<br>最近跨越值/时间清0，两方向DataType字段未显式清除。

**证据**：[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L589–611 LC_ResetResultsAP<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L664–691 LC_ResetResultsWP

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0026<br>RES-LC-0108<br>RES-LC-0126<br>RES-LC-0128<br>RES-LC-0129<br>RES-LC-0130<br>RES-LC-0131<br>RES-LC-0132<br>RES-LC-0157<br>RES-LC-0158<br>RES-LC-0179<br>RES-LC-0181<br>RES-LC-0182<br>RES-LC-0556<br>RES-LC-0557<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0704<br>RES-LC-0705

**ST**：ST-LC-0007<br>ST-LC-0108<br>ST-LC-0126<br>ST-LC-0128<br>ST-LC-0129<br>ST-LC-0130<br>ST-LC-0131<br>ST-LC-0132<br>ST-LC-0157<br>ST-LC-0158<br>ST-LC-0179<br>ST-LC-0181<br>ST-LC-0182<br>ST-LC-0556<br>ST-LC-0557<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8025<br>ST-LC-8027<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8031<br>ST-LC-8040<br>ST-LC-8041<br>ST-LC-8042<br>ST-LC-8043<br>ST-LC-8044<br>ST-LC-8045<br>ST-LC-8085<br>ST-LC-8086<br>ST-LC-8087<br>ST-LC-9004<br>ST-LC-9005

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：补充记录有依据的活动行为；不是NASA正式要求，未运行LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0556<br>ST-LC-0558

**附加字段 obligation_mapping**：full

**附加字段 obligations**：

```json
[
  {
    "description": "统计复位明确保留AP状态/结果以及WP结果/年龄",
    "operation_ids": [
      "ST-LC-0130",
      "ST-LC-0131"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "cold初始化与stats命令区分：WP改STALE/age0，AP改STALE/ADT默认模式",
    "operation_ids": [
      "ST-LC-0157",
      "ST-LC-0158"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "表替换采用初始化语义，不套用统计复位的保留模式",
    "operation_ids": [
      "ST-LC-0179",
      "ST-LC-0181",
      "ST-LC-0182"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：无

## REQ-LC-0075

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：if (Result == CFE_TBL_INFO_UPDATED) ... LC_ResetResultsWP ... LC_CreateHashTable; ... LC_ResetResultsAP

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：WDT替换后清旧WRT并取消/重建订阅；ADT替换后清旧ART并采用新DefaultState。

**触发/条件**：HK处理后或SB超时维护；TBL返回INFO_UPDATED

**输入**：活动WDT/ADT handles、更新返回码

**输出**：新表指针、重置结果、重建WP路由/订阅

**状态与历史**：旧定义表/结果表及CmdPipe

**处理及约束**：先release可加载表地址，Manage两个定义表，再重新GetAddress。<br>WDT更新触发WRT初始化和hash/订阅重建；ADT更新触发ART初始化。<br>表地址获取失败返回fatal maintenance错误；dump-only表也被管理。

**证据**：[evidence/LC/fsw/src/lc_utils.c](evidence/LC/fsw/src/lc_utils.c) L43–108 LC_ManageTables<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L255–259 LC_SendHkCmd<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L111–117 LC_AppMain

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0030<br>RES-LC-0164<br>RES-LC-0165<br>RES-LC-0166<br>RES-LC-0167<br>RES-LC-0168<br>RES-LC-0169<br>RES-LC-0170<br>RES-LC-0171<br>RES-LC-0172<br>RES-LC-0173<br>RES-LC-0174<br>RES-LC-0175<br>RES-LC-0176<br>RES-LC-0177<br>RES-LC-0178<br>RES-LC-0179<br>RES-LC-0180<br>RES-LC-0181<br>RES-LC-0182<br>RES-LC-0502<br>RES-LC-0556<br>RES-LC-0557<br>RES-LC-0702<br>RES-LC-0704

**ST**：ST-LC-0011<br>ST-LC-0164<br>ST-LC-0165<br>ST-LC-0166<br>ST-LC-0167<br>ST-LC-0168<br>ST-LC-0169<br>ST-LC-0170<br>ST-LC-0171<br>ST-LC-0172<br>ST-LC-0173<br>ST-LC-0174<br>ST-LC-0175<br>ST-LC-0176<br>ST-LC-0177<br>ST-LC-0178<br>ST-LC-0179<br>ST-LC-0180<br>ST-LC-0181<br>ST-LC-0182<br>ST-LC-0502<br>ST-LC-0556<br>ST-LC-0557<br>ST-LC-8085<br>ST-LC-8086<br>ST-LC-8087<br>ST-LC-8088<br>ST-LC-8089<br>ST-LC-8090<br>ST-LC-8091<br>ST-LC-8092<br>ST-LC-8093<br>ST-LC-9009

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0019

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：补充记录有依据的活动行为；不是NASA正式要求，未运行LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0502<br>ST-LC-0556

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "WDT更新清旧WRT并重建订阅、ADT更新清ART且新DefaultState",
    "operation_ids": [
      "ST-LC-0178",
      "ST-LC-0179",
      "ST-LC-0180",
      "ST-LC-0181",
      "ST-LC-0182",
      "ST-LC-0164",
      "ST-LC-0166",
      "ST-LC-0168",
      "ST-LC-0173",
      "ST-LC-0176"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "CFE_TBL_Manage/ReleaseAddress/GetAddress、真实订阅更新和fatal return的软件接口绑定待确认；HK发送后及ReceiveBuffer超时两种原维护触发独立保留。",
    "operation_ids": [
      "ST-LC-0502",
      "ST-LC-0556"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：CFE_TBL_Manage/ReleaseAddress/GetAddress、真实订阅更新和fatal return的软件接口绑定待确认；HK发送后及ReceiveBuffer超时两种原维护触发独立保留。

## REQ-LC-0076

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：If LC cannot restore everything from CDS at startup, then LC will initialize everything

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：CDS恢复采用五对象全或无策略；保存失败会禁用后续CDS并继续应用。

**触发/条件**：启动恢复/后续维护CDS操作

**输入**：三LC CDS区、两个cFE critical表、HaveActiveCDS

**输出**：完整恢复或全套默认数据；保存失效后HaveActiveCDS=false

**状态与历史**：CDS handles/标志和五对象

**处理及约束**：任一恢复标志缺失走LC_LoadDefaultTables。<br>三LC区保存顺序WRT→ART→设APP保存标记→APP。<br>维护保存失败禁用CDS，表管理失败仍向主循环返回错误。

**证据**：[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L350–478 LC_TableInit<br>[evidence/LC/fsw/src/lc_utils.c](evidence/LC/fsw/src/lc_utils.c) L116–201 LC_UpdateTaskCDS / LC_PerformMaintenance

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0014<br>RES-LC-0032<br>RES-LC-0146<br>RES-LC-0147<br>RES-LC-0148<br>RES-LC-0149<br>RES-LC-0150<br>RES-LC-0151<br>RES-LC-0155<br>RES-LC-0157<br>RES-LC-0158<br>RES-LC-0159<br>RES-LC-0160<br>RES-LC-0162<br>RES-LC-0183<br>RES-LC-0184<br>RES-LC-0185<br>RES-LC-0186<br>RES-LC-0187<br>RES-LC-0188<br>RES-LC-0189<br>RES-LC-0190<br>RES-LC-0191<br>RES-LC-0192<br>RES-LC-0193<br>RES-LC-0503<br>RES-LC-0525<br>RES-LC-0526<br>RES-LC-0527<br>RES-LC-0558<br>RES-LC-0559<br>RES-LC-0702<br>RES-LC-0705

**ST**：ST-LC-0013<br>ST-LC-0146<br>ST-LC-0147<br>ST-LC-0148<br>ST-LC-0149<br>ST-LC-0150<br>ST-LC-0151<br>ST-LC-0155<br>ST-LC-0157<br>ST-LC-0158<br>ST-LC-0159<br>ST-LC-0160<br>ST-LC-0162<br>ST-LC-0183<br>ST-LC-0184<br>ST-LC-0185<br>ST-LC-0186<br>ST-LC-0187<br>ST-LC-0188<br>ST-LC-0189<br>ST-LC-0190<br>ST-LC-0191<br>ST-LC-0192<br>ST-LC-0193<br>ST-LC-0503<br>ST-LC-0525<br>ST-LC-0526<br>ST-LC-0527<br>ST-LC-0558<br>ST-LC-0559<br>ST-LC-8014<br>ST-LC-8015<br>ST-LC-8016<br>ST-LC-8017<br>ST-LC-8018<br>ST-LC-8025<br>ST-LC-8027<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8030<br>ST-LC-8031

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0018

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：补充记录有依据的活动行为；不是NASA正式要求，未运行LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0503<br>ST-LC-0525<br>ST-LC-0526<br>ST-LC-0527<br>ST-LC-0558

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "五对象全或无状态核对，不混用部分恢复与默认数据",
    "operation_ids": [
      "ST-LC-0146",
      "ST-LC-0147",
      "ST-LC-0148",
      "ST-LC-0149",
      "ST-LC-0150",
      "ST-LC-0151",
      "ST-LC-0155",
      "ST-LC-0157",
      "ST-LC-0158",
      "ST-LC-0159"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "WRT→ART→设APP标记→APP三阶段保存；任一真实失败停后阶段且禁用后续CDS并继续应用",
    "operation_ids": [
      "ST-LC-0183",
      "ST-LC-0184",
      "ST-LC-0185",
      "ST-LC-0186",
      "ST-LC-0187",
      "ST-LC-0188",
      "ST-LC-0189",
      "ST-LC-0190",
      "ST-LC-0191",
      "ST-LC-0192",
      "ST-LC-0193",
      "ST-LC-0503",
      "ST-LC-0525",
      "ST-LC-0526",
      "ST-LC-0527"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "三次CopyToCDS实际提交、逐阶段返回获取、失败EVS事件与维护入口绑定待论文软件资源确认；计算意图和被绑定返回值之间没有被模型伪装成执行。",
    "operation_ids": [
      "ST-LC-0503",
      "ST-LC-0525",
      "ST-LC-0526",
      "ST-LC-0527",
      "ST-LC-0558"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：三次CopyToCDS实际提交、逐阶段返回获取、失败EVS事件与维护入口绑定待论文软件资源确认；计算意图和被绑定返回值之间没有被模型伪装成执行。

## REQ-LC-0077

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：Permanantly disabled actionpoints get reported as unused

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：HK压缩将PERMOFF编码为NOT_USED，完整ART dump才保留两者差异。

**触发/条件**：HK请求打包

**输入**：WRT四值、ART状态/结果

**输出**：2bits/WP、4bits/AP的压缩数组，ActiveAPs计数

**状态与历史**：HK payload

**处理及约束**：WP非法结果编码ERROR；AP非法结果编码ERROR，非法状态编码NOT_USED。<br>PERMOFF和NOT_USED共享HK状态编码；不要按HK还原五状态。<br>WP打包循环每4项、AP每2项，平台容量需满足接口配置约束。

**证据**：[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L140–253 LC_SendHkCmd<br>[evidence/LC/fsw/inc/lc_interface_cfg.h](evidence/LC/fsw/inc/lc_interface_cfg.h) L89–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0030<br>RES-LC-0133<br>RES-LC-0134<br>RES-LC-0135<br>RES-LC-0137<br>RES-LC-0138<br>RES-LC-0139<br>RES-LC-0141<br>RES-LC-0149<br>RES-LC-0524<br>RES-LC-0701

**ST**：ST-LC-0011<br>ST-LC-0133<br>ST-LC-0134<br>ST-LC-0135<br>ST-LC-0137<br>ST-LC-0138<br>ST-LC-0139<br>ST-LC-0141<br>ST-LC-0149<br>ST-LC-0524<br>ST-LC-8022<br>ST-LC-8023<br>ST-LC-8024<br>ST-LC-8028<br>ST-LC-8029<br>ST-LC-8031<br>ST-LC-9000

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：补充记录有依据的活动行为；不是NASA正式要求，未运行LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0524

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "HK中PERMOFF/未知AP状态编码NOT_USED、未知结果ERROR；ART完整值不丢失",
    "operation_ids": [
      "ST-LC-0138",
      "ST-LC-0139",
      "ST-LC-0141"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "完整ART dump由cFE Table Services实际导出，软件服务论文绑定待确认。",
    "operation_ids": [
      "ST-LC-0524"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：完整ART dump由cFE Table Services实际导出，软件服务论文绑定待确认。

## REQ-LC-0078

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：CMakeLists.txt: if (CFE_EDS_ENABLED) lc_eds_dispatch.c else lc_dispatch.c

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：普通与EDS分发是条件构建分支；当前EDS表仅路由CMD/HK，与普通SampleAP/WP路由不等价。

**触发/条件**：构建选择CFE_EDS_ENABLED及消息到达

**输入**：构建标志、EDS dispatch返回值、MID/FC/size

**输出**：普通分支SampleAP/HK/CMD/WP分发；EDS分支仅CMD/HK或错误

**状态与历史**：CmdErrCount及业务路径选择

**处理及约束**：CFE_EDS_ENABLED真只编译lc_eds_dispatch.c，假只编译lc_dispatch.c。<br>EDS dispatch表未列SampleAP；未知MID返回错误后CmdErrCount加一；未见LC_CheckMsgForWPs。<br>EDS schema/生成代码与实际任务部署未冻结，不能外推隐藏的遥测/采样路由；登记功能范围差异。

**证据**：[evidence/LC/CMakeLists.txt](evidence/LC/CMakeLists.txt) L16–33 APP_SRC_FILES<br>[evidence/LC/fsw/src/lc_eds_dispatch.c](evidence/LC/fsw/src/lc_eds_dispatch.c) L42–106 LC_TC_DISPATCH_TABLE / LC_AppPipe<br>[evidence/LC/fsw/src/lc_dispatch.c](evidence/LC/fsw/src/lc_dispatch.c) L314–362 LC_AppPipe

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0020<br>RES-LC-0033<br>RES-LC-0034<br>RES-LC-0194<br>RES-LC-0195<br>RES-LC-0196<br>RES-LC-0504<br>RES-LC-0702

**ST**：ST-LC-0001<br>ST-LC-0016<br>ST-LC-0017<br>ST-LC-0194<br>ST-LC-0195<br>ST-LC-0196<br>ST-LC-0504<br>ST-LC-8032<br>ST-LC-8033<br>ST-LC-9001

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：代码分支事实明确；实际选择未知，LC2003/LC3001支持判断限定普通分支。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0504

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "普通/EDS是条件构建分支，普通四路由与EDS只有CMD/HK表分别表达",
    "operation_ids": [
      "ST-LC-0194",
      "ST-LC-0195",
      "ST-LC-0196",
      "ST-LC-0504"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "任务是否开启CFE_EDS_ENABLED、EDS字典/dispatcher依赖版本及真实失败返回待确认；未提供SampleAP/WP handler不能推定EDS与普通语义等价。",
    "operation_ids": [],
    "status": "pending-interpretation",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  },
  {
    "description": "真实ReceiveBuffer、EdsDispatch、EDS拒绝CmdErrCount持久写回及EVS提交尚未取得论文软件服务绑定。",
    "operation_ids": [
      "ST-LC-0504"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：任务是否开启CFE_EDS_ENABLED、EDS字典/dispatcher依赖版本及真实失败返回待确认；未提供SampleAP/WP handler不能推定EDS与普通语义等价。<br>真实ReceiveBuffer、EdsDispatch、EDS拒绝CmdErrCount持久写回及EVS提交尚未取得论文软件服务绑定。

## REQ-LC-0079

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：code-derived

**原始文字/行为**：uint8 EvalResult = LC_WATCH_FALSE; ... Unexpected LC_CustomFunction call ... return EvalResult;

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：默认custom钩子没有任务计算：发Unexpected错误事件但返回FALSE。

**触发/条件**：OperatorID==CUSTOM调用默认LC_CustomFunction

**输入**：WatchIndex、ProcessedWPData、消息、WDTCustomFuncArg

**输出**：LC_CFCALL_ERR_EID事件、WP结果FALSE

**状态与历史**：调用方按FALSE更新WRT

**处理及约束**：所有case/default进入同一错误事件分支。<br>忽略实际输入和自定义参数，保持初始FALSE返回。<br>该模板不能冒充任务custom函数，也不能推断错误结果ERROR。

**证据**：[evidence/LC/fsw/src/lc_custom.c](evidence/LC/fsw/src/lc_custom.c) L65–96 LC_CustomFunction<br>[evidence/LC/fsw/src/lc_watch.c](evidence/LC/fsw/src/lc_watch.c) L388–395 LC_ProcessWP

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0007<br>RES-LC-0008<br>RES-LC-0010<br>RES-LC-0014<br>RES-LC-0021<br>RES-LC-0022<br>RES-LC-0033<br>RES-LC-0200<br>RES-LC-0217<br>RES-LC-0218<br>RES-LC-0220<br>RES-LC-0226<br>RES-LC-0230<br>RES-LC-0269<br>RES-LC-0507<br>RES-LC-0702

**ST**：ST-LC-0002<br>ST-LC-0003<br>ST-LC-0014<br>ST-LC-0016<br>ST-LC-0200<br>ST-LC-0217<br>ST-LC-0218<br>ST-LC-0220<br>ST-LC-0226<br>ST-LC-0230<br>ST-LC-0269<br>ST-LC-0507<br>ST-LC-8100<br>ST-LC-8106<br>ST-LC-8107<br>ST-LC-8108<br>ST-LC-8110<br>ST-LC-8111<br>ST-LC-8112<br>ST-LC-8113<br>ST-LC-8115<br>ST-LC-8116<br>ST-LC-8117

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0003<br>ISSUE-LC-0004<br>ISSUE-LC-0020

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：补充记录有依据的活动行为；不是NASA正式要求，未运行LC。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0507

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "默认hook所有case/default Unexpected事件计划",
    "operation_ids": [
      "ST-LC-0218",
      "ST-LC-0507"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "返回初始FALSE，忽略数据/参数，调用方按FALSE处理",
    "operation_ids": [
      "ST-LC-0218",
      "ST-LC-0220",
      "ST-LC-0226",
      "ST-LC-0230",
      "ST-LC-0507"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "真实任务custom不能由stub推导",
    "operation_ids": [
      "ST-LC-0269"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "真正调用与EVS提交",
    "operation_ids": [
      "ST-LC-0218",
      "ST-LC-0507"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：ISSUE0020任务custom缺失；不能因错误事件把返回结果改ERROR或认定业务算法满足。

## REQ-LC-0080

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：design-derived

**原始文字/行为**：Watchpoints are evaluated whenever ... telemetry ... received; Actionpoints ... LC_SAMPLE_AP_MID ... normally ... scheduler

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：LC采用两个独立消息入口，AP调度频率是外部任务配置；不能将WP接收和AP评估强行并为一个周期。

**触发/条件**：设计和部署；运行时分别由监测消息及SampleAP消息到达触发

**输入**：外部遥测流、外部SampleAP请求源及其调度表

**输出**：各自入口处理，AP使用当时保存的WP结果

**状态与历史**：WRT跨消息持久保存，AP采样读取；LC没有规定全局ControlPeriod

**处理及约束**：调度器通常提供SampleAP请求，但发送者不是被固定为唯一SCH。<br>文档1HZ/10HZ示例仅部署建议，不能提升成LC必须周期。<br>通信等待超时维护间隔不是WP/AP业务采样周期。

**证据**：[evidence/LC/docs/dox_src/cfs_lc.dox](evidence/LC/docs/dox_src/cfs_lc.dox) L125–139 Design Overview<br>[evidence/LC/docs/dox_src/cfs_lc.dox](evidence/LC/docs/dox_src/cfs_lc.dox) L644–652 scheduler FAQ<br>[evidence/LC/fsw/src/lc_app.c](evidence/LC/fsw/src/lc_app.c) L91–126 LC_AppMain

**RES**：RES-LC-0001<br>RES-LC-0003<br>RES-LC-0004<br>RES-LC-0005<br>RES-LC-0007<br>RES-LC-0014<br>RES-LC-0029<br>RES-LC-0101<br>RES-LC-0194<br>RES-LC-0195<br>RES-LC-0196<br>RES-LC-0504<br>RES-LC-0528<br>RES-LC-0529<br>RES-LC-0530<br>RES-LC-0531<br>RES-LC-0548<br>RES-LC-0549<br>RES-LC-0700<br>RES-LC-0702<br>RES-LC-0707

**ST**：ST-LC-0010<br>ST-LC-0101<br>ST-LC-0194<br>ST-LC-0195<br>ST-LC-0196<br>ST-LC-0504<br>ST-LC-0528<br>ST-LC-0529<br>ST-LC-0530<br>ST-LC-0531<br>ST-LC-0548<br>ST-LC-0549<br>ST-LC-8021<br>ST-LC-8024<br>ST-LC-8032<br>ST-LC-8033<br>ST-LC-8034<br>ST-LC-8038<br>ST-LC-8041<br>ST-LC-8045<br>ST-LC-8075<br>ST-LC-8082<br>ST-LC-8084<br>ST-LC-8117<br>ST-LC-9001<br>ST-LC-9014<br>ST-LC-9015

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：supported

**检查层次**：static<br>manual

**人工语义核对**：设计说明与默认分支两消息入口吻合；未固定调度器版本/任务实际周期。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0504<br>ST-LC-0528<br>ST-LC-0530<br>ST-LC-0548

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "WP数据与SampleAP独立消息入口，模式/表状态跨入口持久共享但不合并周期",
    "operation_ids": [
      "ST-LC-0195",
      "ST-LC-0194",
      "ST-LC-0196",
      "ST-LC-0504"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "消息接收、分发到各独立Composite入口的系统声明，以及外部调度任务周期尚未绑定；没有在SpaceRDL补造固定周期。",
    "operation_ids": [
      "ST-LC-0504",
      "ST-LC-0528",
      "ST-LC-0530",
      "ST-LC-0548"
    ],
    "status": "pending-interface",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：消息接收、分发到各独立Composite入口的系统声明，以及外部调度任务周期尚未绑定；没有在SpaceRDL补造固定周期。

## REQ-LC-0081

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：design-derived

**原始文字/行为**：watchpoint and actionpoint definitions use two separate tables ... careful attention ... consistent with each other

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：任务部署需保持WDT与ADT一致；两表更新不是原子事务，必要时先将应用DISABLED。

**触发/条件**：在应用ACTIVE/PASSIVE期间更新一张或两张定义表

**输入**：新WDT/ADT、更新顺序、应用状态

**输出**：一致的活动定义表集合，或部署策略要求先禁用再更新

**状态与历史**：分开管理的WDT/ADT、WRT/ART

**处理及约束**：文档允许不停应用更新，但要求任务确保两张表关系有效。<br>单表验证仅查WP索引范围，未验证该WP是否已在另一WDT定义；不能宣称跨表一致性由LC自动保证。<br>DISABLED→加载/校验两表→恢复监测是候选任务策略，不是代码强制命令事务。

**证据**：[evidence/LC/docs/dox_src/cfs_lc.dox](evidence/LC/docs/dox_src/cfs_lc.dox) L200–209 table update operation<br>[evidence/LC/fsw/src/lc_action.c](evidence/LC/fsw/src/lc_action.c) L685–697 LC_ValidateRPN<br>[evidence/LC/fsw/src/lc_utils.c](evidence/LC/fsw/src/lc_utils.c) L43–108 LC_ManageTables

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0006<br>RES-LC-0007<br>RES-LC-0009<br>RES-LC-0011<br>RES-LC-0014<br>RES-LC-0023<br>RES-LC-0024<br>RES-LC-0034<br>RES-LC-0320<br>RES-LC-0370<br>RES-LC-0378<br>RES-LC-0380<br>RES-LC-0382<br>RES-LC-0395<br>RES-LC-0554<br>RES-LC-0555<br>RES-LC-0704

**ST**：ST-LC-0004<br>ST-LC-0005<br>ST-LC-0015<br>ST-LC-0017<br>ST-LC-0320<br>ST-LC-0370<br>ST-LC-0378<br>ST-LC-0380<br>ST-LC-0382<br>ST-LC-0395<br>ST-LC-0554<br>ST-LC-0555<br>ST-LC-8000<br>ST-LC-8002<br>ST-LC-8003<br>ST-LC-8004<br>ST-LC-8005<br>ST-LC-8006<br>ST-LC-8008<br>ST-LC-8009<br>ST-LC-8046<br>ST-LC-8047<br>ST-LC-8048<br>ST-LC-8049<br>ST-LC-8050<br>ST-LC-8051<br>ST-LC-8064<br>ST-LC-8065<br>ST-LC-8066<br>ST-LC-8073<br>ST-LC-8074<br>ST-LC-8075<br>ST-LC-8094<br>ST-LC-9006

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：unknown

**检查层次**：static<br>manual

**人工语义核对**：一致性是部署职责；没有用户任务部署表，策略仅有设计建议。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 conversion_revision**：已有计算/状态规则保留；新增真实接收/初始化/发送候选原子，论文软件资源绑定仍pending

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 native_interface_statements**：ST-LC-0554

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "WDT/ADT分表独立验证更新，ADT WP容量检查不等于另一WDT已定义，不能宣称LC自动跨表保证。",
    "operation_ids": [
      "ST-LC-0320",
      "ST-LC-0382",
      "ST-LC-0395"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "任务应保证活动时两表一致；先DISABLED再更新两表再启用仅文档建议策略，是否采用须任务方确认。",
    "operation_ids": [
      "ST-LC-0395"
    ],
    "status": "pending-interpretation",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  }
]
```

**附加字段 remaining**：缺实际任务表集合与更新策略，不能补造原子跨表事务或默认禁用命令；其他独立校验不受影响。

## REQ-LC-0082

**NASA 原始 ID**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**来源类别**：design-derived

**原始文字/行为**：LC_MAX_WATCHPOINTS ... multiple of 4; LC_MAX_ACTIONPOINTS ... multiple of 2; total size ... cFE ... table size limit

**原始理由/补充说明**：不适用（补充需求无 NASA 原始 ID；非算法资源无公式引用）

**规范化中文需求**：平台容量除数量上界外还须满足HK打包粒度及cFE单表最大尺寸约束。

**触发/条件**：平台配置和构建

**输入**：MAX_WATCHPOINTS、MAX_ACTIONPOINTS、结构大小、cFE table size limit

**输出**：合法容量和表尺寸

**状态与历史**：编译期容量；默认均176、实际任务选值未知

**处理及约束**：Watchpoint容量<=65520且为4倍数，避免packed结果越界。<br>Actionpoint容量<=65535且为2倍数。<br>WDT/ADT尺寸按容量乘结构大小计算，不超过依赖cFE平台最大单表尺寸。<br>该cFE上限实际数值和平台ABI未冻结，不编造具体字节大小。

**证据**：[evidence/LC/fsw/inc/lc_interface_cfg.h](evidence/LC/fsw/inc/lc_interface_cfg.h) L86–128 LC_MAX_WATCHPOINTS / LC_MAX_ACTIONPOINTS<br>[evidence/LC/fsw/src/lc_cmds.c](evidence/LC/fsw/src/lc_cmds.c) L140–253 LC_SendHkCmd

**RES**：RES-LC-0001<br>RES-LC-0002<br>RES-LC-0003<br>RES-LC-0007<br>RES-LC-0012<br>RES-LC-0013<br>RES-LC-0014<br>RES-LC-0030<br>RES-LC-0134<br>RES-LC-0135<br>RES-LC-0136<br>RES-LC-0137<br>RES-LC-0138<br>RES-LC-0139<br>RES-LC-0140<br>RES-LC-0197<br>RES-LC-0198

**ST**：ST-LC-0011<br>ST-LC-0134<br>ST-LC-0135<br>ST-LC-0136<br>ST-LC-0137<br>ST-LC-0138<br>ST-LC-0139<br>ST-LC-0140<br>ST-LC-0197<br>ST-LC-0198<br>ST-LC-8022<br>ST-LC-8023<br>ST-LC-8024<br>ST-LC-8039<br>ST-LC-9000

**ISSUE**：ISSUE-LC-0001<br>ISSUE-LC-0002<br>ISSUE-LC-0003<br>ISSUE-LC-0004

**语义映射**：partial

**表达形式**：mixed

**片段模板核对**：checked

**实现证据**：unknown

**检查层次**：static<br>manual

**人工语义核对**：配置约束有明文，默认容量满足粒度；ABI和实际cFE尺寸上限缺依赖版本。 最终映射复查：语义规则与证据已整理；消息/生命周期入口、聚合输入组装或软件服务实际提交仍没有核定的语言绑定，最终映射为partial；不是集成前暂存状态。

**附加字段 expansion_review**：全部义务按本轮分解逐项登记；expressed仅表示运算/赋值义务表达，接口/解释缺口独立保留。

**附加字段 obligation_mapping**：partial

**附加字段 obligations**：

```json
[
  {
    "description": "WP max65520/4倍数、AP max65535/2倍数和两张表的cFE单表尺寸上限均表达",
    "operation_ids": [
      "ST-LC-0197",
      "ST-LC-0198"
    ],
    "status": "expressed",
    "candidate_link_scope": "new sends linked to this obligation producer; unresolved receive/resource correspondence remains pending"
  },
  {
    "description": "实际部署LC_MAX_*、结构ABI sizeof及CFE_PLATFORM_TBL_MAX_SNGL_TABLE_SIZE未固定，不能对部署容量契约给成功结论。",
    "operation_ids": [],
    "status": "pending-interpretation",
    "candidate_link_scope": "broad interface gap: requirement-level candidates only; not a claim of complete obligation satisfaction"
  }
]
```

**附加字段 remaining**：实际部署LC_MAX_*、结构ABI sizeof及CFE_PLATFORM_TBL_MAX_SNGL_TABLE_SIZE未固定，不能对部署容量契约给成功结论。

