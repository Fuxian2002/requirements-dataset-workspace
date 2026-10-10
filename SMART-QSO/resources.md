# SMART-QSO SpaceRDL 资源目录

> 五类资源: 控制器 / 设备与外部系统 / 数据元素 / 算法(FormulaTable) / 协议(ProTable)与端口。
> 命名规则: SpaceRDL 标识 = code.rdl 中实际使用的名字。标注 `[待确认]` 的字段不得在 code.rdl 中写入确定值。

## 1. 控制器

### RES-001 `obc`
- 类型: Controller (CtrOBC)
- 语义名称: 低功耗 OBC，执行飞行软件
- 硬件: STM32L476RG Cortex-M4F 80MHz, Flash 1MB, RAM 128KB（OBC_DESIGN.md:136-151）；与 ARCHITECTURE.md:175-186 的 Ambiq Apollo4 主备关系相反 → ISSUE-020
- 控制周期: 1000ms（ICD_OBC_ADCS.md:301-305、ICD_OBC_EPS.md:288-295 一致）；代码主循环 20ms → ISSUE-015
- 接口: I2C1(100kHz)→EPS、I2C2(400kHz)→ADCS、UART1(115200)→Jetson、SPI1(1MHz)→RF（OBC_DESIGN.md:73-79）
- 来源: docs/hardware/OBC_DESIGN.md:136-183; software/flight/src/main.c:37-46
- 被引用需求: REQ-001~066（全部）
- 置信度: 高（硬件主备、控制周期为争议项）

## 2. 设备与外部系统

### RES-002 `eps`
- 类型: Device (EpsController)
- 语义名称: 电源控制与分配子系统（MPPT+BMS+PDU）
- 端口/协议: I2C，地址 0x48（ICD_OBC_EPS.md:62,76；验证计划写 0x50 → ISSUE-005）；电池监视 0x55、太阳能监视 0x40（无寄存器映射 → ISSUE-025）
- 数据项: BatteryVoltage(mV u16)、BatteryCurrent(mA i16)、BatteryTemp(0.1°C i16)、Soc(% u8)、SolarVoltage、SolarCurrent、BusVoltage、LoadEnableMask(bit3 ADCS/bit2 HEATER/bit1 RF 默认1/bit0 PAYLOAD 默认0)、EpsMode(0=SAFE/1=IDLE/2=ACTIVE)
- 寄存器: STATUS 0x00、MODE 0x01、LOAD_EN 0x02、VBATT 0x10、IBATT 0x12、TBATT 0x14、SOC 0x16、VSOLAR 0x20、ISOLAR 0x22、VBUS 0x30（ICD_OBC_EPS.md:139-156）
- 来源: docs/interfaces/ICD_OBC_EPS.md:51-56,76-100,139-168,275-295
- 被引用需求: REQ-013,017,019,053
- 置信度: 高（物理层 UART vs I2C 矛盾 → ISSUE-004）

### RES-003 `rf`
- 类型: Device (RfTransponder)
- 语义名称: RF 收发机（Si4463）
- 端口/协议: SPI Mode0（CPOL=0/CPHA=0）typ 4MHz/max 10MHz，10 针 J3/J1（ICD_OBC_RF.md:58-69,86-88）；RF_SDN 高=Shutdown
- 数据项: TxPowerLevel(0.5/1.0/2.0W)、TxPowerCmd、TxDisableCmd、RF 中断状态
- 频率/调制: 145.825 MHz 或 145.8-146.0（TBD）、GFSK 9600 vs AFSK 1200 → ISSUE-006/007
- 来源: docs/interfaces/ICD_OBC_RF.md:41,106-114,137-147,156-160,219-244; docs/hardware/RF_DESIGN.md:148-165
- 被引用需求: REQ-037,038,053
- 置信度: 高（调制与功率切换编码为争议项）

