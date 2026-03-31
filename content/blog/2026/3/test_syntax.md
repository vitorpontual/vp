# Test post with syntax highlighting

date: Posted: Mar 30, 2026

```python
def sum(a, b):
	return a + b
>> Output 5
```

Fala pessaol primeira feature que adiciono no meu blog, é o blockcode com highlight syntax.
Utilizei o Prismjs para que já tem o script pronto e adicionei algumas linugagens que
irei utilizar eventualmente.

São eles:

- Pyhton
- Go
- Bash
- Javascript
- C

O site é bem simples [PrismJs](https://prismjs.com/), mas a ferramenta é sensacional, uma instalação bem fácil
plug and play basicamente.

## Aprendizado

O que eu tirei de aprendizado com a construção desse SSG ( Static Site Generator ). 

1. Processamento de Markdown

- Parse de markdwon par HTML;
- Identificação de diferentes tipos de blocos ( heading, code, quote, list);
- Processamento de inline ( **bold**, __italic__, `code`, "![]()", "[]()");
- Extração de metadados (títulos, data, tags);

2. Sistema de Blocs;

```python
- BlockType Enum (PARAGRAPH, HEADING, CODE, QUOTE, OLIST, ULIST, NAV)
- Detecção inteligente de tipos de bloco
- Conversão de cada bloco para HTML específico
```

3. Geração de Páginas 

- Estrutura recursiva para processar arquivos
- Templates com placeholders ({{ Title }}, {{ Content }})

4. **Syntax Highlighting** 

- Integração com Prism.js
- Suporte a múltiplas linguagens ( Python, Go, Bash, C)


5. Fluxo de Processamento

```bash
Markdown -> Blocks -> BlockTypes -> Node HTML -> Pages HTML
```


## Conclusão

Construir um SSG do zero é uma das melhores maneiras de aprender desenvolvimento web. Você dominou conceitos de:

**Backend**: Processamento de arquivos, parsing, geração de HTML

**Frontend**: HTML, CSS, JavaScript, design responsivo

**DevOps**: Build, deploy, estrutura de projeto

**Arquitetura**: Separação de preocupações, padrões de projeto


