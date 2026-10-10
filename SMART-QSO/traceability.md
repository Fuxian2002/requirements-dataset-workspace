# SMART-QSO 追踪矩阵

> 四列: 来源证据 → REQ-ID → Statement ID/约束 → code.rdl 位置 → 状态。
> 每个正式需求至少出现一次；未映射的 REQ 必须带 ISSUE-ID。
> code.rdl 位置以行号为准（spacerdl/code.rdl，生成时版本）。

## 1. 文档/代码 → 需求 → 语句 正向追踪

### docs/requirements/MISSION_REQUIREMENTS.md（MRD）

| 来源证据 | REQ-ID | Statement ID / 约束 | code.rdl 位置 | 状态 |
|---|---|---|---|---|
| MRD-020 (:79) | REQ-033 | ST-020 | AppTask BeaconCycle | mapped |
| MRD-021 (:80) | REQ-036 | ST-020 | AppTask BeaconCycle (ProTable.B1 能力) | mapped |
| MRD-025 (:85) | REQ-062 | 约束注释 | SystemConstraints | constraint-only |
| MRD-030-034 (:90-96) | REQ-033,039,040 | ST-020/022/024 | AppTask | mapped |
| MRD-041 (:101) | REQ-055 | ST-015 | AppTask Compute PowerForecast | mapped(中) |
| MRD-042 (:102) | REQ-057 | - (ISSUE-032) | 无 | uncovered |
| MRD-043 (:103) | REQ-056 | - (ISSUE-031) | 无 | uncovered |
| MRD-002 (:66) | REQ-063 | 约束注释 | SystemConstraints | constraint-only |
| MRD-060 (:113) | REQ-028,029 | ST-011/013 | AppTask | mapped（7 天 vs 1 轨 ISSUE-018） |

### docs/requirements/SYSTEM_REQUIREMENTS.md（SYS）

| 来源证据 | REQ-ID | Statement ID / 约束 | code.rdl 位置 | 状态 |
|---|---|---|---|---|
| SYS-021 (:76) | REQ-005,048 | ST-003/029 | InitTask/InterruptTask | mapped(ISSUE-013) |
| SYS-023 (:77) | REQ-051 | ST-018 | AppTask | mapped |
| SYS-124 (:118) | REQ-013 | ST-006 | AppTask | mapped |
| SYS-200-204 (:131-134) | REQ-037,038 | ST-026 / ProTable.B1 | AppTask Case(SET_TX_POWER) | mapped(ISSUE-006/007) |
| SYS-210 (:139) | REQ-034 | ST-020 | AppTask BeaconCycle | mapped |
| SYS-211 (:140) | REQ-033 | ST-020/025(Case) | AppTask | mapped(ISSUE-008) |
| SYS-212 (:141) | REQ-035 | 约束 (ISSUE-010) | ProTable.B1 注释 | constraint-only |
| SYS-213 (:142) | REQ-036 | ST-020 | AppTask | mapped |
| SYS-214/215 (:143-144) | REQ-039,025 | ST-022 | AppTask | mapped |
| SYS-220/221 (:150-151) | REQ-009,007 | ST-027/023/030 | AppTask/InterruptTask | mapped |
| SYS-300 (:163) | REQ-001 | ST-001 | InitTask | mapped |
| SYS-301 (:164) | REQ-065 | - (ISSUE-026) | 无 | uncovered |
| SYS-303 (:165) | REQ-052 | 约束 (ISSUE-002) | - | constraint-only |
| SYS-305 (:166) | REQ-045,047,050 | ST-016 | AppTask HealthCheck | mapped |
| SYS-310-313 (:172-176) | REQ-051,046 | ST-018/017 | AppTask/InitTask | mapped(ISSUE-039) |
| SYS-320-324 (:183-187) | REQ-004 | ST-002 | InitTask | mapped(ISSUE-004) |
| SYS-400-403 (:197-202) | REQ-027 | ST-007 | AppTask | mapped |
| SYS-410-412 (:200-201) | REQ-031 | ST-014 | AppTask | mapped |
| SYS-420-422 (:208-210) | REQ-028,029,030 | ST-011/012/013 | AppTask | mapped |
| SYS-500-504 (:224-227) | REQ-020 | ST-010 | AppTask | mapped |
| SYS-510-514 (:235-238) | REQ-022,023,024 | ST-019/021 | AppTask | mapped |
| SYS-520-523 (:240-242) | REQ-025,026 | ST-022 / -(ISSUE-028) | AppTask | mapped/uncovered |
| SYS-600-603 (:251-253) | REQ-064 | 约束 (ISSUE-014) | SystemConstraints 注释 | constraint-only |
| SYS-800-802 (:287-289) | REQ-053 | ST-028 | AppTask | mapped |
| SYS-001-005,010-013,100-123 等物理/环境类 | - | 超出 SpaceRDL 范围（无软件可观察动作），见 README 范围说明 | - | 范围外 |

