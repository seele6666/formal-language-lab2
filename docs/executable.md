# 可执行程序说明

本项目是 Python 命令行程序，不需要额外编译。

## 运行前准备

确认已经安装 Python 3.9 或更高版本，并且在 cmd 中可以执行：

```cmd
py --version
```

## 程序入口

```cmd
py main.py simplify examples\grammar_sample.txt
py main.py pda2cfg examples\pda_sample.txt
py main.py pda2cfg examples\pda_sample.txt --simplify
```

## 测试入口

```cmd
py -m unittest discover -s tests
```

如果教师要求提交“可执行程序”，可以将整个代码目录作为程序提交；也可以使用 PyInstaller 在本机打包：

```cmd
py -m pip install pyinstaller
py -m PyInstaller --onefile main.py
```

打包后可执行文件位于 `dist\formal_lang_lab2.exe`。

验证：

```cmd
dist\formal_lang_lab2.exe demo
```
