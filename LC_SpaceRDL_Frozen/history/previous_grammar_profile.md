# LC 使用的 SpaceRDL 语法核定记录

版本：3.0；核定日期：2026-10-11（Asia/Shanghai）。v1.2粗粒度入口合同保留为历史参考；v2.0展开义务；v3.0补齐七类原子形状与真实软件接口对应候选，G01–G20依据不变。用户选择严格论文语法，软件资源到论文设备/端口的对应仍待确认，不宣称标准软件扩展。本文件不是作者发布的语法标准、EBNF或解析器规范。

本次采用论文第 3.3 节表 7 的原子操作模板、表 8 的组合模板作为默认子集。`code.rdl` 可交付按这些模板组织的原子/组合操作片段；LC 事件驱动入口、软件服务接口以及完整系统上下文仍须适配。因此应分别报告“片段模板核对 checked”和“完整系统规约 pending”，不能合并成 `verified` 或声称通过官方解析器。论文介绍了原型编辑器（PDF 第 14 页、第 5.4 节），本次没有取得或运行该工具的正式解析器。

## 1. 依据与定位规则

主要依据 P1 为《面向航天控制系统的系统级需求描述语言》，用户提供文件 `定稿ra012-20260721.pdf`。该 PDF 共 19 页；本文件页码一律按 PDF 文件页序，括号内为页面印刷页码。`P1 p10 / 表 7 / Compute 行` 表示文件第 10 页、表 7 中的 Compute 行，避免把印刷页码 2213 当成文件页码。

| 依据代号 | 文件与固定哈希（SHA-256） | 本次用途 |
|---|---|---|
| P1 | `定稿ra012-20260721.pdf`；`f824899e2ed78fc11d77c91ba46eaa5a521ea386d13da81c56fdb9ba50d491b1` | 主要语法与资源模型依据；已读第 2–4 节，视觉核对 p4–13 的相关页与表 |
| P2 | `SunSearchSystemLeapfrog3.txt`；`8c1bf6567e06c23cb302f59416dd7e00285f17f8b94b11c33ad4d792e42019bc` | 具体案例与差异定位；行号按原文件，不按重新排版文档 |
| S1 | `spacerdl.zip`；`1046f89ca3f78ef151d29908a1bc12fce4229b022dff73c85c0fe64042d015e7` | 七文件组织参考；内部 `code.rdl` 原始行号用于差异记录，不能替代 P1 |
| F1 | `reviewer_feedback.md`；`5f1e4217a9f1682f5b581fad4bc0361f2fb1680cb14389208c903c2c4abecf1a` | 第 5 行指出 Compute 参数及引用字段需纠正；没有提供新的完整语法 |

资料的包内路径、获取信息和哈希复核见 `source_manifest.json`。任何后续语法依据变更都应更新 profile、检查器和受影响语句；不先修改检查器再倒推所谓标准。

## 2. 规则清单

