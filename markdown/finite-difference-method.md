:title: Finite Difference Method
:description: How to solve a non-linear differential equation numerically using the finite difference method.
:year: 2021
:month: 2
:day: 1


In this article we will see how to use the finite difference method to solve non-linear differential equations numerically. We will practice on the pendulum equation, taking air resistance into account, and solve it in Python.

We will find the differential equation of the pendulum starting from scratch, and then solve it. Before we start, we need a little background on Polar coordinates.

# Polar Coordinates

You already know the famous Cartesian coordinates (x, y, z coordinates), which are probably the most used in everyday life. However, in some cases, describing the position of an object in Cartesian coordinates isn't practical. For instance, when an object is in a **circular movement**, sine and cosine functions are going to pop all over the place, so it's generally a much better idea to describe that object's position in what we call **Polar coordinates**.

![polar coordinates](/images/polar.webp;w=80%)

Polar coordinates are described by two variables, the radius `$\rho$` and the angle `$\theta$`. We attach unit vectors to each variable:

- `$\vec{e_{\rho}}$` is a unit vector always pointing in the same direction as vector `$\vec{OM}$`.
- `$\vec{e_{\theta}}$` is a unit vector perpendicular to `$\vec{e_{\rho}}$`.

Our goal now is to express the ***position***, ***velocity***, and ***acceleration*** of an object in Polar coordinates. For this we need to express the relationship between the Polar unit vectors and the Cartesian unit vectors.

![polar cartesian conversion](/images/polar_cartesian.webp;w=50%)

Cartesian to Polar:

```latex
\begin{align*}
&\vec{e_{\rho}} = \cos(\theta) \vec{e_x} + \sin(\theta) \vec{e_y} \\
&\vec{e_{\theta}} = -\sin(\theta) \vec{e_x} + \cos(\theta) \vec{e_y}
\end{align*}
```

Polar to Cartesian:

```latex
\begin{align*}
&\vec{e_x} = \cos(\theta) \vec{e_{\rho}} - \sin(\theta) \vec{e_{\theta}} \\
&\vec{e_y} = \sin(\theta) \vec{e_{\rho}} + \cos(\theta) \vec{e_{\theta}}
\end{align*}
```

Good! Now let's express position, velocity, and acceleration in Polar coordinates.

## Position

This one is simple, it's the whole point of using Polar coordinates!

```latex
\overrightarrow{OM} = \rho \vec{e_{\rho}}
```

## Velocity

We simply differentiate the position with respect to time. We will assume `$\rho$` is a constant, and only `$\theta$` varies over time.

```latex
\begin{align*}
\frac{d\overrightarrow{OM}}{dt} &= \rho \frac{d\vec{e_{\rho}}}{dt} \\
&= \rho \frac{d\vec{e_{\rho}}}{d\theta} \frac{d\theta}{dt} \\
&= \rho (-\sin(\theta) \vec{e_x} + \cos(\theta) \vec{e_y}) \dot{\theta} \\
&= \rho \dot{\theta} \vec{e_{\theta}}
\end{align*}
```

## Acceleration

We differentiate the velocity with respect to time.

```latex
\begin{align*}
\frac{d^2\overrightarrow{OM}}{dt^2} &= \rho \frac{d\dot{\theta} \vec{e_{\theta}}}{dt} \\
&= \rho \left( \frac{d\dot{\theta}}{dt} \vec{e_{\theta}} + \dot{\theta} \frac{d\vec{e_{\theta}}}{dt} \right) \\
&= \rho \left( \ddot{\theta} \vec{e_{\theta}} + \dot{\theta} \frac{d\vec{e_{\theta}}}{d\theta} \frac{d\theta}{dt} \right) \\
&= \rho \left( \ddot{\theta} \vec{e_{\theta}} - \dot{\theta}^2 \vec{e_{\rho}} \right) \\
&= -\rho \dot{\theta}^2 \vec{e_{\rho}} + \rho \ddot{\theta} \vec{e_{\theta}}
\end{align*}
```

Done! We can now work on our problem: the pendulum.

# Pendulum Equation

![pendulum](/images/pendulum.webp;w=50%)

To find the equation that angle `$\theta$` satisfies, we will use Newton's second law of motion, or as we call it in French, the *fundamental principle of dynamic*.

