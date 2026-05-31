# 形式语言与自动机实验（二）实验报告

> 对照文档：`docs/形式语言与自动机课程实验（二）v4.docx`  
> 符合性明细：`docs/v4-要求对照.md`

## 0. 课程实验 v4 要求符合性

| v4 要求条目 | 完成情况 | 验证方式 |
|---|---|---|
| **任务一**：消除 ε 产生式、单产生式、无用符号 | ✓ 已完成 | `py main.py simplify examples\grammar_sample.txt` |
| **任务一**：使用指定 CFG 验证 | ✓ 已完成 | 输出与 v4 样例一致；见 §6.1 |
| **任务二①**：PDA→等价 CFG | ✓ 已完成 | `py main.py pda2cfg examples\pda_sample.txt` |
| **任务二②**：转换后再 CFG 化简 | ✓ 已完成 | `py main.py pda2cfg examples\pda_sample.txt --simplify` |
| **任务二**：使用指定 PDA（空栈 Φ）验证 | ✓ 已完成 | 与 v4 七元组及 6 条 δ 一致；见 §6.2 |
| 分组 3–4 人 | ✓ 4 人 | 见 §1 |
| 程序正确、文档清晰 | ✓ | 24 项单元测试全部通过 |
| 提交：报告 + 源码 + 可执行程序 + 演示视频 | 报告/代码/程序 ✓；**视频待本地录制** | 见 `docs/视频录制指南.md` |
| 报告必含六项内容 | ✓ 全部覆盖 | 见下方 §1–§7 与 v4 逐条对照 |
| 提交截止 | — | v4 要求 **6 月 2 日前** 组内提交云平台 |

**报告结构与 v4.docx「实验报告至少包含以下内容」对照**：

| v4 报告要求 | 本报告章节 |
|---|---|
| 小组成员，班级，姓名，学号；成员分工 | §1 |
| 实验环境描述 | §2 |
| 程序的设计思路及核心算法 | §3、§4 |
| 程序的输入格式，输出格式 | §5 |
| 测试用例，输入，输出，执行效果（截图） | §6 |
| 改进思路和方法（可选） | §7 |

## 1. 小组信息

- **组号**：7 组
- **班级**：2024211301
- **组长**：张恒基（学号 2024210926）
- 小组成员：
  - 姓名：张恒基，学号：2024210926，分工：CFG 数据结构与化简算法。负责 `cfg.py`、`cfg_parser.py`、`cfg_simplifier.py`，实现 epsilon 产生式消除、单产生式消除、无用符号消除，并整理 CFG 算法说明。
  - 姓名：林旭东，学号：2024210915，分工：PDA 数据结构与 PDA 到 CFG 转换。负责 `pda.py`、`pda_parser.py`、`pda_to_cfg.py`，实现 PDA 输入解析、`[p,A,q]` 变量构造和转换算法说明。
  - 姓名：尹浩铭，学号：2024210910，分工：命令行入口与测试验证。负责 `main.py`、`examples/`、`tests/`，整理实验指定样例，编写并运行单元测试，记录运行输出。
  - 姓名：赵博宇，学号：2024210908，分工：实验报告与演示材料。负责 `README.md`、`docs/report.md`、`docs/executable.md`、`docs/video_script.md`，补充实验环境、输入输出格式、截图和演示视频脚本。

## 2. 实验环境

- 操作系统：Windows 11
- 编程语言：Python 3.12
- 依赖情况：程序仅使用 Python 标准库（`dataclasses`、`itertools`、`argparse`、`re`、`unittest` 等），无需安装第三方包；测试框架使用内置 `unittest`
- 运行入口：`main.py`
- 项目结构：

