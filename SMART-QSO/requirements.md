# SMART-QSO 规范化需求文档

> 由 `req-to-spacerdl` 从项目文档与代码逆向提炼。父需求 ID（MRD-/SYS-/SRS-）保留在"原文/行为"列。
> 状态: `mapped`=已映射到语句；`constraint-only`=仅映射为约束；`uncovered`=未覆盖（有 ISSUE）；`conflict`=原文相互冲突（有 ISSUE）。
> 置信度: 高=文档+代码一致；中=单一来源或推断；低=弱证据。

## T1 系统初始化

| REQ-ID | 任务 | 原文/行为 | 来源 | 参与者 | 触发 | 输入/输出 | 可观察结果 | 时间/质量约束 | 候选算子 | 置信度 | 状态 | 问题 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | 初始化 | SYS-300: 上电 30s 内执行飞行软件；SRS-F001 Initialize within 30s | SYSTEM_REQUIREMENTS.md:163; RTM:123; main.c:95-171 | obc, 各设备 | 上电 | -/初始化完成 | 上电 30s 内各接口就绪、进入主循环 | Finished Within 30s | Init×4+GetData+Set (Composite) | 高 | mapped | 无 |
| REQ-002 | 初始化 | SRS-F003-005: 上电自检、复位计数、启动原因记录 | RTM:124-127; system_init.c:225-297,550-583 | obc, fram | 上电 | -/自检结果、bootCount | 自检通过才进入飞行；启动原因可查 | - | GetData+Set | 中 | uncovered | ISSUE-025（模块未接线） |
| REQ-003 | 初始化 | SRS-F002: 从 NVM 加载配置 | RTM:122; mission_data.c:78 | obc, fram | 上电 | MissionConfigData/加载结果 | 配置载入且 CRC 校验通过 | - | GetData | 高 | mapped | 无 |
| REQ-004 | 初始化 | SYS-320-324: OBC 与各子系统接口 | SYSTEM_REQUIREMENTS.md:183-187; OBC_DESIGN.md:73-79 | obc, eps, rf, adcs, jetson | 上电 | 配置结构/端口就绪 | I2C1/SPI1/I2C2/UART1 可通信 | - | Init | 高 | mapped | ISSUE-025（配置结构名待资源库） |
| REQ-005 | 初始化 | SYS-021: 所有处理器看门狗保护 | SYSTEM_REQUIREMENTS.md:76; watchdog_mgr.h:44; OBC_DESIGN.md:331-335 | obc, wdt | 上电 | 超时配置/生效 | 喂狗停止即复位 | - | Init | 中 | mapped | ISSUE-013（5s/30s 冲突） |
| REQ-006 | 初始化 | 上电进入 SAFE 模式 | COMMISSIONING_PLAN.md:50-58; system_state.c:56-69 | obc | 上电 | -/powerMode=SAFE | 遥测 STATE=SAFE | - | Set | 高 | mapped | 无 |
| REQ-007 | 初始化/部署 | SYS-221: 天线展开抑制至分离后 30 分钟 | SYSTEM_REQUIREMENTS.md:151; deployment.h:33; COMMISSIONING_PLAN.md:64-87 | obc, hdrm, rf | 上电/分离 | -/s_rfInhibit | 分离 30min 内无 RF 发射 | At(30min) | Set+At | 高 | mapped | 无 |

## T2 部署

