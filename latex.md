# Introduction

### Part 1: The Basics

###### The minimal document:
```LaTex
\documentclass{article}
\begin{document}
% your content here
\end{document}
```
###### Quotation marks:
```
`text' -> 'text'
``text'' -> "text"
```
###### Special characters:
```
% percent sign
# hash (pound / sharp) sign
& ampersand
$ dollar sign
```
###### `&` is used to mark mathematics in text:

`Let $y = m x + b$ be \ldots`

__(LaTex handles spacing automatically and ignores my spaces)__

###### Use caret `^` for superscript and underscore `_` for subscript:

$y^2 = x_1 + x_2$

###### Use curly braces to group superscript and subscript:

$F_n = F_{n-1} + F_{n-2}$

###### Commands for Greek letters and common notation:

$\mu = A e^{Q/RT}$

$\Omega = \sum_{k=1}^{n} \omega_k$

###### Using `\begin{equation}` and `\end{equation}` do display big equations:

```LaTex
\begin{equation}
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
\end{equation}
```
__(LaTex can't handle blank lines in equation)__
__(Use equation* to unnumbered equations)__

###### Equation is an environment - a context, and a command may produce different output in different context:

```LaTex
We can write
in text, or we can write
$ \Omega = \sum_{k=1}^{n} \omega_k $
in text, or we can write
\begin{equation}
\Omega = \sum_{k=1}^{n} \omega_k
\end{equation}
to display it.
```

###### Load packages with `\usepackage` command:

```LaTex
\usepackage{amsmath}
```

###### `amsmath` defines commands for many common mathematical operators and `\operatorname` for others:
```LaTex
\min_{}{}
\operatorname{}
```

###### Align a sequence of equations at the equals sign with the align* environment:
```LaTex
\begin{align*}
(x+1)^3 &= (x+1)(x+1)(x+1) \\
&= (x+1)(x^2 + 2x + 1) \\
&= x^3 + 3x^2 + 3x + 1
\end{align*}
```
__(An ampersand `&` separates the left column (before the =) from the right column (after the =). 
A double backslash `\\` starts a new line.)__


### Part 2: Structured Documents & More

##### Structured Documents
Use `\title`, `\author` and `\maketitle` for title, abstract environment to make an __Abstract__.
Use `\section` and `subsection` for __Sections__.
Use `\label`, `\ref` (and `\eqref` in amsmath) for __Labels and Cross-References__.

##### Figures and Tables
Use `\includegraphics` to display __Graphics__ (`graphicx` required), and support `\caption` to add caption
Use `tabular` environment to draw __Tables__ (`tabularx` required), 
use `\hline` for horizontal lines (or `\toprule`, `\bottomrule` in `booktabs` package)

### Part 3: Not Just Papers: Presentations & More

##### Presentations with beamer

* 
