# Políticas do projeto (Farol)

<!-- PROPRIEDADE DO TIME — decisão humana, nunca derivada do código.
Lido APENAS pelas skills do Farol (init/contextualize/update/status);
nunca entra no always-on: custo zero nas sessões comuns.
ESCOPO: este arquivo governa o comportamento DO FAROL. Regras gerais
de sessão (ex.: "push só sob ordem") pertencem ao CLAUDE.md e à doc
do time — não as duplique aqui.
Campo ausente ou comentado = comportamento padrão. As skills aplicam
o que estiver declarado SEM reperguntar, e perguntam só o ausente. -->

## a. Fluxo de versionamento do contexto
<!-- ex.: "contexto commitado na mesma branch e no mesmo conjunto de
commits da mudança que o motivou; push sob ordem explícita" -->
- _(não declarado — comportamento padrão)_

## b. O que da pasta .claude/ entra no Git
<!-- padrão: versionar .claude/context/ e CLAUDE.md; ignorar
.claude/backups/. Declare aqui as exceções do time. -->
- _(não declarado — padrão)_

## c. Gatilho de atualização do índice
<!-- A LISTA de docs que prevalecem já vive em "Fontes de autoridade" do
index.md — não a duplique. Declare apenas o GATILHO:
ex.: "o índice atualiza no mesmo PR que altera estrutura" -->
- _(não declarado — padrão: sugerido após mudança estrutural)_

## d. Orçamento de contexto — política (números NÃO)
<!-- Os números vivem SÓ no contextBudget do manifest.json — não os
repita aqui. Declare a política em torno deles: -->
- Recalibrações de bytesPerToken nunca são silenciosas: exigem linha na
memory.md com data, valor anterior, novo valor e método de medição.

## e. Arquivos ainda não mapeados
<!-- "sob demanda" (padrão) | "varredura periódica via /farol:update" -->
- _(não declarado — padrão: sob demanda)_

## f. Orçamento de execução — política (números NÃO)
<!-- Os valores padrão vivem no executionBudget do manifest.json (fonte
para ajuste por projeto). fw-scout e fw-debugger citam esses mesmos
padrões em prosa para legibilidade — divergência entre manifest e agente
é bug a corrigir no manifest, não customização. Declare aqui apenas a
política em torno dos limites: -->
- Exceder `hardMaxAgents`, ativar paralelismo fora do padrão ou desativar
`stopWhenEvidenceIsSufficient` exige justificativa registrada na
resposta da tarefa — nunca silenciosa.

## g. Política de modelos por categoria (aliases NÃO vivem fixos aqui)
<!-- Diferente do executionBudget: o Claude Code lê `model:` do frontmatter
de cada agente ANTES de iniciá-lo, então não há indireção possível via
manifest ou via este arquivo. Este bloco só registra a INTENÇÃO de
mapeamento categoria→alias, para auditoria (`modelPolicy` no
manifest.json); mudar o comportamento real exige editar `model:`
diretamente em `agents/fw-*.md`. Categorias sugeridas: `economical`
(busca/leitura descartável — papel do fw-scout), `balanced` (padrão do
framework — implementação, depuração comum, revisão comum),
`deep-reasoning` (arquitetura complexa, decisão de alto impacto — só
com justificativa). Os aliases reais (`sonnet`/`opus`/`haiku`/ID
completo) dependem da versão do Claude Code e do plano/allowlist da
organização — não presuma disponibilidade. -->
- _(não declarado — padrão: `inherit` em todos os agentes; nenhuma
categoria fixada por este framework)_

## Defasagem no arranque (fw-freshness)
<!-- comportamento das skills: "avisar" (padrão) | "sugerir_update"
limiar em commits — o hook fw-freshness.sh lê a linha abaixo: -->
freshness_limiar: 20