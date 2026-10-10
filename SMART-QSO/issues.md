# SMART-QSO SpaceRDL 待确认问题清单

> 统一格式: 位置 / 证据 / 问题 / 影响 / 建议 / 阻塞级别 / 关联。
> 高阻塞 = 阻止对应语句进入最终 code.rdl 或必须先裁定；当前 code.rdl 中受影响的语句均已在 statements.md 标 `partial` 并回链 ISSUE。

## A. 协议与接口冲突（高阻塞优先）

### ISSUE-001 命令帧存在三套互不兼容的方案
- 位置: docs/operations/CMD_TLM_DATABASE.md:30-44 vs COMMAND_DICTIONARY.md:17-24 vs software/flight/src/input_validation.c:101-131
- 证据: 方案 A SYNC=0xEB90、单字节命令 ID、变长包；方案 B SYNC=0x55AA、16 位操作码、固定 32 字节帧、CRC-16-CCITT；代码方案 C 帧头 [0xAA][0x55]、单字节 ID、16 位累加和校验（非 CRC）。三套均为"CDR Baseline"状态。
- 问题: ProTC 的 ProTable.B2 无法确定唯一解析规则；代码校验方式（累加和）与两套文档（CRC-16）都不同。
- 影响: REQ-040/041/043、ST-024/025 语义悬空，上注/遥控验收无法进行。
- 建议: 由任务方裁定唯一命令帧标准（建议以 CDR 冻结的 COMMAND_DICTIONARY 为基并修正代码），其余版本标记作废。
- 阻塞级别: 高
- 关联: REQ-040,041,042,043,044; RES-015; ST-024,025

### ISSUE-002 遥测帧存在两套方案
- 位置: docs/operations/CMD_TLM_DATABASE.md:160-174 vs TELEMETRY_DICTIONARY.md:17-24
- 证据: 方案 A SYNC=0x1ACF 变长分类包（Housekeeping 1Hz/EPS 1Hz/ADCS 10Hz/RF 0.1Hz/Payload 0.1Hz/Event）；方案 B SYNC=0xAA55 固定 64 字节帧。同名参数编码不同（BATT_V 单位 mV vs V=raw/1000）。
- 问题: 下行遥测帧结构不唯一，地面解码器与星上组包无法对齐。
- 影响: REQ-052（SYS-303）与地面段验收。
- 建议: 裁定唯一遥测 ICD；代码 telemetry.c 的第三套二进制帧（sync 0x1ACFFC1D + CRC32）也应一并纳入裁定。
- 阻塞级别: 高
- 关联: REQ-052; RES-014

### ISSUE-003 上行链路存在性矛盾
- 位置: docs/pdr/SMART-QSO_PDR.md:73,126,234（"no uplink"、开放问题 5 "no uplink operations"）与 docs/hardware/RF_DESIGN.md:35-39（"beacon-only, No uplink command capability"）vs docs/ground/GROUND_STATION_OPERATIONS_MANUAL.md:116-118（435.XXX 上行指挥）、docs/environment/LINK_BUDGET_ANALYSIS.md:164-223（435.100MHz 上行预算）、CLAUDE.md（"Uplink: 435-438 MHz"）、MRD/任务规则中的遥控体系。
- 问题: PDR/RF 设计为"仅信标无上行"，但运营手册、链路预算、任务规则、ICD_SPACE_GROUND 均定义了上行指挥。
- 影响: ProTC（REQ-040）与整个遥控任务域存在性待定；"transponder" 与 "beacon-only" 定位也未裁决。
- 建议: 任务方确认最终任务形态（仅信标 vs 带上行），相应裁剪或保留 T7 域。
- 阻塞级别: 高
- 关联: REQ-040; RES-006

