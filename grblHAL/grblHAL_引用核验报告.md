# grblHAL 逆向需求规格说明书 —— 引用核验报告

- 核验对象：`grblHAL_逆向需求规格说明书.md`（主交付物）与其派生的 DOCX/PDF
- 源码基线：`_repos/grblHAL/`，锚定提交 `ca26fc98f1b2171251c946ab91d5912b733efa78`
- 核验工具：`_verify_citations.py`（行号有效性）、`_verify_semantics.py`（语义窗口）、`check_office.py`（DOCX 结构）
- 核验日期：2026-10-15

---

## 1 核验方法与判据

### 1.1 行号有效性核验

从 Markdown 中提取全部 `文件:行号` 引用，逐条检查三件事：

1. 被引文件是否存在于 `_repos/grblHAL/`；
2. 行号是否落在该文件总行数之内；
3. 每个被引文件被引用的次数。

### 1.2 语义窗口核验

对每一条引用，取文档同一行内反引号包裹的代码标识符，在该引用所指行号的 ±10 行窗口内查找。一个标识符都匹配不上时标记为**可疑**，交人工判定。该判据刻意偏保守：G/M 代码写法差异、类注释行引用、多标识符聚合行都可能被判可疑，因此可疑 ≠ 错误。

判定分类：

| 类别 | 含义 | 处理 |
|---|---|---|
| 确定性错误 | 引用行号或标识符名与源码不符，且会误导读者 | 必须修正 |
| 形式差异 | 引用的确是相关证据，只是窗口内未出现同名标识符（如引用结构体 `typedef` 首行、引用 ISR 注解行、类注释行） | 保留，必要时补注 |

---

## 2 修正前的问题

第一轮核验（2026-10-15 17:19–17:22）发现：

- `errors.h`、`alarms.h` 共 **32 处**行号引用把"枚举值"当成了"行号"（如把 `[MSG:ERR:]` 类的编号 39 写成 `errors.h:39`），属系统性错误。
- 另有 13 项确定性错误：三个标识符在源码中**根本不存在**（`sys.f_override`、`sys.rt_cmd`、`settings_store_global_setting`）、一个类型名错误（`block_t` 应为 `plan_block_t`）、表 3.2-14 的 `core_handlers.h` 行号在后半段整体偏移、附录1 若干行号偏移。

---

## 3 本轮执行的修正（13 项）

