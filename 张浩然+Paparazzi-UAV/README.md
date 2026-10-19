# Paparazzi UAV 需求文档生成说明

本目录中的 `Paparazzi UAV 软件需求规格说明.docx` 是从 Paparazzi UAV 开源项目的文档、配置和源码逆向整理得到的项目级自然语言需求规格说明。

## 原始项目基线

- 官方仓库：<https://github.com/paparazzi/paparazzi>
- 固定提交：`859ce70cab56df31f19cd69af9f150fe45562d8e`
- 版本说明：Paparazzi v7.0 stable release
- 描述边界：Paparazzi UAS 产品族，并以官方 Bebop 2 旋翼机配置作为设备、接口和运行链路的落地参考

## 主要逆向资料

### 项目与架构资料

- `README.md`：项目定位、系统组成、构建和基本使用方式。
- `doc/sphinx/source/developer_guide/system_overview.rst`：地面段、通信段和机载段的总体架构。
- `doc/sphinx/source/developer_guide/PPRZ_System_architecture.png`：系统级组成与交互关系。
- `doc/sphinx/source/developer_guide/PPRZ_Airborne_architecture.png`：机载软件分层与数据通路。
- `doc/sphinx/source/developer_guide/PPRZ_Main_ap_loop.png`：主任务循环和周期调度关系。

### 构型与设备资料

- `conf/conf_example.xml`：官方飞行器示例、机载板、飞行计划和遥测配置之间的组合关系。
- `conf/airframes/examples/bebop2_indi.xml`：Bebop 2 代表构型及其模块装配关系。
- `conf/modules/boards/bebop2.xml`：主控板、端口及板级模块配置。
- `conf/modules/imu_bebop.xml`、`conf/modules/sonar_bebop.xml`：惯性器件和声呐设备接入方式。
- `conf/flight_plans/rotorcraft_basic.xml`：旋翼机任务阶段、航点与飞行流程。
- `conf/telemetry/default_rotorcraft.xml`：机载遥测消息集合与周期配置。

### 关键实现资料

- `sw/airborne/main_ap.c`：机载主程序、任务分组和周期调度入口。
- `sw/airborne/firmwares/rotorcraft/`、`sw/airborne/firmwares/fixedwing/`：不同飞行器类别的模式管理、导航、制导和安全行为。
- `sw/airborne/modules/`：传感器、状态估计、稳定控制、导航、执行机构、数据链和系统监视等功能实现。
- `sw/airborne/boards/`、`sw/airborne/arch/`：板级资源、外设驱动和处理器相关实现。
- `sw/ground_segment/`：地面配置、监控、任务操作和消息转发能力。

## 形成方式

先依据架构资料确定系统边界、参与设备和外部交互，再用官方构型文件固定可部署实例；随后沿主循环、模块依赖、消息与控制数据通路回溯功能处理过程，并把代码中的调用条件、输入、输出和关键步骤改写为自然语言需求。项目族中的互斥能力按适用条件表达，不把所有板卡和飞行器配置误写成同一套同时运行的系统。