```latex
\sum{\overrightarrow{F_{\rightarrow \text{system}}}} = m \vec{a}
```

The sum of all the forces applied to a system is equal to its mass times its acceleration. Let's enumerate all the forces applied to the pendulum and express them in Polar coordinates.

## Weight

The weight of the object due to gravity is one of the forces applied to the object. Its formula is well known, mass times gravity, and will be expressed in our coordinate system as:

```latex
\begin{align*}
\vec{P} &= mg\vec{e_x} \\
&= mg \cos(\theta) \vec{e_{\rho}} - mg \sin(\theta) \vec{e_{\theta}}
\end{align*}
```

Where `$m$` (kg) is the mass of the object, and `$g$` (m/s²) is value of the acceleration of gravity — which is about 9.81 on Earth.

## Rope Tension

The rope exerts a tension pulling the pendulum in the direction of the rope's fixed end.

```latex
\vec{R} = -R \vec{e_{\rho}}
```

Where `$R$` (N) is the rope tension in Newtons.

## Air Resistance

Lastly, the air exerts a friction on the pendulum as it swings, which will make it stop oscillating at some point. Small air resistance is usually modeled as a force opposite to the velocity vector and proportional to the norm of the velocity vector.

```latex
\begin{align*}
\vec{f} &= -k \vec{v} \\
&= -kL \dot{\theta} \vec{e_{\theta}}
\end{align*}
```

Where `$k$` (kg/s) is the friction coefficient that is specific to the object in movement, and `$L$` (m) is the length of the pendulum rope.

> Note: If something is rotating at angular speed `$\omega$` (rad/s) around an axis at a distance `$r$` (m), then the magnitude of the object's velocity is `$r\omega$` (m/s). For example, the speed of the tip of a fan's blade, or a pendulum (which is why we multiply by `$L$`).


## Newton's second law of motion

We can now apply Newton's second law of motion:

```latex
\begin{align*}
\vec{P} + \vec{R} + \vec{f} &= m \vec{a} \\
\iff mg \cos(\theta) \vec{e_{\rho}} - mg \sin(\theta) \vec{e_{\theta}} -R \vec{e_{\rho}} -kL \dot{\theta} \vec{e_{\theta}} &= -mL\dot{\theta}^2 \vec{e_{\rho}} + mL\ddot{\theta} \vec{e_{\theta}}
\end{align*}
```

Then project the result on both axes independently:

```latex
\begin{align}
mg \cos(\theta) - R = -mL\dot{\theta}^2 \\
- mg \sin(\theta) -kL \dot{\theta} = mL\ddot{\theta}
\end{align}
```

Reordering the terms of `$(2)$`, we get:

```latex
\ddot{\theta} + \frac{k}{m} \dot{\theta} + \frac{g}{L} \sin(\theta) = 0
```

Solving this second order non-linear differential equation is *complicated*. This is where the **Finite Difference Method** comes very handy. It will boil down to two lines of Python! Let's see how.

# Finite Difference Method

The method consists of approximating derivatives numerically using a rate of change with a very small step size.

```latex
f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
```

That is the very definition of what a derivative is. Numerically, if we knew `$f$`, we could take a small number `$h$` — e.g. 0.0001 — and compute the above formula for a given `$x$`, which would give us an approximation of `$f'(x)$`.

The finite difference method simply uses that fact to transform differential equations into ordinary equations.

In our case, we start by expressing `$\ddot{\theta}$` with respect to `$\dot{\theta}$` using the rate of change.

```latex
\ddot{\theta}(t) = \frac{\dot{\theta}(t+dt) - \dot{\theta}(t)}{dt}
```

I removed the limit, and wrote `$dt$` to signal this is an infinitesimal value — in practice, just a very small number. We will now plug this equation into the pendulum equation `$(2)$`.

```latex
\begin{align*}
&\ddot{\theta}(t) + \frac{k}{m} \dot{\theta}(t) + \frac{g}{L} \sin(\theta(t)) = 0 \\
\iff & \frac{\dot{\theta}(t+dt) - \dot{\theta}(t)}{dt} + \frac{k}{m} \dot{\theta}(t) + \frac{g}{L} \sin(\theta(t)) = 0 \\
\iff & \dot{\theta}(t+dt) - \dot{\theta}(t) + dt \frac{k}{m} \dot{\theta}(t) + dt \frac{g}{L} \sin(\theta(t)) = 0 \\
\iff & \dot{\theta}(t+dt) = \dot{\theta}(t) - dt \frac{k}{m} \dot{\theta}(t) - dt \frac{g}{L} \sin(\theta(t))
\end{align*}
```