```
formal-language-lab2/
├── main.py                 # 命令行入口
├── cfg.py                  # CFG 数据结构
├── cfg_parser.py           # CFG 文本解析器
├── cfg_simplifier.py       # CFG 化简算法
├── pda.py                  # PDA 数据结构
├── pda_parser.py           # PDA 文本解析器
├── pda_to_cfg.py           # PDA 到 CFG 转换算法
├── pda_convert.py          # 终态 PDA → 空栈 PDA
├── cfg_format.py           # JSON / LaTeX 输出
├── examples/
│   ├── grammar_sample.txt  # 指定 CFG 样例（v4 验证）
│   ├── specified_cfg.txt
│   ├── pda_sample.txt      # 指定 PDA 样例（v4 验证）
│   └── specified_pda.txt
├── tests/                  # 24 项 unittest
│   ├── test_cfg_parser.py
│   ├── test_cfg_simplifier.py
│   ├── test_cfg_format.py
│   ├── test_pda_parser.py
│   ├── test_pda_convert.py
│   ├── test_pda_to_cfg.py
│   └── test_main.py
└── docs/
    ├── report.md
    ├── 实验报告.typ / 实验报告.pdf
    ├── v4-要求对照.md
    ├── 视频录制指南.md
    └── screenshots/
```

## 3. 程序设计思路

### 3.1 整体架构

项目采用模块化分层设计，按功能拆分为三层：**数据结构层**（`cfg.py`、`pda.py`）、**解析层**（`cfg_parser.py`、`pda_parser.py`）、**算法层**（`cfg_simplifier.py`、`pda_to_cfg.py`），最外层由 `main.py` 统一调度。

这种分层的优势在于：
- **算法与数据解耦**：化简算法只操作 `CFG` 对象，不关心输入文本格式；转换算法只操作 `PDA` 对象，不关心输出格式。
- **可组合性**：PDA 转 CFG 后得到的 `CFG` 对象可直接传入化简流水线，实现实验要求的"先转换再化简"的串联流程。
- **可测试性**：每个模块可独立编写单元测试，不依赖命令行或文件 I/O。

### 3.2 CFG 化简流水线

CFG 化简流程按固定顺序依次执行四个步骤：

```
输入 CFG
  → (1) 消除 epsilon 产生式 (eliminate_epsilon_productions)
  → (2) 消除单产生式 (eliminate_unit_productions)
  → (3) 消除非生成符号 (remove_non_generating_symbols)
  → (4) 消除不可达符号 (remove_unreachable_symbols)
  → 输出等价的无 epsilon、无单产生式、无无用符号的 CFG
```

**顺序不可调换的原因**：消除 epsilon 产生式可能引入新的单产生式，因此必须先消 epsilon 再消单产生式；消除单产生式可能使某些变量变为非生成，因此消单产生式必须在消除非生成符号之前；消除非生成符号可能切断某些变量的可达路径，因此先消非生成再消不可达，确保只保留"既能生成终结符串、又能被开始符号到达"的有用符号。

### 3.3 PDA 到 CFG 转换思路

采用教材标准构造：对于空栈接受的 PDA，引入形如 `[p,A,q]` 的变量，其语义为"从状态 p 出发，栈顶为 A，经过若干步后弹出 A 并到达状态 q，期间读入的输入串"。

开始符号 S 的产生式为 `S → [q0, z0, q]`（对所有状态 q），表示从初始状态 q0 出发，初始栈符号 z0 在栈顶，最终弹出 z0 到达某个状态 q，此时栈为空，PDA 接受。

迁移的处理分两种情况：
- **弹出（压入为空）**：δ(p, a, A) = {(q, ε)}，则添加产生式 `[p,A,q] → a`。
- **压入 k 个符号**：δ(p, a, A) = {(q, B₁B₂...Bₖ)}，则对任意可能的状态序列 r₁, r₂, ..., rₖ₋₁, qₖ，枚举中间状态，添加产生式 `[p,A,qₖ] → a [q,B₁,r₁] [r₁,B₂,r₂] ... [rₖ₋₁,Bₖ,qₖ]`。

## 4. 核心算法

### 4.1 epsilon 产生式消除

**问题描述**：形如 A → ε 的产生式称为 epsilon 产生式。消除 epsilon 产生式的目标是得到一个不含 ε-产生式的等价文法（若原语言不含空串 ε）。