| REQ-ID | 任务 | 原文/行为 | 来源 | 参与者 | 触发 | 输入/输出 | 可观察结果 | 时间/质量约束 | 候选算子 | 置信度 | 状态 | 问题 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REQ-008 | 部署 | 检测部署开关分离 | deployment.c:359-370 | obc, hdrm | 周期 | DeploySwitchState/分离标志 | 分离事件被识别 | - | GetData | 中 | mapped | ISSUE-025 |
| REQ-009 | 部署 | SYS-220: 天线展开，烧线 3s | SYSTEM_REQUIREMENTS.md:150; deployment.h:36; deployment.c:153-159 | obc, hdrm | 30min 等待后 | 烧线脉冲/天线展开 | 天线展开状态验证通过 | In(30min) | SendData | 中 | mapped | ISSUE-025 |
| REQ-010 | 部署 | 太阳翼展开，烧线 5s | deployment.h:39; deployment.c:202-208 | obc, hdrm | 天线展开后 | 烧线脉冲/太阳翼展开 | 太阳翼展开 | - | SendData | 中 | mapped | ISSUE-025 |
| REQ-011 | 部署 | 展开验证失败重试 3 次、间隔 60s | deployment.h:42-48; deployment.c:161-174 | obc, hdrm | 验证失败 | 状态/重试 | 最多 3 次重试 | Over(60s, nc, 3) | SendData/GetData | 中 | uncovered | ISSUE-037 |
| REQ-012 | 部署 | 展开失败记录 FAULT_TYPE_DEPLOYMENT | deployment.c:134-150 | obc, fram | 重试耗尽 | 故障/日志条目 | 故障日志有部署失败记录 | - | Set/SendData | 中 | uncovered | ISSUE-037 |

## T3 EPS 遥测与功率模式

| REQ-ID | 任务 | 原文/行为 | 来源 | 参与者 | 触发 | 输入/输出 | 可观察结果 | 时间/质量约束 | 候选算子 | 置信度 | 状态 | 问题 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REQ-013 | 功率管理 | SYS-124: EPS 上报电压/电流/温度；1Hz 轮询 | SYSTEM_REQUIREMENTS.md:118; ICD_OBC_EPS.md:139-156,275-295; sensors.c:68-137 | obc, eps | 1Hz | 寄存读/VBATT,IBATT,TBATT,SOC,VSOLAR,ISOLAR,VBUS | 遥测项每 1s 更新 | 周期 1Hz | GetData | 高 | mapped | ISSUE-027（硬件路径未实现） |
| REQ-014 | 功率管理 | SRS-F013: SOC<25% 进入 SAFE | RTM:131; eps_control.h:41-47; main.c:211-224 | obc | 周期 | Soc/powerMode | SOC<25% 时 STATE=SAFE | - | If/Set | 高 | mapped | ISSUE-012（阈值多套） |
| REQ-015 | 功率管理 | SRS-F014: SOC<40% 进入 IDLE | RTM:132; eps_control.h:41-47; main.c:211-224 | obc | 周期 | Soc/powerMode | SOC<40% 时 STATE=IDLE | - | If/Set | 高 | mapped | ISSUE-012 |
| REQ-016 | 功率管理 | SOC>55% 且阳照进入 ACTIVE | main.c:211-224; eps_control.h:41-47 | obc | 周期 | Soc,sunlit/powerMode | 条件满足时 STATE=ACTIVE | - | If/Set | 高 | mapped | ISSUE-012 |
| REQ-017 | 功率管理 | SRS-F011: 控制负载开关（按模式） | RTM:129; eps_control.c:178-207; ICD_OBC_EPS.md:180-186,250-258 | obc, eps | 模式变化 | powerMode/LoadEnableMask | 各通道通断符合模式 | - | Switch/SendData | 高 | mapped | ISSUE-023 |
| REQ-018 | 功率管理 | 功率限 SAFE 0.5W/IDLE 1.5W/ACTIVE 3.0W | eps_control.h:32-38 | obc | 模式变化 | - | 载荷不超过限值 | - | - | 高 | constraint-only | 无 |
| REQ-019 | 功率管理 | SRS-F017: EPS 配置持久化 | RTM:135; eps_control.c:234-284 | obc, fram | 周期 | EpsConfigData/写入 | 复位后配置恢复 | - | SendData | 高 | mapped | 无 |

## T4 AI 载荷管理

