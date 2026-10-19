# LC 从需求到结果报告的贯通例子

## 性质、版本和来源

这是基于源码的纸面走查，没有运行 LC/cFS，也没有执行官方 SpaceRDL 解析器。所有数值变化是按本包资源规则推演的预期值。修订后的 `code.rdl` 用两个独立的完整入口计算，表达消息内的处理顺序、逐项数据连接和入口结束后的持久状态；真实消息入口到语言的绑定、聚合类型解析及 SB/EVS/TBL/CDS 提交仍待确认。本例不能证明 RTS 已执行或异常已消除。

LC 基线为 `f54e136220d8d6f2e207ba57073a9faeef9d3b0f`。例子选用同一基线的源码注释 WP113/AP101，完整来源文件保存在 `evidence/LC/`，文件指纹见 `source_manifest.json`。这些条目处于注释块，当前默认 WDT/ADT 全为 NOT_USED。走查只假定任务已按当前字段定义装载相应表条目，不声称默认程序已包含它们；本包没有生成可直接装载的飞行表。

## 原始义务、规范化需求和表达位置

下表短原文来自 `evidence/LC/docs/lc_FunctionalRequirements.csv` 的物理行，完整原文及处理约束见 `requirements.md`。

| 原始 ID / 规范化 ID | 短原文 | 来源行 | 本例中的资源 / 语句 |
|---|---|---|---|
| LC2003 / REQ-LC-0009 | “Upon receipt of a message, LC shall compare the data in the message …” | 16–18 | RES-LC-0033/0021；ST-LC-0016，细节 ST-LC-0002 |
| LC2003.1 / REQ-LC-0010 | “LC shall support the following comparison values” （包含 `<`） | 19–25 | RES-LC-0033/0021；ST-LC-0016/0002 |
| LC2003.3 / REQ-LC-0012 | “… False, LC shall set the Number of Consecutive True values to zero.” | 27 | RES-LC-0033/0022；ST-LC-0016/0003 |
| LC2004 / REQ-LC-0014 | “… maintain the following statistics in the dump-only Watchpoint Results Table” | 29–39 | RES-LC-0010/0022/0033；ST-LC-0016/0003 |
| LC3001 / REQ-LC-0018 | “Upon receipt of a Sample Request, LC shall process the request specified Actionpoints …” | 46–48 | RES-LC-0034/0023/0024；ST-LC-0017，细节 ST-LC-0004/0005 |
| LC3001.1 / REQ-LC-0019 | “… Reverse Polish Operators … equals” | 49–54 | RES-LC-0034/0023；ST-LC-0017/0004 |
| LC3002.3 / REQ-LC-0027 | “… Fail result for the table-defined consecutive number of times limit …” | 64–67 | RES-LC-0034/0024；ST-LC-0017/0005 |
| LC3002.3.1 / REQ-LC-0028 | “Once an RTS is initiated, LC shall change … to Passive.” | 68 | RES-LC-0034/0024；ST-LC-0017/0005；实现顺序差异在 issues.md 登记 |
| LC3002.4 / REQ-LC-0029 | “… currently Passive … action was not taken …” | 69–71 | RES-LC-0034/0024；ST-LC-0017/0005 禁止路径 |
| LC3006 / REQ-LC-0033 | “… statistics in the dump-only Actionpoint Results Table” | 75–83 | RES-LC-0011/0024/0034；ST-LC-0017/0005 |
| LC8000 / REQ-LC-0050 | “… generate a housekeeping message …” | 136–145 | RES-LC-0012/0030；ST-LC-0011 |

消息到达与采样请求是两种独立触发。这里没有指定调度周期，也没有把 `LC_SB_TIMEOUT` 转成控制周期。

## 先看清楚两个入口怎样连接

