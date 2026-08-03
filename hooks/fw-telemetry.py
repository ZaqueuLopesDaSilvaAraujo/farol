#!/usr/bin/env python3
"""fw-telemetry.py — escritor deterministico de telemetria do Farol (v2.2.0).

Hook opcional, opt-in duplo: so age se ESTIVER instalado em .claude/hooks/ E
o manifesto declarar telemetry.enabled = true. Desligado, sai 0 em silencio.

Principio: codigo conta o que e contavel; o modelo so declara o que so ele
sabe (a classificacao T0-T3 do Task Router). Se o modelo nao declarar, a
linha sai degradada (task_class = null) — nunca ausente.

Modos (um por evento de hook do Claude Code):
    --prompt        UserPromptSubmit  abre a tarefa e injeta 1 linha de
                    instrucao SO quando a telemetria esta ligada (custo zero
                    no always-on quando desligada)
    --tool          PostToolUse       registra nome da ferramenta usada
    --subagent      SubagentStop      registra agente fw-* que terminou
    --consolidate   Stop              agrega e grava 1 linha JSONL
    --probe         qualquer          grava as CHAVES do payload (nunca os
                    valores) para inspecionar o contrato da sua versao

Nunca falha a sessao: qualquer erro interno resulta em exit 0.
Uso: python3 .claude/hooks/fw-telemetry.py --tool
"""
import hashlib
import json
import os
import re
import sys
import time

SCHEMA_VERSION = 1

# Unico dado que o modelo fornece. A extracao le o fim do transcript e
# PERSISTE APENAS o token casado por esta regex — o buffer lido e descartado
# sem nunca ser gravado. Nenhum prompt, codigo ou conteudo de arquivo sai daqui.
MARKER = re.compile(r"fw:class=(T[0-3])")

# ASCII puro de proposito: o stdout deste hook e injetado como contexto e, no
# Windows, sai por um pipe em cp1252 — um travessao aqui levanta
# UnicodeEncodeError, e o guarda de erro do main() engoliria a instrucao em
# silencio. Nada fora de ASCII entra nesta string.
INSTRUCAO = (
    "fw: telemetria local ativa - inclua `<!-- fw:class=T0|T1|T2|T3 -->` ao "
    "final da resposta, com a classificacao do Task Router. Nenhum outro dado "
    "e coletado por voce; o restante e medido pelos hooks."
)

EDIT_TOOLS = {"Write", "Edit", "NotebookEdit", "MultiEdit"}


