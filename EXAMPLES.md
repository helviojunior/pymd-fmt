# Exemplos de conversão — pymd-fmt

Este documento mostra cada conversão suportada pela biblioteca: o Markdown de
entrada e o HTML exatamente como é gerado por `pymd_fmt.render(...)`.

> Os blocos de HTML abaixo foram gerados automaticamente pelo renderer, então
> refletem fielmente a saída atual.
{: .prompt-info }

## Sumário

- [Títulos (h1–h6)](#títulos-h1h6)
- [Parágrafo](#parágrafo)
- [Quebra de linha suave](#quebra-de-linha-suave)
- [Negrito](#negrito)
- [Itálico (asterisco e underscore)](#itálico-asterisco-e-underscore)
- [Código inline](#código-inline)
- [Bloco de código com linguagem](#bloco-de-código-com-linguagem)
- [Links](#links)
- [Lista não-ordenada](#lista-não-ordenada)
- [Lista não-ordenada aninhada](#lista-não-ordenada-aninhada)
- [Lista ordenada](#lista-ordenada)
- [Citação (blockquote)](#citação-blockquote)
- [Callouts (estilo Chirpy)](#callouts-estilo-chirpy)
- [Escape de HTML](#escape-de-html)

---

## Títulos (h1–h6)

**Markdown:**

```markdown
# Título 1
## Título 2
### Título 3
#### Título 4
##### Título 5
###### Título 6
```

**HTML gerado:**

```html
<h1>Título 1</h1>
<h2>Título 2</h2>
<h3>Título 3</h3>
<h4>Título 4</h4>
<h5>Título 5</h5>
<h6>Título 6</h6>
```

---

## Parágrafo

Uma linha em branco separa parágrafos.

**Markdown:**

```markdown
Primeiro parágrafo.

Segundo parágrafo.
```

**HTML gerado:**

```html
<p>Primeiro parágrafo.</p>
<p>Segundo parágrafo.</p>
```

---

## Quebra de linha suave

Linhas consecutivas (sem linha em branco) viram quebras `<br>` dentro do mesmo
parágrafo.

**Markdown:**

```markdown
Linha um
Linha dois
```

**HTML gerado:**

```html
<p>Linha um<br>
Linha dois</p>
```

---

## Negrito

**Markdown:**

```markdown
Texto com **negrito** no meio.
```

**HTML gerado:**

```html
<p>Texto com <strong>negrito</strong> no meio.</p>
```

---

## Itálico (asterisco e underscore)

A forma com underscore exige limites de palavra, então `snake_case` fica intacto.

**Markdown:**

```markdown
Texto com *itálico* e _também assim_.
Mas do_the_thing fica intacto.
```

**HTML gerado:**

```html
<p>Texto com <em>itálico</em> e <em>também assim</em>.<br>
Mas do_the_thing fica intacto.</p>
```

---

## Código inline

**Markdown:**

```markdown
Use o comando `pip install pymd-fmt`.
```

**HTML gerado:**

```html
<p>Use o comando <code>pip install pymd-fmt</code>.</p>
```

---

## Bloco de código com linguagem

A linguagem após a cerca vira a classe `language-*`. O conteúdo não é
formatado e tem seus caracteres especiais escapados.

**Markdown:**

````markdown
```python
def soma(a, b):
    return a + b
```
````

**HTML gerado:**

```html
<pre><code class="language-python">def soma(a, b):
    return a + b</code></pre>
```

---

## Links

**Markdown:**

```markdown
Veja o [repositório](https://github.com/helviojunior/pymd-fmt).
```

**HTML gerado:**

```html
<p>Veja o <a href="https://github.com/helviojunior/pymd-fmt">repositório</a>.</p>
```

---

## Lista não-ordenada

Aceita os marcadores `-`, `*` e `+`.

**Markdown:**

```markdown
- Maçã
- Banana
- Laranja
```

**HTML gerado:**

```html
<ul>
<li>Maçã</li>
<li>Banana</li>
<li>Laranja</li>
</ul>
```

---

## Lista não-ordenada aninhada

O aninhamento é definido pela indentação.

**Markdown:**

```markdown
- Frutas
  - Maçã
  - Banana
- Legumes
```

**HTML gerado:**

```html
<ul>
<li>Frutas</li>
<ul>
<li>Maçã</li>
<li>Banana</li>
</ul>
<li>Legumes</li>
</ul>
```

---

## Lista ordenada

**Markdown:**

```markdown
1. Primeiro
2. Segundo
3. Terceiro
```

**HTML gerado:**

```html
<ol>
<li>Primeiro</li>
<li>Segundo</li>
<li>Terceiro</li>
</ol>
```

---

## Citação (blockquote)

**Markdown:**

```markdown
> Uma citação simples.
> Em duas linhas.
```

**HTML gerado:**

```html
<blockquote>
Uma citação simples.<br>
Em duas linhas.
</blockquote>
```

---

## Callouts (estilo Chirpy)

Uma linha de atributo `{: .classe }` logo abaixo de um blockquote aplica a
classe ao `<blockquote>`.

**Markdown:**

```markdown
> Dica útil para o usuário.
{: .prompt-tip }

> Informação relevante.
{: .prompt-info }

> Atenção com este ponto.
{: .prompt-warning }

> Cuidado, risco elevado.
{: .prompt-danger }
```

**HTML gerado:**

```html
<blockquote class="prompt-tip">
Dica útil para o usuário.
</blockquote>
<blockquote class="prompt-info">
Informação relevante.
</blockquote>
<blockquote class="prompt-warning">
Atenção com este ponto.
</blockquote>
<blockquote class="prompt-danger">
Cuidado, risco elevado.
</blockquote>
```

---

## Escape de HTML

Os caracteres `&`, `<` e `>` são escapados automaticamente.

**Markdown:**

```markdown
Comparação: 1 < 2 & 3 > 0, com <tag> literal.
```

**HTML gerado:**

```html
<p>Comparação: 1 &lt; 2 &amp; 3 &gt; 0, com &lt;tag&gt; literal.</p>
```