| REQ-ID | 任务 | 原文/行为 | 来源 | 参与者 | 触发 | 输入/输出 | 可观察结果 | 时间/质量约束 | 候选算子 | 置信度 | 状态 | 问题 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REQ-020 | 载荷管理 | SYS-503: 载荷由 OBC 命令功率门控 | SYSTEM_REQUIREMENTS.md:225; eps_control.c:86-117; ICD_OBC_JETSON.md:89-100 | obc, eps, jetson | 周期 | 门控命令/PWR_EN | Jetson 供电随模式通断 | 上电时序 100ms/500ms/30s | SendData | 高 | mapped | 无 |
| REQ-021 | 载荷管理 | SOC<55% 禁止开启载荷 | eps_control.h:41-47 (EPS_SOC_PAYLOAD_THRESHOLD 0.55) | obc | 周期 | Soc/允许标志 | SOC<55% 时载荷不开机 | - | If | 高 | mapped | ISSUE-012 |
| REQ-022 | 载荷管理 | SYS-511: 健康数据发往载荷（60s CSV） | SYSTEM_REQUIREMENTS.md:235; main.c:304-379; ICD_OBC_JETSON.md:121 | obc, jetson | 60s | TelemetryCsv/UART | Jetson 每 60s 收到 TELEMETRY 行 | 周期 60s | SendData | 高 | mapped | 无 |
| REQ-023 | 载荷管理 | SYS-512: 请求并接收 AI 文本 ≤10s | SYSTEM_REQUIREMENTS.md:236; ICD_OBC_JETSON.md:160-171,222-228 | obc, jetson | 信标周期 | BEACON_REQ/BEACON_RSP | 文本在 10s 内返回或超时 | Finished Within 10s | GetData | 高 | mapped | ISSUE-028（接收路径未接线） |
| REQ-024 | 载荷管理 | SYS-513: 文本 ASCII-only 且限长 | SYSTEM_REQUIREMENTS.md:237; beacon.c:442-464; BEACON_SPEC.md:30-32 | obc | 收到文本 | 文本/有效标志 | 非 ASCII/超长文本被拒 | 长度 120/200B 冲突 | GetData(能力) | 中 | mapped | ISSUE-017 |
| REQ-025 | 载荷管理 | SYS-520/521: 失败或超时回退模板信标 | SYSTEM_REQUIREMENTS.md:240-241; beacon.c:131-156 | obc | AI 无效 | 文本源选择 | 信标用模板文本 | - | If/Set | 高 | mapped | 无 |
| REQ-026 | 载荷管理 | SYS-523: 重复失败自动断电重启 | SYSTEM_REQUIREMENTS.md:242; ICD_OBC_JETSON.md:261-265 | obc, jetson | 3 次失败 | 失败计数/重启 | 3 次失败后断电重启 | 60s 后重连 | If/SendData | 中 | uncovered | ISSUE-028 |

## T5 姿态确定与控制