def payload():
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def project_root(data):
    d = os.path.abspath(data.get("cwd") or os.getcwd())
    while True:
        if os.path.isdir(os.path.join(d, ".claude", "context")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return os.path.abspath(data.get("cwd") or os.getcwd())
        d = parent


def config(root):
    """Devolve o bloco telemetry se habilitado; None caso contrario."""
    try:
        with open(os.path.join(root, ".claude", "context", "manifest.json"),
                  encoding="utf-8") as fh:
            manifest = json.load(fh)
    except Exception:
        return None
    tel = manifest.get("telemetry")
    if not isinstance(tel, dict) or not tel.get("enabled"):
        return None
    tel = dict(tel)
    tel["_framework_version"] = manifest.get("version")
    return tel


def log_path(root, cfg):
    destino = cfg.get("path") or ".claude/context/telemetry/log.jsonl"
    return destino if os.path.isabs(destino) else os.path.join(root, destino)


def raw_path(root, session, cfg):
    """O arquivo transitorio da tarefa mora ONDE o log mora — inclusive quando
    telemetry.path e absoluto e aponta para fora do repositorio. Fixa-lo em
    .claude/context/ deixaria residuo dentro do projeto se a sessao fosse
    interrompida entre o primeiro prompt e o Stop."""
    return os.path.join(os.path.dirname(log_path(root, cfg)),
                        ".task-%s.jsonl" % (session or "anon"))


def append_raw(root, session, record, cfg):
    path = raw_path(root, session, cfg)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    record["t"] = time.time()
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def classify_path(root, path, record_paths):
    """('context'|'workspace'|'other', identificador).

    Arquivos do proprio Farol viajam pelo nome (sao do framework, sem risco e
    e a metrica que justifica sua existencia). Qualquer outro arquivo vira
    hash — conta releitura sem nunca registrar o caminho, salvo opt-in
    explicito em telemetry.recordFilePaths.
    """
    if not path:
        return None, None
    try:
        rel = os.path.relpath(os.path.abspath(path), root).replace(os.sep, "/")
    except Exception:
        rel = str(path).replace(os.sep, "/")
    if rel.startswith(".claude/context/workspace/"):
        return "workspace", os.path.basename(rel)
    if rel.startswith(".claude/context/"):
        return "context", os.path.basename(rel)
    if record_paths:
        return "other", rel
    return "other", hashlib.sha1(rel.encode("utf-8")).hexdigest()[:12]


def mode_prompt(root, data, cfg):
    append_raw(root, data.get("session_id"), {"e": "start"}, cfg)
    print(INSTRUCAO)


def mode_tool(root, data, cfg):
    tool = data.get("tool_name")
    if not tool:
        return
    tool_input = data.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    kind, ident = classify_path(root, path, bool(cfg.get("recordFilePaths")))
    # Eventos de ferramenta DENTRO de um subagente carregam agent_type: e o que
    # permite atribuir custo por agente sem o agente escrever nada.
    append_raw(root, data.get("session_id"),
               {"e": "tool", "n": tool, "k": kind, "i": ident,
                "a": data.get("agent_type")}, cfg)


def mode_subagent(root, data, cfg):
    # Documentado: agent_type e o nome do agente (para subagentes customizados,
    # o campo `name` do frontmatter) e agent_id o identificador unico.
    append_raw(root, data.get("session_id"),
               {"e": "subagent", "n": data.get("agent_type"),
                "id": data.get("agent_id"),
                "fim": data.get("subagent_exit_reason")}, cfg)


def task_class(data):
    """Devolve SO o token T0-T3 casado pela regex; nada mais e persistido.

    Fonte primaria: last_assistant_message do proprio evento Stop — contem so
    o texto final do assistente, nunca o prompt do usuario, e a documentacao
    recomenda preferi-lo ao transcript ("which may lag"). O transcript fica
    como fallback, e mesmo ali so o token casado sobrevive: o buffer lido e
    descartado sem jamais ser gravado.
    """
    msg = data.get("last_assistant_message")
    if isinstance(msg, str):
        achados = MARKER.findall(msg)
        if achados:
            return achados[-1]
    path = data.get("transcript_path")
    if not path or not os.path.isfile(path):
        return None
    try:
        with open(path, "rb") as fh:
            fh.seek(0, os.SEEK_END)
            size = fh.tell()
            fh.seek(max(0, size - 65536))
            tail = fh.read().decode("utf-8", "ignore")
    except Exception:
        return None
    achados = MARKER.findall(tail)
    return achados[-1] if achados else None


def prune(lines, cfg):
    dias = cfg.get("retainDays")
    if isinstance(dias, (int, float)) and dias > 0:
        limite = time.time() - dias * 86400
        mantidas = []
        for linha in lines:
            try:
                ts = json.loads(linha).get("ts_epoch", 0)
            except Exception:
                ts = 0
            if not ts or ts >= limite:
                mantidas.append(linha)
        lines = mantidas
    teto = cfg.get("maxLines") or 5000
    return lines[-int(teto):] if len(lines) > int(teto) else lines


def mode_consolidate(root, data, cfg):
    # Stop dispara TAMBEM dentro de um subagente (o payload traz agent_type
    # nesse caso). Consolidar ali fecharia e apagaria a raw no meio da tarefa,
    # gerando varias linhas truncadas no lugar de uma. So o Stop da conversa
    # principal — sem agent_type — encerra a tarefa.
    if data.get("agent_type"):
        return
    session = data.get("session_id")
    raw = raw_path(root, session, cfg)
    if not os.path.isfile(raw):
        return  # nada observado nesta tarefa
    eventos = []
    try:
        with open(raw, encoding="utf-8") as fh:
            for linha in fh:
                try:
                    eventos.append(json.loads(linha))
                except Exception:
                    pass
    except Exception:
        return
    finally:
        try:
            os.remove(raw)
        except Exception:
            pass
    if not eventos:
        return

    inicio = min(e.get("t", 0) for e in eventos) or time.time()
    fim = time.time()
    tools, agentes, ctx_docs = {}, [], []
    tools_por_agente = {}
    vistos, relidos = set(), 0
    workspace_reused = False
    context_updated = False

    for ev in eventos:
        if ev.get("e") == "tool":
            nome = ev.get("n")
            tools[nome] = tools.get(nome, 0) + 1
            dono = ev.get("a") or "principal"
            tools_por_agente[dono] = tools_por_agente.get(dono, 0) + 1
            kind, ident = ev.get("k"), ev.get("i")
            if kind == "workspace":
                workspace_reused = True
            if kind in ("context", "workspace") and nome in EDIT_TOOLS:
                context_updated = True
            if kind == "context" and ident and ident not in ctx_docs:
                ctx_docs.append(ident)
            if nome == "Read" and ident:
                if ident in vistos:
                    relidos += 1
                vistos.add(ident)
        elif ev.get("e") == "subagent":
            agentes.append(ev.get("n"))

    linha = {
        "v": SCHEMA_VERSION,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(fim)),
        "ts_epoch": round(fim, 3),
        "session_id": session,
        "framework_version": cfg.get("_framework_version"),
        # prompt_id e o identificador oficial da rodada de prompt; o hash so
        # entra em versoes que ainda nao o expoem.
        "task_id": data.get("prompt_id") or ("t-" + hashlib.sha1(
            ("%s%s" % (session, inicio)).encode("utf-8")).hexdigest()[:8]),
        "task_class": task_class(data),
        "agents": [a for a in agentes if a],
        "agents_total": len(agentes),
        "models": {},
        "tools": tools,
        "tools_by_agent": tools_por_agente,
        "tool_calls_total": sum(tools.values()),
        "files_read": len(vistos),
        "files_reread": relidos,
        "context_docs": ctx_docs,
        "workspace_reused": workspace_reused,
        "context_updated": context_updated,
        "duration_ms": int((fim - inicio) * 1000),
        "result": "completed",
        "tests_passed": None,
    }

    destino = log_path(root, cfg)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    existentes = []
    if os.path.isfile(destino):
        try:
            with open(destino, encoding="utf-8") as fh:
                existentes = fh.read().splitlines()
        except Exception:
            existentes = []
    existentes.append(json.dumps(linha, ensure_ascii=False))
    existentes = prune(existentes, cfg)
    with open(destino, "w", encoding="utf-8") as fh:
        fh.write("\n".join(existentes) + "\n")


def mode_probe(root, data, cfg):
    """Grava so as CHAVES do payload — nunca os valores. Use para descobrir o
    contrato do SubagentStop da sua versao do Claude Code."""
    destino = os.path.join(os.path.dirname(log_path(root, cfg)), "probe.txt")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "a", encoding="utf-8") as fh:
        fh.write("%s: %s\n" % (data.get("hook_event_name", "?"),
                               sorted(data.keys())))


MODOS = {
    "--prompt": mode_prompt,
    "--tool": mode_tool,
    "--subagent": mode_subagent,
    "--consolidate": mode_consolidate,
    "--probe": mode_probe,
}


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Windows: pipe nasce cp1252
    except Exception:
        pass
    modo = sys.argv[1] if len(sys.argv) > 1 else ""
    if modo not in MODOS:
        return
    data = payload()
    root = project_root(data)
    cfg = config(root)
    if cfg is None:
        return  # telemetria desligada: hook inerte
    MODOS[modo](root, data, cfg)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # telemetria nunca derruba a sessao
    sys.exit(0)
