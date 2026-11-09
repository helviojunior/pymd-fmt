"""pymd-fmt — parse Markdown and render it to HTML tags.

Public API::

    from pymd_fmt import render, render_file

    html = render("# Hello\\n\\nSome **bold** text.")
"""

from __future__ import annotations

from pymd_fmt.renderer import MarkdownRenderer, render, render_file

__all__ = ["MarkdownRenderer", "render", "render_file"]
__version__ = "0.1.0"
