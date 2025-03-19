#grid(
  gutter: 10pt,
  // triangle
  polygon(
    fill: none,
    stroke: blue,
    (4cm, 0pt),
    (4cm, 3cm),
    (0pt, 3cm),
  ),
  // trigonometric functions
  grid(
    columns: 2,
    rows: 3,
    gutter: 10pt,
    $ sin theta = "opp" / "hyp" $, $ csc theta = "hyp" / "opp" $,
    $ cos theta = "adj" / "hyp" $, $ sec theta = "hyp" / "adj" $,
    $ tan theta = "opp" / "adj" $, $ cot theta = "adj" / "opp" $,
  )
)