### ISSUE-004 OBC-EPS 物理层 UART vs I2C 矛盾
- 位置: docs/interfaces/INTERFACE_CONTROL_MASTER.md:137-143,147-153 vs ICD_OBC_EPS.md:51-56,62-74
- 证据: 主文档写 "OBC-EPS UART 3.3V Command/Response 4-pin header、9600bps Binary"；EPS ICD 全篇 I2C/PC-104（SCL/SDA H2-5/H2-6、100-400kHz）；验证计划与代码 HAL（I2C_ADDR_EPS_CONTROLLER 0x48）支持 I2C。
- 问题: 物理层与连接器不一致（另有验证计划 DF13-6P 第三方案）。
- 影响: REQ-004/013（Init I2C1、GetData eps）传输介质待定。
- 建议: 更新主文档与验证计划至 I2C 方案（或明确 UART 方案并重写 EPS ICD）。
- 阻塞级别: 高
- 关联: REQ-004,013; RES-002; ST-002,006

### ISSUE-005 I2C 地址矛盾
- 位置: ICD_OBC_EPS.md:76（EPS 0x48）vs INTERFACE_VERIFICATION_PLAN.md:55（0x50）；ICD_OBC_ADCS.md:96（LSM6DS3 0x6A）vs INTERFACE_VERIFICATION_PLAN.md:143（0x68）
- 问题: 地址不唯一会导致寻址冲突（0x48 同时出现在 EPS 总线与 ADCS 温度传感器定义中，跨总线冲突未说明）。
- 影响: Init 配置与 GetData 寻址。
- 建议: 以单 ICD 为权威修订验证计划；明确 0x48 在各总线上的复用规则。
- 阻塞级别: 中
- 关联: REQ-013,027; RES-002,004

### ISSUE-006 信标调制 AFSK 1200 vs GFSK 9600 矛盾
- 位置: ICD_BEACON_FORMAT.md:216-223（AFSK 1200、mark 1200Hz/space 2200Hz、50 前导）vs ICD_OBC_RF.md:156-160,219-222（GFSK 9600、偏差 3.5kHz 为主）vs ICD_SPACE_GROUND.md:63-72（GFSK 9600 主、AFSK 1200 降级）vs INTERFACE_CONTROL_MASTER.md:152-153（1200bps AX.25/AFSK）
- 问题: 主调制方式未裁决；SYS-202 只要求"支持 AFSK 1200"。
- 影响: ProTable.B1 射频层参数；地面站 TNC 配置（GSOM 按 1200bps AFSK）。
- 建议: 明确主/备调制及切换条件；同步地面站配置。
- 阻塞级别: 高
- 关联: REQ-037,038; RES-003,014; ST-020,026

### ISSUE-007 下行频率与频段矛盾
- 位置: SYSTEM_REQUIREMENTS.md:131 与 LINK_BUDGET_ANALYSIS.md:29（145.825 MHz）vs PDR.md:33,73（145.8-146.0 MHz 待 IARU）vs TELEMETRY_DICTIONARY.md:184（145.XXX 占位）vs ARCHITECTURE.md:136（另提 437.425 MHz 备用）
- 问题: 频率未冻结（两处 TBD-001 均指向 IARU 协调结果）。
- 影响: 射频配置与地面站守听频率。
- 建议: 等待 IARU 协调后回填；当前不写入确定值。
- 阻塞级别: 中（TBD 已登记，不影响语句结构）
- 关联: REQ-038; RES-003

### ISSUE-008 信标间隔多方矛盾
- 位置: 代码 beacon.h:39-45（ACTIVE 30s/IDLE 60s/SAFE 180s）vs system_state.c:413-423（可配置 10-120s）vs ICD_BEACON_FORMAT.md:241-245（60/30/30s）vs ICD_SPACE_GROUND.md:242-247（120/90/60s，食期 120s）vs BEACON_SPEC.md:11,61-66（自适应 15-180s、默认 60s，SAFE 或 SOC<20% 180s）vs MISSION_OPERATIONS_PLAN.md:148-152（120/60/30s）vs COMMAND_DICTIONARY.md:132（SET_BEACON_RATE 30-300s）
- 问题: 默认值与按模式值共 6 套表述；可配置范围 10-120s 与 30-300s 冲突。
- 影响: REQ-033 的 At(0,60000ms) 周期与 SET_BEACON_RATE 参数范围验收。
- 建议: 以 MRD-020"至少每 60s"为下限基线，裁定默认 60s 与各模式档位，统一 SET_BEACON_RATE 范围。
- 阻塞级别: 高
- 关联: REQ-033; ST-020,025