LC 先把一条监测消息算成 WP 的结果并存入 WRT。之后独立到达的 SampleAP 请求，读取那时已经保存的 WRT，依据 AP 的表达式、当前状态和历史计数决定是否请求 RTS。没有 SampleAP 请求时，遥测比较结束就停在 WRT；同一份 WP 结果可以被后续多个采样请求读取。一个入口完成后形成的新状态，是下一个入口的历史输入。

完整入口对应实际 `code.rdl` 中的两条语句：

```text
Compute MonitorMessageOutput MonitorMessageInput ReqCapByFormTable FormulaTable.MonitorMessageFlow;
Compute SampleRequestOutput SampleRequestInput ReqCapByFormTable FormulaTable.SampleRequestFlow;
```

这是两个分别调用的算法，文本相邻不表示收到遥测后立即执行采样。ST-LC-0016 / RES-LC-0033 只处理监测消息；ST-LC-0017 / RES-LC-0034 只处理独立采样请求。它们引用的算法资源完整规定内部循环、数据组装、分支和写入/调用顺序。保留的 WP/AP 原子语句及 Composite 是子规则的展开视图，用于复核算法细节，不能再作为额外业务步骤重复执行或重复累计计数。

| 时点 | 本次入口输入 | 本次入口输出 | 下一步怎样取得数据 |
|---|---|---|---|
| 收到监测消息 | MonitorMessageInput.message 与入口前 StateSnapshot | MonitorMessageOutput.state 中的新 WRT、整包监测计数及有序事件记录 | 对应 LC 已写入的持久 WRT/AppData；等待另一条消息 |
| 收到 SampleAP 请求 | SampleRequestInput.message 与此时的持久 StateSnapshot | SampleRequestOutput.state 中的新 ART/AppData 和最后更新的 WP 年龄；有序请求/事件记录 | 对应本次采样完成后的持久 ART/WRT/AppData |
| 再收到 SampleAP 或 HK 请求 | 上一次入口结束后的状态，允许中间合法命令或表维护改变它 | 再次采样后的状态，或由 HK 打包的报告 | 不从最初初值重算，不丢失先前累计和状态改变 |

以上字段属于本项目数据合同，不是新增 SpaceRDL 字段访问或事件语法。`orderedSteps` 保存源码中可核对的写入与服务调用次序，不能解释成“先一次性提交最终快照，再批量发送所有事件/请求”。`status=snapshot-only` 表示只计算候选结果，`ignored` 表示被状态门或入口条件跳过，`rejected` 表示已知校验失败，`indeterminate` 表示无法据现有证据推导后续结果。`actualResultKnown` 只说明该状态变换结果可否推导；即使可推导，也不证明真实服务已执行。未运行时 RTS/event 的提交状态仍不为成功。

## 例子的表输入与初始状态

WP113 来自 `fsw/tables/lc_def_wdt.c:58–68`；AP101 来自 `fsw/tables/lc_def_adt.c:68–83`。下列参数原样保留来源值，不把它们升级为 NASA 的通用业务阈值。

| 条目 | 字段和值 | 说明 |
|---|---|---|
| WP113 | DataType = UWORD_BE；OperatorID = LT | 16 位无符号大端，严格小于 |
| WP113 | MessageID = PSE_FAST_HK_TLM_MID | 符号的具体数值不在 LC 仓库中，保留未知 |
| WP113 | WatchpointOffset = 184；BitMask = LC_BITMASK_NONE | 偏移从完整消息首字节计算，含消息头；掩码为 0xFFFFFFFF |
| WP113 | ComparisonValue.Unsigned16 = 3319 | 注释旧路径是 `.Unsigned16in32.Unsigned16`；当前 `LC_MultiType_t` 在 `config/default_lc_tblstruct.h:81–91` 定义 `.Unsigned16`。本例用当前字段解释阈值，没有改动源码注释或把旧初始化器当成可编译表 |
| WP113 | ResultAgeWhenStale = 0；CustomFuncArgument = 0 | 原注释参数；不是为演示而新造年龄 |
| AP101 | DefaultState = DISABLED；三个事件限额均为 2 | MaxPassiveEvents/MaxPassFailEvents/MaxFailPassEvents 各 2 |
| AP101 | RTSId = RTS_ID_DIVINER_SAFE_MODE；MaxFailsBeforeRTS = 3 | RTS 数字未知，不给它随意分配 ID |
| AP101 | RPNEquation = `{113, LC_RPN_EQUAL}` | EQUAL 终止并取结果，不是双目相等比较 |
| AP101 | EventType = INFORMATION；EventID = LC_BASE_AP_EID + 101 | `LC_BASE_AP_EID=1000`，故该例事件号为 1101；事件文本为 `Diviner: low input volt (2)` |

