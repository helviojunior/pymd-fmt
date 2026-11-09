# pymd-fmt

Uma pequena biblioteca Python para fazer o parsing de Markdown e transformá-lo
em tags HTML. Sem dependências — apenas a biblioteca padrão.

A lógica do parser gera **tags HTML semânticas
limpas** (sem classes de CSS), tornando a saída reutilizável em qualquer lugar.

## Instalação

```bash
pip install pymd-fmt
```

Durante o desenvolvimento, a partir do repositório:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Uso

```python
from pymd_fmt import render, render_file

html = render("# Olá\n\nUm texto com **negrito** e `código`.")
print(html)
# <h1>Olá</h1>
# <p>Um texto com <strong>negrito</strong> e <code>código</code>.</p>

# Ou a partir de um arquivo:
html = render_file("documento.md")
```

Para configuração/extensão, use a classe diretamente:

```python
from pymd_fmt import MarkdownRenderer

renderer = MarkdownRenderer()
html = renderer.render("...")
```

## Elementos suportados

| Markdown                         | HTML                                      |
| -------------------------------- | ----------------------------------------- |
| `# …` até `###### …`             | `<h1>` … `<h6>`                           |
| Parágrafos / quebras de linha    | `<p>` com `<br>` para quebras suaves      |
| `**texto**`                      | `<strong>`                                |
| `*texto*` / `_texto_`            | `<em>` (preserva `snake_case`)            |
| `` `código` ``                   | `<code>`                                  |
| ` ```lang ` … ` ``` `            | `<pre><code class="language-lang">`       |
| `[texto](url)`                   | `<a href="url">`                          |
| `- item` / `* item` / `+ item`   | `<ul><li>` (aninhamento por indentação)   |
| `1. item`                        | `<ol><li>` (aninhamento por indentação)   |
| `> citação`                      | `<blockquote>`                            |
| `> …` + `{: .prompt-tip }`       | `<blockquote class="prompt-tip">` (callout)|

Os caracteres `&`, `<` e `>` são escapados automaticamente, inclusive dentro de
blocos de código.

### Callouts (estilo Chirpy/Jekyll)

Uma linha de atributo `{: .classe }` logo abaixo de um blockquote aplica a
classe ao `<blockquote>`, permitindo os callouts do tema Chirpy:

```markdown
> Cuidado com isto.
{: .prompt-danger }
```

```html
<blockquote class="prompt-danger">
Cuidado com isto.
</blockquote>
```

Funciona com `.prompt-tip`, `.prompt-info`, `.prompt-warning`, `.prompt-danger`
ou qualquer outra classe (inclusive várias: `{: .prompt-tip .destaque }`).

## Desenvolvimento

```bash
pytest        # roda os testes
ruff check .  # lint
ruff format . # formatação
```

## Licença

BSD 2-Clause
