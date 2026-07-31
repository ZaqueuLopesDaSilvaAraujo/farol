---
name: fw-contextualize
description: >
  Contextualiza o projeto: descobre stack, arquitetura, módulos, comandos,
  integrações, convenções e riscos, e preenche .claude/context/ lendo o
  mínimo necessário. Invocado explicitamente pelo usuário com /fw-contextualize
  após /fw-init. Nunca altera código-fonte.
disable-model-invocation: true
---

# /fw-contextualize — Contextualização do projeto

Objetivo: preencher `.claude/context/` com conhecimento **permanente e
verificado**, sob orçamento estrito de leitura. Nunca altere código-fonte.

## Orçamento de leitura (inegociável)

- Toda exploração de código acontece via subagent `fw-scout` (uma missão por
  rodada, com pergunta específica). A sessão principal lê apenas os resumos.
- Exclusões absolutas: lockfiles, `node_modules/`, `vendor/`, `dist/`,
  `build/`, `target/`, `.git/`, gerados, binários, assets, migrações antigas.
- Estratégia de amostragem: manifestos → entrypoints → estrutura de diretórios
  → UM arquivo exemplar por camada (um controller, um service, um teste...).
  Exemplar ensina o padrão; não é preciso ler os 40 irmãos.

## Rodada 0 — documentação do time (antes de qualquer scout)

Leia a documentação artesanal existente (AGENTS.md, CONTRIBUTING.md, README,
docs/, arquivos de decisão do time). Ela é FONTE de autoridade, não alvo de
paráfrase. Extraia dela duas coisas:
1. **Princípios e restrições invioláveis** — princípios de produto, restrições
   legais/compliance, regras "nunca faça X". Vão para a seção própria do
   índice, com fonte citada. Cace-os ativamente; é a seção mais importante.
2. **A ordem de autoridade** — quais docs mandam e em que ordem (seção
   "Fontes de autoridade" do índice).

**Modo adopt** (`adopt_mode: true` no manifesto, ou docs densos detectados):
o índice vira um ÍNDICE DE PONTEIROS — cada seção aponta para o doc do time
que a cobre (`ver AGENTS.md §X`), e você só ESCREVE o que for novo e
verificado (ausente dos docs). Duplicar documentação existente cria uma
segunda fonte de verdade que apodrece: é proibido.

## Rodadas de descoberta (missões do fw-scout)

0. Confirme/corrija na primeira missão qualquer campo `a confirmar` deixado
   pelo /fw-init (especialmente o tipo de aplicação).
1. **Panorama**: árvore de diretórios (2 níveis), entrypoints, workspaces.
   → confirma tipo de aplicação e mapa de alto nível.
2. **Comandos**: scripts do manifesto, Makefile/justfile, CI. Marque cada
   comando como verificado (aparece em script/CI) ou inferido.
3. **Arquitetura**: camadas, fluxo de uma requisição/ação típica, fronteiras
   entre módulos, padrões visíveis (via exemplares).
4. **Integrações e riscos**: bancos, filas, APIs externas, variáveis de
   ambiente esperadas (nomes, nunca valores), módulos críticos/sensíveis.
5. **Convenções**: naming, organização de testes, estilo de erro/log,
   linters e formatters configurados.

Se o resultado de uma rodada já responde a próxima, pule-a. Projetos pequenos
podem resolver tudo em 2 missões.

## Escrita do contexto (uma responsabilidade por arquivo)

Use os templates em `.claude/context/_templates/`:

- `index.md` → identidade, stack, comandos, mapa de módulos (1 linha cada),
  tabela "Carregue quando". Teto: 120 linhas. É o ÚNICO arquivo always-on.
  **Regra de escala (monorepo/microsserviços)**: no índice, 1 linha por
  workspace/serviço, sem exceção; o detalhe de cada workspace crítico vai em
  `modules/<workspace>.md`. O teto do índice nunca é estourado — profundidade
  vai para baixo (modules/), não para o arquivo always-on.
- `architecture.md` → visão de camadas, fluxo típico, fronteiras. Teto: 120 linhas.
- `conventions.md` → regras de código do time, com exemplos mínimos. Teto: 100 linhas.
- `modules/<nome>.md` → SOMENTE para módulos críticos ou não óbvios (regra:
  se um dev sênior entenderia o módulo em 5 min olhando o código, não precisa
  de arquivo). Teto: 60 linhas cada.

Regras de conteúdo: fatos, não prosa; nada duplicado entre arquivos NEM com
docs do time (apontar > repetir); incertezas marcadas como `(inferido)`;
nunca colar documentação de dependências. Caminhos listados no `.gitignore`
não sustentam afirmações sobre o repositório ou distribuição — presença em
disco ≠ presença no repo; marque fatos desses caminhos como `(local, fora
do repo)`. Nunca deixe o índice apontar para um arquivo que você não criou:
ao final, verifique cada alvo da tabela "Carregue quando" e da lista de
módulos.

## Finalização

1. Atualize `manifest.json`: `contextualized_at`; se `anchor_mode` = "git",
   `anchor_commit` = `git rev-parse HEAD`; e `inventory` com
   `{"arquivo": {"hash": "<git hash-object arquivo>"}}` para cada arquivo de
   contexto. Use SEMPRE `git hash-object` (determinístico e idêntico em
   qualquer OS — nunca sha1sum/shasum). Sem git, deixe `inventory` vazio.
2. Peça ao usuário para validar 3–5 fatos-chave descobertos (comandos e
   arquitetura). Corrija o que ele apontar.
3. Relatório final em até 15 linhas: o que foi documentado, incertezas
   restantes, e lembrete de `/fw-update` após mudanças relevantes.