### RES-004 `adcs`
- 类型: Device (AdcsBoard)
- 语义名称: 姿态确定与控制板
- 端口/协议: I2C（磁强计 LIS3MDL 0x1E ±4gauss 10Hz；陀螺 LSM6DS3 0x6A ±250°/s 26Hz；验证计划写 0x68 → ISSUE-005）+ MTQ PWM（1-20kHz，0-255 → 0-100mA → 0-0.2A·m²，128=关，<128 负/>128 正）+ 6 路太阳敏感器 ADC
- 数据项: MagField[3](µT)、GyroRate[3]、SunVector[3](归一化)、MtqPwm[3](-100..100)、MtqDipole[3](±0.2 A·m²)、rateMag
- 来源: docs/interfaces/ICD_OBC_ADCS.md:57-69,93-98,102-116,124-189,244-248,301-325; software/flight/src/adcs_control.c:401-506
- 被引用需求: REQ-027,028,029,030,031
- 置信度: 高

### RES-005 `jetson`
- 类型: Device (JetsonPayload)
- 语义名称: AI 载荷（Jetson Orin Nano Super，降频限功率）
- 端口/协议: UART 115200 8N1 无校验无流控 + Power Enable GPIO（ICD_OBC_JETSON.md:29-36,68-74）；消息 `<MSG_TYPE>,<F1>...<CRC16>\n`，CRC-16 CCITT poly 0x1021 init 0xFFFF
- 数据项: PowerEnableCmd、PowerDisableCmd、TelemetryCsv(TELEMETRY,...)、BeaconText(BEACON_RSP)、STATUS 健康字段
- 时序: 上电 T+100ms PWR_EN→T+500ms 启动→T+30s 就绪；断电 SHUTDOWN→T+5s 撤使能→T+100ms 断 5V；BEACON_RSP 超时 10s；重试 3 次后断电重启（ICD_OBC_JETSON.md:89-100,222-228,253-265）
- 功耗: Boot 10W/Idle 5W/Inference 7.5W/Peak 15W（ICD_OBC_JETSON.md:105-110）
- 来源: docs/interfaces/ICD_OBC_JETSON.md:29-36,51-55,68-74,89-110,121-134,160-171,195-265
- 被引用需求: REQ-020,022,023,025,047
- 置信度: 高

### RES-006 `ground`
- 类型: ExternalDevice（系统边界外，ProTC/ProTM 对象）
- 语义名称: 业余无线电地面站网
- 端口/协议: RFLink；下行 145.825MHz±1kHz AFSK 1200/GFSK 9600（冲突 ISSUE-006/007）；上行 435.XXX（存在性冲突 ISSUE-003）；AX.25 UI 帧；地面侧 Direwolf KISS
- 数据项: CommandFrame、CommandAck(0x00 ACK/0x01-0x07 NAK)、BeaconFrame
- 来源: docs/interfaces/ICD_SPACE_GROUND.md:63-83,103-111,167-197; docs/ground/GROUND_STATION_OPERATIONS_MANUAL.md:36-48,108-119
- 被引用需求: REQ-033,034,040,041
- 置信度: 高（存在性本身为争议项）

### RES-007 `wdt`
- 类型: Device (WdtPeriph)
- 语义名称: 硬件看门狗 IWDG（LSI 32kHz）
- 数据项: KickSignal、ResetSignal
- 超时: 30s（OBC_DESIGN.md:331-335、watchdog_mgr.h:44）vs 5s（MISSION_RULES.md:128-131、system_init.h:42）→ ISSUE-013
- 来源: docs/hardware/OBC_DESIGN.md:331-335; software/flight/include/watchdog_mgr.h:44
- 被引用需求: REQ-005,048
- 置信度: 高（超时值为争议项）

### RES-008 `hdrm`
- 类型: Device (DeployMech)
- 语义名称: 部署机构（烧线 HDRM + 部署开关）
- 数据项: DeploySwitchState（常闭、分离断开，deployment.c:359-370）、AntennaBurnPulse(3s)、SolarBurnPulse(5s)、AntennaDeployStatus、DragDeployCmd
- 参数: 烧线 2A/3s、双烧线冗余、重试 3 次/60s（RF_DESIGN.md:199-226; deployment.h:33-48）
- GPIO: DEPLOY_EN=4、DEPLOY_SENSE=9（hal_gpio.h:33-38）
- 来源: software/flight/src/deployment.c:26-29,117-208; software/flight/include/deployment.h:33-48
- 被引用需求: REQ-007,008,009,010,053
- 置信度: 中（模块未接入 main.c → ISSUE-025）

