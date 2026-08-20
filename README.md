# Projeto de Compiladores — Etapa 1: Lexer

Este repositório é o ponto de partida da primeira etapa do compilador de
MicroC. O trabalho deve ser realizado pelo grupo registrado no Canvas e no
GitHub Classroom. A entrega é feita integralmente por este repositório.

Leia o [enunciado completo](ENUNCIADO.pdf) antes de começar. A especificação da
linguagem disponibilizada pela disciplina é a referência normativa para os
programas MicroC.

## Estrutura do repositório

```text
.
├── .github/workflows/classroom.yml  # testes públicos no GitHub Actions
├── tests/test.py                    # testes públicos
├── ENUNCIADO.pdf                    # enunciado da etapa
├── Lexer.py                         # arquivo principal a implementar
├── runner.py                        # interface de linha de comando fornecida
├── test.microc                      # programa para experimentação
├── pyproject.toml                   # configuração do pytest
└── requirements-dev.txt             # dependências dos testes
```

Implemente o lexer em `Lexer.py`. É permitido criar módulos Python auxiliares,
mas as classes públicas, o `runner.py` e o formato de saída especificado não
devem ser alterados. Não adicione ao repositório ambientes virtuais, caches ou
arquivos gerados.

O grupo pode escolher livremente entre uma implementação manual, uma
implementação dirigida por tabela de autômato ou uma abordagem mista. O
esqueleto deliberadamente não fornece operações de avanço, estados ou tabela de
transições. Não é permitido usar SLY, PLY ou outro gerador de lexer, nem delegar
todo o reconhecimento a uma coleção global de expressões regulares.

Ao baixar o starter, os testes que exercitam o lexer falharão com
`NotImplementedError`. Isso é esperado: eles passarão progressivamente conforme
o reconhecimento for implementado.

## Preparação do ambiente

É necessário ter Python 3 instalado. A automação do repositório utiliza Python
3.12 como ambiente de referência.

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

No Windows PowerShell, ative o ambiente com:

```powershell
.venv\Scripts\Activate.ps1
```

## Execução

Para imprimir os tokens do programa de exemplo:

```sh
python runner.py test.microc
```

Para executar todos os testes públicos:

```sh
python -m pytest -q
```

O arquivo se chama `tests/test.py`; o `pyproject.toml` configura explicitamente
sua descoberta pelo pytest. Os testes públicos não constituem a correção
completa. A avaliação também utilizará testes privados compatíveis com o
contrato publicado no enunciado.

## Antes de entregar

- confirme que `python -m pytest -q` realmente coleta e executa os testes;
- confira a aba **Actions** depois de cada `push`;
- não altere os números e nomes de `TokenKind`;
- preserve as assinaturas e os campos públicos fornecidos; e
- verifique se o último commit está no repositório correto do grupo.