纸面场景中只有此 WP 和 AP 被使用，其他条目仍为 NOT_USED；初始化完成但未有监测消息时，WRT113 是 STALE/Countdown0，ART101 是 STALE/DISABLED，相关计数均 0。应用仓库默认上电状态也是 DISABLED。先发送两条合法地面命令：SetLCState(ACTIVE)，再 SetAPState(AP101, ACTIVE)。源码状态命令见 `lc_cmds.c:317–474`；候选表示为 ST-LC-0006 / RES-LC-0025 的命令快照变换。两个命令成功后 CmdCount=2，CmdErrCount=0；状态不是自行变成 ACTIVE。

## 正常路径：比较、三次评估、动作计划和报告

### 1. 相关消息到达，生成 WP 结果

教学测试输入为无符号值 **3300**：这是自拟的测试数据，不是任务配置、正式需求阈值或实测遥测。完整消息的偏移 184、185 处是大端字节 `0x0C 0xE4`，实际长度至少 186，MID 为上述保留符号。消息时间戳用输入报文的有效时间 `T_msg` 表示，不补造历元/时间数值。

真实调用链：`LC_AppPipe` 将其他 MID 转给 `LC_CheckMsgForWPs`（`lc_dispatch.c:314–360`）；应用 ACTIVE 且 MID 匹配则调用 `LC_ProcessWP`（`lc_watch.c:270–452`）。本例偏移 184、数据宽度 2 不发生求和回绕，长度检查为 `184+2 <= actualLength`；按 UWORD_BE 提取为 3300，按掩码后仍为 3300，`3300 < 3319` 为 TRUE。极端偏移的另一条实现路径在后文单独说明。

MonitorMessageInput 从本次消息、处理前持久 StateSnapshot、当前索引上下文、配置和备用当前时间组装。应用允许处理时，MonitorMessageFlow 先解析消息时间戳，仅在秒和子秒均为零时取当前时间，再按真实 MID 索引遍历有关联的 WP；未找到 WP 时只规划 LC_MID_INF_EID 的 INFORMATION 事件，业务状态和监测计数保持不变。每项把同一 WPIndex 的 WDT 与当前 WRT 送入 WatchCompare，再将比较输出连同该项原 WRT/WDT 送入 WatchStats。ST-LC-0014 中保留的细节为：

```text
Compute WatchCompareOutput WatchCompareInput ReqCapByFormTable FormulaTable.WatchCompare;
Compute WatchStatsOutput WatchStatsInput ReqCapByFormTable FormulaTable.WatchStats;
```

本次 WP113 的具体连接是 `WatchStatsInput.comparison = WatchCompareOutput`、oldResult = 比较前 WRT113、definition = 同一 WDT113、WPIndex = 113。比较后先写 WatchResult，再增加 EvaluationCount，随后更新 TRUE/FALSE/ERROR/STALE 各分支字段。WatchStatsOutput.newResult 成为本次工作状态的 WRT113。所有关联 WP 处理结束后，仅把 MonitoredMsgCount 加一。完整的组装和状态推进由 RES-LC-0033 明确规定；这不是裸 Composite 自动提供的能力，正式类型与入口绑定仍待确认。

