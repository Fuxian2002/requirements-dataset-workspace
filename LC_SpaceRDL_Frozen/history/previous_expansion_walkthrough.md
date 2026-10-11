# LC 本轮原子分解：从真实需求到完整处理链

## 1. 本文证明什么，不证明什么

本轮不再用两条整入口 `Compute` 代替业务流程。监测、独立采样、命令、初始化、表验证/订阅、HK 与 CDS 已分别整理为操作和带分支/循环的流程；每项规范化需求另有义务清单。完整库存是 REQ-LC-0001 至 REQ-LC-0082，原正式要求与代码补充仍分开，操作数不是完成率。

本文是按冻结需求、源码和本轮资源规则进行的纸面贯通讲解，不是运行结果。LC 基线仍为 `f54e136220d8d6f2e207ba57073a9faeef9d3b0f`，本地LC-dev97文件与冻结证据逐字节相同，没有修改原工程。表7全部七类原子形状及表8的Composite/If/While用于候选片段；条件使用已定义boolean，RDL正文不混入C字段、数组访问、OnMessage或虚构周期。五类交互的软件资源对应仍pending，语句形状与资源语义分开核定。

软件SB/EVS/TBL/ES/CDS的源码行为已形成接收/发送等候选操作；到论文设备/端口的正式对应、ProjectFlowContext类型/成员别名加载及完整System入口仍待确认。Compute产生effects只作描述；发送义务由紧邻交互候选单独表达，不能默认Compute已发消息，更不证明LC或官方解释器已运行。

本轮真实连接增加：监测入口`GetData LCSoftwareBus LCMonitorEnvelope;`，独立采样入口`GetData LCSoftwareBus LCSampleEnvelope;`，HK入口`GetData LCSoftwareBus LCHKRequestEnvelope;`；接收后经当前消息和持久状态桥接进入后文业务链。共享CmdPipe只接收一次，这些是互斥选中路径的规约视图，不在每个handler重复接收。地面命令才用ProTC，保留原payload字节，先验证实际sizeof长度再访问typed字段。

许可动作分支在ST0342意图位置后增加`SendData LCRTSConsumer LCRTSRequestFrame;`（ST-LC-0523），仍在AP转PASSIVE后、请求次数计算前；禁止分支没有这条语句。ST0348动作事件参数之后增加`SendData LCEventService LCEventData0348;`（ST-LC-0515），随后才计事件数。HK负载Set之后经时间戳/发送意图位置进入`ProTM LCDataManager LCHousekeepingFrame;`（ST-LC-0524），随后维护表和CDS。以上均为明确标注pending的软件绑定候选，不算论文标准已确认。

详细规则和证据见 [resources.md](resources.md)、[statements.md](statements.md) 和 [动作点分解](data/decomposition/action_contribution.json)、[监测点分解](data/decomposition/watch_contribution.json)、[命令与生命周期分解](data/decomposition/commands_lifecycle_contribution.json)。语句以实际 [code.rdl](code.rdl) 为准；旧入口封装只作为历史背景，不再追加执行一次。

## 2. 两种消息入口，经持久状态衔接

```text
监测消息到达                         独立 SampleAP 请求到达
  GetData → 应用/MID/偏移门             GetData → 长度/状态/范围/首项门
  取数 → native字节序 → 掩码             读取此时已经保存的 WRT
  关系/custom比较                       逐 AP RPN → AP 结果 Set
  WP 结果 Set → 比较次数 Set              连续计数 Set → 阈值与许可/禁止
  TRUE/FALSE/ERROR/STALE统计 Set          RTS SendData或抑制 → 事件/计数
  整包计数一次 Set                      所有 AP 之后才维护 WP age
             └── 持久 WRT/AppData ───────┘
                                        ↓ 等待另一条独立 HK 请求
                                  状态快照 → 位打包 → HK负载 Set
                                  ProTM时间戳/发送 → 表/CDS维护边界
```

这里的横向连接是状态来源，不是新触发条件。收到遥测不会自动触发 AP；没有新遥测也可以再次采样同一 WP 结果。同一采样请求内后一 AP 读取前一 AP 已更新的 AppData，不能反复复制入口初始计数。所有 AP 结束后更新的 WRT age，才由下一次请求看到。

本轮用平坦工作符号承接中间结果。以 `WMonitorWorking` 为例，每条同名输入/输出 `Compute` 的右参数读取操作前快照，左参数是操作后快照；资源规则逐项列出改变成员，未列成员保持。独立标量 `Set` 写当前 WP 对应持久字段，并同步其工作镜像。boolean 输出只供分支选择，不能替代工作状态。

## 3. 一个完整例子：WP113 / AP101

### 3.1 依据、参数和前置命令

