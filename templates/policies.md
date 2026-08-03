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
Padrão do próprio framework (confirmado: Claude Code suporta `model:` no frontmatter de agentes, inclusive os de plugin): `fw-scout` roda em `economical` (`model: haiku`); `fw-debugger` e `fw-reviewer` rodam em `balanced` (`model: sonnet`). Para sobrescrever, copie o agente para `.claude/agents/` do projeto e edite o `model:` lá — nunca edite os agentes do plugin diretamente.

Categorias de referência (nomes conceituais, não aliases de modelo — o alias real depende da versão/plano do Claude Code instalado):
- `economical`: localização, inventário, busca, classificação, leitura simples, síntese objetiva.
- `balanced`: implementação, depuração normal, testes, revisão comum, refatoração — categoria padrão do framework para depuração e revisão.
- `deepReasoning` (`deep-reasoning`): arquitetura complexa, investigação ambígua, decisões de alto impacto, segurança crítica — só com justificativa explícita na resposta da tarefa; nenhum agente do framework fixa esta categoria por padrão.

`modelPolicy.declared`/`categories` no manifesto nascem vazios (`false`/`null`) e servem para o TIME registrar, para fins de auditoria, customizações do projeto além do padrão do framework — preencher o manifesto não altera o modelo real sozinho; a edição de `model:` no frontmatter do agente correspondente é sempre manual e distinta. Antes de declarar `modelPolicy.declared: true`, confirme via `/farol:status` (verificação 16) que o agente correspondente realmente tem `model:` fixado.

## h. Telemetria local (opcional) — schema NÃO vive fixo aqui
(não declarado — padrão: `enabled: false` no manifesto; nenhuma métrica registrada)

Princípio: **código conta o que é contável; o modelo só declara o que só ele sabe.** Quem grava é o hook `fw-telemetry.py`, nunca o modelo e nunca um agente. O único campo de origem semântica é a classificação T0–T3; sua ausência degrada a linha (`task_class: null`), jamais a suprime.

Campos permitidos por linha, quando habilitada: id da tarefa, classificação T0–T3, agentes acionados, modelo/categoria, chamadas de ferramentas (com discriminação por ferramenta), arquivos lidos/relidos, documentos de contexto carregados, workspace reutilizado, duração, resultado, testes aprovados, atualização de contexto realizada, `session_id`, versão do framework e versão do schema (`v`) — os três últimos são o que torna possível comparar execuções entre sessões e entre versões.

Campos PROIBIDOS, sempre, mesmo habilitada: prompts completos, código-fonte, segredos, tokens, credenciais, informações pessoais, conteúdo integral de arquivo. Um campo proibido gravado é falha de política, não detalhe de implementação.

Caminhos de arquivo: por padrão arquivos fora de `.claude/context/` entram como hash (conta releitura sem registrar o caminho). `telemetry.recordFilePaths: true` no manifesto troca isso por caminhos relativos — opt-in explícito do time. Arquivos do próprio contexto viajam pelo nome: são do framework e é a métrica que justifica sua existência.

Classificação T0–T3: quando a telemetria está ligada, o hook injeta (via `UserPromptSubmit`) a instrução para o modelo marcar a classe na resposta, e o consolidador extrai **apenas** o token casado pela regex `fw:class=(T[0-3])` do `last_assistant_message` do evento `Stop` — que contém só o texto final do assistente, **nunca o prompt do usuário**. O transcript é fallback, e mesmo ali só o token sobrevive. Desligada, nada é injetado — **custo zero no always-on**.

Atribuição por agente: eventos de ferramenta disparados dentro de um subagente carregam `agent_type`, então `tools_by_agent` credita cada chamada a quem a fez. Sem isso, o total da tarefa seria creditado a todos os agentes acionados e qualquer comparação sairia inflada.

Cobertura: com os três hooks instalados (`UserPromptSubmit`, `PostToolUse`, `Stop`), **todas** as classificações registram, inclusive T0 sem nenhuma chamada de ferramenta. Sem o hook instalado, nada é registrado — telemetria não tem caminho alternativo pelo modelo, por decisão de projeto (registro não verificável é pior que ausência de registro). O relatório sempre exibe a cobertura de classificação declarada; lacuna se reporta, não se esconde.

Armazenamento é local por padrão; recomenda-se adicionar o caminho ao `.gitignore` — é registro operacional, não conhecimento de projeto. Retenção e teto de linhas vivem no manifesto (`retainDays`, `maxLines`), nunca aqui.

## Defasagem no arranque (fw-freshness)

`freshness_limiar: 20`