### ISSUE-009 信标信息字段格式三套并存
- 位置: ICD_BEACON_FORMAT.md:93-153（16B ASCII 头 + 64B key=value 遥测 + `|` + 文本）vs ICD_SPACE_GROUND.md:136-163（0x01 + 序号 + Unix 时间 + 定长二进制表）vs beacon.c:200-211（`de %s: %s | T=... M=... SOC=... BV=...` 单一 ASCII 行）
- 问题: 星载实际格式（代码）与两份 ICD 均不一致。
- 影响: 地面解码器开发与验收；ProTable.B1 载荷布局。
- 建议: 以代码实现为基准修订 ICD，或明确代码为占位实现。
- 阻塞级别: 高
- 关联: REQ-034,036; RES-014; ST-020

### ISSUE-010 呼号不一致
- 位置: GSOM:462（SQSO-1）vs PDR.md:107/ML_MODELS.md:20（SMARTQ-1 示例）vs ICD_SPACE_GROUND.md:117（SQSO）vs ICD_BEACON_FORMAT.md:66（KK6XXX 示例、须协调）vs COMMAND_DICTIONARY.md:479（N0CALL 占位）；代码 beacon.h:36 = "SQSO-1"
- 问题: 最终呼号未协调确定（多处标注 TBD）。
- 影响: REQ-035 与信标源地址。
- 建议: 取得 IARU/执照呼号后统一回填。
- 阻塞级别: 中
- 关联: REQ-035

### ISSUE-011 电池拓扑/电压/容量三套参数
- 位置: ARCHITECTURE.md:92-94（4S 50Wh 13.5Ah 12.0-14.8V）vs EPS_DESIGN.md:188-194（4S1P 3.5Ah 50.4Wh 14.4V 12.0-16.8V）vs POWER_BUDGET_ANALYSIS.md:29-37（2S2P 5.2Ah 7.4V 38.5Wh）；RF_DESIGN.md:338 与 ICD_BEACON_FORMAT.md:407 的 BV 6.0-8.4V 仅与 2S 吻合；EXECUTIVE_SUMMARY.md:26 又写 7Wh
- 问题: 电池组拓扑未冻结，遥测量程（BV 6.0-8.4V vs 12.0-16.8V）随之悬空。
- 影响: REQ-013 遥测解码量程、EOL 放电策略。
- 建议: 由 EPS 负责人裁决电池组构型并统一所有量程引用。
- 阻塞级别: 高
- 关联: REQ-013,053; RES-002

## B. 阈值/参数冲突

### ISSUE-012 SOC 阈值多套并存
- 位置: 代码 eps_control.h:41-47/main.c:211-224（SAFE<25%、IDLE<40%、载荷需>55%、ACTIVE>55%+阳照）vs MISSION_RULES.md:86-94（SOC<30% 减操作禁 AI、<20% 转 SAFE、<15% 绝对下限）vs TELEMETRY_DICTIONARY.md:190-196（RED<15/YEL<25）vs AUTONOMY_DESIGN.md:58-67（<20% SAFE、<30% IDLE、>80%+5min ACTIVE、食期<50% IDLE）vs ML_MODELS.md:35-37（≥60% 3B、40-60% 1B、<40% 模板）vs EPS_DESIGN.md:278-282（SAFE<25/IDLE 25-55/ACTIVE>55）
- 问题: 同一个"转 SAFE"存在 20% 与 25% 两个版本；载荷使能 55% 与 AI 分档 60% 不一致。
- 影响: REQ-014/015/016/021 的判定阈值验收。
- 建议: 裁决单一阈值表（代码 25/40/55 与 EPS_DESIGN 一致，可作为基准），更新 MISSION_RULES 与 AUTONOMY_DESIGN。
- 阻塞级别: 高
- 关联: REQ-014,015,016,021,059; ST-008,010

