import re
import abc
import html
import random
import string
from typing import Callable


class MarkdownRenderer(abc.ABC):
    @abc.abstractmethod
    def render_heading(self, text: str, level: int) -> str:
        return

    @abc.abstractmethod
    def render_bold(self, text: str) -> str:
        return

    @abc.abstractmethod
    def render_italic(self, text: str) -> str:
        return

    @abc.abstractmethod
    def render_paragraph(self, text: str) -> str:
        return

    @abc.abstractmethod
    def render_code_block(self, text: str, lang: str) -> str:
        return

    @abc.abstractmethod
    def render_quote(self, lines: list[str]) -> str:
        return

    @abc.abstractmethod
    def render_unordered_list(self, items: list[str]) -> str:
        return

    @abc.abstractmethod
    def render_inline_code(self, text: str) -> str:
        return

    @abc.abstractmethod
    def render_link(self, title: str, url: str) -> str:
        return

    @abc.abstractmethod
    def render_link_preview(self, url: str) -> str:
        return

    @abc.abstractmethod
    def render_image(self, alt: str, url: str) -> str:
        return

    @abc.abstractmethod
    def render_separator(self) -> str:
        return

    @abc.abstractmethod
    def render_include(self, path: str) -> str:
        return

    @abc.abstractmethod
    def render_download(self, url: str) -> str:
        return


class Markdown:
    HEADINGS = re.compile(r'^(?P<level>#{1,3})\s(?P<text>.+)$')
    ITALIC = re.compile(r'\*(?P<text>.+?)\*')
    BOLD = re.compile(r'(\*\*)(?P<text>.+?)(\*\*)')
    CODE_BLOCKS = re.compile(r'```(?P<lang>\w+)?\n(?P<text>[\s\S]+?)\n```')
    QUOTE = re.compile(r'(?m)^(?P<block>(?:>\s?.*(?:\n>\s?.*)*))')
    UNORDERED_LIST = re.compile(r'(?m)^(?P<list>(?:\s+-[^-].*\n?)+)$')
    INLINE_BLOCK = re.compile(r'`(?P<text>.+?)`')
    INLINE_BLOCK_ALT = re.compile(r'``\s(?P<text>.+?)\s``')
    LINK = re.compile(r'\[(?P<title>.*)\]\((?P<url>.+?)\)')
    IMAGE = re.compile(r'!\[(?P<alt>.*)\]\((?P<url>.+?)\)')
    INCLUDE = re.compile(r'\[#include\]\((?P<path>.*?)\)')
    DOWNLOAD = re.compile(r'\[#download\]\((?P<url>.*?)\)')
    LINK_PREVIEW = re.compile(r'\[\]\((?P<url>.*?)\)')
    SEPARATOR = re.compile(r'^---$')
    UUID = re.compile(r'(?P<uid><uid>[a-z]{5}-[a-z]{3}</uid>)')
    HTML = re.compile(r'^<(\w+).*>(.*</\1>)?$')

    def __init__(self, renderer: MarkdownRenderer):
        self.renderer = renderer
        self.immutables: dict[str, str] = dict()

    def _immutable(render: Callable[[re.Match[str]], str]) -> Callable[[re.Match[str]], str]:
        """Prevents a content from being altered by other tags, e.g. bold, italic, etc."""

        def _render(self: 'Markdown', match: re.Match[str]) -> str:
            uid = Markdown._uuid()
            rendered = render(self, match)
            self.immutables[uid] = rendered
            return uid
        return _render

    def _render_uid(self, match: re.Match[str]) -> str:
        uid = match.group('uid')
        return self.immutables.pop(uid)

    def _render_bold(self, match: re.Match[str]) -> str:
        text = match.group('text')
        return self.renderer.render_bold(text)

    def _render_italic(self, match: re.Match[str]) -> str:
        text = match.group('text')
        return self.renderer.render_italic(text)

    @_immutable
    def _render_inline_code(self, match: re.Match[str]) -> str:
        text = html.escape(match.group('text'))
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
        return self.renderer.render_quote(lines)

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
        title = html.escape(match.group('title'))
        url = html.escape(match.group('url'))
        return self.renderer.render_link(title, url)

    @_immutable
    def _render_link_preview(self, match: re.Match[str]) -> str:
        url = html.escape(match.group('url'))
        return self.renderer.render_link_preview(url)

    @_immutable
    def _render_image(self, match: re.Match[str]) -> str:
        alt = html.escape(match.group('alt'))
        url = html.escape(match.group('url'))
        return self.renderer.render_image(alt, url)

    def _render_separator(self, _: re.Match[str]) -> str:
        return self.renderer.render_separator()

    @_immutable
    def _render_include(self, match: re.Match[str]) -> str:
        path = match.group('path')
        return self.renderer.render_include(path)

    def _render_download(self, match: re.Match[str]) -> str:
        url = match.group('url')
        return self.renderer.render_download(url)

    def _render_inlines(self, text: str) -> str:
        text = Markdown.HEADINGS.sub(self._render_header, text)
        text = Markdown.INLINE_BLOCK_ALT.sub(self._render_inline_code, text)
        text = Markdown.INLINE_BLOCK.sub(self._render_inline_code, text)
        text = Markdown.IMAGE.sub(self._render_image, text)
        text = Markdown.DOWNLOAD.sub(self._render_download, text)
        text = Markdown.LINK_PREVIEW.sub(self._render_link_preview, text)
        text = Markdown.LINK.sub(self._render_link, text)
        text = Markdown.BOLD.sub(self._render_bold, text)
        text = Markdown.ITALIC.sub(self._render_italic, text)
        text = Markdown.SEPARATOR.sub(self._render_separator, text)
        return text

    def _render_multilines(self, text: str) -> str:
        text = Markdown.INCLUDE.sub(self._render_include, text)
        text = Markdown.CODE_BLOCKS.sub(self._render_code_block, text)
        text = Markdown.QUOTE.sub(self._render_quote, text)
        text = Markdown.UNORDERED_LIST.sub(self._render_unordered_list, text)
        return text

    def convert(self, markdown: str) -> str:
        markdown = self._render_multilines(markdown)

        html = []
        for line in markdown.splitlines():
            line = line.strip()

            if not line:
                continue

            line = self._render_inlines(line)
            if not Markdown.HTML.match(line):
                line = self.renderer.render_paragraph(line)

            html.append(line)

        result = '\n'.join(html)

        # some uids might be nested under other uids...
        while self.immutables:
            tmp = result
            result = Markdown.UUID.sub(self._render_uid, result)
            if tmp == result:
                raise ValueError("UIDs not found: ", self.immutables)

        return result

    @staticmethod
    def _uuid() -> str:
        letters = string.ascii_lowercase
        a = ''.join(random.choice(letters) for _ in range(5))
        b = ''.join(random.choice(letters) for _ in range(3))
        return f'<uid>{a}-{b}</uid>'
