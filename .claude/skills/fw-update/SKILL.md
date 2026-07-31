---
name: fw-update
description: >
  Atualiza o contexto do projeto de forma incremental, lendo apenas o que
  mudou desde a última contextualização (ancorado em git). Use quando o
  usuário pedir /fw-update, ou sugira quando /fw-status indicar contexto
  desatualizado. Nunca reconstrói do zero, nunca altera código.
disable-model-invocation: true
---

# /fw-update — Atualização incremental do contexto

Princípio: o git diz o que mudou; só isso é revisitado. Conhecimento anterior
é preservado — atualização é cirurgia, não reconstrução.

## Procedimento

1. Leia o manifesto (`.claude/context/manifest.json`).
   - `contextualized_at` nulo → pare e instrua rodar `/fw-contextualize`.
   - `anchor_mode` = "date" (projeto sem git) → incremental por diff é
     impossível: pergunte ao usuário QUAIS áreas mudaram e despache missões
     do fw-scout restritas a elas; pule os passos 2–3.
   - `anchor_commit` não existe mais (rebase/force) → fallback: data
     `contextualized_at` com `git log --since`.
2. Rode `git diff --stat <anchor_commit>..HEAD` e
   `git log --oneline <anchor_commit>..HEAD | head -30`.
   - Diff vazio → atualize a âncora, informe "contexto em dia", fim.
3. Classifique as mudanças por área/módulo. Ignore mudanças em arquivos das
   listas de exclusão (lockfiles, gerados, assets).
4. Para cada área com mudança **estrutural** (novos diretórios, novos
   entrypoints, dependência nova no manifesto, módulo renomeado), despache UMA
   missão do `fw-scout` restrita àquela área. Mudanças apenas internas a
   arquivos já documentados normalmente não exigem leitura — julgue pelo stat.
5. Aplique edições mínimas nos arquivos de contexto afetados (respeitando os
   tetos de linhas). Nunca apague seções válidas; se algo deixou de existir,
   remova a linha correspondente e, se a remoção tiver justificativa
   relevante, registre via /fw-decision.
6. Atualize `manifest.json`: nova `anchor_commit` (se `anchor_mode` = "git"),
   `contextualized_at`, e hashes do `inventory` para os arquivos alterados —
   sempre via `git hash-object` (nunca sha1sum/shasum).
7. Relatório em até 10 linhas: commits cobertos, arquivos de contexto
   alterados, o que foi considerado irrelevante.
