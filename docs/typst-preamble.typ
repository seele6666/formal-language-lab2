// 形式语言实验报告 — 排版与 Unveil INTERFACE.typ 一致
// 在 docs/实验报告.typ 中：#import "typst-preamble.typ": *

#let page-footer = context place(
  bottom + center,
  dy: -14pt,
)[
  #text(size: 10.5pt, fill: rgb(148, 163, 184))[#counter(page).display()]
]

#set page(
  margin: (left: 2.5cm, right: 2.5cm, top: 2.2cm, bottom: 2.2cm),
  numbering: "1",
  footer: page-footer,
)

#let main-font = ("SimSun", "SimHei", "Microsoft YaHei")
#set text(font: main-font, size: 12pt)
#set par(leading: 0.85em, first-line-indent: 0pt, spacing: 0.65em)
#set heading(numbering: "1.")

#let h1-size = 20pt
#let h2-size = 15pt
#let h3-size = 13pt
#let code-size = 10.5pt
#let seq-size = 11pt
#let payload-size = 9pt
#let caption-size = 11pt
#let hint-size = 11pt

#show heading: set text(font: main-font)

#show heading.where(level: 1): it => {
  block(breakable: false, above: 2em, below: 1em)[
    #block(
      width: 100%,
      inset: (left: 10pt, top: 10pt, bottom: 10pt),
      fill: rgb("#eff6ff"),
      radius: 4pt,
      stroke: (left: 4pt + rgb("#1e40af")),
    )[
      #text(size: h1-size, weight: "bold", fill: rgb("#1e3a8a"))[#it]
    ]
  ]
}
#show heading.where(level: 2): it => {
  block(above: 1.4em, below: 0.7em)[
    #text(size: h2-size, weight: "bold", fill: rgb("#1e40af"))[#it]
    #v(0.15em)
    #line(length: 100%, stroke: 0.5pt + rgb("#bfdbfe"))
  ]
}
#show heading.where(level: 3): it => {
  block(above: 1.1em, below: 0.55em)[
    #text(size: h3-size, weight: "bold", fill: rgb("#334155"))[#it]
  ]
}

#show figure.caption: set text(size: caption-size)
#set table(inset: (x: 10pt, y: 8pt))

#let mono-font = ("Consolas", "Courier New", "DejaVu Sans Mono")
#show raw.where(block: false): set text(font: mono-font, size: code-size)

#let inline-code(s) = text(font: mono-font, size: code-size)[#raw(s, lang: none)]

#let as_payload_str(content) = {
  if type(content) == str { content } else { content.text }
}

#let seq-diagram(content, caption, roles: none) = figure(
  block(
    width: 100%,
    fill: rgb("#f8fafc"),
    inset: 14pt,
    radius: 4pt,
    stroke: 0.5pt + rgb("#e2e8f0"),
    breakable: true,
  )[
    #if roles != none [
      #align(center)[
        #text(size: hint-size, fill: rgb("#334155"))[#roles]
      ]
      #v(8pt)
    ]
    #set text(font: mono-font, size: seq-size)
    #set par(leading: 0.75em, spacing: 0pt)
    #raw(block: true, lang: "text", as_payload_str(content).trim())
  ],
  caption: caption,
)

#let payload-block(content, title: none) = block(
  width: 100%,
  fill: rgb("#f8fafc"),
  inset: 12pt,
  radius: 4pt,
  stroke: 0.5pt + rgb("#e2e8f0"),
  breakable: true,
)[
  #if title != none [
    #text(weight: "bold", size: hint-size)[#title]
    #v(6pt)
  ]
  #set text(font: mono-font, size: payload-size)
  #set par(leading: 0.62em, spacing: 0pt)
  #for line in as_payload_str(content).trim().split("\n") {
    let row = line.trim()
    if row.len() > 0 [
      #raw(row)
      #linebreak()
    ]
  }
]

#show raw.where(block: true): it => block(
  width: 100%,
  breakable: true,
  fill: rgb("#f8fafc"),
  inset: 10pt,
  radius: 3pt,
  stroke: 0.5pt + rgb("#e2e8f0"),
)[
  #set text(font: mono-font, size: code-size)
  #set par(leading: 0.65em)
  #it
]

#let hdr-table(body) = {
  show table: set table(
    stroke: (x, y) => if y < 1 { (bottom: 0.5pt + black) },
  )
  body
}

#let def-counter = counter("definition")
#let thm-counter = counter("theorem")
#let alg-counter = counter("algorithm")

#let definition(title, body) = {
  def-counter.step()
  figure(
    kind: "definition",
    supplement: [定义],
    caption: context [#def-counter.display(). #title],
    body,
  )
}

#let theorem(title, body) = {
  thm-counter.step()
  figure(
    kind: "theorem",
    supplement: [定理],
    caption: context [#thm-counter.display(). #title],
    body,
  )
}

#let algorithm(title, body) = {
  alg-counter.step()
  figure(
    kind: "algorithm",
    supplement: [算法],
    caption: context [#alg-counter.display(). #title],
    body,
  )
}

#let body-start() = {
  pagebreak()
  set page(numbering: none, footer: none)
  outline(title: "目录", indent: 2em)
  pagebreak()
  set page(numbering: "1", footer: page-footer)
  counter(page).update(1)
}
