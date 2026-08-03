# Workspace de Investigação — {título da investigação}

<!-- Arquivo TEMPORÁRIO de trabalho, não é conhecimento permanente.
Um workspace por investigação ativa, em .claude/context/workspace/.
Carregue apenas o workspace relacionado à tarefa atual (ver index.md,
tabela "Carregue quando") — nunca carregue todos de uma vez.
Não é diário de sessão: registre o que faz a investigação avançar,
não cada ação tomada. Ao concluir, siga o "Ciclo de encerramento". -->

## Metadados
- Título: {resumo curto da investigação}
- Iniciada em: {AAAA-MM-DD}
- Atualizada em: {AAAA-MM-DD}
- Commit-base: {sha curto do commit em que a investigação começou}
- Responsável: {sessão/agente que abriu a investigação}
- Estado: {ativa | interrompida | concluída}

## Escopo
- {o que está sendo investigado; o que fica explicitamente fora}

## Pergunta principal
- {a pergunta que orienta toda a investigação}

## Fatos confirmados
- {fato} — {evidência/fonte}

## Hipóteses
<!-- Ordenadas por probabilidade/custo. Debugger: no máximo 3 ativas. -->
- {hipótese} — {status: em teste | aguardando}

## Hipóteses descartadas
- {hipótese} — {motivo do descarte}

## Arquivos analisados
<!-- Consulte esta lista antes de reler um arquivo já investigado. -->
- {caminho} — {o que foi encontrado}

## Comandos/experimentos executados
<!-- Consulte antes de repetir um experimento já registrado aqui. -->
- {comando/experimento} — {resultado}

## Resultados
- {resultado consolidado até o momento}

## Achados adjacentes não investigados
<!-- Registre sem expandir o escopo da missão atual. -->
- {achado} — {por que não foi aprofundado}

## Pendências
- {o que falta para fechar esta investigação}

## Conclusão atual
- {resposta parcial ou final à pergunta principal}

## Ciclo de encerramento
<!-- Ao concluir ou abandonar a investigação, nesta ordem: -->
1. Promova fatos permanentes para o arquivo definitivo (architecture.md,
   conventions.md, modules/{nome}.md) — nunca deixe fato permanente só
   aqui.
2. Se houve decisão com trade-offs, crie um ADR em `decisions/`.
3. Preferências e aprendizados duráveis vão para `memory.md`.
4. Apague as hipóteses descartadas; elas não têm valor permanente.
5. Remova ou arquive este arquivo — um workspace concluído não deve
   continuar sendo carregado como se fosse investigação ativa.

## Versionamento
- Padrão recomendado: local e temporário. A política do projeto decide
  se `workspace/` entra no controle de versão ou fica fora dele (ex.:
  `.gitignore`); nenhuma das duas opções é obrigatória pelo Farol.