**算法步骤**：

1. **计算 nullable 变量集合**：采用不动点迭代。
   - 初始化 `nullable = ∅`。
   - 重复扫描所有产生式：若存在产生式 A → α，且 α 中所有符号都在 nullable 中（空串 α 视为自动满足），则将 A 加入 nullable。
   - 直到 nullable 不再增长。

2. **扩展产生式右部**：对每个产生式 A → X₁X₂...Xₙ：
   - 找出右部中所有 nullable 符号的位置。
   - 枚举这些位置的所有删除组合（含删除 0 个，即保留原右部）。
   - 对每种组合，将删除后的右部作为新产生式加入结果文法。
   - 若删除后右部为空（即全部符号被删），不加入（除非是保留开始符号 ε 的可选模式）。

3. **删除原 epsilon 产生式**：上述步骤中跳过空右部，自然实现了删除。

**复杂度分析**：nullable 计算最多迭代 |V| 次，每次扫描 |P| 个产生式，复杂度 O(|V|·|P|)。扩展右部时，若右部有 k 个 nullable 符号，则枚举 2ᵏ 种组合。最坏情况下 nullable 符号数量可达到 |V|，但实际文法中通常很小。

**代码实现要点**（`cfg_simplifier.py:19-39`）：使用 `itertools.combinations` 枚举所有删除组合，`find_nullable_variables()` 返回 nullable 变量集合。

### 4.2 单产生式消除

**问题描述**：形如 A → B（A, B 均为变量）的产生式称为单产生式。单产生式本身不产生终结符，但可能形成链 A ⇒ B ⇒ C ⇒ ...，增加推导步数且使文法膨胀。

**算法步骤**：

1. **计算 unit-closure**：对每个变量 A，通过 BFS 计算其通过单产生式可达的所有变量集合 `unit_closure[A]`。
   - 初始化 `unit_closure[A] = {A}`。
   - 重复：若 B ∈ unit_closure[A] 且存在单产生式 B → C，则将 C 加入。
   - 直到不再增长。

2. **替换产生式**：对每个变量 A，遍历 `unit_closure[A]` 中的每个变量 B：
   - 将 B 的所有非单产生式右部（长度 ≠ 1 或该符号不是变量）加入 A 的产生式集合。
   - 不再保留任何单产生式。

**复杂度分析**：unit-closure 计算对 |V| 个变量各做一次 BFS，每次 BFS 遍历可能包含所有变量，复杂度 O(|V|·(|V| + |P|))。替换阶段复杂度 O(|V|·|P|)。

**代码实现要点**（`cfg_simplifier.py:58-74`）：`_unit_reachable_variables()` 使用显式栈的 DFS 实现传递闭包；`_is_unit_production()` 检查右部长度是否为 1 且该符号是否属于变量集。

### 4.3 无用符号消除

无用符号分为两类：**非生成符号**（不能推导出任何终结符串）和**不可达符号**（从开始符号出发无法到达）。消除必须按"先非生成、后不可达"的顺序进行。

#### 第一步：消除非生成符号

**算法步骤**：

1. **计算生成变量集合**（不动点迭代）：
   - 初始化 `generating = ∅`。
   - 重复：对每个产生式 A → α，若 α 中所有**变量**都在 generating 中（终结符自动视为可生成），则将 A 加入 generating。
   - 直到不再增长。

2. **过滤产生式**：删除左部不在 generating 中的产生式；对于保留的产生式，若其右部包含非生成变量，则该产生式也被删除（因为非生成变量永远无法推导出终结符串）。

#### 第二步：消除不可达符号

**算法步骤**：

1. **计算可达变量集合**（BFS）：
   - 初始化 `reachable = {S}`。
   - 重复：对每个可达变量 A，检查其所有产生式右部，将其中出现的变量加入 reachable。
   - 直到不再增长。

