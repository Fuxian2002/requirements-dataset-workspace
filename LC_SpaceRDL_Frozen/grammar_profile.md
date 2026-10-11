# 本轮冻结的语法核定与检查边界

论文表7的数据操作形状：

```spacerdl
Compute outputName inputName ReqCapByFormTable FormulaTable.formulaName;
Set outputName inputName;
```

表8采用Composite、If/Else、While结构。FormulaTable的本项目具体函数合同、聚合数据序列化与变量别名不能仅因形状吻合就称为完整论文语义获确认。

论文中的Init/GetData/SendData/ProTM/ProTC未被删除；本轮仅排除了44个未建立论文设备/硬件端口/数管对应依据的软件候选。五类目前为0，不表示LC没有收发或后续最终只能使用Compute/Set。

不引入自造Device、软件适配语法、固定ControlPeriod或消息中断绑定；不把Compute中的请求描述当成真实发送。

本地检查覆盖操作形状、符号、公式输入输出合同、布尔条件符号与括号结构。未执行官方解析器，未证明全量语义等价。

[原论文](<evidence/reference/reference_materials/定稿ra012-20260721.pdf>)；具体阻塞见STRICT_CONVERSION_BLOCKER.md。
