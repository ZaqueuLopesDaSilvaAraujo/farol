#!/usr/bin/env bash
# fw-guard.sh — Hook PreToolUse (Bash) do Farol (v2.0.2)
# Bloqueia deterministicamente comandos destrutivos. exit 2 = bloquear.
# Analisa APENAS o campo tool_input.command (não o payload inteiro).
# Exceções do time: .claude/hooks/fw-guard-allow (1 regex por linha) —
# arquivo do TIME, preservado em upgrades.

INPUT="$(cat)"

extract_command() {
  if command -v jq >/dev/null 2>&1; then
    printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null
    return
  fi
  if command -v python3 >/dev/null 2>&1; then
    printf '%s' "$INPUT" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null
    return
  fi
  # Sem jq/python3: analisa o payload inteiro (pode gerar falso positivo,
  # nunca falso negativo). Instale jq para precisão total.
  printf '%s' "$INPUT"
}

CMD="$(extract_command | tr '\n' ' ')"
[ -z "$CMD" ] && exit 0

# Exceções explícitas do time (avaliadas antes dos bloqueios)
ALLOW_FILE="$(dirname "$0")/fw-guard-allow"
if [ -f "$ALLOW_FILE" ]; then
  while IFS= read -r allow; do
    case "$allow" in ''|\#*) continue ;; esac
    printf '%s' "$CMD" | grep -qiE "$allow" && exit 0
  done < "$ALLOW_FILE"
fi

BLOCK_PATTERNS=(
  'rm[[:space:]]+-[a-zA-Z]*r[a-zA-Z]*f'            # rm -rf e variantes
  '(^|[;&|[:space:]])git[[:space:]]+push'          # qualquer push (inclui --force)
  'git[[:space:]]+reset[[:space:]]+--hard'
  'git[[:space:]]+clean[[:space:]]+-[a-zA-Z]*f'
  'DROP[[:space:]]+(TABLE|DATABASE|SCHEMA)'
  'TRUNCATE[[:space:]]+TABLE'
  'mkfs|dd[[:space:]]+if='
  'chmod[[:space:]]+-R[[:space:]]+777'
  ':\(\)\{[[:space:]]*:\|:&[[:space:]]*\};:'       # forkbomb
)

for p in "${BLOCK_PATTERNS[@]}"; do
  if printf '%s' "$CMD" | grep -qiE "$p"; then
    echo "fw-guard: comando bloqueado (padrão: $p)." >&2
    echo "Se o usuário autorizou explicitamente, ele deve executar manualmente" >&2
    echo "ou adicionar uma exceção em .claude/hooks/fw-guard-allow." >&2
    exit 2
  fi
done

exit 0
