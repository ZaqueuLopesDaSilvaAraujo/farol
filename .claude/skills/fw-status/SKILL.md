---
name: fw-status
description: >
  Verifica a saúde do framework e o frescor do contexto: idade da âncora,
  commits acumulados, tamanho da memória, integridade dos arquivos. Use
  quando o usuário pedir /fw-status ou no início de tarefas grandes se houver
  suspeita de contexto desatualizado.
---

# /fw-status — Saúde do contexto

Somente leitura. Sem missões de scout, sem leitura de código-fonte.

## Verificações

1. `manifest.json` existe e é válido? (não → sugerir /fw-init)
2. `contextualized_at` nulo? (sim → sugerir /fw-contextualize)
3. Distância da âncora:
   - `anchor_mode` = "date" → reporte idade em dias e a limitação (sem git,
     sem incremental por diff); 30+ dias → recomendar /fw-update guiado.
   - `anchor_mode` = "git" → `git rev-list --count <anchor_commit>..HEAD`:
     0 → em dia · 1–19 → ok · 20+ → recomendar /fw-update. Âncora
     inexistente (rebase) → avisar; /fw-update resolve via fallback por data.
4. `memory.md`: linhas > 150 → recomendar /fw-consolidate.
5. Integridade: arquivos do `inventory` existem? Hash bate?
   Compare com `git hash-object <arquivo>` (mesmo método da escrita).
   (divergência = edição manual — legítima; apenas avise que o inventário
   será realinhado no próximo /fw-update.)
6. Tetos: algum arquivo de contexto estourou seu limite de linhas?
7. **Ponteiros do índice**: TODO alvo referenciado no `index.md` (tabela
   "Carregue quando", módulos, fontes de autoridade) existe no disco?
   Ponteiro morto num arquivo always-on é a falha de prioridade máxima
   deste relatório — pior que ausência, porque mente com confiança.
8. Seção "Princípios e restrições (INVIOLÁVEIS)" existe e não está vazia?
9. Bloco gerenciado: marcadores `ccf:managed-start`/`ccf:managed-end`
   presentes e únicos no CLAUDE.md?
10. Recursos instalados: os 3 agents e as 6 skills `fw-*` existem no disco?
11. Obrigatórios por modo: adopt → "Fontes de autoridade" preenchida com
    alvos existentes; augment → lacunas pendentes listadas (ou zeradas);
    bootstrap → `architecture.md` e `conventions.md` existem.
12. Orçamento de contexto: some os bytes dos arquivos always-on (CLAUDE.md +
    index.md + imports diretos), estime tokens (bytes ÷ `bytesPerToken` do
    manifesto) e compare com o `contextBudget`. Se `bytesPerToken` estiver
    ausente ou for 4 com conteúdo em idioma acentuado, ALERTE: a estimativa
    está inflada em ~55% a favor da luz verde — recalibre no manifesto. Acima de `warningThresholdTokens` →
    alerta com sugestão concreta de corte; acima de `hardLimitTokens` →
    ERRO.

## Saída

Painel de até 15 linhas: versão, modo, idade do contexto (commits e dias),
custo always-on estimado vs orçamento, status de cada verificação
(OK/atenção/erro), e no máximo 2 ações recomendadas em ordem de prioridade.
