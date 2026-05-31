"""Generate docs/实验报告.typ per cursor-tasks.md structure."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "实验报告.typ"

COVER = r'''// 形式语言与自动机实验（二）· CFG 化简与 PDA 转 CFG
// 编译: typst compile docs/实验报告.typ docs/实验报告.pdf

#import "typst-preamble.typ": *

#set document(
  title: "形式语言与自动机实验（二）实验报告",
  author: ("张恒基", "林旭东", "尹浩铭", "赵博宇"),
  date: datetime(year: 2026, month: 5, day: 31),
)

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
        #text(size: 11pt, weight: "bold", fill: rgb("#334155"))[第 7 组 · 小组成员]
        #v(0.55cm)
        #grid(
          columns: (1fr, 1fr),
          column-gutter: 1.6cm,
          row-gutter: 0.65cm,
          align: center + horizon,
          [
            #text(size: 13pt, weight: "bold")[张恒基（组长）] \
            #v(0.25cm)
            #text(size: 12pt, fill: rgb("#64748b"))[2024211301 / 2024210926]
          ],
          [
            #text(size: 13pt, weight: "bold")[林旭东] \
            #v(0.25cm)
            #text(size: 12pt, fill: rgb("#64748b"))[2024211301 / 2024210915]
          ],
          [
            #text(size: 13pt, weight: "bold")[尹浩铭] \
            #v(0.25cm)
            #text(size: 12pt, fill: rgb("#64748b"))[2024211301 / 2024210910]
          ],
          [
            #text(size: 13pt, weight: "bold")[赵博宇] \
            #v(0.25cm)
            #text(size: 12pt, fill: rgb("#64748b"))[2024211301 / 2024210908]
          ],
        )
      ]
    ]
    #v(1.4cm)
    #align(center)[
      #text(size: 11pt, fill: rgb("#64748b"))[项目代号：formal-language-lab2]
      #v(0.25cm)
      #text(size: 11pt, fill: rgb("#64748b"))[2026 年 5 月 31 日]
    ]
  ]
  #v(1fr)
  #align(center)[
    #text(size: caption-size, fill: rgb(148, 163, 184))[
      本文档为实验二程序设计、算法证明、测试验证与改进方案的完整记录
    ]
  ]
]

#body-start()
'''

BODY = r'''
= 1 小组信息与实验环境 <sec:env>

*组号*：7 组。*班级*：2024211301。*组长*：张恒基（2024210926）。

本实验对照 v4 任务书完成 CFG 四步化简与空栈接受 PDA→CFG 转换；程序 `24` 项单元测试全部通过，可执行文件位于 #inline-code("dist/formal_lang_lab2.exe")。

== 成员分工

#hdr-table[
  #table(
    columns: (auto, auto, auto, 1fr),
    align: (left, left, left, left),
    table.header([*姓名*], [*学号*], [*角色*], [*分工*]),
    [张恒基], [2024210926], [组长], [CFG 化简：#inline-code("cfg_simplifier.py")、解析器、算法证明],
    [林旭东], [2024210915], [PDA], [PDA 解析、#inline-code("pda_to_cfg.py")、终态→空栈转换],
    [尹浩铭], [2024210910], [测试], [#inline-code("main.py")、#inline-code("examples/")、#inline-code("tests/")（24 项）],
    [赵博宇], [2024210908], [文档], [Typst 报告、#inline-code("report.md")、演示材料与 PyInstaller 打包],
  )
]

== 实验环境

#hdr-table[
  #table(
    columns: (auto, auto),
    stroke: none,
    align: (left, left),
    [*项目*], [*配置*],
    [操作系统], [Windows 11],
    [语言], [Python 3.12（兼容 3.9+）],
    [依赖], [仅标准库；测试用 #inline-code("unittest")],
    [入口], [#inline-code("main.py simplify|pda2cfg|demo")；可选 #inline-code("dist/formal_lang_lab2.exe")],
    [排版], [Typst 0.13+ 编译 #inline-code("docs/实验报告.pdf")],
  )
]

= 2 形式化定义 <sec:formal>

本章建立后续算法与证明共用的符号体系。读完本章，读者应能独立写出小型 CFG/PDA 的形式化描述，并手工追踪一步推导或格局迁移。

== CFG 四元组

#definition("上下文无关文法（CFG）")[
  一个 CFG 是四元组 $G=(V, Sigma, P, S)$，其中：
  - $V$：*变量*（非终结符）的*有穷*集合；
  - $Sigma$：*终结符*的有穷字母表；
  - $P subset V times (V union Sigma)^*$：*产生式*的有穷集合，每条形如 $A arrow.r alpha$；
  - $S in V$：起始符号。

  约束：$V inter Sigma = emptyset$；右部 $alpha$ 至少含一个符号（空产生式在程序中用 #inline-code("()") 表示 $A arrow.r epsilon$）。
]

*指定 CFG 样例*（v4 任务一）：$V={S,A,B,C,D}$，$Sigma={a,b,c,d}$，$S$ 为起始符号。产生式包括 $S arrow.r a bar b A bar B bar c c D$，$A arrow.r a b B bar epsilon$，$B arrow.r a A$，$C arrow.r d d C$，$D arrow.r d d d$。可验证 $V inter Sigma=emptyset$，且 $|P|=8$（含 $A arrow.r epsilon$）。

== 推导、句型与句子

#definition("直接推导与闭包")[
  若 $A arrow.r beta in P$，则对任意 $u,v in (V union Sigma)^*$ 有 $u A v arrow.r u beta v$（一步直接推导）。
  记 $arrow.r^*$ 为 $arrow.r$ 的自反传递闭包（零步或多步推导）。
  语言 $L(G)={w in Sigma^* bar S arrow.r^* w}$；*句子*是完全由终结符组成的句型。
]

*推导链示例*：在指定 CFG 中，由 $S arrow.r b A$ 与 $A arrow.r a b B$、$B arrow.r a A$、$A arrow.r epsilon$ 可得：
#align(center)[
  $S arrow.r b A arrow.r b a b B arrow.r b a b a A arrow.r b a b a arrow.r b a b a$
]
共 5 步，最终句子 #inline-code("babab") $in L(G)$。该链说明 $B$ 可生成含终结符的串，但 $B not arrow.r^* epsilon$（见第 6.1 节 Step 1）。

== 待消除结构的定义

#definition("ε-产生式、nullable、单产生式、无用符号")[
  - *ε-产生式*：右部为空的产生式 $A arrow.r epsilon$。若 $epsilon in L(G)$ 则必须保留 $S arrow.r epsilon$（本程序用 #inline-code("--keep-start-epsilon") 控制）。
  - *nullable 变量*：$A in V$ 满足 $A arrow.r^* epsilon$。
  - *单产生式*：$A arrow.r B$ 且 $B in V$（右部恰为单个变量）。
  - *非生成变量*：不存在以该变量为根、仅含终结符的推导树。
  - *不可达变量*：不存在 $S arrow.r^* alpha A beta$ 的句型。
]

*反例说明*：若保留 $A arrow.r epsilon$ 而不展开，自顶向下分析器可能在读入终结符前无限猜测是否选用 $A arrow.r epsilon$；单产生式链 $S arrow.r A arrow.r B arrow.r b$ 使语法表面含冗余非终结符；不可达变量 $B$（$S arrow.r a A$ 但无产生式引用 $B$）浪费存储且干扰化简顺序。

== PDA 七元组

#definition("下推自动机（PDA）")[
  $M=(Q, Sigma, Gamma, delta, q_0, z_0, F)$：
  - $Q$：有限状态集；$Sigma$：输入字母表；$Gamma$：栈字母表；
  - $delta subset Q times (Sigma union {epsilon}) times Gamma times Q times Gamma^*$：转移函数（程序用集合写法 $delta(q,a,X)={(p,gamma)}$）；
  - $q_0 in Q$：初态；$z_0 in Gamma$：初栈符号；$F subset Q$：终态集（空栈接受时 $F=emptyset$，记 accept 为 $Phi$）。
]

*指定 PDA*：$Q={q_0,q_1}$，$Sigma={a,b}$，$Gamma={B,z_0}$，$q_0$ 初态，$z_0$ 初栈，空栈接受。六条 $delta$ 见第 5.2 节。

== 格局与接受方式

#definition("格局（ID）与一步迁移")[
  格局三元组 $(q, w, gamma)$ 表示：处于状态 $q$，未读输入为 $w in Sigma^*$，栈内容为 $gamma in Gamma^*$（栈顶在右端）。
  若 $(p, beta) in delta(q, a, X)$ 且 $gamma = gamma' X$，则
  $(q, a w, gamma' X) arrow.r (p, w, gamma' beta)$。
  空栈接受语言：$L(M)={w in Sigma^* bar (q_0, w, z_0) arrow.r^* (q, epsilon, epsilon)}$。
]

*三步 ID 链*（$delta(q_0,b,z_0)={(q_0,B z_0)}$）：
#align(center)[
  $(q_0, b w, z_0 gamma) arrow.r (q_0, w, B z_0 gamma) arrow.r (q_0, w_2, B' z_0 gamma) arrow.r dots.h$
]
第二步若再读 $b$ 且 $delta(q_0,b,B)={(q_0,B B)}$，则栈顶压入第二个 $B$。

== 空栈接受与终态接受

#definition("两种接受方式")[
  *空栈接受*：$L(M)={w bar (q_0,w,z_0) arrow.r^* (q,epsilon,epsilon)}$，本实验 v4 指定 PDA 采用此方式（$F=Phi$）。
  *终态接受*：$L(M)={w bar (q_0,w,z_0) arrow.r^* (q_f,w',gamma)$ 对某 $q_f in F$}。
]

*等价转换思路*（标准教材构造）：引入新栈底符 $dollar$，满足 $dollar not in Gamma$，新初态 $q_0'$ 用 $epsilon$ 迁移压入 $dollar z_0$，再进入原 $q_0$；从每个原终态 $epsilon$ 迁移到收集状态并弹空栈；最终仅在 $dollar$ 被弹出且栈空时接受。本程序 #inline-code("pda_convert.py") 对终态 PDA 做简化实现，测试见 #inline-code("test_pda_convert.py")。

== PDA→CFG 变量直觉

#definition("三元组非终结符")[
  对每个 $p,q in Q$、$A in Gamma$，引入变量 #inline-code("[p,A,q]")，其语义为：从状态 $p$ 出发、栈顶为 $A$，读完某输入串后弹出 $A$ 并到达 $q$ 的串集合。
  起始产生式 $S arrow.r [q_0,z_0,q]$（$q$ 遍历 $Q$）。
]

= 3 程序设计思路 <sec:design>

== 整体架构

采用「数据结构 → 解析 → 算法 → CLI」四层流水线，与第 2 章形式化对象一一对应：

#seq-diagram(
  "
  cfg.py / pda.py          数据结构与合法性检查
  cfg_parser / pda_parser  文本 -> 对象
  cfg_simplifier           四步化简（可 verbose）
  pda_to_cfg + pda_convert PDA -> CFG（可选 simplify）
  main.py                  simplify | pda2cfg | demo
  ",
  [模块依赖（自上而下调用）],
)

== CFG 化简流水线

四步顺序固定，不可调换（第 4.3 节给出顺序必要性）：
#enum[
  (1) 消除 ε-产生式（nullable 不动点 + 右部组合展开）；
  (2) 消除单产生式（unit-closure + 非单产生式并入）；
  (3) 删除非生成符号（generating 不动点）；
  (4) 删除不可达符号（从 $S$ 的 BFS）。
]

== PDA 处理流水线

#enum[
  解析 PDA；若 accept 为终态则 #inline-code("convert_final_to_empty_stack")；
  #inline-code("pda_to_cfg") 构造 $[p,A,q]$ 变量与产生式；
  可选 #inline-code("--simplify") 对结果 CFG 再执行四步化简。
]

== CLI 设计要点

#hdr-table[
  #table(
    columns: (auto, 1fr),
    table.header([*命令*], [*说明*]),
    [#inline-code("simplify FILE")], [CFG 四步化简；#inline-code("-v") 分步输出；#inline-code("--keep-start-epsilon") 保留 $S arrow.r epsilon$],
    [#inline-code("pda2cfg FILE")], [PDA→CFG；#inline-code("--simplify") 继续化简；#inline-code("--format json|latex")],
    [#inline-code("demo")], [运行 v4 指定样例并打印期望输出],
  )
]

== 核心源文件职责

#hdr-table[
  #table(
    columns: (auto, 1fr),
    table.header([*文件*], [*职责*]),
    [#inline-code("cfg.py")], [CFG 数据类：变量集、产生式映射、拷贝与格式化],
    [#inline-code("cfg_parser.py")], [文本→CFG；支持 Unicode 箭头与 ε 别名],
    [#inline-code("cfg_simplifier.py")], [四步化简 + #inline-code("simplify_cfg_verbose")],
    [#inline-code("pda.py") / #inline-code("pda_parser.py")], [PDA 七元组与块/数学格式解析],
    [#inline-code("pda_to_cfg.py")], [[p,A,q] 变量构造与产生式枚举],
    [#inline-code("pda_convert.py")], [终态接受→空栈接受（选做）],
    [#inline-code("cfg_format.py")], [JSON / LaTeX 导出（选做）],
    [#inline-code("main.py")], [argparse 子命令与 stdin 管道],
  )
]

== 错误处理策略

解析阶段对非法产生式、未知符号引用抛出明确异常；化简阶段不修改输入对象（函数式返回新 #inline-code("CFG")）。CLI 捕获异常并以非零退出码打印错误信息，便于脚本化测试。

= 4 核心算法 <sec:algo>

本章给出算法步骤、正确性证明与复杂度分析，是报告的理论核心。

== ε-产生式消除

#algorithm("nullable 不动点与 ε-展开")[
  *输入*：CFG $G$。*输出*：无 ε-产生式（或保留 $S arrow.r epsilon$）的 $G'$。

  1. $N_0=emptyset$；重复：若 $A arrow.r alpha$ 且 $alpha$ 中符号均已在 $N$，则 $A in N$，直到 $N$ 不变。
  2. 对每个 $A arrow.r X_1 dots.h X_k$（$k>=1$），令 $I={i bar X_i in N}$；对每个 $J subset I$，添加 $A arrow.r$ 删去 $J$ 中位置后的右部。
  3. 删除所有 $A arrow.r epsilon$（默认含 $S$）；若 #inline-code("keep_start_epsilon") 且 $S in N$ 则保留 $S arrow.r epsilon$。
]

#theorem("ε-消除保持语言等价（空串不在语言中时）")[
  设 $G'$ 为对 CFG $G$ 执行 ε-消除算法的结果。若 $epsilon not in L(G)$，则 $L(G')=L(G)$。

  *证明*（对 $G$ 中推导步数 $n$ 归纳）：

  *(⇒)* 设 $S arrow.r_G^* w$ 且 $w != epsilon$，推导长度为 $n$。对 $n=0$ 无意义。对 $n>=1$，若最后一步未用 ε-产生式，则该步在 $P'$ 中仍合法。若最后一步为 $A arrow.r epsilon$，因 $epsilon not in L(G)$，此步必非唯一一步；存在更早句型含 $B arrow.r alpha A beta$。算法步骤 2 已将 $alpha$ 中 nullable 位置枚举展开，故 $G'$ 含 $B arrow.r alpha' beta$（删去 $A$），可构造长度更短的 $G$ 中推导，由归纳假设得 $S arrow.r_G'^* w$。

  *(⇐)* 设 $S arrow.r_G'^* w$。$G'$ 中每条产生式要么属于原 $P$（去掉 ε-产生式），要么为步骤 2 的「删 nullable 子集」变体。后者对应 $G$ 中：先保留 nullable 符号再一步 $arrow.r epsilon$，不增加新终结串；故 $w in L(G)$。

  *关键引理*：若 $A in N$ 且 $B arrow.r alpha A beta in P$，则 $G'$ 含 $B arrow.r alpha beta$（取 $J={i bar X_i=A}$）。归纳步用此替换一次 $A arrow.r epsilon$ 的使用。

  *基例* $n=1$：仅能用非 ε-产生式，$G'=G$ 在非 ε-产生式上相同。∎
]

*证明补充（nullable 不动点）*：初始 $N=emptyset$。每轮若 $A arrow.r alpha$ 且 $alpha$ 中符号均在 $N union Sigma$ 的 nullable 部分，则加入 $A$。因 $N$ 单调增且有上界 $|V|$，最多 $|V|$ 轮收敛；与程序 #inline-code("find_nullable_variables") 一致。

== 单产生式消除

#algorithm("unit-closure 替换")[
  对每个 $A in V$，用栈/队列 BFS 求 $U(A)={B bar A arrow.r^* B}$（仅经单产生式边）。
  对每个 $B in U(A)$、每条非单产生式 $B arrow.r beta$，加入 $A arrow.r beta$；最后删除所有单产生式。
]

#theorem("unit-closure 替换的完全性")[
  设 $G'$ 为对 $G$ 执行单产生式消除后的文法，则 $L(G')=L(G)$。

  *证明*：$U(A)$ 由显式栈迭代：初始 push $A$；若 $A arrow.r B$ 且 $B$ 未访问则 push $B$。因 $V$ 有穷，栈必在 $|V|$ 步内稳定，故 $U(A)$ 精确等于「仅经单产生式边可达的变量集」。

  *完全性*：若 $A arrow.r^* w$ 且首步为单产生式 $A arrow.r B$，则 $B arrow.r^* w$；单产生式图无环或有限环，链长 $< |V|$，必到达某 $C$ 使 $C arrow.r beta$ 非单。算法已将 $C$ 的非单产生式并入 $A$，故 $A arrow.r_G' w$。

  *不动点*：unit-closure 即单产生式图上的可达集；栈式 BFS 与迭代扩大 $U(A)$ 等价，至多 $|V|$ 轮。

  *可靠性*：$G'$ 中 $A arrow.r beta$ 要么来自原 $P$，要么来自某 $B in U(A)$ 的非单产生式；前者显然 $L(G)$；后者对应 $A arrow.r^* B arrow.r beta$。∎
]

== 无用符号消除 <sec:proof-order>

#algorithm("非生成与不可达")[
  *非生成*：$G_0=emptyset$；若 $A arrow.r alpha$ 且 $alpha$ 中符号均在 $G union Sigma$，则 $A in G$，迭代至不动点；删左部或右部含非生成变量的产生式。
  *不可达*：从 ${S}$ BFS 沿产生式右部变量扩展；只保留左部可达的产生式。
]

#theorem("消除顺序：先非生成、后不可达")[
  设 $G_1$ 为删非生成后的文法，$G_2$ 为再删不可达后的文法。则 $L(G_2)=L(G)$，且 $G_2$ 中变量均为*生成*且*可达*。

  *反例*（若先删不可达）：文法 $S arrow.r a A$，$A arrow.r b$，$B arrow.r c$。$B$ 生成但不可达。先删不可达得 ${S,A}$，再删非生成结果不变——本例顺序无关。换文法 $S arrow.r T a$，$T arrow.r T$（$T$ 可达但非生成）：先删不可达保留 $T$；先删非生成则删 $T arrow.r T$，再删不可达得仅 $S arrow.r a$ 的等价结果。真正风险在于：先删不可达可能保留大量「从 $S$ 不可达但 generating」的变量，增加后续步骤开销；教材标准顺序为先 semantic（生成）再 syntax（可达）。

  *单调性*：非生成变量不出现在任何 $S arrow.r^* w$（$w in Sigma^+$）的推导树中；不可达变量不出现在任何 $S arrow.r^*$ 句型中。删之不改变 $L(G)$。∎
]

== PDA 到 CFG

#algorithm("迁移到产生式")[
  对每个 $delta(p,a,A) supset (q, epsilon)$：添加 #inline-code("[p,A,q] -> a")。
  对每个 $delta(p,a,A) supset (q, B_1 dots.h B_k)$（$k>=1$）：对每个 $q_k in Q$ 与 $r_1,dots,r_(k-1) in Q$，添加
  #inline-code("[p,A,qk] -> a [q,B1,r1] ... [rk-1,Bk,qk]")。
  添加 $S arrow.r [q_0,z_0,q]$（$q in Q$）。
]

#theorem("PDA 计算与 CFG 推导等价")[
  对空栈 PDA $M$ 与构造文法 $G_M$，对任意 $p,q in Q$、$A in Gamma$、$w in Sigma^*$：
  $(p,w,A) arrow.r^* (q,epsilon,epsilon)$ 当且仅当 $[p,A,q] arrow.r^* w$（在 PDA 计算与 $G_M$ 推导意义下）。

  *证明*（对 PDA 接受计算步数 $m$ 归纳）：

  *Base* ($m=1$)：唯一一步为弹出，$delta(p,a,A) supset (q,epsilon)$，产生式 #inline-code("[p,A,q] -> a")，故 $[p,A,q] arrow.r a=w$。

  *Inductive* ($m>1$)：首步 $delta(p,a,A) supset (r, B_1 dots.h B_k)$（$k>=1$），剩余 $m-1$ 步依次清空栈。由归纳假设，存在 $r_0=r, r_1,dots,r_k=q$ 使各段 $w_i$ 由对应链变量生成，且 $w=a w_1 dots.h w_k$。产生式 #inline-code("[p,A,q] -> a [r,B1,r1]...[rk-1,Bk,q]") 给出最左推导。

  *反向*：对 $[p,A,q] arrow.r^* w$ 的最左推导，首步必为上述模板；各子变量推导对应栈上分段弹出，合成 PDA 接受计算。

  *为何枚举全部 $r_i$*：PDA 非确定性使「读同一输入段后到达何状态」不唯一；遗漏某 $r_i$ 会丢失对应串。指定 PDA 中 $|Q|=2$ 故每条压栈迁移最多 $2^k$ 条产生式。∎
]

*引理细化（压栈 $k=2$）*：设 $delta(p,a,A) supset (r,B C)$。产生式 #inline-code("[p,A,q2] -> a [r,B,r1] [r1,C,q2]") 表示：读 $a$ 后，由 #inline-code("[r,B,r1]") 生成 $w_1$、#inline-code("[r1,C,q2]") 生成 $w_2$，且 $w=a w_1 w_2$。归纳假设保证 $w_1,w_2$ 与子格局一一对应。

*引理细化（弹出）*：$delta(p,a,A) supset (q,epsilon)$ 时无中间变量，对应产生式右部长度 1，与 Base case 一致。

*程序实现对应*：#inline-code("pda_to_cfg.py") 对每条迁移双重循环 $q_k in Q$ 与中间状态笛卡尔积（标准库 #inline-code("itertools.product")），与证明中「枚举全部中间状态序列」同构。

== 复杂度分析

记 $|V|$ 为变量数，$|P|$ 为产生式数，$K$ 为右部最大长度；PDA 中 $|Q|$、$|Gamma|$、$|delta|$，$K_max$ 为最大压栈长度。

=== CFG 化简各步

- *nullable 不动点*：每轮扫描 $|P|$ 条产生式，最多 $|V|$ 轮，$O(|V| dot |P| dot K)$。
- *ε 展开*：单条产生式含 $n$ 个 nullable 符号时枚举 $2^n$ 子集，最坏 $O(|P| dot 2^K)$。
- *unit-closure*：每个变量 BFS $O(|V|+|P|)$，共 $|V|$ 次，$O(|V| dot (|V|+|P|))$。
- *非生成不动点*：同 nullable，$O(|V| dot |P| dot K)$。
- *可达 BFS*：$O(|V|+|P|)$。

=== PDA→CFG

- 变量数：$|Q|^2 |Gamma| + 1$。
- 产生式：每条迁移压栈 $k$ 时 $O(|Q|^k)$；总计 $O(|delta| dot |Q|^K_max)$。
- 实践：指定 PDA $|Q|=2$，$K_max=2$，指数因子为 $4$；压栈 3 测试 $|Q|=2$ 时单迁移最多 $8$ 条（第 6.6 节）。

=== 空间复杂度

- CFG 化简：存储中间文法 $O(|P| dot K)$；ε 展开最坏复制 $2^K$ 倍产生式。
- PDA→CFG：变量 $O(|Q|^2 |Gamma|)$，产生式最坏 $O(|delta| dot |Q|^K_max dot K_max)$。
- 程序采用不可变 #inline-code("CFG") 对象逐步替换，峰值内存与最终文法规模同阶。

=== 指定样例数量级

指定 CFG：$|V|=5$，$|P|=8$，$K=3$。nullable 约 $5 times 8 = 40$ 次检查；含 $A$ 的产生式展开 $2^1$；unit-closure 约 $5 times 13 = 65$；整体 $< 10^3$ 次基本操作。

*逐式估算（ε 展开）*：
#enum[
  $S arrow.r b A$：1 个 nullable 位，展开为 $2^1=2$ 条变体；
  $B arrow.r a A$：1 个 nullable 位，展开为 $2$ 条变体；
  其余产生式无 nullable 位，保持不变；
  合计新增约 2 条候选（#inline-code("S->b")、#inline-code("B->a")）。
]

*逐式估算（PDA 指定样例）*：$|Q|=2$，$|delta|=6$；压栈长度 2 的迁移 4 条，每条 $2^2=4$ 变体；弹出 2 条各 1 变体；合计约 $4 times 4 + 2 = 18$ 量级（与程序输出 14 条候选同阶）。

#hdr-table[
  #figure(
    table(
      columns: (auto, auto, auto),
      align: (left, center, left),
      table.header([*步骤*], [*时间复杂度*], [*关键因子*]),
      [nullable / 非生成], [$O(|V| dot |P| dot K)$], [不动点迭代轮数],
      [ε 展开], [$O(|P| dot 2^K)$], [单条右部 nullable 个数],
      [unit-closure], [$O(|V| dot (|V|+|P|))$], [单产生式图 BFS],
      [可达 BFS], [$O(|V|+|P|)$], [产生式右部总长度],
      [PDA 变元构造], [$O(|Q|^2 |Gamma|)$], [状态与栈符号笛卡尔积],
      [PDA 产生式生成], [$O(|delta| dot |Q|^K_max)$], [压栈长度指数],
      [整流水线（CFG）], [乘积上界], [通常 $|V|,|P| < 20$ 可瞬时完成],
    ),
    caption: [算法复杂度汇总（第 4 章）],
  )
]

= 5 输入与输出格式 <sec:io>

== CFG 输入 <sec:io-cfg>

#payload-block(
  ```
  S -> a | b A | B | c c D
  A -> a b B | eps
  B -> a A
  C -> d d C
  D -> d d d
  ```,
  title: [块格式（#inline-code("examples/grammar_sample.txt")）],
)

箭头支持 #inline-code("->")、#inline-code("=>")、#inline-code("→")；ε 别名 #inline-code("epsilon")/#inline-code("eps")/#inline-code("ε")；#inline-code("|") 分隔候选；#inline-code("#") 行注释。

== PDA 输入 <sec:io-pda>

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
  title: [块格式（#inline-code("examples/pda_sample.txt")）],
)

亦支持数学格式 #inline-code("delta(q,a,A)={(q,...)")}；#inline-code("accept: empty_stack") 表示 $Phi$ 空栈接受。

== 输出约定

- 默认文本：变量按字典序，$S$ 置顶；多字符符号空格分隔；ε 打印为 #inline-code("epsilon")。
- #inline-code("--format json")：结构化 #inline-code("variables/terminals/productions/start")。
- #inline-code("--format latex")：LaTeX 产生式，如 $S arrow.r a mid b A$。

= 6 测试用例与执行效果 <sec:test>

== 指定 CFG 化简（任务一）

*目的*：验证 v4 指定 CFG 四步化简结果。

*输入*：#inline-code("examples/grammar_sample.txt")。

*命令*：#inline-code("py main.py simplify examples\\grammar_sample.txt")。

*输出*：

#payload-block(
  ```
  S -> a | aA | b | bA | ccD
  A -> abB
  B -> a | aA
  D -> ddd
  ```,
)

*分析*：$C$ 非生成被删；$A arrow.r epsilon$ 与 $S arrow.r B$ 已消除；与 v4 期望一致。

#figure(
  image("screenshots/6-1-cfg-simplify.png", width: 100%),
  caption: [指定 CFG 化简终端截图],
)

=== CFG 逐步追踪 <sec:cfg-trace>

以下为人工作注释的推理（非 #inline-code("--verbose") 原样转储），对应第 2 章指定 CFG。

*Step 1 nullable*：第一轮：$A arrow.r epsilon$ 得 $A in N$。第二轮：$B arrow.r a A$ 需 $a in N$（终结符永不在 $N$），故 $B not in N$；$S arrow.r b A$ 需 $b,A$ 均在 $N$，$b not in N$，故 $S not in N$。结论 $N={A}$。（注：$B$ 可推导终结串但不可推导 $epsilon$。）

*Step 2 ε 展开*：对含 $A in N$ 的产生式展开：
#align(center)[
  $S arrow.r b A$ 得 $S arrow.r b$；$B arrow.r a A$ 得 $B arrow.r a$；其余不变；删 $A arrow.r epsilon$。
]

*Step 3 unit-closure*：$S arrow.r B$ 为单产生式，$U(S)={S,B}$（$B$ 无单产生式出边）。将 $B$ 的非单产生式 $B arrow.r a A bar a$ 并入 $S$。

*Step 4 单产生式替换后*：删 $S arrow.r B$ 等单产生式；保留 $S arrow.r a bar a A bar b bar b A bar c c D$ 等。

*Step 5 非生成*：$C arrow.r d d C$ 无法到达终结符串，$C not in$ generating；删除 $C$ 及相关产生式。

*Step 6 不可达*：从 $S$ BFS 得 ${S,A,B,D}$ 均可达；无新增删除。

*Step 7 最终*：4 个变量、8 条候选产生式（化简后 4 行输出）。

*Step 8 与程序对照*：#inline-code("--verbose") 四步输出与上表一致——(1) 后含 #inline-code("S->b")、#inline-code("B->a")；(2) 后 #inline-code("S->a|aA|b|bA|ccD")；(3) 后删 #inline-code("C->ddC")；(4) 无变化。

#payload-block(
  ```
  py main.py simplify examples/grammar_sample.txt --verbose
  === final ===
  S -> a | aA | b | bA | ccD
  A -> abB
  B -> a | aA
  D -> ddd
  ```,
  title: [verbose 最终步与 Step 8 一致],
)

== 指定 PDA 转换（任务二）

=== 要求 (1)：仅 PDA→CFG

*命令*：#inline-code("py main.py pda2cfg examples\\pda_sample.txt")。

*关键输出*：约 9 个变量（$S$ 加 8 个 #inline-code("[p,A,q]")），14 条产生式候选（见下文 PDA 追踪 Step 4）。

=== 要求 (2)：转换后再化简

*命令*：#inline-code("py main.py pda2cfg examples\\pda_sample.txt --simplify")。

#payload-block(
  ```
  S -> b [q0,B,q1]
  [q0,B,q1] -> a | b [q0,B,q1] | b [q0,B,q1] [q1,B,q1]
  [q1,B,q1] -> a
  ```,
)

*分析*：语言 $L={b^m a^n bar m,n >= 1, n <= m}$（非 $b^n a^n$）。BFS 可生成 #inline-code("ba")、#inline-code("bbbaaa")；不可生成 #inline-code("baa")。

#figure(
  image("screenshots/6-2-pda2cfg-simplify.png", width: 100%),
  caption: [PDA 转 CFG 并化简截图],
)

=== PDA 逐步追踪 <sec:pda-trace>

*Step 1 变量*：$|Q|=2$，$|Gamma|=2$，共 $2^2 times 2=8$ 个 #inline-code("[p,A,q]") 加 $S$。

*Step 2 起始产生式*：$S arrow.r [q_0,z_0,q_0] bar [q_0,z_0,q_1]$。

*Step 3 迁移分析*：
#enum[
  $delta(q_0,b,z_0)={(q_0,B z_0)}$，$k=2$：4 条 #inline-code("[q0,z0,qk] -> b [q0,B,r] [r,z0,qk]")；
  $delta(q_0,b,B)={(q_0,B B)}$，$k=2$：4 条 #inline-code("[q0,B,qk] -> b ...")；
  $delta(q_0,a,B)={(q_1,epsilon)}$：1 条 #inline-code("[q0,B,q1] -> a")；
  $delta(q_1,a,B)={(q_1,epsilon)}$：1 条 #inline-code("[q1,B,q1] -> a")；
  $delta(q_1,epsilon,B)={(q_1,epsilon)}$：1 条 #inline-code("[q1,B,q1] -> epsilon")；
  $delta(q_1,epsilon,z_0)={(q_1,epsilon)}$：1 条 #inline-code("[q1,z0,q1] -> epsilon")。
]

*Step 4*：化简前共 14 条产生式（部分变量无产生式）。

*Step 5 化简后 4 条*：分别对应「读 $b$ 入栈」「读 $b$ 复制栈符号」「读 $a$ 弹栈」「$q_1$ 自环弹 $B$」四种模式。

*Step 6 语义验证*：对化简 CFG 枚举 $|w|<=4$ 的生成串，与 $b^m a^n$ 约束一致。

*Step 7 与 v4 两步对照*：要求 (1) 仅 #inline-code("pda2cfg") 时保留全部 #inline-code("[q0,B,q1]") 链；要求 (2) #inline-code("--simplify") 后仅 4 条产生式，与任务书样例输出一致。

*Step 8 BFS 短串表*（化简后 CFG，$|w|<=3$ 可生成）：

#hdr-table[
  #table(
    columns: (auto, auto),
    table.header([*串*], [*是否属于* $L$]),
    [#inline-code("ba")], [是],
    [#inline-code("bba")], [是],
    [#inline-code("bbba")], [是],
    [#inline-code("baa")], [否（$n > m$）],
    [#inline-code("ab")], [否（须先读 $b$）],
  )
]

== 边界用例 3：纯 ε 文法

*目的*：验证默认删 $S arrow.r epsilon$ 与 #inline-code("--keep-start-epsilon") 行为。

*输入*：#inline-code("examples/case_epsilon.txt")（$S arrow.r epsilon$）。

*推理*：$N={S}$；默认模式删 $S arrow.r epsilon$ 后无产生式，文法为空；keep 模式保留 $S arrow.r epsilon$，语言仍为 ${epsilon}$。

*输出（默认）*：空（无产生式打印）。

*输出（keep）*：#inline-code("S -> epsilon")。

*命令*：#inline-code("py main.py simplify examples\\case_epsilon.txt")；#inline-code("py main.py simplify examples\\case_epsilon.txt --keep-start-epsilon")。

#figure(
  image("screenshots/6-4-epsilon.png", width: 100%),
  caption: [纯 ε 文法化简截图],
)

== 边界用例 4：单元环

*目的*：验证 $S arrow.r A arrow.r B arrow.r C arrow.r A bar a$ 不陷入死循环。

*输入*：#inline-code("examples/case_unit_cycle.txt")。

*推理*：$U(S)={S,A,B,C}$；并入 $C arrow.r a$ 后 $S arrow.r a$；单产生式全部删除；BFS 不陷入 $A arrow.r B arrow.r C arrow.r A$ 环。

*输出*：#inline-code("S -> a")。

*命令*：#inline-code("py main.py simplify examples\\case_unit_cycle.txt")。

#figure(
  image("screenshots/6-5-unit-cycle.png", width: 100%),
  caption: [单元环化简截图],
)

== 边界用例 5：不可达变量

*目的*：$B$ 生成但不可达，应在 Step 4 删除。

*输入*：#inline-code("examples/case_unreachable.txt")（$S arrow.r a A$，$A arrow.r b$，$B arrow.r c$）。

*推理*：Step 3 后 ${S,A,B}$ 均 generating；Step 4 从 $S$ 仅可达 ${S,A}$，删 $B arrow.r c$ 与变量 $B$。

*输出*：#inline-code("S -> a A") 与 #inline-code("A -> b")（或等价分行）。

*命令*：#inline-code("py main.py simplify examples\\case_unreachable.txt")。

#figure(
  image("screenshots/6-6-unreachable.png", width: 100%),
  caption: [不可达变量删除截图],
)

== 边界用例 6：压栈长度 3 <sec:test-push3>

*目的*：验证 $delta(p,a,A)={(q,B C D)}$ 时产生式右部长度为 $1+3=4$（$a$ 加三个 #inline-code("[..]") 变量）。

*输入*：#inline-code("examples/case_push3.txt")。

*推理*：$|Q|=2$ 时需枚举 $r_1,r_2 in Q$ 与 $q_3 in Q$，单迁移最多 $2^2 times 2=8$ 条产生式；$|Q|=3$ 时为 $27$ 条。右部长度 $1+3=4$（终结符 $a$ 加三个链变量）。

*命令*：#inline-code("py main.py pda2cfg examples\\case_push3.txt")。

*单元测试*：#inline-code("test_push_length_three_generates_long_rhs") 断言存在长度 4 的右部。

#figure(
  image("screenshots/6-7-push3.png", width: 100%),
  caption: [压栈长度 3 的 PDA→CFG 截图],
)

== 自动化测试

24 项 #inline-code("unittest") 覆盖指定样例、verbose、keep-start-epsilon、JSON/LaTeX、终态 PDA 转换、压栈 3 等。

#payload-block(
  ```
  py -m unittest discover -s tests
  Ran 24 tests in 0.01s — OK
  ```,
)

#figure(
  image("screenshots/6-3-unittest.png", width: 100%),
  caption: [单元测试运行截图],
)

== 已实现扩展功能摘要

#hdr-table[
  #table(
    columns: (auto, 1fr),
    table.header([*功能*], [*说明*]),
    [#inline-code("--verbose")], [四步中间文法，对应第 6.1 节 Step 8],
    [#inline-code("--keep-start-epsilon")], [保留 $S arrow.r epsilon$，见用例 3],
    [#inline-code("--format json|latex")], [机器可读 / 论文排版输出],
    [终态 PDA 自动转换], [#inline-code("pda_convert.py")],
    [24 项 unittest], [含 verbose、format、压栈 3、单元环等],
  )
]

可执行程序：#inline-code("pyinstaller --onefile --name formal_lang_lab2 main.py") → #inline-code("dist/formal_lang_lab2.exe demo")。

= 7 改进思路 <sec:improve>

以下每条为微型提案：问题 → 方案 → 技术点 → 预期收益。

== GUI 分步可视化

*问题*：#inline-code("--verbose") 仅文本，难以对比相邻步骤差异。

*方案*：Streamlit 应用，#inline-code("st.session_state") 保存 #inline-code("simplify_cfg_verbose") 四步快照，#inline-code("st.selectbox") 切换步骤，#inline-code("st.table") 展示产生式。

*技术点*：#inline-code("[p,A,q]") 变量需折叠显示或语法高亮；并支持 diff 高亮新增/删除的产生式。

*预期收益*：实验演示与调试效率提升，助教批改时可逐步核对。

== LL(1)/LR(1) 分析器集成

*问题*：化简后 CFG 仍可能有左递归，无法直接 LL(1) 解析。

*方案*：在化简流水线后增加左递归消除与左公因子提取模块，输出 FIRST/FOLLOW 表与 LL(1) 判定结果。

*技术点*：与 unit-closure 协同，避免重复扫描；对 PDA 来源 CFG 需先重命名 $[p,A,q]$ 为普通非终结符。

*预期收益*：从「文法工具」延伸到「编译器前端原型」。

== 推导树生成与对比

*问题*：化简前后语言等价性缺乏直观证据。

*方案*：对给定串 $w$，用 CYK 或 Earley 在化简前后 CFG 上各建推导树，Graphviz #inline-code("dot") 输出 PNG，Typst #inline-code("#figure(image(...))") 嵌入报告。

*技术点*：需限制 $|w|<=10$ 防止指数爆炸；对指定 CFG 可选固定展示 #inline-code("babab") 的推导树。

*预期收益*：教学与验收可视化。

== 大文法性能基准

*问题*：最坏 $O(|P| dot 2^K)$ 缺乏实测数据。

*方案*：随机 CFG 生成器（控制 $|V|,|P|,K$），在 10/50/100/500 产生式规模下测量四步耗时，绘制折线图。

*技术点*：固定随机种子保证可复现；分别记录 nullable 与 ε 展开耗时占比。

*预期收益*：指导输入规模与优化优先级。

== 并行化 nullable / generating

*问题*：不动点迭代在 $|V|$ 大时串行扫描慢。

*方案*：将变量更新视为数据流方程，按依赖分片并行（需保证轮次同步）。

*技术点*：Python #inline-code("concurrent.futures") 按产生式分块；每轮 barrier 后合并 $N$ 或 generating 集。

*预期收益*：大规模文法化简加速（理论）。

== Unicode 输入增强

*问题*：已支持 $delta,epsilon,Phi$，但全角希腊字母或数学粗体仍可能解析失败。

*方案*：在 #inline-code("cfg_parser.py") 入口增加 Unicode 归一化表（NFKC + 自定义映射）。

*技术点*：映射表覆盖 $arrow.r, epsilon, delta$ 常见异体；单元测试逐字符断言。

*预期收益*：降低用户输入摩擦，兼容 Word 粘贴。

== WebAssembly 浏览器端运行

*问题*：需安装 Python 或下载 exe。

*方案*：Pyodide 打包 #inline-code("main.py") 核心逻辑，静态页提供 simplify/pda2cfg 表单。

*技术点*：裁剪 #inline-code("tests/") 与 PyInstaller 依赖；stdout 重定向到页面 pre 块。

*预期收益*：零安装在线试用，便于助教批改与课堂演示。

= 附录 A：关键代码接口（≤ 40 行）

#payload-block(
  ```python
  def simplify_cfg(g, keep_start_epsilon=False) -> CFG: ...
  def simplify_cfg_verbose(g) -> tuple[CFG, list]: ...
  def pda_to_cfg(pda) -> CFG: ...
  def convert_final_to_empty_stack(pda) -> PDA: ...
  # CLI: simplify | pda2cfg | demo
  # Flags: --verbose, --keep-start-epsilon, --format json|latex, --simplify
  ```,
  title: [#inline-code("cfg_simplifier.py") / #inline-code("pda_to_cfg.py") / #inline-code("main.py") 入口摘要],
)
'''

def main() -> None:
    content = COVER + BODY
    OUT.write_text(content, encoding="utf-8")
    lines = content.count("\n") + 1
    print(f"Wrote {OUT} ({lines} lines)")

if __name__ == "__main__":
    main()
