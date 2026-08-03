# Políticas do projeto (Farol)

## a. Fluxo de versionamento do contexto
(não declarado — comportamento padrão)

## b. O que da pasta `.claude/` entra no Git
(não declarado — padrão)

## c. Gatilho de atualização do índice
(não declarado — padrão: sugerido após mudança estrutural)

## d. Orçamento de contexto — política (números NÃO)
Recalibrações de `bytesPerToken` nunca são silenciosas: exigem linha na `memory.md` com data, valor anterior, novo valor e método de medição.

## e. Arquivos ainda não mapeados
(não declarado — padrão: sob demanda)

## f. Orçamento de execução — política (números NÃO)
Exceder `hardMaxAgents`, ativar paralelismo fora do padrão ou desativar `stopWhenEvidenceIsSufficient` exige justificativa registrada na resposta da tarefa — nunca silenciosa.

## g. Política de modelos por categoria (aliases NÃO vivem fixos aqui)
(não declarado — padrão: `inherit` em todos os agentes; nenhuma categoria fixada por este framework)

## h. Telemetria local (opcional) — schema NÃO vive fixo aqui
(não declarado — padrão: `enabled: false` no manifesto; nenhuma métrica registrada)

Campos permitidos por linha, quando habilitada: id da tarefa, classificação T0–T3, agentes acionados, modelo/categoria, chamadas de ferramentas, arquivos lidos/relidos, documentos de contexto carregados, workspace reutilizado, duração, resultado, causa confirmada, testes aprovados, atualização de contexto realizada.

Campos PROIBIDOS, sempre, mesmo habilitada: prompts completos, código-fonte, segredos, tokens, credenciais, informações pessoais, conteúdo integral de arquivo. Um campo proibido gravado é falha de política, não detalhe de implementação.

Cobertura: tarefas T2/T3 registram via o agente `fw-*` acionado (regra carregada sob demanda); tarefas T0/T1 só registram se a linha condicional do `CLAUDE.md.ccf` estiver presente — habilitar a telemetria sem essa linha produz cobertura parcial, não erro silencioso (ver `tests/PROTOCOL.md`).

Armazenamento é local por padrão; recomenda-se adicionar o caminho ao `.gitignore` — é registro operacional, não conhecimento de projeto.

## Defasagem no arranque (fw-freshness)

`freshness_limiar: 20`