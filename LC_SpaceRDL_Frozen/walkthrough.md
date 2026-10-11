# 需求—资源—片段—结果的贯通讲解

这是源码行为与当前表达范围的贯通说明，不是已可运行的全系统SpaceRDL例程。监测消息和独立Sample Request是两个入口，不能合成一个虚构周期。

## 1. 监测消息更新持久结果

lc_app.c接收软件消息，lc_dispatch.c按MID路由到监测处理；这个接收/触发过程未获得论文任务绑定。输入已到达后，片段检查LC状态，选中WP，按源码原类型计算偏移、解码和比较，再提交WP结果、统计与age，最后提交整包监测次数。

极端偏移可能整数回绕：必须保留代码实际算术及风险记录，不能把片段解释为“所有越界必然拒绝”。NaN、STALE/ERROR及统计更新以各片段规则和证据为准，不凭其他版本审查推定错误。

## 2. 独立评估请求读取此前的监测结果

只有另一个Sample Request到达才进入AP评估，读取已经持久化的WRT/ART和状态。DISABLED、NOT_USED、PERMOFF不请求RTS；其他路径按RPN结果、连续失败阈值和LC ACTIVE/PASSIVE条件继续。不能让一个监测Compute暗中调用评估。

## 3. 正常动作和禁止动作

允许路径保留源码AP先变PASSIVE、准备RTS、提交位置、请求尝试计数、事件及结果的相对顺序；禁止路径不生成RTS效果并按规则更新抑制统计。请求描述和提交位置仅是数据，实际CFE_SB_TransmitMsg及事件发送尚未表达；因此不能将这些片段称为已发出请求的运行证明。

## 4. 精确映射实例（完整规则可顺着链接审阅）

### ST-LC-0200 — 读取独立监测入口快照

需求：REQ-LC-0006, REQ-LC-0007, REQ-LC-0008, REQ-LC-0009, REQ-LC-0010, REQ-LC-0011, REQ-LC-0012, REQ-LC-0013, REQ-LC-0014, REQ-LC-0016, REQ-LC-0065, REQ-LC-0066, REQ-LC-0067, REQ-LC-0079

资源合同：RES-LC-0200（resources.md / resources.json）

```spacerdl
Set WMonitorWorking WMonitorEntry;
```

产生/保持的结果：M是本次监测工作快照；仅复制已有输入，不创建周期、不接入采样入口。

