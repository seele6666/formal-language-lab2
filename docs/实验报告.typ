// 形式语言与自动机实验（二）· CFG 化简与 PDA 转 CFG
// 排版与 C:\projects\Unveil\docs\INTERFACE.typ 一致
// 编译: typst compile docs/实验报告.typ docs/实验报告.pdf

#import "typst-preamble.typ": *

#set document(
  title: "形式语言与自动机实验（二）实验报告",
  author: ("张恒基", "林旭东", "尹浩铭", "赵博宇"),
  date: datetime(year: 2026, month: 5, day: 22),
)

// ============================================================
// 封面
// ============================================================

#page(margin: (top: 2.2cm, bottom: 2.2cm, x: 2.8cm), numbering: none, footer: none)[
  #set text(font: main-font)
  #align(center + horizon)[
    #block(
      width: 15cm,
      inset: (y: 1.1cm),
      stroke: (top: 2.5pt + rgb("#1a365d"), bottom: 0.75pt + rgb("#cbd5e1")),
    )[
      #align(center)[
        #text(size: 10.5pt, tracking: 0.35em, fill: rgb("#475569"))[形 式 语 言 与 自 动 机 · 实 验 二]
        #v(0.55cm)
        #text(size: 26pt, weight: "bold", fill: rgb("#0f172a"))[上下文无关文法与下推自动机]
        #v(0.65cm)
        #text(size: 19pt, weight: "medium", fill: rgb("#1e40af"))[CFG 化简与 PDA→CFG 转换实验报告]
        #v(0.35cm)
        #text(size: 13pt, fill: rgb("#64748b"))[Formal Languages Lab 2 · CFG Simplification & PDA to CFG]
      ]
    ]

    #v(1.5cm)

    #box(
      width: 13cm,
      inset: (x: 1.2cm, y: 0.95cm),
      fill: rgb("#f8fafc"),
      radius: 6pt,
      stroke: 0.75pt + rgb("#e2e8f0"),
    )[
      #align(center)[
        #text(size: 11pt, weight: "bold", fill: rgb("#334155"))[小组成员]
        #v(0.55cm)
        #grid(
          columns: (1fr, 1fr),
          column-gutter: 1.6cm,
          row-gutter: 0.65cm,
          align: center + horizon,
          [
            #text(size: 13pt, weight: "bold")[张恒基（组长）] \
            #v(0.25cm)
            #text(size: 12pt, fill: rgb("#64748b"))[
              2024211301 \
              2024210926
            ]
          ],
          [
            #text(size: 13pt, weight: "bold")[林旭东] \
            #v(0.25cm)
            #text(size: 12pt, fill: rgb("#64748b"))[
              2024211301 \
              2024210915
            ]
          ],
          [
            #text(size: 13pt, weight: "bold")[尹浩铭] \
            #v(0.25cm)
            #text(size: 12pt, fill: rgb("#64748b"))[
              2024211301 \
              2024210910
            ]
          ],
          [
            #text(size: 13pt, weight: "bold")[赵博宇] \
            #v(0.25cm)
            #text(size: 12pt, fill: rgb("#64748b"))[
              2024211301 \
              2024210908
            ]
          ],
        )
      ]
    ]

    #v(1.4cm)

    #align(center)[
      #text(size: 11pt, fill: rgb("#64748b"))[项目代号：formal-language-lab2]
      #v(0.25cm)
      #text(size: 11pt, fill: rgb("#64748b"))[2026 年 5 月 22 日]
    ]
  ]

  #v(1fr)
  #align(center)[
    #text(size: caption-size, fill: rgb(148, 163, 184))[
      本文档为实验二程序设计、算法说明与运行验证的完整记录
    ]
  ]
]

#body-start()

// ============================================================
// 第一章：小组信息与实验环境
// ============================================================

= 小组信息与实验环境

== 成员分工

#hdr-table[
  #table(
    columns: (auto, auto, auto, 1fr),
    align: (left, left, left, left),
    table.header([*姓名*], [*学号*], [*角色*], [*分工与负责模块*]),
    [张恒基], [2024210926], [组长], [
      CFG 数据结构与化简算法；#inline-code("cfg.py")、#inline-code("cfg_parser.py")、#inline-code("cfg_simplifier.py")；epsilon / 单产生式 / 无用符号消除及算法文档。
    ],
    [林旭东], [2024210915], [PDA / 转换], [
      PDA 数据结构与 PDA→CFG；#inline-code("pda.py")、#inline-code("pda_parser.py")、#inline-code("pda_to_cfg.py")；#inline-code("[p,A,q]") 变量构造。
    ],
    [尹浩铭], [2024210910], [入口 / 测试], [
      命令行与样例测试；#inline-code("main.py")、#inline-code("examples/")、#inline-code("tests/")；12 项单元测试与运行记录。
    ],
    [赵博宇], [2024210908], [文档 / 演示], [
      实验报告、可执行说明与演示脚本；#inline-code("README.md")、#inline-code("docs/")、PyInstaller 打包与视频脚本。
    ],
  )
]

