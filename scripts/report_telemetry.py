#!/usr/bin/env python3
"""report_telemetry.py — leitor da telemetria local do Farol (v2.2.0).

Toda agregacao acontece AQUI, em codigo: o /farol:status apenas executa e
exibe. O modelo nunca soma nada.

Uso:
    python3 scripts/report_telemetry.py [raiz] [--panel] [--since N]
                                        [--compare vA vB] [--json]

    --panel        3 linhas, para embutir no painel do /farol:status
                   (que tem teto declarado de 15 linhas)
    --since N      considera so os ultimos N dias
    --compare A B  delta entre duas versoes do framework, por classificacao
    --json         despeja o agregado bruto

Nunca bloqueia: exit 0 mesmo com arquivo ausente, vazio ou linha corrompida
(linhas invalidas sao contadas e reportadas, nunca fatais). Exit 1 apenas se
a raiz informada nao existir.
"""
import json
import os
import sys
import time

DEFAULT_PATH = os.path.join(".claude", "context", "telemetry", "log.jsonl")
CLASSES = ("T0", "T1", "T2", "T3")


def carregar(root, since_days=None):
    caminho = DEFAULT_PATH
    try:
        with open(os.path.join(root, ".claude", "context", "manifest.json"),
                  encoding="utf-8") as fh:
            tel = json.load(fh).get("telemetry") or {}
            caminho = tel.get("path") or DEFAULT_PATH
    except Exception:
        pass
    destino = caminho if os.path.isabs(caminho) else os.path.join(root, caminho)
    linhas, invalidas = [], 0
    if not os.path.isfile(destino):
        return linhas, invalidas, destino
    limite = time.time() - since_days * 86400 if since_days else None
    with open(destino, encoding="utf-8") as fh:
        for bruta in fh:
            if not bruta.strip():
                continue
            try:
                reg = json.loads(bruta)
            except Exception:
                invalidas += 1
                continue
            if limite and (reg.get("ts_epoch") or 0) < limite:
                continue
            linhas.append(reg)
    return linhas, invalidas, destino


def mediana(valores):
    if not valores:
        return 0
    ordenados = sorted(valores)
    meio = len(ordenados) // 2
    if len(ordenados) % 2:
        return ordenados[meio]
    return round((ordenados[meio - 1] + ordenados[meio]) / 2, 1)


def agregar(linhas):
    ag = {
        "tarefas": len(linhas),
        "sessoes": len({r.get("session_id") for r in linhas if r.get("session_id")}),
        "por_classe": {},
        "por_agente": {},
        "por_ferramenta": {},
        "por_versao": {},
        "com_classe": sum(1 for r in linhas if r.get("task_class")),
        "context_docs": {},
    }
    for reg in linhas:
        classe = reg.get("task_class") or "?"
        alvo = ag["por_classe"].setdefault(
            classe, {"n": 0, "tool_calls": [], "agentes": 0, "duracoes": []})
        alvo["n"] += 1
        alvo["tool_calls"].append(reg.get("tool_calls_total") or 0)
        alvo["agentes"] += reg.get("agents_total") or 0
        alvo["duracoes"].append(reg.get("duration_ms") or 0)

        for agente in reg.get("agents") or []:
            linha = ag["por_agente"].setdefault(agente, {"n": 0, "tool_calls": 0})
            linha["n"] += 1
        # Atribuicao real: chamadas feitas DENTRO de cada agente, via agent_type
        # do PostToolUse. Antes disso o total da tarefa era creditado a todos os
        # agentes acionados — o que inflava qualquer comparacao.
        for dono, qtd in (reg.get("tools_by_agent") or {}).items():
            linha = ag["por_agente"].setdefault(dono, {"n": 0, "tool_calls": 0})
            linha["tool_calls"] += qtd

        for nome, qtd in (reg.get("tools") or {}).items():
            ag["por_ferramenta"][nome] = ag["por_ferramenta"].get(nome, 0) + qtd

        for doc in reg.get("context_docs") or []:
            ag["context_docs"][doc] = ag["context_docs"].get(doc, 0) + 1

        versao = reg.get("framework_version") or "?"
        vlinha = ag["por_versao"].setdefault(
            versao, {"n": 0, "tool_calls": [], "agentes": 0})
        vlinha["n"] += 1
        vlinha["tool_calls"].append(reg.get("tool_calls_total") or 0)
        vlinha["agentes"] += reg.get("agents_total") or 0
    return ag


def cobertura(ag):
    if not ag["tarefas"]:
        return 0
    return round(100.0 * ag["com_classe"] / ag["tarefas"])


def render_panel(ag, invalidas):
    if not ag["tarefas"]:
        return ["telemetria: nenhuma tarefa registrada"]
    total_tools = sum(ag["por_ferramenta"].values())
    top = sorted(ag["por_ferramenta"].items(), key=lambda x: -x[1])[:3]
    resumo = " ".join("%s=%d" % (n, q) for n, q in top)
    linhas = [
        "telemetria: %d tarefas / %d sessoes · %d chamadas de ferramenta (%s)"
        % (ag["tarefas"], ag["sessoes"], total_tools, resumo),
        "  por classe: " + " ".join(
            "%s=%d" % (c, ag["por_classe"].get(c, {}).get("n", 0))
            for c in CLASSES) + " · sem classe=%d"
        % ag["por_classe"].get("?", {}).get("n", 0),
        "  cobertura de classificacao: %d%%%s" % (
            cobertura(ag),
            " · %d linha(s) invalida(s)" % invalidas if invalidas else ""),
    ]
    return linhas


