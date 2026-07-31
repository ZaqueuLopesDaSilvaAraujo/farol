#!/usr/bin/env bash
# fw-freshness.sh — Hook SessionStart opcional do Farol (v2.0.2)
# Injeta 1 linha de aviso quando o contexto está velho. Custo ~0 tokens.
MANIFEST=".claude/context/manifest.json"
[ -f "$MANIFEST" ] || exit 0
command -v git >/dev/null 2>&1 || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

ANCHOR="$(grep -o '"anchor_commit"[[:space:]]*:[[:space:]]*"[^"]*"' "$MANIFEST" | sed 's/.*"\([^"]*\)"$/\1/')"
[ -z "$ANCHOR" ] || [ "$ANCHOR" = "null" ] && exit 0
git cat-file -e "$ANCHOR" 2>/dev/null || { echo "fw: âncora de contexto inválida (rebase?). Rode /fw-update."; exit 0; }

N="$(git rev-list --count "$ANCHOR"..HEAD 2>/dev/null || echo 0)"
if [ "${N:-0}" -ge 20 ]; then
  echo "fw: contexto desatualizado ($N commits desde a última contextualização). Recomende /fw-update antes de tarefas grandes."
fi
exit 0