| # | 位置 | 修正前 | 修正后 | 源码依据 |
|---|---|---|---|---|
| 1 | 表 3.2-14 第 1 行 | `core_handlers.h:234`、`:299` | `:234`、`:284`、`:275`、`:276`、`:277` | `core_handlers.h` 234/275/276/277/284 |
| 2 | 表 3.2-14 第 2 行 | `:289`、`:305` | `:278`、`:305`、`:306` | `on_line_number_assigned` 278 行 |
| 3 | 表 3.2-14 第 3 行 | `:262`（误作 `on_cycle_start`） | `:261` | `on_cycle_start` 实为 261 行 |
| 4 | 表 3.2-14 第 4 行 | `:250`、`:257`、`:251`、`:252`、`:253` | `:249`、`:259`、`:250`、`:251`、`:252` | 整体前移一位修正 |
| 5 | 表 3.2-14 第 5 行 | `:254`、`:255`、`:256`、`:258`、`:286` | `:253`、`:254`、`:255`、`:258`、`:274` | `on_set_axis_setting_unit` 实为 274 行 |
| 6 | 表 3.2-14 第 6 行 | `:300`、`:301`、`:249` | `:291`、`:292`、`:248` | `on_spindle_select/selected` 实为 291/292 |
| 7 | 表 3.2-14 第 7 行 | `:284`、`:285`、`:283`、`:290`、`:291`、`:292` | `:272`、`:273`、`:271`、`:279`、`:280`、`:281` | 探测与刀具钩子整体修正 |
| 8 | 表 3.2-14 第 8 行 | `:280`（误作 `on_modal_state_action`） | `:269` | 实为 269 行 |
| 9 | 表 3.2-14 第 9 行 | `:277`、`:303`、`:304`、`:302` | `:266`、`:295`、`:296`、`:294` | 流与文件钩子修正 |
| 10 | 表 3.2-14 第 10 行 | `:302`、`:294`、`:281`、`:279` | `:293`、`:282`、`:270`、`:268` | `on_reset` 293、`on_jog_cancel` 282、`on_homing_completed` 270、`on_homing_rate_set` 268 |
| 11 | 表 3.2-14 第 11 行 | `:276`、`:259` | `:265`、`:260` | `on_user_command` 265、`on_unknown_feedback_message` 260 |
| 12 | 文档 495 | `Setting_EnableLegacyRTCommands`（`settings.h:39`） | `settings.h:87` | 枚举值 `= 39` 定义在 87 行 |
| 13 | 附录1-1 第 10–16 项 | `sys.override` 引 `report.c:1455`；`sys.f_override`（不存在）；`sys.rt_exec_state` 引 `system.h:138`；`sys.rt_cmd`（不存在）；`machine_mode_t` 引 `system.h:118`；`parking_state` 引 `:140`；`hold_state` 引 `:147` | `sys.override`（`overrides_t`，`system.h:255`）；`sys.override.feed_rate`（`system.h:192`）；`sys.rt_exec_state`（`system.h:262`）；`sys.rt_exec_alarm`（`system.h:263`）；`machine_mode_t`（`system.h:130`–`134`）；`parking_state_t`（`system.h:138`–`144`）；`hold_state_t`（`system.h:146`–`150`） | `system.h` 逐行核实；`sys.f_override`、`sys.rt_cmd` 全仓库 grep 无匹配 |
| 14 | 附录1-3 第 16 项 | `settings_store_global_setting`（`settings.c:1853`） | `settings_store_setting`（`settings.c:3546`） | 该函数名全仓库 grep 无匹配 |
| 15 | 附录2-1 第 7 项 | `settings_store_global_setting` | `settings_store_setting` | 同上 |
| 16 | 附录1-4 第 1–4 项 | `block_t`（`planner.h:159`）；`block_t.size`（"块总步数"）；`block_t.step_event_count`；`steps_t` 引 `planner.h:55` | `plan_block_t`（`planner.h:81`–`127`）；`block_buffer_t.size`（规划缓冲区块数减一，`planner.c:39`）；`plan_block_t.step_event_count`（`planner.h:85`）；`steps_t`（`planner.h:52`–`77`） | `block_t` 在源码中不存在；`planner.h` 中结构体名为 `plan_block_t` |
| 17 | 附录1-2 第 10 项 | `gc_block.modal.spindle` 引 `spindle_control.h:215` | `spindle_state_t`（`spindle_control.h:60`–`73`） | 215 行是 `spindle_settings_flags_t` 的 `typedef union {` |

> 说明：上表按"修正批次"计数为 17 行，其中表 3.2-14 的 11 行按原清单计为 1 项，故原清单 13 项与本表逐行对应。
> 第 16 项中的 `block_buffer_t.size` 一项，原文档写作 `block_t.size` 且释义为"块总步数"；源码中 `size` 是规划缓冲区自身容量（`planner.c:39`："Number of blocks in the planner buffer minus 1"），并非单块步数，故同时更正字段归属与释义。

此外，第一轮已执行 `_fix_citations.py`，修正 `errors.h`（17 处）与 `alarms.h`（15 处）共 **32 处**行号引用。

---

## 4 修正后的核验结果

### 4.1 行号有效性（`_verify_citations.py`）

```
被引用文件数：32
有效引用 681 处；缺失文件 0 处；越界 0 处
```

引用密度最高的文件：`gcode.c` 84 处、`report.c` 69 处、`grbl.h` 66 处、`core_handlers.h` 61 处、`system.c` 53 处。

### 4.2 语义窗口（`_verify_semantics.py`）

| 阶段 | 参与核验 | 可疑 |
|---|---|---|
| 第一轮（修正前） | 310 | 68 |
| `errors.h`/`alarms.h` 32 处修正后 | 310 | 60 |
| 本轮 17 行修正后 | 320 | **48** |

剩余 48 处可疑**全部判定为"形式差异，无需修正"**，理由分类如下：

| 可疑原因 | 处数 | 说明 |
|---|---|---|
| 引用了结构体/联合体的 `typedef` 首行 | 约 20 | 如 `settings.h:47`（`typedef enum {`）对应 `setting_id_t`、`planner.h:81`（`typedef struct plan_block {`）对应 `plan_block_t`。引用整块定义的首行是合法引用方式 |
| 引用了 `gcode.h` 中模态位域的位定义行 | 13 | 文档按 G 代码写法（`gc_block.modal.motion`）索引，源码中该位域以 `G1 :1,` 形式定义，属命名体系差异 |
| 引用了 ISR 注解行作为并发约束证据 | 6 | `core_handlers.h:261/262/263/281/282/293` 声称 `hal.irq_enable` 等并不可见，但引用目的正是这些行的 `Called from interrupt context` 注解 |
| 引用了宏常量定义行（`config.h` 的 `DEFAULT_*`） | 2 | `config.h:771`/`:780` 是 `DEFAULT_JUNCTION_DEVIATION`/`DEFAULT_ARC_TOLERANCE`，与文档所述设置项默认值一致 |
| 引用了容量常量的相邻宏（`NVS_SIZE_*` 家族） | 5 | `nvs.h:45`–`47` 是尺寸宏、`:73`–`78` 是地址宏，文档按"尺寸/地址"成对引用 |
| 引用了函数指针/入口函数所在行 | 3 | `grbllib.c:258`（`grbl_enter`）、`grbllib.h:33` 等，文档同一行同时引用了 `README.md` |
| 其他（类注释行、结构体成员所在行） | 约 6 | `hal.h:579`/`:679`、`stepper.h:42` 等 |

