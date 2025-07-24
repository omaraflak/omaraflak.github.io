import re
import marko
import marko.inline
import metadata
import datetime
import templates
import unicodedata
import link_preview.link_preview


def _make_tag(title: str) -> str:
    s = title.lower()
    s = unicodedata.normalize("NFKD", s).encode(
        "ascii", "ignore").decode("utf-8")
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    s = s.strip("-")
    return s


def _format_date(year: int, month: int, day: int) -> str:
    date = datetime.datetime(year, month, day)
    return date.strftime("%b %d, %Y")


def _parse_image_data(location: str) -> tuple[str, str, str]:
    parts = location.split(";")
    mapping = dict(part.split("=") for part in parts[1:])
    return parts[0], mapping.get("h", ""), mapping.get("w", "")


def _render_elements(elements: list[marko.block.Element]) -> str:
    return "".join(_render_element(element) for element in elements)


def _render_element(element: marko.block.Element) -> str:
    if isinstance(element, marko.inline.RawText):
        return element.children
    elif isinstance(element, marko.block.Paragraph):
        return f"<p>{_render_elements(element.children)}</p>"
    elif isinstance(element, marko.block.Heading):
        title = _render_elements(element.children)
        if element.level == 1:
            return f'<h2 id={_make_tag(title)} class="article-section">{title}</h2>'
        elif element.level == 2:
            return f'<h3 id={_make_tag(title)} class="article-small-section">{title}</h3>'
        else:
            print(f"Heading with level {element.level} is not supported!")
    elif isinstance(element, marko.block.Quote):
        quote = _render_elements(element.children)
        return f'<div class="article-quote">{quote}</div>'
    elif isinstance(element, marko.block.List):
        tmp = _render_elements(element.children)
        return f'<ul>{tmp}</ul>'
    elif isinstance(element, marko.block.ListItem):
        tmp = _render_elements(element.children)
        return f'<li class="article-li">{tmp}</li>'
    elif isinstance(element, marko.block.ThematicBreak):
        return '<div class="article-hr"></div>'
    elif isinstance(element, marko.inline.Emphasis):
        text = _render_elements(element.children)
        return f'<span class="article-italic">{text}</span>'
    elif isinstance(element, marko.inline.StrongEmphasis):
        text = _render_elements(element.children)
        return f'<span class="article-bold">{text}</span>'
    elif isinstance(element, marko.inline.Link):
        title = _render_elements(element.children)
        if title:
            return f'<a class="article-link" target="_blank" href="{element.dest}">{title}</a>'
        else:
            preview = link_preview.link_preview.generate_dict(element.dest)
            return f'''
                <a class="article-link-preview-link" target="_blank" href="{element.dest}">
                    <div class="article-link-preview-container">
                        <p class="article-link-preview-title">{preview["title"]}</p>
                        <p class="article-link-preview-description">{preview["description"]}</p>
                        <p class="article-link-preview-website">{preview["website"]}</p>
                    </div>
                </a>
            '''
    elif isinstance(element, marko.inline.Image):
        alt = _render_elements(element.children)
        url, height, width = _parse_image_data(element.dest)
        return f'<center><img class="article-image" height="{height}" width="{width}" src="{url}" alt="{alt}"></center>'
    elif isinstance(element, marko.block.BlankLine):
        return ""
    elif isinstance(element, marko.inline.LineBreak):
        return "</br>"
    elif isinstance(element, marko.inline.CodeSpan):
        return f'<code class="article-code-inline">{element.children}</code>'
    elif isinstance(element, marko.block.FencedCode):
        code = _render_elements(element.children)
        if element.lang == "latex":
            return f'<div class="article-latex">$${code}$$</div>'
        else:
            return f'<pre class="article-code-block {element.lang}"><code>{code}</code></pre>'
    elif isinstance(element, marko.block.HTMLBlock):
        return element.body
    elif isinstance(element, marko.inline.Literal):
        return element.children
    elif isinstance(element, marko.inline.InlineHTML):
        return element.children
    else:
        print(f"{element.get_type()} is not supported!")
    return ""


def make_article(markdown: str) -> str:
    keys = ["title", "description", "year", "month", "day"]
    meta = metadata.parse_metadata(markdown, keys)
    text = metadata.strip_metadata(markdown, keys)
    generated_html = _render_elements(marko.parse(text).children)
    date = _format_date(
        int(meta["year"]),
        int(meta["month"]),
        int(meta["day"])
    )
    html = templates.ARTICLE
    html = html.replace("{{title}}", meta["title"])
    html = html.replace("{{description}}", meta["description"])
    html = html.replace("{{date}}", date)
    html = html.replace("{{content}}", generated_html)
    html = html.strip()
    return html


def make_article_entry(markdown: str, filename: str) -> str:
    keys = ["title", "description", "year", "month", "day"]
    meta = metadata.parse_metadata(markdown, keys)
    date = _format_date(
        int(meta["year"]),
        int(meta["month"]),
        int(meta["day"])
    )
    html = templates.ENTRY
    html = html.replace("{{filename}}", filename)
    html = html.replace("{{title}}", meta["title"])
    html = html.replace("{{description}}", meta["description"])
    html = html.replace("{{date}}", date)
    html = html.strip()
    return html
