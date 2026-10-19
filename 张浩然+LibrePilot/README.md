# LibrePilot 需求文档生成说明

本目录中的 `LibrePilot 软件需求规格说明.docx` 是从 LibrePilot 开源项目的项目资料、Revolution 板级配置、UAVObject 定义、飞控模块和地面站源码逆向整理得到的项目级自然语言需求规格说明。

## 原始项目基线

- 官方仓库：<https://github.com/librepilot/LibrePilot>
- 固定提交：`4952aa59583187f3e807cff7d8df5a4e2680e963`
- 版本基线：LibrePilot 16.09
- 代表构型：Revolution 飞控板；项目级范围同时覆盖机载固件、UAVObject/UAVTalk 和地面控制站的主要交互

## 主要逆向资料

### 项目与版本资料

- `README.md`：项目定位、机载端与地面端组成及构建入口。
- `WHATSNEW.txt`、`MILESTONES.txt`：16.09 版本能力和项目演进信息，用于限定版本范围。

### 板级与设备资料

- `flight/targets/boards/revolution/board-info.mk`：处理器、Flash 分区和板卡标识。
- `flight/targets/boards/revolution/board_hw_defs.c`：SPI、I2C、传感器、端口、无线和执行通道等硬件资源。
- `flight/targets/boards/revolution/firmware/revolution.cpp`、`pios_board.c`：板级启动、设备初始化、端口角色和模块装载。
- `flight/targets/boards/revolution/firmware/inc/FreeRTOSConfig.h`：实时调度和系统资源配置。
- `flight/pios/`：MPU6000、HMC5x83、MS5611、接收机、PWM、USB、Flash、RFM22B 等底层驱动。

### 数据模型、控制与地面交互资料

- `shared/uavobjectdefinition/`、`flight/uavobjects/`：设置、命令、状态和遥测对象的字段与元数据。
- `flight/uavtalk/`：UAVObject 的序列化和链路传输协议。
- `flight/modules/Sensors/`、`Attitude/`、`StateEstimation/`、`GPS/`：传感器采集、姿态和导航状态估计。
- `flight/modules/ManualControl/`、`Stabilization/`、`Actuator/`：人工输入、飞行模式、稳定控制、混控和物理输出。
- `flight/modules/PathPlanner/`、`PathFollower/`：任务路径、航点推进和不同机型的路径跟随。
- `flight/modules/Telemetry/`、`Logging/`、`FirmwareIAP/`、`System/`：遥测、日志、升级、告警、看门狗和配置持久化。
- `ground/gcs/`：地面配置、对象浏览、飞行监控、任务操作和固件维护。

## 形成方式

先以 Revolution 的板级文件固定处理器、板载设备、外部端口和安全启动条件，再以 UAVObject 作为跨模块数据主线，沿传感器采集、状态估计、模式管理、稳定控制、航迹控制、执行输出和遥测维护链路回溯功能。各需求的输入、输出和处理步骤由对象定义与模块实现共同确定，其他飞控板或载具类型的差异按可选构型说明。

