# SMART-QSO 需求 → SpaceRDL 语句映射

> 每个原子操作只对应一个算子和一件可观察的事。`SpaceRDL 语句`列与 `code.rdl` 逐字一致。
> GetData/SendData/ProTC/ProTM 的协议细节（取数指令、等待、校验、重发）属于资源能力，在软件映射文档中展开，不反向拆成新原子语句。

| # | Statement ID | REQ-ID | 任务 | 来源/证据 | 类型 | 句型 | SpaceRDL 语句 | 时间约束 | 置信度 | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ST-001 | REQ-001 | 初始化 | main.c:95-171; SYS-300 | Composite | 顺序组合 | `Composite InitSequence Finished Within 30000ms { ... }` | Finished Within 30s | 高 | verified |
| 2 | ST-002 | REQ-004 | 初始化 | OBC_DESIGN.md:73-79; SYS-320-324 | Init | 初始化端口 | `Init I2C1 EpsI2CConfig; Init I2C2 AdcsI2CConfig; Init SPI1 RfSpiConfig; Init UART1 JetsonUartConfig;` | - | 高 | verified |
| 3 | ST-003 | REQ-005 | 初始化 | watchdog_mgr.h:44; SYS-021 | Init | 初始化定时器 | `Init WDT1 WatchdogConfig;` | - | 中 | partial(ISSUE-013) |
| 4 | ST-004 | REQ-003 | 初始化 | mission_data.c:78; SRS-F002 | GetData | 从设备采集 | `GetData fram MissionConfigData;` | - | 高 | verified |
| 5 | ST-005 | REQ-006,007 | 初始化 | COMMISSIONING_PLAN.md:50-58; system_state.c:56-69 | Set | 变量赋值 | `Set powerMode SAFE; Set s_rfInhibit true; Set beaconInterval 60000; Set s_aiEnabled false;` | - | 高 | verified |
| 6 | ST-006 | REQ-013 | 功率管理 | ICD_OBC_EPS.md:139-156,275-295; sensors.c:68-137 | GetData | 从设备采集 | `GetData eps {BatteryVoltage, BatteryCurrent, BatteryTemp, Soc, SolarVoltage, SolarCurrent, BusVoltage};` | 每周期(1s) | 高 | verified |
| 7 | ST-007 | REQ-027 | 姿态控制 | ICD_OBC_ADCS.md:124-171; adcs_control.c:336-382 | GetData | 从设备采集 | `GetData adcs {MagField[3], GyroRate[3], SunVector[3]};` | 每周期(1s) | 中 | verified |
| 8 | ST-008 | REQ-014,015,016 | 功率管理 | eps_control.h:41-47; main.c:211-224 | If/Else+Set | 条件赋值 | `If (Soc < 0.25) { Set powerMode SAFE; } Else { If (Soc < 0.40) { Set powerMode IDLE; } Else { If (Soc > 0.55 && sunlit) { Set powerMode ACTIVE; } } }` | 每周期 | 高 | partial(ISSUE-012) |
| 9 | ST-009 | REQ-017 | 功率管理 | eps_control.c:178-207; ICD_OBC_EPS.md:180-186 | Switch+SendData | 按模式发控制 | `Switch (powerMode) { Case(SAFE): { SendData eps LoadSwitchSafe; } Case(IDLE): { SendData eps LoadSwitchIdle; } Case(ACTIVE): { SendData eps LoadSwitchActive; } }` | 模式变化后 | 高 | partial(ISSUE-023) |
| 10 | ST-010 | REQ-020,021 | 载荷管理 | eps_control.c:86-117; ICD_OBC_JETSON.md:89-100 | If/Else+SendData | 条件发控制 | `If (powerMode == ACTIVE && Soc > 0.55) { SendData jetson PowerEnableCmd; } Else { SendData jetson PowerDisableCmd; }` | 每周期 | 高 | verified |
| 11 | ST-011 | REQ-028 | 姿态控制 | adcs_control.c:401-423; ADCS_DESIGN.md:212-219 | Compute | 公式变换 | `Compute BDotControl {MtqDipole[3]} {MagField[3], MagFieldPrev[3]} ReqCapByTable FormulaTable.B1;` | 每周期 | 高 | verified |
| 12 | ST-012 | REQ-030 | 姿态控制 | adcs_control.c:425-472; ADCS_DESIGN.md:249-265 | Compute | 公式变换 | `Compute SunPointControl {MtqDipole[3]} {SunVector[3], MagField[3]} ReqCapByTable FormulaTable.B2;` | 每周期 | 高 | verified |
| 13 | ST-013 | REQ-029,030 | 姿态控制 | adcs_control.h:39-45; adcs_control.c:156-214 | If+Set | 条件赋值 | `If (rateMag < 0.0087) { Set adcsMode SUNPOINT; } If (adcsMode == SUNPOINT && !sunlit) { Set adcsMode ECLIPSE; } If (adcsMode == ECLIPSE && sunlit) { Set adcsMode SUNPOINT; }` | 每周期 | 中 | partial(ISSUE-037) |
| 14 | ST-014 | REQ-031 | 姿态控制 | ICD_OBC_ADCS.md:177-189; adcs_control.c:474-506 | SendData | 向设备发数据 | `SendData adcs MtqPwm[3];` | 每周期 | 中 | partial(ISSUE-027) |
| 15 | ST-015 | REQ-055 | AI | PDR.md:96-97; ML_MODELS.md:3 | Compute | 算法变换 | `Compute PowerForecast {EnergyForecast90min} {InsolationHistory, Soc} ReqCapByTable FormulaTable.B3;` | 周期未定 | 中 | partial(ISSUE-033) |
| 16 | ST-016 | REQ-045,047,050 | 故障管理 | main.c:43,271,280; fault_mgmt.c:156,208-233 | Composite | 条件组合 | `At(0, 10000ms) Composite HealthCheck { If (epsTemp > 40.0) { Set faultFlag THERMAL; SendData jetson PowerDisableCmd; Set powerMode IDLE; SendData fram FaultLogEntry; } If (Soc < 0.30) { Set faultFlag POWER; SendData fram FaultLogEntry; } If (criticalFault) { Set powerMode SAFE; } }` | At(0,10s) | 高 | partial(ISSUE-014) |
| 17 | ST-017 | REQ-046 | 故障管理 | fault_mgmt.c:75-80,164-195; smart_qso.h:61 | SendData | 向设备发数据 | `SendData fram FaultLogEntry;`（健康检查内、故障条件分支中） | 故障发生时 | 高 | verified |
| 18 | ST-018 | REQ-019,051 | 数据管理 | main.c:46(100 tick×20ms); mission_data.c:56-89 | SendData | 向设备发数据 | `At(0, 2000ms) SendData fram MissionStateData;` | At(0,2s) | 高 | verified |
| 19 | ST-019 | REQ-022 | 载荷管理 | main.c:67,304-379; ICD_OBC_JETSON.md:121 | SendData | 向设备发数据 | `At(0, 60000ms) SendData jetson TelemetryCsv;` | At(0,60s) | 高 | verified |
| 20 | ST-020 | REQ-033,034,036,038,039,066 | 信标 | beacon.c:131-156,220-264; ICD_BEACON_FORMAT.md:39-45; SRS-P002 | Composite+ProTM | 周期组合+打包发送 | `At(0, 60000ms) Composite BeaconCycle Finished Within 5000ms { If (s_aiEnabled && powerMode != SAFE) { GetData jetson BeaconText Finished Within 10000ms; } If (!beaconTextValid) { Set beaconText TemplateText; } If (!s_rfInhibit) { ProTM ground BeaconFrame ReqCapByTable ProTable.B1; } }` | At(0,60s)、Finished Within 5s | 高 | partial(ISSUE-008/009) |
| 21 | ST-021 | REQ-023,024,066 | 载荷管理 | ICD_OBC_JETSON.md:160-171,222-228; SYS-512 | GetData | 从设备采集 | `GetData jetson BeaconText Finished Within 10000ms;`（s_aiEnabled && powerMode!=SAFE 分支内） | Finished Within 10s | 高 | partial(ISSUE-028) |
| 22 | ST-022 | REQ-025,039 | 信标 | beacon.c:131-156; SYS-520/521 | If+Set | 条件赋值 | `If (!beaconTextValid) { Set beaconText TemplateText; }` | 信标周期内 | 高 | verified |
| 23 | ST-023 | REQ-007 | 初始化/部署 | SRS-S001; deployment.h:33 | If | 条件发射 | `If (!s_rfInhibit) { ProTM ground BeaconFrame ... }` | 30min 前抑制 | 高 | verified |
| 24 | ST-024 | REQ-040,041 | 遥控 | COMMAND_DICTIONARY.md:17-56,378-431 | ProTC | 从外部系统接收解析 | `ProTC ground CommandFrame ReqCapByTable ProTable.B2;` | 每周期 | 中 | partial(ISSUE-001) |
| 25 | ST-025 | REQ-042,043 | 遥控 | cmd_handler.c:223-258; COMMAND_DICTIONARY.md:416-431 | Switch | 按命令分发 | `Switch (cmdId) { Case(SAFE_MODE): { Set powerMode SAFE; } Case(RELEASE_SAFE): { If (Soc > 0.30) { Set powerMode IDLE; } } Case(SET_MODE): { Set powerMode TargetModeParam; } Case(SET_BEACON_RATE): { Set beaconInterval RateParam; } Case(SET_TX_POWER): { SendData rf TxPowerCmd; } Case(JETSON_POWER): { If (PowerParam == ON) { SendData jetson PowerEnableCmd; } Else { SendData jetson PowerDisableCmd; } } Case(AI_ENABLE): { Set s_aiEnabled true; } Case(AI_DISABLE): { Set s_aiEnabled false; } Case(FORCE_FALLBACK): { Set s_aiEnabled false; Set beaconText TemplateText; } Case(REQUEST_TLM): { ProTM ground CommandAck ReqCapByTable ProTable.B1; } Case(CLEAR_FAULTS): { Set faultFlags 0; } Case(SW_RESET): { SendData wdt ResetSignal; } }` | 命令到达后 | 中 | partial(ISSUE-022) |
| 26 | ST-026 | REQ-037 | 信标 | COMMAND_DICTIONARY.md:140-150; MISSION_RULES.md FC-004 | SendData | 向设备发数据 | `Case(SET_TX_POWER): { SendData rf TxPowerCmd; }` | 命令到达后 | 中 | partial(ISSUE-006) |
| 27 | ST-027 | REQ-008,009,010 | 部署 | deployment.c:117-208; deployment.h:33-48 | Composite | 顺序组合 | `Composite DeploymentSequence { GetData hdrm DeploySwitchState; In(1800000ms) SendData hdrm AntennaBurnPulse; In(10000ms) GetData hdrm AntennaDeployStatus; SendData hdrm SolarBurnPulse; Set s_deploymentComplete true; }` | In(30min)、In(10s) | 中 | partial(ISSUE-025/037) |
| 28 | ST-028 | REQ-053,054 | EOL | END_OF_LIFE_PLAN.md:37-39,72-106 | If+SendData | 条件发控制 | `If (lastContactAge > 2592000000ms || Soc < 0.15) { Set eolFlag true; } If (eolFlag) { SendData eps ChargerDisableCmd; SendData rf TxDisableCmd; SendData hdrm DragDeployCmd; }` | 条件满足后 | 高 | verified |
| 29 | ST-029 | REQ-048 | 故障管理 | FDIR_DESIGN.md:345-370; watchdog_mgr.c:167-183 | SendData | 向设备发数据 | `At(0, 10000ms) SendData wdt KickSignal;` | At(0,10s) | 中 | partial(ISSUE-013) |
| 30 | ST-030 | REQ-007 | 初始化/部署 | deployment.h:33; COMMISSIONING_PLAN.md:64-87 | Set | 变量赋值 | `At(1800000ms) Set s_rfInhibit false;` | At(30min 绝对) | 高 | verified |
| 31 | ST-031 | REQ-061 | 约束 | OBC_DESIGN.md:136-151; CMakeLists.txt:19 | 系统约束 | 空间/语言约束 | `Executed Within 128kb; Language Standard C11;` | - | 高 | partial(ISSUE-020) |

