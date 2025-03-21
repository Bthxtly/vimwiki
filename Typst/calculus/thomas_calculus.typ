#import "@preview/cetz:0.3.4"

// https://stackoverflow.com/questions/78272599/show-current-heading-number-and-body-in-page-header
#set page(
  header: context {
    let selector = selector(heading).before(here())
    let level = counter(selector)
    let headings = query(selector)

    if headings.len() == 0 {
      return
    }

    let heading = headings.last()

    level.display(heading.numbering)
    h(1em)
    heading.body
  },
  fill: rgb("f2e5bc"),
)

#set heading(numbering: "1.")

#show heading.where(level: 2): it => text(
  size: 11pt,
  weight: "bold",
  style: "italic",
  line(length: 100%) + it.body + [.\ ],
)

#show "Proof": name => [
  #text("Proof", weight: "bold", font: "FreeSans")
  #h(10pt)
]

#align(
  center,
  text(size: 17pt, font: "Nimbus Roman")[*Thomas' Calculus*],
)

= Preliminaries
This chapter is too easy, but still worth a figure drawn with `CeTZ`:
// trigonometric functions
#grid(
  columns: 2,
  gutter: 10pt,
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
    gutter: 10pt,
    $
      bold("sine: ") & sin theta = "opp" / "hyp"\
      bold("cosine: ") & cos theta = "adj" / "hyp"\
      bold("tangent: ") & sin theta = "opp" / "adj"
    $,
    $
      bold("cosecant: ") & csc theta = "hyp" / "opp"\
      bold("secant: ") & sec theta = "hyp" / "adj"\
      bold("cotangent: ") & cot theta = "adj" / "opp"
    $,
  ),
)

= Limits and Continuity

== Limits of Function Values
Let $f(x)$ be defined on an open interval about $x_0$, _except possibly at $x_0$
itself_. If $f(x)$ gets arbitrarily close to $L$ (as close to $L$ as we like)
for all $x$ sufficiently close to $x_0$, we say that $f$ approaches the *limit*
$L$ as x approaches $x_0$, and we write $ lim_(x arrow x_0)f(x) = L $

== Definition of Limit
Let $f(x)$ be defined on an open interval about $c$, except possibly at $c$
itself. We say that the *limit of $f(x)$ as $x$ approaches $c$ is the number
$L$*, and write
$ lim_(x arrow c)f(x) = L, $
if, for every number $epsilon$ > 0,
there exist a corresponding number $delta$ > 0 such that for all $x$,
$ 0 < |x - c| < delta #h(20pt) => #h(20pt) |f(x) - L| < epsilon. $

== Definition of Limits involving Infinity
1. We say that $f(x)$ has the *limit $L$ as $x$ approaches Infinity* and write
$ lim_(x arrow infinity)f(x) = L $
if, for every number $epsilon$ > 0, there exists a corresponding number $M$
such that for all $x$,
$ x > M #h(20pt) => #h(20pt) |f(x) - L| < epsilon. $
2. We say that $f(x)$ has the *limit L as $x$ approaches minus infinity* and write
$ lim_(x arrow minus infinity)f(x) = L $
if, for every number $epsilon$ > 0, there exists a corresponding number $N$
such that for all $x$,
$ x < N #h(20pt) => #h(20pt) |f(x) - L| < epsilon. $

== Limits Involving $(sin theta)$/$theta$
$ lim_(x arrow 0)(sin theta)/theta = 1 #h(20pt) (theta "in radians") $
Proof Consider @lim_sin_theta_div_theta. Notice that
$ "area" triangle "OAP" < "area" "sector" "OAP" < "area" triangle "OAP". $
Then express these areas in terms of $theta$, and thus,
$ 1 / 2 sin theta < 1 / 2 theta < 1 / 2 tan theta. $
So
$ 1 > (sin theta) / theta > cos theta. $
Since $lim_(theta arrow 0^plus)cos theta = 1$, the Sandwich Theorem gives
$ lim_(theta arrow 0^plus)(sin theta) / theta = 1. $
Because $(sin theta)/theta$ is an even function, so
$
  lim_(theta arrow 0^plus)(sin theta) / theta =
  lim_(theta arrow 0^minus)(sin theta) / theta = 1.
