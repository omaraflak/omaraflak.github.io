:title: Bézier Curve
:description: Understand the mathematics of Bézier curves.
:year: 2020
:month: 5
:day: 2

Bézier curves are used extensively in computer graphics, often to produce smooth curves. If you have ever used Photoshop you might have stumbled upon that tool called "Anchor" where you can put anchor points and draw some curves with them... These are Bézier curves. Or if you have used vector-based graphic, SVG, these too use Bézier curves. Let's see how it works.

# General Definition

Given `$n+1$` points `$\{P_0, ..., P_n\}$` called the ***control points***, the [Bézier curve](https://en.wikipedia.org/wiki/B%C3%A9zier_curve) traced by these points is defined as:


```latex
\begin{align}
Z(t) = \sum_{i=0}^n B_i^n(t) \cdot P_i, \quad t \in[0, 1]
\end{align}
```

Where `$P_i=\{x_i, y_i\}$`, and `$B_i^n(t)$` is the [Bernstein polynomial](https://en.wikipedia.org/wiki/Bernstein_polynomial):


```latex
B_i^n(t) = {n \choose i} t^i (1-t)^{n-i}, \quad {n \choose i} = \frac{n!}{i! (n-i)!}
```

> Note that `$Z(t)$` is not a number, but a point!

Notice that Bernstein polynomial looks a lot like the `$k^{\text{th}}$` term in Newton's binomial formula:

```latex
(a+b)^n = \sum_{i=0}^n {n \choose i} a^i b^{n-1}
```

For the particular values of `$a=1$` and `$b=t-1$`. It then becomes obvious that:

```latex
\sum_{i=0}^n B_i^n(t) = 1
```

Therefore, you can interpret `$Z(t)$` as a weighted average of the control points. As `$t$` changes, the weighted average `$Z(t)$` smoothly moves from the **first** control point to the **last** control point. Indeed:

```latex
\begin{align*}
Z(0) &= \sum_{i=0}^n B_i^n(0) \cdot P_i \\
&= P_0
\end{align*}
```

That is because:

```latex
B_i^n(0) =
\left\{
\begin{array}{ll}
1 \quad \text{if} \quad i = 0 \\
0 \quad \text{if} \quad i \neq 0
\end{array}
\right.
```

Similarily:

```latex
\begin{align*}
Z(n) &= \sum_{i=0}^n B_i^n(n) \cdot P_i \\
&= P_n
\end{align*}
```

# Quadratic Bézier Curve

The quadratic Bézier curve is how we call the Bézier curve with 3 control points, since the degree of `$Z(t)$` will be 2. Let's calculate the Bézier curve given 3 control points and explore some properties we might find! Remember, `$(1)$` holds for `$n+1$` points, so in our case `$n=2$`.

```latex
\begin{align*}
Z(t) &= \sum_{i=0}^2 B_i^2(t) \cdot P_i \\
&= \sum_{i=0}^2 {2 \choose i} t^i (1 - t)^{2-i} \cdot P_i \\
&= {2 \choose 0} t^0 (1 - t)^{2-0} \cdot P_0 + {2 \choose 1} t^1 (1 - t)^{2-1} \cdot P_1 + {2 \choose 2} t^2 (1 - t)^{2-2} \cdot P_2 \\
&= (1-t)^2 \cdot P_0 + 2t(1-t) \cdot P_1 + t^2 \cdot P_2
\end{align*}
```

Now we just have to choose three control points and evaluate the curve on the range `$[0, 1]$`. We can do this in Python easily.

```python
import numpy as np
import matplotlib.pyplot as plt

P0, P1, P2 = np.array([
	[0, 0],
	[2, 4],
	[5, 3]
])

# define bezier curve
Z = lambda t: (1 - t)**2 * P0 + 2 * t * (1 - t) * P1 + t**2 * P2

# evaluate the curve on [0, 1] sliced in 50 points
points = np.array([Z(t) for t in np.linspace(0, 1, 50)])

# get x and y coordinates of points separately
x, y = points[:,0], points[:,1]

# plot
plt.plot(x, y, 'b-')
plt.plot(*P0, 'r.')
plt.plot(*P1, 'r.')
plt.plot(*P2, 'r.')
plt.show()
```

![bezier](/images/bezier_1.webp;w=80%)

Notice that the curve does indeed start and end at the first and last control points. Because of that, if you fix `$P_0$` and `$P_2$`, the `$P1$` entirely determines the shape of the curve. Moving `$P1$` around you might notice something:

![bezier different P1](/images/bezier_2.webp;w=100%)

The Bézier curve is always contained in the polygon formed by the control points. This polygon is hence called the control polygon, or Bézier polygon. This property also holds for any number of control points, which makes their manipulation quite intuitive when using a software.

![bezier curve is contained in convex hull](/images/bezier_3.webp;w=100%)

## Matrix Representation

We can actually represent the Bézier formula using matrix multiplication, which might be useful in other contexts, for instance for splitting the Bézier curve. If we go back to our example we can rewrite `$Z(t)$` as follows:

```latex
\begin{align*}
Z(t) &= (1-t)^2 \cdot P_0 + 2t(1-t) \cdot P_1 + t^2 \cdot P_2 \\
&= (1-2t+t^2) \cdot P_0 + (2t-2t^2) \cdot P_1 + t^2 \cdot P_2 \\
&= \begin{bmatrix} (1-2t+t^2) & (2t-2t^2) & t^2 \end{bmatrix} \cdot \begin{bmatrix} P_0 \\ P_1 \\ P_2 \end{bmatrix}  \\
&= \begin{bmatrix} 1 & t & t^2 \end{bmatrix} \cdot \begin{bmatrix} 1 & 0 & 0 \\ -2 & 2 & 0 \\ 1 & -2 & 1 \end{bmatrix} \cdot \begin{bmatrix} P_0 \\ P_1 \\ P_2 \end{bmatrix}  \\
&= T \cdot M \cdot P
\end{align*}
```

All the information of the quadratic Bézier curve is now compacted into one matrix, `$M$`. Notice the `$i^{\text{th}}$` column of `$M$` is just the coefficients of the polynomial `$B_i^n$`. However, if we want to program this, it will be easier to create a matrix row by row, instead of column by column. Luckily, because `${n \choose i} = {n \choose n-i}$`, the `$i^{\text{th}}$` row of the matrix is just the reversed `$(n-i)^{\text{th}}$` column.

```latex
\begin{align*}
Z(t) &= {n \choose n-i} t^{n-i} (1 - t)^{n-(n-i)} \\
&= {n \choose i} t^{n-i} (1 - t)^i \\
&= {n \choose i} t^{n-i} \sum_{k=0}^i {i \choose k} 1^k (-t)^{i-k} \\
&= {n \choose i} t^{n-i} \sum_{k=0}^i {i \choose k} (-1)^{i-k} t^{i-k} \\
&= \sum_{k=0}^i {n \choose i} {i \choose k} (-1)^{i-k} t^{n-k}
\end{align*}
```

Therefore, the coefficients of the matrix are nothing but the coefficients of `$t$`:

```latex
{n \choose i} {i \choose k} (-1)^{i-k}, \quad \left\{
\begin{array}{ll}
i = 0, ..., n \\
k = 0, ..., i
\end{array}
\right.
```

```python
from math import comb

def get_bezier_matrix(n: int) -> list[list[float]]:
    coef = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        for k in range(i + 1):
            coef[i][k] = comb(n, i) * comb(i, k) * (-1)**(i - k)
    return coef
```

---

Lastly, this is a general version of the polynomial version:

```python
import numpy as np
import matplotlib.pyplot as plt
from math import comb

def get_bezier_curve(points):
    n = len(points) - 1
    return lambda t: sum(
        comb(n, i) * t**i * (1 - t)**(n - i) * points[i]
        for i in range(n + 1)
    )

def evaluate_bezier(points, total):
    bezier = get_bezier_curve(points)
    new_points = np.array([bezier(t) for t in np.linspace(0, 1, total)])
    return new_points[:,0], new_points[:,1]

points = np.array([
    [0, 0],
    [-1, 3],
    [4, 3],
    [6, 0],
    [7, 2.5]
])

x, y = points[:,0], points[:,1]
bx, by = evaluate_bezier(points, 50)
plt.plot(bx, by, 'b-')
plt.plot(x, y, 'r.')
plt.show()
```