### RES-009 `fram`
- 类型: Device (MassMemory)
- 语义名称: 非易失存储 FRAM FM25V10 128KB（+W25Q128 16MB SPI 未建模）
- 数据项: MissionConfigData、MissionStateData、FaultLogEntry（100 条、含 CRC32）、EpsConfigData
- 来源: docs/hardware/OBC_DESIGN.md:180-183; software/flight/src/mission_data.c; fault_mgmt.h:29
- 被引用需求: REQ-003,019,046,051
- 置信度: 高（容量 128KB vs ARCHITECTURE 4MB → ISSUE-020；SYS-310 要求 ≥1MB → ISSUE-039）

## 3. 数据元素（DataDictionary 登记）

| 标识 | 类型/范围 | 单位 | 初值 | 来源 | 引用需求 |
|---|---|---|---|---|---|
| powerMode | enum SAFE/IDLE/ACTIVE | - | SAFE | eps_control.h:25-27; COMMISSIONING_PLAN.md:50-58 | REQ-006,014-017,050 |
| Soc | float 0..1 | % | 0.75(仿真) | main.c:71; eps_control.h | REQ-014-016,021,054,059 |
| sunlit | bool | - | 1 | beacon.c:168 | REQ-016,030 |
| epsTemp | float | °C | - | sensors.c:115-137 | REQ-045 |
| beaconInterval | uint 10..120 | s | 60 | system_state.c:413-423 | REQ-033 |
| beaconText / TemplateText | ASCII 可打印 | B | 模板轮询 | beacon.c:34-43,442-464 | REQ-024,025,039 |
| beaconTextValid | bool | - | false | beacon.c:131-156 | REQ-025 |
| s_aiEnabled | bool | - | false | eps_control.c:20-29(载荷默认关) | REQ-023,039 |
| s_rfInhibit | bool | - | true | COMMISSIONING_PLAN.md:50-58 | REQ-007,033 |
| s_deploymentComplete | bool | - | false | deployment.c 状态机 | REQ-008-010 |
| faultFlag / faultFlags / criticalFault | enum/位图 | - | 0 | smart_qso.h:124-147 | REQ-045,050 |
| eolFlag | bool | - | false | END_OF_LIFE_PLAN.md:37-39 | REQ-053,054 |
| lastContactAge | uint | ms | 0 | END_OF_LIFE_PLAN.md:37-39（30 天阈值） | REQ-054 |
| cmdId / TargetModeParam / RateParam / PowerParam | 命令解析结果 [待确认命名] | - | - | COMMAND_DICTIONARY.md:71-187 | REQ-040-043 |
| adcsMode | enum IDLE/DETUMBLE/SUNPOINT/ECLIPSE/SAFE | - | IDLE | adcs_control.h:72-78 | REQ-028-030 |
| rateMag | float | rad/s | - | adcs_control.h:39(阈值 0.0087) | REQ-029 |
| EnergyForecast90min / InsolationHistory | [待确认维度] | Wh | - | PDR.md:96-97; ML_MODELS.md:3 | REQ-055 |
| MagFieldPrev[3] | float[3] | µT | - | adcs_control.c:401-423(B-dot 差分) | REQ-028 |

## 4. 算法（AlgorithmRepository → FormulaTable 条目）

### RES-010 `FormulaTable.B1` BDotControl
- 公式: m = -k · B_dot，k = 5.0e6 A·m²·s/T；B_dot = (B_meas - B_prev)/dt；|m| ≤ 0.2 A·m²
- 输入: MagField[3]、MagFieldPrev[3]；输出: MtqDipole[3]
- 来源: docs/hardware/ADCS_DESIGN.md:208-219; software/flight/src/adcs_control.c:401-423
- 引用需求: REQ-028；置信度: 高

