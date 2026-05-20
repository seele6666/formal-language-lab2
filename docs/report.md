# 形式语言与自动机实验（二）实验报告

## 1. 小组信息

- 班级：TODO
- 组号：TODO
- 组长：TODO
- 小组成员：
  - 姓名：TODO，学号：TODO，分工：CFG 数据结构与化简算法。负责 `cfg.py`、`cfg_parser.py`、`cfg_simplifier.py`，实现 epsilon 产生式消除、单产生式消除、无用符号消除，并整理 CFG 算法说明。
  - 姓名：TODO，学号：TODO，分工：PDA 数据结构与 PDA 到 CFG 转换。负责 `pda.py`、`pda_parser.py`、`pda_to_cfg.py`，实现 PDA 输入解析、`[p,A,q]` 变量构造和转换算法说明。
  - 姓名：TODO，学号：TODO，分工：命令行入口与测试验证。负责 `main.py`、`examples/`、`tests/`，整理实验指定样例，编写并运行单元测试，记录运行输出。
  - 姓名：TODO，学号：TODO，分工：实验报告与演示材料。负责 `README.md`、`docs/report.md`、`docs/executable.md`、`docs/video_script.md`，补充实验环境、输入输出格式、截图和演示视频脚本。

## 2. 实验环境

- 操作系统：Windows
- 编程语言：Python 3.9 或更高版本
- 依赖情况：程序仅使用 Python 标准库；测试使用 `unittest`
- 运行入口：`main.py`

## 3. 程序设计思路

项目按功能拆分为 CFG、PDA、解析器、算法和命令行入口。CFG 化简流程依次执行 epsilon 产生式消除、单产生式消除、不能生成终结符串的符号消除、不可达符号消除。PDA 转 CFG 使用变量 `[p,A,q]` 表示从状态 `p` 出发，在栈顶为 `A` 时读入某个串并弹出 `A`，最后到达状态 `q`。

## 4. 核心算法

### 4.1 epsilon 产生式消除

先迭代计算 nullable 变量集合；然后对每个产生式右部中的 nullable 变量枚举所有删除组合，补出新的产生式，最后删除原 epsilon 产生式。

### 4.2 单产生式消除

对每个变量计算 unit-closure，即通过单产生式可达的变量集合。再把闭包中变量的所有非单产生式并入当前变量。

### 4.3 无用符号消除

第一步迭代计算可生成终结符串的变量，删除不能生成终结符串的变量和相关产生式。第二步从开始符号出发计算可达变量，删除不可达变量和相关产生式。

### 4.4 PDA 到 CFG

对每个状态 `p`、栈符号 `A`、状态 `q` 构造变量 `[p,A,q]`。开始符号 `S` 产生 `[q0,z0,q]`。若迁移弹出栈顶且压入若干栈符号，则枚举中间状态，构造对应的变量链。

## 5. 输入格式和输出格式

CFG 输入格式示例：

```text
S -> a | b A | B | c c D
A -> a b B | eps
```

PDA 输入格式示例：

```text
states: q0 q1
input_symbols: a b
stack_symbols: B z0
start_state: q0
start_stack: z0
accept: empty_stack
transitions:
q0,b,z0 -> q0,B z0
```

输出格式为产生式列表，例如：

```text
S -> a | bA
A -> abB
```

## 6. 测试用例与执行效果

### 6.1 CFG 指定样例

输入文件：`examples/grammar_sample.txt`

运行命令：

```cmd
py main.py simplify examples\grammar_sample.txt
```

输出粘贴区：

```text
TODO：粘贴运行输出
```

截图占位：TODO

### 6.2 PDA 指定样例

输入文件：`examples/pda_sample.txt`

运行命令：

```cmd
py main.py pda2cfg examples\pda_sample.txt --simplify
```

输出粘贴区：

```text
TODO：粘贴运行输出
```

截图占位：TODO

### 6.3 自动化测试

运行命令：

```cmd
py -m unittest discover -s tests
```

截图占位：TODO

## 7. 改进思路

- 增加图形界面或网页界面，便于课堂演示。
- 增加更多教材样例和边界用例。
- 对包含空串的语言，可提供保留开始符号 epsilon 产生式的可选模式。