== 实验环境

#hdr-table[
  #table(
    columns: (auto, auto),
    stroke: none,
    align: (left, left),
    [*项目*], [*配置*],
    [操作系统], [Windows 11（x86-64）],
    [编程语言], [Python 3.12（兼容 3.9+）],
    [依赖], [仅标准库：#inline-code("dataclasses")、#inline-code("itertools")、#inline-code("argparse")、#inline-code("re")、#inline-code("unittest")],
    [运行入口], [#inline-code("main.py")；可选 #inline-code("dist/formal_lang_lab2.exe")],
    [打包], [PyInstaller #inline-code("--onefile --name formal_lang_lab2")],
  )
]

== 项目结构

#payload-block(
  ```
  formal-language-lab2/
  ├── main.py                 # 命令行入口（simplify / pda2cfg / demo）
  ├── cfg.py                  # CFG 数据结构
  ├── cfg_parser.py           # CFG 文本解析
  ├── cfg_simplifier.py       # CFG 化简（四步流水线）
  ├── pda.py                  # PDA 五元组
  ├── pda_parser.py           # PDA 文本解析（块格式 + 数学符号格式）
  ├── pda_to_cfg.py           # PDA→CFG 标准构造
  ├── examples/
  │   ├── grammar_sample.txt  # 指定 CFG 样例
  │   ├── specified_cfg.txt
  │   ├── pda_sample.txt      # 指定 PDA 样例
  │   └── specified_pda.txt
  ├── tests/                  # 12 项 unittest
  └── docs/                   # 本报告、截图、可执行说明
  ```,
  title: [仓库目录（提交源码根目录）],
)

= 程序设计

== 整体架构

项目采用*模块化分层*：数据结构层（#inline-code("cfg.py")、#inline-code("pda.py")）→ 解析层（#inline-code("cfg_parser.py")、#inline-code("pda_parser.py")）→ 算法层（#inline-code("cfg_simplifier.py")、#inline-code("pda_to_cfg.py")），由 #inline-code("main.py") 统一调度。

#enum[
  *算法与数据解耦*：化简只操作 #inline-code("CFG") 对象；PDA 转换只操作 #inline-code("PDA") 对象，与文本格式无关。
  *可组合*：#inline-code("pda2cfg") 输出 #inline-code("CFG") 后可接 #inline-code("simplify_cfg")，满足「先转换再化简」。
  *可测试*：各模块独立单测，不依赖命令行或磁盘 I/O（除解析入口）。
]

