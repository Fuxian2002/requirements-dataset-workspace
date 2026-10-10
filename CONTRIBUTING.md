# 提交说明

## 学生提交步骤

```bash
git switch main
git pull
git switch -c 姓名-项目名

# 修改或添加文件后
git add .
git commit -m "add 项目名 requirement analysis"
git push -u origin 姓名-项目名
```

推送后在 GitHub 上创建 Pull Request，不直接向 `main` 分支提交。

## 合并前检查

- 源项目 URL、提交 SHA 和许可证已记录；
- 需求来源能够定位到文件、需求 ID 或代码位置；
- 原始内容、人工改写内容和模型推断内容能够区分；
- SpaceRDL 语句符合当前采用的语法版本；
- 冲突和未确认信息没有被伪装成确定事实；
- 未提交密钥、账号信息或不允许公开的材料。

