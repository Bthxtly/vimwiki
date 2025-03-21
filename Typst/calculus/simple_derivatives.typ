#set page(fill: rgb("f2e5bc"))

= The derivative of $f(x)=a^x$
We use the definition of derivatives here
$
  f'(x) &= lim_(h->0) (f(x+h)-f(x)) / h \
  &= lim_(h->0) (a^(x+h)-a^x) / h \
  &= lim_(h->0) (a^x (a^h - 1)) / h \
  &= a^x dot lim_(h->0) (a^h - 1) / h \
  &= a^x dot lim_(h->0) (e^(h ln a) - 1) / h \
$

Then, we apply L'Hôpital's rule to the second part
$
  lim_(h->0) (e^(h ln a) - 1) / h &= lim_(h->0) (e^(h ln a) - 1)' / h' \
  &= lim_(h->0) (ln a dot e^(h ln a)) / 1 \
  &= lim_(h->0) (ln a dot a^h) \
  &= ln a
$

So
$ (a^x)' = a^x dot ln a $

= The derivative of $f(x)=log_a x$
Since this function is the inverse function of $g(x)=a^x$, that is,
$f^(-1)(x)=a^x$
$
  f'(x) &= 1 / ((f^(-1))'(f(x))) \
  &= 1 / ((f^(-1))'(log_a x)) \
  &= 1 / (a^(log_a x) dot ln a) \
  &= 1 / (x dot ln a)
$

So $ (log_a x)' = 1 / (x dot ln a) $