| 规则 | 采用规则 | 外部依据与定位 | 适用范围及状态 |
|---|---|---|---|
| G01 | 原子语句形状为 `[调用时间约束] 原子操作 [运行时间约束]` | P1 p9（2212）/ §3.3(3)；p10（2213）/ 表 6–7 | 模板 checked；方括号是文献的可选元符号，不是要求原样写进语句 |
| G02 | 原子算子采用 `Init`、`GetData`、`SendData`、`ProTM`、`ProTC`、`Set`、`Compute` | P1 p9 / 表 5“操作指令”各行；p10 / 表 7“操作算子”列 | 本子集 checked；`DetAtt`、`CalCtrl` 等不加入算子集 |
| G03 | `Compute` 核心参数为 **输出、输入、引用关键字、算法条目**，不额外插入功能名 | P1 p9 / 表 5“控制计算”行：`Compute outputData inputData`；p10 / 表 7“Compute”行 | checked；算法功能名放资源，不占原子参数位置 |
| G04 | Compute 必须使用 `ReqCapByFormTable formDesc`；本次以 `FormulaTable.X` 命名已定义算法条目 | P1 p10 / §3.3(3)表 7 前段“只有 Compute…必选项”及表 7“Compute”行；`FormulaTable.B5` 的示例定位见 p13 / §5.2 代码 | 关键字与角色 checked；`FormulaTable` 是沿案例采用的引用命名，本项目需真正定义每个 X |
| G05 | 其他六个原子模板不附加公式/协议引用后缀 | P1 p10 / 表 7“Init/GetData/SendData/ProTM/ProTC/Set”各行 | checked；协议仍完整写入相关资源和追踪关系 |
| G06 | `Set varName value` 把目标变量赋为目标值；不能颠倒方向 | P1 p10 / 表 7“Set”行；p12（2215）/ 表 10“Set”行 | checked；若 value 是表达式，其具体表达式语法未完整给出，不自行扩大词法能力 |
| G07 | 组合算子采用 `Composite`、`If…Else`、`Switch…Case`、`While`、`Parallel`；可嵌套 | P1 p10 / §3.4 最后一段，明确 F1/F2 可为原子或组合；p11（2214）/ 表 8 | 模板 checked；表达式解析和并发调度语义需另有依据 |
| G08 | 组合预算位于组合右花括号之后：`Composite{…} Finished Within T`，分支、循环、并发同理 | P1 p11 / 表 8“语句模板”各行；p13 / §5.2 AppTask 完成时限说明；p14（2217）/ §5.3 的 If 示例 | checked；不采用预算置于左花括号前的旧 SMART 写法 |
| G09 | 不歧义的顺序可以用 `;` 表达；显式未命名 `Composite{…}` 是表 8 的顺序组合模板 | P1 p11 / 表 8“顺序”行“仅用‘;’作为间隔符”和 `Composite{F1; … F2; …}`；p12 / 表 11“Composite”行 | 作为操作片段 checked；裸组合不是完整系统根结构的证据 |
| G10 | 命名组合 `Composite modeProcess{…}` 是案例写法，未列入表 8 的参数模板 | P1 p13 / §5.2 代码首行；P2 原行 38；对比 P1 p11 / 表 8 | 本次默认不使用组合名称，以注释记录业务名称/ST；别名或命名规则 pending |
| G11 | 输入/输出集合 `{a, b}` 及数组标记 `[n]` 在案例中有依据，表 7 本身只列抽象参数 | P1 p13 / §5.2 `GetData gyro1 {deltG[9], GyroPowerState[9]}` 与 `Compute {nextMode} {…}` | 属案例扩展；一般集合语法、类型规则、数组下标与长度规则 pending；默认使用各一个已定义聚合数据名 |
| G12 | `At(t, period)` 表示从周期内 0 时刻算起的 t 时刻；第二项 `period` 不是任意独立数值周期声明 | P1 p10 / 表 6“指定时刻发生约束”两行；p14 / §5.2 `At(110ms, period)` 说明 | 模板 checked；LC 不据此写 `At(0, 60000ms)` 多周期调度 |
| G13 | `Over(T, c, n)` / `Over(T, nc, n)` 是时间窗口内连续/非连续发生 n 次 F，不能替代任意连续失败计数逻辑 | P1 p9 / §3.3(2)；p10 / 表 6“累积时间发生约束”两行 | 模板 checked；LC 的具体计数与动作逻辑在算法资源内按源码逐项定义 |
| G14 | `In(T1)`/`In[t1,t2]`/`After(T1)` 的含义按表 8，而非自然语言猜测 | P1 p11 / 表 8“顺序”行“含义”列 (1)–(3) | 模板可记录，未用于 LC 时不创造时间值；严格端点仍 pending |
| G15 | 完整模板包含 Import、System、任务、SystemConstraints；AppTask 具有预设控制周期；InterruptTask 可打断应用任务 | P1 p7（2210）/ §3.1 三类任务与图 3；p8（2211）/ §3.2 声明模板 | 模板 checked；LC 的消息到达/请求到达不是这些结构的自动等价物 |
| G16 | Controller/Device/Connect 描述硬件控制计算机、物理交互设备与端口连接 | P1 p4（2207）/ §2.1“物理设备”；p7–8 / §3.2 及三个声明模板；p5 / 表 1–2 | LC 的 SB/TBL/EVS/ES 软件服务记为真实软件资源，不擅自套 Device/端口/CPU |
| G17 | 算法资源处理过程可为公式、流程图或伪代码；资源须定义输入、输出和处理规则 | P1 p5（2208）/ §2.2(3)及表 3各行；p6（2209）/ §2.3 关联验证说明 | checked；逻辑/计数/状态变换可整理为算法，不要求硬凑数学公式 |
| G18 | 数据应有名称、类型、初值、单位、有效范围和语义；算法变量与资源定义关联且类型、单位一致 | P1 p6 / 表 4及 §2.3“关联验证”段 | 资源核对规则 checked；本项目 Markdown/JSON 是交付序列化，不是官方库文件格式 |
| G19 | Compute 映射为“输入→输出”，通信原子映射还有端口/协议/校验等资源展开 | P1 p12 / 表 10“Compute/GetData/SendData/ProTM/ProTC”各行；p11 / §4.1 | 数据变换可保留；向软件服务的实际提交及其失败路径不能仅因生成了输出就声称完成 |
| G20 | 对每条语句的分号、括号、追踪注释采用保守工程格式；检查范围必须显式列出 | P1 p7 / 图 3含 Import 分号与注释；p13 / §5.2 实际原子语句分号；交接文档 §6、§10 | 工程约定，不能据此推出作者完整词法规范；注释不增加触发或约束语义 |

