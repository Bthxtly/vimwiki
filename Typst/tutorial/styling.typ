#let title = [
  A fluid dynamic model for glacier flow
]

// paper size, header and numbering
#set page(
  paper: "us-letter",
  header: align(
    right + horizon,
    title,
  ),
  numbering: "1",
  columns: 2,
)

#place(
  top + center,
  float: true,
  scope: "parent",
  clearance: 2em,
)[
  // justify
  #set par(justify: true)

  //font
  #set text(
    font: "Libertinus Serif",
    size: 11pt,
  )

  // title
  #align(
    text(17pt)[
      *#title*
    ],
  )

  // authors
  #grid(
    columns: (1fr, 1fr),
    [
      Therese Tungsten \
      Artos Institute \
      #link("mailto:tung@artos.edu")
    ],
    [
      Dr. John Doe \
      Artos Institute \
      #link("mailto:doe@artos.edu")
    ],
  )

  // abstract
  #set par(justify: false)
  *Abstract* \
  #lorem(80)
]

// custom heading
#show heading.where(level: 1): it => block(width: 100%)[
  #set align(center)
  #set text(13pt, weight: "regular")
  #smallcaps(it.body)
]

#show heading.where(level: 2): it => text(
  size: 11pt,
  weight: "regular",
  style: "italic",
  it.body + [.],
)


// main text
= Introduction
#lorem(100)

== Motivation
#lorem(200)

= Related Work
#lorem(200)
