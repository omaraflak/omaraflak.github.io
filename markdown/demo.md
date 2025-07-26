:title: Demo
:description: Demo of all editing features of the blosg
:year: 2025
:month: 7
:day: 26

This is a demo file for all features available.

# This is a title

You can have inline code such as `def main()`. If you surround the inner code by '$' signs on both side then it renders `$\LaTeX$`. This formula `$E=mc^2$` relates the energy contained by an object with its mass.

## This is a secondary title

Links are also supported. Check out my [github](https://github.com/omaraflak). Use the following formatting `[title](https://example.com)`.

If no title is provided, then the link will be in preview mode `[](https://example.com)`:

[](https://github.com/omaraflak)

You can include images as well with `![alt](/image/path)`:

![svg](../markdown/automata.svg)

The height and/or width of the image can be specified in pixels or percentage using the following syntax:

```md
![alt](/image/path;h=100) # height is 100px
![alt](/image/path;w=50%) # width is 50% of the page
![alt](/image/path;h=200;w=200) # height is 200px and width is 200px
```

Use `---` for a horizontal line.

---

You can display code blocks by surround your code with 3 back ticks `` ``` `` before and after the code. Specify a language after the opening backticks to change the code highlighting.

```python
def multiply(a: int, b: int) -> int:
    return a * b
```

If the language specified is `latex`, i.e. `` ```latex ``, then the renderer will show `$\LaTeX$` in display mode.

```latex
(a+b)^n = \sum_{i=0}^n {n \choose k} a^k b^{n-k}
```

The renderer also supports Graphviz! Juse use `` ```dot `` for the opening code block.

```dot
digraph {
    bgcolor="transparent";
    graph [rankdir="LR"]
    node [shape="circle"]
    a [label=<<i>A</i>>, color="red"]
    b [label=<<b>B</b>>, color="green"]
    a -> b [label="1"]
    b -> c:name [label="2"]
    subgraph cluster_1 {
        c [label=<<table><tr><td port="name">C</td></tr></table>>]
    }
}
```