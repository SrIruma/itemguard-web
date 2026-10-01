#!/usr/bin/env bash
# Todas las comprobaciones, en orden y sin dependencias.
#
#   ./scripts/check-all.sh
#
# Sale con codigo distinto de cero si algo falla, asi que sirve tal
# cual como paso previo a publicar. No necesita npm: este sitio es
# estatico y el build es un script de Python.
set -uo pipefail

cd "$(dirname "$0")/.."

fail=0
for s in check-html check-perf check-responsive; do
  printf '\n== %s ==\n' "$s"
  if python3 "scripts/$s.py"; then
    :
  else
    fail=1
  fi
done

printf '\n== regenerar desde cero ==\n'
# build.py vuelve a envolver el contenido y rehacer los indices. Si el
# resultado difiere del que hay en el arbol, algo se edito a mano sin
# pasar por el generador.
if python3 scripts/build.py >/dev/null 2>&1; then
  if git diff --quiet -- docs es search-index.json es/search-index.json 2>/dev/null; then
    echo "  OK el arbol esta sincronizado con el generador"
  else
    echo "  AVISO: docs/ o es/ difieren de lo que genera build.py"
    echo "         ejecuta python3 scripts/build.py y commitea el resultado"
  fi
else
  echo "  FALLA build.py"
  fail=1
fi

printf '\n== enlaces ==\n'
if python3 - <<'PY'
import re, os, glob, sys
root = os.getcwd(); bad = []
for f in glob.glob(root + '/**/*.html', recursive=True):
    if any(s in f for s in ('/.git/', '/node_modules/', '/dist/', '/.astro/')):
        continue
    s = open(f, encoding='utf-8').read()
    for href in re.findall(r'(?:href|src)="(/itemguard-web/[^"#?]*)"', s):
        rel = href[len('/itemguard-web/'):]
        t = os.path.join(root, rel, 'index.html') if rel.endswith('/') else os.path.join(root, rel)
        if not os.path.exists(t):
            bad.append((os.path.relpath(f, root), href))
if bad:
    print(f"  FALLA {len(bad)} enlace(s) roto(s)")
    for b in bad[:8]:
        print("   ", b[0], "->", b[1])
    sys.exit(1)
print("  OK ningun enlace roto")
PY
then :; else fail=1; fi

if [ "$fail" -eq 0 ]; then
  printf '\nTODO CORRECTO\n'
else
  printf '\nHAY PROBLEMAS\n'
fi
exit "$fail"
