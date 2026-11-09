"""Markdown-to-HTML renderer.

The approach is ported from the line-based renderer in the sibling ``matrix``
project (``frontend/src/lib/markdown.js``):

1. Escape the raw HTML special characters.
2. Lift fenced code blocks out of the text so later steps don't touch them.
3. Apply inline replacements (code, bold, italic, links) to the whole text.
4. Walk the remaining lines to build block-level elements: headings,
   blockquotes, nested ordered/unordered lists, and paragraphs.
5. Restore the fenced code blocks.

Unlike the ``matrix`` version, which emits Tailwind utility classes for an
in-app preview, this renderer emits plain semantic HTML tags so the output is
reusable anywhere.
"""

from __future__ import annotations

import re
from pathlib import Path

__all__ = ["MarkdownRenderer", "render", "render_file"]

# Sentinels used to hide fenced code blocks from the line-level processing.
_PLACEHOLDER = "\x00CODEBLOCK{}\x00"
_PLACEHOLDER_RE = re.compile(r"\x00CODEBLOCK(\d+)\x00")

# Block-level fences: ```lang\n ... ``` (the language/info string is optional).
_FENCE_RE = re.compile(r"```([^\n`]*)\n?(.*?)```", re.DOTALL)

# Inline patterns, applied to the whole (escaped) text.
_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC_STAR_RE = re.compile(r"\*([^*\n]+)\*")
# The underscore form requires word boundaries so snake_case is left alone.
_ITALIC_UNDERSCORE_RE = re.compile(r"(^|[\s(])_([^_\n]+)_(?=$|[\s.,;:!?)])")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")

# Line-level patterns.
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_OL_RE = re.compile(r"^(\s*)(\d+)\.\s+(.*)$")
_UL_RE = re.compile(r"^(\s*)[-*+]\s+(.*)$")
# HTML is escaped before this pass runs, so ">" is already "&gt;" here.
_BLOCKQUOTE_RE = re.compile(r"^\s*&gt;\s?(.*)$")

# Kramdown/Jekyll "inline attribute list" applied to the preceding blockquote,
# e.g. ``{: .prompt-danger }``. Used by the Chirpy theme for callouts.
_ATTR_RE = re.compile(r"^\s*\{:\s*(.+?)\s*\}\s*$")
_CLASS_TOKEN_RE = re.compile(r"\.([A-Za-z0-9_-]+)")