## 3. 原子模板与 Compute 参数角色

下表只展示语法形状，所有小写占位名必须在交付中替换成有定义且有证据的资源/数据标识。A 表示可选调用时间约束，D 表示可选 `Finished Within T`。

| 原子算子 | 本次采用模板 | 参数含义 |
|---|---|---|
| Init | `A Init portName config D;` | portName 为硬件端口，config 为配置结构（表 7）；LC 不虚构硬件端口 |
| GetData | `A GetData devName dataName D;` | 从已建模设备获得数据（表 7）；LC 消息软件服务接收适配 pending |
| SendData | `A SendData devName dataName D;` | 向已建模设备输出控制数据（表 7）；LC 启动请求的消息提交适配 pending |
| ProTC | `A ProTC obdhName dataName D;` | 从数据管理计算机接收并按协议解析遥控（表 7），不是任何 CFE_SB 接收的别名 |
| ProTM | `A ProTM obdhName dataName D;` | 按数据管理计算机协议打包并发送遥测（表 7），不是任何 CFE_SB 发布的别名 |
| Set | `A Set varName value D;` | 左参数为被写变量，右参数为值或已定义数据（表 7） |
| Compute | `A Compute outputData inputData ReqCapByFormTable FormulaTable.F D;` | outputData 为输出，inputData 为输入，FormulaTable.F 为完整算法规则引用（表 7） |

Compute 的功能名称应放在算法资源的“功能名称”栏（P1 p5 / 表 3），不能放在 outputData 之前。以下正反例只是模板说明，不是 LC 的实际语句或已定义资源。

```text
Compute outputData inputData ReqCapByFormTable FormulaTable.F;
```

```text
// 以下不属于本次采用的模板：多插入了功能名参数。
Compute EvaluateWatchpoint outputData inputData ReqCapByFormTable FormulaTable.F;
// 以下不属于本次采用的模板：引用关键字采用了案例短写。
Compute outputData inputData ReqCapByTable FormulaTable.F;
// 以下不属于本次采用的模板：把引用字段加给了非 Compute 操作。
ProTM externalName packedData ReqCapByFormTable ProTable.TM;
```