### docs/requirements/REQUIREMENTS_TRACEABILITY.md（RTM/SRS）

| 来源证据 | REQ-ID | Statement ID / 约束 | code.rdl 位置 | 状态 |
|---|---|---|---|---|
| SRS-F001 (:123) | REQ-001 | ST-001 | InitTask | mapped |
| SRS-F002 (:122) | REQ-003 | ST-004 | InitTask | mapped |
| SRS-F003-005 (:124-127) | REQ-002 | - (ISSUE-025) | 无 | uncovered |
| SRS-F010-017 (:128-135) | REQ-013,014,015,017,019 | ST-006/008/009/018 | AppTask | mapped |
| SRS-F020-025 (:136-141) | REQ-034,033,039,025,024 | ST-020/022 | AppTask | mapped |
| SRS-F030-035 (:142-147) | REQ-022,023,026 | ST-019/021/-(ISSUE-028) | AppTask | mapped/uncovered |
| SRS-F040-045 (:148-153) | REQ-045,046,047,050 | ST-016/017 | AppTask | mapped |
| SRS-F050-052 (:154-156) | REQ-048 | ST-029 | InterruptTask | mapped |
| SRS-F060-063 (:158-161) | REQ-051 | ST-018 | AppTask | mapped |
| SRS-F070-073 (:162-164) | REQ-013,036 | ST-006/020 | AppTask | mapped |
| SRS-P002 (:171) | REQ-033 | ST-020 Finished Within 5s | AppTask | mapped |
| SRS-S001 (:212) | REQ-007 | ST-023/030 | AppTask/InterruptTask | mapped |

### 软件代码（software/flight）

| 来源证据 | REQ-ID | Statement ID / 约束 | code.rdl 位置 | 状态 |
|---|---|---|---|---|
| main.c:95-171 init_system | REQ-001 | ST-001 | InitTask | mapped |
| main.c:37-46 循环节拍/健康检查/持久化 | REQ-045,051 | ST-016/018 | AppTask | mapped(ISSUE-015) |
| main.c:211-241 SOC 分级与恢复 | REQ-014-016 | ST-008 | AppTask | mapped |
| main.c:304-379 send_telemetry_to_jetson | REQ-022 | ST-019 | AppTask | mapped |
| eps_control.c:86-117,178-207 | REQ-020,021,017 | ST-010/009 | AppTask | mapped |
| eps_control.h:32-38 功率限 0.5/1.5/3.0W | REQ-018 | 约束（功率限值，SystemConstraints 注释级） | - | constraint-only |
| adcs_control.c:401-472 | REQ-028,030 | ST-011/012 | AppTask | mapped |
| beacon.c:131-156,220-264,442-464 | REQ-025,034,024 | ST-022/020/021(能力) | AppTask | mapped |
| beacon.h:39-45; system_state.c:413-423 | REQ-033 | ST-020/025 | AppTask | mapped(ISSUE-008) |
| deployment.c:117-208; deployment.h:33-48 | REQ-008,009,010,007 | ST-027/030 | AppTask/InterruptTask | mapped(ISSUE-025) |
| cmd_handler.c:223-258,260-290 | REQ-042,043 | ST-025 | AppTask | mapped(ISSUE-001) |
| fault_mgmt.c:75-80,156,208-233 | REQ-046,050,047 | ST-017/016 | AppTask | mapped |
| watchdog_mgr.c:86-111,167-183 | REQ-049,048 | -(ISSUE-038)/ST-029 | InterruptTask | uncovered/mapped |
| time_utils.c:19-32 | REQ-065 | - (ISSUE-026) | 无 | uncovered |
| 未接线模块群 (scheduler/telemetry/system_init/state_machine…) | REQ-002,011,012 | - (ISSUE-025) | 无 | uncovered |

### 接口文档（docs/interfaces）

