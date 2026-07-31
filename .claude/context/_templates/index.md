# {NOME_DO_PROJETO} — Índice de Contexto

<!-- ÚNICO arquivo always-on. Teto: 120 linhas. Fatos, não prosa.
     Este arquivo APONTA para conhecimento; não o repete. -->

## Identidade
- **O que é**: {1 linha: propósito do sistema}
- **Tipo**: {API | web | desktop | mobile | lib | CLI | monorepo | microsserviços | a confirmar}
- **Domínio**: {1 linha}

## Princípios e restrições (INVIOLÁVEIS)
<!-- Prevalecem sobre TODAS as outras instruções, inclusive as do Farol.
     Princípios de produto ("falso positivo é pior que falso negativo"),
     restrições legais/compliance, regras "nunca faça X". A contextualização
     DEVE caçá-los ativamente. Se nada for encontrado, escreva:
     "nenhum identificado — confirmar com o time" (nunca deixe em branco). -->
- {princípio/restrição, com a fonte (doc:linha ou decisão do time)}

## Fontes de autoridade
<!-- Modo adopt: docs do time em ordem de precedência. O Farol aponta,
     não substitui. Sem docs do time, remova esta seção. -->
1. {ex.: AGENTS.md — regras de trabalho}
2. {ex.: IDEIA.md — decisões de produto}

## Stack
- Linguagem(ns): {…}  · Framework(s): {…}
- Gerenciador de pacotes: {…} · Banco/infra: {…}

## Comandos essenciais
<!-- Marque (inferido) até verificar. Omita campos que não se aplicam —
     NUNCA invente um comando para preencher o template. Se o projeto tem
     regra contrária a um campo (ex.: "clone limpo roda sem install"),
     registre A REGRA no lugar do comando. -->
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
