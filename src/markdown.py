import re
import random
import string
from typing import Callable


class MarkdownRenderer:
    def render_heading(self, text: str, level: int) -> str:
        return f'<h{level}>{text}</h{level}>'

    def render_bold(self, text: str) -> str:
        return f'<strong>{text}</strong>'

    def render_italic(self, text: str) -> str:
        return f'<em>{text}</em>'

    def render_paragraph(self, text: str) -> str:
        return f'<p>{text}</p>'

    def render_code_block(self, text: str, lang: str) -> str:
        if lang:
            return f'<pre><code class="language-{lang}">{text}</code></pre>'
        else:
            return f'<pre><code>{text}</code></pre>'

    def render_quote(self, text: str) -> str:
        return f'<span>{text}</span>'

    def render_unordered_list(self, items: list[str]) -> str:
        li = '\n'.join(f'<li>{i}</li>' for i in items)
        return f'<ul>{li}</ul>'

    def render_inline_code(self, text: str) -> str:
        return f'<pre>{text}</pre>'

    def render_link(self, title: str, url: str) -> str:
        return f'<a href="{url}">{title}</a>'

    def render_image(self, alt: str, url: str) -> str:
        return f'<img src="{url}" alt="{alt}">'

    def render_separator(self) -> str:
        return '<hr>'


class Markdown:
    HEADINGS = re.compile(r'^(?P<level>#{1,3})\s(?P<text>.+)$')
    ITALIC = re.compile(r'\*(?P<text>.+?)\*')
    BOLD = re.compile(r'(\*\*)(?P<text>.+?)(\*\*)')
    CODE_BLOCKS = re.compile(r'```(?P<lang>\w+)?\n(?P<text>[\s\S]+?)\n```')
    QUOTE = re.compile(r'(?m)^(?P<block>(?:>\s?.*(?:\n>\s?.*)*))')
    UNORDERED_LIST = re.compile(r'(?m)^(?P<list>(?:\s+-[^-].*\n?)+)$')
    INLINE_BLOCK = re.compile(r'`(?P<text>.+?)`')
    INLINE_BLOCK_ALT = re.compile(r'``\s(?P<text>.+?)\s``')
    LINK = re.compile(r'\[(?P<title>.*)\]\((?P<url>.+)\)')
    IMAGE = re.compile(r'!\[(?P<alt>.*)\]\((?P<url>.+)\)')
    SEPARATOR = re.compile(r'^---$')
    UUID = re.compile(r'(\%\%[a-z]{5}-[a-z]{3}\%\%)')
    HTML = re.compile(r'^<(\w+).*>(.*</\1>)?$')

    def __init__(self, renderer: MarkdownRenderer | None = None):
        self.renderer = renderer or MarkdownRenderer()
        self.immutables: dict[str, str] = dict()

    def _immutable(render: Callable[[re.Match[str]], str]) -> Callable[[re.Match[str]], str]:
        def _render(self: 'Markdown', match: re.Match[str]) -> str:
            uid = Markdown._uuid()
            rendered = render(self, match)
            self.immutables[uid] = rendered
            return uid
        return _render

    def _render_uid(self, match: re.Match[str]) -> str:
        uid = match.group(1)
        return self.immutables[uid]

    def _render_bold(self, match: re.Match[str]) -> str:
        text = match.group('text')
        return self.renderer.render_bold(text)

    def _render_italic(self, match: re.Match[str]) -> str:
        text = match.group('text')
        return self.renderer.render_italic(text)

    @_immutable
    def _render_inline_code(self, match: re.Match[str]) -> str:
        text = match.group('text')
        return self.renderer.render_inline_code(text)

    @_immutable
    def _render_code_block(self, match: re.Match[str]) -> str:
        lang = match.group('lang')
        text = match.group('text')
        return self.renderer.render_code_block(text, lang)

    def _render_quote(self, match: re.Match[str]) -> str:
        text = match.group('block')
        lines = [line.strip() for line in text.splitlines()]
        lines = [line.strip('>').strip() for line in lines if line]
        quote = '</br>'.join(lines)
        return self.renderer.render_quote(quote)

    def _render_unordered_list(self, match: re.Match[str]) -> str:
        text = match.group('list')
        lines = [line.strip() for line in text.splitlines()]
        lines = [line.strip('-').strip() for line in lines if line]
        return self.renderer.render_unordered_list(lines)

    def _render_header(self, match: re.Match[str]) -> str:
        text = match.group('text')
        level = len(match.group('level'))
        return self.renderer.render_heading(text, level)

    @_immutable
    def _render_link(self, match: re.Match[str]) -> str:
        title = match.group('title')
        url = match.group('url')
        return self.renderer.render_link(title, url)

    @_immutable
    def _render_image(self, match: re.Match[str]) -> str:
        alt = match.group('alt')
        url = match.group('url')
        return self.renderer.render_image(alt, url)

    def _render_separator(self, _: re.Match[str]) -> str:
        return self.renderer.render_separator()

    def _render_inlines(self, text: str) -> str:
        text = Markdown.HEADINGS.sub(self._render_header, text)
        text = Markdown.INLINE_BLOCK_ALT.sub(self._render_inline_code, text)
        text = Markdown.INLINE_BLOCK.sub(self._render_inline_code, text)
        text = Markdown.IMAGE.sub(self._render_image, text)
        text = Markdown.LINK.sub(self._render_link, text)
        text = Markdown.BOLD.sub(self._render_bold, text)
        text = Markdown.ITALIC.sub(self._render_italic, text)
        text = Markdown.SEPARATOR.sub(self._render_separator, text)
        return text

    def _render_multilines(self, text: str) -> str:
        text = Markdown.CODE_BLOCKS.sub(self._render_code_block, text)
        text = Markdown.QUOTE.sub(self._render_quote, text)
        text = Markdown.UNORDERED_LIST.sub(self._render_unordered_list, text)
        return text

    def convert(self, markdown_text: str) -> str:
        markdown_text = self._render_multilines(markdown_text)

        html = []
        for line in markdown_text.splitlines():
            if not line.strip():
                continue

            line = self._render_inlines(line)
            line = Markdown.UUID.sub(self._render_uid, line)
            if not Markdown.HTML.match(line):
                line = self.renderer.render_paragraph(line)

            html.append(line)

        return '\n'.join(html)

    @staticmethod
    def _uuid() -> str:
        letters = string.ascii_lowercase
        a = ''.join(random.choice(letters) for _ in range(5))
        b = ''.join(random.choice(letters) for _ in range(3))
        return f'%%{a}-{b}%%'