2. **过滤产生式**：只保留左部在 reachable 中的产生式；对于保留的产生式，若右部包含不可达变量，同样删除。

**复杂度分析**：两个步骤均为不动点迭代，复杂度各为 O(|V|·|P|)。

**代码实现要点**（`cfg_simplifier.py:77-138`）：`find_generating_variables()` 和 `find_reachable_variables()` 分别实现上述迭代过程。注意在判定"右部符号是否满足条件"时，终结符总是自动满足。

### 4.4 PDA 到 CFG 的等价构造

**前置条件**：PDA 必须以空栈方式接受（`accepts_by_empty_stack = True`）。若 PDA 使用终态接受，需先转换为空栈接受。

**算法步骤**：

1. **构造变量集合**：对所有状态 p, q ∈ Q 和栈符号 A ∈ Γ，构造变量 `[p,A,q]`，其语义为"从状态 p 出发，栈顶为 A，读入某个串后弹出 A 并到达状态 q"。变量总数 = |Q|² × |Γ|。

2. **构造开始产生式**：对每个状态 q ∈ Q，添加：
   ```
   S → [q0, z0, q]
   ```
   其中 q0 为初始状态，z0 为初始栈符号。

3. **构造迁移产生式**：对每个迁移 δ(p, a, A) = {(q, B₁B₂...Bₖ)}：
   - **若 k = 0**（仅弹出）：添加 `[p,A,q] → a`。
   - **若 k ≥ 1**：枚举所有中间状态 r₁, r₂, ..., rₖ₋₁ ∈ Q，添加：
     ```
     [p,A,qₖ] → a [q,B₁,r₁] [r₁,B₂,r₂] ... [rₖ₋₁,Bₖ,qₖ]
     ```
     其中 qₖ 取遍所有状态。

4. **ε-迁移处理**：若输入符号为 ε（即 δ(p, ε, A)），则上述步骤中 a = ε，产生式右部以变量串开头。

**复杂度分析**：构造的变量数为 |Q|² × |Γ|。对于压入 k 个符号的迁移，需枚举 |Q|^(k-1) 个中间状态组合，再乘以 |Q| 种 qₖ 选择，共 |Q|^k 种。总产生式数量在最坏情况下为 O(|Q|^(K+1) × |Γ|)，其中 K 为最大压入长度。

**代码实现要点**（`pda_to_cfg.py:15-95`）：使用 `itertools.product` 枚举中间状态；`_add_transition_productions()` 分别处理 push 长度为 0 和 ≥1 的情况；对仅支持空栈接受的 PDA 做了显式校验。

## 5. 输入格式和输出格式

### 5.1 CFG 输入格式

支持两种写法风格：

**紧凑风格**（单字符符号直接拼接）：
```text
S -> a | bA | B | ccD
A -> abB | epsilon
B -> aA
C -> ddC
D -> ddd
```

**空格分隔风格**（多字符符号用空格隔开，如 `[q0,B,q1]`）：
```text
S -> b [q0,B,q1]
[q0,B,q1] -> a | b [q0,B,q1]
```

**解析规则**：
- 产生式箭头支持 `->`、`=>`、`-->`、`:`、`=` 及 Unicode 箭头 `→`。
- ε 的别名：`epsilon`, `eps`, `e`, `lambda`, `empty`, `ε`。
- 用 `|` 分隔多个候选右部。
- `#` 至行尾为注释。
- 起始终结符从产生式自动推导。

### 5.2 PDA 输入格式

支持两种格式：

**格式一：数学符号格式**
```text
M = ({q0,q1}, {a,b}, {B,z0}, delta, q0, z0, empty)
delta(q0,b,z0) = {(q0,Bz0)}
delta(q0,b,B) = {(q0,BB)}
delta(q0,a,B) = {(q1,epsilon)}
delta(q1,a,B) = {(q1,epsilon)}
delta(q1,epsilon,B) = {(q1,epsilon)}
delta(q1,epsilon,z0) = {(q1,epsilon)}
```

