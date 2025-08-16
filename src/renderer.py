import re
import os
import datetime
import metadata
import templates
import unicodedata
import markdown
import links


class Renderer(markdown.MarkdownRenderer):
    _LINKS = links.LinkPreview()

    def render_heading(self, text: str, level: int) -> str:
        if level == 1:
            return f'<h2 id={Renderer._make_tag(text)} class="article-section">{text}</h2>'
        elif level == 2:
            return f'<h3 id={Renderer._make_tag(text)} class="article-small-section">{text}</h3>'
        else:
            print(f"Heading with level {level} is not supported!")

    def render_bold(self, text: str) -> str:
        return f'<span class="article-bold">{text}</span>'

    def render_italic(self, text: str) -> str:
        return f'<span class="article-italic">{text}</span>'

    def render_paragraph(self, text: str) -> str:
        return f'<p>{text}</p>'

    def render_code_block(self, text: str, lang: str) -> str:
        if lang == "latex":
            return f'<div class="article-latex">[begin-latex]{text}[end-latex]</div>'
        elif lang == "dot":
            return f'<center><div class="article-graphviz">{text}</div></center>'
        else:
            return f'<pre class="article-code-block {lang}"><code>{text}</code></pre>'

    def render_quote(self, lines: list[str]) -> str:
        quote = '</br>'.join(lines)
        return f'<div class="article-quote">{quote}</div>'

    def render_unordered_list(self, items: list[str]) -> str:
        li = '\n'.join(f'<li class="article-li">{i}</li>' for i in items)
        return f'<ul>{li}</ul>'

    def render_inline_code(self, text: str) -> str:
        if text.startswith('$') and text.endswith('$'):
            return f'[begin-latex-inline]{text[1:-1]}[end-latex-inline]'
        else:
            return f'<code class="article-code-inline">{text}</code>'

    def render_link(self, title: str, url: str) -> str:
        return f'<a class="article-link" target="_blank" href="{url}">{title}</a>'

    def render_link_preview(self, url: str) -> str:
        preview = Renderer._LINKS.get_link_preview(url)
        if not preview:
            print("Could not fetch link preview: ", url)
            title = '<span style="color:red;">ERROR NO INTERNET TO FETCH LINK PREVIEW</span>'
            return f'<a class="article-link" target="_blank" href="{url}">{title}</a>'

        return f'''
            <div class="article-link-preview-container">
                <a class="article-link-preview-link" target="_blank" href="{url}">
                    <span class="article-link-preview-title">{preview.title}</span>
                    <span class="article-link-preview-description">{preview.description}</span>
                    <span class="article-link-preview-website">{preview.website}</span>
                </a>
            </div>
        '''

    def render_download(self, path: str) -> str:
        filename = os.path.basename(path)
        return f'''
            <center>
                <div class="article-file-download-container">
                    <a class="article-file-download-link" href="{path}" download>
                        <img src="/images/download.svg" alt="download" height="30" width="30">
                        <span class="article-file-download-title">{filename}</span>
                    </a>
                </div>
            </center>
        '''

    def render_image(self, alt: str, url: str) -> str:
        url, height, width = Renderer._parse_image_data(url)
        return f'<center><img class="article-image" height="{height}" width="{width}" src="{url}" alt="{alt}"></center>'

    def render_separator(self) -> str:
        return '<div class="article-hr"></div>'

    def render_include(self, path: str) -> str:
        return open(path, "r").read()

    @staticmethod
    def _make_tag(title: str) -> str:
        s = title.lower()
        s = unicodedata.normalize("NFKD", s).encode(
            "ascii", "ignore").decode("utf-8")
        s = re.sub(r"[^a-z0-9\s-]", "", s)
        s = re.sub(r"\s+", "-", s)
        s = re.sub(r"-+", "-", s)
        s = s.strip("-")
        return s

    @staticmethod
    def _parse_image_data(location: str) -> tuple[str, str, str]:
        parts = location.split(";")
        mapping = dict(part.split("=") for part in parts[1:])
        return parts[0], mapping.get("h", ""), mapping.get("w", "")


def _format_date(date: datetime.date) -> str:
    return date.strftime("%b %d, %Y")


def _get_styles(meta: metadata.Metadata) -> str:
    styles = []
    if meta.math:
        styles.append(templates.KATEX_STYLES)
    if meta.code:
        styles.append(templates.HIGHLIGHT_STYLES)
    return "\n".join(styles)


def _get_scripts(meta: metadata.Metadata) -> str:
    scripts = []
    if meta.math:
        scripts.append(templates.KATEX_SCRIPTS)
    if meta.code:
        scripts.append(templates.HIGHLIGHT_SCRIPTS)
    if meta.dot:
        scripts.append(templates.GRAPHVIZ_SCRIPTS)
    return "\n".join(scripts)


def _get_updated_date(meta: metadata.Metadata) -> str:
    if not meta.updated_date:
        return ""
    date = _format_date(meta.updated_date)
    return templates.UPDATED_DATE.replace("{{date}}", date)


def make_article(markdown_text: str) -> str:
    md = markdown.Markdown(Renderer())
    meta = metadata.parse_metadata(markdown_text)
    text = metadata.strip_metadata(markdown_text)
    html = templates.ARTICLE
    html = html.replace("{{title}}", meta.title)
    html = html.replace("{{description}}", meta.description)
    html = html.replace("{{date}}", _format_date(meta.date))
    html = html.replace("{{updated_date}}", _get_updated_date(meta))
    html = html.replace("{{content}}", md.convert(text))
    html = html.replace("{{styles}}", _get_styles(meta))
    html = html.replace("{{scripts}}", _get_scripts(meta))
    html = html.strip()
    return html


def make_article_entry(meta: metadata.Metadata, filename: str) -> str:
    html = templates.ARTICLE_ENTRY
    html = html.replace("{{filename}}", filename)
    html = html.replace("{{title}}", meta.title)
    html = html.replace("{{description}}", meta.description)
    html = html.replace("{{date}}", _format_date(meta.date))
    html = html.replace("{{pin}}", templates.PIN if meta.pinned else "")
    html = html.strip()
    return html
