= Set rules
== text
With the `text` function, we can adjust the font for all text within it.

the quick brown fox jumps over the lazy dog

#text(font: "New Computer Modern")[
  the quick brown fox jumps over the lazy dog
]

To apply style properties to all occurrences of some kind of content, use _set rules_.

#set text(font: "New Computer Modern")
the quick brown fox jumps over the lazy dog

== others
There are other functions that are commonly used in set rules:
- `text` to set font family, size, color, and other properties of text
- `page` to set the page size, margins, headers, enable columns, and footers
- `par` to justify paragraphs, set line spacing, and more
- `heading` to set the appearance of headings and enable numbering
- `document` to set the metadata contained in the PDF output like title, author

Here is an example:
#grid(
  columns: 2,
  gutter: 2mm,
  rect(```typst
  #set page(paper: "a6", margin: (x: 1.8cm, y: 1.5cm))
  #set text(font: "New Computer Modern", size: 10pt)
  #set par(justify: true, leading: 0.52em)

  = Introduction
  In this report, we will explore the various factors that influence fluid
  dynamics in glaciers and how they contribute to the formation and behaviour of
  these natural structures.

  ...

  #align(center + bottom)[
    #image("typst.png" width: 70%)

    *Glaciers form an important part of the earth's climate system.*
  ]
  ```),
  rect(image("image/formatting.png")),
)

#set heading(numbering: "1.a")
= Number headings
Can be easily done with `#set heading(numbering: "1.")`
== `lorem`
Use this function to generate some placeholder text.== Foo
#lorem(10)
== Bar
#lorem(12)

= Show rules
Define a custom function. For example, yields the logo with its image to avoid
tedious typing.

#show "Typst": name => box[
  #box(image("image/typst.png", height: 0.7em))
  #name
]

Typst is fantastic! I love Typst!