**格式二：块格式（推荐）**
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

**解析规则**：
- 自动识别 U+03B4 (δ)、U+03B5 (ε)、U+03A6 (Φ) 等 Unicode 字符并归一化。
- 全角字符（＝，（）等）自动转为半角。
- `accept` 字段：`empty_stack` / `empty` / `phi` / `Φ` 表示空栈接受。
- 栈符号串（如 `Bz0`）会根据已知栈符号集合自动分词。

### 5.3 输出格式

输出为标准产生式列表，按变量名排序（开始符号 S 始终排在最前）：

```text
S -> a | aA | b | bA | ccD
A -> abB
B -> a | aA
D -> ddd
```

多字符符号自动以空格分隔输出，ε 统一显示为 `epsilon`。

## 6. 测试用例与执行效果

### 6.1 CFG 指定样例

**输入文法**（`examples/grammar_sample.txt`）：
```
S → a | bA | B | ccD
A → abB | ε
B → aA
C → ddC
D → ddd
```

**分析**：
- A 有 ε-产生式 A → ε，因此 A 是 nullable。
- B → aA 中的 A 是 nullable，展开后得到 B → aA | a。
- S → bA 展开后得到 S → bA | b；S → B 为单产生式，unit-closure 将 B 的非单产生式（如 B → a A 及其 ε 展开）并入 S。
- C → ddC：C 只产生自己，属于非生成符号，应被删除。

**运行命令**：
```cmd
py main.py simplify examples\grammar_sample.txt
```

**输出**：
```text
S -> a | aA | b | bA | ccD
A -> abB
B -> a | aA
D -> ddd
```

**结果分析**：
- C 被正确删除（非生成变量，C → ddC 永远无法终止）。
- ε-产生式 A → ε 被消除，取而代之的是在包含 A 的右部中删除 A 的版本（如 S → aA | a，B → aA | a）。
- 单产生式 S → B 被消除；B → a A 不是单产生式，其经 nullable 展开后的右部通过 unit-closure 并入 S（如输出中的 S → a | aA 等）。
- D → ddd 保留（D 可生成终结符串且从 S 可达）。

![CFG 化简运行截图](screenshots/6-1-cfg-simplify.png)

### 6.2 PDA 指定样例（v4 任务二）

v4 指定 PDA（空栈接受，终态集 Φ 为空）：

```
M = ({q0,q1}, {a,b}, {B,z0}, δ, q0, z0, Φ)

δ(q0,b,z0) = {(q0,Bz0)}
δ(q0,b,B)  = {(q0,BB)}
δ(q0,a,B)  = {(q1,ε)}
δ(q1,a,B)  = {(q1,ε)}
δ(q1,ε,B)  = {(q1,ε)}
δ(q1,ε,z0) = {(q1,ε)}
```

#### 6.2.1 要求（1）：PDA → 等价 CFG

**运行命令**：

```cmd
py main.py pda2cfg examples\pda_sample.txt
```

**输出（原始 CFG，节选）**：

```text
Raw CFG:
S -> [q0,z0,q0] | [q0,z0,q1]
[q0,B,q0] -> b [q0,B,q0] [q0,B,q0] | b [q0,B,q1] [q1,B,q0]
[q0,B,q1] -> a | b [q0,B,q0] [q0,B,q1] | b [q0,B,q1] [q1,B,q1]
[q0,z0,q0] -> b [q0,B,q0] [q0,z0,q0] | b [q0,B,q1] [q1,z0,q0]
[q0,z0,q1] -> b [q0,B,q0] [q0,z0,q1] | b [q0,B,q1] [q1,z0,q1]
[q1,B,q1] -> epsilon | a
[q1,z0,q1] -> epsilon
```

变量 `[p,A,q]` 表示：从状态 p、栈顶 A 出发，读入串后弹出 A 并到达 q。

#### 6.2.2 要求（2）：转换结果再 CFG 化简

**运行命令**：

```cmd
py main.py pda2cfg examples\pda_sample.txt --simplify
```