#hdr-table[
  #figure(
    table(
      columns: (auto, 1fr),
      align: (left, left),
      table.header([*源文件*], [*职责*]),
      [#inline-code("cfg.py")], [产生式集合、变量/终结符集合、文本输出],
      [#inline-code("cfg_parser.py")], [多箭头写法、#inline-code("eps") 别名、注释过滤],
      [#inline-code("cfg_simplifier.py")], [nullable / unit-closure / 生成 / 可达四步化简],
      [#inline-code("pda.py")], [状态、栈符号、迁移表、空栈接受标志],
      [#inline-code("pda_parser.py")], [块格式与 #inline-code("delta(q,a,A)=") 数学格式],
      [#inline-code("pda_to_cfg.py")], [[p,A,q] 变量法、压栈长度枚举],
      [#inline-code("main.py")], [子命令 #inline-code("simplify")、#inline-code("pda2cfg")、#inline-code("demo")],
    ),
    caption: [模块划分与源文件对应关系],
  )
]

== 命令行接口

#hdr-table[
  #table(
    columns: (auto, auto, 1fr),
    align: (left, left, left),
    table.header([*子命令*], [*别名*], [*功能*]),
    [#inline-code("simplify")], [#inline-code("simplify-cfg")], [读入 CFG 文件，输出化简后产生式],
    [#inline-code("pda2cfg")], [#inline-code("pda-to-cfg")], [读入 PDA，输出转换 CFG；#inline-code("--simplify") 继续化简],
    [#inline-code("demo")], [—], [内置 #inline-code("SPECIFIED_CFG") 与 #inline-code("SPECIFIED_PDA") 一次演示],
  )
]

#v(0.2cm)
#text(size: hint-size, fill: gray)[处理流水线：读文件 → 解析 → 算法 → 标准产生式文本输出。]

== CFG 化简流水线

#seq-diagram(
  "
      输入 CFG 文本
            |
            v
      cfg_parser.parse_cfg()
            |
            v
   (1) eliminate_epsilon_productions
            |
            v
   (2) eliminate_unit_productions
            |
            v
   (3) remove_non_generating_symbols
            |
            v
   (4) remove_unreachable_symbols
            |
            v
      CFG.to_text()  -->  终端输出
  ",
  [CFG 化简四步流水线（顺序不可调换）],
)

*顺序不可调换*：消 epsilon 可能引入新单产生式；消单产生式可能产生新的非生成符号；先删非生成再删不可达，才能保留「可生成终结符串且从开始符号可达」的符号。

== PDA 到 CFG 组合流水线

#seq-diagram(
  "
      输入 PDA 文本
            |
            v
      pda_parser.parse_pda()
            |
            v
      pda_to_cfg(pda)  -->  原始 CFG（含 [p,A,q] 变量）
            |
            +---- 默认：直接打印
            |
            +---- --simplify：simplify_cfg() -->  化简 CFG
            |
            v
      终端输出产生式列表
  ",
  [PDA→CFG 与可选化简组合流程],
)

= 核心算法

== epsilon 产生式消除

*问题*：$A arrow.r epsilon$ 使语言可能含空串；目标是在语言不含空串时得到*无 epsilon 产生式*的等价文法。

*步骤*：

#enum[
  *计算 nullable*（不动点）：若 $A arrow.r alpha$ 且 $alpha$ 中符号均在 nullable，则 $A in$ nullable。
  *扩展右部*：对每个产生式，枚举 nullable 位置的所有删除组合，加入新产生式。
  *删除*：原 epsilon 产生式不再保留（空右部不加入，除非可选保留 $S arrow.r epsilon$）。
]

*复杂度*：nullable 迭代 $O(|V| dot |P|)$；右部 $k$ 个 nullable 时组合 $2^k$。

*实现*：#inline-code("cfg_simplifier.py") 中 #inline-code("find_nullable_variables()")、#inline-code("itertools.combinations")。

== 单产生式消除

*问题*：$A arrow.r B$ 不直接产生终结符，形成 $A =>^* B$ 链，使文法冗余。

*步骤*：

#enum[
  对每个 $A$ 计算 #inline-code("unit_closure[A]")（经单产生式可达的变量集，BFS/DFS）。
  将闭包中每个 $B$ 的*非单产生式*并入 $A$。
  删除全部单产生式。
]

*复杂度*：$O(|V| dot (|V| + |P|))$。

*实现*：#inline-code("_unit_reachable_variables()")、#inline-code("_is_unit_production()")。

== 无用符号消除

分两步，*必须先非生成、后不可达*。

=== 消除非生成符号

#enum[
  不动点计算 #inline-code("generating")：产生式右部变量均在 generating 中则左部加入（终结符恒可生成）。
  删除左部非 generating 的产生式；右部含非生成变量的产生式一并删除。
]

=== 消除不可达符号

#enum[
  从 $\{S\}$ 出发 BFS 得 #inline-code("reachable")。
  仅保留左部在 reachable 的产生式；右部含不可达变量的产生式删除。
]

*实现*：#inline-code("find_generating_variables()")、#inline-code("find_reachable_variables()")（#inline-code("cfg_simplifier.py:77-138")）。

== PDA 到 CFG 等价构造

*前置*：仅支持*空栈接受*（#inline-code("accepts_by_empty_stack = True")）。

#hdr-table[
  #table(
    columns: (auto, 1fr),
    align: (left, left),
    table.header([*步骤*], [*说明*]),
    [1. 变量], [对每个 $(p,A,q)$ 引入 #inline-code("[p,A,q]")：从 $p$ 出发栈顶 $A$，读串后弹出 $A$ 到 $q$；共 $|Q|^2|Gamma|$ 个],
    [2. 开始式], [$S arrow.r [q_0,z_0,q]$，$q$ 取遍所有状态],
    [3. 迁移], [$delta(p,a,A)=(q,epsilon)$ → #inline-code("[p,A,q] -> a")],
    [4. 压栈], [$delta(p,a,A)=(q,B_1...B_k)$ 时枚举中间状态，链式产生式],
    [5. ε 迁移], [输入 $epsilon$ 时右部可为纯变量串],
  )
]

*复杂度*：压栈长度 $k$ 时单条迁移最多 $O(|Q|^k)$ 条产生式；总 worst-case $O(|Q|^(K+1)|Gamma|)$。