### ISSUE-013 看门狗超时 5s vs 30s
- 位置: MISSION_RULES.md:128-131（"Watchdog timeout: 5 seconds"）与 EXECUTIVE_SUMMARY.md:109（5s）vs OBC_DESIGN.md:331-335（IWDG 30s）、watchdog_mgr.h:44 / hal_wdt.h:28 / smart_qso.h:64（30000ms）、FDIR_DESIGN.md:345-370（软 10s/硬 30s 双层）、TIMING_ANALYSIS.md:42（30s）；system_init.h:42（5000ms）
- 问题: 硬件超时与任务规则直接矛盾（5 倍差距）。
- 影响: REQ-005/048 验收；看门狗若按 30s 配置将违反任务规则 FC-005。
- 建议: 裁决硬件超时值（若 5s，需评估 20ms 主循环喂狗余量）。
- 阻塞级别: 高
- 关联: REQ-005,048; RES-007; ST-003,029

### ISSUE-014 热阈值多套并存
- 位置: 代码 main.c:271（>40°C 告警）、sensors.c:126-133（>45°C/<-10°C）、system_state.c:312-313（>60°C/<-20°C）vs FDIR_DESIGN.md:74-87（OBC -30/70°C、Jetson -20/70°C、电池 -10/45°C）vs MISSION_RULES.md:99-104（电池 -10~+45、OBC -40~+85、Jetson -20~+70、PA -20~+60）vs GSOM:271-275（OBC -40/+85、BAT -10/+45、JET -20/+70）vs PAYLOAD_DESIGN.md:437（70°C 急停）vs ML_MODELS.md:35（55°C 限 AI）
- 问题: 同一组件告警阈值相差可达 45°C。
- 影响: REQ-045 检测条件、REQ-064 约束验收。
- 建议: 以 MISSION_RULES FC-002 为约束基线，统一软件告警阈值表。
- 阻塞级别: 高
- 关联: REQ-045,064; ST-016

### ISSUE-015 主循环周期与采样率冲突
- 位置: 代码 main.c:40（20ms 节拍）vs RTOS_ARCHITECTURE.md:100 与 TIMING_ANALYSIS.md:62（Main Loop 100ms）vs ICD_ADCS/EPS（控制环 1000ms）；TIMING_ANALYSIS.md:44（传感器 10Hz）vs sensors.yaml（1000/2000ms 即 1/0.5Hz）
- 问题: 控制器 ControlPeriod 依据不唯一（code.rdl 取 1000ms，依据 ICD 一致证据）。
- 影响: 全部 At(t,period) 时间约束与 CPU 利用率估算。
- 建议: 明确 FreeRTOS 迁移后的任务周期表（与 ISSUE-024 一并裁决）。
- 阻塞级别: 中
- 关联: REQ-001,013; RES-001

### ISSUE-016 AI 占空比 10% vs 20% vs 30% vs 36%
- 位置: MISSION_RULES.md:107-113（≤10%、单次≤60s、间隔≥540s）vs EPS_DESIGN.md:169（20%）vs PAYLOAD_DESIGN.md:65,196-197（20% 门限/30% 目标）vs POWER_BUDGET_ANALYSIS.md:226-236（36% 最大、保守 10%）
- 问题: 硬性规则（10%）与设计目标（20-30%）混用。
- 影响: REQ-060 约束验收。
- 建议: 以任务规则 10% 为硬约束，其余作为设计裕度说明。
- 阻塞级别: 中
- 关联: REQ-060

### ISSUE-017 信标文本长度 120/150/175/200/256 并存
- 位置: PDR.md:106,110 与 BEACON_SPEC.md:30（文本 ≤120B）vs TELEMETRY_DICTIONARY.md:174（AI 消息 ≤150 字符）vs ICD_BEACON_FORMAT.md:140（文本 0-175B）vs beacon.c:442-464 与 beacon.h:30（BEACON_MAX_TEXT_LEN 200B）vs beacon.h:52/ICD（Info ≤256B）；PAYLOAD_DESIGN.md:251-254（输出 20-200 字符）
- 问题: 文本上限不唯一，AI 提示词（120B）与代码校验（200B）不一致。
- 影响: REQ-024 验收。
- 建议: 以 120B（LLM 提示词与 BEACON_SPEC 一致）为信标文本上限，Info 字段 ≤256B 不变。
- 阻塞级别: 中
- 关联: REQ-024; RES-013,014

