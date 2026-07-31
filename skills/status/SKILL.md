---
name: status
description: >
  Verifica a saúde do framework e o frescor do contexto: idade da âncora,
  commits acumulados, tamanho da memória, integridade dos arquivos. Use
  quando o usuário pedir /farol:status ou no início de tarefas grandes se houver
  suspeita de contexto desatualizado.
---

# /farol:status — Saúde do contexto

Somente leitura. Sem missões de scout, sem leitura de código-fonte.

## Verificações

1. `manifest.json` existe e é válido? (não → sugerir /farol:init)
2. `contextualized_at` nulo? (sim → sugerir /farol:contextualize)
3. Distância da âncora:
   - `anchor_mode` = "date" → reporte idade em dias e a limitação (sem git,
     sem incremental por diff); 30+ dias → recomendar /farol:update guiado.
   - `anchor_mode` = "git" → `git rev-list --count <anchor_commit>..HEAD`:
     0 → em dia · 1–19 → ok · 20+ → recomendar /farol:update. Âncora
     inexistente (rebase) → avisar; /farol:update resolve via fallback por data.
4. `memory.md`: linhas > 150 → recomendar /farol:consolidate.
5. Integridade: arquivos do `inventory` existem? Hash bate?
   Compare com `git hash-object <arquivo>` (mesmo método da escrita).
   (divergência = edição manual — legítima; apenas avise que o inventário
   será realinhado no próximo /farol:update.)
6. Tetos: algum arquivo de contexto estourou seu limite de linhas?
7. **Ponteiros do índice**: TODO alvo referenciado no `index.md` (tabela
   "Carregue quando", módulos, fontes de autoridade) existe no disco?
   Ponteiro morto num arquivo always-on é a falha de prioridade máxima
   deste relatório — pior que ausência, porque mente com confiança.
8. Seção "Princípios e restrições (INVIOLÁVEIS)" existe e não está vazia?
   (vazia em modo adopt → sugerir reavaliar para augment)
9. Bloco gerenciado: marcadores `ccf:managed-start`/`ccf:managed-end`
   presentes, únicos E com a MESMA versão do plugin
   (`${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`)? Divergência =
   ERRO: o bloco always-on está ensinando comandos de outra era — rode
   /farol:init para atualizá-lo.
10. Recursos instalados: o plugin `farol` está ativo (as skills `/farol:*`
    respondem) e os 3 agents `fw-*` aparecem entre os agents disponíveis?
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
13. Esquema legado: o manifesto contém `adopt_mode`, ou não contém `mode`
    ou `bytesPerToken`? → ALERTA "manifesto no esquema 1.x" com ponteiro
    para a migração do UPGRADE.md. Templates do projeto mencionando
    comandos `/fw-*` → mesmo alerta (rode /farol:init para refrescá-los).
14. Políticas: `policies.md` existe? Se sim, há duplicação proibida
    (números de orçamento repetidos fora do manifesto; lista de
    autoridade repetida fora do index.md) ou campo que conflita com o
    manifesto? → alerta com o trecho.

## Saída

Painel de até 15 linhas: versão, modo, idade do contexto (commits e dias),
custo always-on estimado vs orçamento, status de cada verificação
(OK/atenção/erro), e no máximo 2 ações recomendadas em ordem de prioridade.
