# 形式语言与自动机实验（二）：上下文无关文法与下推自动机

> 完整要求见 `docs/形式语言与自动机课程实验（二）v4.docx`  
> 符合性对照见 `docs/v4-要求对照.md`

本项目实现两个核心功能：

1. 上下文无关文法 CFG 的化简：
   - 消除 epsilon 产生式；
   - 消除单产生式；
   - 消除无用符号，包括不能推出终结符串的符号和不可达符号。
2. 由下推自动机 PDA 构造等价上下文无关文法 CFG，并继续调用 CFG 化简算法。

## 指定 CFG 样例

```text
S -> a | bA | B | ccD
A -> abB | epsilon
B -> aA
C -> ddC
D -> ddd
```

期望化简后没有 epsilon 产生式、单产生式、不能推出终结符串的符号或不可达符号。

## 指定 PDA 样例

```text
M = ({q0,q1}, {a,b}, {B,z0}, delta, q0, z0, empty)
delta(q0,b,z0) = {(q0,Bz0)}
delta(q0,b,B) = {(q0,BB)}
delta(q0,a,B) = {(q1,epsilon)}
delta(q1,a,B) = {(q1,epsilon)}
delta(q1,epsilon,B) = {(q1,epsilon)}
delta(q1,epsilon,z0) = {(q1,epsilon)}
```

该 PDA 以空栈接受。PDA 转 CFG 后，应能继续调用 CFG 化简算法输出等价的简化 CFG。