实现核对还应检查 FormulaTable.F 的输入与输出与语句一致；只检查词数不能识别方向反转。若数据包含历史值，资源应把入参说明为处理前快照，出参说明为处理后结果，并列出提交顺序、禁止覆盖的状态和所有写入者。一个聚合输入/输出的成员仍须逐项定义：使用聚合名称不能隐去未知数据、失败条件或外部副作用。

论文没有发布本次可用的结构类型/字段访问完整词法语法。默认以资源目录中的单个聚合数据名称代表一份已定义输入或输出；这是在表 7 参数占位符上采用的项目命名办法，聚合类型的正式解析器支持仍为 pending。使用该办法必须保留真实 LC 类型和逐字段映射，不声称论文规定了新的 `struct` 语法。

## 4. 组合、时间及片段边界

表 8 支持下面的组合形状。方括号表示可选，不写入交付；F 是实际原子或组合，省略号仅是论文元符号，不能在实际 `code.rdl` 中代替处理。

```text
Composite { F1; F2; } [Finished Within T]
If (condExpr) { F1; } [Else { F2; }] [Finished Within T]
Switch (varName) { Case(value): { F1; }; } [Finished Within T]
While (condExpr) { F1; } [Finished Within T]
Parallel { F1 || F2 } [Finished Within T]
```

出处均为 P1 p11 / 表 8 对应行。实际片段选用 `Composite { ... }` 时不增加组合名。组合块末尾不凭空附加原子分号；原子内部依案例与工程约定以分号结束。条件表达式只在证据足够时使用；表 8 的 `condExpr` 不是一份已提供的 C 表达式语法。诸如 `&&`、按位操作、数组寻址和函数调用不能仅凭 C 源码存在就认定为 SpaceRDL 标准表达式。

时间含义应保留如下区别。

| 形状 | 表中含义及定位 | LC 使用注意 |
|---|---|---|
| `F Finished Within T` | P1 p10 / 表 6：F 在规定 T 内完成 | 无 LC 时限来源时省略，而不是用主循环等待值补造预算 |
| `At(t) F` | P1 p10 / 表 6：从绝对时间 0 算起的 t 时刻 | 0 时刻的系统含义需有证据；不是收到消息之后 t |
| `At(t, period) F` | P1 p10 / 表 6：从周期内 0 算起的 t 时刻 | 需已有周期上下文；不能拿第二项任意数值表示另一个周期 |
| `Over(T,c,n) F` | P1 p10 / 表 6：T 内连续发生 n 次 F | 不等价于“第 n 次失败后动作”；失败/通过复位在算法中明定 |
| `Over(T,nc,n) F` | P1 p10 / 表 6：T 内非连续发生 n 次 F | 不等价于永久累计；窗口边界不能猜测 |
| `F1; In(T1) F2` | P1 p11 / 表 8顺序行(1)：F1 后等待 T1，等待期间不可执行其他操作 | 不改写为普通非阻塞调度，也不把它移植成 LC 睡眠 |
| `F1; In[t1,t2] F2` | P1 p11 / 表 8顺序行(2)：F1 后等待 t1–t2，期间不可执行其他操作 | 开闭端点、精确起算事件未明确时 pending |
| `F1; After(T1) F2` | P1 p11 / 表 8顺序行(3)：F1/F2 发生间隔在 T1 内 | 表中并非“至少等 T1”；不按英文 After 猜译 |

P1 p11 / 表 8 的 While 行说明总执行时长在 T 内，P1 p12 / 表 11 的 While 映射行说明“单次迭代时间不超过运行时间约束”。两处作用域不能自动视为一致。LC 不因此选用未经核定的循环预算；如有使用，应单列 ISSUE，区分总预算和单次预算，语法/时序语义标 pending。

