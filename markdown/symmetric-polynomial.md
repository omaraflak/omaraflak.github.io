:title: Symmetric Polynomials
:description: Divide the degree of a polynomial by 2!
:year: 2021
:month: 11
:day: 3
:math: true

Can you solve the following equation?

```latex
6x^4 + 5x^3 - 8x^2 + 5x + 6 = 0
```

# Example

It turns out you can use the symmetry of the coefficients to solve this equation. To start off, divide by `$x^2$` then factorize:

```latex
\begin{align*}
&6x^4 + 5x^3 - 8x^2 + 5x + 6 = 0 \\[3ex]
\iff& \dfrac{6x^4 + 5x^3 - 8x^2 + 5x + 6}{x^2} = 0 \\[3ex]
\iff& 6x^2 + 5x - 8 + \frac{5}{x} + \dfrac{6}{x^2} = 0 \\[3ex]
\iff& 6\left(x^2 + \dfrac{1}{x^2}\right) + 5\left(x + \dfrac{1}{x}\right) - 8 = 0
\end{align*}
```

You can now do a change of variable:

```latex
X = x + \frac{1}{x}
```

And luckily:

```latex
\begin{align*}
X^2 &= \left(x + \frac{1}{x}\right)^2 \\[3ex]
&= x^2 + \frac{1}{x^2} + 2
\end{align*}
```

Therefore,

```latex
\begin{align*}
& 6\left(x^2 + \dfrac{1}{x^2}\right) + 5\left(x + \dfrac{1}{x}\right) - 8 = 0 \\[3ex]
\iff& 6(X^2 - 2) + 5X - 8 = 0 \\[3ex]
\iff& 6X^2 + 5X - 20 = 0
\end{align*}
```

We end up with a quadratic equation that we know how to solve. The two solutions will then lead to two other quadratic equations when plugged in the equation `$X=x+\frac{1}{x}$`, which will yield four solutions overall.

> Can we generalize this trick ?

# Generalization

Let's see if this works all the time. We need a polynimal with an even degree, `$2k$`, and symmetrical coefficients, then divide by `$x^k$`:

```latex
\begin{align*}
& a_0x^0 + a_1x^1 + \cdots + a_kx^k + \cdots + a_1x^{2k-1} + a_0x^{2k} = 0 \\[3ex]
\iff& \dfrac{a_0}{x^k} + \dfrac{a_1}{x^{k-1}} + \cdots + a_k + \cdots + a_1x^{k-1} + a_0x^k = 0 \\[3ex]
\iff& a_0\left(x^k + \dfrac{1}{x^k}\right) + a_1\left(x^{k-1} + \dfrac{1}{x^{k-1}}\right) + \cdots + a_{k-1}\left(x + \dfrac{1}{x}\right) + a_k = 0
\end{align*}
```

Now the question is: can we use `$X=x+\frac{1}{x}$` change of variable? Using the binomial formula:

```latex
\begin{align*}
X^k &= \left(x + \dfrac{1}{x} \right)^k \\[3ex]
&= \sum_{i=0}^k {k \choose i} x^{2i-k} \\[3ex]
&= {k \choose 0} \dfrac{1}{x^k} + {k \choose 1} \dfrac{1}{x^{k-2}} + \cdots + {k \choose k-1} x^{k-2} + {k \choose k} x^k \\[3ex]
&= \left(x^k + \dfrac{1}{x^k}\right) + {k \choose 1} \left(\dfrac{1}{x^{k-2}} + x^{k-2}\right) + {k \choose 2} \left(\dfrac{1}{x^{k-4}} + x^{k-4}\right) + \cdots \\[3ex]
&= \left(x^k + \dfrac{1}{x^k}\right) + P(X), \quad deg(P) < k
\end{align*}
```

In conclusion, we can always substitute `$X=x + \frac{1}{x}$` as it will divide the degree of the initial polynomial by 2!