Okay! We managed to express the angular velocity at time `$t+dt$` with respect to the angle and angular velocity at time `$t$`. In other words, if for instance `$dt=0.001$` and if you know `$\theta(0)$` and `$\dot{\theta}(0)$` (which are the initial conditions of the system), then you can compute `$\dot{\theta}(0.001)$`! If we could also compute `$\theta(0.001)$` then the recursion is complete and we can compute `$\{\theta(t), \dot{\theta}(t)\}$` for any `$t$` starting with known initial conditions.

Fortunately, there is a way to compute `$\theta(t+dt)$`:

```latex
\begin{align*}
&\dot{\theta}(t) = \frac{\theta(t+dt) - \theta(t)}{dt} \\
\iff & \theta(t+dt) = dt \dot{\theta}(t) + \theta(t)
\end{align*}
```

This is again the definition of the derivative, applied to `$\dot{\theta}(t)$`! With that equation in hand we can also compute the angle at time `$t+dt$` given the angle and the angular velocity at time `$t$`.

Using these two equations we can now compute the angle `$\theta$` at any time step!

```latex
\left\{
\begin{array}{ll}
\dot{\theta}(t+dt) = \dot{\theta}(t) - dt \frac{k}{m} \dot{\theta}(t) - dt \frac{g}{L} \sin(\theta(t)) \\
\theta(t+dt) = dt \dot{\theta}(t) + \theta(t)
\end{array}
\right.
```

Given `$\{\theta(0), \dot{\theta}(0)\}$` you can compute `$\{\theta(dt), \dot{\theta}(dt)\}$`. Given `$\{\theta(dt), \dot{\theta}(dt)\}$` you can compute `$\{\theta(2dt), \dot{\theta}(2dt)\}$`, and so on.

# Python Simulation

```python
import numpy as np
import matplotlib.pyplot as plt

N = 100         # in how many sub pieces we should break a 1 second interval
T = 15          # total duration of the simulation in seconds
dt = 1 / N      # dt
g = 9.81        # acceleration of gravity
L = 1           # pendulum rope length
k = 0.8         # air resistance coefficient
m = 1           # mass of the pendulum

theta = [np.pi / 2]     # initial angle
theta_dot = [0]         # initial angular velocity
t = [0]                 # initial time

for i in range(N * T):
    theta_dot.append(theta_dot[-1] - theta_dot[-1] * dt * k / m - np.sin(theta[-1]) * dt * g / L)
    theta.append(theta_dot[-1] * dt + theta[-1])
    t.append((i + 1) * dt)

plt.plot(t, theta, label='theta')
plt.plot(t, theta_dot, label='theta dot')
plt.legend()
plt.show()
```

We iteratively compute `$\theta(t)$` and `$\dot{\theta}(t)$` using the formulas we found, and put the results in two separate lists. Running the code produces the following plot.

![pendulum result](/images/pendulum_result.webp;w=100%)

Two happy observations:

- The angular velocity seems to reach extremums when the angle is zero, which makes sense since this is where the pendulum has accumulated all its inertia and is about to slow down because it's going up.
- The angular velocity seems to reach zero when the angle reaches an extremum, which makes sense since this is when the pendulum is slowing down and is about to go in the other direction.

Playing with the code a little, you might want to set the initial velocity to `$2\pi$` for instance.

![pendulum full rotation](/images/pendulum_result_2.webp;w=100%)

Notice how the angle keeps increasing before going down. What happened is that the initial velocity was high enough to make the pendulum make a full spin before entering the oscillation!

You can try to increase `$dt$` and see how this affects the simulation. We would expect a smaller `$dt$` to give more accurate results (since that controls the approximation of the derivative). Let's see what happens for `N=3,2,1`.

![pendulum different dt](/images/pendulum_result_3.webp;w=100%)

I was actually surprised to see that for only 3 points per second (and even 2), we still manage to get the general shape of the solution. `N=1` is another story...