def render_full(ag, invalidas, destino):
    out = ["Telemetria - Farol", "", "Arquivo: %s" % destino]
    if not ag["tarefas"]:
        out.append("Nenhuma tarefa registrada.")
        return out
    out.append("Tarefas: %d · Sessoes: %d · Tarefas/sessao: %.1f" % (
        ag["tarefas"], ag["sessoes"],
        ag["tarefas"] / ag["sessoes"] if ag["sessoes"] else 0))
    out.append("Cobertura de classificacao declarada: %d%% (%d de %d)" % (
        cobertura(ag), ag["com_classe"], ag["tarefas"]))
    if invalidas:
        out.append("Linhas invalidas ignoradas: %d" % invalidas)

    out += ["", "Por classificacao (Task Router)"]
    for classe in CLASSES + ("?",):
        d = ag["por_classe"].get(classe)
        if not d:
            continue
        out.append("  %-3s n=%-4d tool_calls_mediana=%-5s agentes/tarefa=%.2f "
                   "duracao_mediana=%sms" % (
                       classe, d["n"], mediana(d["tool_calls"]),
                       d["agentes"] / d["n"], mediana(d["duracoes"])))

    out += ["", "Por agente (chamadas atribuidas a quem as fez)"]
    if ag["por_agente"]:
        for nome, d in sorted(ag["por_agente"].items(),
                              key=lambda x: -x[1]["tool_calls"]):
            out.append("  %-14s execucoes=%-4d tool_calls=%-5d" % (
                nome or "(anonimo)", d["n"], d["tool_calls"]))
    else:
        out.append("  nenhum subagente registrado")

    out += ["", "Por ferramenta"]
    total = sum(ag["por_ferramenta"].values()) or 1
    for nome, qtd in sorted(ag["por_ferramenta"].items(), key=lambda x: -x[1]):
        out.append("  %-14s %-6d %4.1f%%" % (nome, qtd, 100.0 * qtd / total))

    out += ["", "Documentos de contexto carregados"]
    if ag["context_docs"]:
        for nome, qtd in sorted(ag["context_docs"].items(), key=lambda x: -x[1]):
            out.append("  %-24s %d" % (nome, qtd))
    else:
        out.append("  nenhum")

    out += ["", "Por versao do framework"]
    for versao, d in sorted(ag["por_versao"].items()):
        out.append("  %-10s n=%-4d tool_calls_mediana=%-5s agentes/tarefa=%.2f"
                   % (versao, d["n"], mediana(d["tool_calls"]),
                      d["agentes"] / d["n"]))
    return out


def render_compare(linhas, va, vb):
    out = ["Comparacao %s -> %s" % (va, vb), ""]
    grupos = {}
    for versao in (va, vb):
        grupos[versao] = agregar([r for r in linhas
                                  if (r.get("framework_version") or "?") == versao])
    if not grupos[va]["tarefas"] or not grupos[vb]["tarefas"]:
        out.append("Dados insuficientes: %s n=%d, %s n=%d." % (
            va, grupos[va]["tarefas"], vb, grupos[vb]["tarefas"]))
        out.append("Nenhum numero de economia deve ser declarado sem execucoes "
                   "registradas nas duas versoes (ver tests/PROTOCOL.md).")
        return out
    out.append("%-4s %-22s %-22s %s" % ("", va, vb, "delta"))
    for classe in CLASSES + ("?",):
        a = grupos[va]["por_classe"].get(classe)
        b = grupos[vb]["por_classe"].get(classe)
        if not a or not b:
            continue
        ma, mb = mediana(a["tool_calls"]), mediana(b["tool_calls"])
        delta = "%+.1f%%" % (100.0 * (mb - ma) / ma) if ma else "n/a"
        out.append("%-4s n=%-3d tool_calls=%-8s n=%-3d tool_calls=%-8s %s" % (
            classe, a["n"], ma, b["n"], mb, delta))
    return out


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Windows: pipe nasce cp1252
    except Exception:
        pass
    args = sys.argv[1:]
    root = "."
    if args and not args[0].startswith("--"):
        root = args[0]
        args = args[1:]
    if not os.path.isdir(root):
        print("raiz inexistente: %s" % root)
        sys.exit(1)

    since = None
    if "--since" in args:
        try:
            since = float(args[args.index("--since") + 1])
        except Exception:
            since = None

    linhas, invalidas, destino = carregar(root, since)

    if "--compare" in args:
        i = args.index("--compare")
        try:
            va, vb = args[i + 1], args[i + 2]
        except IndexError:
            print("--compare exige duas versoes")
            sys.exit(0)
        print("\n".join(render_compare(linhas, va, vb)))
        sys.exit(0)

    ag = agregar(linhas)
    if "--json" in args:
        print(json.dumps(ag, ensure_ascii=False, indent=2))
    elif "--panel" in args:
        print("\n".join(render_panel(ag, invalidas)))
    else:
        print("\n".join(render_full(ag, invalidas, destino)))
    sys.exit(0)


if __name__ == "__main__":
    main()