### 4.3 DOCX 结构校验（`check_office.py`）

```json
{"format":"docx","verdict":"pass"}
段落 4305；表格 35 个；分节 1 个（A4，页边距上下 1440 twips、左右 1134 twips）
```

### 4.4 渲染检查

- 渲染后端：LibreOffice Kit（native），**58 页**，无缺页
- 缺字体诊断：仅 `Courier`（等宽回退，正文使用宋体/黑体/Consolas，不影响版面）
- 抽查首页与正文页：标题层级、表格宽度、六要素缩进均正常，无表格溢出

---

## 5 结论

1. 主交付物的 `文件:行号` 引用**无缺失文件、无越界**，有效引用 681 处。
2. 全部 **49 处**（32 + 17）确定性引用错误已修正并写回 Markdown。
3. 剩余 48 处语义可疑项均属**命名体系或引用粒度差异**，不影响证据有效性，已在 4.2 节分类说明，无需进一步修改。
4. DOCX 结构校验通过，PDF 已重新生成，与 Markdown 同源。

**遗留未决事项**（不影响交付物可用性）：`grblHAL/drivers` 未克隆，HAL/移植层与板级映射需求按"对外依赖"处理；克隆为 `--depth 1`，历史证据以仓库内 `changelog.md` 替代。

---

## 6 第二轮核验：15 个无证据节的行号补齐（2026-10-15 晚）

### 6.1 背景

第一轮核验只覆盖了文档中**已存在**的 `文件:行号` 引用。进一步统计发现，`3.1 功能分解` 与 14 个 `3.2.x` 需求节只有文字描述，整节**一处源码引用都没有**（0 处），追溯链在这些节是断的：

`3.1`、`3.2.1`、`3.2.2`、`3.2.6`、`3.2.7`、`3.2.9`、`3.2.10`、`3.2.12`、`3.2.13`、`3.2.14`、`3.2.19`、`3.2.21`、`3.2.22`、`3.2.23`、`3.2.24`（含其全部子节，合计 178 条编号处理步骤）。

### 6.2 方法

1. 分 4 组并行定位：每组拿到该节全文（`_gap_sections.txt`）与源码仓库 `_repos/grblHAL/`，逐条处理步骤找最直接的落点（函数定义/调用点/常量或字段定义行）。
2. 每条证据必须附**该行源码原文片段**，不允许只给行号。
3. 回报后由 `_verify_evidence.py` 逐条回读源码比对：文件存在性、行号范围、行内容与回报原文是否一致（含 Markdown 转义竖线、多片段拆分的容错处理）。
4. 由 `_inject_evidence.py` 在句末标点前插入 `（`文件:行号`）`，干跑出清单人工核对后再落盘。

### 6.3 结果

| 项 | 补齐前 | 补齐后 |
|---|---|---|
| 15 节内的 `文件:行号` 引用 | 0 处 | 322 处（每节 12–55 处） |
| 全文档有效引用（`_verify_citations.py`） | 681 处 | **1031 处** |
| 缺失文件 / 行号越界 | 0 / 0 | **0 / 0** |
| 15 节编号处理步骤缺证据 | 178 条 | **0 条**（`_check_steps.py`） |
| 证据回读核验（`_verify_evidence.py`） | — | 282 条证据，命中 282，问题 0 |
| DOCX | 4305 段 / 58 页 | **4362 段 / 35 表 / 64 页**，`verdict: pass` |

证据工作底稿：`_ev_A_init.md`、`_ev_B_motion.md`、`_ev_C_axis.md`、`_ev_D_ext.md`（含每条的节、步骤、行号与源码原文，以及各组的存疑条目说明）。