**输出（化简后 CFG）**：

```text
Simplified CFG:
S -> b [q0,B,q1]
[q0,B,q1] -> a | b [q0,B,q1] | b [q0,B,q1] [q1,B,q1]
[q1,B,q1] -> a
```

**结果分析**：
- 化简后 $S$ 仅剩 `S -> b [q0,B,q1]`：`[q0,B,q1]` 表示在 q0 栈顶为 B 时读入并弹出 B 到达 q1；与 $z_0$ 相关的冗余变量产生式已在化简中删除。
- `[q0,B,q1] → a` 对应 δ(q0,a,B)={(q1,ε)}：读 a 弹出 B。
- `[q0,B,q1] → b [q0,B,q1]` 对应 δ(q0,b,B)={(q0,BB)}，中间状态取 r=q1，第二个 B 弹出的终点为 q1。
- `[q0,B,q1] → b [q0,B,q1] [q1,B,q1]` 对应上述迁移中中间状态取 r=q0 的情况，形成递归产生式。
- `[q1,B,q1] → a` 对应 δ(q1,a,B)={(q1,ε)}。
- 化简后产生式由原始数十条降至 4 条；**无 ε 产生式、无单产生式、无无用符号**，满足 v4 任务二②。

**语言识别**：L = { bᵐ aⁿ | m,n ≥ 1, n ≤ m }（先 b 压栈，再 a/ε 弹栈；**不是** bⁿ aⁿ）。

**语义验证**：化简后文法可生成 ba、bba、bbaa、bbbaaa 等（m ≥ n ≥ 1）；不能生成空串、单独的 b 或 a、以及 a 多于 b 的串（如 baa）。这与 L = { bᵐ aⁿ | m,n ≥ 1, n ≤ m } 一致。

![PDA 转 CFG 并化简运行截图](screenshots/6-2-pda2cfg-simplify.png)

### 6.3 自动化测试

共 **24** 个单元测试，覆盖 v4 指定样例及边界场景：

| 测试文件 | 测试数 | 覆盖内容 |
|---|---|---|
| `test_cfg_parser.py` | 2 | 指定 CFG 解析、多字符符号 |
| `test_cfg_simplifier.py` | 7 | nullable、指定化简、单产生式环、keep-epsilon、纯 ε、不可达、verbose |
| `test_cfg_format.py` | 2 | JSON / LaTeX 输出 |
| `test_pda_parser.py` | 2 | 块格式 / 数学符号 PDA（v4 指定 PDA） |
| `test_pda_convert.py` | 3 | 终态→空栈、自动转换 |
| `test_pda_to_cfg.py` | 4 | 变量构造、压栈 0–3、化简后语言 BFS |
| `test_main.py` | 4 | demo、CLI 别名、verbose、JSON 格式 |

**运行命令**：

```cmd
py -m unittest discover -s tests
```

**运行结果（2026-05-31 实测）**：

```
Ran 24 tests in 0.01s — OK
```

![自动化测试运行截图](screenshots/6-3-unittest.png)

### 6.4 可执行程序

PyInstaller 打包：`dist/formal_lang_lab2.exe`；验证命令 `dist\formal_lang_lab2.exe demo`。

## 7. 改进思路（可选）

v4 标注为可选。本项目已实现部分扩展，其余作为后续方向：

| 方向 | 状态 | 说明 |
|---|---|---|
| `--verbose` 逐步化简输出 | **已实现** | 对应 v4 报告「执行效果」深化 |
| `--keep-start-epsilon` | **已实现** | 语言含空串时保留 S→ε |
| 终态 PDA 自动转空栈 | **已实现** | `pda_convert.py` |
| JSON / LaTeX 输出 | **已实现** | `cfg_format.py` |
| 边界测试扩充 | **已实现** | 24 项测试 |
| Web 可视化界面 | 规划中 | Streamlit 分步展示 |
| CYK / PDA 模拟验证 | 规划中 | 交互式判定 w∈L |
