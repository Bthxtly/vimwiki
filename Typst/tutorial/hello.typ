= Title
Hello, world!

== Subheading
This is a new paragraph.
+ number list1
  - bulleted list1
  - bulleted list2
+ number list2
+ number list3

== Figure
PNG, JPEG, GIF and SVG are supported.
#image("image/typst.png", width: 10%)

We can make it fancy with the figure function, and refer to the figure with
lable is fine, like @logo
#figure(
  image("image/typst.png", width: 40%),
  caption: [
    the Typst logo
  ],
) <logo>

// == Bibliography
// #bibliography("something.bib")

== Maths
Wrapping equations in \$ signs to let Typst know it should expect a mathematical
expression: $S = pi r^2$

That equation is typeset inline. To have it on its own line instead, simply
insert a single space at its start and end:
$ Q = rho A v + C $

A variable consists of multiple letters is can be included with quotes:
$ Q = rho A v + "time offset" $

Use the `sum` symbol to express a sum formula, and `_` and `^` for subscript and
superscript resepectively:
$ sum_(i=1)^(n) i^2 = ((2n+1) (n+1) n) / 6 $

Mostly, we use functions for math constructs instead of special syntax. For
example, to insert a column vector, we can use the `vec` function. Within math
mode(double `$`), functions calls don't need to start with the `#` character.
$ v := vec(x_1, x_2, x_3) $

Since many symbols hase a lot of varianets, we can select among these varianets
by appending a dot and a modifier name to a symbol's name:
$ a arrow.squiggly b $