P1 p12 / 表 11 也明确顺序组合“严格的先后顺序”，以及 If/Switch 各分支路径、Parallel 整体执行时间的约束范围。纸面人工检查须比较操作时限与所属组合预算，不仅检查预算文字放在右花括号后。T 的严格/非严格端点、单位词法全集及超时事件表示未由资料完整给出，需保留原要求与未决项。

**裸 Composite 的核定结论：**`Composite { F1; F2; }` 有 P1 表 8 的直接语法依据，可交付为“顺序组合操作片段”。表 8 没有把它定义为完整系统的顶层编译单元；P1 §3.1、图 3 所示系统规约另含资源导入、硬件组成、任务和约束。故片段可以人工/静态核对其内部模板，文件整体的可解析性、片段加载方式和事件入口绑定必须 pending。无需为了让它外观完整而编造 LC 的 Controller、Device 或 ControlPeriod。

## 5. LC 执行上下文和软件接口的处理约定

LC 范围和触发证据以固定版本的正式要求、设计、源码为准。两个有区别的入口不能通过一个 Composite 的排列就合并成连续一次执行：收到被监测数据后形成 watchpoint 结果，以及收到 actionpoint 采样/评估请求后评估，是两类触发。实际代码位置在 `requirements.md`、`resources.md`、`statements.md` 和 `walkthrough.md` 逐项提供。

论文 p4 / §2.1 对业务逻辑的定义和 p5 / 表 3 支持整理 LC 的比较、RPN 求值、连续失败计数、状态更新等数据处理算法。论文 p7–8 / §3.1–3.2 同时显示其任务/设备模型面向硬件周期控制系统；这不足以确认软件总线、事件服务和表服务可直接声明为 Device。因此本次：

- 算法规则、输入输出和历史状态以资源目录保存；有确定数据变换义务的部分用表 7 Compute 表达。
- 真实 LC 的 SB、EVS、TBL、ES、CDS 等交互按软件服务/软件端点记录实际角色、接口、参数、返回值和失败路径。协议定义不会由于 RDL 不带 ProTable 后缀而删去。
- 可用输出对象明确区分“计算得到请求描述”与“已经向服务提交成功”。Compute 不自动代表 SB 发布、EVS 发事件、TBL 更新或外部 RTS 执行；实际提交或外部副作用保留在资源能力与规范化需求，正式语句映射依适配程度为 partial 或 none。
- 执行入口、实际调用顺序和资源绑定在注释与语句表中说明，但注释不算机器可检查的触发条件。完整外部调用与事件绑定需集中登记 ISSUE，继续完成独立数据变换。

最小片段组织如下（本段仅示意组织办法，数据与 FormulaTable 名必须换成实际已定义条目）：

```text
// 候选原子/组合片段；完整系统上下文和事件入口绑定 pending。
// ST/REQ 追踪注释：由真实 LC 数据接收入口调用，非周期/非中断声明。
Composite {
    Compute wpOutput wpInput ReqCapByFormTable FormulaTable.WP;
}

// 独立片段：仅在真实 LC 评估请求入口被调用，不能与上块合并为同一触发。
Composite {
    Compute apOutput apInput ReqCapByFormTable FormulaTable.AP;
}
```

实际交付 `code.rdl` 不能出现 `FormulaTable.WP` 等未定义占位项。ST 注释用于定位；语法核对只对实际操作本身和组合结构开展。可以同时统计原子与组合 ST，但包含关系必须显式，不能把一条原子因为被某组合包含而重复计为需求覆盖。

### 5.1 修订后的完整入口算法与持久状态合同

实际交付增加 ST-LC-0016 / RES-LC-0033 与 ST-LC-0017 / RES-LC-0034，仍只使用 G03–G04 已核定的四参数 Compute：

```text
Compute MonitorMessageOutput MonitorMessageInput ReqCapByFormTable FormulaTable.MonitorMessageFlow;
Compute SampleRequestOutput SampleRequestInput ReqCapByFormTable FormulaTable.SampleRequestFlow;
```