WP113 来自 `evidence/LC/fsw/tables/lc_def_wdt.c` 的 58–68 行，AP101 来自 `evidence/LC/fsw/tables/lc_def_adt.c` 的 68–83 行。它们在源码注释中，不是当前已装载的飞行表；默认 WDT/ADT 条目均为 NOT_USED。本文沿用原 [walkthrough.md](walkthrough.md) 的教学场景，假定按当前字段定义装载这些条目，没有生成可直接装载的任务表。

| 项目 | 保留的来源参数 |
|---|---|
| WP113 | UWORD_BE、LT、MID=`PSE_FAST_HK_TLM_MID`、偏移184、掩码 `LC_BITMASK_NONE` |
| WP113 | 比较阈值3319；age=0；custom参数0 |
| AP101 | 初始 DISABLED；RPN `{113, LC_RPN_EQUAL}`；连续FAIL阈值3 |
| AP101 | RTS符号 `RTS_ID_DIVINER_SAFE_MODE`；三个事件限额各2；INFO事件 `LC_BASE_AP_EID+101` |

原注释使用旧联合体初始化字段，按当前 `LC_MultiType_t` 解释其阈值，不假称旧注释原样即可编译。MID/RTS符号的部署数值缺失，不能随意补编号。

先有两条合法独立地面命令：设置应用 ACTIVE，再设置单个 AP101 为 ACTIVE。`FLOW-SET-LC-STATE` 与 `FLOW-SET-AP-STATE-IMPLEMENTATION` 分别核验新状态、范围和不可改状态，最后由 ST-LC-0107 将实际改动的 CommandContext 成员赋回持久状态。成功计数/事件与拒绝计数/事件分支不同，NOT_USED/PERMOFF 不被普通 SetAPState 恢复。纸面初值为计数0，两条命令后 CmdCount=2、CmdErrCount=0；状态不是自行变成 ACTIVE。

### 3.2 收到监测数据：明确比较与提交，不执行 AP

教学报文值3300是自拟输入，不是实测遥测或新增飞行参数。其大端字节为 `0x0C 0xE4`，放在完整消息偏移184和185处，长度至少186，MID为上述符号，时间戳为输入 `T_msg`。

原要求 LC2003 / REQ-LC-0009 要求在应用 ACTIVE/PASSIVE 时收到相关消息即比较；LC2006 / REQ-LC-0016 要求先转本机字节序；LC2004 / REQ-LC-0014 要求保存结果和统计。它们在本轮对应 `FLOW-WP-MONITOR`：

| 操作 | 资源规则与真实数据连接 |
|---|---|
| ST-LC-0200–0206 | 取独立入口快照、应用门、消息时间、完整MID/hash WP链与有限循环条件；保留原链顺序 |
| ST-LC-0207–0215 | 原C偏移/类型算术门及风险分类；安全可推导路径才按BE/LE取数，拒绝/未知另分支 |
| ST-LC-0216–0219 | 掩码、CUSTOM选择、冻结stub或六关系/类型化比较；产生本次WP结果 |
| ST-LC-0220–0222 | 先提交四值WatchResult，再计算并提交EvaluationCount |
| ST-LC-0223–0230 | TRUE/FALSE/ERROR统计与跨越门分别计算，提交本WP统计/age候选，不覆盖前面的结果和次数 |
| ST-LC-0231–0235 | 游标前进、guard重算；所有关联WP可推导完成后整包计数只加一次并提交 |

实际语句中的一个确定片段如下；输入输出、公式名和赋值方向均来自本轮操作定义：

```text
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPRelationalCompare;
Set WPResultPersistent WComparedResult;
Compute WMonitorWorking WMonitorWorking ReqCapByFormTable FormulaTable.WPIncrementEvaluationCount;
Set WPEvaluationCountPersistent WNewEvaluationCount;
```

该片段处在正确门控分支中，不能脱离取数成功和活动算子条件单独调用。资源把 WPResultPersistent / WPEvaluationCountPersistent 分别绑定到当前索引的 WRT 字段；这些是项目别名，不是论文已确认的软件字段访问语法。

普通偏移184+宽度2未回绕且不超报文，转换/掩码得到3300，`3300 < 3319` 为 TRUE。实现视图推演为 WatchResult=TRUE、EvaluationCount=1、连续TRUE=1、累计TRUE=1、Countdown=0，整包 MonitoredMsgCount=1。旧结果 STALE→TRUE 被实现算入 FalseToTrueCount 和 LastFalseToTrue；正式 LC2004 字面只写 FALSE→TRUE，因此 ST-LC-0264–0266 的 documentary 统计视图不纳入 STALE，冲突继续登记，不把实现结果冒充正式统计完全一致。

监测出口只保存 WRT/AppData；ART101仍为 STALE/ACTIVE，APSampleCount和RTS计数仍0，不发RTS，不更新WP年龄。

