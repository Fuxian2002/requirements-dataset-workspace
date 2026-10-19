# NASA cFS Memory Dwell 需求文档生成说明

本目录中的 `NASA cFS Memory Dwell 软件需求规格说明.docx` 是从 NASA Memory Dwell（MD）应用的正式需求、设计资料、接口定义、平台配置和 C 源码逆向整理得到的自然语言需求规格说明。

## 原始项目基线

- 官方仓库：<https://github.com/nasa/MD>
- 固定提交：`7e027886b22eb9e6492d59700cdc4549b116c698`
- 版本基线：v7.0.1
- 描述边界：完整 MD 应用，包括地面命令、驻留表、内存读取、驻留遥测、管家遥测、事件和复位恢复

## 主要逆向资料

### 正式需求与设计资料

- `docs/md_FunctionalRequirements.csv`：NASA 项目给出的功能需求编号、需求陈述和层级关系，是正文和追踪矩阵的重要上游依据。
- `docs/dox_src/cfs_md.dox`：应用概述、运行方式、命令、表和遥测说明。
- `docs/users_guide_historical/MD_DevelopersGuide.docx`：历史开发者指南，用于补充设计背景、接口语义和运行流程。
- `README.md`：项目定位、构建方式和与 cFS 的集成关系。

### 配置与接口资料

- `fsw/inc/md_interface_cfg.h`、`md_internal_cfg.h`：驻留表数量、表项数量、管道深度等接口和内部配置。
- `fsw/inc/md_fcncodes.h`、`md_topicids.h`、`md_eventids.h`：命令码、消息主题和事件定义。
- `config/default_md_*`：默认任务、平台、消息、表结构和功能码配置。
- `eds/MD.xml`：命令、驻留表、管家遥测和驻留遥测的数据结构定义。
- `fsw/tables/md_dw01.c`～`md_dw04.c`：四张默认驻留表实例。

### 关键实现资料

- `fsw/src/md_app.c`、`md_dispatch.c`：应用初始化、软件总线接入和消息分派。
- `fsw/src/md_cmds.c`：No-op、复位、启动、停止、Jam、签名等地面命令处理。
- `fsw/src/md_dwell_tbl.c`：驻留表注册、验证、派生字段和恢复处理。
- `fsw/src/md_dwell_pkt.c`：周期驻留调度、内存采样和驻留包发送。
- `fsw/src/md_utils.c`：符号解析、地址校验及平台内存访问辅助处理。
- `unit-test/`：异常分支、边界条件和接口行为的辅助核对资料。

## 形成方式

先以 NASA 正式需求表恢复应覆盖的能力，再依据 EDS、配置头文件和默认表确定消息、表项及平台边界；随后沿应用入口、消息分派、命令处理、驻留调度、目标内存读取和遥测发送链路核对每项处理过程。历史指南只用于补充语义，最终描述以固定版本的当前接口和 C 实现为准。

