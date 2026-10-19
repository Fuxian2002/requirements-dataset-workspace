# 82条需求的当前追踪表

各条需求均列出当前保留片段、已剔除候选与剩余义务。不以有片段等同于全需求完成；requirements.json旧链接原样留作历史审查。当前全量状态blocked。

## REQ-LC-0001 — LC1000

接受 No-Op 地面命令后，有效命令计数加一并发送说明 LC 存活的事件。

当前保留数据片段：

- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0535](statements.md#st-lc-0535) Compute；code.rdl L343

已剔除的软件接口候选：ST-LC-0501 (SendData), ST-LC-0534 (ProTC)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0002 — LC1001

接受 Reset 命令后，把六项 housekeeping 计数清零。

当前保留数据片段：

- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0108](statements.md#st-lc-0108) Compute；code.rdl L443, L471
- [ST-LC-0109](statements.md#st-lc-0109) Compute；code.rdl L445
- [ST-LC-0537](statements.md#st-lc-0537) Compute；code.rdl L451

已剔除的软件接口候选：ST-LC-0501 (SendData), ST-LC-0536 (ProTC)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
  "LC1001清零最终ValidCommandCounter与LC1003所有有效命令加一相冲突；实现Reset不加一。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0003 — LC1002

所有 LC 命令头声明长度与预期长度不等时，拒绝执行并发送错误事件。

当前保留数据片段：

- [ST-LC-0100](statements.md#st-lc-0100) Compute；code.rdl L165, L188, L347, L384, L455, L486, L547, L845, L928
- [ST-LC-0101](statements.md#st-lc-0101) Compute；code.rdl L163, L186, L345, L382, L453, L484, L545, L843, L926
- [ST-LC-0102](statements.md#st-lc-0102) Compute；code.rdl L171, L194, L353, L390, L413, L421, L461, L492, L529, L553, L851, L894, L902, L910, L934, L954
- [ST-LC-0103](statements.md#st-lc-0103) Compute；code.rdl L174, L197, L356, L393, L415, L423, L464, L495, L531, L556, L854, L896, L904, L912, L937, L956
- [ST-LC-0104](statements.md#st-lc-0104) Compute；code.rdl L169, L192, L351, L388, L417, L425, L459, L490, L533, L551, L849, L898, L906, L914, L932, L958
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961

已剔除的软件接口候选：ST-LC-0500 (SendData)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0004 — LC1003

接受任何有效地面命令，应执行命令、有效命令计数加一并发事件；调度器内部请求不在此计数范围。

当前保留数据片段：

- [ST-LC-0101](statements.md#st-lc-0101) Compute；code.rdl L163, L186, L345, L382, L453, L484, L545, L843, L926
- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0108](statements.md#st-lc-0108) Compute；code.rdl L443, L471
- [ST-LC-0109](statements.md#st-lc-0109) Compute；code.rdl L445
- [ST-LC-0120](statements.md#st-lc-0120) Compute；code.rdl L886

已剔除的软件接口候选：ST-LC-0501 (SendData)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0005 — LC1004

拒绝 LC 地面命令时，停止该命令执行、拒绝计数加一并发错误事件。

当前保留数据片段：

- [ST-LC-0100](statements.md#st-lc-0100) Compute；code.rdl L165, L188, L347, L384, L455, L486, L547, L845, L928
- [ST-LC-0101](statements.md#st-lc-0101) Compute；code.rdl L163, L186, L345, L382, L453, L484, L545, L843, L926
- [ST-LC-0102](statements.md#st-lc-0102) Compute；code.rdl L171, L194, L353, L390, L413, L421, L461, L492, L529, L553, L851, L894, L902, L910, L934, L954
- [ST-LC-0103](statements.md#st-lc-0103) Compute；code.rdl L174, L197, L356, L393, L415, L423, L464, L495, L531, L556, L854, L896, L904, L912, L937, L956
- [ST-LC-0104](statements.md#st-lc-0104) Compute；code.rdl L169, L192, L351, L388, L417, L425, L459, L490, L533, L551, L849, L898, L906, L914, L932, L958
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0110](statements.md#st-lc-0110) Compute；code.rdl L944
- [ST-LC-0112](statements.md#st-lc-0112) Compute；code.rdl L861
- [ST-LC-0113](statements.md#st-lc-0113) Compute；code.rdl L833, L864
- [ST-LC-0114](statements.md#st-lc-0114) Compute；code.rdl L866
- [ST-LC-0118](statements.md#st-lc-0118) Compute；code.rdl L878
- [ST-LC-0120](statements.md#st-lc-0120) Compute；code.rdl L886
- [ST-LC-0122](statements.md#st-lc-0122) Compute；code.rdl L400
- [ST-LC-0123](statements.md#st-lc-0123) Compute；code.rdl L403
- [ST-LC-0126](statements.md#st-lc-0126) Compute；code.rdl L502
- [ST-LC-0127](statements.md#st-lc-0127) Compute；code.rdl L504

已剔除的软件接口候选：ST-LC-0500 (SendData)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0006 — LC2000

最多监测平台定义数量的 Watchpoint；平台值是容量，不是采样周期。

当前保留数据片段：

- [ST-LC-0200](statements.md#st-lc-0200) Set；code.rdl L1112
- [ST-LC-0203](statements.md#st-lc-0203) Compute；code.rdl L1119
- [ST-LC-0206](statements.md#st-lc-0206) Compute；code.rdl L1124, L1203
- [ST-LC-0231](statements.md#st-lc-0231) Compute；code.rdl L1201
- [ST-LC-0236](statements.md#st-lc-0236) Set；code.rdl L1229
- [ST-LC-0237](statements.md#st-lc-0237) Compute；code.rdl L1231
- [ST-LC-0238](statements.md#st-lc-0238) Compute；code.rdl L1233, L1271
- [ST-LC-0251](statements.md#st-lc-0251) Compute；code.rdl L1269
- [ST-LC-0252](statements.md#st-lc-0252) Compute；code.rdl L1274
- [ST-LC-0255](statements.md#st-lc-0255) Compute；code.rdl L793, L1047
- [ST-LC-0256](statements.md#st-lc-0256) Compute；code.rdl L795, L814, L1049, L1068
- [ST-LC-0262](statements.md#st-lc-0262) Compute；code.rdl L812, L1066
- [ST-LC-0553](statements.md#st-lc-0553) Compute；code.rdl L1227

已剔除的软件接口候选：ST-LC-0510 (SendData), ST-LC-0552 (GetData)

剩余义务（保留原审查）：

```json
[
  "部署平台值、活动目录、ABI/cFE资源加载pending-interface；不造固定周期。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0007 — LC2001

WDT 每个 Watchpoint 有一个决定何时变为 STALE 的 age 参数。

当前保留数据片段：

- [ST-LC-0200](statements.md#st-lc-0200) Set；code.rdl L1112
- [ST-LC-0213](statements.md#st-lc-0213) Set；code.rdl L1186, L1198
- [ST-LC-0224](statements.md#st-lc-0224) Compute；code.rdl L1160
- [ST-LC-0226](statements.md#st-lc-0226) Compute；code.rdl L1166
- [ST-LC-0227](statements.md#st-lc-0227) Compute；code.rdl L1169
- [ST-LC-0230](statements.md#st-lc-0230) Set；code.rdl L1179
- [ST-LC-0253](statements.md#st-lc-0253) Set；code.rdl L788, L1042
- [ST-LC-0254](statements.md#st-lc-0254) Compute；code.rdl L790, L1044
- [ST-LC-0255](statements.md#st-lc-0255) Compute；code.rdl L793, L1047
- [ST-LC-0256](statements.md#st-lc-0256) Compute；code.rdl L795, L814, L1049, L1068
- [ST-LC-0257](statements.md#st-lc-0257) Compute；code.rdl L798, L1052
- [ST-LC-0258](statements.md#st-lc-0258) Compute；code.rdl L800, L1054
- [ST-LC-0259](statements.md#st-lc-0259) Set；code.rdl L803, L1057
- [ST-LC-0260](statements.md#st-lc-0260) Compute；code.rdl L805, L1059
- [ST-LC-0261](statements.md#st-lc-0261) Set；code.rdl L808, L1062
- [ST-LC-0262](statements.md#st-lc-0262) Compute；code.rdl L812, L1066

已剔除的软件接口候选：无直接关联；仍有系统入口/资源绑定缺口

剩余义务（保留原审查）：

```json
[
  "正式未给墙钟单位，不补秒/毫秒；真实UpdateAge节奏、部署值和接口pending。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0008 — LC2002

每个 WDT Watchpoint 的数据 age 应被维护。

当前保留数据片段：

- [ST-LC-0200](statements.md#st-lc-0200) Set；code.rdl L1112
- [ST-LC-0211](statements.md#st-lc-0211) Compute；code.rdl L1182, L1194
- [ST-LC-0212](statements.md#st-lc-0212) Set；code.rdl L1184, L1196
- [ST-LC-0213](statements.md#st-lc-0213) Set；code.rdl L1186, L1198
- [ST-LC-0224](statements.md#st-lc-0224) Compute；code.rdl L1160
- [ST-LC-0226](statements.md#st-lc-0226) Compute；code.rdl L1166
- [ST-LC-0227](statements.md#st-lc-0227) Compute；code.rdl L1169
- [ST-LC-0230](statements.md#st-lc-0230) Set；code.rdl L1179
- [ST-LC-0253](statements.md#st-lc-0253) Set；code.rdl L788, L1042
- [ST-LC-0254](statements.md#st-lc-0254) Compute；code.rdl L790, L1044
- [ST-LC-0255](statements.md#st-lc-0255) Compute；code.rdl L793, L1047
- [ST-LC-0256](statements.md#st-lc-0256) Compute；code.rdl L795, L814, L1049, L1068
- [ST-LC-0257](statements.md#st-lc-0257) Compute；code.rdl L798, L1052
- [ST-LC-0258](statements.md#st-lc-0258) Compute；code.rdl L800, L1054
- [ST-LC-0259](statements.md#st-lc-0259) Set；code.rdl L803, L1057
- [ST-LC-0260](statements.md#st-lc-0260) Compute；code.rdl L805, L1059
- [ST-LC-0261](statements.md#st-lc-0261) Set；code.rdl L808, L1062
- [ST-LC-0262](statements.md#st-lc-0262) Compute；code.rdl L812, L1066

已剔除的软件接口候选：ST-LC-0506 (SendData)

剩余义务（保留原审查）：

```json
[
  "age是同次请求续段，不是新入口；原子字段/服务及类型加载pending。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0009 — LC2003

应用 ACTIVE/PASSIVE 时，相关消息到达立即触发 WDT 所列数据点比较。

当前保留数据片段：

- [ST-LC-0200](statements.md#st-lc-0200) Set；code.rdl L1112
- [ST-LC-0201](statements.md#st-lc-0201) Compute；code.rdl L1114
- [ST-LC-0202](statements.md#st-lc-0202) Compute；code.rdl L1117
- [ST-LC-0203](statements.md#st-lc-0203) Compute；code.rdl L1119
- [ST-LC-0204](statements.md#st-lc-0204) Compute；code.rdl L1121
- [ST-LC-0205](statements.md#st-lc-0205) Compute；code.rdl L1217
- [ST-LC-0206](statements.md#st-lc-0206) Compute；code.rdl L1124, L1203
- [ST-LC-0207](statements.md#st-lc-0207) Compute；code.rdl L1127
- [ST-LC-0208](statements.md#st-lc-0208) Compute；code.rdl L1129
- [ST-LC-0209](statements.md#st-lc-0209) Compute；code.rdl L1132
- [ST-LC-0210](statements.md#st-lc-0210) Compute；code.rdl L1190
- [ST-LC-0214](statements.md#st-lc-0214) Compute；code.rdl L1135
- [ST-LC-0216](statements.md#st-lc-0216) Compute；code.rdl L1140
- [ST-LC-0217](statements.md#st-lc-0217) Compute；code.rdl L1142
- [ST-LC-0218](statements.md#st-lc-0218) Compute；code.rdl L1145
- [ST-LC-0219](statements.md#st-lc-0219) Compute；code.rdl L1148
- [ST-LC-0220](statements.md#st-lc-0220) Set；code.rdl L1151
- [ST-LC-0230](statements.md#st-lc-0230) Set；code.rdl L1179
- [ST-LC-0231](statements.md#st-lc-0231) Compute；code.rdl L1201
- [ST-LC-0232](statements.md#st-lc-0232) Compute；code.rdl L1206
- [ST-LC-0233](statements.md#st-lc-0233) Compute；code.rdl L1209
- [ST-LC-0234](statements.md#st-lc-0234) Set；code.rdl L1211
- [ST-LC-0235](statements.md#st-lc-0235) Compute；code.rdl L1214, L1219
- [ST-LC-0263](statements.md#st-lc-0263) Compute；code.rdl L1092
- [ST-LC-0529](statements.md#st-lc-0529) Compute；code.rdl L1110

已剔除的软件接口候选：ST-LC-0505 (SendData), ST-LC-0507 (SendData), ST-LC-0508 (SendData), ST-LC-0528 (GetData)

剩余义务（保留原审查）：

```json
[
  "真实SB/EVS入口与持久资源绑定pending-interface，非EDS路由部署待确认；风险不改成安全拒绝。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0010 — LC2003.1

Watchpoint 支持 =、!=、>、>=、<、<= 六种关系比较。

当前保留数据片段：

- [ST-LC-0200](statements.md#st-lc-0200) Set；code.rdl L1112
- [ST-LC-0216](statements.md#st-lc-0216) Compute；code.rdl L1140
- [ST-LC-0219](statements.md#st-lc-0219) Compute；code.rdl L1148
- [ST-LC-0244](statements.md#st-lc-0244) Compute；code.rdl L1249
- [ST-LC-0245](statements.md#st-lc-0245) Compute；code.rdl L1251
- [ST-LC-0553](statements.md#st-lc-0553) Compute；code.rdl L1227

已剔除的软件接口候选：ST-LC-0508 (SendData), ST-LC-0552 (GetData)

剩余义务（保留原审查）：

```json
[
  "ABI/浮点容差/活动WDT输入绑定pending-interface，未运行官方解释器/LC。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0011 — LC2003.2

WDT 选择 Custom operator 时，将消息中的数据送给任务自定义函数。

当前保留数据片段：

- [ST-LC-0200](statements.md#st-lc-0200) Set；code.rdl L1112
- [ST-LC-0216](statements.md#st-lc-0216) Compute；code.rdl L1140
- [ST-LC-0217](statements.md#st-lc-0217) Compute；code.rdl L1142
- [ST-LC-0218](statements.md#st-lc-0218) Compute；code.rdl L1145
- [ST-LC-0220](statements.md#st-lc-0220) Set；code.rdl L1151
- [ST-LC-0226](statements.md#st-lc-0226) Compute；code.rdl L1166
- [ST-LC-0244](statements.md#st-lc-0244) Compute；code.rdl L1249
- [ST-LC-0269](statements.md#st-lc-0269) Compute；code.rdl L1076
- [ST-LC-0553](statements.md#st-lc-0553) Compute；code.rdl L1227

已剔除的软件接口候选：ST-LC-0507 (SendData), ST-LC-0552 (GetData)

剩余义务（保留原审查）：

```json
[
  "ISSUE0020任务自定义算法待提供；documentary义务与默认stub事实并列，不补造算法。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0012 — LC2003.3

WP 比较结果为 FALSE 时，把该 WP 连续 TRUE 次数清零。

当前保留数据片段：

- [ST-LC-0200](statements.md#st-lc-0200) Set；code.rdl L1112
- [ST-LC-0225](statements.md#st-lc-0225) Compute；code.rdl L1163
- [ST-LC-0226](statements.md#st-lc-0226) Compute；code.rdl L1166
- [ST-LC-0230](statements.md#st-lc-0230) Set；code.rdl L1179

已剔除的软件接口候选：无直接关联；仍有系统入口/资源绑定缺口

剩余义务（保留原审查）：

```json
[
  "真实字段持久绑定与入口pending-interface；ERROR/STALE保持计数另由REQ0067记录。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0013 — LC2003.4

Watchpoint 无法评估时，将该项 WRT 结果置为 ERROR。

当前保留数据片段：

- [ST-LC-0200](statements.md#st-lc-0200) Set；code.rdl L1112
- [ST-LC-0207](statements.md#st-lc-0207) Compute；code.rdl L1127
- [ST-LC-0208](statements.md#st-lc-0208) Compute；code.rdl L1129
- [ST-LC-0209](statements.md#st-lc-0209) Compute；code.rdl L1132
- [ST-LC-0210](statements.md#st-lc-0210) Compute；code.rdl L1190
- [ST-LC-0211](statements.md#st-lc-0211) Compute；code.rdl L1182, L1194
- [ST-LC-0212](statements.md#st-lc-0212) Set；code.rdl L1184, L1196
- [ST-LC-0213](statements.md#st-lc-0213) Set；code.rdl L1186, L1198
- [ST-LC-0215](statements.md#st-lc-0215) Compute；code.rdl L1137
- [ST-LC-0219](statements.md#st-lc-0219) Compute；code.rdl L1148
- [ST-LC-0220](statements.md#st-lc-0220) Set；code.rdl L1151
- [ST-LC-0221](statements.md#st-lc-0221) Compute；code.rdl L1153
- [ST-LC-0222](statements.md#st-lc-0222) Set；code.rdl L1155
- [ST-LC-0227](statements.md#st-lc-0227) Compute；code.rdl L1169
- [ST-LC-0235](statements.md#st-lc-0235) Compute；code.rdl L1214, L1219
- [ST-LC-0267](statements.md#st-lc-0267) Compute；code.rdl L1082
- [ST-LC-0268](statements.md#st-lc-0268) Set；code.rdl L1085

已剔除的软件接口候选：ST-LC-0506 (SendData), ST-LC-0508 (SendData)

剩余义务（保留原审查）：

```json
[
  "ISSUE0021/0004 ABI及风险指针行为待确认；documentaryERROR义务不是现码万能检错保证；接口pending。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0014 — LC2004

每个 WP 在 dump-only WRT 中保存结果及九类比较、连续、累计、跨越和age统计。

当前保留数据片段：

- [ST-LC-0200](statements.md#st-lc-0200) Set；code.rdl L1112
- [ST-LC-0202](statements.md#st-lc-0202) Compute；code.rdl L1117
- [ST-LC-0212](statements.md#st-lc-0212) Set；code.rdl L1184, L1196
- [ST-LC-0220](statements.md#st-lc-0220) Set；code.rdl L1151
- [ST-LC-0221](statements.md#st-lc-0221) Compute；code.rdl L1153
- [ST-LC-0222](statements.md#st-lc-0222) Set；code.rdl L1155
- [ST-LC-0223](statements.md#st-lc-0223) Compute；code.rdl L1157
- [ST-LC-0224](statements.md#st-lc-0224) Compute；code.rdl L1160
- [ST-LC-0225](statements.md#st-lc-0225) Compute；code.rdl L1163
- [ST-LC-0226](statements.md#st-lc-0226) Compute；code.rdl L1166
- [ST-LC-0227](statements.md#st-lc-0227) Compute；code.rdl L1169
- [ST-LC-0228](statements.md#st-lc-0228) Compute；code.rdl L1173
- [ST-LC-0229](statements.md#st-lc-0229) Compute；code.rdl L1176
- [ST-LC-0230](statements.md#st-lc-0230) Set；code.rdl L1179
- [ST-LC-0257](statements.md#st-lc-0257) Compute；code.rdl L798, L1052
- [ST-LC-0259](statements.md#st-lc-0259) Set；code.rdl L803, L1057
- [ST-LC-0261](statements.md#st-lc-0261) Set；code.rdl L808, L1062
- [ST-LC-0264](statements.md#st-lc-0264) Compute；code.rdl L1098
- [ST-LC-0265](statements.md#st-lc-0265) Compute；code.rdl L1101
- [ST-LC-0266](statements.md#st-lc-0266) Set；code.rdl L1103

已剔除的软件接口候选：无直接关联；仍有系统入口/资源绑定缺口

剩余义务（保留原审查）：

```json
[
  "ISSUE0006 STALE跨越口径冲突不记全部full；dump-only资源建立与软件提交不是Compute完成。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0015 — LC2005

WDT 更新时验证算子、数据大小和消息 ID。

当前保留数据片段：

- [ST-LC-0236](statements.md#st-lc-0236) Set；code.rdl L1229
- [ST-LC-0237](statements.md#st-lc-0237) Compute；code.rdl L1231
- [ST-LC-0238](statements.md#st-lc-0238) Compute；code.rdl L1233, L1271
- [ST-LC-0239](statements.md#st-lc-0239) Compute；code.rdl L1236
- [ST-LC-0240](statements.md#st-lc-0240) Compute；code.rdl L1238
- [ST-LC-0241](statements.md#st-lc-0241) Compute；code.rdl L1241
- [ST-LC-0242](statements.md#st-lc-0242) Compute；code.rdl L1244
- [ST-LC-0243](statements.md#st-lc-0243) Compute；code.rdl L1246
- [ST-LC-0244](statements.md#st-lc-0244) Compute；code.rdl L1249
- [ST-LC-0245](statements.md#st-lc-0245) Compute；code.rdl L1251
- [ST-LC-0246](statements.md#st-lc-0246) Compute；code.rdl L1254
- [ST-LC-0247](statements.md#st-lc-0247) Compute；code.rdl L1256
- [ST-LC-0248](statements.md#st-lc-0248) Compute；code.rdl L1259
- [ST-LC-0249](statements.md#st-lc-0249) Compute；code.rdl L1264
- [ST-LC-0250](statements.md#st-lc-0250) Compute；code.rdl L1267
- [ST-LC-0251](statements.md#st-lc-0251) Compute；code.rdl L1269
- [ST-LC-0252](statements.md#st-lc-0252) Compute；code.rdl L1274
- [ST-LC-0553](statements.md#st-lc-0553) Compute；code.rdl L1227

已剔除的软件接口候选：ST-LC-0509 (SendData), ST-LC-0510 (SendData), ST-LC-0552 (GetData)

剩余义务（保留原审查）：

```json
[
  "原WDT完全不验WatchpointOffset；未冻结cFE谓词、回调/EVS/更新绑定pending-interface。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0016 — LC2006

评估 WP/AP 方程前，将遥测数据转换为 CPU 本机字节序。

当前保留数据片段：

- [ST-LC-0200](statements.md#st-lc-0200) Set；code.rdl L1112
- [ST-LC-0214](statements.md#st-lc-0214) Compute；code.rdl L1135
- [ST-LC-0215](statements.md#st-lc-0215) Compute；code.rdl L1137
- [ST-LC-0216](statements.md#st-lc-0216) Compute；code.rdl L1140
- [ST-LC-0219](statements.md#st-lc-0219) Compute；code.rdl L1148
- [ST-LC-0220](statements.md#st-lc-0220) Set；code.rdl L1151
- [ST-LC-0235](statements.md#st-lc-0235) Compute；code.rdl L1214, L1219

已剔除的软件接口候选：ST-LC-0508 (SendData)

剩余义务（保留原审查）：

```json
[
  "目标swap map/ABI及AP组持久连接待核定；不以静态规则宣称运行通过。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0017 — LC3000

支持最多平台定义数量的 Actionpoint。

当前保留数据片段：

- [ST-LC-0300](statements.md#st-lc-0300) Compute；code.rdl L563
- [ST-LC-0302](statements.md#st-lc-0302) Compute；code.rdl L568
- [ST-LC-0306](statements.md#st-lc-0306) Compute；code.rdl L574
- [ST-LC-0307](statements.md#st-lc-0307) Compute；code.rdl L576, L773
- [ST-LC-0370](statements.md#st-lc-0370) Compute；code.rdl L12
- [ST-LC-0371](statements.md#st-lc-0371) Compute；code.rdl L14, L83
- [ST-LC-0388](statements.md#st-lc-0388) Compute；code.rdl L81
- [ST-LC-0531](statements.md#st-lc-0531) Compute；code.rdl L543
- [ST-LC-0555](statements.md#st-lc-0555) Compute；code.rdl L10

已剔除的软件接口候选：ST-LC-0530 (GetData), ST-LC-0554 (GetData)

剩余义务（保留原审查）：

```json
[
  "平台默认容量只是冻结源码基线，实际飞行容量与依赖部署尚未固定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0018 — LC3001

应用 ACTIVE/PASSIVE 收到 Sample Request 时处理请求指定的 Actionpoint。

当前保留数据片段：

- [ST-LC-0300](statements.md#st-lc-0300) Compute；code.rdl L563
- [ST-LC-0301](statements.md#st-lc-0301) Compute；code.rdl L565
- [ST-LC-0302](statements.md#st-lc-0302) Compute；code.rdl L568
- [ST-LC-0303](statements.md#st-lc-0303) Compute；code.rdl L821
- [ST-LC-0304](statements.md#st-lc-0304) Compute；code.rdl L571
- [ST-LC-0305](statements.md#st-lc-0305) Compute；code.rdl L777
- [ST-LC-0306](statements.md#st-lc-0306) Compute；code.rdl L574
- [ST-LC-0307](statements.md#st-lc-0307) Compute；code.rdl L576, L773
- [ST-LC-0308](statements.md#st-lc-0308) Compute；code.rdl L579
- [ST-LC-0309](statements.md#st-lc-0309) Compute；code.rdl L768
- [ST-LC-0310](statements.md#st-lc-0310) Compute；code.rdl L582
- [ST-LC-0311](statements.md#st-lc-0311) Set；code.rdl L584
- [ST-LC-0312](statements.md#st-lc-0312) Compute；code.rdl L586
- [ST-LC-0324](statements.md#st-lc-0324) Set；code.rdl L631
- [ST-LC-0366](statements.md#st-lc-0366) Compute；code.rdl L771
- [ST-LC-0367](statements.md#st-lc-0367) Compute；code.rdl L782
- [ST-LC-0368](statements.md#st-lc-0368) Compute；code.rdl L785
- [ST-LC-0369](statements.md#st-lc-0369) Compute；code.rdl L825
- [ST-LC-0391](statements.md#st-lc-0391) Compute；code.rdl L106
- [ST-LC-0396](statements.md#st-lc-0396) Compute；code.rdl L780
- [ST-LC-0531](statements.md#st-lc-0531) Compute；code.rdl L543

已剔除的软件接口候选：ST-LC-0511 (SendData), ST-LC-0512 (SendData), ST-LC-0530 (GetData)

剩余义务（保留原审查）：

```json
[
  "真实独立消息/软件回调入口、项目聚合数据与持久成员别名仍待官方接口绑定；不以注释或effects冒充执行。",
  "首项拒绝整范围与请求指定AP的正式义务待ISSUE-LC-0015裁定；EDS路径不默认视为非EDS等价。",
  "同次AP后age续段已由ST0368内联ST0253–0262；ActionWorking到WAgeWorking的官方聚合/别名加载仍待确认，不能把项目资源绑定当官方验收。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0019 — LC3001.1

支持 AND、OR、XOR、NOT、EQUAL 五种逆波兰算子。

当前保留数据片段：

- [ST-LC-0312](statements.md#st-lc-0312) Compute；code.rdl L586
- [ST-LC-0313](statements.md#st-lc-0313) Compute；code.rdl L588, L622
- [ST-LC-0314](statements.md#st-lc-0314) Compute；code.rdl L591
- [ST-LC-0315](statements.md#st-lc-0315) Compute；code.rdl L594
- [ST-LC-0316](statements.md#st-lc-0316) Compute；code.rdl L598
- [ST-LC-0317](statements.md#st-lc-0317) Compute；code.rdl L602
- [ST-LC-0318](statements.md#st-lc-0318) Compute；code.rdl L606
- [ST-LC-0319](statements.md#st-lc-0319) Compute；code.rdl L610
- [ST-LC-0320](statements.md#st-lc-0320) Compute；code.rdl L613
- [ST-LC-0321](statements.md#st-lc-0321) Compute；code.rdl L620
- [ST-LC-0322](statements.md#st-lc-0322) Compute；code.rdl L626
- [ST-LC-0323](statements.md#st-lc-0323) Compute；code.rdl L629
- [ST-LC-0378](statements.md#st-lc-0378) Compute；code.rdl L35
- [ST-LC-0379](statements.md#st-lc-0379) Compute；code.rdl L37, L44
- [ST-LC-0380](statements.md#st-lc-0380) Compute；code.rdl L40
- [ST-LC-0381](statements.md#st-lc-0381) Compute；code.rdl L42
- [ST-LC-0382](statements.md#st-lc-0382) Compute；code.rdl L47
- [ST-LC-0395](statements.md#st-lc-0395) Compute；code.rdl L1036
- [ST-LC-0555](statements.md#st-lc-0555) Compute；code.rdl L10

已剔除的软件接口候选：ST-LC-0513 (SendData), ST-LC-0554 (GetData)

剩余义务（保留原审查）：

```json
[
  "项目公式/聚合/枚举的官方库加载格式与解析器尚待验收；不声称该候选片段是完整可运行系统。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0020 — LC3001.2

AP 方程结果 PASS 时，将该AP连续FAIL次数清零。

当前保留数据片段：

- [ST-LC-0356](statements.md#st-lc-0356) Compute；code.rdl L726
- [ST-LC-0362](statements.md#st-lc-0362) Set；code.rdl L747, L755
- [ST-LC-0365](statements.md#st-lc-0365) Compute；code.rdl L722, L749, L757, L762

已剔除的软件接口候选：无直接关联；仍有系统入口/资源绑定缺口

剩余义务（保留原审查）：

```json
[]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0021 — LC3001.3

AP 无法评估时，ART 中该AP结果置为 ERROR。

当前保留数据片段：

- [ST-LC-0312](statements.md#st-lc-0312) Compute；code.rdl L586
- [ST-LC-0313](statements.md#st-lc-0313) Compute；code.rdl L588, L622
- [ST-LC-0314](statements.md#st-lc-0314) Compute；code.rdl L591
- [ST-LC-0315](statements.md#st-lc-0315) Compute；code.rdl L594
- [ST-LC-0316](statements.md#st-lc-0316) Compute；code.rdl L598
- [ST-LC-0317](statements.md#st-lc-0317) Compute；code.rdl L602
- [ST-LC-0318](statements.md#st-lc-0318) Compute；code.rdl L606
- [ST-LC-0319](statements.md#st-lc-0319) Compute；code.rdl L610
- [ST-LC-0320](statements.md#st-lc-0320) Compute；code.rdl L613
- [ST-LC-0321](statements.md#st-lc-0321) Compute；code.rdl L620
- [ST-LC-0322](statements.md#st-lc-0322) Compute；code.rdl L626
- [ST-LC-0323](statements.md#st-lc-0323) Compute；code.rdl L629
- [ST-LC-0324](statements.md#st-lc-0324) Set；code.rdl L631
- [ST-LC-0363](statements.md#st-lc-0363) Compute；code.rdl L752
- [ST-LC-0364](statements.md#st-lc-0364) Compute；code.rdl L760
- [ST-LC-0365](statements.md#st-lc-0365) Compute；code.rdl L722, L749, L757, L762

已剔除的软件接口候选：ST-LC-0513 (SendData), ST-LC-0519 (SendData)

剩余义务（保留原审查）：

```json
[
  "EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0022 — LC3002

表定义AP状态ACTIVE或PASSIVE时，将其采样结果保存在dump-only ART。

当前保留数据片段：

- [ST-LC-0300](statements.md#st-lc-0300) Compute；code.rdl L563
- [ST-LC-0308](statements.md#st-lc-0308) Compute；code.rdl L579
- [ST-LC-0309](statements.md#st-lc-0309) Compute；code.rdl L768
- [ST-LC-0310](statements.md#st-lc-0310) Compute；code.rdl L582
- [ST-LC-0311](statements.md#st-lc-0311) Set；code.rdl L584
- [ST-LC-0312](statements.md#st-lc-0312) Compute；code.rdl L586
- [ST-LC-0323](statements.md#st-lc-0323) Compute；code.rdl L629
- [ST-LC-0324](statements.md#st-lc-0324) Set；code.rdl L631
- [ST-LC-0339](statements.md#st-lc-0339) Set；code.rdl L668
- [ST-LC-0366](statements.md#st-lc-0366) Compute；code.rdl L771
- [ST-LC-0391](statements.md#st-lc-0391) Compute；code.rdl L106

已剔除的软件接口候选：无直接关联；仍有系统入口/资源绑定缺口

剩余义务（保留原审查）：

```json
[
  "真实独立消息/软件回调入口、项目聚合数据与持久成员别名仍待官方接口绑定；不以注释或effects冒充执行。",
  "本组只表达ART存储，不虚构表dump服务或将ART当自动HK完整遥测。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0023 — LC3002.1

AP 求值发生 PASS→FAIL 时发出失败事件。

当前保留数据片段：

- [ST-LC-0325](statements.md#st-lc-0325) Compute；code.rdl L633
- [ST-LC-0330](statements.md#st-lc-0330) Compute；code.rdl L644
- [ST-LC-0331](statements.md#st-lc-0331) Compute；code.rdl L647
- [ST-LC-0332](statements.md#st-lc-0332) Set；code.rdl L649
- [ST-LC-0333](statements.md#st-lc-0333) Compute；code.rdl L651
- [ST-LC-0334](statements.md#st-lc-0334) Compute；code.rdl L654
- [ST-LC-0335](statements.md#st-lc-0335) Compute；code.rdl L656, L689, L715, L741
- [ST-LC-0336](statements.md#st-lc-0336) Set；code.rdl L658, L691, L717, L743

已剔除的软件接口候选：ST-LC-0514 (SendData)

剩余义务（保留原审查）：

```json
[
  "EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0024 — LC3002.1.1

PASS→FAIL 转换事件数不得超过表定义最大值。

当前保留数据片段：

- [ST-LC-0330](statements.md#st-lc-0330) Compute；code.rdl L644
- [ST-LC-0331](statements.md#st-lc-0331) Compute；code.rdl L647
- [ST-LC-0332](statements.md#st-lc-0332) Set；code.rdl L649
- [ST-LC-0333](statements.md#st-lc-0333) Compute；code.rdl L651
- [ST-LC-0334](statements.md#st-lc-0334) Compute；code.rdl L654
- [ST-LC-0335](statements.md#st-lc-0335) Compute；code.rdl L656, L689, L715, L741
- [ST-LC-0336](statements.md#st-lc-0336) Set；code.rdl L658, L691, L717, L743

已剔除的软件接口候选：ST-LC-0514 (SendData)

剩余义务（保留原审查）：

```json
[
  "EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0025 — LC3002.2

AP 求值发生 FAIL→PASS 时发出恢复到限值内事件。

当前保留数据片段：

- [ST-LC-0335](statements.md#st-lc-0335) Compute；code.rdl L656, L689, L715, L741
- [ST-LC-0336](statements.md#st-lc-0336) Set；code.rdl L658, L691, L717, L743
- [ST-LC-0356](statements.md#st-lc-0356) Compute；code.rdl L726
- [ST-LC-0357](statements.md#st-lc-0357) Compute；code.rdl L729
- [ST-LC-0358](statements.md#st-lc-0358) Compute；code.rdl L732
- [ST-LC-0359](statements.md#st-lc-0359) Set；code.rdl L734
- [ST-LC-0360](statements.md#st-lc-0360) Compute；code.rdl L736
- [ST-LC-0361](statements.md#st-lc-0361) Compute；code.rdl L739
- [ST-LC-0362](statements.md#st-lc-0362) Set；code.rdl L747, L755
- [ST-LC-0365](statements.md#st-lc-0365) Compute；code.rdl L722, L749, L757, L762

已剔除的软件接口候选：ST-LC-0518 (SendData)

剩余义务（保留原审查）：

```json
[
  "EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0026 — LC3002.2.1

FAIL→PASS 转换事件数不得超过表定义最大值。

当前保留数据片段：

- [ST-LC-0335](statements.md#st-lc-0335) Compute；code.rdl L656, L689, L715, L741
- [ST-LC-0336](statements.md#st-lc-0336) Set；code.rdl L658, L691, L717, L743
- [ST-LC-0356](statements.md#st-lc-0356) Compute；code.rdl L726
- [ST-LC-0357](statements.md#st-lc-0357) Compute；code.rdl L729
- [ST-LC-0358](statements.md#st-lc-0358) Compute；code.rdl L732
- [ST-LC-0359](statements.md#st-lc-0359) Set；code.rdl L734
- [ST-LC-0360](statements.md#st-lc-0360) Compute；code.rdl L736
- [ST-LC-0361](statements.md#st-lc-0361) Compute；code.rdl L739

已剔除的软件接口候选：ST-LC-0518 (SendData)

剩余义务（保留原审查）：

```json
[
  "EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0027 — LC3002.3

连续FAIL达到ADT阈值且AP ACTIVE时，生成事件、向SC请求启动表定义RTS，并累计发出请求次数。

当前保留数据片段：

- [ST-LC-0325](statements.md#st-lc-0325) Compute；code.rdl L633
- [ST-LC-0326](statements.md#st-lc-0326) Compute；code.rdl L636
- [ST-LC-0327](statements.md#st-lc-0327) Set；code.rdl L638
- [ST-LC-0328](statements.md#st-lc-0328) Compute；code.rdl L640
- [ST-LC-0329](statements.md#st-lc-0329) Set；code.rdl L642
- [ST-LC-0335](statements.md#st-lc-0335) Compute；code.rdl L656, L689, L715, L741
- [ST-LC-0336](statements.md#st-lc-0336) Set；code.rdl L658, L691, L717, L743
- [ST-LC-0337](statements.md#st-lc-0337) Compute；code.rdl L662
- [ST-LC-0338](statements.md#st-lc-0338) Compute；code.rdl L665
- [ST-LC-0339](statements.md#st-lc-0339) Set；code.rdl L668
- [ST-LC-0340](statements.md#st-lc-0340) Compute；code.rdl L670
- [ST-LC-0341](statements.md#st-lc-0341) Compute；code.rdl L673
- [ST-LC-0342](statements.md#st-lc-0342) Compute；code.rdl L675
- [ST-LC-0343](statements.md#st-lc-0343) Compute；code.rdl L677
- [ST-LC-0344](statements.md#st-lc-0344) Set；code.rdl L679
- [ST-LC-0345](statements.md#st-lc-0345) Compute；code.rdl L681
- [ST-LC-0346](statements.md#st-lc-0346) Set；code.rdl L683
- [ST-LC-0347](statements.md#st-lc-0347) Compute；code.rdl L685
- [ST-LC-0348](statements.md#st-lc-0348) Compute；code.rdl L687
- [ST-LC-0351](statements.md#st-lc-0351) Compute；code.rdl L698
- [ST-LC-0355](statements.md#st-lc-0355) Compute；code.rdl L713
- [ST-LC-0365](statements.md#st-lc-0365) Compute；code.rdl L722, L749, L757, L762

已剔除的软件接口候选：ST-LC-0515 (SendData), ST-LC-0516 (SendData), ST-LC-0517 (SendData), ST-LC-0523 (SendData)

剩余义务（保留原审查）：

```json
[
  "真实独立消息/软件回调入口、项目聚合数据与持久成员别名仍待官方接口绑定；不以注释或effects冒充执行。",
  "EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。",
  "commands sent/RTS initiated边界及原代码忽略发送返回策略待ISSUE-LC-0007；错误间隔的“连续”待ISSUE-LC-0011/0017。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0028 — LC3002.3.1

一旦RTS被发起，应将关联AP当前状态改为PASSIVE防止重复发起。

当前保留数据片段：

- [ST-LC-0337](statements.md#st-lc-0337) Compute；code.rdl L662
- [ST-LC-0338](statements.md#st-lc-0338) Compute；code.rdl L665
- [ST-LC-0339](statements.md#st-lc-0339) Set；code.rdl L668
- [ST-LC-0340](statements.md#st-lc-0340) Compute；code.rdl L670
- [ST-LC-0342](statements.md#st-lc-0342) Compute；code.rdl L675
- [ST-LC-0351](statements.md#st-lc-0351) Compute；code.rdl L698
- [ST-LC-0392](statements.md#st-lc-0392) Set；code.rdl L94

已剔除的软件接口候选：ST-LC-0516 (SendData), ST-LC-0523 (SendData)

剩余义务（保留原审查）：

```json
[
  "initiated含义、失败策略与先置PASSIVE差异需裁定；不得把实现视图自动当原文完整覆盖。",
  "EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0029 — LC3002.4

连续FAIL达到阈值且AP PASSIVE时，不执行动作，应发抑制事件并加Passive RTS计数。

当前保留数据片段：

- [ST-LC-0325](statements.md#st-lc-0325) Compute；code.rdl L633
- [ST-LC-0326](statements.md#st-lc-0326) Compute；code.rdl L636
- [ST-LC-0327](statements.md#st-lc-0327) Set；code.rdl L638
- [ST-LC-0335](statements.md#st-lc-0335) Compute；code.rdl L656, L689, L715, L741
- [ST-LC-0336](statements.md#st-lc-0336) Set；code.rdl L658, L691, L717, L743
- [ST-LC-0337](statements.md#st-lc-0337) Compute；code.rdl L662
- [ST-LC-0338](statements.md#st-lc-0338) Compute；code.rdl L665
- [ST-LC-0349](statements.md#st-lc-0349) Compute；code.rdl L694, L706
- [ST-LC-0350](statements.md#st-lc-0350) Set；code.rdl L696, L708
- [ST-LC-0352](statements.md#st-lc-0352) Compute；code.rdl L702
- [ST-LC-0353](statements.md#st-lc-0353) Set；code.rdl L704
- [ST-LC-0354](statements.md#st-lc-0354) Compute；code.rdl L710
- [ST-LC-0355](statements.md#st-lc-0355) Compute；code.rdl L713
- [ST-LC-0365](statements.md#st-lc-0365) Compute；code.rdl L722, L749, L757, L762
- [ST-LC-0393](statements.md#st-lc-0393) Compute；code.rdl L100

已剔除的软件接口候选：ST-LC-0517 (SendData), ST-LC-0522 (SendData)

剩余义务（保留原审查）：

```json
[
  "EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。",
  "原文没有MaxPassiveEvents限额，保留ISSUE-LC-0010与documentary对照，不偷偷补修代码。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0030 — LC3003

AP DISABLED 时跳过该AP处理，不产生该AP的采样动作。

当前保留数据片段：

- [ST-LC-0308](statements.md#st-lc-0308) Compute；code.rdl L579
- [ST-LC-0309](statements.md#st-lc-0309) Compute；code.rdl L768
- [ST-LC-0365](statements.md#st-lc-0365) Compute；code.rdl L722, L749, L757, L762
- [ST-LC-0366](statements.md#st-lc-0366) Compute；code.rdl L771
- [ST-LC-0391](statements.md#st-lc-0391) Compute；code.rdl L106

已剔除的软件接口候选：无直接关联；仍有系统入口/资源绑定缺口

剩余义务（保留原审查）：

```json
[]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0031 — LC3004

AP UNUSED 时跳过该AP处理。

当前保留数据片段：

- [ST-LC-0304](statements.md#st-lc-0304) Compute；code.rdl L571
- [ST-LC-0305](statements.md#st-lc-0305) Compute；code.rdl L777
- [ST-LC-0308](statements.md#st-lc-0308) Compute；code.rdl L579
- [ST-LC-0309](statements.md#st-lc-0309) Compute；code.rdl L768
- [ST-LC-0365](statements.md#st-lc-0365) Compute；code.rdl L722, L749, L757, L762
- [ST-LC-0391](statements.md#st-lc-0391) Compute；code.rdl L106

已剔除的软件接口候选：ST-LC-0512 (SendData)

剩余义务（保留原审查）：

```json
[
  "范围首项NOT_USED整体拒绝与LC3001/LC3004的组合意义待ISSUE-LC-0015。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0032 — LC3005

AP PERMANENTLY DISABLED 时跳过该AP处理。

当前保留数据片段：

- [ST-LC-0304](statements.md#st-lc-0304) Compute；code.rdl L571
- [ST-LC-0305](statements.md#st-lc-0305) Compute；code.rdl L777
- [ST-LC-0308](statements.md#st-lc-0308) Compute；code.rdl L579
- [ST-LC-0309](statements.md#st-lc-0309) Compute；code.rdl L768
- [ST-LC-0365](statements.md#st-lc-0365) Compute；code.rdl L722, L749, L757, L762
- [ST-LC-0391](statements.md#st-lc-0391) Compute；code.rdl L106

已剔除的软件接口候选：ST-LC-0512 (SendData)

剩余义务（保留原审查）：

```json
[
  "范围首项PERMOFF组合解释待ISSUE-LC-0015；状态命令不能解除PERMOFF的规则由命令组负责，不在本组捏造解锁。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0033 — LC3006

每个 AP 在 dump-only ART 保存最近结果、当前状态、两向转换、连续/累计FAIL、RTS请求累计和事件总计。

当前保留数据片段：

- [ST-LC-0308](statements.md#st-lc-0308) Compute；code.rdl L579
- [ST-LC-0309](statements.md#st-lc-0309) Compute；code.rdl L768
- [ST-LC-0310](statements.md#st-lc-0310) Compute；code.rdl L582
- [ST-LC-0311](statements.md#st-lc-0311) Set；code.rdl L584
- [ST-LC-0322](statements.md#st-lc-0322) Compute；code.rdl L626
- [ST-LC-0323](statements.md#st-lc-0323) Compute；code.rdl L629
- [ST-LC-0324](statements.md#st-lc-0324) Set；code.rdl L631
- [ST-LC-0325](statements.md#st-lc-0325) Compute；code.rdl L633
- [ST-LC-0326](statements.md#st-lc-0326) Compute；code.rdl L636
- [ST-LC-0327](statements.md#st-lc-0327) Set；code.rdl L638
- [ST-LC-0328](statements.md#st-lc-0328) Compute；code.rdl L640
- [ST-LC-0329](statements.md#st-lc-0329) Set；code.rdl L642
- [ST-LC-0330](statements.md#st-lc-0330) Compute；code.rdl L644
- [ST-LC-0331](statements.md#st-lc-0331) Compute；code.rdl L647
- [ST-LC-0332](statements.md#st-lc-0332) Set；code.rdl L649
- [ST-LC-0333](statements.md#st-lc-0333) Compute；code.rdl L651
- [ST-LC-0334](statements.md#st-lc-0334) Compute；code.rdl L654
- [ST-LC-0335](statements.md#st-lc-0335) Compute；code.rdl L656, L689, L715, L741
- [ST-LC-0336](statements.md#st-lc-0336) Set；code.rdl L658, L691, L717, L743
- [ST-LC-0337](statements.md#st-lc-0337) Compute；code.rdl L662
- [ST-LC-0339](statements.md#st-lc-0339) Set；code.rdl L668
- [ST-LC-0342](statements.md#st-lc-0342) Compute；code.rdl L675
- [ST-LC-0343](statements.md#st-lc-0343) Compute；code.rdl L677
- [ST-LC-0344](statements.md#st-lc-0344) Set；code.rdl L679
- [ST-LC-0345](statements.md#st-lc-0345) Compute；code.rdl L681
- [ST-LC-0346](statements.md#st-lc-0346) Set；code.rdl L683
- [ST-LC-0347](statements.md#st-lc-0347) Compute；code.rdl L685
- [ST-LC-0348](statements.md#st-lc-0348) Compute；code.rdl L687
- [ST-LC-0349](statements.md#st-lc-0349) Compute；code.rdl L694, L706
- [ST-LC-0350](statements.md#st-lc-0350) Set；code.rdl L696, L708
- [ST-LC-0351](statements.md#st-lc-0351) Compute；code.rdl L698
- [ST-LC-0352](statements.md#st-lc-0352) Compute；code.rdl L702
- [ST-LC-0353](statements.md#st-lc-0353) Set；code.rdl L704
- [ST-LC-0354](statements.md#st-lc-0354) Compute；code.rdl L710
- [ST-LC-0355](statements.md#st-lc-0355) Compute；code.rdl L713
- [ST-LC-0356](statements.md#st-lc-0356) Compute；code.rdl L726
- [ST-LC-0357](statements.md#st-lc-0357) Compute；code.rdl L729
- [ST-LC-0358](statements.md#st-lc-0358) Compute；code.rdl L732
- [ST-LC-0359](statements.md#st-lc-0359) Set；code.rdl L734
- [ST-LC-0360](statements.md#st-lc-0360) Compute；code.rdl L736
- [ST-LC-0361](statements.md#st-lc-0361) Compute；code.rdl L739
- [ST-LC-0362](statements.md#st-lc-0362) Set；code.rdl L747, L755
- [ST-LC-0363](statements.md#st-lc-0363) Compute；code.rdl L752
- [ST-LC-0364](statements.md#st-lc-0364) Compute；code.rdl L760
- [ST-LC-0394](statements.md#st-lc-0394) Compute；code.rdl L112

已剔除的软件接口候选：ST-LC-0513 (SendData), ST-LC-0514 (SendData), ST-LC-0515 (SendData), ST-LC-0516 (SendData), ST-LC-0517 (SendData), ST-LC-0518 (SendData), ST-LC-0519 (SendData), ST-LC-0523 (SendData)

剩余义务（保留原审查）：

```json
[
  "原统计口径/错误间隔待ISSUE-LC-0011/0017；真实EVS/SB提交pending-interface，不能从统计增量证明服务成功。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0034 — LC3007

ADT 更新时验证默认状态、RTS号、事件类型、失败阈值、RPN语法。

当前保留数据片段：

- [ST-LC-0370](statements.md#st-lc-0370) Compute；code.rdl L12
- [ST-LC-0371](statements.md#st-lc-0371) Compute；code.rdl L14, L83
- [ST-LC-0372](statements.md#st-lc-0372) Compute；code.rdl L17
- [ST-LC-0373](statements.md#st-lc-0373) Compute；code.rdl L20
- [ST-LC-0374](statements.md#st-lc-0374) Compute；code.rdl L23
- [ST-LC-0375](statements.md#st-lc-0375) Compute；code.rdl L26
- [ST-LC-0376](statements.md#st-lc-0376) Compute；code.rdl L29
- [ST-LC-0377](statements.md#st-lc-0377) Compute；code.rdl L32
- [ST-LC-0378](statements.md#st-lc-0378) Compute；code.rdl L35
- [ST-LC-0379](statements.md#st-lc-0379) Compute；code.rdl L37, L44
- [ST-LC-0380](statements.md#st-lc-0380) Compute；code.rdl L40
- [ST-LC-0381](statements.md#st-lc-0381) Compute；code.rdl L42
- [ST-LC-0382](statements.md#st-lc-0382) Compute；code.rdl L47
- [ST-LC-0383](statements.md#st-lc-0383) Compute；code.rdl L50
- [ST-LC-0384](statements.md#st-lc-0384) Compute；code.rdl L53, L57, L61, L65, L69
- [ST-LC-0385](statements.md#st-lc-0385) Compute；code.rdl L73
- [ST-LC-0386](statements.md#st-lc-0386) Compute；code.rdl L76
- [ST-LC-0387](statements.md#st-lc-0387) Compute；code.rdl L78
- [ST-LC-0388](statements.md#st-lc-0388) Compute；code.rdl L81
- [ST-LC-0389](statements.md#st-lc-0389) Compute；code.rdl L86
- [ST-LC-0390](statements.md#st-lc-0390) Compute；code.rdl L88
- [ST-LC-0395](statements.md#st-lc-0395) Compute；code.rdl L1036
- [ST-LC-0555](statements.md#st-lc-0555) Compute；code.rdl L10

已剔除的软件接口候选：ST-LC-0520 (SendData), ST-LC-0521 (SendData), ST-LC-0554 (GetData)

剩余义务（保留原审查）：

```json
[
  "真实独立消息/软件回调入口、项目聚合数据与持久成员别名仍待官方接口绑定；不以注释或effects冒充执行。",
  "EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。",
  "TBL回调返回/表激活与跨表一致性不由本校验快照完成。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0035 — LC4000

将LC应用状态设置为ACTIVE。

当前保留数据片段：

- [ST-LC-0100](statements.md#st-lc-0100) Compute；code.rdl L165, L188, L347, L384, L455, L486, L547, L845, L928
- [ST-LC-0102](statements.md#st-lc-0102) Compute；code.rdl L171, L194, L353, L390, L413, L421, L461, L492, L529, L553, L851, L894, L902, L910, L934, L954
- [ST-LC-0103](statements.md#st-lc-0103) Compute；code.rdl L174, L197, L356, L393, L415, L423, L464, L495, L531, L556, L854, L896, L904, L912, L937, L956
- [ST-LC-0104](statements.md#st-lc-0104) Compute；code.rdl L169, L192, L351, L388, L417, L425, L459, L490, L533, L551, L849, L898, L906, L914, L932, L958
- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0110](statements.md#st-lc-0110) Compute；code.rdl L944
- [ST-LC-0111](statements.md#st-lc-0111) Compute；code.rdl L947
- [ST-LC-0539](statements.md#st-lc-0539) Compute；code.rdl L924

已剔除的软件接口候选：ST-LC-0500 (SendData), ST-LC-0501 (SendData), ST-LC-0538 (ProTC)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0036 — LC4001

将LC应用状态设置为PASSIVE。

当前保留数据片段：

- [ST-LC-0100](statements.md#st-lc-0100) Compute；code.rdl L165, L188, L347, L384, L455, L486, L547, L845, L928
- [ST-LC-0102](statements.md#st-lc-0102) Compute；code.rdl L171, L194, L353, L390, L413, L421, L461, L492, L529, L553, L851, L894, L902, L910, L934, L954
- [ST-LC-0103](statements.md#st-lc-0103) Compute；code.rdl L174, L197, L356, L393, L415, L423, L464, L495, L531, L556, L854, L896, L904, L912, L937, L956
- [ST-LC-0104](statements.md#st-lc-0104) Compute；code.rdl L169, L192, L351, L388, L417, L425, L459, L490, L533, L551, L849, L898, L906, L914, L932, L958
- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0110](statements.md#st-lc-0110) Compute；code.rdl L944
- [ST-LC-0111](statements.md#st-lc-0111) Compute；code.rdl L947
- [ST-LC-0539](statements.md#st-lc-0539) Compute；code.rdl L924

已剔除的软件接口候选：ST-LC-0500 (SendData), ST-LC-0501 (SendData), ST-LC-0538 (ProTC)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0037 — LC4002

将LC应用状态设置为DISABLED。

当前保留数据片段：

- [ST-LC-0100](statements.md#st-lc-0100) Compute；code.rdl L165, L188, L347, L384, L455, L486, L547, L845, L928
- [ST-LC-0102](statements.md#st-lc-0102) Compute；code.rdl L171, L194, L353, L390, L413, L421, L461, L492, L529, L553, L851, L894, L902, L910, L934, L954
- [ST-LC-0103](statements.md#st-lc-0103) Compute；code.rdl L174, L197, L356, L393, L415, L423, L464, L495, L531, L556, L854, L896, L904, L912, L937, L956
- [ST-LC-0104](statements.md#st-lc-0104) Compute；code.rdl L169, L192, L351, L388, L417, L425, L459, L490, L533, L551, L849, L898, L906, L914, L932, L958
- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0110](statements.md#st-lc-0110) Compute；code.rdl L944
- [ST-LC-0111](statements.md#st-lc-0111) Compute；code.rdl L947
- [ST-LC-0539](statements.md#st-lc-0539) Compute；code.rdl L924

已剔除的软件接口候选：ST-LC-0500 (SendData), ST-LC-0501 (SendData), ST-LC-0538 (ProTC)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0038 — LC4003

收到命令后将指定单个AP置为ACTIVE；原文义务与当前例外分别保留。

当前保留数据片段：

- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0112](statements.md#st-lc-0112) Compute；code.rdl L861
- [ST-LC-0113](statements.md#st-lc-0113) Compute；code.rdl L833, L864
- [ST-LC-0114](statements.md#st-lc-0114) Compute；code.rdl L866
- [ST-LC-0115](statements.md#st-lc-0115) Compute；code.rdl L869, L883
- [ST-LC-0116](statements.md#st-lc-0116) Compute；code.rdl L872
- [ST-LC-0117](statements.md#st-lc-0117) Compute；code.rdl L875
- [ST-LC-0118](statements.md#st-lc-0118) Compute；code.rdl L878
- [ST-LC-0119](statements.md#st-lc-0119) Compute；code.rdl L881
- [ST-LC-0120](statements.md#st-lc-0120) Compute；code.rdl L886
- [ST-LC-0121](statements.md#st-lc-0121) Compute；code.rdl L835
- [ST-LC-0541](statements.md#st-lc-0541) Compute；code.rdl L841

已剔除的软件接口候选：ST-LC-0501 (SendData), ST-LC-0540 (ProTC)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
  "正式单项状态命令未声明NOT_USED/PERMOFF例外，代码单选拒绝；激活PERMOFF另受LC4009.1约束，需需求裁决。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0039 — LC4004

收到命令后将全部AP置为ACTIVE；原文义务与当前例外分别保留。

当前保留数据片段：

- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0112](statements.md#st-lc-0112) Compute；code.rdl L861
- [ST-LC-0113](statements.md#st-lc-0113) Compute；code.rdl L833, L864
- [ST-LC-0114](statements.md#st-lc-0114) Compute；code.rdl L866
- [ST-LC-0115](statements.md#st-lc-0115) Compute；code.rdl L869, L883
- [ST-LC-0116](statements.md#st-lc-0116) Compute；code.rdl L872
- [ST-LC-0117](statements.md#st-lc-0117) Compute；code.rdl L875
- [ST-LC-0118](statements.md#st-lc-0118) Compute；code.rdl L878
- [ST-LC-0119](statements.md#st-lc-0119) Compute；code.rdl L881
- [ST-LC-0120](statements.md#st-lc-0120) Compute；code.rdl L886
- [ST-LC-0121](statements.md#st-lc-0121) Compute；code.rdl L835
- [ST-LC-0541](statements.md#st-lc-0541) Compute；code.rdl L841

已剔除的软件接口候选：ST-LC-0501 (SendData), ST-LC-0540 (ProTC)

剩余义务（保留原审查）：

```json
[
  "正式ALL包含NOT_USED/PERMOFF与代码跳过例外、LC4009.1的冲突待裁决；不宣称代码流程全满足ALL原文。",
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0040 — LC4005

收到命令后将指定单个AP置为PASSIVE；原文义务与当前例外分别保留。

当前保留数据片段：

- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0112](statements.md#st-lc-0112) Compute；code.rdl L861
- [ST-LC-0113](statements.md#st-lc-0113) Compute；code.rdl L833, L864
- [ST-LC-0114](statements.md#st-lc-0114) Compute；code.rdl L866
- [ST-LC-0115](statements.md#st-lc-0115) Compute；code.rdl L869, L883
- [ST-LC-0116](statements.md#st-lc-0116) Compute；code.rdl L872
- [ST-LC-0117](statements.md#st-lc-0117) Compute；code.rdl L875
- [ST-LC-0118](statements.md#st-lc-0118) Compute；code.rdl L878
- [ST-LC-0119](statements.md#st-lc-0119) Compute；code.rdl L881
- [ST-LC-0120](statements.md#st-lc-0120) Compute；code.rdl L886
- [ST-LC-0121](statements.md#st-lc-0121) Compute；code.rdl L835
- [ST-LC-0541](statements.md#st-lc-0541) Compute；code.rdl L841

已剔除的软件接口候选：ST-LC-0501 (SendData), ST-LC-0540 (ProTC)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
  "正式单项状态命令未声明NOT_USED/PERMOFF例外，代码单选拒绝；激活PERMOFF另受LC4009.1约束，需需求裁决。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0041 — LC4006

收到命令后将全部AP置为PASSIVE；原文义务与当前例外分别保留。

当前保留数据片段：

- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0112](statements.md#st-lc-0112) Compute；code.rdl L861
- [ST-LC-0113](statements.md#st-lc-0113) Compute；code.rdl L833, L864
- [ST-LC-0114](statements.md#st-lc-0114) Compute；code.rdl L866
- [ST-LC-0115](statements.md#st-lc-0115) Compute；code.rdl L869, L883
- [ST-LC-0116](statements.md#st-lc-0116) Compute；code.rdl L872
- [ST-LC-0117](statements.md#st-lc-0117) Compute；code.rdl L875
- [ST-LC-0118](statements.md#st-lc-0118) Compute；code.rdl L878
- [ST-LC-0119](statements.md#st-lc-0119) Compute；code.rdl L881
- [ST-LC-0120](statements.md#st-lc-0120) Compute；code.rdl L886
- [ST-LC-0121](statements.md#st-lc-0121) Compute；code.rdl L835
- [ST-LC-0541](statements.md#st-lc-0541) Compute；code.rdl L841

已剔除的软件接口候选：ST-LC-0501 (SendData), ST-LC-0540 (ProTC)

剩余义务（保留原审查）：

```json
[
  "正式ALL包含NOT_USED/PERMOFF与代码跳过例外、LC4009.1的冲突待裁决；不宣称代码流程全满足ALL原文。",
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0042 — LC4007

收到命令后将指定单个AP置为DISABLED；原文义务与当前例外分别保留。

当前保留数据片段：

- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0112](statements.md#st-lc-0112) Compute；code.rdl L861
- [ST-LC-0113](statements.md#st-lc-0113) Compute；code.rdl L833, L864
- [ST-LC-0114](statements.md#st-lc-0114) Compute；code.rdl L866
- [ST-LC-0115](statements.md#st-lc-0115) Compute；code.rdl L869, L883
- [ST-LC-0116](statements.md#st-lc-0116) Compute；code.rdl L872
- [ST-LC-0117](statements.md#st-lc-0117) Compute；code.rdl L875
- [ST-LC-0118](statements.md#st-lc-0118) Compute；code.rdl L878
- [ST-LC-0119](statements.md#st-lc-0119) Compute；code.rdl L881
- [ST-LC-0120](statements.md#st-lc-0120) Compute；code.rdl L886
- [ST-LC-0121](statements.md#st-lc-0121) Compute；code.rdl L835
- [ST-LC-0541](statements.md#st-lc-0541) Compute；code.rdl L841

已剔除的软件接口候选：ST-LC-0501 (SendData), ST-LC-0540 (ProTC)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。",
  "正式单项状态命令未声明NOT_USED/PERMOFF例外，代码单选拒绝；激活PERMOFF另受LC4009.1约束，需需求裁决。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0043 — LC4008

收到命令后将全部AP置为DISABLED；原文义务与当前例外分别保留。

当前保留数据片段：

- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0112](statements.md#st-lc-0112) Compute；code.rdl L861
- [ST-LC-0113](statements.md#st-lc-0113) Compute；code.rdl L833, L864
- [ST-LC-0114](statements.md#st-lc-0114) Compute；code.rdl L866
- [ST-LC-0115](statements.md#st-lc-0115) Compute；code.rdl L869, L883
- [ST-LC-0116](statements.md#st-lc-0116) Compute；code.rdl L872
- [ST-LC-0117](statements.md#st-lc-0117) Compute；code.rdl L875
- [ST-LC-0118](statements.md#st-lc-0118) Compute；code.rdl L878
- [ST-LC-0119](statements.md#st-lc-0119) Compute；code.rdl L881
- [ST-LC-0120](statements.md#st-lc-0120) Compute；code.rdl L886
- [ST-LC-0121](statements.md#st-lc-0121) Compute；code.rdl L835
- [ST-LC-0541](statements.md#st-lc-0541) Compute；code.rdl L841

已剔除的软件接口候选：ST-LC-0501 (SendData), ST-LC-0540 (ProTC)

剩余义务（保留原审查）：

```json
[
  "正式ALL包含NOT_USED/PERMOFF与代码跳过例外、LC4009.1的冲突待裁决；不宣称代码流程全满足ALL原文。",
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0044 — LC4009

收到 Permanent Disable 命令后，使指定AP不能再被Activated。

当前保留数据片段：

- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0122](statements.md#st-lc-0122) Compute；code.rdl L400
- [ST-LC-0123](statements.md#st-lc-0123) Compute；code.rdl L403
- [ST-LC-0124](statements.md#st-lc-0124) Compute；code.rdl L406
- [ST-LC-0125](statements.md#st-lc-0125) Compute；code.rdl L374
- [ST-LC-0543](statements.md#st-lc-0543) Compute；code.rdl L380

已剔除的软件接口候选：ST-LC-0501 (SendData), ST-LC-0542 (ProTC)

剩余义务（保留原审查）：

```json
[
  "LC4009未规定原状态必须Disabled，而代码规定此门控；需需求裁决。",
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0045 — LC4009.1

对已永久禁用AP的激活命令必须拒绝。

当前保留数据片段：

- [ST-LC-0102](statements.md#st-lc-0102) Compute；code.rdl L171, L194, L353, L390, L413, L421, L461, L492, L529, L553, L851, L894, L902, L910, L934, L954
- [ST-LC-0103](statements.md#st-lc-0103) Compute；code.rdl L174, L197, L356, L393, L415, L423, L464, L495, L531, L556, L854, L896, L904, L912, L937, L956
- [ST-LC-0104](statements.md#st-lc-0104) Compute；code.rdl L169, L192, L351, L388, L417, L425, L459, L490, L533, L551, L849, L898, L906, L914, L932, L958
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0116](statements.md#st-lc-0116) Compute；code.rdl L872
- [ST-LC-0118](statements.md#st-lc-0118) Compute；code.rdl L878
- [ST-LC-0121](statements.md#st-lc-0121) Compute；code.rdl L835
- [ST-LC-0124](statements.md#st-lc-0124) Compute；code.rdl L406
- [ST-LC-0543](statements.md#st-lc-0543) Compute；code.rdl L380

已剔除的软件接口候选：ST-LC-0500 (SendData), ST-LC-0542 (ProTC)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0046 — LC4010

重置指定AP的六类统计，保留AP状态和最近结果。

当前保留数据片段：

- [ST-LC-0102](statements.md#st-lc-0102) Compute；code.rdl L171, L194, L353, L390, L413, L421, L461, L492, L529, L553, L851, L894, L902, L910, L934, L954
- [ST-LC-0103](statements.md#st-lc-0103) Compute；code.rdl L174, L197, L356, L393, L415, L423, L464, L495, L531, L556, L854, L896, L904, L912, L937, L956
- [ST-LC-0104](statements.md#st-lc-0104) Compute；code.rdl L169, L192, L351, L388, L417, L425, L459, L490, L533, L551, L849, L898, L906, L914, L932, L958
- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0126](statements.md#st-lc-0126) Compute；code.rdl L502
- [ST-LC-0127](statements.md#st-lc-0127) Compute；code.rdl L504
- [ST-LC-0128](statements.md#st-lc-0128) Compute；code.rdl L509, L521
- [ST-LC-0129](statements.md#st-lc-0129) Compute；code.rdl L507
- [ST-LC-0130](statements.md#st-lc-0130) Compute；code.rdl L513
- [ST-LC-0132](statements.md#st-lc-0132) Compute；code.rdl L519
- [ST-LC-0545](statements.md#st-lc-0545) Compute；code.rdl L482

已剔除的软件接口候选：ST-LC-0500 (SendData), ST-LC-0501 (SendData), ST-LC-0544 (ProTC)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0047 — LC4011

重置所有AP的六类统计，保留AP状态和最近结果。

当前保留数据片段：

- [ST-LC-0102](statements.md#st-lc-0102) Compute；code.rdl L171, L194, L353, L390, L413, L421, L461, L492, L529, L553, L851, L894, L902, L910, L934, L954
- [ST-LC-0103](statements.md#st-lc-0103) Compute；code.rdl L174, L197, L356, L393, L415, L423, L464, L495, L531, L556, L854, L896, L904, L912, L937, L956
- [ST-LC-0104](statements.md#st-lc-0104) Compute；code.rdl L169, L192, L351, L388, L417, L425, L459, L490, L533, L551, L849, L898, L906, L914, L932, L958
- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0126](statements.md#st-lc-0126) Compute；code.rdl L502
- [ST-LC-0127](statements.md#st-lc-0127) Compute；code.rdl L504
- [ST-LC-0128](statements.md#st-lc-0128) Compute；code.rdl L509, L521
- [ST-LC-0129](statements.md#st-lc-0129) Compute；code.rdl L507
- [ST-LC-0130](statements.md#st-lc-0130) Compute；code.rdl L513
- [ST-LC-0132](statements.md#st-lc-0132) Compute；code.rdl L519
- [ST-LC-0545](statements.md#st-lc-0545) Compute；code.rdl L482

已剔除的软件接口候选：ST-LC-0500 (SendData), ST-LC-0501 (SendData), ST-LC-0544 (ProTC)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0048 — LC4012

重置指定WP的八类统计，保留最近结果和age倒计数。

当前保留数据片段：

- [ST-LC-0102](statements.md#st-lc-0102) Compute；code.rdl L171, L194, L353, L390, L413, L421, L461, L492, L529, L553, L851, L894, L902, L910, L934, L954
- [ST-LC-0103](statements.md#st-lc-0103) Compute；code.rdl L174, L197, L356, L393, L415, L423, L464, L495, L531, L556, L854, L896, L904, L912, L937, L956
- [ST-LC-0104](statements.md#st-lc-0104) Compute；code.rdl L169, L192, L351, L388, L417, L425, L459, L490, L533, L551, L849, L898, L906, L914, L932, L958
- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0126](statements.md#st-lc-0126) Compute；code.rdl L502
- [ST-LC-0127](statements.md#st-lc-0127) Compute；code.rdl L504
- [ST-LC-0128](statements.md#st-lc-0128) Compute；code.rdl L509, L521
- [ST-LC-0129](statements.md#st-lc-0129) Compute；code.rdl L507
- [ST-LC-0131](statements.md#st-lc-0131) Compute；code.rdl L516
- [ST-LC-0132](statements.md#st-lc-0132) Compute；code.rdl L519
- [ST-LC-0545](statements.md#st-lc-0545) Compute；code.rdl L482

已剔除的软件接口候选：ST-LC-0500 (SendData), ST-LC-0501 (SendData), ST-LC-0544 (ProTC)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0049 — LC4013

重置所有WP的八类统计，保留最近结果和age倒计数。

当前保留数据片段：

- [ST-LC-0102](statements.md#st-lc-0102) Compute；code.rdl L171, L194, L353, L390, L413, L421, L461, L492, L529, L553, L851, L894, L902, L910, L934, L954
- [ST-LC-0103](statements.md#st-lc-0103) Compute；code.rdl L174, L197, L356, L393, L415, L423, L464, L495, L531, L556, L854, L896, L904, L912, L937, L956
- [ST-LC-0104](statements.md#st-lc-0104) Compute；code.rdl L169, L192, L351, L388, L417, L425, L459, L490, L533, L551, L849, L898, L906, L914, L932, L958
- [ST-LC-0105](statements.md#st-lc-0105) Compute；code.rdl L363, L408, L524, L889, L949
- [ST-LC-0106](statements.md#st-lc-0106) Compute；code.rdl L365, L410, L473, L526, L891, L951
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0126](statements.md#st-lc-0126) Compute；code.rdl L502
- [ST-LC-0127](statements.md#st-lc-0127) Compute；code.rdl L504
- [ST-LC-0128](statements.md#st-lc-0128) Compute；code.rdl L509, L521
- [ST-LC-0129](statements.md#st-lc-0129) Compute；code.rdl L507
- [ST-LC-0131](statements.md#st-lc-0131) Compute；code.rdl L516
- [ST-LC-0132](statements.md#st-lc-0132) Compute；code.rdl L519
- [ST-LC-0545](statements.md#st-lc-0545) Compute；code.rdl L482

已剔除的软件接口候选：ST-LC-0500 (SendData), ST-LC-0501 (SendData), ST-LC-0544 (ProTC)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0050 — LC8000

生成包含六项计数、应用状态、WRT和ART选定信息的housekeeping消息。

当前保留数据片段：

- [ST-LC-0133](statements.md#st-lc-0133) Compute；code.rdl L204
- [ST-LC-0134](statements.md#st-lc-0134) Compute；code.rdl L206, L213
- [ST-LC-0135](statements.md#st-lc-0135) Compute；code.rdl L209
- [ST-LC-0136](statements.md#st-lc-0136) Compute；code.rdl L211
- [ST-LC-0137](statements.md#st-lc-0137) Compute；code.rdl L216, L225
- [ST-LC-0138](statements.md#st-lc-0138) Compute；code.rdl L219
- [ST-LC-0139](statements.md#st-lc-0139) Compute；code.rdl L221
- [ST-LC-0140](statements.md#st-lc-0140) Compute；code.rdl L223
- [ST-LC-0141](statements.md#st-lc-0141) Set；code.rdl L228
- [ST-LC-0142](statements.md#st-lc-0142) Compute；code.rdl L230
- [ST-LC-0143](statements.md#st-lc-0143) Compute；code.rdl L232
- [ST-LC-0533](statements.md#st-lc-0533) Compute；code.rdl L184

已剔除的软件接口候选：ST-LC-0524 (ProTM), ST-LC-0532 (GetData)

剩余义务（保留原审查）：

```json
[
  "独立HK消息入口及CFE_SB_TimeStampMsg/TransmitMsg真实调用的论文资源语法绑定待确认；意图不表示已发送。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0051 — LC9000

cFE Power-On 初始化六项计数、平台默认应用状态以及bitmapped WP/AP结果。

当前保留数据片段：

- [ST-LC-0108](statements.md#st-lc-0108) Compute；code.rdl L443, L471
- [ST-LC-0144](statements.md#st-lc-0144) Compute；code.rdl L241
- [ST-LC-0145](statements.md#st-lc-0145) Compute；code.rdl L243
- [ST-LC-0155](statements.md#st-lc-0155) Compute；code.rdl L246, L287
- [ST-LC-0156](statements.md#st-lc-0156) Compute；code.rdl L248, L284, L289
- [ST-LC-0159](statements.md#st-lc-0159) Compute；code.rdl L255, L296
- [ST-LC-0160](statements.md#st-lc-0160) Set；code.rdl L307
- [ST-LC-0163](statements.md#st-lc-0163) Compute；code.rdl L258, L299
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[
  "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0052 — LC9001

Power-On 将所有WP结果置STALE，比较/连续/累计统计和两向跨越值/时间清零。

当前保留数据片段：

- [ST-LC-0144](statements.md#st-lc-0144) Compute；code.rdl L241
- [ST-LC-0155](statements.md#st-lc-0155) Compute；code.rdl L246, L287
- [ST-LC-0156](statements.md#st-lc-0156) Compute；code.rdl L248, L284, L289
- [ST-LC-0157](statements.md#st-lc-0157) Compute；code.rdl L251, L292
- [ST-LC-0160](statements.md#st-lc-0160) Set；code.rdl L307
- [ST-LC-0163](statements.md#st-lc-0163) Compute；code.rdl L258, L299
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[
  "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0053 — LC9002

Power-On 将所有AP结果置STALE，状态取ADT.DefaultState，六类统计归零。

当前保留数据片段：

- [ST-LC-0144](statements.md#st-lc-0144) Compute；code.rdl L241
- [ST-LC-0155](statements.md#st-lc-0155) Compute；code.rdl L246, L287
- [ST-LC-0156](statements.md#st-lc-0156) Compute；code.rdl L248, L284, L289
- [ST-LC-0158](statements.md#st-lc-0158) Compute；code.rdl L253, L294
- [ST-LC-0160](statements.md#st-lc-0160) Set；code.rdl L307
- [ST-LC-0163](statements.md#st-lc-0163) Compute；code.rdl L258, L299
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[
  "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0054 — LC9003

Processor Reset/LC App Reset 且不保存Critical Data时，采用Power-On等价初始化。

当前保留数据片段：

- [ST-LC-0108](statements.md#st-lc-0108) Compute；code.rdl L443, L471
- [ST-LC-0144](statements.md#st-lc-0144) Compute；code.rdl L241
- [ST-LC-0145](statements.md#st-lc-0145) Compute；code.rdl L243
- [ST-LC-0155](statements.md#st-lc-0155) Compute；code.rdl L246, L287
- [ST-LC-0156](statements.md#st-lc-0156) Compute；code.rdl L248, L284, L289
- [ST-LC-0157](statements.md#st-lc-0157) Compute；code.rdl L251, L292
- [ST-LC-0158](statements.md#st-lc-0158) Compute；code.rdl L253, L294
- [ST-LC-0159](statements.md#st-lc-0159) Compute；code.rdl L255, L296
- [ST-LC-0160](statements.md#st-lc-0160) Set；code.rdl L307
- [ST-LC-0163](statements.md#st-lc-0163) Compute；code.rdl L258, L299
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[
  "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0055 — LC9004

Reset 且保存Critical Data开启时，应恢复HK数据、WDT、WP统计、ADT、AP统计。

当前保留数据片段：

- [ST-LC-0144](statements.md#st-lc-0144) Compute；code.rdl L241
- [ST-LC-0146](statements.md#st-lc-0146) Compute；code.rdl L262
- [ST-LC-0147](statements.md#st-lc-0147) Compute；code.rdl L265
- [ST-LC-0148](statements.md#st-lc-0148) Compute；code.rdl L267
- [ST-LC-0149](statements.md#st-lc-0149) Compute；code.rdl L269
- [ST-LC-0150](statements.md#st-lc-0150) Compute；code.rdl L271
- [ST-LC-0151](statements.md#st-lc-0151) Compute；code.rdl L273
- [ST-LC-0160](statements.md#st-lc-0160) Set；code.rdl L307
- [ST-LC-0161](statements.md#st-lc-0161) Compute；code.rdl L305
- [ST-LC-0163](statements.md#st-lc-0163) Compute；code.rdl L258, L299
- [ST-LC-0551](statements.md#st-lc-0551) Compute；code.rdl L322
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0550 (Init), ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[
  "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
  "源码CriticalData有效性依赖cFE恢复返回及APP保存标志；全部初始化的validation callback保证未由LC源代码单独证明，需核实依赖版本/保证。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0056 — LC9004.1

恢复CDS时，将LC应用状态设置为平台默认Reset State。

当前保留数据片段：

- [ST-LC-0147](statements.md#st-lc-0147) Compute；code.rdl L265
- [ST-LC-0152](statements.md#st-lc-0152) Compute；code.rdl L275
- [ST-LC-0153](statements.md#st-lc-0153) Compute；code.rdl L278
- [ST-LC-0154](statements.md#st-lc-0154) Compute；code.rdl L281
- [ST-LC-0160](statements.md#st-lc-0160) Set；code.rdl L307
- [ST-LC-0551](statements.md#st-lc-0551) Compute；code.rdl L322
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0550 (Init), ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[
  "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0057 — LC9004.1.1

Default Reset State 指定FROM_CDS时，使用CDS恢复的复位前LC应用状态。

当前保留数据片段：

- [ST-LC-0147](statements.md#st-lc-0147) Compute；code.rdl L265
- [ST-LC-0152](statements.md#st-lc-0152) Compute；code.rdl L275
- [ST-LC-0153](statements.md#st-lc-0153) Compute；code.rdl L278
- [ST-LC-0154](statements.md#st-lc-0154) Compute；code.rdl L281
- [ST-LC-0160](statements.md#st-lc-0160) Set；code.rdl L307
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[
  "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0058 — LC9004.2

Critical Data无效时，全套采用Power-On初始化。

当前保留数据片段：

- [ST-LC-0108](statements.md#st-lc-0108) Compute；code.rdl L443, L471
- [ST-LC-0144](statements.md#st-lc-0144) Compute；code.rdl L241
- [ST-LC-0145](statements.md#st-lc-0145) Compute；code.rdl L243
- [ST-LC-0146](statements.md#st-lc-0146) Compute；code.rdl L262
- [ST-LC-0155](statements.md#st-lc-0155) Compute；code.rdl L246, L287
- [ST-LC-0156](statements.md#st-lc-0156) Compute；code.rdl L248, L284, L289
- [ST-LC-0157](statements.md#st-lc-0157) Compute；code.rdl L251, L292
- [ST-LC-0158](statements.md#st-lc-0158) Compute；code.rdl L253, L294
- [ST-LC-0159](statements.md#st-lc-0159) Compute；code.rdl L255, L296
- [ST-LC-0160](statements.md#st-lc-0160) Set；code.rdl L307
- [ST-LC-0161](statements.md#st-lc-0161) Compute；code.rdl L305
- [ST-LC-0163](statements.md#st-lc-0163) Compute；code.rdl L258, L299
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[
  "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
  "源码CriticalData有效性依赖cFE恢复返回及APP保存标志；全部初始化的validation callback保证未由LC源代码单独证明，需核实依赖版本/保证。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0059 — LC9005

任何初始化均应验证WDT的有效算子、数据大小和MID。

当前保留数据片段：

- [ST-LC-0155](statements.md#st-lc-0155) Compute；code.rdl L246, L287
- [ST-LC-0156](statements.md#st-lc-0156) Compute；code.rdl L248, L284, L289
- [ST-LC-0161](statements.md#st-lc-0161) Compute；code.rdl L305
- [ST-LC-0163](statements.md#st-lc-0163) Compute；code.rdl L258, L299
- [ST-LC-0236](statements.md#st-lc-0236) Set；code.rdl L1229
- [ST-LC-0237](statements.md#st-lc-0237) Compute；code.rdl L1231
- [ST-LC-0238](statements.md#st-lc-0238) Compute；code.rdl L1233, L1271
- [ST-LC-0239](statements.md#st-lc-0239) Compute；code.rdl L1236
- [ST-LC-0240](statements.md#st-lc-0240) Compute；code.rdl L1238
- [ST-LC-0241](statements.md#st-lc-0241) Compute；code.rdl L1241
- [ST-LC-0242](statements.md#st-lc-0242) Compute；code.rdl L1244
- [ST-LC-0243](statements.md#st-lc-0243) Compute；code.rdl L1246
- [ST-LC-0244](statements.md#st-lc-0244) Compute；code.rdl L1249
- [ST-LC-0245](statements.md#st-lc-0245) Compute；code.rdl L1251
- [ST-LC-0246](statements.md#st-lc-0246) Compute；code.rdl L1254
- [ST-LC-0247](statements.md#st-lc-0247) Compute；code.rdl L1256
- [ST-LC-0248](statements.md#st-lc-0248) Compute；code.rdl L1259
- [ST-LC-0249](statements.md#st-lc-0249) Compute；code.rdl L1264
- [ST-LC-0250](statements.md#st-lc-0250) Compute；code.rdl L1267
- [ST-LC-0251](statements.md#st-lc-0251) Compute；code.rdl L1269
- [ST-LC-0252](statements.md#st-lc-0252) Compute；code.rdl L1274
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0509 (SendData), ST-LC-0510 (SendData), ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[
  "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
  "源码CriticalData有效性依赖cFE恢复返回及APP保存标志；全部初始化的validation callback保证未由LC源代码单独证明，需核实依赖版本/保证。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0060 — LC9006

任何初始化均应验证ADT的默认状态、RTS号、事件类型、失败次数和RPN语法。

当前保留数据片段：

- [ST-LC-0155](statements.md#st-lc-0155) Compute；code.rdl L246, L287
- [ST-LC-0156](statements.md#st-lc-0156) Compute；code.rdl L248, L284, L289
- [ST-LC-0161](statements.md#st-lc-0161) Compute；code.rdl L305
- [ST-LC-0163](statements.md#st-lc-0163) Compute；code.rdl L258, L299
- [ST-LC-0370](statements.md#st-lc-0370) Compute；code.rdl L12
- [ST-LC-0371](statements.md#st-lc-0371) Compute；code.rdl L14, L83
- [ST-LC-0372](statements.md#st-lc-0372) Compute；code.rdl L17
- [ST-LC-0373](statements.md#st-lc-0373) Compute；code.rdl L20
- [ST-LC-0374](statements.md#st-lc-0374) Compute；code.rdl L23
- [ST-LC-0375](statements.md#st-lc-0375) Compute；code.rdl L26
- [ST-LC-0376](statements.md#st-lc-0376) Compute；code.rdl L29
- [ST-LC-0377](statements.md#st-lc-0377) Compute；code.rdl L32
- [ST-LC-0378](statements.md#st-lc-0378) Compute；code.rdl L35
- [ST-LC-0379](statements.md#st-lc-0379) Compute；code.rdl L37, L44
- [ST-LC-0380](statements.md#st-lc-0380) Compute；code.rdl L40
- [ST-LC-0381](statements.md#st-lc-0381) Compute；code.rdl L42
- [ST-LC-0382](statements.md#st-lc-0382) Compute；code.rdl L47
- [ST-LC-0383](statements.md#st-lc-0383) Compute；code.rdl L50
- [ST-LC-0384](statements.md#st-lc-0384) Compute；code.rdl L53, L57, L61, L65, L69
- [ST-LC-0385](statements.md#st-lc-0385) Compute；code.rdl L73
- [ST-LC-0386](statements.md#st-lc-0386) Compute；code.rdl L76
- [ST-LC-0387](statements.md#st-lc-0387) Compute；code.rdl L78
- [ST-LC-0388](statements.md#st-lc-0388) Compute；code.rdl L81
- [ST-LC-0389](statements.md#st-lc-0389) Compute；code.rdl L86
- [ST-LC-0390](statements.md#st-lc-0390) Compute；code.rdl L88
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0520 (SendData), ST-LC-0521 (SendData), ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[
  "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
  "源码CriticalData有效性依赖cFE恢复返回及APP保存标志；全部初始化的validation callback保证未由LC源代码单独证明，需核实依赖版本/保证。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0061 — LC9007

任何初始化均订阅WDT中定义的消息。

当前保留数据片段：

- [ST-LC-0150](statements.md#st-lc-0150) Compute；code.rdl L271
- [ST-LC-0162](statements.md#st-lc-0162) Compute；code.rdl L309
- [ST-LC-0164](statements.md#st-lc-0164) Compute；code.rdl L994
- [ST-LC-0165](statements.md#st-lc-0165) Compute；code.rdl L996, L1003
- [ST-LC-0166](statements.md#st-lc-0166) Compute；code.rdl L999
- [ST-LC-0167](statements.md#st-lc-0167) Compute；code.rdl L1001
- [ST-LC-0168](statements.md#st-lc-0168) Compute；code.rdl L1006
- [ST-LC-0169](statements.md#st-lc-0169) Compute；code.rdl L1008, L1027
- [ST-LC-0170](statements.md#st-lc-0170) Compute；code.rdl L1011
- [ST-LC-0171](statements.md#st-lc-0171) Compute；code.rdl L1014
- [ST-LC-0172](statements.md#st-lc-0172) Compute；code.rdl L1017
- [ST-LC-0173](statements.md#st-lc-0173) Compute；code.rdl L1019
- [ST-LC-0174](statements.md#st-lc-0174) Compute；code.rdl L1022
- [ST-LC-0175](statements.md#st-lc-0175) Compute；code.rdl L1025
- [ST-LC-0176](statements.md#st-lc-0176) Set；code.rdl L1030
- [ST-LC-0177](statements.md#st-lc-0177) Compute；code.rdl L988
- [ST-LC-0547](statements.md#st-lc-0547) Compute；code.rdl L316
- [ST-LC-0549](statements.md#st-lc-0549) Compute；code.rdl L319
- [ST-LC-0551](statements.md#st-lc-0551) Compute；code.rdl L322
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0502 (SendData), ST-LC-0546 (Init), ST-LC-0548 (Init), ST-LC-0550 (Init), ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[
  "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
  "实际SB Subscribe执行与失败事件提交待论文软件服务资源绑定；只形成数据和意图不能声称完成订阅。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0062 — LC9007.1

Processor Reset 且Save Critical Data开启时，订阅CDS恢复WDT中的消息。

当前保留数据片段：

- [ST-LC-0150](statements.md#st-lc-0150) Compute；code.rdl L271
- [ST-LC-0162](statements.md#st-lc-0162) Compute；code.rdl L309
- [ST-LC-0164](statements.md#st-lc-0164) Compute；code.rdl L994
- [ST-LC-0168](statements.md#st-lc-0168) Compute；code.rdl L1006
- [ST-LC-0169](statements.md#st-lc-0169) Compute；code.rdl L1008, L1027
- [ST-LC-0170](statements.md#st-lc-0170) Compute；code.rdl L1011
- [ST-LC-0171](statements.md#st-lc-0171) Compute；code.rdl L1014
- [ST-LC-0172](statements.md#st-lc-0172) Compute；code.rdl L1017
- [ST-LC-0173](statements.md#st-lc-0173) Compute；code.rdl L1019
- [ST-LC-0174](statements.md#st-lc-0174) Compute；code.rdl L1022
- [ST-LC-0175](statements.md#st-lc-0175) Compute；code.rdl L1025
- [ST-LC-0176](statements.md#st-lc-0176) Set；code.rdl L1030
- [ST-LC-0177](statements.md#st-lc-0177) Compute；code.rdl L988
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0502 (SendData), ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[
  "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
  "实际SB Subscribe执行与失败事件提交待论文软件服务资源绑定；只形成数据和意图不能声称完成订阅。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0063 — LC9007.2

Application Reset 且Save Critical Data开启时，订阅CDS恢复WDT中的消息。

当前保留数据片段：

- [ST-LC-0150](statements.md#st-lc-0150) Compute；code.rdl L271
- [ST-LC-0162](statements.md#st-lc-0162) Compute；code.rdl L309
- [ST-LC-0164](statements.md#st-lc-0164) Compute；code.rdl L994
- [ST-LC-0168](statements.md#st-lc-0168) Compute；code.rdl L1006
- [ST-LC-0169](statements.md#st-lc-0169) Compute；code.rdl L1008, L1027
- [ST-LC-0170](statements.md#st-lc-0170) Compute；code.rdl L1011
- [ST-LC-0171](statements.md#st-lc-0171) Compute；code.rdl L1014
- [ST-LC-0172](statements.md#st-lc-0172) Compute；code.rdl L1017
- [ST-LC-0173](statements.md#st-lc-0173) Compute；code.rdl L1019
- [ST-LC-0174](statements.md#st-lc-0174) Compute；code.rdl L1022
- [ST-LC-0175](statements.md#st-lc-0175) Compute；code.rdl L1025
- [ST-LC-0176](statements.md#st-lc-0176) Set；code.rdl L1030
- [ST-LC-0177](statements.md#st-lc-0177) Compute；code.rdl L988
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0502 (SendData), ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[
  "启动/复位入口与cFE Table/CDS的真实注册、加载、地址获取、恢复服务调用严格论文软件资源绑定未核定；外部返回/聚合数据序列化和任务部署配置仍待确认。",
  "实际SB Subscribe执行与失败事件提交待论文软件服务资源绑定；只形成数据和意图不能声称完成订阅。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0064 — None

WP时效由有效带UpdateAge请求推进；先AP求值再推进age，0阈值不自行过期。

当前保留数据片段：

- [ST-LC-0253](statements.md#st-lc-0253) Set；code.rdl L788, L1042
- [ST-LC-0254](statements.md#st-lc-0254) Compute；code.rdl L790, L1044
- [ST-LC-0255](statements.md#st-lc-0255) Compute；code.rdl L793, L1047
- [ST-LC-0256](statements.md#st-lc-0256) Compute；code.rdl L795, L814, L1049, L1068
- [ST-LC-0257](statements.md#st-lc-0257) Compute；code.rdl L798, L1052
- [ST-LC-0258](statements.md#st-lc-0258) Compute；code.rdl L800, L1054
- [ST-LC-0259](statements.md#st-lc-0259) Set；code.rdl L803, L1057
- [ST-LC-0260](statements.md#st-lc-0260) Compute；code.rdl L805, L1059
- [ST-LC-0261](statements.md#st-lc-0261) Set；code.rdl L808, L1062
- [ST-LC-0262](statements.md#st-lc-0262) Compute；code.rdl L812, L1066
- [ST-LC-0300](statements.md#st-lc-0300) Compute；code.rdl L563
- [ST-LC-0301](statements.md#st-lc-0301) Compute；code.rdl L565
- [ST-LC-0302](statements.md#st-lc-0302) Compute；code.rdl L568
- [ST-LC-0303](statements.md#st-lc-0303) Compute；code.rdl L821
- [ST-LC-0305](statements.md#st-lc-0305) Compute；code.rdl L777
- [ST-LC-0367](statements.md#st-lc-0367) Compute；code.rdl L782
- [ST-LC-0368](statements.md#st-lc-0368) Compute；code.rdl L785
- [ST-LC-0369](statements.md#st-lc-0369) Compute；code.rdl L825
- [ST-LC-0396](statements.md#st-lc-0396) Compute；code.rdl L780

已剔除的软件接口候选：ST-LC-0511 (SendData), ST-LC-0512 (SendData)

剩余义务（保留原审查）：

```json
[
  "正倒数减1/到0置STALE以及FALSE/TRUE加载阈值、ERROR/STALE倒数清0已由WP操作表达，ST0368已在同次采样内联ST0253–0262；聚合/字段别名的官方加载格式仍待确认。",
  "次数不是秒/毫秒，真实请求节奏外部未知；不增造周期。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0065 — None

执行源码的偏移/类型门控后按BE/LE取数、扩展和掩码；极端偏移回绕放行时后续值未知。

当前保留数据片段：

- [ST-LC-0200](statements.md#st-lc-0200) Set；code.rdl L1112
- [ST-LC-0206](statements.md#st-lc-0206) Compute；code.rdl L1124, L1203
- [ST-LC-0207](statements.md#st-lc-0207) Compute；code.rdl L1127
- [ST-LC-0208](statements.md#st-lc-0208) Compute；code.rdl L1129
- [ST-LC-0209](statements.md#st-lc-0209) Compute；code.rdl L1132
- [ST-LC-0210](statements.md#st-lc-0210) Compute；code.rdl L1190
- [ST-LC-0211](statements.md#st-lc-0211) Compute；code.rdl L1182, L1194
- [ST-LC-0212](statements.md#st-lc-0212) Set；code.rdl L1184, L1196
- [ST-LC-0213](statements.md#st-lc-0213) Set；code.rdl L1186, L1198
- [ST-LC-0214](statements.md#st-lc-0214) Compute；code.rdl L1135
- [ST-LC-0215](statements.md#st-lc-0215) Compute；code.rdl L1137
- [ST-LC-0216](statements.md#st-lc-0216) Compute；code.rdl L1140
- [ST-LC-0219](statements.md#st-lc-0219) Compute；code.rdl L1148
- [ST-LC-0232](statements.md#st-lc-0232) Compute；code.rdl L1206
- [ST-LC-0235](statements.md#st-lc-0235) Compute；code.rdl L1214, L1219

已剔除的软件接口候选：ST-LC-0506 (SendData), ST-LC-0508 (SendData)

剩余义务（保留原审查）：

```json
[
  "ISSUE0021/0004 C算术/接口与风险指针实际行为未知；希望安全算法不混成已实现要求。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0066 — None

当前实现把STALE→TRUE也当FalseToTrue跨越，STALE→FALSE也保存LastTrueToFalse；正式统计含义需确认。

当前保留数据片段：

- [ST-LC-0200](statements.md#st-lc-0200) Set；code.rdl L1112
- [ST-LC-0223](statements.md#st-lc-0223) Compute；code.rdl L1157
- [ST-LC-0228](statements.md#st-lc-0228) Compute；code.rdl L1173
- [ST-LC-0229](statements.md#st-lc-0229) Compute；code.rdl L1176
- [ST-LC-0230](statements.md#st-lc-0230) Set；code.rdl L1179
- [ST-LC-0264](statements.md#st-lc-0264) Compute；code.rdl L1098
- [ST-LC-0265](statements.md#st-lc-0265) Compute；code.rdl L1101
- [ST-LC-0266](statements.md#st-lc-0266) Set；code.rdl L1103

已剔除的软件接口候选：无直接关联；仍有系统入口/资源绑定缺口

剩余义务（保留原审查）：

```json
[
  "补充事实不改原正式要求；ISSUE0006开放，持久绑定pending-interface。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0067 — None

WP ERROR/STALE分支清时效倒计数，但保持已有连续TRUE计数；不误补为连续TRUE归零。

当前保留数据片段：

- [ST-LC-0200](statements.md#st-lc-0200) Set；code.rdl L1112
- [ST-LC-0211](statements.md#st-lc-0211) Compute；code.rdl L1182, L1194
- [ST-LC-0212](statements.md#st-lc-0212) Set；code.rdl L1184, L1196
- [ST-LC-0213](statements.md#st-lc-0213) Set；code.rdl L1186, L1198
- [ST-LC-0215](statements.md#st-lc-0215) Compute；code.rdl L1137
- [ST-LC-0219](statements.md#st-lc-0219) Compute；code.rdl L1148
- [ST-LC-0220](statements.md#st-lc-0220) Set；code.rdl L1151
- [ST-LC-0221](statements.md#st-lc-0221) Compute；code.rdl L1153
- [ST-LC-0222](statements.md#st-lc-0222) Set；code.rdl L1155
- [ST-LC-0225](statements.md#st-lc-0225) Compute；code.rdl L1163
- [ST-LC-0227](statements.md#st-lc-0227) Compute；code.rdl L1169
- [ST-LC-0230](statements.md#st-lc-0230) Set；code.rdl L1179

已剔除的软件接口候选：ST-LC-0506 (SendData), ST-LC-0508 (SendData)

剩余义务（保留原审查）：

```json
[
  "真实入口、EVS、持久提交pending-interface；本规则与FALSE清连续TRUE分别走查。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0068 — None

AP STALE清连续FAIL；AP ERROR保留连续FAIL并发错误事件，不应推导ERROR中断失败连续性。

当前保留数据片段：

- [ST-LC-0322](statements.md#st-lc-0322) Compute；code.rdl L626
- [ST-LC-0323](statements.md#st-lc-0323) Compute；code.rdl L629
- [ST-LC-0324](statements.md#st-lc-0324) Set；code.rdl L631
- [ST-LC-0326](statements.md#st-lc-0326) Compute；code.rdl L636
- [ST-LC-0327](statements.md#st-lc-0327) Set；code.rdl L638
- [ST-LC-0356](statements.md#st-lc-0356) Compute；code.rdl L726
- [ST-LC-0362](statements.md#st-lc-0362) Set；code.rdl L747, L755
- [ST-LC-0363](statements.md#st-lc-0363) Compute；code.rdl L752
- [ST-LC-0364](statements.md#st-lc-0364) Compute；code.rdl L760
- [ST-LC-0365](statements.md#st-lc-0365) Compute；code.rdl L722, L749, L757, L762
- [ST-LC-0394](statements.md#st-lc-0394) Compute；code.rdl L112

已剔除的软件接口候选：ST-LC-0513 (SendData), ST-LC-0519 (SendData)

剩余义务（保留原审查）：

```json
[
  "ERROR间隔是否中断业务连续性待ISSUE-LC-0017；真实错误事件提交pending-interface。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0069 — None

AP范围采样先检查首项可操作状态；首项NOT_USED/PERMOFF会拒绝整个范围，即使后续AP可用。

当前保留数据片段：

- [ST-LC-0300](statements.md#st-lc-0300) Compute；code.rdl L563
- [ST-LC-0302](statements.md#st-lc-0302) Compute；code.rdl L568
- [ST-LC-0303](statements.md#st-lc-0303) Compute；code.rdl L821
- [ST-LC-0304](statements.md#st-lc-0304) Compute；code.rdl L571
- [ST-LC-0305](statements.md#st-lc-0305) Compute；code.rdl L777
- [ST-LC-0306](statements.md#st-lc-0306) Compute；code.rdl L574
- [ST-LC-0307](statements.md#st-lc-0307) Compute；code.rdl L576, L773
- [ST-LC-0308](statements.md#st-lc-0308) Compute；code.rdl L579
- [ST-LC-0309](statements.md#st-lc-0309) Compute；code.rdl L768
- [ST-LC-0366](statements.md#st-lc-0366) Compute；code.rdl L771
- [ST-LC-0367](statements.md#st-lc-0367) Compute；code.rdl L782
- [ST-LC-0368](statements.md#st-lc-0368) Compute；code.rdl L785
- [ST-LC-0391](statements.md#st-lc-0391) Compute；code.rdl L106
- [ST-LC-0396](statements.md#st-lc-0396) Compute；code.rdl L780

已剔除的软件接口候选：ST-LC-0511 (SendData), ST-LC-0512 (SendData)

剩余义务（保留原审查）：

```json
[
  "该实现与正式请求逐项义务的冲突按ISSUE-LC-0015保留；跨贡献末尾年龄尚需集成。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0070 — None

达到连续FAIL阈值的ACTIVE AP先转PASSIVE，随后由应用状态决定发RTS或只记被动抑制。

当前保留数据片段：

- [ST-LC-0337](statements.md#st-lc-0337) Compute；code.rdl L662
- [ST-LC-0338](statements.md#st-lc-0338) Compute；code.rdl L665
- [ST-LC-0339](statements.md#st-lc-0339) Set；code.rdl L668
- [ST-LC-0340](statements.md#st-lc-0340) Compute；code.rdl L670
- [ST-LC-0349](statements.md#st-lc-0349) Compute；code.rdl L694, L706
- [ST-LC-0350](statements.md#st-lc-0350) Set；code.rdl L696, L708
- [ST-LC-0351](statements.md#st-lc-0351) Compute；code.rdl L698
- [ST-LC-0392](statements.md#st-lc-0392) Set；code.rdl L94
- [ST-LC-0394](statements.md#st-lc-0394) Compute；code.rdl L112

已剔除的软件接口候选：ST-LC-0516 (SendData)

剩余义务（保留原审查）：

```json
[
  "EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。",
  "与原Once initiated状态时机及总事件口径差异分别保留ISSUE-LC-0007/0017。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0071 — None

RTS适配函数构造任务配置MID/命令码/RTSId的请求包；发送返回码被忽略，计数表示尝试。

当前保留数据片段：

- [ST-LC-0340](statements.md#st-lc-0340) Compute；code.rdl L670
- [ST-LC-0341](statements.md#st-lc-0341) Compute；code.rdl L673
- [ST-LC-0342](statements.md#st-lc-0342) Compute；code.rdl L675
- [ST-LC-0343](statements.md#st-lc-0343) Compute；code.rdl L677
- [ST-LC-0344](statements.md#st-lc-0344) Set；code.rdl L679
- [ST-LC-0345](statements.md#st-lc-0345) Compute；code.rdl L681
- [ST-LC-0346](statements.md#st-lc-0346) Set；code.rdl L683
- [ST-LC-0394](statements.md#st-lc-0394) Compute；code.rdl L112

已剔除的软件接口候选：ST-LC-0523 (SendData)

剩余义务（保留原审查）：

```json
[
  "EVS/SB待提交描述已分开，不代表实际服务调用或成功；软件资源提交/失败语法pending-interface。",
  "实际软件接口原子语法和依赖线格式未确认；不补造SC回执。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0072 — None

状态命令不能改变NOT_USED/PERMOFF；全选略过它们，单选拒绝。

当前保留数据片段：

- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0112](statements.md#st-lc-0112) Compute；code.rdl L861
- [ST-LC-0113](statements.md#st-lc-0113) Compute；code.rdl L833, L864
- [ST-LC-0114](statements.md#st-lc-0114) Compute；code.rdl L866
- [ST-LC-0115](statements.md#st-lc-0115) Compute；code.rdl L869, L883
- [ST-LC-0116](statements.md#st-lc-0116) Compute；code.rdl L872
- [ST-LC-0117](statements.md#st-lc-0117) Compute；code.rdl L875
- [ST-LC-0118](statements.md#st-lc-0118) Compute；code.rdl L878
- [ST-LC-0119](statements.md#st-lc-0119) Compute；code.rdl L881
- [ST-LC-0120](statements.md#st-lc-0120) Compute；code.rdl L886
- [ST-LC-0547](statements.md#st-lc-0547) Compute；code.rdl L316
- [ST-LC-0549](statements.md#st-lc-0549) Compute；code.rdl L319
- [ST-LC-0551](statements.md#st-lc-0551) Compute；code.rdl L322

已剔除的软件接口候选：ST-LC-0546 (Init), ST-LC-0548 (Init), ST-LC-0550 (Init)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0073 — None

永久关闭命令仅允许单个已DISABLED AP，拒绝ALL和其他原状态。

当前保留数据片段：

- [ST-LC-0102](statements.md#st-lc-0102) Compute；code.rdl L171, L194, L353, L390, L413, L421, L461, L492, L529, L553, L851, L894, L902, L910, L934, L954
- [ST-LC-0103](statements.md#st-lc-0103) Compute；code.rdl L174, L197, L356, L393, L415, L423, L464, L495, L531, L556, L854, L896, L904, L912, L937, L956
- [ST-LC-0104](statements.md#st-lc-0104) Compute；code.rdl L169, L192, L351, L388, L417, L425, L459, L490, L533, L551, L849, L898, L906, L914, L932, L958
- [ST-LC-0107](statements.md#st-lc-0107) Set；code.rdl L177, L200, L359, L367, L396, L428, L467, L475, L498, L536, L559, L857, L917, L940, L961
- [ST-LC-0122](statements.md#st-lc-0122) Compute；code.rdl L400
- [ST-LC-0123](statements.md#st-lc-0123) Compute；code.rdl L403
- [ST-LC-0124](statements.md#st-lc-0124) Compute；code.rdl L406
- [ST-LC-0125](statements.md#st-lc-0125) Compute；code.rdl L374

已剔除的软件接口候选：ST-LC-0500 (SendData)

剩余义务（保留原审查）：

```json
[
  "已表达命令业务计算/状态提交与事件描述；原消息入口、CFE_EVS_SendEvent实际提交及软件接口资源绑定严格论文语法尚未核定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0074 — None

统计重置和表初始化分离：重置保留结果/状态/age；初始化重置结果为STALE且AP采用ADT默认状态。

当前保留数据片段：

- [ST-LC-0108](statements.md#st-lc-0108) Compute；code.rdl L443, L471
- [ST-LC-0126](statements.md#st-lc-0126) Compute；code.rdl L502
- [ST-LC-0128](statements.md#st-lc-0128) Compute；code.rdl L509, L521
- [ST-LC-0129](statements.md#st-lc-0129) Compute；code.rdl L507
- [ST-LC-0130](statements.md#st-lc-0130) Compute；code.rdl L513
- [ST-LC-0131](statements.md#st-lc-0131) Compute；code.rdl L516
- [ST-LC-0132](statements.md#st-lc-0132) Compute；code.rdl L519
- [ST-LC-0157](statements.md#st-lc-0157) Compute；code.rdl L251, L292
- [ST-LC-0158](statements.md#st-lc-0158) Compute；code.rdl L253, L294
- [ST-LC-0179](statements.md#st-lc-0179) Compute；code.rdl L973
- [ST-LC-0181](statements.md#st-lc-0181) Compute；code.rdl L979
- [ST-LC-0182](statements.md#st-lc-0182) Set；code.rdl L982
- [ST-LC-0557](statements.md#st-lc-0557) Compute；code.rdl L968
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0556 (GetData), ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0075 — None

WDT替换后清旧WRT并取消/重建订阅；ADT替换后清旧ART并采用新DefaultState。

当前保留数据片段：

- [ST-LC-0164](statements.md#st-lc-0164) Compute；code.rdl L994
- [ST-LC-0165](statements.md#st-lc-0165) Compute；code.rdl L996, L1003
- [ST-LC-0166](statements.md#st-lc-0166) Compute；code.rdl L999
- [ST-LC-0167](statements.md#st-lc-0167) Compute；code.rdl L1001
- [ST-LC-0168](statements.md#st-lc-0168) Compute；code.rdl L1006
- [ST-LC-0169](statements.md#st-lc-0169) Compute；code.rdl L1008, L1027
- [ST-LC-0170](statements.md#st-lc-0170) Compute；code.rdl L1011
- [ST-LC-0171](statements.md#st-lc-0171) Compute；code.rdl L1014
- [ST-LC-0172](statements.md#st-lc-0172) Compute；code.rdl L1017
- [ST-LC-0173](statements.md#st-lc-0173) Compute；code.rdl L1019
- [ST-LC-0174](statements.md#st-lc-0174) Compute；code.rdl L1022
- [ST-LC-0175](statements.md#st-lc-0175) Compute；code.rdl L1025
- [ST-LC-0176](statements.md#st-lc-0176) Set；code.rdl L1030
- [ST-LC-0177](statements.md#st-lc-0177) Compute；code.rdl L988
- [ST-LC-0178](statements.md#st-lc-0178) Compute；code.rdl L970
- [ST-LC-0179](statements.md#st-lc-0179) Compute；code.rdl L973
- [ST-LC-0180](statements.md#st-lc-0180) Compute；code.rdl L976
- [ST-LC-0181](statements.md#st-lc-0181) Compute；code.rdl L979
- [ST-LC-0182](statements.md#st-lc-0182) Set；code.rdl L982
- [ST-LC-0557](statements.md#st-lc-0557) Compute；code.rdl L968

已剔除的软件接口候选：ST-LC-0502 (SendData), ST-LC-0556 (GetData)

剩余义务（保留原审查）：

```json
[
  "CFE_TBL_Manage/ReleaseAddress/GetAddress、真实订阅更新和fatal return的软件接口绑定待确认；HK发送后及ReceiveBuffer超时两种原维护触发独立保留。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0076 — None

CDS恢复采用五对象全或无策略；保存失败会禁用后续CDS并继续应用。

当前保留数据片段：

- [ST-LC-0146](statements.md#st-lc-0146) Compute；code.rdl L262
- [ST-LC-0147](statements.md#st-lc-0147) Compute；code.rdl L265
- [ST-LC-0148](statements.md#st-lc-0148) Compute；code.rdl L267
- [ST-LC-0149](statements.md#st-lc-0149) Compute；code.rdl L269
- [ST-LC-0150](statements.md#st-lc-0150) Compute；code.rdl L271
- [ST-LC-0151](statements.md#st-lc-0151) Compute；code.rdl L273
- [ST-LC-0155](statements.md#st-lc-0155) Compute；code.rdl L246, L287
- [ST-LC-0157](statements.md#st-lc-0157) Compute；code.rdl L251, L292
- [ST-LC-0158](statements.md#st-lc-0158) Compute；code.rdl L253, L294
- [ST-LC-0159](statements.md#st-lc-0159) Compute；code.rdl L255, L296
- [ST-LC-0160](statements.md#st-lc-0160) Set；code.rdl L307
- [ST-LC-0162](statements.md#st-lc-0162) Compute；code.rdl L309
- [ST-LC-0183](statements.md#st-lc-0183) Compute；code.rdl L118
- [ST-LC-0184](statements.md#st-lc-0184) Compute；code.rdl L121
- [ST-LC-0185](statements.md#st-lc-0185) Compute；code.rdl L123
- [ST-LC-0186](statements.md#st-lc-0186) Compute；code.rdl L126
- [ST-LC-0187](statements.md#st-lc-0187) Compute；code.rdl L128
- [ST-LC-0188](statements.md#st-lc-0188) Compute；code.rdl L131
- [ST-LC-0189](statements.md#st-lc-0189) Set；code.rdl L133
- [ST-LC-0190](statements.md#st-lc-0190) Compute；code.rdl L135
- [ST-LC-0191](statements.md#st-lc-0191) Compute；code.rdl L137
- [ST-LC-0192](statements.md#st-lc-0192) Compute；code.rdl L141, L147, L153
- [ST-LC-0193](statements.md#st-lc-0193) Set；code.rdl L143, L149, L155
- [ST-LC-0559](statements.md#st-lc-0559) Compute；code.rdl L239

已剔除的软件接口候选：ST-LC-0503 (SendData), ST-LC-0525 (SendData), ST-LC-0526 (SendData), ST-LC-0527 (SendData), ST-LC-0558 (GetData)

剩余义务（保留原审查）：

```json
[
  "三次CopyToCDS实际提交、逐阶段返回获取、失败EVS事件与维护入口绑定待论文软件资源确认；计算意图和被绑定返回值之间没有被模型伪装成执行。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0077 — None

HK压缩将PERMOFF编码为NOT_USED，完整ART dump才保留两者差异。

当前保留数据片段：

- [ST-LC-0133](statements.md#st-lc-0133) Compute；code.rdl L204
- [ST-LC-0134](statements.md#st-lc-0134) Compute；code.rdl L206, L213
- [ST-LC-0135](statements.md#st-lc-0135) Compute；code.rdl L209
- [ST-LC-0137](statements.md#st-lc-0137) Compute；code.rdl L216, L225
- [ST-LC-0138](statements.md#st-lc-0138) Compute；code.rdl L219
- [ST-LC-0139](statements.md#st-lc-0139) Compute；code.rdl L221
- [ST-LC-0141](statements.md#st-lc-0141) Set；code.rdl L228
- [ST-LC-0149](statements.md#st-lc-0149) Compute；code.rdl L269

已剔除的软件接口候选：ST-LC-0524 (ProTM)

剩余义务（保留原审查）：

```json
[
  "完整ART dump由cFE Table Services实际导出，软件服务论文绑定待确认。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0078 — None

普通与EDS分发是条件构建分支；当前EDS表仅路由CMD/HK，与普通SampleAP/WP路由不等价。

当前保留数据片段：

- [ST-LC-0194](statements.md#st-lc-0194) Compute；code.rdl L330
- [ST-LC-0195](statements.md#st-lc-0195) Compute；code.rdl L336
- [ST-LC-0196](statements.md#st-lc-0196) Compute；code.rdl L333

已剔除的软件接口候选：ST-LC-0504 (SendData)

剩余义务（保留原审查）：

```json
[
  "任务是否开启CFE_EDS_ENABLED、EDS字典/dispatcher依赖版本及真实失败返回待确认；未提供SampleAP/WP handler不能推定EDS与普通语义等价。",
  "真实ReceiveBuffer、EdsDispatch、EDS拒绝CmdErrCount持久写回及EVS提交尚未取得论文软件服务绑定。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0079 — None

默认custom钩子没有任务计算：发Unexpected错误事件但返回FALSE。

当前保留数据片段：

- [ST-LC-0200](statements.md#st-lc-0200) Set；code.rdl L1112
- [ST-LC-0217](statements.md#st-lc-0217) Compute；code.rdl L1142
- [ST-LC-0218](statements.md#st-lc-0218) Compute；code.rdl L1145
- [ST-LC-0220](statements.md#st-lc-0220) Set；code.rdl L1151
- [ST-LC-0226](statements.md#st-lc-0226) Compute；code.rdl L1166
- [ST-LC-0230](statements.md#st-lc-0230) Set；code.rdl L1179
- [ST-LC-0269](statements.md#st-lc-0269) Compute；code.rdl L1076

已剔除的软件接口候选：ST-LC-0507 (SendData)

剩余义务（保留原审查）：

```json
[
  "ISSUE0020任务custom缺失；不能因错误事件把返回结果改ERROR或认定业务算法满足。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0080 — None

LC采用两个独立消息入口，AP调度频率是外部任务配置；不能将WP接收和AP评估强行并为一个周期。

当前保留数据片段：

- [ST-LC-0101](statements.md#st-lc-0101) Compute；code.rdl L163, L186, L345, L382, L453, L484, L545, L843, L926
- [ST-LC-0194](statements.md#st-lc-0194) Compute；code.rdl L330
- [ST-LC-0195](statements.md#st-lc-0195) Compute；code.rdl L336
- [ST-LC-0196](statements.md#st-lc-0196) Compute；code.rdl L333
- [ST-LC-0529](statements.md#st-lc-0529) Compute；code.rdl L1110
- [ST-LC-0531](statements.md#st-lc-0531) Compute；code.rdl L543
- [ST-LC-0549](statements.md#st-lc-0549) Compute；code.rdl L319

已剔除的软件接口候选：ST-LC-0504 (SendData), ST-LC-0528 (GetData), ST-LC-0530 (GetData), ST-LC-0548 (Init)

剩余义务（保留原审查）：

```json
[
  "消息接收、分发到各独立Composite入口的系统声明，以及外部调度任务周期尚未绑定；没有在SpaceRDL补造固定周期。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0081 — None

任务部署需保持WDT与ADT一致；两表更新不是原子事务，必要时先将应用DISABLED。

当前保留数据片段：

- [ST-LC-0320](statements.md#st-lc-0320) Compute；code.rdl L613
- [ST-LC-0370](statements.md#st-lc-0370) Compute；code.rdl L12
- [ST-LC-0378](statements.md#st-lc-0378) Compute；code.rdl L35
- [ST-LC-0380](statements.md#st-lc-0380) Compute；code.rdl L40
- [ST-LC-0382](statements.md#st-lc-0382) Compute；code.rdl L47
- [ST-LC-0395](statements.md#st-lc-0395) Compute；code.rdl L1036
- [ST-LC-0555](statements.md#st-lc-0555) Compute；code.rdl L10

已剔除的软件接口候选：ST-LC-0554 (GetData)

剩余义务（保留原审查）：

```json
[
  "缺实际任务表集合与更新策略，不能补造原子跨表事务或默认禁用命令；其他独立校验不受影响。"
]
```

最终范围：仅数据处理片段；非完整系统转换。

## REQ-LC-0082 — None

平台容量除数量上界外还须满足HK打包粒度及cFE单表最大尺寸约束。

当前保留数据片段：

- [ST-LC-0134](statements.md#st-lc-0134) Compute；code.rdl L206, L213
- [ST-LC-0135](statements.md#st-lc-0135) Compute；code.rdl L209
- [ST-LC-0136](statements.md#st-lc-0136) Compute；code.rdl L211
- [ST-LC-0137](statements.md#st-lc-0137) Compute；code.rdl L216, L225
- [ST-LC-0138](statements.md#st-lc-0138) Compute；code.rdl L219
- [ST-LC-0139](statements.md#st-lc-0139) Compute；code.rdl L221
- [ST-LC-0140](statements.md#st-lc-0140) Compute；code.rdl L223
- [ST-LC-0197](statements.md#st-lc-0197) Compute；code.rdl L435
- [ST-LC-0198](statements.md#st-lc-0198) Compute；code.rdl L437

已剔除的软件接口候选：无直接关联；仍有系统入口/资源绑定缺口

剩余义务（保留原审查）：

```json
[
  "实际部署LC_MAX_*、结构ABI sizeof及CFE_PLATFORM_TBL_MAX_SNGL_TABLE_SIZE未固定，不能对部署容量契约给成功结论。"
]
```

最终范围：仅数据处理片段；非完整系统转换。
