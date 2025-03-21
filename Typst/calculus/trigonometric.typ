#import "@preview/cetz:0.3.4"

#grid(
  gutter: 10pt,
  // trigonometric functions
  cetz.canvas({
    import cetz.draw: *
    set-style(stroke: blue)
    line((0, 0), (4, 0), name: "adj")
    line((4, 0), (4, 3), name: "opp")
    line((4, 3), (0, 0), name: "hyp")
    content("adj", [adjacent], padding: .1, anchor: "north")
    content("opp", [opposite], padding: .1, anchor: "west")
    content("hyp", [hypotenuse], padding: .2, anchor: "east")

    line((3.7, 0), (3.7, 0.3), (4, 0.3), stroke: black + .4pt)
    arc(
      (1, 0),
      start: 0deg,
      stop: 19deg,
      radius: 2,
      stroke: red,
      name: "arc",
      mark: (end: "straight", stroke: red + .4pt),
    )
    content(
      ("arc.start", 50%, "arc.end"),
      [$theta$],
      padding: .2,
      anchor: "west",
    )
  }),
  grid(
    columns: 2,
    rows: 3,
    gutter: 10pt,
    $ sin theta = "opp" / "hyp" $, $ csc theta = "hyp" / "opp" $,
    $ cos theta = "adj" / "hyp" $, $ sec theta = "hyp" / "adj" $,
    $ tan theta = "opp" / "adj" $, $ cot theta = "adj" / "opp" $,
  )
)