| 来源证据 | REQ-ID | Statement ID / 约束 | code.rdl 位置 | 状态 |
|---|---|---|---|---|
| ICD_OBC_EPS.md:76-156,275-328 | REQ-013,017 | ST-006/009 | AppTask | mapped(ISSUE-004/005) |
| ICD_OBC_RF.md:41,106-160 | REQ-037,038 | ST-026/ProTable.B1 | AppTask | mapped(ISSUE-006) |
| ICD_OBC_ADCS.md:124-189,244-325 | REQ-027-031 | ST-007/011-014 | AppTask | mapped |
| ICD_OBC_JETSON.md:89-110,121-134,160-171,222-265 | REQ-020,022,023,026 | ST-010/019/021 | AppTask | mapped/uncovered |
| ICD_BEACON_FORMAT.md:39-45,93-153 | REQ-034,036 | ST-020 | AppTask | mapped(ISSUE-009) |
| ICD_SPACE_GROUND.md:63-83,167-197 | REQ-040,041,037 | ST-024/026 | AppTask | mapped(ISSUE-001/003) |

### 运维文档（docs/operations）

| 来源证据 | REQ-ID | Statement ID / 约束 | code.rdl 位置 | 状态 |
|---|---|---|---|---|
| COMMAND_DICTIONARY.md:17-56,71-370,408-431 | REQ-040-044 | ST-024/025 | AppTask | mapped(ISSUE-001) |
| MISSION_RULES.md:86-131 FC-001~005 | REQ-059,060,037,048,064 | 约束注释 | SystemConstraints | constraint-only |
| COMMISSIONING_PLAN.md:50-87 | REQ-006,007,009 | ST-005/023/027/030 | InitTask/AppTask/InterruptTask | mapped |
| END_OF_LIFE_PLAN.md:37-39,72-106 | REQ-053,054 | ST-028 | AppTask | mapped |
| MISSION_OPERATIONS_PLAN.md:148-152 | REQ-033 | ST-020 | AppTask | mapped(ISSUE-008) |

### 设计/硬件文档（docs/pdr、docs/hardware、docs/ML_MODELS、docs/BEACON_SPEC）

| 来源证据 | REQ-ID | Statement ID / 约束 | code.rdl 位置 | 状态 |
|---|---|---|---|---|
| PDR.md:96-97,105-111 | REQ-055,024,066 | ST-015/021 | AppTask | mapped(中) |
| PDR.md:27 vs :114-115 | REQ-058 | - (ISSUE-034) | 无 | conflict |
| ML_MODELS.md:3,17-51 | REQ-055,023,024 | ST-015/021(RES-013) | AppTask | mapped(中,ISSUE-033) |
| BEACON_SPEC.md:8-11,21-66 | REQ-038,033,024 | ProTable.B1/ST-020/021 | AppTask | mapped(ISSUE-008/017) |
| ADCS_DESIGN.md:208-265 | REQ-028,030 | ST-011/012 (FormulaTable.B1/B2) | AppTask | mapped |
| OBC_DESIGN.md:73-79,136-183,331-335 | REQ-004,061,005 | ST-002/031/003 | InitTask/SystemConstraints | mapped(ISSUE-020) |
| POWER_BUDGET_ANALYSIS.md:226-259 | REQ-060 | 约束注释 | SystemConstraints | constraint-only(ISSUE-016) |

## 2. 未使用资源（资源目录中有、无需求引用）

| RES-ID | 说明 |
|---|---|
| RES-013 TinyLMBeacon | 载荷侧算法，作为 jetson 资源能力被 REQ-023/024/066 引用（能力型引用，非 OBC 算子），不算未使用 |
| （其余 RES-001~016 均至少被一个 REQ 引用） | 无未使用资源 |

## 3. 需求覆盖缺口总览

| REQ | 缺口性质 | 阻塞级别 | ISSUE |
|---|---|---|---|
| REQ-002,011,012,049 | 模块存在但未接入 main.c 执行路径 | 高 | ISSUE-025,037,038 |
| REQ-026,032 | 设计文档有方案、代码无实现 | 中 | ISSUE-028,027 |
| REQ-056,057 | 需求存在、模型/公式/算法缺失 | 中 | ISSUE-031,032 |
| REQ-058 | 两处原文直接矛盾 | 高 | ISSUE-034 |
| REQ-065 | 飞行路径时间源 TODO 未实现 | 中 | ISSUE-026 |
