# Convenções

<!-- Carga sob demanda ao escrever/revisar código. Teto: 100 linhas.
     Só regras DESTE projeto que o Claude não adivinharia sozinho.
     Não repita o óbvio da linguagem/framework. -->

## Nomenclatura
- {ex.: arquivos em kebab-case; classes de serviço com sufixo Service}

## Organização
- {ex.: um módulo por feature em src/features/<nome>; testes ao lado do código}

## Erros e logging
- {ex.: nunca lançar erro genérico; usar AppError com código; log estruturado}

## Testes
- Framework: {…} · Padrão de nome: {…}
- {ex.: unidade para domínio, integração para adapters; sem mock de banco em X}

## Estilo verificado por ferramenta
- {linter/formatter}: config em `{arquivo}` — não discutir estilo coberto por ele

## Exemplos canônicos
<!-- aponte, não copie -->
- Endpoint bem feito: `{caminho/arquivo}` · Teste bem feito: `{caminho/arquivo}`