## 未映射为语句的 REQ 处理

| REQ-ID | 处理方式 | 关联 ISSUE |
|---|---|---|
| REQ-002,011,012,026,032,049,056,057,065 | uncovered：无实现证据或关键资源缺失，不生成猜测语句 | ISSUE-025,028,031,032,033,037,038 |
| REQ-018,035,044,052,059,060,062,063,064 | constraint-only：进入 SystemConstraints 注释或问题清单 | ISSUE-002,014,016 |
| REQ-058 | conflict：两处原文直接矛盾（联邦学习 vs 无上行更新），不选边 | ISSUE-034 |

## 软件需求映射要点（对应 references/software-mapping.md）

- **ST-006 GetData eps**: 软件经 I2C1 按 ICD_OBC_EPS.md:128-135 写读时序（START|ADDR+W|REG|DATA|STOP、读带 RESTART）取数；NACK 重试 3 次、超时 100ms；总线恢复=SCL 9 时钟+STOP（ICD_OBC_EPS.md:316-328）。
- **ST-021 GetData jetson BeaconText**: 软件发 BEACON_REQ,<seq>,<max_len>、等待 BEACON_RSP,<seq>,<text>、CRC16 校验、ASCII/长度校验，总时长 ≤10s，超时判 AI 不可用（ICD_OBC_JETSON.md:160-171,222-228）。
- **ST-024 ProTC**: 软件收帧后按 SYNC→呼号→序列防重放→CRC→操作码→参数范围校验，非法回 NAK（COMMAND_DICTIONARY.md:37-43,395-404）。注意三套帧方案冲突（ISSUE-001），验收前必须先裁定。
- **ST-020 ProTM**: 软件构造 AX.25 UI 帧（地址编码左移 1 位、FCS CRC-16-CCITT LSB 先）并经 rf 以 AFSK 1200 发射；总时长 ≤5s（beacon.c:54-71,307-309,424-440; SRS-P002）。
- **ST-011 Compute**: 软件用当前与上一拍磁场差分求 B_dot，按 m=-k·B_dot（k=5.0e6）计算并饱和到 ±0.2 A·m²（adcs_control.c:401-423）。