| WRT113 / 全局字段 | 比较前 | 比较后 | 依据 |
|---|---|---|---|
| WatchResult | STALE | TRUE | RES-LC-0021/0022 |
| EvaluationCount | 0 | 1 | 合法提取并进行比较 |
| ConsecutiveTrueCount / CumulativeTrueCount | 0 / 0 | 1 / 1 | TRUE 分支 |
| FalseToTrueCount | 0 | 1 | 源码把旧 STALE 到 TRUE 也记录在这里 |
| LastFalseToTrue | 值/时间 0 | 值 3300、DataType UWORD_BE、时间 T_msg | 来源为本次掩码后的数据和消息时间 |
| CountdownToStale | 0 | 0 | 装入原表参数 ResultAgeWhenStale=0 |
| MonitoredMsgCount | 0 | 1 | 每个有关联 WP 的消息加一次，不按 WP 个数加 |

MonitorMessageOutput.state 保存下表的新 WRT113 和全局监测计数，ART101 仍为 STALE/ACTIVE，APSampleCount 仍为 0，RTS 请求计数仍为 0。消息到达仅刷新 WP，尚未评估 AP，没有 RTS 计划。

### 2. 三个后续采样请求分别评估 AP101

每次采样的载荷为 StartIndex=EndIndex=101，UpdateAge 非零，长度为当前构建的 `sizeof(LC_SampleAPCmd_t)`；不猜测 cFE 消息头字节数。三个请求之间没有新监测报文，原表 age=0 使 Countdown 仍为 0，不会在递减循环中变成 STALE。因此三次采样都消费上述同一个 TRUE 结果；连续失败阈值计数的是 AP 评估，不要求三条独立遥测。

真实入口先验证消息长度与采样范围，再检查起始 AP 可工作，单 AP 只有 ACTIVE/PASSIVE 才被评估（`lc_cmds.c:44–107`、`lc_action.c:41–108`）。SampleRequestInput.state 取上次入口已保存的状态，SampleRequestFlow 此时才开始 AP 处理。每个合格 AP 先增加全局 APSampleCount，再求 RPN。RPN `{113, EQUAL}` 压入 WRT113 的 TRUE，再取出作为最终结果；TRUE 映射到 ACTION_FAIL。

SampleRequestFlow 在内部逐 AP 连接求值与决策；ST-LC-0015 保留的细节为：

```text
Compute RPNOutput RPNInput ReqCapByFormTable FormulaTable.EvaluateRPN;
Compute ActionOutput ActionInput ReqCapByFormTable FormulaTable.ActionDecision;
```

RPNInput.WPResults 读取本请求开始后、年龄递减前的 WRT 全表。ActionInput.evaluation 取刚生成的 RPNOutput，oldResult 取本 AP 的历史 ART，oldApp 取工作状态中到此时为止的 AppData，definition/APIndex 始终对应同一 AP。若一次请求有多个 AP，后一个 AP 的 oldApp 必须继承前一 AP 已更新的全局计数，不能每项重复使用请求最初的快照；单 AP 的 APSampleCount 在求值前增加一次，子规则不得再增加一次。ActionOutput.newResult/newApp 回写工作状态，使下一个 AP 看到累积后的状态。

全部 AP 完成后，且仅在合法范围与 UpdateAge 非零时，才遍历所有 WRT 的非零 Countdown 并递减；减至零才写 STALE。本例原 age=0，所以三次都保持 TRUE。SampleRequestOutput.state 既包含 AP 决策后的状态，也包含末尾年龄更新后的状态；每次保存该输出后，再等待下一条独立请求。Dispatch 的分类结果不能在求 RPN 之前提前执行年龄更新。未执行真实提交时 RTSPlan.submitted=false、acknowledged=unknown，事件也不标为已发出。