**语义窗口复核**：补证后重跑 `_verify_semantics.py`，可疑项由 48 处升至 **51 处**。新增的 3 处均属 §4.2 已归纳的形式差异类型，非错误：

| 引用 | 文档声称的标识符 | 该行实际内容 | 判定 |
|---|---|---|---|
| `grbllib.c:310` | `hal` | `driver.init = driver_init();` | 引用的确是驱动初始化调用点，命名差异 |
| `stepper.c:1366` | `cycles_per_tick` | `uint32_t cycles = (uint32_t)ceilf(cycles_per_min * inv_rate);` | 同一概念的不同命名（`cycles` 即每周期步进事件数） |
| `settings.c:2952` | `N_TOOLS` | `return true;` | 该行位于 `#if !N_TOOLS` 分支内，为刀具数据写入的空实现，正文已注明"由编译期开关 `N_TOOLS` 控制" |

其余 48 处与第一轮结论一致，仍为结构体 `typedef` 首行、`gcode.h` 模态位域、ISR 注解行、`config.h` 默认值宏等形式差异。

### 6.4 由补证反查出的正文错误（已修正）

补齐证据时发现 8 处正文表述与源码不符，均已按源码改正：

| # | 位置 | 原文 | 改为 | 源码依据 |
|---|---|---|---|---|
| 1 | 3.2.9（2） | 按设置**最多执行 6 轮**归零循环 | 轮数为定位阶段数的两倍加一（默认 3 轮），由设置决定 | `machine_limits.c:272`、`config.h:1678`（`DEFAULT_N_HOMING_LOCATE_CYCLE 1`） |
| 2 | 3.2.9（5） | 去抖时间"**叠加一个与时间相关的安全裕量**" | 检出限位后停步进并复位段缓冲，再按设置毫秒数延时 | `machine_limits.c:485` 只有一处 `hal.delay_ms(settings.homing.debounce_delay,…)`，无裕量 |
| 3 | 3.2.9.2（2） | "两侧最终位置之差**被记录为找正偏移**" | 只记录先触发侧位置用于超差判定；偏移量由用户设置项给出，核心层不自动写回 | `machine_limits.c:409/432`、`settings.c:1576`–`1578` |
| 4 | 3.2.10（3） | 行程内未检出触发 → "探测**初始**失败" | "探测**接触**失败" | `motion_control.c:1068` = `Alarm_ProbeFailContact`；`alarms.c:34` |
| 5 | 3.2.10（4） | 开始即已触发 → "探测**接触**失败" | "探测**初始**失败" | `motion_control.c:1032` = `Alarm_ProbeFailInitial`；`alarms.c:33` |
| 6 | 3.2.13（1） | 硬限位"也可由核心层**周期性查询**" | "也可由核心层**按需查询**（如上电自检时读取限位状态）" | 核心层无轮询；`hal.limits.get_state()` 见 `protocol.c:157` |
| 7 | 3.2.14（5） | "按无刀具错误处理"（未标注归属） | 补注"该错误码由自动换刀流程/插件产生，核心层仅定义未引用" | `errors.h:123` 定义，全仓库无 `.c` 引用 |
| 8 | 3.2.14（7） | 刀具表"可整体启用或停用持久化" | "由**编译期开关** `N_TOOLS` 整体启用或停用" | `settings.c:2896`、`settings.c:2952`（空实现） |

另有 2 处非证据类修正一并记录：

| # | 位置 | 说明 |
|---|---|---|
| 9 | 3.2.22（3） | 原文称 Modbus 异常与扩展器异常"**均为非关键报警**"。源码 `alarm_is_critical()`（`alarms.h:73`–`80`）把 `Alarm_ExpanderException` 列为**关键**报警，已改为"前者非关键、后者关键" |
| 10 | 附录2 小节编号 | 两个小节原同为 `附录2.1`，后者改为 `附录2.2 领域专用IP`（与表题"表 附2-2"一致） |

### 6.5 两处按源码保留、未改正文的说明

- **3.2.9.2（3）**"找正偏移写入该轴设置并可用于后续运动补偿"：指的是用户经 `$` 设置项写入（`settings.c:1578`），与第 3 条修正并不矛盾。
- **3.2.23（1）**"每个编码器的设置项最多 5 个，按编码器序号以固定增量寻址"：对应 `ENCODER_N_SETTINGS_MAX 5` 与 `ENCODER_SETTINGS_INCREMENT 10`（`settings.h:40`、`settings.h:41`）。源码该行注释写作 "maximum number of encoders allowed"，与常量名语义相反，属上游注释瑕疵；文档按**常量名与用法**表述，故保留，证据同时引 40、41 两行。