$
So $lim_(x arrow 0)(sin theta)/theta = 1$
#figure(
  caption: [
    The proof of $lim_(theta arrow 0)(sin theta)/theta = 1$
  ],
  cetz.canvas({
    import cetz.draw: *
    set-style(stroke: 0.4pt)
    scale(4)
    // x, y axes
    line(
      (-0.1, 0),
      (1.2, 0),
      mark: (end: "straight", length: 0.05, width: 0.05),
      name: "x_axis",
    )
    line(
      (0, -0.1),
      (0, 1.2),
      mark: (end: "straight", length: 0.05, width: 0.05),
      name: "y_axis",
    )
    // arcs and the slope line
    arc((1, 0), start: 0deg, stop: 90deg)
    let degree = 45deg
    let len = 0.707
    let corner_len = 0.05
    let arc_len = 0.2
    line((0, 0), (1, 1), name: "slope")
    arc((arc_len, 0), start: 0deg, stop: degree, radius: arc_len, name: "arc")
    // lines
    line((len, len), (1, 0))
    line((0, 0), (len, 0), name: "cos", stroke: red + 1.2pt)
    line((len, 0), (len, len), name: "sin", stroke: blue + 1.2pt)
    line((1, 0), (1, 1), name: "tan", stroke: yellow + 1.2pt)
    line((len - corner_len, 0), (rel: (0, corner_len)), (rel: (corner_len, 0)))
    line((1 + corner_len, 0), (rel: (0, corner_len)), (rel: (-corner_len, 0)))
    // contents
    content((0, 0), "O", padding: 0.2, anchor: "north-east", name: "O")
    content((len, len), "P", padding: 0.2, anchor: "south", name: "P")
    content((1, 1), "T", padding: 0.2, anchor: "south", name: "T")
    content((len, 0), "Q", padding: 0.2, anchor: "north", name: "Q")
    content((1, 0), "A(1, 0)", padding: 0.2, anchor: "north", name: "A")
    content((0, 1), "1", padding: 0.2, anchor: "east")
    content("x_axis.end", [$x$], padding: 0.1, anchor: "west")
    content("y_axis.end", [$y$], padding: 0.1, anchor: "south")
    content(("O", 50%, "P"), "1", padding: 0.2, anchor: "south")
    content("sin", [$sin theta$], padding: 0.1, anchor: "east")
    content("cos", [$cos theta$], padding: 0.1, anchor: "south")
    content("tan", [$tan theta$], padding: 0.1, anchor: "west")
    content(
      ("arc.start", 80%, "arc.end"),
      [$theta$],
      padding: 0.2,
      anchor: "west",
    )
  }),
) <lim_sin_theta_div_theta>

== Definition of Continuity
Let $c$ be a real number on the $x$-axis.\
The function is *continuous at $c$* if $ lim_(x arrow c)f(x) = f(c). $
The function is *right-continuous at $c$ (or continuous from the right)* if
$ lim_(x arrow c^plus)f(x) = f(c). $
The function is *left-continuous at $c$ (or continuous from the left)* if
$ lim_(x arrow c^minus)f(x) = f(c). $

== Continuity Test
A function $f(x)$ is continuous at a point $x=c$ if and only if it meets the
following three conditions.
#grid(
  columns: 2,
  gutter: 40pt,
  [
    + $f(c)$ exists
    + $lim_(x arrow c)f(x)$ exists
    + $lim_(x arrow c)f(x)=f(c)$
  ],
  [
    ($c$ lies in the domain of $f$).\
    ($f$ has a limit as $x arrow c$).\
    (the limit equals the function value).\
  ],
)

== Some kinds of discontinuities
#grid(
  columns: 2,
  gutter: 10pt,
  [
    - removable discontinuity
    - jump discontinuity
    - infinite discontinuity
    - oscillating discontinuity
  ],
  [
    ($x^2/x$ at $0$)\
    ($floor.l x floor.r$ at $1$)\
    ($1/x^2$ at $0$)\
    ($sin 1/x$ at $0$\)
  ],
)

= Derivatives

== Definition of the derivative of functions
The *derivative* of the function $f(x)$ with respect to the variable $x$ is the
function $f'$ whose value at $x$ is
$ f'(x) = lim_(h arrow 0)(f(x+h) - f(x)) / h $
or, alternatively
$ f'(x) = lim_(z arrow x)(f(z) - f(x)) / (z - x) $
provided the limit exists.

== The derivatives of some trigonometric functions
- $d / (d x) (tan x) = sec^2 x$\
- $d / (d x) (cot x) = -csc^2 x$\
- $d / (d x) (sec x) = sec x tan x$\
- $d / (d x) (csc x) = -csc x cot x$,

== The Chain Rule
If $f(u)$ is differentiable at the point $u=g(x)$ and $g(x)$ is differentiable
at $x$, then the composite function $(f circle.stroked.small g)(x) = f(g(x))$ is
differentiable at $x$, and
$ (f circle.small g)'(x) = f'(g(x)) dot g'(x). $
In Leibniz's notation, if $y=f(u)$ and $u = g(x)$, then
$ (d y) / (d x) = (d y) / (d u) dot (d u) / (d x), $
where $(d y) / (d u)$ is evaluated at $u = g(x)$.

== Implicit Differentiation
1. #[Differentiate both sides of the equation with respect to $x$, treating $y$
    as a differentiable function of $x$.]
2. #[
    Collect the terms with $(d y) / (d x)$ on one side of the equation and
    solve for $(d y) / (d x)$
  ]

== The Derivative Rule for Inverses
If $f$ has an interval $I$ as domain and $f'(x)$ exists and is never zero
on $I$, the $f^(-1)$ is differentiable at every point in its domain. The value of
$(f^(-1))'$ at a point $b$ in the domain of $f^(-1)$ is the reciprocal of the
value of $f'$ at the point $a=f^(-1)(b)$:
$ (f^(-1))'(b) = 1 / (f'(f^(-1)(b))) $
or
$
  lr((d f^(-1))/(d x)|)_(x=b) = display(1/display(lr((d f)/(d x)|)))_(x=f^(-1)(b)).
$
