# grblHAL

- 项目类型：数控机床运动控制固件核心层（C 语言，HAL 分层，面向 8/32 位 MCU）
- 上游仓库：https://github.com/grblHAL/core
- 锚定提交：`ca26fc98f1b2171251c946ab91d5912b733efa78`（2026-10-08）；版本标识 `GRBL_VERSION "1.1f"`、`GRBL_BUILD 20261008`、`HAL_VERSION 10`
- 许可证：GPL-3.0（仓库根 `COPYING`）
- 逆向产出：《grblHAL 软件需求规格说明书（竣工需求·逆向）》md / docx / pdf 三件套 + 《引用核验报告》
- 需求规模：72 个需求块（`GH-FREQ` / `GH-PREQ` / `GH-SREQ`），文档编号 `REQ-GRBLHAL-ASB-001`
- 处理范围：grblHAL/core 核心库 114 个 `.c`/`.h` 文件、46,348 行；不含各板卡驱动与插件仓库
- 产出日期：2026-10-15（文档）/ 2026-10-19（入库）
- 方法：大模型辅助的源码静态逆向，按《太搜文档》格式组织；每条需求附 `文件:行号` 证据，可回溯到锚定提交

## 目录内容

| 文件 | 说明 |
| --- | --- |
| `grblHAL_逆向需求规格说明书.md` | 主交付物（Markdown 源） |
| `grblHAL_逆向需求规格说明书.docx` | Word 版 |
| `grblHAL_逆向需求规格说明书.pdf` | PDF 版 |
| `grblHAL_引用核验报告.md` | 引用可解析性、语义窗口与 DOCX 结构的核验记录 |
| `SOURCE.md` | 源项目地址、提交、许可证与处理范围 |
| `图/` | Markdown 中引用的 6 张关系图（PNG） |

## 说明

- 文中证据路径写作 `文件:行号`，相对锚定提交的仓库根；本目录未复制第三方源码，复核时请按 `SOURCE.md` 检出指定提交。
- 关系图由离线渲染器 `uml_render.py` 从 JSON 描述生成，图源 JSON 未随本目录上传。