| REQ-ID | 任务 | 原文/行为 | 来源 | 参与者 | 触发 | 输入/输出 | 可观察结果 | 时间/质量约束 | 候选算子 | 置信度 | 状态 | 问题 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REQ-027 | 姿态控制 | SYS-323/400-403: 磁强计/太阳敏感器/陀螺采集 | SYSTEM_REQUIREMENTS.md:186,197-202; ICD_OBC_ADCS.md:124-171; adcs_control.c:336-382 | obc, adcs | 10Hz(磁)/26Hz(陀螺)/1Hz(太阳) | I2C 读/MagField[3],GyroRate[3],SunVector[3] | 传感器数据更新 | - | GetData | 中 | mapped | ISSUE-027 |
| REQ-028 | 姿态控制 | SYS-421: B-dot 消旋 m=-k·B_dot, k=5.0e6, |m|≤0.2 | SYSTEM_REQUIREMENTS.md:209; adcs_control.c:401-423; ADCS_DESIGN.md:212-219 | obc | 1Hz | MagField/MtqDipole[3] | 偶极子指令随磁场变化率输出 | - | Compute (FormulaTable.B1) | 高 | mapped | 无 |
| REQ-029 | 姿态控制 | 消旋完成判定 rate<0.0087 rad/s 且稳定 300s | adcs_control.h:39-45 | obc | 1Hz | rateMag/模式切换 | 收敛后转 SUNPOINT | 300s settling | If/Set | 中 | mapped | ISSUE-037 |
| REQ-030 | 姿态控制 | SYS-422: 太阳指向 kp=0.001, m=(τ×B)/|B|² | SYSTEM_REQUIREMENTS.md:210; adcs_control.c:425-472; ADCS_DESIGN.md:249-265 | obc | 1Hz | SunVector,MagField/MtqDipole[3] | 指向误差趋零 | - | Compute (FormulaTable.B2) | 高 | mapped | 无 |
| REQ-031 | 姿态控制 | SYS-412: 磁力矩器独立可控 PWM 0-255→0-0.2A·m² | SYSTEM_REQUIREMENTS.md:201; ICD_OBC_ADCS.md:177-189; adcs_control.c:474-506 | obc, adcs | 1Hz | MtqDipole/MtqPwm[3] | PWM 信号输出 | - | SendData | 中 | mapped | ISSUE-027 |
| REQ-032 | 姿态控制 | 磁强计离线→禁用 ADCS；陀螺离线→仅磁；太阳失效→仅磁 | ICD_OBC_ADCS.md:320-325 | obc | 故障 | 传感器状态/降级模式 | 降级行为符合表 | - | If/Set | 中 | uncovered | ISSUE-027 |

## T6 信标与下行

| REQ-ID | 任务 | 原文/行为 | 来源 | 参与者 | 触发 | 输入/输出 | 可观察结果 | 时间/质量约束 | 候选算子 | 置信度 | 状态 | 问题 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REQ-033 | 信标 | MRD-020: 至少每 60s 一次信标；SYS-211: 间隔 10-120s 可配置；默认 60s | MISSION_REQUIREMENTS.md:79; SYSTEM_REQUIREMENTS.md:140; beacon.h:39-45; system_state.c:413-423 | obc, rf, ground | 60s 周期 | beaconInterval/帧 | 地面每 60s 内收到信标 | Finished Within 5s | At/ProTM | 高 | mapped | ISSUE-008（多方周期冲突） |
| REQ-034 | 信标 | SYS-210: AX.25 UI 帧 (Ctrl 0x03, PID 0xF0, FCS CRC-16-CCITT) | SYSTEM_REQUIREMENTS.md:139; beacon.c:220-264,424-440; ICD_BEACON_FORMAT.md:39-45 | obc, ground | 信标周期 | 载荷/帧 | 帧结构符合 AX.25 校验 | - | ProTM(能力) | 高 | mapped | ISSUE-009 |
| REQ-035 | 信标 | SYS-212: 信标含呼号 | SYSTEM_REQUIREMENTS.md:141; beacon.h:36 "SQSO-1" | obc | 信标周期 | CALLSIGN/帧源地址 | 帧含呼号 | - | - | 中 | constraint-only | ISSUE-010（SQSO-1/SMARTQ-1/SQSO 冲突） |
| REQ-036 | 信标 | SYS-213/MRD-021: 健康遥测入信标 | SYSTEM_REQUIREMENTS.md:142; beacon.c:200-211 | obc | 信标周期 | T,SOC,BV,SUN,RF,QSO/信息字段 | 解码可得健康数据 | - | ProTM(能力) | 高 | mapped | 无 |
| REQ-037 | 信标 | SYS-201: 0.5-2W 可选功率；FC-004 ≤2W | SYSTEM_REQUIREMENTS.md:131; MISSION_RULES.md:118-125; COMMAND_DICTIONARY.md:140-150 | obc, rf | 命令 | TxPowerCmd/功率档 | 功率档 0.5/1.0/2.0W | - | SendData | 中 | mapped | ISSUE-006（切换编码缺失） |
| REQ-038 | 信标 | SYS-202: AFSK 1200 bps | SYSTEM_REQUIREMENTS.md:132; BEACON_SPEC.md:8; RF_DESIGN.md:134-144 | obc, rf | 发射 | 数据/调制信号 | 频谱符合 1200Hz/2200Hz 音 | - | ProTM(能力) | 中 | mapped | ISSUE-006（vs GFSK 9600） |
| REQ-039 | 信标 | SYS-214/215: AI 文本优先、模板回退 | SYSTEM_REQUIREMENTS.md:143-144; beacon.c:131-156 | obc, jetson | 信标周期 | 文本/帧信息字段 | AI 可用时用 AI 文本 | - | If/Set | 高 | mapped | 无 |