### ISSUE-018 detumble 时限 7 天 vs 1 轨道 vs 90 分钟
- 位置: MRD-060/SYS-420（<5°/s、7 天内）vs PDR.md:37（detumble ≤1 orbit）vs ADCS_DESIGN.md:47-64（≤10°/s 一轨内；代码 adcs_control.h:45 超时 5400s=90min）vs LAUNCH_SITE_OPS.md:244（T+90min）
- 问题: 收敛时限与速率阈值（5°/s vs 10°/s vs 0.5°/s）多套。
- 影响: REQ-028/029 验收判据。
- 建议: 裁定速率阈值与时限（MRD 为 7 天上限，设计目标 1 轨，二者可并存但需写明层级）。
- 阻塞级别: 中
- 关联: REQ-028,029

### ISSUE-019 质量/寿命/发电预算冲突
- 位置: SYS-002 ≤2.0kg vs PDR.md:32 ≤1.80kg vs EXECUTIVE_SUMMARY.md:25 1.2kg vs ARCHITECTURE.md:57 ≤1.33kg；MRD-001/SYS-010 12 个月 vs PDR 12-18 个月 vs ES 2 年；SYS-100 ≥2W 轨道平均 vs PDR 3.5-5W vs EPS_DESIGN 5.0W vs POWER_BUDGET 6.2W
- 问题: 预算基线多版本并存。
- 影响: 物理类需求（非 SpaceRDL 语句），影响功率约束上下文。
- 建议: 以 CDR 基线（ES 为 CDR Baseline）统一，或明确各文档修订状态。
- 阻塞级别: 低
- 关联: REQ-063

### ISSUE-020 OBC 主备、RAM、FRAM、Jetson 规格冲突
- 位置: OBC_DESIGN.md:136-164（主 STM32L476RG、备 Apollo4 Blue Plus）vs ARCHITECTURE.md:175-186（主 Apollo4、次 STM32L4）vs RTOS_ARCHITECTURE.md:42-44（目标 STM32L4R5）与 system_init.c:511-518（TARGET_STM32L4 宏）；FRAM FM25V10 128KB（OBC_DESIGN.md:183）vs 4MB（ARCHITECTURE.md:198）；Jetson 6 核 1.5GHz/67TOPS（PAYLOAD_DESIGN.md:138-148）vs 8 核 2.0GHz/20TOPS（ARCHITECTURE.md:152-156）
- 问题: code.rdl 的 `Executed Within 128kb` 与 CtrOBC 硬件基线随之悬空。
- 影响: REQ-061、SystemConstraints。
- 建议: 由 OBC/载荷负责人裁决主备与规格，统一架构文档。
- 阻塞级别: 中
- 关联: REQ-061; RES-001,009; ST-031

### ISSUE-021 RTM 编号体系与正式需求文档不匹配
- 位置: docs/requirements/REQUIREMENTS_TRACEABILITY.md:69-103 vs SYSTEM_REQUIREMENTS.md
- 证据: RTM 中 SYS-020=功率模式管理、SYS-040=Jetson 通信、SYS-060=故障检测；正式文档 SYS-020=单点故障、SYS-040 不存在（AI 载荷为 SYS-500+）。RTM 引用的 SRS-Fxxx 亦无独立 SRS 文档。
- 问题: 两层需求编号无法互查，追溯链断裂。
- 影响: 全部追踪与验证活动；本目录已按正式 SYS/MRD 编号为准并标注。
- 建议: 重建 RTM 编号映射表或修订其中 SYS/SRS 引用。
- 阻塞级别: 高
- 关联: 全部 REQ 的父需求引用

