# MESC Firmware 需求文档生成说明

本目录中的 `MESC Firmware 软件需求规格说明.docx` 是从 MESC Firmware 开源项目的说明文档、硬件配置、目标工程和控制源码逆向整理得到的项目级自然语言需求规格说明。

## 原始项目基线

- 官方仓库：<https://github.com/davidmolony/MESC_Firmware>
- 固定提交：`aa159cc6f0b55aee0d07dabd10055dfd89d20317`
- 分支基线：`master`
- 代表构型：`MESC_F405RG` 控制器与 `MP2_V0_1` 功率板组成的单电机控制系统

## 主要逆向资料

### 项目与控制原理资料

- `README.md`：项目定位、目标平台和总体功能。
- `src/introduction/FEATURES.md`：控制模式、传感方式、保护和通信能力。
- `src/operation/INTRODUCTION.md`、`src/operation/CONTROL.md`：PWM 中断、采样、磁场定向控制、磁链观测、弱磁和旋转跟踪原理。
- `src/hardware/MOTOR_PARAM.md`：电机参数及辨识过程。
- `src/debugging/FIRMWARE_INTRO.md`：固件入口、实时任务和调试通路。

### 硬件与目标工程资料

- `MESC_F405RG/MESC_F405RG.ioc`：STM32F405RG 的 ADC、PWM、定时器、CAN、UART、USB 和中断配置。
- `MESC_F405RG/Core/Inc/MESC_F405.h`：目标级频率、实例数量和编译配置。
- `MESC_F405RG/Core/Inc/MP2_V0_1.h`：功率板采样比例、PWM、死区、电流、电压和温度限制。
- `src/hardware/MP2_F405PILL_PINOUTS.md`：MP2 功率板引脚、采样和控制接口。
- `MESC_F405RG/STM32F405RGTX_FLASH.ld`、`FreeRTOSConfig.h`：程序、参数区和运行内存配置。

### 关键实现资料

- `MESC_F405RG/Core/Src/main.c`、`MESChw_setup.c`、`stm32f4xx_it.c`：上电初始化、硬件映射和中断入口。
- `MESC_Common/Src/MESCfoc.c`、`MESCpwm.c`、`MESCfluxobs.c`、`MESChfi.c`：采样换算、FOC、调制、无感观测和低速注入。
- `MESC_Common/Src/MESCmeasure.c`、`MESCposition.c`、`MESCinput.c`：电机参数辨识、位置/速度获取和控制请求汇聚。
- `MESC_Common/Src/MESCtemp.c`、`MESCerror.c`、`MESCmotor_state.c`：温度降额、故障关断和运行状态转换。
- `MESC_RTOS/Tasks/task_can.c`、`CAN_helper.c`：CAN 命令、状态与遥测交互。
- `MESC_RTOS/TTerm/`、`MESC_RTOS/Common/RTOS_flash.c`、`MESC_RTOS/MESC/MESCinterface.c`：终端配置、参数保存恢复和运行诊断。

## 形成方式

先用硬件头文件和 `.ioc` 固定真实可部署构型，再从 ADC/PWM/定时器中断入口恢复快速环和慢速环的时序；之后沿输入、状态机、位置估计、FOC、三相调制、保护和通信链路逐项回溯。需求中的每个处理步骤均按“操作对象＋操作方式＋产生结果”的粒度整理，项目支持但代表构型未启用的能力以可选路径表述。