## T7 遥控

| REQ-ID | 任务 | 原文/行为 | 来源 | 参与者 | 触发 | 输入/输出 | 可观察结果 | 时间/质量约束 | 候选算子 | 置信度 | 状态 | 问题 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REQ-040 | 遥控 | 接收并解析上行命令 | COMMAND_DICTIONARY.md:17-24,378-391; ICD_SPACE_GROUND.md:167-186 | ground, obc | 上行帧到达 | CommandFrame/cmdId,参数 | 命令被识别并执行 | - | ProTC | 高 | mapped | ISSUE-001（三套帧方案） |
| REQ-041 | 遥控 | 命令校验: SYNC/呼号/序列号防重放/CRC/参数范围 | COMMAND_DICTIONARY.md:37-43; input_validation.c:101-131,415-424 | obc | 收帧 | 帧/接受或 NAK | 非法帧被拒并回 NAK | - | ProTC(能力) | 高 | mapped | ISSUE-001 |
| REQ-042 | 遥控 | 状态允许矩阵: 各状态仅允许特定命令 | cmd_handler.c:223-258; COMMAND_DICTIONARY.md:416-424 | obc | 命令到达 | 状态/cmdId 过滤 | 非法组合被拒 | - | Switch | 中 | mapped | ISSUE-022（状态集冲突） |
| REQ-043 | 遥控 | 危险命令授权 (RESET/CLEAR_FAULTS/PLD_ENABLE 需 AUTH 0xDEADBEEF) | cmd_handler.c:26,260-290; COMMAND_DICTIONARY.md:426-431 | obc | 危险命令 | 授权码/执行 | 无授权被拒 | 两步确认 60s | ProTC(能力) | 中 | mapped | ISSUE-001 |
| REQ-044 | 遥控 | 命令限速 ≤1 次/秒 | COMMAND_DICTIONARY.md:408-414 | obc | 命令流 | 速率/拒绝 | 超速被拒 | - | - | 高 | constraint-only | 无 |

## T8 故障管理