### ISSUE-022 状态机三套定义
- 位置: 代码 state_machine.h:41-49（BOOT/SAFE/DETUMBLE/IDLE/ACTIVE/EMERGENCY）vs AUTONOMY_DESIGN.md:121-166（LAUNCH/LEOP/COMMISSIONING/NOMINAL/SAFE/RECOVERY）vs TELEMETRY_DICTIONARY.md:88-96（INIT/SAFE/IDLE/ACTIVE/FAULT）
- 问题: 命令允许矩阵（cmd_handler.c 按 BOOT/SAFE/IDLE/ACTIVE/EMERGENCY）与遥测枚举不一致。
- 影响: REQ-042 状态允许矩阵、地面显示。
- 建议: 统一为遥测枚举 + 内部扩展态（如 DETUMBLE 映射 IDLE），并更新 AUTONOMY_DESIGN。
- 阻塞级别: 中
- 关联: REQ-042; ST-025

### ISSUE-023 RF_EN 常开与 SAFE 关 radio 矛盾
- 位置: ICD_OBC_EPS.md:250-258（"RF_EN always enabled in all modes"）vs eps_control.c:178-207（SAFE 模式 radio off、beacon on）
- 问题: SAFE 下 RF 供电策略不唯一；且代码中 SAFE=beacon on 但 radio off 自相矛盾（发信标需 RF）。
- 影响: REQ-017 的 LoadSwitchSafe 数据值。
- 建议: 明确 SAFE 模式信标供电策略（收发信标需 RF 供电），修正代码或 ICD。
- 阻塞级别: 中
- 关联: REQ-017; RES-002; ST-009

## C. 代码与文档不符 / 实现缺口

### ISSUE-024 FreeRTOS 架构文档与实现不符
- 位置: docs/RTOS_ARCHITECTURE.md:48-105 vs software/flight/src（无任何 FreeRTOS 调用）；docs/INCLUDE_DEPENDENCIES.md:93 引用的 hal_freertos.c 不存在
- 证据: 9 任务/优先级/周期的文档架构 vs main.c 单线程 20ms 循环；scheduler.c 协作式调度器未被调用。
- 问题: 架构基线（FreeRTOS 多任务）与代码基线（单循环）脱节。
- 影响: 全部任务周期与并发语义（SpaceRDL 任务块按文档架构建模）。
- 建议: 明确实现路线（迁移 FreeRTOS 或废弃文档架构），冻结后再复核语句周期。
- 阻塞级别: 高
- 关联: REQ-001; RES-001; 全部 At() 约束

### ISSUE-025 十个模块编译但未接入主循环
- 位置: software/flight/CMakeLists.txt:103-125 vs main.c（无调用点）
- 证据: beacon/deployment/adcs_control/telemetry/cmd_handler/scheduler/watchdog_mgr/state_machine/system_init 全部编译进固件但 main.c 从未调用（agent 全量 grep 证实）。
- 问题: 代码证据只能证明"模块存在"，不能证明"行为发生"；本目录对这类语句标 partial 且置信度降级。
- 影响: REQ-002,008-012,023,033-039,040-043,048 的代码级验证。
- 建议: 完成模块集成（或提供集成分支），补充集成测试后再升级置信度。
- 阻塞级别: 高
- 关联: REQ-002,008-012,023,033-039,040-043,048; ST-021,027

### ISSUE-026 飞行路径时间源未实现
- 位置: software/flight/src/time_utils.c:27-31（FLIGHT_BUILD 下 `TODO: return 0`）
- 问题: MET/UTC 维护（SYS-301、TIME_MANAGEMENT.md 的完整设计）在飞行构建中无实现。
- 影响: REQ-065 未覆盖；lastContactAge（REQ-054）与信标时间戳依赖此。
- 建议: 实现 HAL 时间源（RTC/32.768kHz）与 MET 维护。
- 阻塞级别: 中
- 关联: REQ-054,065