MonitorMessageFlow 的算法资源展开关联WP遍历、同项比较输出到统计输入的组装、逐项WRT写入和整包监测计数。SampleRequestFlow 展开独立请求的长度/范围/状态门、逐AP求值与动作决策、请求/事件调用顺序，以及所有AP结束后的WP年龄更新。这两条语句分别由两个真实消息入口触发；它们没有合成为一次执行或固定周期，也没有新增事件关键字。原子的 WatchCompare/WatchStats、EvaluateRPN/ActionDecision 及两个 Composite 保留作子规则的展开视图，不作为完整入口之后再重复运行的业务步骤。

每个入口 Input.state 是入口时的持久 StateSnapshot；Output.state 是本入口内部步骤后的状态。监测入口输出先对应持久 WRT/AppData，后续采样入口才读取它；每次采样后的状态再进入下一次采样或 HK 输入。同一采样区间中后一个 AP 的全局状态取前一 AP 已更新的工作状态，不能从请求最初快照重复组装。此合同以资源算法规则和项目数据字段检查，不是论文新增的字段访问、函数调用、结构声明或提交算子。

Output.orderedSteps 是本项目的有序写入/调用记录，用来保留状态提交和外部调用的交错顺序；Output.state 不是“全部副作用发生之前一次性提交”的指令。例如允许RTS路径保留 AP置PASSIVE → RTS调用 → 两项请求计数 → 动作事件 → 事件计数。采样计数在RPN之前增加，WP年龄在全部AP之后更新。未执行的事件/RTS计划保持未提交、回执未知；Compute 输出不能证明服务调用已发生。

status 区分 snapshot-only、ignored、rejected、indeterminate。actualResultKnown 区分可从输入/明确算术模型推导的状态结果与无法推导的结果，不表示真实服务运行成功。若原始32位无符号偏移求和回绕而放行巨大偏移，必须保留 indeterminate 与已知执行前缀，不能用理想化安全边界规则伪造 ERROR 或后续正常统计。目标ABI及服务实际观察结果未知处仍由问题清单登记。

上述合同改善了需求数据连接和语义可审查性；正式消息入口绑定、聚合类型加载、完整System上下文和真实服务提交仍为 pending，语法核对没有因此升级为官方解析或执行通过。

## 6. 材料间的差异及采用决定

