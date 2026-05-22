# 实验二提交打包说明

## 已完成项

- `docs/report.md` 第 6 节运行输出与截图已填充
- `dist/formal_lang_lab2.exe` 已通过 `demo` 命令验证
- `docs/实验报告.typ`：Typst 排版（参照本组 DataLink / NFA 实验报告风格），编译得 `docs/实验报告.pdf`
- `docs/report.docx` 可由 `scripts/md_to_docx.py` 从 `report.md` 重新生成

## 待你本地完成

### 1. 录制演示视频（任务 3）

按 `docs/video_script.md` 使用 OBS 录制 720p，时长约 4 分钟，文件控制在 100MB 以内。

建议保存为：

```text
docs/demo.mp4
```

### 2. 填写组号并打包（任务 4）

报告中未填写**组号**。确认组号后，在项目根目录执行：

```powershell
.\scripts\package_submission.ps1 -GroupNumber "你的组号"
```

将生成：

```text
实验二{组号}2024211301张恒基.zip
```

压缩包内含：

- `{组号}2024211301张恒基报告.docx`
- `{组号}2024211301张恒基代码/`
- `{组号}2024211301张恒基程序/formal_lang_lab2.exe`
- `{组号}2024211301张恒基视频.mp4`

## 常用命令

```cmd
cd docs
typst compile 实验报告.typ 实验报告.pdf
py ..\scripts\capture_terminal_screenshots.py
py ..\scripts\md_to_docx.py report.md report.docx
pyinstaller --onefile --name formal_lang_lab2 main.py
dist\formal_lang_lab2.exe demo
```
