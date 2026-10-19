# LC SpaceRDL 最后冻结结果（文件夹版）

本文件夹整理完整82条需求（63正式＋19补充）及当前保留的数据处理片段，未改LC原工程、不压缩。
**全量严格转换仍未完成（blocked）。**282是独立片段定义数，共423个出现位置，不是全部需求已完成数。

| 原子操作 | 独立定义数 |
| --- | ---: |
| Init | 0 |
| GetData | 0 |
| SendData | 0 |
| ProTM | 0 |
| ProTC | 0 |
| Set | 34 |
| Compute | 248 |
| 合计 | 282 |

七个主文件：

1. [README.md](README.md)：导航与冻结结论。
2. [requirements.md](requirements.md)：完整整理/补全需求、原文及审查记录。
3. [resources.md](resources.md)：资源与数据字典；软件端点与数据处理合同分栏。
4. [statements.md](statements.md)：282定义、当前行号、输入输出与规则。
5. [code.rdl](code.rdl)：最后冻结的数据片段，非完整系统程序。
6. [traceability.md](traceability.md)：全部82条需求对应的保留片段、剔除候选与剩余义务。
7. [issues.md](issues.md)：44候选逐项拒绝依据及保留的原问题状态。

补充阅读：[语法说明](grammar_profile.md)、[贯通讲解](walkthrough.md)、[具体阻塞](STRICT_CONVERSION_BLOCKER.md)。
来源：[源码快照](evidence/LC/docs/lc_FunctionalRequirements.csv)、[来源清单](source_manifest.json)。
冻结来源commit为f54e136220d8d6f2e207ba57073a9faeef9d3b0f；97个本地源码文件此前逐字节核对。
本地LC-dev没有.git，不宣称核定其本地HEAD。部署配置/外部依赖版本未知，不补造参数。

根目录JSON为保留的权威输入；data/issues.json保留问题与人工状态。旧ST/资源链接及native_interface_statements、syntax等字段只作历史审查，当前位置只认projection_lines和code.rdl；历史目录不用于完成验收。
data_fragments.rdl为检查脚本兼容副本，必须与code.rdl字节一致，不应分别编辑。

## 独立复查与再生成

在本文件夹打开终端运行（仅需Python 3标准库，不依赖相邻ZIP或LC-dev）：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_data_projection.py --root .
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_bundle.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/regenerate_docs.py
```

再生成脚本只读取现有JSON并稳定排序生成Markdown，不重新初始化或重置人工问题、状态、审查结论。
freeze_manifest.json用于检测冻结输入变化；有意修改后出现哈希差异须审查，不自动覆盖基准。
[本轮执行报告](logs/execution.json)列出实际运行输出；这些是静态/一致性及检查工具回归测试，未运行LC/cFE或官方解析器，也没有全量等价证明。
五种设备相关操作当前为0，是剔除无依据的软件服务映射后的结果，不是说LC没有收发行为或最终只能有两类操作。