| REQ-ID | 任务 | 原文/行为 | 来源 | 参与者 | 触发 | 输入/输出 | 可观察结果 | 时间/质量约束 | 候选算子 | 置信度 | 状态 | 问题 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REQ-045 | 故障管理 | SRS-F040: 故障检测（热>40°C、SOC<30%、电压/电流越限） | RTM:148; main.c:271,280; sensors.c:76-137 | obc | 10s/周期 | 遥测/故障标志 | 越限即置位并记录 | 检测<100ms (SRS-P003) | If/Set | 高 | mapped | ISSUE-014（阈值多套） |
| REQ-046 | 故障管理 | SRS-F041: 故障日志 NVM 100 条 CRC | RTM:149; fault_mgmt.c:75-80,164-195; smart_qso.h:61 | obc, fram | 故障发生 | FaultLogEntry/持久化 | 复位后日志可读、损坏条目丢弃 | - | SendData | 高 | mapped | ISSUE-013/039（容量冲突） |
| REQ-047 | 故障管理 | SRS-F042: 自主恢复（热→关载荷+IDLE；功率→降模式） | RTM:150; fault_mgmt.c:208-233 | obc, jetson | 故障 | 恢复动作/模式 | 载荷关闭、模式降级 | - | If/SendData/Set | 高 | mapped | 无 |
| REQ-048 | 故障管理 | SYS-021: 看门狗喂狗 | SYSTEM_REQUIREMENTS.md:76; watchdog_mgr.c:167-183; FDIR_DESIGN.md:345-370 | obc, wdt | 10s | KickSignal/复位计时清零 | 喂狗停止即复位 | 双层 10s/30s | SendData | 中 | mapped | ISSUE-013 |
| REQ-049 | 故障管理 | 任务级看门狗: miss≥3 判 stalled | watchdog_mgr.h:38-50; watchdog_mgr.c:86-111 | obc | 1s | 心跳/FAULT_TYPE_WATCHDOG | 停滞任务被标记 | miss≥3 | If/Set | 中 | uncovered | ISSUE-038 |
| REQ-050 | 故障管理 | SRS-F043: 严重故障转 SAFE | RTM:151; fault_mgmt.c:156 | obc | 严重故障 | criticalFault/powerMode | STATE=SAFE | - | If/Set | 中 | mapped | 无 |

## T9 数据存储

| REQ-ID | 任务 | 原文/行为 | 来源 | 参与者 | 触发 | 输入/输出 | 可观察结果 | 时间/质量约束 | 候选算子 | 置信度 | 状态 | 问题 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REQ-051 | 数据管理 | SYS-310-313: 任务数据 ≥1MB、CRC32 保护、跨复位持久 | SYSTEM_REQUIREMENTS.md:172-176; mission_data.c:56-89; crc32.c:93-108 | obc, fram | 2s | MissionStateData/写入 | 复位后数据完好 | 持久化<500ms (SRS-P007) | SendData | 高 | mapped | ISSUE-039（1MB vs 128KB FRAM） |
| REQ-052 | 数据管理 | SYS-303: 采集并存储遥测 | SYSTEM_REQUIREMENTS.md:165; telemetry.c:53-57,141-234 | obc | 周期 | 遥测帧/存储 | 遥测可回放 | 速率 10-300s 可配 | GetData | 中 | constraint-only | ISSUE-002 |

## T10 寿命末期

| REQ-ID | 任务 | 原文/行为 | 来源 | 参与者 | 触发 | 输入/输出 | 可观察结果 | 时间/质量约束 | 候选算子 | 置信度 | 状态 | 问题 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REQ-053 | EOL | SYS-800-802: 钝化序列（禁充电→最大负载→关 RF→部署拖曳） | SYSTEM_REQUIREMENTS.md:287-289; END_OF_LIFE_PLAN.md:72-106 | obc, eps, rf, hdrm | eolFlag | 各命令/执行 | 无储能、无发射、拖曳装置部署 | T-15m 禁充电/T-5m 关 RF | If/SendData | 高 | mapped | 无 |
| REQ-054 | EOL | 自主钝化触发: 30 天无有效接触或 SOC<15% 持续 | END_OF_LIFE_PLAN.md:37-39,97-106 | obc | 周期 | lastContactAge,Soc/eolFlag | 触发后按序列钝化 | 30 天 | If/Set | 高 | mapped | 无 |

## T11 AI 能力与运行约束

