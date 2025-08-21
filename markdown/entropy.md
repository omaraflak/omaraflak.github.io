:title: Information & Entropy
:description: What is information and how is it measured? What is entropy? Cross entropy? Relative entropy (aka KL Divergence)?
:year: 2025
:month: 2
:day: 21
:pinned: true
:math: true

# Information

Information is tied to the field of **probabilities**, and it can be seen as a measure of **uncertainty** or **surprise**. To avoid extrapolation and misuse of this concept, you need to remember that it only makes sense to talk about information (in the mathematical sense) when you are studying a **probabilistic event**.

> Information relates to probabilities in that the realization of an event with low probability brings a lot of information, and the realization of an event with high probability brings little information.

So the information gained by knowing an event has realized relates to probability of the event realization. Therefore it has to be a function of the form `$I(p)$`, but what is it ***exactly***?

Let's explore the properties we would like such a mapping to have:

1. Low probability `$\implies$` high information
2. High probability `$\implies$` low information
3. `$p=1 \implies I=0$` (if an event is certain to be realized, then knowing about it doesn't bring about any information)
4. `$ p \to 0 \implies I \to \inf$` (the opposite of 3 must be true)
5. Information should be additive for independent events, i.e. learning about two independent events should give you the amount of information equal to the sum of the information gained from each event separately:

```latex
p(E_1 \cap E_2) = p(E_1) * p(E_2) \implies I(p(E_1 \cap E_2)) = I(p(E_1)) + I(p(E_2))
```

If we need this mapping function to be continuous, which we do since probabilities themselves are continuous and that information should not *jump* suddenly, then there's only one family of functions that meets those requirements: ***logarithms***.

More precisely, the negative logarithms:

<div class="article-center-row"><div id="negative-log"></div></div>

We define information mathematically as:

```latex
I(x) = -log(p(x)) \\
\text{or} \\
I(p) = -log(p)
```

*I might use either notation depending on the context to make the equations lighter.*

We said ***the family of functions*** — indeed, logarithms of *all* bases meet the requirements listed above. Any base is valid, the difference will be in the **unit** of the information:

- `$log_2(x)$` will give ***bits***
- `$log_{10}(x)$` will give ***dits***
- `$log_e(x)$` will give ***nats***

All of those are valid ways of expressing information. In practice, we often use the base 2 logarithm.

> **Bit**: represents the amount of information content gained with a binary choice.

## Example 1

I flip a fair coin `$p(\text{heads}) = p(\text{tails}) = \frac{1}{2}$` and tell you the result. I have just given you: `$-log_2(\frac{1}{2}) = log_2(2) = 1$` **bit** of information! In other words, I have given you the information content gained with ***1 binary choice***, i.e. one *yes/no* question.

Recall that `$log(\frac{1}{x}) = -log(x)$`.

> Logarithm in base 2 answers the question: "how many times do I have to divide x by 2 to get 1 (or less) ?". In other words, how many **binary choices** do I have to make on my input space to be left with 1 element (or less). Each of these binary choices (divisions) represent one bit of information.

## Example 2

I have to pick one fruit amongst 8 different fruits (assume each is equally likely to be picked). I pick one and tell you which: I have just given you `$-log_2(\frac{1}{8}) = log_2(8) = 3$` **bits** of information. In other words, I have given you the information content gained with ***3 binary choices*** (divide 8 by two 3 times).

> I could have measured information in *dits* instead. It is equally correct to say that I would have given you `$-log_{10}(\frac{1}{8}) = log_{10}(8) = 0.9$` **dits** of information.
>
> `$3 \text{ bits} = 0.9 \text{ dits}$`

# Entropy

In the previous examples, you'll notice that I used **uniform probability distributions**. The probability of each outcome was equally likely (`$p=\frac{1}{2}$` for the coin toss, and `$p=\frac{1}{8}$` for the fruit pick). Then I asked:

> What is the information gained for observing one of those events?

Since the probability was the same for all events, then the answer to that question would be the **same regardless of the outcome** of the random experiment.

> What if each outcome had a different probability of realization?

What if I had to pick between 3 fruits, each with a different probability according to my preferences:

- **M**ango `$p=0.7$`
- **A**pples `$p=0.2$`
- **O**range `$p=0.1$`

A natural question is: ***on average***, what is the information gained for observing an event from that random experiment? We are asking the same question as before, but of course since each outcome has a different probability, and since the information depends on the probability, the result will change for different outcomes. Therefore we ask about the ***average*** outcome.

One way is to sum the information gained by each event ***weighted*** by the probability of realization.

```latex
\begin{align*}
\mathbb{E}[I] &= p(M) * I(M) + p(A) * I(A) + p(O) * I(O) \\
&= -p(M)*log(p(M)) -p(A)*log(p(A)) -p(O)*log(p(O)) \\
&= -0.7*log(0.7) -0.2*log(0.2) -0.1*log(0.1) \\
&= 0.35
\end{align*}
```

> That is exactly what **entropy** is!

We call entropy the **expected amount of information** gained for observing an event from a random variable. In other words, this answers the question: "If I sample an event from a variable `$X$`; On average, what is the information gained for observing one of `$x_1$`, `$x_2$`, ..., or `$x_n$` given the probability distribution of those events?".

We usually denote the entropy of a random variable `$X$` as `$H(X)$`:

```latex
\begin{align*}
H(X) &= \sum_x p(x) * I(x) \\
&= - \sum_x p(x) * log(p(x))
\end{align*}
```

> An interesting follow up question is: when is the entropy minimal/maximal ?

We can try to intuitively answer. Give it a thought!

## Minimal Entropy

Since entropy is the expected information to be gained from observing a random variable, and since information is minimal when events are certain to be realized, the absolute minimum would be reached if a random variable could be predictable every time, i.e. if it had an event with probability `$p=1$` and the rest `$p=0$` (in which case `$H(X)=0$`). Any other probability distribution would yield some amount of information.

## Maximum Entropy

Entropy is maximized if the average information is maximal. We know information is highest for most improbable events (`$p \to 0$`). If we have multiple events, each with a certain probability, and we want those probabilities to be as **low** as possible, then the lowest we can go on average is when we spread the probability space over all events equally, that is `$p=\frac{1}{n}$` with `$n$` the number of events. In other words: a ***uniform probability distribution***.

> You can see the uniform distribution as the most ***"unpredictable"*** — the one for which each event brings the maximum amount of information content upon realization.

---

I highly advise checking out 3B1B video on how to solve the game Wordle using the concept of entropy.

[](https://www.youtube.com/watch?v=v68zYyaEmEA)

---

There's also another way to interpret entropy, and it's going to be useful for the rest of the article, so before going further with *Cross Entropy* and *Relative Entropy*, we're making a little stop at ***encoders***.

# Encoders

An encoder is a machine/routine/code that assigns a code to each event of a probability distribution (let's say in bits, but we could use another base).

An encoder is **optimal**, if on *average*, it uses the theoretical ***minimum number of bits*** possible to represent an event drawn from the distribution.

## Example 1

Say we have three events `$\{A,B,C\}$`, with `$p(A)=p(B)=p(C)=\frac{1}{3}$`.

We could create a coding (a mapping) that uses 2 bits to encode each outcome:

- `$A \coloneqq 00$`
- `$B \coloneqq 01$`
- `$C \coloneqq 10$`

If I then give you a list of bits, e.g. `011000`, you are able to decode it (by splitting every 2 bits and using the mapping above): `011000` → `BCA`. This works out fine, but we are waisting the `11` state of our 2 bits, which accounts for 25% of all possible states! This is not very optimal.

> What if we assigned less bits to some events ?

## Example 2

Consider the following encoder:

- `$A \coloneqq 0$`
- `$B \coloneqq 10$`
- `$C \coloneqq 11$`

Here, we use a total of **5 bits** to encode **3 states** (instead of 6 bits in the previous coding), that is `$\frac{5}{3} = 1.7$` ***bits*** on average, which is less than 2 bits like previously.

With this new encoder, suppose we read the first 2 bits of a message `$b_1, b_2$`:

- `$b_1 = 0 \implies A$`
- `$b_1 = 1, b_2 = 0 \implies B$`
- `$b_1 = 1, b_2 = 1 \implies C$`

And we can keep reading and decoding a long string of bits that way.

> Why not use even less bits?

## Example 3 ❌

Consider this final encoder:

- `$A \coloneqq 0$`
- `$B \coloneqq 1$`
- `$C \coloneqq 00$`

This uses less bits than the previous too, but it is also **ambiguous**!

The bit string `$00$` could be either `$AA$` or `$C$`, and there's no way to go around this.

> An encoder must be unambiguous, i.e. decodable in a single way.

## Encoders & Entropy

How does that relate to entropy?

Think about the optimal encoder: that will be the encoder that assigns, ***on average***, the ***least amount of bits*** possible to an event of your distribution.

In example 2 above, we considered `$\{A,B,C\}$` to be equally likely; but what if `$C$` was more probable than `$A$` and `$B$`? Wouldn't it be better then to assign the ***single bit*** to `$C$` and two bits to `$A$` and `$B$`?

> To achieve optimality, we need to assign less bits to more probable outcomes, and more bits to less probable outcomes.

A natural question is then:

> What is the minimum number of bits we can use to encode events drawn from a given probability distribution?

The answer is... **entropy**!

[](https://en.wikipedia.org/wiki/Shannon%27s_source_coding_theorem)

To clarify: the entropy is the **theoretical minimum**, but in practice you may not come up with an encoder that uses `$H(X)$` number of bits on average.

Now that we're equipped with this new insight, let's tackle the next concepts!

# Cross Entropy

Let's say I have a machine that produces random letters (a-z) according to a certain unknown probability distribution `$P = \{p(a), p(b), ..., p(z)\}$`.

Your task is to create an optimal encoder for `$P$`, i.e. an encoder that uses, on average, the least amount of bits possible to encode events from this distribution.

We know from earlier that the optimal encoder uses, on average, a number of bits equal to the entropy of the distribution `$H(P)$`. But for this you need to know the exact distribution, and here you don't!

Therefore, you will have to ***guess*** what the true distribution is and produce an encoder based on your guess. Let's call your guessed distribution `$Q = \{q(a), q(b), ..., q(z)\}$`. By definition, the average number of bits used by your encoder for `$Q$` will be higher or equal to `$H(P)$`... and the actual amount is called the **cross entropy** between `$P$` and `$Q$`.

> The cross entropy between `$P$` and `$Q$` is the average number of bits needed to encode events from `$P$` using an optimal encoder for `$Q$`. We denote that number `$H(P, Q)$`.

Said differently, it means that you were **expecting** data from a probability distribution `$Q$`, but in reality the data belonged to a probability distribution `$P$`. And the average number of bits used to encode those events from `$P$` (while expecting they were drawn from `$Q$`) is what we call the cross entropy.

*Can you guess the formula?*

```latex
\begin{align*}
H(P, Q) &= p(x_1) * I(q(x_1)) + p(x_2) * I(q(x_2)) + \ldots \\
&= \sum_x p(x) * I(q(x)) \\
&= - \sum_x p(x) * log(q(x)) \\
\end{align*}
```

This looks very much like `$H(Q)$`, but the information is weighted by the probabilities coming from `$P$`. This makes sense:

You will be using `$Q$` to encode events coming from the machine, therefore the information content will be calculated using `$q(x)$`. However, the ***actual weighting*** of the information for each event comes from `$P$` since that is the **true frequency** of the events.

> Notice that `$H(P, Q) \neq H(Q, P)$`.

Also, notice that if you had guessed `$P$` perfectly well (`$Q=P$`), then the result should be the theoretical minimum number of bits possible to encode events from `$P$`, which is the **entropy**:

```latex
\begin{align*}
H(P, P) &= - \sum_x p(x) * log(p(x)) \\
&= H(P)
\end{align*}
```

# Relative Entropy

Lastly, the ***relative entropy***, also known as the ***KL divergence***.

If you've understood the *cross entropy*, then this should be a piece of cake!

The ***cross entropy*** is the average number of bits used if you encode events drawn from a distribution `$P$` while expecting the events to come from a distribution `$Q$`. We said this number must be higher or equal to `$H(P)$` since that would be the number of bits used by a perfect encoder for `$P$`. `$H(P)$` is a **lower bound** for `$H(P, Q)$`.

The number of ***extra*** bits used ***relative to*** `$H(P)$` is what we call the ***relative entropy*** and we denote it `$KL(P||Q)$`! That is, not the entire entropy but just the extra you used due to the error in guessing `$P$`.

> The relative entropy is the difference in information used by a suboptimal encoder and an optimal encoder: `$H(P, Q) - H(P)$`.

```latex
\begin{align*}
KL(P || Q) &= H(P, Q) - H(P) \\
&= -\sum_x p(x) * log(q(x)) + \sum_x p(x) log(p(x)) \\
&= \sum_x p(x) * (log(p(x)) - log(q(x))) \\
&= \sum_x p(x) * log\left(\frac{p(x)}{q(x)}\right) \\
\end{align*}
```

Like the cross entropy, the *relative entropy* is not commutative: `$KL(P||Q) \neq KL(Q||P)$`. You can understand it as a measure of ***relative difference*** between two probability distributions, the minimum being `$0$` when `$Q=P$`.

# Last Note

In machine learning, we try to minimize the cross entropy:

```latex
H(P, Q) = KL(P || Q) + H(P)
```

Where `$P$` is the distribution of the **data**, and `$Q$` is the distribution of the **model**. Since the data doesn't change during the training, `$H(P)$` is a constant, we are essentially **minimizing the relative entropy**, i.e. the difference between `$P$` and `$Q$`.

Interestingly, in the context of LLMs (Large Language Models), when we minimize the cross entropy and therefore minimize the relative entropy, the loss we end up with after training is an approximation (as KL goes to 0) of the entropy of the data distribution, that is, the ***entropy of language***.

<script src="https://cdnjs.cloudflare.com/ajax/libs/function-plot/1.25.1/function-plot.min.js" integrity="sha512-fsvE52IC5bx7NhuaGLoNE+Sq3EKFQ+fcvaJPE5hGemvMwQudqQuNXC4eG/8CjU2a90P88NzYPRl77iOcXerCHg==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="/assets/entropy/log.js"></script>