*实现*：#inline-code("itertools.product") 枚举中间状态；#inline-code("_add_transition_productions()") 区分 push 长度 0 与 $>= 1$。

= 输入与输出格式

== CFG 输入

*紧凑风格*：

#payload-block(
  ```
  S -> a | bA | B | ccD
  A -> abB | epsilon
  B -> aA
  C -> ddC
  D -> ddd
  ```,
)

*多字符变量*（PDA 转换后）：

#payload-block(
  ```
  S -> b [q0,B,q1]
  [q0,B,q1] -> a | b [q0,B,q1]
  ```,
)

#hdr-table[
  #table(
    columns: (auto, 1fr),
    stroke: none,
    align: (left, left),
    [*规则*], [*说明*],
    [箭头], [#inline-code("->")、#inline-code("=>")、#inline-code("→") 等],
    [空串], [#inline-code("epsilon")、#inline-code("eps")、#inline-code("ε") 等],
    [分隔], [#inline-code("|") 分隔候选右部；\# 起为注释],
    [推断], [开始符号、变量集、终结符集由产生式自动收集],
  )
]

== PDA 输入

*块格式（推荐，#inline-code("examples/pda_sample.txt")）*：

#payload-block(
  ```
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
  ```,
)

*数学符号格式*：与 #inline-code("tests/test_pda_to_cfg.py") 中 #inline-code("SPECIFIED_PDA") 字符串一致；解析器归一化 $delta$、$epsilon$、全角括号等。

== 输出格式

按变量名排序输出（$S$ 固定最前）；多字符符号以空格分隔；空串统一打印 #inline-code("epsilon")。

= 测试用例与执行效果

== CFG 指定样例

*输入*（#inline-code("examples/grammar_sample.txt")）：

#payload-block(
  ```
  S -> a | b A | B | c c D
  A -> a b B | eps
  B -> a A
  C -> d d C
  D -> d d d
  ```,
  title: [化简前（课程指定 CFG）],
)

*分析要点*：

#enum[
  $A arrow.r epsilon$ ⇒ $A$ nullable；$B arrow.r a A$ 展开得 $B arrow.r a A | a$。
  $S arrow.r b A$ 展开得 $S arrow.r b A | b$；$S arrow.r B$ 为单产生式，unit-closure 将 $B$ 的非单产生式并入 $S$。
  $C arrow.r d d C$ 仅自引用 ⇒ $C$ 非生成，应删除。
]

*命令*：

#payload-block(
  ```
  py main.py simplify examples\grammar_sample.txt
  ```,
)

*输出*：

#payload-block(
  ```
  S -> a | aA | b | bA | ccD
  A -> abB
  B -> a | aA
  D -> ddd
  ```,
  title: [化简后（终端实测）],
)

*结果*：$C$ 删除；epsilon 与 $S arrow.r B$ 消除；$D arrow.r d d d$ 保留。

#figure(
  image("screenshots/6-1-cfg-simplify.png", width: 100%),
  caption: [CFG 化简命令运行截图],
)

== PDA 指定样例

*输入 PDA*：见 #inline-code("examples/pda_sample.txt")；等价于 #inline-code("main.py") 内 #inline-code("SPECIFIED_PDA")。

*识别语言*：

$ L = \{ b^m a^n \mid m \ge 1,\ n \ge 1,\ n \le m \} $

（先读 $b$ 压栈，再读 $a$/ε 弹栈；*不是* $b^n a^n$。与 #inline-code("test_simplified_cfg_matches_specified_pda_examples") 一致。）

*命令*：

#payload-block(
  ```
  py main.py pda2cfg examples\pda_sample.txt --simplify
  ```,
)

*输出*：

#payload-block(
  ```
  S -> b [q0,B,q1]
  [q0,B,q1] -> a | b [q0,B,q1] | b [q0,B,q1] [q1,B,q1]
  [q1,B,q1] -> a
  ```,
  title: [转换并化简后（4 条产生式）],
)

*产生式含义*：

