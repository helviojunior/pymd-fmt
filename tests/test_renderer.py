"""Tests for the Markdown-to-HTML renderer."""

from __future__ import annotations

import pytest

from pymd_fmt import render


def test_empty_input():
    assert render("") == ""
    assert render(None) == ""  # type: ignore[arg-type]


@pytest.mark.parametrize("level", range(1, 7))
def test_headings(level):
    text = "#" * level + " Title"
    assert render(text) == f"<h{level}>Title</h{level}>"


def test_paragraph():
    assert render("Hello world.") == "<p>Hello world.</p>"


def test_paragraph_soft_breaks():
    assert render("line one\nline two") == "<p>line one<br>\nline two</p>"


def test_blank_line_splits_paragraphs():
    assert render("one\n\ntwo") == "<p>one</p>\n<p>two</p>"


def test_bold():
    assert render("a **b** c") == "<p>a <strong>b</strong> c</p>"


def test_italic_star_and_underscore():
    assert render("*em*") == "<p><em>em</em></p>"
    assert render("an _em_ word") == "<p>an <em>em</em> word</p>"


def test_underscore_leaves_snake_case_alone():
    assert render("call do_the_thing now") == "<p>call do_the_thing now</p>"


def test_inline_code():
    assert render("use `x = 1`") == "<p>use <code>x = 1</code></p>"


def test_link():
    assert render("[site](https://ex.com)") == '<p><a href="https://ex.com">site</a></p>'


def test_html_is_escaped():
    assert render("1 < 2 & 3 > 0") == "<p>1 &lt; 2 &amp; 3 &gt; 0</p>"


def test_fenced_code_block_with_language():
    out = render("```python\nx = 1\n```")
    assert out == '<pre><code class="language-python">x = 1</code></pre>'


def test_fenced_code_block_preserves_special_chars():
    out = render("```\nif a < b & c:\n```")
    assert out == "<pre><code>if a &lt; b &amp; c:</code></pre>"


def test_fenced_code_block_is_not_formatted():
    out = render("```\n**not bold**\n```")
    assert "<strong>" not in out
    assert "**not bold**" in out


def test_unordered_list():
    out = render("- a\n- b")
    assert out == "<ul>\n<li>a</li>\n<li>b</li>\n</ul>"


def test_ordered_list():
    out = render("1. a\n2. b")
    assert out == "<ol>\n<li>a</li>\n<li>b</li>\n</ol>"


def test_nested_list():
    out = render("- a\n  - b")
    assert out == "<ul>\n<li>a</li>\n<ul>\n<li>b</li>\n</ul>\n</ul>"


def test_blockquote():
    assert render("> quoted") == "<blockquote>\n<p>quoted</p>\n</blockquote>"


def test_blockquote_multiline():
    out = render("> one\n> two")
    assert out == "<blockquote>\n<p>one</p>\n<p>two</p>\n</blockquote>"


@pytest.mark.parametrize("kind", ["prompt-danger", "prompt-info", "prompt-tip", "prompt-warning"])
def test_prompt_callout(kind):
    out = render("> Meu texto bla bla bla\n{: ." + kind + " }")
    assert out == f'<blockquote class="{kind}">\n<p>Meu texto bla bla bla</p>\n</blockquote>'


def test_prompt_callout_multiline():
    out = render("> line one\n> line two\n{: .prompt-tip }")
    assert out == '<blockquote class="prompt-tip">\n<p>line one</p>\n<p>line two</p>\n</blockquote>'


def test_plain_blockquote_without_attr_has_no_class():
    assert render("> plain") == "<blockquote>\n<p>plain</p>\n</blockquote>"


def test_heading_inside_blockquote_becomes_heading():
    out = render("> ### Título\n> \n> corpo do aviso\n{: .prompt-warning }")
    assert out == (
        '<blockquote class="prompt-warning">\n<h3>Título</h3>\n<p>corpo do aviso</p>\n</blockquote>'
    )


def test_blockquote_blank_lines_are_dropped():
    out = render("> um\n> dois\n> \n> três")
    assert out == "<blockquote>\n<p>um</p>\n<p>dois</p>\n<p>três</p>\n</blockquote>"


def test_stray_attribute_line_is_dropped():
    assert render("just text\n{: .prompt-tip }") == "<p>just text</p>"


def test_consecutive_callouts():
    out = render("> a\n{: .prompt-info }\n\n> b\n{: .prompt-danger }")
    assert out == (
        '<blockquote class="prompt-info">\n<p>a</p>\n</blockquote>\n'
        '<blockquote class="prompt-danger">\n<p>b</p>\n</blockquote>'
    )


def test_mixed_document():
    text = "# Title\n\nIntro **para**.\n\n- one\n- two\n\n> note"
    out = render(text)
    assert "<h1>Title</h1>" in out
    assert "<strong>para</strong>" in out
    assert "<ul>\n<li>one</li>\n<li>two</li>\n</ul>" in out
    assert "<blockquote>\n<p>note</p>\n</blockquote>" in out
