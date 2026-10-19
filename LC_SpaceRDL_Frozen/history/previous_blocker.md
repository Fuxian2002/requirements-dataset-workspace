# LC 严格转换：已执行的纠正与必须补充的依据

本目录是未完成的工作结果，不是“全部需求已严格转换”的交付包。旧 lc_spacerdl_7ops.zip 不能作为严格转换验收结果。

## 已做的工作

重新核对论文第2.1节、第3.1–3.4节、表7和表10，逐条检查旧包44个软件交互候选。它们的目标都是cFE软件服务，没有获得论文所要求的设备/硬件端口对应依据，因此全部拒绝进入严格数据片段。没有把它们替换成带隐藏发送副作用的Compute，也没有补造Device、端口或ControlPeriod。

保留82条完整需求及其原始文字、处理规则、证据和人工结论；requirements.md与旧包该文件逐字节相同。其历史候选ST链接属于旧审查记录，不能看作本目录严格片段的有效转换完成证据。新的片段定位只以data_fragment_statements.json为准。

生成248 Compute与34 Set的数据处理片段，保持原有业务计算/状态赋值的相对顺序。**它们只描述输入已经到达后的数据处理，不完整表达接收、事件发送、RTS发送、HK发送或软件服务调用。**不将此投影当作完整流程、完整系统或282项已标准确认的需求。其他五种算子在这些片段里为0，是严格剔除无依据映射后的结果，不是遗忘其存在。

## 具体阻塞证据，不再笼统称“待确认”

### 1. 事件发送不能直接写成向设备发送控制信号

正式需求LC1000在LC-dev/docs/lc_FunctionalRequirements.csv第2行明确要求No-Op后增加有效命令计数并生成事件。代码LC-dev/fsw/src/lc_cmds.c第267–280行调用CFE_EVS_SendEvent。

论文表7（PDF文件第10页）SendData的定义是向devName标识的设备发送控制信号；第2.1节将系统/外部设备限定为硬件单元，表10（文件第12页）还要求目标设备的硬件端口和通信协议。LCEventService是软件事件服务，不是上述设备；现有LC材料没有把这一服务绑定到该论文设备模型的定义。

因此旧`SendData LCEventService LCEventData0106;`不是有充分依据的严格转换。只用Compute构造事件参数或Set保存事件描述，也不等于完成该需求的事件发送义务。

### 2. 向SC任务发RTS请求不等于向物理设备发控制信号

正式需求LC3002.3在同CSV第64–67行明确要求向SC task发启动RTS命令。代码LC-dev/fsw/src/lc_custom.c第42–55行构造LC_RTSRequestCmd_t并调用CFE_SB_TransmitMsg；lc_action.c第148–175行保留AP先PASSIVE、请求、计数和事件的源码次序。

SC task是外部软件任务，LC本身未提供或操作该任务的硬件端口。论文没有给出SC task到SendData设备资源的映射规则。不得把SC虚构成Device，也不得把“计算得到请求帧”替代“发出请求”。这直接阻止把LC3002.3标为全部严格转换完成。

### 3. 非周期软件消息入口不能擅自改成周期或硬件中断

LC2003（CSV第16–18行）与LC3001（第46–48行）分别由监测消息和独立Sample Request触发。代码lc_app.c第91–126行通过共享CmdPipe的CFE_SB_ReceiveBuffer接收，lc_dispatch.c第314–361行按MID分别路由。

论文第3.1节（文件第7页）给出一次性InitTask、预设控制周期的AppTask及打断应用任务的InterruptTask；第3.2节的Controller/Device/Connect描述硬件拓扑。已提供材料没有定义LC这种软件消息入口的任务绑定。不能编造固定周期，不能将普通软件管道消息假定成硬件中断，不能用注释替代触发语义。

### 4. 软件注册不等于硬件端口初始化

代码lc_app.c第241–264行执行CFE_EVS_Register，第270–344行建立软件管道并订阅消息。论文表7的Init明确初始化portName标识的硬件端口。旧包的3个软件Init候选没有这一对应依据，已从严格片段排除。软件变量初始化可使用有依据的Set；软件服务注册的实际调用不能因此自动获得表达。

## 需要补充什么才能继续完成全量严格转换

不是要求放宽“严格”，也不是再申请自造软件适配。需要**作者/语言维护者确认的SpaceRDL定义或扩展资料**，具体覆盖：cFE类软件服务/消息端点、软件事件与软件任务间请求、非周期软件消息触发的任务上下文。若选择从更高层完整硬件系统建模，则还必须提供真实部署拓扑与框架职责边界，并确认分析范围变更；不得仅凭LC源码猜测这些信息。

已尝试访问论文第5节指向的https://re4cps.org/spacerdl-appendix/以寻找完整定义，本机HTTPS连接失败。这不证明网站或扩展永远不存在，只表示本次未取得可据以采用的新规则。

## 复查

```sh
python3 scripts/strict_projection.py --archive ../lc_spacerdl_7ops.zip --output .
python3 scripts/check_data_projection.py --root .
```

strict_audit.json记录每个被拒绝候选的ST、算子、目标、REQ和源码定位。data_projection_check.json只报告数据片段形状/引用检查；full_LC_conversion始终不能因该检查通过改成完成。LC/cFE运行、官方SpaceRDL解析器和全量语义等价均未执行或未获证明。
