# Hooks do framework

## Filosofia: hooks só onde determinismo é indispensável

Regras declarativas (CLAUDE.md) dependem do modelo obedecê-las. Dois casos
merecem garantia mecânica; todo o resto fica declarativo de propósito:

1. **Segurança** (`fw-guard.sh`, PreToolUse): bloqueia comandos destrutivos
   antes de executarem, sempre.
2. **Frescor do contexto** (`fw-freshness.sh`, SessionStart): injeta 1 linha
   de aviso quando há 20+ commits desde a última contextualização — a
   detecção de "contexto que mente" não pode depender de o modelo lembrar.

NÃO usamos hooks para injetar contexto de projeto (redundante com o índice
always-on) nem para atualizar memória automaticamente (mudança silenciosa em
base de conhecimento é corrupção difícil de detectar; preferimos as skills
explícitas /fw-update e /fw-consolidate).

## fw-guard.sh (opcional — requer bash; Windows: Git Bash/WSL)

- Analisa APENAS `tool_input.command` (via `jq`, ou `python3`, ou fallback
  bruto). Instale `jq` para precisão máxima.
- Exceções do time: `.claude/hooks/fw-guard-allow` (1 regex por linha).
  Esse arquivo é do TIME e sobrevive a upgrades — nunca edite o script.
- Comando bloqueado + autorização do usuário = o usuário executa manualmente
  ou adiciona exceção. O hook não tem como saber o que foi autorizado na
  conversa; por isso bloqueia apenas o irreversível/raro (push, rm -rf,
  DROP...), não operações rotineiras como commit.

## Ativação

1. `chmod +x .claude/hooks/fw-guard.sh .claude/hooks/fw-freshness.sh`
2. Mescle em `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [ { "type": "command", "command": "bash .claude/hooks/fw-guard.sh" } ] }
    ],
    "SessionStart": [
      { "hooks": [ { "type": "command", "command": "bash .claude/hooks/fw-freshness.sh" } ] }
    ]
  }
}
```

3. Ajuste `BLOCK_PATTERNS` do guard à realidade do time (deploys, CLIs de
   infra, migrações) — ou, preferível, mantenha o script intacto e use
   `fw-guard-allow` para exceções.

Sem os hooks, as proibições continuam como regra declarativa no CLAUDE.md —
apenas sem garantia mecânica.
