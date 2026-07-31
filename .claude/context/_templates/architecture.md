# Arquitetura

<!-- Carga sob demanda. Teto: 120 linhas. Nada que já esteja no index.md. -->

## Estilo arquitetural
{camadas | hexagonal | MVC | event-driven | …} — {1 linha de por quê, ou ADR}

## Camadas / componentes
- **{camada}** (`{caminho/}`): {responsabilidade em 1 linha} — depende de: {…}

## Fluxo típico
<!-- o caminho de UMA requisição/ação representativa, passo a passo -->
1. {entrada} → 2. {…} → 3. {…} → 4. {saída}

## Fronteiras e regras de dependência
- {ex.: domínio não importa infraestrutura}
- {ex.: comunicação entre módulos só via {mecanismo}}

## Integrações externas
- {serviço/banco/fila}: {para quê} — config via `{VAR_DE_AMBIENTE}` (nome, nunca valor)

## Pontos de atenção estruturais
- {acoplamentos perigosos, partes legadas, zonas de não-mexer}