### RES-011 `FormulaTable.B2` SunPointControl
- 公式: 误差 = sun_vector × [1,0,0]；τ = kp · error，kp = 0.001；m = (τ × B)/|B|²（防除零 |B|²>1.0）；|m| ≤ 0.2
- 输入: SunVector[3]、MagField[3]；输出: MtqDipole[3]
- 来源: docs/hardware/ADCS_DESIGN.md:249-265; software/flight/src/adcs_control.c:425-472
- 引用需求: REQ-030；置信度: 高

### RES-012 `FormulaTable.B3` PowerForecast
- 算法: 功率预测 LSTM 型模型，INT8，<100kB（输入/输出维度与周期未定义 → ISSUE-033）
- 输入: InsolationHistory、Soc；输出: EnergyForecast90min（每轨日照与季节漂移学习、90 分钟能量预报，PDR.md:96-97）
- 来源: docs/ML_MODELS.md:3; docs/pdr/SMART-QSO_PDR.md:96-97
- 引用需求: REQ-055；置信度: 中

### RES-013 `TinyLMBeacon`（载荷侧算法，非 OBC Compute）
- 算法: Llama 3.2 3B (Instruct) INT8/FP8，TensorRT batch=1；24 token 生成 250-400ms；输出 ≤120 ASCII 字节、`de <CALL>:` 开头、非 SAFE 以 `73!` 结尾；违规拒绝/重生成一次后回退模板
- 来源: docs/ML_MODELS.md:17-51; docs/pdr/SMART-QSO_PDR.md:105-111
- 引用需求: REQ-023,024,066（作为 jetson 的 GetData 资源能力，OBC 不执行 Compute）
- 置信度: 中（尺寸 0.8-1.2MB vs 4MB → ISSUE-020/033）

## 5. 协议（ProTable）与端口

### RES-014 `ProTable.B1`（下行遥测/信标协议）
- AX.25 UI: Flag 0x7E | Dest 7B("CQ"+SSID 0xE0) | Src 7B(呼号+SSID 0x61) | Ctrl 0x03 | PID 0xF0 | Info(≤256B) | FCS CRC-16-CCITT(LSB 先)
- 信息字段: `de <CALL>: <text> | T=<t> M=<mode> SOC=<soc> BV=<v> SUN=<0|1> RF=<0|1> QSO=<n>`（beacon.c:200-211）
- 调制: AFSK 1200 bps mark 1200Hz/space 2200Hz、NRZI、5 连 1 插 0（BEACON_SPEC.md:8-9; ICD_BEACON_FORMAT.md:216-233）；GFSK 9600 冲突 → ISSUE-006
- 来源: software/flight/src/beacon.c:54-71,220-264,424-440; docs/interfaces/ICD_BEACON_FORMAT.md:39-45
- 引用需求: REQ-033-036,038；置信度: 高（字段格式三套 → ISSUE-009）

### RES-015 `ProTable.B2`（上行命令协议）
- 帧: SYNC 0x55AA | CALLSN 6B | SEQ u16 | CMD u16 | PARAM 16B | SPARE 2B | CRC-16（COMMAND_DICTIONARY.md:17-33）
- 校验: SYNC→呼号白名单→序列号防重放→CRC→操作码→参数范围（:37-43）；响应码 ACK 0x00/NAK 0x01-0x07
- 限速: ≤1 命令/秒；危险命令两步确认（CONFIRM=0/1，60s 内）
- 冲突: 与 CMD_TLM_DATABASE.md（SYNC 0xEB90、单字节 ID）及代码 cmd_handler.c（0xAA 0x55、16 位累加和）三套方案并存 → ISSUE-001
- 来源: docs/operations/COMMAND_DICTIONARY.md:17-56,378-431
- 引用需求: REQ-040-044；置信度: 中（三套方案冲突）

### RES-016 端口
- `I2C1`（100kHz，EPS）、`I2C2`（400kHz，ADCS）、`SPI1`（1MHz，RF）、`UART1`（115200 8N1，Jetson）——OBC_DESIGN.md:73-79
- `RFLink`（星地链路逻辑端口，物理经 rf 收发机）；`WDT1`（IWDG）
- 配置结构名（EpsI2CConfig/AdcsI2CConfig/RfSpiConfig/JetsonUartConfig/WatchdogConfig）为生成占位标识，项目资源库尚未建立 → ISSUE-025
