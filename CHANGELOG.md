# Changelog

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
