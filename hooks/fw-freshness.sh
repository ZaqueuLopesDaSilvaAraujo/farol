#!/usr/bin/env bash
# fw-freshness.sh — Hook SessionStart opcional do Farol (v2.1.0)
# Injeta 1 linha de aviso quando o contexto está velho. Custo ~0 tokens.
MANIFEST=".claude/context/manifest.json"
[ -f "$MANIFEST" ] || exit 0
command -v git >/dev/null 2>&1 || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

ANCHOR="$(grep -o '"anchor_commit"[[:space:]]*:[[:space:]]*"[^"]*"' "$MANIFEST" | sed 's/.*"\([^"]*\)"$/\1/')"
[ -z "$ANCHOR" ] || [ "$ANCHOR" = "null" ] && exit 0
git cat-file -e "$ANCHOR" 2>/dev/null || { echo "fw: âncora de contexto inválida (rebase?). Rode /farol:update."; exit 0; }

N="$(git rev-list --count "$ANCHOR"..HEAD 2>/dev/null || echo 0)"
LIMIAR="${FAROL_FRESHNESS_LIMIAR:-}"
if [ -z "$LIMIAR" ] && [ -f .claude/context/policies.md ]; then
  LIMIAR="$(grep -oE 'freshness_limiar:[[:space:]]*[0-9]+' .claude/context/policies.md | grep -oE '[0-9]+' | head -1)"
fi
LIMIAR="${LIMIAR:-20}"
if [ "${N:-0}" -ge "$LIMIAR" ]; then
  echo "fw: contexto desatualizado ($N commits desde a última contextualização). Recomende /farol:update antes de tarefas grandes."
fi
exit 0