def _escape(text: str) -> str:
    """Escape the three HTML-significant characters (matching matrix)."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class MarkdownRenderer:
    """Render Markdown text into an HTML fragment.

    The renderer is stateless between calls, so a single instance can be
    reused. It is a class mainly so the inline and block passes can be
    overridden by subclasses.
    """

    def render(self, text: str) -> str:
        """Return an HTML fragment for ``text`` (an empty string if falsy)."""
        if not text:
            return ""

        html = _escape(text)

        code_blocks: list[str] = []
        html = self._extract_code_blocks(html, code_blocks)
        html = self._render_inline(html)
        html = self._render_blocks(html)

        # Restore the fenced code blocks.
        def _restore(match: re.Match[str]) -> str:
            return code_blocks[int(match.group(1))]

        return _PLACEHOLDER_RE.sub(_restore, html)

    # -- passes ---------------------------------------------------------------

    def _extract_code_blocks(self, html: str, sink: list[str]) -> str:
        """Replace each fenced block with a placeholder, storing the HTML."""

        def _replace(match: re.Match[str]) -> str:
            info = match.group(1).strip()
            code = match.group(2)
            # Drop a single leading/trailing newline introduced by the fence.
            code = code.strip("\n")
            lang = info.split()[0] if info else ""
            cls = f' class="language-{lang}"' if lang else ""
            idx = len(sink)
            sink.append(f"<pre><code{cls}>{code}</code></pre>")
            return _PLACEHOLDER.format(idx)

        return _FENCE_RE.sub(_replace, html)

    def _render_inline(self, html: str) -> str:
        """Apply inline replacements to the whole text, in precedence order."""
        html = _INLINE_CODE_RE.sub(r"<code>\1</code>", html)
        html = _BOLD_RE.sub(r"<strong>\1</strong>", html)
        # Bold ran first, so a lone asterisk left here is an emphasis marker.
        html = _ITALIC_STAR_RE.sub(r"<em>\1</em>", html)
        html = _ITALIC_UNDERSCORE_RE.sub(r"\1<em>\2</em>", html)
        html = _LINK_RE.sub(r'<a href="\2">\1</a>', html)
        return html

    def _render_blocks(self, html: str) -> str:
        """Walk the lines and assemble block-level elements."""
        out: list[str] = []
        para: list[str] = []
        quote: list[str] = []
        # Each stack entry is (tag, indent) for an open list.
        stack: list[tuple[str, int]] = []

        def flush_para() -> None:
            if para:
                out.append("<p>" + "<br>\n".join(para) + "</p>")
                para.clear()

        def flush_quote(css_class: str | None = None) -> None:
            if quote:
                attr = f' class="{css_class}"' if css_class else ""
                out.append(f"<blockquote{attr}>\n" + "<br>\n".join(quote) + "\n</blockquote>")
                quote.clear()

        def close_all_lists() -> None:
            while stack:
                tag, _ = stack.pop()
                out.append(f"</{tag}>")

        def flush_all() -> None:
            flush_para()
            flush_quote()
            close_all_lists()

        def handle_list(tag: str, indent: int, content: str) -> None:
            flush_para()
            flush_quote()
            # Close deeper lists, and same-level lists of a different type.
            while stack:
                top_tag, top_indent = stack[-1]
                if top_indent > indent or (top_indent == indent and top_tag != tag):
                    stack.pop()
                    out.append(f"</{top_tag}>")
                else:
                    break
            # Open a new list when going deeper (or starting fresh).
            if not stack or stack[-1][1] < indent:
                out.append(f"<{tag}>")
                stack.append((tag, indent))
            out.append(f"<li>{content}</li>")

        for line in html.split("\n"):
            # Fenced-code placeholders pass straight through.
            if "\x00CODEBLOCK" in line:
                flush_all()
                out.append(line)
                continue

            if line.strip() == "":
                flush_all()
                continue

            heading = _HEADING_RE.match(line)
            if heading:
                flush_all()
                level = len(heading.group(1))
                out.append(f"<h{level}>{heading.group(2).strip()}</h{level}>")
                continue

            quote_match = _BLOCKQUOTE_RE.match(line)
            if quote_match:
                flush_para()
                close_all_lists()
                quote.append(quote_match.group(1))
                continue

            # An attribute line decorates the blockquote just above it; when
            # there is none it is a stray directive and gets dropped.
            attr_match = _ATTR_RE.match(line)
            if attr_match:
                classes = _CLASS_TOKEN_RE.findall(attr_match.group(1))
                if quote:
                    flush_quote(" ".join(classes) if classes else None)
                continue

            ol = _OL_RE.match(line)
            if ol:
                handle_list("ol", len(ol.group(1)), ol.group(3))
                continue

            ul = _UL_RE.match(line)
            if ul:
                handle_list("ul", len(ul.group(1)), ul.group(2))
                continue

            # Anything else is paragraph text.
            flush_quote()
            close_all_lists()
            para.append(line)

        flush_all()
        return "\n".join(out)


# A module-level default instance powers the convenience functions.
_DEFAULT = MarkdownRenderer()


def render(text: str) -> str:
    """Render a Markdown string to an HTML fragment."""
    return _DEFAULT.render(text)


def render_file(path: str | Path, encoding: str = "utf-8") -> str:
    """Read a Markdown file and render it to an HTML fragment."""
    return _DEFAULT.render(Path(path).read_text(encoding=encoding))
