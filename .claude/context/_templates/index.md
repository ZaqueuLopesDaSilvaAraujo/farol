# {NOME_DO_PROJETO} — Índice de Contexto

<!-- ÚNICO arquivo always-on. Teto: 120 linhas. Fatos, não prosa.
     Este arquivo APONTA para conhecimento; não o repete. -->

## Identidade
- **O que é**: {1 linha: propósito do sistema}
- **Tipo**: {API | web | desktop | mobile | lib | CLI | monorepo | microsserviços}
- **Domínio**: {1 linha}

## Stack
- Linguagem(ns): {…}  · Framework(s): {…}
- Gerenciador de pacotes: {…} · Banco/infra: {…}

## Comandos essenciais
<!-- marque (inferido) até verificar -->
- Instalar deps: `{…}`
- Rodar: `{…}`
- Testar: `{…}`
- Lint/format: `{…}`
- Build: `{…}`

## Mapa do projeto
<!-- 1 linha por área. Detalhe vai em modules/<nome>.md, se crítico.
     Monorepo/microsserviços: 1 linha por workspace/serviço, SEM exceção;
     profundidade vai para modules/<workspace>.md, nunca para este arquivo. -->
- `{caminho/}` — {o que é}

## Módulos críticos
- {nome} → ver `modules/{nome}.md`

## Riscos e limitações
- {1 linha por risco: módulo sensível, dívida conhecida, restrição}

## Carregue quando (carga sob demanda)
| Arquivo | Carregue quando a tarefa envolver |
|---|---|
| `architecture.md` | design, novo módulo, mudança estrutural, dúvida de fluxo |
| `conventions.md` | escrever ou revisar código |
| `modules/{nome}.md` | mexer no módulo {nome} |
| `decisions/` | questionar/alterar uma decisão existente (leia só o ADR relevante) |
| `memory.md` | início de tarefa não trivial (arquivo curto) |