### 3.3 三次独立采样：结果、连续计数与动作资格逐步相接

每次请求 StartIndex=EndIndex=101、UpdateAge非零、长度取实际构建的 `sizeof(LC_SampleAPCmd_t)`。三个请求之间没有新监测报文。原表age=0不进入正倒计数递减，因此三次都读取同一个 TRUE 结果；连续FAIL计的是 AP 求值次数，不要求三条独立遥测，也没有固定采样周期。

`FLOW-SAMPLE-IMPLEMENTATION` 对应 LC3001、LC3002.3、LC3006 等原要求：

| 操作 | 它独立表达的义务 |
|---|---|
| ST-LC-0300–0309 | 独立请求、应用门、ALL/有界闭区间、首项整范围门与各AP资格；非法/跳过路径不同 |
| ST-LC-0310–0311 | RPN之前计算并Set全局APSampleCount，合格AP恰一次 |
| ST-LC-0312–0324 | 有界RPN栈、逐token、四值AND/OR/XOR/NOT、EQUAL终止、非法诊断、最终结果映射和AP结果Set |
| ST-LC-0325–0337 | FAIL判断，连续/累计FAIL分别Compute/Set，转换和事件限额，使用新增后连续数判断阈值 |
| ST-LC-0338–0348 | 原AP ACTIVE/PASSIVE、AP转PASSIVE、应用RTS许可、请求描述/位置、请求计数和动作事件分别保留 |
| ST-LC-0349–0365 | 应用PASSIVE/AP PASSIVE抑制、事件限额及PASS/STALE/ERROR不同统计路径 |
| ST-LC-0366、0396、0367–0368 | AP游标前进及guard重算；范围处理返回后才ValidSampleCmd=true，再判断age交接 |

RPN `{113,EQUAL}` 把当前 WRT113 的 TRUE 压栈，EQUAL弹出并终止；它不是双目相等比较。最终 WP TRUE→AP FAIL，先由 ST-LC-0324提交ActionResult，再增加本AP连续/累计FAIL。

| 独立请求 | 连续/累计FAIL | AP前→后 | 动作结果（纸面推演） |
|---|---|---|---|
| 第一次 | 1/1 | ACTIVE→ACTIVE | 未达3，不请求RTS |
| 第二次 | 2/2 | ACTIVE→ACTIVE | 未达3，不请求RTS |
| 第三次 | 3/3 | ACTIVE→PASSIVE | 应用ACTIVE，形成一次RTS请求意图与动作事件 |

达到阈值时实现顺序为 ST-LC-0339先把AP置PASSIVE，ST-LC-0340才核定应用ACTIVE；允许分支 ST-LC-0341组请求、0342登记提交位置，之后0343–0346计算/Set两个请求尝试计数，再0347–0348动作事件，最后0335–0336事件计数。`LC_ExecuteRTS`返回void且原码忽略Transmit返回，不把这些计数解释为外部SC收到或RTS执行完成。

正式 LC3002.3.1 写“Once an RTS is initiated”后改变AP状态，与实现先变PASSIVE及被动应用仍变PASSIVE的顺序不同。documentary 与 code-derived 视图并列，不能改源代码语义来制造等价。

### 3.4 年龄在所有AP之后，不是新的触发入口

总成在 ST-LC-0368 的交接后内联 `FLOW-WP-AGE-CONTINUATION` 的 ST-LC-0253–0262。0253读同次请求的最新WRT/ValidSampleCmd/UpdateAge，0254门只允许有效请求且UpdateAge非零；0255–0256建立全表有限游标。每轮0257计算减一候选，0258确认旧值正，0259先Set倒计数，0260检测新值零，0261才Set STALE，0262推进并重算0256。

本例Countdown0不写STALE、结果保持TRUE。另一个通用边界输入若Countdown=1、WatchResult=TRUE，则本次AP仍使用TRUE；全部AP之后倒计数变0并置STALE，下一请求才读取STALE。这个1是纸面边界输入，不是WP113表参数。

合法范围但首AP NOT_USED/PERMOFF会拒绝整个AP区间；源码返回后ValidSampleCmd仍true，所以非零UpdateAge仍可能维护全部WP。长度错误、应用DISABLED或范围非法则不老化。这些路径不得归并成一个“采样失败全部不更新”的规则。

### 3.5 独立HK请求：读最新状态，形成可报告结果

`FLOW-HOUSEKEEPING` 的 ST-LC-0133从此时持久AppData/WRT/ART复制基础字段；0134–0136逐组压WP结果，0137–0140逐组压AP状态/结果并统计ACTIVE AP；0141将负载Set到HkPacket，0142–0143仅形成时间戳/发送意图。真实源码随后维护表/CDS，不能把维护计划或发送意图当服务已经成功。

