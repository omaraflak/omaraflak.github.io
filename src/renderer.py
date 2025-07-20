import re
import marko
import marko.inline
import datetime


TEMPLATE = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <link rel="stylesheet" href="../styles/index.css">
    <link rel="stylesheet" href="../styles/fonts.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <link rel="stylesheet" href="https://unpkg.com/@highlightjs/cdn-assets@11.7.0/styles/github.min.css">
</head>

<body>
    <div id="header"></div>
    <div class="article-header">
        <div class="article-header-content">
            <h1 class="article-title">{{title}}</h1>
            <p class="article-description">{{description}}</p>
            <p class="article-date">{{date}}</p>
        </div>
    </div>
    <main class="article-main">
        <article class="article-body">
            {{content}}
        </article>
    </main>
    <div class="article-hr"></div>
    <div id="footer"></div>
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
    <script src="../scripts/common.js"></script>
</body>

</html>
"""

METADATA_PATTERN = r"^:(.+):(.+)$"


def strip(text: str, sub: str) -> str:
    while True:
        tmp = text.removeprefix(sub).removesuffix(sub)
        if tmp == text:
            return tmp
        text = tmp


def make_tag(title: str) -> str:
    return title.lower().replace(" ", "-")


def parse_image_size(location: str) -> tuple[str, str, str]:
    parts = location.split(";")
    mapping = dict(part.split("=") for part in parts[1:])
    return parts[0], mapping.get("h", ""), mapping.get("w", "")


def format_date(year: int, month: int, day: int) -> str:
    date = datetime.datetime(year, month, day)
    return date.strftime("%b %d, %Y")


def parse_metadata(text: str, metadata: dict[str, str]) -> bool:
    search = re.findall(METADATA_PATTERN, text)
    if search:
        key, value = search[0]
        metadata[key] = value.strip()
        return True
    return False


def parse_elements(elements: list[marko.block.Element], metadata: dict[str, str]) -> str:
    return "".join(parse_element(element, metadata) for element in elements)


def parse_element(element: marko.block.Element, metadata: dict[str, str]) -> str:
    if isinstance(element, marko.inline.RawText):
        if not parse_metadata(element.children, metadata):
            return element.children
    elif isinstance(element, marko.block.Paragraph):
        return parse_elements(element.children, metadata)
    elif isinstance(element, marko.block.Heading):
        title = parse_elements(element.children, metadata)
        if element.level == 1:
            return f'<h2 id={make_tag(title)} class="article-section">{title}</h2>'
        elif element.level == 2:
            return f'<h3 id={make_tag(title)} class="article-small-section">{title}</h3>'
        else:
            print(f"Heading with level {element.level} is not supported!")
    elif isinstance(element, marko.block.Quote):
        quote = parse_elements(element.children, metadata)
        return f'<div class="article-quote">{quote}</div>'
    elif isinstance(element, marko.block.List):
        tmp = parse_elements(element.children, metadata)
        return f'<ul>{tmp}</ul>'
    elif isinstance(element, marko.block.ListItem):
        tmp = parse_elements(element.children, metadata)
        return f'<li class="article-li">{tmp}</li>'
    elif isinstance(element, marko.block.ThematicBreak):
        return '<div class="article-hr"></div>'
    elif isinstance(element, marko.inline.Emphasis):
        text = parse_elements(element.children, metadata)
        return f'<span class="article-italic">{text}</span>'
    elif isinstance(element, marko.inline.StrongEmphasis):
        text = parse_elements(element.children, metadata)
        return f'<span class="article-bold">{text}</span>'
    elif isinstance(element, marko.inline.Link):
        title = parse_elements(element.children, metadata)
        return f'<a class="article-link" href="{element.dest}">{title}</a>'
    elif isinstance(element, marko.inline.Image):
        alt = parse_elements(element.children, metadata)
        url, height, width = parse_image_size(element.dest)
        return f'<center><img class="article-image" height="{height}" width="{width}" src="{url}" alt="{alt}"></center>'
    elif isinstance(element, marko.block.BlankLine):
        return "<p></p>"
    elif isinstance(element, marko.inline.LineBreak):
        return "</br>"
    elif isinstance(element, marko.inline.CodeSpan):
        return f'<code class="article-code-inline">{element.children}</code>'
    elif isinstance(element, marko.block.FencedCode):
        code = parse_elements(element.children, metadata)
        return f'<pre class="article-code-block"><code>{code}</code></pre>'
    elif isinstance(element, marko.block.HTMLBlock):
        return element.body
    else:
        print(f"{element.get_type()} is not supported!")
    return ""


def parse_document(document: marko.block.Document) -> tuple[str, dict[str, str]]:
    metadata = dict()
    html = parse_elements(document.children, metadata)
    html = strip(html, "<p></p>")
    html = strip(html, "</br>")
    html = strip(html, "<p></p>")
    html = strip(html, "</br>")
    return html, metadata


def to_html(markdown: str) -> str:
    content, metadata = parse_document(marko.parse(markdown))
    date = format_date(
        int(metadata["year"]),
        int(metadata["month"]),
        int(metadata["day"])
    )
    html = TEMPLATE.replace("{{title}}", metadata["title"])
    html = html.replace("{{description}}", metadata["description"])
    html = html.replace("{{date}}", date)
    html = html.replace("{{content}}", content)
    html = html.strip()
    return html