| 请求 | RPN / AP 结果 | 连续 / 累计 FAIL | AP 状态（前→后） | 本次 RTS / 事件效果 |
|---|---|---|---|---|
| 第一次 | TRUE → FAIL | 1 / 1 | ACTIVE → ACTIVE | 未达 3；前结果 STALE，不产生 PASS→FAIL 转换事件 |
| 第二次 | TRUE → FAIL | 2 / 2 | ACTIVE → ACTIVE | 未达 3；前结果 FAIL，不产生转换事件 |
| 第三次 | TRUE → FAIL | 3 / 3 | ACTIVE → PASSIVE | 应用 ACTIVE，形成一次 RTS 请求与 ADT 动作 INFO 事件 |

第三次的源码顺序是：先增加 APSampleCount、求值并写 ActionResult/失败计数；达阈值后先把 AP 置 PASSIVE；应用 ACTIVE 时调用 `LC_ExecuteRTS`；调用返回后增加 ART.CumulativeRTSExecCount 和 AppData.RTSExecCount；再发 ADT 动作事件，之后增加 ART.CumulativeEventMsgsSent（`lc_action.c:100–182`）。本例没有 PASS→FAIL 转变事件，所以这一阶段的 orderedSteps 不包含该调用；有该转变时，它发生在阈值分支之前。

预期请求内容为当前配置的 LC_RTS_REQ_MID / LC_RTS_REQ_CC 和表符号 RTS_ID_DIVINER_SAFE_MODE；默认接口 MID=0x18A9、CC=4 仅是仓库默认值，不证明当前部署采用它。消息由 `LC_RTSRequestCmd_t` 定义，LC_Custom 的真实发布见 `lc_custom.c:42–55`。LC_ExecuteRTS 返回 void，内部没有以 SB 成功回执控制这些计数，不能把调用后加一改写成外部 RTS 完成后加一。

按该源码路径推演：APSampleCount=3，ART101.CumulativeRTSExecCount=1，AppData.RTSExecCount=1，CumulativeEventMsgsSent=1，PassToFailCount=0，PassiveRTSExecCount=0。动作事件号为 1101，INFO，文本为源表文本加 `: AP = %d, FailCount = %d, RTS = %d` 尾文；参数 AP=101、FailCount=3、RTS=上述符号。这里的计数表示请求调用路径，不是 SB 交付或 RTS 完成确认。

### 3. 独立 HK 请求报告当前状态

合法 LC_SEND_HK_MID 请求触发 ST-LC-0011：

```text
Compute HKOutput HKInput ReqCapByFormTable FormulaTable.Housekeeping;
```

HKInput.state 读取第三次 SampleRequestOutput.state 保存后的 AppData、WRT/ART，并附运行上下文；HKOutput 形成待发布 packet 与维护计划。真实 `LC_SendHkCmd` 的顺序是时间戳、发送 HK，再表/CDS 维护（`lc_cmds.c:114–260`）。为隔离本例，假定请求前后没有新表更新；没有运行服务时，维护 observedStatus 仍是 not-run。

| HK 字段 | 推演值 | 数据连接 |
|---|---|---|
| CmdCount / CmdErrCount | 2 / 0 | 前置两条状态命令；地面计数内部 uint16 转 HK uint8 |
| CurrentLCState | ACTIVE=1 | AppData.CurrentLCState |
| APSampleCount / MonitoredMsgCount | 3 / 1 | 三次 AP 评估 / 一次相关消息 |
| RTSExecCount / PassiveRTSExecCount | 1 / 0 | 允许请求路径 / 无被动抑制 |
| WPsInUse / ActiveAPs | 1 / 0 | 一条活动 WP；AP101 已 PASSIVE |
| WP113 的 2 bit | TRUE=1，位于 WPResults[28] 的 bit2–3 | `113//4=28`、移位 `2*(113%4)=2`；所选位置掩码值 0x04 |
| AP101 的 4 bit | `(PASSIVE=2)<<2 \| (FAIL=1)` = 0x9，位于 APResults[50] 高半字节 | `101//2=50`、移位 `4*(101%2)=4`；所选位置掩码值 0x90 |

不能把原 STALE 枚举 255 直接打进 HK；WP 与 AP 结果先变成两位编码。这里给出的 0x04/0x90 是所选条目的位贡献，其他同字节条目也有各自编码。结果消息是否被消费者收到未有本次运行证据。