| 差异 | 直接定位 | 本次决定 | 尚未得到的结论 |
|---|---|---|---|
| `ReqCapByFormTable` 与 `ReqCapByTable` | P1 p10 / 表 7前说明和 Compute 行采用长写；P1 p13 / §5.2 Compute 案例采用短写；P2 原行 29、35–39、49–50 均采用短写；S1 `code.rdl` 原行 4、107、111、129、173、179等 | 默认表 7长写，所有实际 Compute 统一 | 两者是否解析器别名未确认，不能宣称其中一种是所有版本唯一拼写 |
| Compute 额外功能名 | P1 p10 / 表 7只含输出、输入；S1 `code.rdl` 原行 107、111、129分别多出 BDotControl/SunPointControl/PowerForecast | 不复制旧 SMART 的参数列表 | 更新方言是否支持额外功能名未知 |
| 功能名被写成算子 | P2 原行 35–39、49有 ProVld/DetAtt/SwitchMode/CalCtrl；P1 表 7没有这些操作 | 功能名归算法资源，以 Compute 引用 | P2 对应完整语言版本未知 |
| 非 Compute 添加引用后缀 | P2 原行 29、50 的 ProTC/ProTM；S1 `code.rdl` 原行 173、179、191 的 ProTM/ProTC | 采用表 7两参数模板；协议保存到资源 | 更新版本是否支持 ProTable 后缀未知 |
| 组合预算位置 | S1 `code.rdl` 原行 47、159为 `Composite name Finished Within T {`；P1 p11 / 表 8预算在 `}` 后 | 后置预算；无有据 LC 时限则省略 | 旧检查器是否放行不能证明前置写法合法 |
| 命名 Composite | P1 p11 / 表 8无名称；P1 p13 / §5.2有 `Composite modeProcess`；P2 原行 38也有名称 | 默认未命名 Composite；业务名放注释 | 命名是否可作为定义/调用、是否必选未知 |
| Switch 冒号/Case 分块 | P1 p11 / 表 8：`Switch(varName){Case(value):{F1};…}`；P1 p13 / 案例 Case 后直接 Set；P2 原行 43为 `Switch(nextmode):{` | 如使用则按表 8；不复制 Switch 后冒号 | 宽松解析器接受范围未知 |
| 集合/数组语法 | 表 7为抽象参数，P1 p13 / §5.2集合与 `[9]` 的案例 | 优先单个聚合符号，集合扩展另标 | 一般集合、数组、维度解析及类型规则未知 |
| 任务周期数字 | P1 p12–14 / §5.1–5.2为 128ms/100ms/110ms；P2 原行 11、51、54为 160ms/130ms/128ms | 只作不同案例版本，不移植给 LC | 不能据此选择 LC 的周期或预算 |
| 案例语义与拼写疑义 | P1 p13叙述“若两者相同”初始化，而同页 If 是 `currentMode!=nextMode`；案例 Switch 写 nextmode，Compute 写 nextMode；P2 原行 54输出 pulseWidth 的对象为 gyro1 | 不复制疑义；LC 每个条件与符号对其自己的证据核对 | 无作者更正材料，不静默宣布案例哪一处正确 |
| While 预算范围 | P1 p11 / 表 8 While 行与 p12 / 表 11 While 行 | 不使用未经核定的循环预算 | 总时长与单次迭代约束关系待作者/解析器确认 |

## 7. 静态检查器的合同与限制

`scripts/validate_bundle.py` 是本项目交付一致性和模板子集检查器，既不是论文官方解析器，也不是 LC 程序测试。实际已实现、执行情况及正反例结果见 `validation_report.md`。本文件给出其应核对的依据和禁止扩大结论的边界。

| 检查目标 | 所依据规则 | 可自动判定的部分 | 必须另行人工核对/保持 pending 的部分 |
|---|---|---|---|
| 算子白名单 | G02 / 表 7 | 未知基本算子、错误拼写 | 新语言版本是否有合法扩展 |
| Compute 参数 | G03–G04 / 表 7、表 5 | 含额外功能名、缺公式表字段、关键字混用、引用条目不存在 | 输入输出方向、字段依赖、算法完整性与类型单位 |
| 引用范围 | G05 / 表 7 | 非 Compute 使用 ReqCap 后缀 | 资源内协议是否足够定义交互能力 |
| 组合与预算 | G07–G10 / 表 8 | 括号不配对、前置预算、违反所采用模板的命名组合 | 真实调用/触发、分支和总预算是否相容 |
| 数据/资源存在 | G17–G19 / 表 3–4及 §2.3 | 已定义 ID/数据名、引用存在、声明和算法输入输出名一致 | 快照/更新时刻、未知数据、接口提交、副作用完整性 |
| 分号/追踪定位 | G20 / 案例与本项目约定 | 原子分号、语句表和实际 code 片段一致、行号有效 | 注释不能证明触发或约束可执行 |
| 完整文件上下文 | G15–G16 / §3.1–3.2 | 可识别本次声明的“操作片段”身份 | 完整根结构、软件端点/事件适配和官方解析器加载均未核定 |

检查器应对其尚未支持的结构报告“未检查”，不能以忽略该结构的方式给通过。如果实际 code 只使用 Compute 和未命名 Composite，报告范围就限定这两者；其他模板记为人工核定而非自动验收。验证报告必须至少区分：包内一致性、片段模板、资源适配、需求语义、LC 实现证据、真实执行测试。

