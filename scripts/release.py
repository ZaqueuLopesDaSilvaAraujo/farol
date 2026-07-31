#!/usr/bin/env python3
"""release.py — empacotamento deterministico do Farol.

Uso: python3 scripts/release.py [saida.zip]
Multiplataforma (Windows/Linux/macOS): usa apenas stdlib, sem shell.
Falha (exit != 0) em qualquer inconsistencia. So arquivos entram no zip —
diretorio vazio nunca e empacotado (a licao da release 1.1.0).
"""
import filecmp, os, sys, tempfile, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules"}
REQUIRED = [
    "VERSION", "README.md", "INSTALL.md", "CHANGELOG.md", "UPGRADE.md",
    "LICENSE", "CLAUDE.md.ccf",
    ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
    "agents/fw-scout.md", "agents/fw-reviewer.md", "agents/fw-debugger.md",
    "skills/init/SKILL.md", "skills/contextualize/SKILL.md",
    "skills/update/SKILL.md", "skills/consolidate/SKILL.md",
    "skills/decision/SKILL.md", "skills/status/SKILL.md",
    "templates/index.md", "hooks/fw-guard.sh",
    "assets/banner.png", "scripts/release.py", "tests/PROTOCOL.md",
]

def collect():
    files = []
    for root, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for n in names:
            p = os.path.relpath(os.path.join(root, n), ROOT)
            files.append(p.replace(os.sep, "/"))
    return sorted(files)

def validate_names(files):
    errs = []
    for p in files:
        if any(c in p for c in "{}\\"):
            errs.append(f"caractere invalido no caminho: {p}")
        if len(p) > 200:
            errs.append(f"caminho longo demais ({len(p)}): {p}")
    for r in REQUIRED:
        if r not in files:
            errs.append(f"arquivo obrigatorio ausente: {r}")
    return errs

def main():
    version = open(os.path.join(ROOT, "VERSION")).read().strip()
    out = sys.argv[1] if len(sys.argv) > 1 else f"farol-v{version}.zip"

    files = collect()
    errs = validate_names(files)
    if errs:
        print("FALHA na validacao pre-empacotamento:")
        for e in errs:
            print("  -", e)
        sys.exit(1)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(os.path.join(ROOT, p), p)

    with tempfile.TemporaryDirectory() as d:
        with zipfile.ZipFile(out) as z:
            bad = [n for n in z.namelist() if any(c in n for c in "{}\\")]
            if bad:
                print("FALHA: caminhos invalidos dentro do zip:", bad)
                sys.exit(1)
            z.extractall(d)
        extracted = []
        for root, dirs, names in os.walk(d):
            for n in names:
                extracted.append(
                    os.path.relpath(os.path.join(root, n), d).replace(os.sep, "/"))
        extracted.sort()
        if extracted != files:
            print("FALHA: estrutura extraida diverge da origem")
            print("  faltando:", sorted(set(files) - set(extracted)))
            print("  sobrando:", sorted(set(extracted) - set(files)))
            sys.exit(1)
        for p in files:
            if not filecmp.cmp(os.path.join(ROOT, p), os.path.join(d, p), shallow=False):
                print("FALHA: conteudo divergente apos extracao:", p)
                sys.exit(1)

    print(f"OK: {out} — {len(files)} arquivos; nomes, extracao e conteudo validados")

if __name__ == "__main__":
    main()
