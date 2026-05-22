// 形式语言与自动机实验报告 — 共用排版（参照本组 DataLink / NFA 实验报告风格）
// 在 docs/实验报告.typ 中：#import "typst-preamble.typ": *

#set document(
  title: [形式语言与自动机实验（二）实验报告],
  author: ("张恒基", "林旭东", "尹浩铭", "赵博宇"),
)

#let accent = rgb("#1e3a5f")
#let accent-light = rgb("#e8eef5")
#let rule-color = rgb("#cbd5e1")
#let muted = rgb("#64748b")

#let font-en = "Times New Roman"
#let font-body = (font-en, "SimSun", "STSong")
#let font-heading = (font-en, "SimHei", "Microsoft YaHei", "SimSun")
#let sz-body = 10.5pt
#let sz-code = 10.5pt
#let lead-body = 1.28em
#let space-par = 1.0em

#set page(
  paper: "a4",
  margin: (x: 2.6cm, y: 2.5cm),
  header: context [
    #set text(font: font-body, size: 9pt, fill: muted)
    #grid(
      columns: (1fr, 1fr),
      align: (left, right),
      [形式语言与自动机 · 实验二],
      [CFG 化简与 PDA 转 CFG 实验报告],
    )
    #line(length: 100%, stroke: 0.4pt + rule-color)
    #v(4pt)
  ],
  footer: context [
    #line(length: 100%, stroke: 0.4pt + rule-color)
    #v(4pt)
    #set text(font: font-body, size: 9pt, fill: muted)
    #align(center)[#counter(page).display("1")]
  ],
)

#set text(font: font-body, size: sz-body, weight: "regular", lang: "zh", region: "cn")
#show strong: it => it
#show emph: it => it
#set par(justify: true, first-line-indent: 2em, leading: lead-body, spacing: space-par)
#set list(spacing: space-par, body-indent: 0.5em)
#set enum(spacing: space-par, body-indent: 0.5em)

#let cn-section = ("一", "二", "三", "四", "五", "六", "七", "八")
#set heading(numbering: (..nums) => {
  let n = nums.pos()
  if n.len() == 1 [#cn-section.at(n.first() - 1)、] else if n.len() == 2 [#n.at(0).#n.at(1)] else [#n.at(0).#n.at(1).#n.at(2)]
})
#set figure(gap: 0.6em, placement: none)
#show figure: set block(breakable: true)

#show heading.where(level: 1): it => {
  set text(font: font-heading, weight: "regular")
  v(1.4em, weak: true)
  text(size: 15pt, fill: accent)[#it]
  v(0.85em, weak: true)
}
#show heading.where(level: 2): it => {
  set text(font: font-heading, weight: "regular")
  v(1em, weak: true)
  text(size: 12.5pt, fill: accent)[#it]
  v(0.65em, weak: true)
}
#show outline.entry: it => {
  set par(leading: 1.05em, spacing: 0.16em, first-line-indent: 0em)
  set text(font: font-body, size: 9.5pt, weight: "regular", fill: black)
  it
}
#show outline.entry.where(level: 1): it => {
  set text(size: 10pt)
  set par(spacing: 0.28em)
  it
}
#show figure.caption: set text(font: font-body, size: sz-body, weight: "regular")
#show table: it => block(width: 100%)[#it]
#show table: set table(stroke: 0.45pt + rule-color, inset: (x: 10pt, y: 12pt))
#show table.cell: it => {
  set par(first-line-indent: 0em, justify: false, leading: lead-body, spacing: 0.55em)
  set text(font: font-body, size: sz-body, weight: "regular")
  set align(left + top)
  it
}
#show table.header: it => {
  set table(fill: accent-light, stroke: (bottom: 0.8pt + accent))
  set text(font: font-body, size: sz-body, weight: "regular")
  set par(leading: lead-body, spacing: 0.45em)
  set align(left + top)
  it
}

#let code-in-cell(s) = block(width: 100%)[
  #text(font: ("Consolas", "Courier New", font-en), size: sz-code, weight: "regular")[#raw(s, lang: none)]
]
#show raw.where(block: true): set block(
  fill: luma(248),
  stroke: 0.5pt + rule-color,
  radius: 3pt,
  inset: 10pt,
  width: 100%,
)
#show raw: set text(font: ("Consolas", "Courier New", font-en), size: sz-code, weight: "regular")

#let toc-page() = {
  page(header: none, footer: none, numbering: none, margin: (x: 2.6cm, y: 2.1cm))[
    #set par(leading: 1.05em, spacing: 0em)
    #align(center)[
      #text(font: font-heading, fill: accent, weight: "regular", size: 13pt)[目　录]
      #v(0.55em, weak: true)
    ]
    #outline(indent: 0.95em, depth: 2)
  ]
  pagebreak()
  counter(page).update(1)
}