上述正常例子纸面得到 APSampleCount=3、MonitoredMsgCount=1、RTSExecCount=1、PassiveRTSExecCount=0、AP101的累计RTS尝试1、计数口径内事件1；CmdCount/CmdErrCount=2/0，AP101为PASSIVE/FAIL，ActiveAPs=0。WP TRUE压为两位1，AP PASSIVE/FAIL压为半字节9；原STALE枚举255不能直接打入两位结果。包是否发出/被收到未有本轮运行证据。

## 4. 禁止、失败和未确定路径

| 路径 | 明确保留的处理；不能偷换成正常路径 |
|---|---|
| 应用PASSIVE、原AP ACTIVE、FAIL达阈值 | AP仍先PASSIVE；0340为false，0349–0351只增全局抑制数和DEBUG计划，无RTS请求/两个RTS计数，该DEBUG不增加ART累计事件 |
| 原AP PASSIVE、FAIL达阈值 | 0352–0354记录AP与全局抑制；0355仅限额内INFO，限额外仍计抑制，不发RTS |
| 未达连续FAIL阈值 | 不生成RTS/阈值动作事件；已发生的PASS↔FAIL转变事件不因此被取消 |
| AP PASS / STALE / ERROR | PASS和STALE由0362清连续FAIL；ERROR走0364保留连续FAIL并发错误计划，无RTS，不把ERROR当PASS；实现连续性差异独立登记 |
| 普通短包：offset184、width2、length185 | 原检查拒绝，0211事件位置→0212 ERROR→0213 age0，不取数/不计EvaluationCount；找到关联WP的整包仍计一次 |
| 浮点取数成功后NaN | 0219 ERROR及NaN事件；0220/0221/0222仍保存结果并计比较一次；0227只清age，保持连续TRUE和历史 |
| 浮点无穷 | 收到的WP值按原比较算子处理；WDT阈值的NaN/无穷则由0248排除，两者不同 |
| 默认custom | 0218产生Unexpected错误事件但返回FALSE；按FALSE统计，不改成ERROR，不宣称已有任务custom算法 |
| offset0xFFFFFFFF、width2、length186 | 明确32位无符号模型下和回绕成1，原检查可能放行；0209为不可推导读取，0210仅保留前缀，无猜测ERROR/比较/统计/成功出口。目标ABI未确认，审查停止不等于LC安全拒绝 |

极端值只是受控算术/纸面条件，不运行非法指针。希望所有不合法跨度都安全拒绝的要求与现有码差距另列；不能偷偷换成无限精度加法或安全相减来解释源代码。

## 5. 贯通样例之外的范围也有实际分解

WDT验证 `FLOW-WP-WDT-VALIDATION` 按0236–0252分别表达候选输入、NOT_USED、类型、算子、真实MID谓词观察、浮点阈值、每项分类、首错明细/返回、全表报告；它不验证offset。ADT验证另有逐项字段和RPN栈深流程，不能用比较业务RPN结果代替定义表校验。

命令组另有 NOOP、六HK计数复位、单项/ALL AP状态、永久关闭、AP/WP统计复位；保留命令复位与初始化/换表复位的不同保留字段。正常与拒绝计数、RESET通用接受要求冲突、单项/ALL与PERMOFF冲突分别登记。

生命周期组分别描述冷初始化、五对象完整恢复、默认回退、真实表可用性、定义表验证输入、状态提交和订阅交接；缺一恢复标志不能混合采用部分旧数据。订阅重建保留完整MID唯一订阅与WP关联链，以及订阅失败仍继续的源码行为。表更新续段清对应WRT/ART，CDS维护按WRT→ART→Saved标记→App顺序；保存失败关闭CDS，真实注册/恢复/保存返回值由接口观察输入，不编造成功。

这些操作均有原需求/代码定位和义务清单，但入口、软件服务或解释冲突未核定时仍是pending。82项库存齐全不等于82项full，也不等于完整系统可解析、已实施或已执行。

## 6. 本轮回归检查的层次

[tests/test_expansion.py](tests/test_expansion.py) 检查三组贡献的82项需求库存与义务引用、AST节点/boolean定义、循环guard末尾刷新、监测结果Set先于统计、允许/抑制路径的RTS节点、PASS/STALE/ERROR分支，以及总成AP后内联age。

路径检查只在指定boolean取值下对AST做一次结构展开；循环只展开一轮以核对顺序，不求值FormulaTable、不计算真实消息/RPN/计数，也不运行LC/cFS。因此即使测试通过，也仅说明这些静态结构断言通过。资源规则语义仍由源码纸面核对，真实算法执行、软件提交、目标ABI及官方解析器未因此升级为通过。

执行命令、时间、退出码和结果由本轮验证报告记录。旧合同模型/旧检查通过不能替代本轮完整转换验收，本文也不作为全量语义等价证明。