| REQ-ID | 任务 | 原文/行为 | 来源 | 参与者 | 触发 | 输入/输出 | 可观察结果 | 时间/质量约束 | 候选算子 | 置信度 | 状态 | 问题 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REQ-055 | AI | MRD-041: 学习功率可用性并做 90 分钟能量预报 | MISSION_REQUIREMENTS.md:101; PDR.md:96-97; ML_MODELS.md:3 | obc | 周期 | InsolationHistory,Soc/EnergyForecast90min | 预报输出 | - | Compute (FormulaTable.B3) | 中 | mapped | ISSUE-033 |
| REQ-056 | AI | MRD-043: QSO 公平优先级 | MISSION_REQUIREMENTS.md:103; ARCHITECTURE.md:242 | obc, ground | QSO 请求 | - | 公平性度量 Gini≤0.35 | 60 天窗口 | Compute | 低 | uncovered | ISSUE-031（无公式/模型规格） |
| REQ-057 | AI | MRD-042: 预测区域需求 | MISSION_REQUIREMENTS.md:102 | obc | - | - | 区域需求预测 | - | Compute | 低 | uncovered | ISSUE-032（无模型） |
| REQ-058 | AI | 社区模型更新（联邦学习 vs 无上行更新） | PDR.md:27,114-115; CLAUDE.md 设计原则 | ground, obc | - | - | 模型更新应用 | 每季度≥1 次 vs 禁止 | - | 低 | conflict | ISSUE-034 |
| REQ-059 | 约束 | SOC 绝对下限 15% | MISSION_RULES.md:86-94 | obc | 周期 | Soc/禁操作 | SOC 不低于 15% | - | - | 高 | constraint-only | 无 |
| REQ-060 | 约束 | AI 推理占空比 ≤10%、单次≤60s、间隔≥540s | MISSION_RULES.md:107-113 | obc, jetson | 推理 | 占空比计数/限流 | 占空比不超限 | - | - | 高 | constraint-only | ISSUE-016 |
| REQ-061 | 约束 | 内存 ≤128KB RAM、C11 | OBC_DESIGN.md:136-151; CMakeLists.txt:19 | obc | 编译/运行 | - | 构建通过、内存不越界 | Executed Within 128kb | - | 高 | constraint-only(ST-031) | ISSUE-020 |
| REQ-062 | 约束 | MRD-025: 全部传输明文无加密 | MISSION_REQUIREMENTS.md:85 | obc, rf | 发射 | - | 帧可被业余台站解码 | - | - | 高 | constraint-only | 无 |
| REQ-063 | 约束 | MRD-002: 无地面接触自主运行 7 天 | MISSION_REQUIREMENTS.md:66 | obc | - | - | 7 天无人干预运行 | - | - | 高 | constraint-only | 无 |
| REQ-064 | 约束 | 组件热限 -20/+50°C 运行 | SYSTEM_REQUIREMENTS.md:251 | obc | - | - | 组件温度在限内 | - | - | 中 | constraint-only | ISSUE-014 |
| REQ-065 | 时间 | SYS-301: 维护任务时间 MET | SYSTEM_REQUIREMENTS.md:164; time_utils.c:19-32 | obc | 上电 | 时钟源/uptime | MET 单调递增 | - | GetData/Set | 中 | uncovered | ISSUE-026（飞行路径 TODO 返回 0） |
| REQ-066 | 载荷 | SYS-512: 信标文本 10s 内生成 | SYSTEM_REQUIREMENTS.md:236; ICD_OBC_JETSON.md:222-228 | obc, jetson | 请求 | - | 10s 内返回或超时回退 | Finished Within 10s | GetData | 高 | mapped | 无 |

## 覆盖统计

| 状态 | 数量 | REQ 列表 |
|---|---|---|
| mapped | 46 | REQ-001,003,004,005,006,007,008,009,010,013,014,015,016,017,019,020,021,022,023,024,025,027,028,029,030,031,033,034,036,037,038,039,040,041,042,043,045,046,047,048,050,051,053,054,055,066 |
| constraint-only | 10 | REQ-018,035,044,052,059,060,061,062,063,064 |
| uncovered | 9 | REQ-002,011,012,026,032,049,056,057,065 |
| conflict | 1 | REQ-058 |
| **合计** | **66** | |
