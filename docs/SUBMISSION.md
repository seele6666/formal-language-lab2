# 实验二提交打包说明（v4 对齐）

对照：`docs/形式语言与自动机课程实验（二）v4.docx`  
符合性检查：`docs/v4-要求对照.md`

## v4 提交清单

| 材料 | v4 要求 | 本地路径 | 状态 |
|---|---|---|---|
| 实验报告 | 必交 | `docs/report.docx` / `docs/实验报告.pdf` | ✓ 已生成 |
| 源代码 | 必交 | 项目根目录 | ✓ |
| 可执行程序 | 必交 | `dist/formal_lang_lab2.exe` | ✓ |
| 演示视频 | 必交，≤100MB | `docs/demo.mp4` | ⚠ 占位文件可自动生成，**提交前须替换为真实录制** |

## v4 文件命名

示例（v4.docx）：`1组+301+张三+报告.docx`，压缩包 `实验二+1组+301+张三.zip`

本组（**7 组**，班级 2024211301，组长 张恒基）：

```text
7组+2024211301+张恒基+报告.docx
7组+2024211301+张恒基+代码/
7组+2024211301+张恒基+程序/formal_lang_lab2.exe
7组+2024211301+张恒基+视频.mp4

实验二+7组+2024211301+张恒基.zip
```

## 一键重建并打包

```powershell
.\scripts\rebuild_submission.ps1 -GroupNumber "7"
```

或分步：

```powershell
py -m unittest discover -s tests -q
py scripts\md_to_docx.py docs\report.md docs\report.docx
cd docs; typst compile 实验报告.typ 实验报告.pdf; cd ..
py scripts\capture_terminal_screenshots.py
pyinstaller --noconfirm --onefile --name formal_lang_lab2 main.py
.\scripts\package_submission.ps1 -GroupNumber "7"
```

## 打包命令（仅打包）

1. 组号已填：**7 组**
2. 录制视频至 `docs/demo.mp4`（见 `docs/视频录制指南.md`）
3. 执行：

```powershell
.\scripts\package_submission.ps1 -GroupNumber "7"
```

## 提交前自检（v4 验证命令）

```cmd
py main.py simplify examples\grammar_sample.txt
py main.py pda2cfg examples\pda_sample.txt
py main.py pda2cfg examples\pda_sample.txt --simplify
py -m unittest discover -s tests
py main.py demo
```

## 重新生成报告

```cmd
py scripts\md_to_docx.py docs\report.md docs\report.docx
cd docs && typst compile 实验报告.typ 实验报告.pdf
py scripts\capture_terminal_screenshots.py
```

## 截止日期

v4 要求：**6 月 2 日前** 以组为单位提交到云平台。