### ISSUE-027 硬件读写路径未实现
- 位置: adcs_control.c:336-356,474-506（`TODO: Read from actual I2C magnetometer`、`TODO: Apply via HAL GPIO/PWM`）；eps_control.c（无 I2C 访问，仅内存状态）；sensors.c 全仿真
- 问题: 设备交互在仿真模式下为合成值，真实硬件路径缺失。
- 影响: REQ-013,027,031 的飞行行为未验证。
- 建议: 实现 HAL 层真实驱动（HAL 头文件已备：hal_i2c/hal_gpio/hal_pwm）。
- 阻塞级别: 中
- 关联: REQ-013,027,031,032; ST-006,007,014

### ISSUE-028 Jetson 文本接收/重启路径缺失
- 位置: uart_comm.c uart_receive() 无调用点；无 BEACON_REQ/BEACON_RSP 会话代码；无"3 次失败断电重启"实现（仅 ICD_OBC_JETSON.md:253-265 与 AUTONOMY_DESIGN.md:229-235 设计描述）
- 问题: REQ-023/026 仅有设计与数据流证据。
- 影响: ST-021（GetData jetson BeaconText）置信度受限；REQ-026 未覆盖。
- 建议: 实现 BEACON_REQ/RSP 会话、10s 超时与失败计数/断电重启状态机。
- 阻塞级别: 中
- 关联: REQ-023,026; ST-021

### ISSUE-029 RBF（发射前移除插销）机制缺失
- 位置: SYS-005 要求 RBF；全仓库 grep 无 RBF/Remove Before 匹配
- 问题: 安全需求无对应实现/设计。
- 影响: SYS-005 验证。
- 建议: 补充 RBF 设计（硬件或部署开关等效机制并书面论证）。
- 阻塞级别: 中
- 关联: SYS-005（范围外 REQ，未纳入本目录 66 条）

### ISSUE-030 上行调制/速率未定义
- 位置: docs/operations/ 8 份文件中无上行速率/调制；ICD_SPACE_GROUND.md:76-83 仅给 GFSK 9600 与 EIRP，未给帧级调制细节
- 问题: ProTable.B2 射频层不完整。
- 影响: 上行链路验收。
- 建议: 在 ICD_SPACE_GROUND 中补充上行调制/编码/前导。
- 阻塞级别: 中
- 关联: REQ-040; RES-015

### ISSUE-031 QSO 公平性/优先级无公式与模型规格
- 位置: MRD-043 与 PDR.md:27（Gini ≤0.35/60 天）vs ARCHITECTURE.md:242（仅 "Tiny CNN (~1MB)" 一句）vs ML_MODELS.md（无 QSO 模型）
- 问题: 需求存在、量化指标存在，但打分公式、模型 I/O、执行位置均无。
- 影响: REQ-056 未覆盖（不生成猜测性 Compute）。
- 建议: 提供 QSO 优先级模型的输入/输出/算法规格或明确降级为地面评估。
- 阻塞级别: 中
- 关联: REQ-056

### ISSUE-032 区域需求预测模型缺失
- 位置: MRD-042 要求"预测区域需求"；ML_MODELS.md/代码均无对应模型
- 问题: 需求无实现载体。
- 影响: REQ-057 未覆盖。
- 建议: 明确该能力由哪个代理/模型承担及 I/O 规格，或调整需求。
- 阻塞级别: 中
- 关联: REQ-057

### ISSUE-033 功率预测模型 I/O 与周期未定义
- 位置: ML_MODELS.md:3（"Power Forecast (LSTM-style, INT8, <100 kB)" 一行）与 PDR.md:96-97（"90-min ahead energy forecast"）；无输入特征、输出维度、运行周期、运行硬件说明
- 问题: ST-015 的输入 {InsolationHistory, Soc} 与输出 EnergyForecast90min 为 PDR 语义推导（中置信度），非规格。
- 影响: FormulaTable.B3 无法实现验收。
- 建议: 补充模型规格表（特征、窗口、输出、周期、TFLM 运行位置）。
- 阻塞级别: 中
- 关联: REQ-055; RES-012; ST-015