[完整规则](statements.md#st-lc-0200)；code.rdl L1112

### ST-LC-0201 — 实现监测入口应用状态门

需求：REQ-LC-0009

资源合同：RES-LC-0201（resources.md / resources.json）

```spacerdl
Compute WMonitorEnabled WMonitorWorking ReqCapByFormTable FormulaTable.WMonitorEnabled;
```

产生/保持的结果：WMonitorEnabled是下一If/While使用的已定义boolean；不提交持久状态。

[完整规则](statements.md#st-lc-0201)；code.rdl L1114

### ST-LC-0207 — 按原C算术判断偏移并单独识别回绕风险

需求：REQ-LC-0009, REQ-LC-0013, REQ-LC-0065

资源合同：RES-LC-0207（resources.md / resources.json）

```spacerdl
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPOffsetArithmetic;
```

产生/保持的结果：WMonitorWorking为本操作后的工作快照；下一上下文操作右参数读取此值。仅下面列明的成员改变，其余message/table/config/state/effects及历史保持。

[完整规则](statements.md#st-lc-0207)；code.rdl L1127

### ST-LC-0230 — 提交当前WP统计与age候选

需求：REQ-LC-0007, REQ-LC-0008, REQ-LC-0009, REQ-LC-0012, REQ-LC-0014, REQ-LC-0066, REQ-LC-0067, REQ-LC-0079

资源合同：RES-LC-0230（resources.md / resources.json）

```spacerdl
Set WPStatisticsPersistent WStatisticsCandidate;
```

产生/保持的结果：仅提交当前WP CumulativeTrueCount、ConsecutiveTrueCount、CountdownToStale、FalseToTrueCount与两向记录中候选改变的字段；不覆盖已经提交WatchResult/EvaluationCount和其他WP。

[完整规则](statements.md#st-lc-0230)；code.rdl L1179

### ST-LC-0234 — 提交一次整包监测计数

需求：REQ-LC-0009

资源合同：RES-LC-0234（resources.md / resources.json）

```spacerdl
Set WMonitoredMsgCountPersistent WNewMonitoredMsgCount;
```

产生/保持的结果：绑定LC_AppData.MonitoredMsgCount并更新工作镜像。

[完整规则](statements.md#st-lc-0234)；code.rdl L1211

### ST-LC-0300 — 取得独立采样请求与已持久化监测结果快照

需求：REQ-LC-0017, REQ-LC-0018, REQ-LC-0022, REQ-LC-0064, REQ-LC-0069

资源合同：RES-LC-0300（resources.md / resources.json）

```spacerdl
Compute ActionWorking ActionInput0300 ReqCapByFormTable FormulaTable.SampleEntrySnapshot;
```

产生/保持的结果：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

[完整规则](statements.md#st-lc-0300)；code.rdl L563

### ST-LC-0309 — 保留 DISABLED、NOT_USED、PERMOFF AP 且禁止其RTS

需求：REQ-LC-0018, REQ-LC-0022, REQ-LC-0030, REQ-LC-0031, REQ-LC-0032, REQ-LC-0033, REQ-LC-0069

资源合同：RES-LC-0309（resources.md / resources.json）

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.PreserveSkippedAP;
```

产生/保持的结果：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

[完整规则](statements.md#st-lc-0309)；code.rdl L768

### ST-LC-0340 — 核定应用ACTIVE才许可RTS请求

需求：REQ-LC-0027, REQ-LC-0028, REQ-LC-0070, REQ-LC-0071

资源合同：RES-LC-0340（resources.md / resources.json）

```spacerdl
Compute ApplicationActiveForRTS ActionWorking ReqCapByFormTable FormulaTable.ApplicationActiveForRTS;
```

产生/保持的结果：定义平坦的 boolean 数据 ApplicationActiveForRTS，供后继条件或 Set 使用；不替换工作快照。

[完整规则](statements.md#st-lc-0340)；code.rdl L670

### ST-LC-0341 — 按现有任务配置组装RTS请求描述

需求：REQ-LC-0027, REQ-LC-0071

资源合同：RES-LC-0341（resources.md / resources.json）

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.PrepareRTSRequest;
```

产生/保持的结果：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

[完整规则](statements.md#st-lc-0341)；code.rdl L673

### ST-LC-0342 — 在允许路径登记RTS请求提交位置

需求：REQ-LC-0027, REQ-LC-0028, REQ-LC-0033, REQ-LC-0071

资源合同：RES-LC-0342（resources.md / resources.json）

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.AppendRTSRequestEffect;
```

产生/保持的结果：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

[完整规则](statements.md#st-lc-0342)；code.rdl L675

### ST-LC-0343 — 在RTS效果位置之后计算AP请求尝试数

需求：REQ-LC-0027, REQ-LC-0033, REQ-LC-0071

资源合同：RES-LC-0343（resources.md / resources.json）

```spacerdl
Compute APRTSAttemptNext ActionWorking ReqCapByFormTable FormulaTable.IncrementAPRTSAttempt;
```

产生/保持的结果：定义平坦的 uint32 数据 APRTSAttemptNext，供后继条件或 Set 使用；不替换工作快照。

[完整规则](statements.md#st-lc-0343)；code.rdl L677

### ST-LC-0346 — 写回全局RTS请求尝试数

需求：REQ-LC-0027, REQ-LC-0033, REQ-LC-0071

资源合同：RES-LC-0346（resources.md / resources.json）

```spacerdl
Set PersistentGlobalRTSAttempt GlobalRTSAttemptNext;
```

产生/保持的结果：持久绑定 LC_AppData.RTSExecCount，仅此成员写回；后续工作快照读取此新值，不重置同AP其他统计或应用/WP状态。 ActionWorking中的对应成员是该持久目标的别名：本Set写回同时刷新该别名，供下一Compute使用；别名绑定是项目数据合同、官方格式仍待确认。

[完整规则](statements.md#st-lc-0346)；code.rdl L683

### ST-LC-0365 — 记录本AP不满足动作条件时RTS禁止不变量

需求：REQ-LC-0020, REQ-LC-0021, REQ-LC-0025, REQ-LC-0027, REQ-LC-0029, REQ-LC-0030, REQ-LC-0031, REQ-LC-0032, REQ-LC-0068

资源合同：RES-LC-0365（resources.md / resources.json）

```spacerdl
Compute ActionWorking ActionWorking ReqCapByFormTable FormulaTable.NoRTSForCurrentResult;
```

产生/保持的结果：显式就地写新 ActionWorking；后继 Compute/If/While 读取其新值；只变更本操作所列成员/effects。项目聚合/成员别名格式仍pending-interface，未声称官方struct语法。

[完整规则](statements.md#st-lc-0365)；code.rdl L722, L749, L757, L762

## 审查结论

可贯通查阅需求、资源、源码定位、片段和数据结果；真实软件消息入口/提交仍blocked。不存在全需求已严格转换完成的贯通运行例子。
