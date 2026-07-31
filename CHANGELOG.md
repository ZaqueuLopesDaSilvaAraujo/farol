# Changelog

## 2.0.2 — Quinto relato de campo (parcial: canal de update)
- **Canal de atualização consertado** (achado nº 1): a v2.0.1 bumpou tudo
  MENOS `.claude-plugin/plugin.json` e `marketplace.json` — os arquivos que
  o Claude Code lê para decidir updates. `claude plugin update` respondia
  "already at latest (2.0.0)" e ninguém recebia as correções. Manifestos
  agora em 2.0.2.
- **Mecanização da classe do bug**: `release.py` valida consistência de
  versão em todas as fontes (manifestos, marcador do bloco, títulos,
  template do init) e FALHA a release em divergência — o equivalente ao
  `claude plugin tag`, que não rodávamos.
- **Fonte única de versão** (achado nº 3): o template de manifesto do
  `/farol:init` não carrega mais número literal; a versão vem sempre de
  `plugin.json`.
- **CRLF residual** (achado nº 4): hooks tocados de propósito para forçar
  re-extração com LF em clones antigos; nota de `git add --renormalize` no
  UPGRADE e `sed -i 's/\r$//'` no passo de cópia dos hooks no Windows.
- Confirmado pelo relato: modo atualização do init e detecção de ponteiro
  morto funcionaram exatamente como especificados ao vivo.

## 2.0.1 — Quarto relato de campo
- **Migração não falha mais em silêncio** (o bug mais sério do relato):
  `/farol:init` ganhou modo atualização — compara a versão do marcador
  `ccf:managed-*` com a do plugin, substitui o bloco gerenciado e oferece
  refrescar os templates do projeto (única exceção à não-sobrescrita, com
  backup e comparação que ignora CRLF). UPGRADE.md com a migração completa,
  incluindo sobras e a armadilha do CRLF no Windows.
- **`/farol:status` vigia eras**: checagem 9 compara versão do bloco vs
  plugin (divergência = ERRO); nova checagem 13 detecta manifesto 1.x
  (`adopt_mode`) e templates ensinando comandos `/fw-*` mortos.
- **`.gitattributes`** força LF em `*.sh`/`*.py` — mata o
  `bad interpreter: ^M` do fw-guard sob Git Bash na origem.
- **Custo global documentado com franqueza**: ~0,9k tokens em toda sessão
  da máquina, mesmo sem Farol no projeto; prática do `/plugin disable`
  registrada. CLI (`claude plugin …`) documentado para agentes.
- **Regra de modo refinada**: dimensão "princípios de produto" pesa
  separadamente; adopt com invioláveis vazios sugere reavaliar (init,
  contextualize e status).

## 2.0.0 — Plugin do Claude Code (breaking)
- **Distribuição por plugin**: instala com 2 comandos
  (`/plugin marketplace add ZaqueuLopesDaSilvaAraujo/farol` +
  `/plugin install farol@farol`), vale para todos os projetos da máquina e
  atualiza nativamente. O conceito fundador vira infraestrutura:
  inteligência no plugin (uma vez), contexto em cada projeto.
- **BREAKING — comandos renomeados**: `/fw-<skill>` → `/farol:<skill>`; o
  namespace do plugin absorve o antigo prefixo. Agents mantêm os nomes
  (`fw-scout`, `fw-reviewer`, `fw-debugger`).
- **BREAKING — layout**: `skills/`, `agents/`, `hooks/`, `templates/` na
  raiz do plugin; o zip vira instalação LOCAL de plugin
  (`/plugin install ~/farol`), não mais extração na raiz do projeto.
- Templates copiados para `.claude/context/_templates/` do projeto no
  `/farol:init` (customizáveis pelo time); fontes via `${CLAUDE_PLUGIN_ROOT}`.
- Hooks de segurança seguem **opt-in por projeto** — o plugin não os
  auto-ativa, de propósito.
- Migração da 1.x em `UPGRADE.md`.

## 1.3.1 — Terceiro relato de campo
- **Razão bytes/token calibrável** (`contextBudget.bytesPerToken`): bytes ÷ 4
  subestimava pt-BR em ~55% (medição de campo: 2,59 B/token) e o guarda dava
  luz verde a índice no limite. Agora: calibração contra documento conhecido
  no /fw-init, ou escolha por idioma (pt-BR ≈ 2,6 · en ≈ 4,0 · misto ≈ 3,0);
  na dúvida, o valor MENOR — guarda superestima, nunca subestima. O
  /fw-status alerta razão suspeita.
- **Adopt promete fidelidade, não economia**: medido em campo, o modo adopt
  sobre doc madura CUSTA MAIS que a paráfrase da v1.1.0 (+princípios
  invioláveis, +precedência) e entrega em troca lacunas e divergências
  verificadas — "o que é verdade e não está na doc". Toda a documentação
  foi corrigida para esse argumento; a previsão anterior de "acréscimo
  mínimo" estava errada e fica aqui registrada como tal.

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
