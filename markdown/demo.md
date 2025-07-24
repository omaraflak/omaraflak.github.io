:title: Demo
:description: A summary of all available commands and formattings for this blog.
:year: 2025
:month: 7
:day: 20

These are the different formatting options of this blog.

# This is a title

This is a normal paragraph. This is a normal paragraph. This is a normal paragraph. This is a normal paragraph. This is a normal paragraph. This is a normal paragraph. This is a normal paragraph. This is a normal paragraph. This is a normal paragraph. This is a normal paragraph. This is a normal paragraph. This is a normal paragraph. This is a normal paragraph.

> You can also write quotes. You can also write quotes. You can also write quotes. You can also write quotes. You can also write quotes. You can also write quotes. You can also write quotes. You can also write quotes. You can also write quotes. You can also write quotes. You can also write quotes. You can also write quotes. You can also write quotes. You can also write quotes.

## This is a secondary title

Text can be formatted as *italic* (`*text*`), **bold** (`**text**`), or ***italic and bold !*** (`***text***`)

By the way, those `inlined blocks` are created with backticks: `` `text` ``.

You can create unordered lists by prepending each line with a dash followed by a space `- `:

- One
- Two
- Three

Links are defined as: `[placeholder](https://example.com)`

Visit my [GitHub](https://github.com/omaraflak)!

If no placeholder is given, i.e. `[](https://example.com)`, then the link is displayed in preview mode:

[](https://github.com/omaraflak)

You can link to *sections* of the document by using the special url `#this-is-a-title`: [first section](#this-is-a-title).

When you need to have a separator use the `---` placeholder on one line, it will have the following effect:

---

You can also include images: `![description](/path/to/image.png)`.

![image](../md/image.webp;w=200)

You can optionally specify a height and/or a width, in pixelx or percentage like so:


- `![image](/path/image.png;h=200)` height is 200px
- `![image](/path/image.png;w=100%)` width is 100% of the page
- `![image](/path/image.png;h=100;w=100)` 100x100 pixels

And even code blocks:

```
def multiply(a: int, b: int) -> int:
    return a * b

print(multiply(5, 8))
```

Code blocks are displayed by surrounding your code with 3 backticks: `` ``` ``. You can specify the code language after the opening back ticks for syntax highlighting. If you don't specify anything, the language will be detected automatically on best effort.

# $\LaTeX$

Last, but not least, you can render $\LaTeX$ formulas directly in the document. Either surround the text with `$` for inline mode like $E=mc^2$, or use triple back ticks with "latext" language for display mode.

For example this:

````
```latex
(a + b)^n = \sum_{i=0}^n {n \choose k} a^k b^{n-k}
```
````

Will render like this:

```latex
(a + b)^n = \sum_{i=0}^n {n \choose k} a^k b^{n-k}
```

---

<canvas id="canvas" style="width: 100%; background-color: black"></canvas>
<script src="../scripts/canvas.js"></script>
<script src="../scripts/matrix.js"></script>
<script src="../scripts/donut.js"></script>
