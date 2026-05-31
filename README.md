# 形式语言与自动机实验（二）

本项目实现“上下文无关文法与下推自动机”实验：

- CFG 化简：消除 epsilon 产生式、单产生式、无用符号。
- PDA 转 CFG：将空栈接受 PDA 转换为等价 CFG。
- PDA 转 CFG 后可继续调用 CFG 化简流程。

## 运行环境

- Python 3.9 或更高版本。
- 仅使用 Python 标准库，测试使用 `unittest`。

## 常用命令（cmd）

```cmd
py main.py simplify examples\grammar_sample.txt
py main.py simplify examples\grammar_sample.txt --verbose
py main.py pda2cfg examples\pda_sample.txt
py main.py pda2cfg examples\pda_sample.txt --simplify
py -m unittest discover -s tests
```

可选参数：

- `--verbose`：打印化简流水线每一步中间文法
- `--keep-start-epsilon`：开始符号 nullable 时保留 `S -> epsilon`
- `--format text|json|latex`：输出格式（默认 text）
- `--no-auto-convert`：不将终态 PDA 自动转为空栈 PDA

兼容命令：

```cmd
py main.py simplify-cfg examples\grammar_sample.txt
py main.py pda-to-cfg examples\pda_sample.txt --simplify
py main.py demo
```

## 输入格式

CFG 示例：

```text
S -> a | b A | B | c c D
A -> a b B | eps
B -> a A
C -> d d C
D -> d d d
```

PDA 示例：

```text
states: q0 q1
input_symbols: a b
stack_symbols: B z0
start_state: q0
start_stack: z0
accept: empty_stack
transitions:
q0,b,z0 -> q0,B z0
q0,b,B -> q0,B B
q0,a,B -> q1,eps
q1,a,B -> q1,eps
q1,eps,B -> q1,eps
q1,eps,z0 -> q1,eps
```

## 项目结构

- `cfg.py`：CFG 数据结构。
- `cfg_parser.py`：CFG 文本解析。
- `cfg_simplifier.py`：CFG 化简算法。
- `pda.py`：PDA 数据结构。
- `pda_parser.py`：PDA 文本解析。
- `pda_to_cfg.py`：PDA 到 CFG 的构造算法。
- `pda_convert.py`：终态 PDA 转空栈 PDA。
- `cfg_format.py`：JSON / LaTeX 输出。
- `main.py`：命令行入口。
- `tests/`：单元测试（24 项）。
- `examples/`：实验指定样例输入。