## 禁止路径：应用或 AP 被动时抑制请求

从同样的一条 TRUE 监测结果和零失败计数重新开始，只把应用状态经合法命令设为 PASSIVE，AP101 仍 ACTIVE。应用 PASSIVE 允许监测比较及采样；前三次仍产生 FAIL 1、2、3。第三次达到阈值后，源码先令 AP101 PASSIVE，但不调用 LC_ExecuteRTS、不生成 RTS 计划、不增加两个 RTS 请求计数；AppData.PassiveRTSExecCount=1。改走 LC_PASSIVE_FAIL_DBG_EID 的 DEBUG 事件路径，该事件不增加 ART.CumulativeEventMsgsSent；PassiveAPCount 此时还是 0。依据为 `lc_action.c:143–196` / RES-LC-0024。原需求“RTS initiated 后变 PASSIVE”与这一实现顺序差异保留在 issues.md。

若继续采样已经 PASSIVE 的 AP101，其 FAIL 计数仍增加。下一次达阈值会令 PassiveAPCount=1、PassiveRTSExecCount=2，产生 LC_AP_PASSIVE_FAIL_INF_EID 的 INFO 事件；随后 PassiveAPCount=2 时仍发事件，=3 时超过表限额2而停止该类事件，但抑制计数继续递增（`lc_action.c:199–219`）。没有自动重新激活 AP，没有外部 RTS 请求。此路径保留 LC3002.4 的“禁止动作、统计和有限事件”三项关系。

## 边界和失败路径检查

1. **严格阈值边界**：在正常路径第三次后接收值 3319（自拟边界输入，大端字节 `0x0C 0xF7`）。LT 比较为 FALSE；WRT 连续 TRUE 清零、LastTrueToFalse 记录值/时间，再采样得到 PASS、AP 连续 FAIL 清零。AP 状态仍 PASSIVE，不自动回 ACTIVE；由 FAIL→PASS 的转换事件受 MaxFailPassEvents=2 限制。对应 REQ-LC-0012/0020 和 RES-LC-0021/0022/0024。
2. **普通短消息**：本例偏移仍为184、宽度2，求和不回绕。长度185时 `184+2>185`，LC_WPOffsetValid 拒绝该 WP，先调用错误事件，再写 WRT ERROR/Countdown0，禁止提取字节，不增加 EvaluationCount；但有关联 WP 的整包 MonitoredMsgCount 仍加一。随后合法采样的 RPN 消费 ERROR，ART 置 ERROR、不产生 RTS；源码保留旧 ConsecutiveFailCount，不能把 ERROR 当作 PASS。此结论仅属于本次普通短消息分支，不能推广为所有数学越界输入均被拒绝。对应 LC2003.4/LC3001.3（REQ-LC-0013/0021），证据 `lc_watch.c:780–866`、`lc_action.c:259–275`。
3. **首次消息之前与过期**：WRT113 初值 STALE；采样结果为 ACTION_STALE，并清 AP 连续 FAIL。本例的 age=0 只是不由倒计时机制自动转 STALE，不能推导“从来没有 STALE”。非零 age 的末尾递减规则在 RES-LC-0034 中保留，没有为本例另造一个飞行表参数。例如仅就通用规则检查一个入口前 Countdown=1 的 TRUE：本次 AP 仍读取 TRUE；全部 AP 处理后该 WP 才变 STALE，下一次请求读取 STALE。该数值是通用边界检查输入，不是 WP113 的表参数。
4. **应用 DISABLED**：同一遥测或采样请求不进行 WP/AP 评估，采样也不更新 WP 年龄。AP DISABLED/NOT_USED/PERMOFF 不被单条评估；特别是采样起始 AP NOT_USED/PERMOFF 会阻止整个请求区间评估，而合法范围的 UpdateAge 更新仍可继续。这是源码补充规则，不能以理想化“逐项自动跳过”替代。
5. **极端偏移可能回绕**：独立算术检查改用 Offset=0xFFFFFFFF、宽度2、MsgLength=186；它不是 WP113 的任务参数。LC_WPOffsetValid 的 Offset/NumOfDataBytes 均声明为 uint32，源码先求 `Offset+NumOfDataBytes` 再与 size_t 长度比较（`lc_watch.c:782–866`）。在两操作数按32位无符号类型运算的目标上，和回绕成1，`1>186` 为假，检查会放行；随后 LC_ProcessWP 仍用原偏移形成指针并读取，不能推断成 ERROR 或正常比较结果。目标ABI尚未固定，应同时保留该算术模型的前提与目标确认问题。MonitorMessageOutput 对此是 `status=indeterminate`、`actualResultKnown=false`，orderedSteps 只保留可确认的检查/尝试读取前缀，不伪造后续 WRT、统计或成功结束状态。没有运行真实非法内存访问。“所有数学越界都应被拒绝”作为安全要求与实现差距单列，不偷偷换成安全求和来解释原代码。
6. **NaN 与统计边界**：本例 UWORD_BE 不承载 NaN；在另一个合法 FLOAT WP 的纸面检查中，成功提取的掩码后位模式若为 NaN，FloatCompare 返回 ERROR，但已经进入比较，所以 EvaluationCount 加一，连续 TRUE 保持，Countdown清零；它与第2项“未进入比较、不加评估计数”不同。下一次合格 AP 采样仍增加 APSampleCount，ERROR 保持连续 FAIL并禁止 RTS。数据无穷按比较算子处理，不能统一改为 ERROR；WDT 浮点阈值必须有限且非NaN。依据 `lc_watch.c:379–452`、`lc_watch.c:677–774` 和 `lc_action.c:100–275`。