### ISSUE-034 联邦学习与"无上行更新"直接矛盾
- 位置: CLAUDE.md 设计原则（"Federated learning: Community can submit bounded, rate-limited model updates via public uplink"）与 PDR.md:27（"accept... at least one model/parameter update per quarter"）vs PDR.md:114-115（"No uplink updates... models are fixed at launch"）与 PDR.md:234（开放问题 5 "no uplink operations"）
- 问题: 同一份 PDR 内 2.1 节与 5.3 节矛盾。
- 影响: REQ-058 冲突态；影响上行链路定位（与 ISSUE-003 联动）。
- 建议: 裁决是否保留在轨模型更新；若保留需定义更新帧、验证、回滚与限速。
- 阻塞级别: 高
- 关联: REQ-058

### ISSUE-035 存储容量 1MB 要求 vs 128KB FRAM
- 位置: SYS-310（≥1MB 任务数据）vs OBC_DESIGN.md:180-183（FM25V10 128KB；另有 W25Q128 16MB SPI flash 未在软件中建模）
- 问题: 需求与当前硬件选型不符（除非计入 16MB SPI flash）。
- 影响: REQ-051 验收；故障日志/任务数据存放介质待定。
- 建议: 明确数据分级存储（FRAM=关键状态、Flash=大容量日志）并更新 SYS-310 实现依据。
- 阻塞级别: 中
- 关联: REQ-051

### ISSUE-036 任务级看门狗未接入
- 位置: watchdog_mgr.c:86-111（miss≥3 判 stalled）与 wdt_mgr_kick 均无 main.c 调用点
- 问题: 任务心跳/停滞检测无执行路径。
- 影响: REQ-049 未覆盖。
- 建议: 接入 scheduler 或主循环任务心跳注册。
- 阻塞级别: 中
- 关联: REQ-049

### ISSUE-037 展开重试/验证逻辑未纳入语句
- 位置: deployment.h:42-48（重试 3 次、延时 60s、验证超时 10s）与 deployment.c:161-174；code.rdl ST-027 仅建模名义序列
- 问题: 组合语义（失败→延时→重试→FAILED）无对应 SpaceRDL 结构；Over(T,nc,3) 语义不完全匹配重试循环。
- 影响: REQ-011/012 未覆盖；REQ-029 的 300s settling 同理。
- 建议: 确认方言是否支持重试组合（While+计数），或升级为专用组合算子后再补。
- 阻塞级别: 低
- 关联: REQ-011,012,029

### ISSUE-038 仿真行为与注释不符（部署 5s vs 100ms 周期）
- 位置: deployment.c:362-366（"Simulate separation after 5 seconds" 依赖 100ms 调用周期，但 main.c 未调用）
- 问题: 仿真语义依赖未验证的调用假设。
- 影响: 低（仿真环境）。
- 建议: 与 ISSUE-025 一并解决。
- 阻塞级别: 低
- 关联: REQ-008

### ISSUE-039 EPS UART 命令集缺失（若裁定 UART 方案）
- 位置: SYS-320 允许 UART 或 I2C；若按 INTERFACE_CONTROL_MASTER 的 UART 9600 方案，EPS UART 命令集不存在
- 问题: 与 ISSUE-004 联动。
- 影响: REQ-013 实现选型。
- 建议: 随 ISSUE-004 裁定。
- 阻塞级别: 低
- 关联: REQ-013

### ISSUE-040 功率模式表与 BURST 模式缺失
- 位置: SYSTEM_REQUIREMENTS.md:49-54（SAFE<1W/IDLE<2W/ACTIVE<4W/BURST<10W）vs POWER_BUDGET_ANALYSIS.md:89-108（SAFE 100mW/IDLE 200mW/ACTIVE 500mW/AI burst 10W）vs PDR.md:155-160（Idle 0.3W/Active ~4.0W/Learning ~1.0W）
- 问题: 模式定义与功耗数值三套；BURST 模式在除 SYS 外的文档中不存在（"AI burst"为 ACTIVITY 非模式）。
- 影响: 功率预算验收与 REQ-060 上下文。
- 建议: 统一模式集（建议 SAFE/IDLE/ACTIVE+AI burst 活动）与功耗表。
- 阻塞级别: 低
- 关联: REQ-060,064