正反例应覆盖 Compute 多余参数、错误引用后缀、未定义数据/算法、组合时限前置、错误 ISSUE 引用、statements/code 不一致。遗漏持续条件或将采样请求与数据到达合并为同一触发，不应伪报为正则检查器可判定，应在人工走查和 walkthrough 中逐项复核。

## 8. 集中待确认事项

这些是语法/建模问题，不是 LC 的新增业务需求。它们已映射到 `issues.md` 的实际 ISSUE-ID，只阻塞相应表达部分，不阻塞正式需求清单、资源补全或数据变换片段。

1. 片段如何导入完整 SpaceRDL 编译单元、是否允许无 System/任务上下文，以及规范根结构的完整 EBNF。
2. 与硬件周期控制不同的事件驱动软件应用如何绑定真实消息入口；应用消息不得自动映射为 InterruptTask，也不得补造 ControlPeriod。
3. SB/EVS/TBL/ES/CDS 软件服务是否有经过确认的资源类型与交互原子；现有 Device/Connect 模型不足以直接确认。
4. ReqCapByTable 是否为 ReqCapByFormTable 的正式别名；非 Compute 协议后缀和功能名算子是否属于另一个确认版本。
5. 命名 Composite、集合/数组/聚合类型、表达式和单位的完整词法、语法及类型规则。
6. While 预算的总执行/单次迭代范围，时间间隔的起算点与端点以及超时处理语法。
7. 是否能取得可复现的官方语法解析器和相匹配的资源库格式；本次没有此条件，不给官方解析通过标签。

本交付对语法的结论为：**表 7/8 的已选片段模板可以核对；软件资源与事件上下文采用明确记录的待适配边界；完整 LC SpaceRDL 系统规约和官方解析器验收 pending。**这三个结论必须分别报告。

## 9. 本次实际采用的自动检查子集

最终code.rdl保留旧15 Compute和2 Composite为历史非执行参考；当前有326个独立定义：Init 3、GetData 7、SendData 27、ProTM 1、ProTC 6、Set 34、Compute 248。前五类44个操作均为软件资源对应候选、paper_binding=pending，不作为严格标准已确认计数。库存由data/statistics.json复算；循环/复用以occurrences定位，不重复算独立操作。旧§5的入口合同不在新增AST后再次执行。

本轮检查器支持七类原子形状及未命名无预算Composite、If (declaredBoolean)、While (declaredBoolean)，Else须对应If。新增五类仅接受两个单名参数和分号，拒绝引用后缀；参数须分别追踪到真实软件端点与数据定义，方向与合同逐项匹配，且强制保持paper_binding=pending。checked只表示形状/项目合同检查。拒绝条件内C表达式、字面量、字段/数组访问及未知guard。每个guard需在使用前产生，While体须刷新guard。资源别名官方格式仍pending，不能误当默认TRUE输入。

Switch、Parallel、命名组合、时限、完整System/任务/硬件/端口未纳入自动接受范围，遇到显式失败。已依LC-dev真实调用形成SendData等候选，但LC软件服务与论文物理设备/端口不能自动等价；未新增Device、Connect、port或周期，相关接口义务仍pending-interface。Init尤其仅表达软件注册候选，不把注册成功写成论文硬件端口初始化已获确认。正式原文与代码差异单列documentary视图及pending-interpretation。

新检查scripts/check_expansion.py核对全部82条的义务清单、expressed操作存在/位置/反向REQ、pending缺口登记、boolean产生及循环刷新；tests/test_expansion.py检查流程顺序和禁止路径。这些是结构及纸面核对，不证明算法公式真实执行、语义等价、LC运行或官方解析通过。

片段的完整事件上下文、软件服务提交、聚合资源格式与官方解析器验收分别由 ISSUE-LC-0001/0002/0003 登记为 pending；参考材料方言差异见 ISSUE-LC-0014。实际执行结果与限制以 validation_report.md 和随包日志为准。