这些是静态源码核对和纸面分支推演。随包针对性检查的真实命令、结果和范围见 validation_report.md；即使项目合同模型或算术样例实际运行通过，也不能记为 LC/cFS 程序运行通过。

## 衔接和保留边界

| 上游输出 | 下游消费 | 本包中的连接与状态 |
|---|---|---|
| SB 监测消息 / MID / actualLength | MonitorMessageInput.message | RES-LC-0033完整入口；真实软件入口到规约绑定 pending |
| WatchCompareOutput | 同一WP的 WatchStatsInput.comparison，加旧 WRT/WDT/WPIndex | MonitorMessageFlow 内部明确组装并写入工作 WRT，子语句不重复运行 |
| MonitorMessageOutput.state | 持久 WRT/AppData，再进入独立 SampleRequestInput.state | 跨消息读上次已保存的结果，不自动触发AP、不要求新遥测 |
| RPNOutput | 同一AP的 ActionInput.evaluation，加当前工作 ART/AppData/ADT | APSampleCount先加；多AP使用逐项推进的AppData，年龄尚未递减 |
| ActionOutput.newResult/newApp | 当前请求工作状态；所有AP完成后更新WP年龄 | 状态写入与服务调用顺序由 orderedSteps展开，不能合并为一次先行提交 |
| SampleRequestOutput.state | 持久 ART/WRT/AppData，再由下一次 SampleRequestInput或HKInput读取 | 最终状态含末尾老化；表/状态命令可在后续消息间改变状态 |
| SampleRequestOutput.RTSRequests/events | SB / EVS 调用边界 | 只形成有序计划；submitted=false；没有 SC 回执/执行完成证据 |
| HKOutput.packet/servicePlans | HK 发布与表/CDS 维护 | 字段/顺序已定义；真实 API 结果为 not-run；HK 调用处忽略维护返回的实现限制另登记 |

本例的两条完整入口计算给出可以逐字段复核的状态处理链，保留真实入口绑定、正式聚合类型和服务执行的表达边界。它是独立审查的检查样例，不能用作全量覆盖率或正式解析/执行通过的证明。
