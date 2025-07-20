:title: Entropy & Information
:description: What is information and how is it measured? What is entropy? Cross entropy? Relative entropy (aka KL Divergence)?
:year: 2025
:month: 2
:day: 21


# Information

Information is tied to the field of **probabilities**, and it can be seen as a measure of **uncertainty**. To avoid extrapolation and misuse of this concept, you need to remember that it only makes sense to talk about information (in the mathematical sense) when you are studying a **probabilistic event**.

> Information relates to probabilities in that the realisation of an event with low probability brings a lot of information, and the realisation of an event with high probability brings little information.

For example: the event *“It rains in London”* is very ***likely*** therefore it brings ***little*** information. In contrast, the event *“It rains in the Sahara Desert”* is so ***unlikely***, it brings a lot ***more*** information (e.g. it could more realistically help you pin-point the day of the event).

So information relates to probability, but how ***exactly***?

Let’s explore the properties we would like such a mapping to have:

1. Low probability $\implies$ high information (already established)
2. High probability $\implies$ low information (already established)
3. Probability = 1 $\implies$ Information = 0 (derived from 2 — that’s because if an event is certain to be realised, then knowing about it doesn’t bring about any information)
4. Probability → 0 $\implies$ Information → $\inf$ (the opposite of 3 must be true)
5. Information should be **additive for independent events**, i.e. learning about two independent events should give you the amount of information equal to the sum of the information gained from each event separately:

information(event1 and event2) = information(event1) + information(event2)

[this is a link](#information)