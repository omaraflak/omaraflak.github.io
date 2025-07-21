:title: Article Title
:description: This is a short description of the article content.
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

Code blocks are displayed by surrounding your code with 3 backticks: `` ``` ``.

# $\LaTeX$

Last, but not least, you can render $\LaTeX$ formulas directly in the document. Either surround the text with `$` for inline mode like $E=mc^2$, or with `$$` for display mode.

For example this:

```
$$(a + b)^n = \sum_{i=0}^n {n \choose k} a^k b^{n-k}$$
```

Will render like this:

$$(a + b)^n = \sum_{i=0}^n {n \choose k} a^k b^{n-k}$$