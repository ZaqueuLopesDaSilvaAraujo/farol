# Changelog

## 1.3.0 — Triagem do segundo relato
- **Modo `augment`** e seleção explícita: `/fw-init --mode
  adopt|augment|bootstrap`; sem flag, o init avalia maturidade documental
  por sinais objetivos e RECOMENDA — em dúvida relevante, pergunta, nunca
  escolhe em silêncio.
- **Estados de confiança formalizados**: Confirmado (com evidência) /
  Inferido (nunca vira fato) / Não identificado (lacuna honesta) — no
  contrato do scout, nas regras da contextualização e no template do índice.
- **Orçamento de contexto**: bloco `contextBudget` no manifesto; a
  contextualização mede e grava o custo always-on (bytes ÷ 4) e corta antes
  de estourar o warning; `/fw-status` vigia e trata `hardLimit` como erro.
- **`/fw-status` expandido**: integridade do bloco gerenciado, recursos
  `fw-*` no disco, arquivos obrigatórios por modo, orçamento.
- **Release determinístico**: `scripts/release.py` empacota, valida nomes e
  comprimentos, extrai em diretório temporário e compara conteúdo byte a
  byte — falha o release em qualquer divergência (só arquivos entram no
  zip: diretório vazio nunca mais). `tests/PROTOCOL.md` documenta os 10
  cenários de validação reproduzíveis.
- Recusados conscientemente (ver discussão da triagem): templates por modo,
  scripts de instalação em shell, merge de 3 vias, taxonomia de 6 classes de
  tarefa e a redefinição de `/fw-update` (atualização de framework virá como
  plugin, sem colisão de nomes).

## 1.2.0 — Relato de campo (experimento em projeto real)
Correções derivadas do primeiro teste de campo — projeto pequeno com
contexto artesanal denso. Obrigado ao relato: cada item abaixo veio dele.
- **Zip corrigido**: a release 1.1.0 empacotava diretórios literais de
  expansão de chaves (quebrava Expand-Archive no Windows). Empacotamento
  agora é verificado programaticamente antes da release.
- **Princípios e restrições INVIOLÁVEIS**: nova seção obrigatória no índice
  para princípios de produto e restrições legais/compliance, com precedência
  máxima. A contextualização os caça ativamente na Rodada 0.
- **Precedência explícita**: documentação do time SEMPRE prevalece sobre o
  Farol em divergências; bloco gerenciado sem H1 duplicado.
- **Modo adopt**: com docs artesanais densos, o índice vira índice de
  ponteiros — apontar, nunca parafrasear (segunda fonte de verdade apodrece).
- **Detecção de stack**: recursiva (2 níveis), reconhece manifestos com
  nomes localizados (ex.: requisitos.txt) e identifica por conteúdo;
  subdiretório com manifesto = runtime do produto.
- **Sem chutes no índice**: tipo de aplicação só é preenchido se inequívoco;
  campos de comando são omitidos (nunca inventados) quando não se aplicam.
- **fw-scout e contextualize**: presença em disco ≠ presença no repo —
  caminhos gitignorados não sustentam afirmações sobre distribuição.
- **fw-status**: valida todos os ponteiros do índice (ponteiro morto em
  arquivo always-on = prioridade máxima) e a presença da seção de princípios.
- **INSTALL.md**: instrução explícita de abrir sessão NOVA (skills são
  descobertas no arranque) e seção "este framework é para o seu projeto?".
- **README**: seção "Quando usar — e quando não usar", incluindo a
  recomendação honesta de, às vezes, não usar.

## 1.1.0 — Marca
- Projeto batizado de **Farol**; banner e social preview em `assets/`;
  LICENSE (MIT), `.gitignore` e disclaimer de não afiliação no README.
  O prefixo `fw-` permanece (agora lê-se Farol Workspace) — zero renomeação
  de arquivos funcionais, zero breaking change.

## 1.1.0 — Auditoria de engenharia (correções pré-release)
- **INSTALL.md**: guia de instalação de 1 página para distribuição ao
  time, incluindo política de versionamento no git (commitar `.claude/` +
  `CLAUDE.md`; ignorar apenas `.claude/backups/`).
- **fw-guard.sh**: analisa apenas `tool_input.command` (jq → python3 →
  fallback), eliminando falsos positivos por grep no payload inteiro;
  novo `fw-guard-allow` (exceções do time, sobrevive a upgrades).
- **Hash portável**: inventário do manifesto agora usa `git hash-object`
  (idêntico em Linux/macOS/Windows) em contextualize, update e status.
- **fw-init**: ordem segura (índice-stub criado ANTES da mesclagem do
  CLAUDE.md — nenhum estado intermediário deixa import quebrado); novo campo
  `anchor_mode` (git | date).
- **Sem git**: degradação graciosa em fw-update (missões guiadas por área) e
  fw-status (idade por data).
- **Monorepos**: regra de escala explícita — índice sempre 1 linha por
  workspace; profundidade vai para modules/, teto de 120 linhas inviolável.
- **fw-freshness.sh** (SessionStart, opcional): aviso determinístico de
  contexto desatualizado (20+ commits desde a âncora).
- **Descrições dos subagents** enxugadas (~40%): menos imposto fixo de
  tokens em toda sessão.
- **memory.md**: regra de resolução de conflitos de merge (manter ambas;
  /fw-consolidate deduplica).

## 1.0.0
- Estrutura inicial: 3 subagents (fw-scout, fw-reviewer, fw-debugger),
  6 skills (init, contextualize, update, consolidate, decision, status),
  hook opcional fw-guard (PreToolUse), templates de contexto e manifesto.