#hdr-table[
  #table(
    columns: (auto, 1fr),
    align: (left, left),
    table.header([*产生式*], [*对应迁移直觉*]),
    [#inline-code("S -> b [q0,B,q1]")], [从 $q_0$ 弹 $z_0$ 且读 $b$ 压 $B$ 到 $q_1$ 的路径],
    [#inline-code("[q0,B,q1] -> a")], [$delta(q_0,a,B)=(q_1,epsilon)$],
    [#inline-code("[q0,B,q1] -> b [q0,B,q1]")], [$delta(q_0,b,B)=(q_0,BB)$，中间状态 $r=q_1$],
    [#inline-code("[q0,B,q1] -> b [q0,B,q1] [q1,B,q1]")], [同上，$r=q_0$ 形成递归],
    [#inline-code("[q1,B,q1] -> a")], [$delta(q_1,a,B)=(q_1,epsilon)$],
  )
]

*语义验证*（BFS 枚举短串）：可生成 #inline-code("ba")、#inline-code("bba")、#inline-code("bbaa")、#inline-code("bbbaaa")；不可生成 #inline-code("baa")、空串、单独 #inline-code("b")/#inline-code("a")。

#figure(
  image("screenshots/6-2-pda2cfg-simplify.png", width: 100%),
  caption: [PDA 转 CFG 并化简运行截图],
)

== 自动化测试

#hdr-table[
  #figure(
    table(
      columns: (auto, auto, 1fr),
      align: (left, center, left),
      table.header([*测试文件*], [*用例数*], [*覆盖内容*]),
      [#inline-code("test_cfg_parser.py")], [2], [指定 CFG、多字符符号解析],
      [#inline-code("test_cfg_simplifier.py")], [3], [nullable、指定 CFG 化简、单产生式环],
      [#inline-code("test_pda_parser.py")], [2], [块格式 / 数学符号 PDA],
      [#inline-code("test_pda_to_cfg.py")], [3], [变量构造、压栈长度、化简后语言 BFS 验证],
      [#inline-code("test_main.py")], [2], [#inline-code("demo") 输出、CLI 别名],
    ),
    caption: [单元测试覆盖（合计 12 项）],
  )
]

#inline-code("test_pda_to_cfg.py") 对化简 CFG 做有界 BFS，逐串校验是否属于上述 $L$，保证「转换 + 化简」端到端正确。

#payload-block(
  ```
  py -m unittest discover -s tests
  Ran 12 tests in 0.08s — OK
  ```,
  title: [测试命令与结果],
)

#figure(
  image("screenshots/6-3-unittest.png", width: 100%),
  caption: [unittest 运行截图],
)

= 可执行程序与打包

#hdr-table[
  #table(
    columns: (auto, 1fr),
    align: (left, left),
    table.header([*步骤*], [*命令*]),
    [安装], [#inline-code("pip install pyinstaller")],
    [打包], [#inline-code("pyinstaller --onefile --name formal_lang_lab2 main.py")],
    [产物], [#inline-code("dist/formal_lang_lab2.exe")],
    [验证], [#inline-code("dist\\formal_lang_lab2.exe demo")],
  )
]

#payload-block(
  ```
  Specified CFG simplified:
  S -> a | aA | b | bA | ccD
  ...

  Specified PDA converted and simplified:
  S -> b [q0,B,q1]
  ...
  ```,
  title: [#inline-code("demo") 子命令实测输出摘要],
)

= 改进思路

#hdr-table[
  #table(
    columns: (auto, 1fr),
    stroke: none,
    align: (left, left),
    [*方向*], [*说明*],
    [图形界面], [Web（Streamlit/Gradio）分步展示四步化简中间文法],
    [边界测试], [全非生成文法、纯 epsilon、长单产生式链、压栈 $k>3$],
    [#inline-code("--keep-start-epsilon")], [语言含空串时可选保留 $S arrow.r epsilon$],
    [终态接受 PDA], [自动插入 ε 迁移转为空栈接受],
    [#inline-code("--verbose")], [打印每步化简后的 CFG],
  )
]

// ============================================================
// 附录
// ============================================================

= 附录 A：命令快速参考

#hdr-table[
  #table(
    columns: (auto, 1fr),
    align: (left, left),
    table.header([*命令*], [*说明*]),
    [#inline-code("py main.py simplify FILE")], [CFG 化简],
    [#inline-code("py main.py pda2cfg FILE")], [PDA→CFG（原始）],
    [#inline-code("py main.py pda2cfg FILE --simplify")], [PDA→CFG 再化简],
    [#inline-code("py main.py demo")], [内置两例演示],
    [#inline-code("py -m unittest discover -s tests")], [全部单元测试],
  )
]

= 附录 B：版本记录

#hdr-table[
  #table(
    columns: (1.1cm, 2.4cm, 1fr),
    align: (center + horizon, center + horizon, left),
    table.header([*版本*], [*日期*], [*说明*]),
    [v1.0], [2026-05], [完成 CFG 化简、PDA→CFG、命令行与 12 项测试],
    [v1.1], [2026-05-22], [填充运行截图；Typst 报告排版对齐 INTERFACE.typ],
  )
]
