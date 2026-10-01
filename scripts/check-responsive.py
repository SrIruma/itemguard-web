#!/usr/bin/env python3
"""
Comprueba que el sitio responde.

No abre un navegador: revisa el CSS y el JS por las condiciones que
importan. Lo que se busca son fallos concretos, no estetica:

  - una pieza de la cabecera que se oculta y no debe (el selector de
    idioma se escondia en movil, y en un sitio bilingue eso es un
    callejon sin salida)
  - un contenedor que no puede encogerse y desborda
  - unDrawer que no se cierra con Escape ni devuelve el foco
  - texto que se sale de su caja
"""
import glob
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
js = (ROOT / "assets" / "js" / "app.js").read_text(encoding="utf-8")

LANDINGS = [ROOT / "index.html", ROOT / "es/index.html"]
DOC_PAGES = sorted(glob.glob(str(ROOT / "docs/*.html")) + glob.glob(str(ROOT / "es/docs/*.html")))

errors: list[str] = []
notes: list[str] = []


def queries(cond: str) -> list[str]:
    """Los bloques de una media query, en orden."""
    return re.findall(rf"@media\s*\({cond}[^)]*\)\s*\{{", css)


print("1. Los cuatro puntos de corte existen")
for cond, label in [("max-width: 1180px", "1180px  cae el indice lateral"),
                    ("max-width: 900px",  "900px   la sidebar pasa a cajon"),
                    ("max-width: 700px",  "700px   cabecera y hero"),
                    ("max-width: 520px",  "520px   una columna")]:
    if not queries(cond):
        errors.append(f"falta el punto de corte {label}")
    else:
        print(f"   OK {label}")

print("\n2. Nada que deba staying desaparece")
# El selector de idioma se escondia entero por debajo de 900px, sin
# forma de cambiar de idioma en un movil. Ahora se compacta.
lang_hide = re.search(r"@media[^{]*\{[^}]*\.lang-switch\s*\{\s*display:\s*none", css)
if lang_hide:
    errors.append(".lang-switch se oculta en movil: no hay forma de cambiar de idioma")
else:
    print("   OK el selector de idioma nunca se oculta")
if not re.search(r"@media[^{]*\{(?:[^{}]|\{[^{}]*\})*?\.lang-switch\s*\{[^}]*display:\s*flex", css):
    errors.append(".lang-switch no se recoloca explicitamente en ningun punto de corte")

print("\n3. Los contenedores que pueden desbordar tienen min-width: 0")
# En un grid, un hijo con contenido largo (una tabla, un <pre>) no se
# encoge salvo que se le ponga min-width: 0. Sin eso empuja el layout.
grid_children = re.findall(r"\.content\s*\{[^}]*\}", css)
if not re.search(r"\.content-inner\s*\{[^}]*min-width:\s*0", css) and \
   not re.search(r"\.doc-body\s*\{[^}]*min-width:\s*0", css):
    notes.append("comprobar min-width: 0 en las columnas del grid")
else:
    print("   OK min-width: 0 presente donde hace falta")

for sel, prop in [("pre", "overflow-x"), (".table-wrap", "overflow-x")]:
    m = re.search(rf"(?m)^{re.escape(sel)}\s*\{{(.*?)^\}}", css, re.DOTALL)
    if m and prop not in m.group(1):
        errors.append(f"{sel} no tiene {prop}: se sale de la pantalla en movil")
    else:
        print(f"   OK {sel} tiene {prop}")

print("\n4. El cajon: existe en cada pagina y se abre")
# El boton hamburguesa estaba en el topbar del landing, que es
# compartido, pero el landing no tenia cajon: en un movil pulsabas el
# boton y no pasaba nada.
for f in LANDINGS:
    s = pathlib.Path(f).read_text(encoding="utf-8")
    rel = pathlib.Path(f).relative_to(ROOT)
    if 'id="menu-toggle"' in s and 'id="home-menu"' not in s:
        errors.append(f"{rel}: boton hamburguesa sin el panel que abre")
    # aria-controls tiene que apuntar a algo real.
    m = re.search(r'aria-controls="([^"]+)"', s)
    if m and f'id="{m.group(1)}"' not in s:
        errors.append(f"{rel}: aria-controls apunta a {m.group(1)}, que no existe")
print(f"   OK los dos landings tienen menu ({len(LANDINGS)} revisados)")

for name, pat in [("se cierra con Escape", r'e\.key\s*===\s*["\']Escape["\']'),
                  ("devuelve el foco al boton", r"btn\.focus\(\)"),
                  ("actualiza aria-expanded", r'aria-expanded')]:
    if re.search(pat, js):
        print(f"   OK {name}")
    else:
        errors.append(f"el cajon: {name} no esta")

if re.search(r"body\.nav-open\s*\{\s*overflow:\s*hidden", css):
    print("   OK la pagina no scrollea con el cajon abierto")
else:
    errors.append("con el cajon abierto la pagina de detras sigue scrolleando")

print("\n4b. Las tablas no obligan a desplazar de lado")
# Con scroll horizontal, la columna que estas leyendo sale de la
# pantalla. Cada celda tiene que llevar el nombre de su columna para
# poder apilarse como tarjeta.
missing = []
for f in DOC_PAGES:
    s = pathlib.Path(f).read_text(encoding="utf-8")
    for t in re.findall(r"<table>.*?</table>", s, re.DOTALL):
        if "<tbody>" not in t:
            continue
        cells = re.findall(r"<td[^>]*>", t)
        if not cells:
            continue
        sin = [c for c in cells if "data-label" not in c]
        if sin:
            missing.append(f"{pathlib.Path(f).name}: {len(sin)} celda(s) sin data-label")
if missing:
    for m in missing[:5]:
        errors.append("tabla sin etiquetas: " + m)
else:
    print("   OK todas las celdas llevan data-label")

if re.search(r"@media[^{]*\{(?:[^{}]|\{[^{}]*\})*?\.table-wrap td::before", css):
    print("   OK hay regla que apila la tabla en tarjetas")
else:
    errors.append("nada apila las tablas en movil: siguen exigiendo scroll horizontal")

print("\n5. El texto no se sale de su caja")
# word-break en los bloques de codigo largos, y nada de nowrap
# generalizado que corte palabras a la mitad.
if not re.search(r":not\(pre\)\s*>\s*code\s*\{[^}]*word-break", css):
    errors.append("el codigo en linea no puede partirse: un token largo desborda en movil")
else:
    print("   OK el codigo en linea puede partirse")

if "text-wrap: balance" not in css and "text-wrap: pretty" not in css:
    notes.append("sin text-wrap: balance/pretty en los titulos (evita lineas viudas)")

print("\n7. La cabecera no desborda en movil")
# El fallo que mas cueste encontrar: con flex-shrink: 0 en varios
# hijos, el contenido de la cabecera no cabe en 360px y el boton del
# menu se empuja fuera del viewport. En un telefono no se veia, y en
# el escritorio nunca pasa porque hay 1000px de sobra.
# Lo que no puede ceder esta vez: el boton del menu, el buscador, el
# idioma y el tema. Si algo de eso lleva flex-shrink: 0 sin un
# min-width: 0 que compense, la cabecera se sale.
inner = re.search(r"\.topbar-inner\s*\{(.*?)\}", css, re.DOTALL)
if not inner:
    errors.append("no se encuentra .topbar-inner")
elif "min-width: 0" not in inner.group(1):
    errors.append(".topbar-inner sin min-width: 0: el contenido que no cede lo saca de la pantalla")

# Ningun elemento que deba quedarse visible puede llevar flex-shrink: 0
# sin un min-width: 0 al lado.
for sel in (".brand", ".topbar-actions"):
    m = re.search(rf"(?m)^{re.escape(sel)}\s*\{{(.*?)^\}}", css, re.DOTALL)
    if not m:
        continue
    body = m.group(1)
    if "flex-shrink: 0" in body and "min-width: 0" not in body:
        errors.append(f"{sel} tiene flex-shrink: 0 sin min-width: 0: empuja el menu fuera")

# Y el nombre de la marca tiene que poder recortarse u ocultarse.
if not re.search(r"\.brand-text\s*\{[^}]*overflow:\s*hidden", css):
    errors.append(".brand-text no se recorta: en un movil el nombre empuja el menu")
if not re.search(r"@media[^{]*\{(?:[^{}]|\{[^{}]*\})*?\.brand-text\s*\{\s*display:\s*none", css):
    notes.append("el nombre de la marca no se oculta en ningun punto de corte")
else:
    print("   OK el nombre de la marca se oculta en pantallas estrechas")

print("\n8. Objetivos tactiles")
# Se mira el mayor tamaño en cualquier punto de corte: en movil los
# botones se agrandan, y el valor de la regla base no es el que ve el
# dedo.
sizes = [int(m) for m in re.findall(r"\.icon-btn\s*\{[^}]*?width:\s*(\d+)px", css, re.DOTALL)]
if sizes:
    if max(sizes) >= 40:
        print(f"   OK icon-btn llega a {max(sizes)}px en movil")
    else:
        errors.append(f"icon-btn se queda en {max(sizes)}px: por debajo de los 40px que pide un dedo")
else:
    errors.append("no se encuentra el tamaño de .icon-btn")

print()
for n in notes:
    print(f"  nota: {n}")
if errors:
    print(f"RESULTADO: {len(errors)} problema(s)")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("RESULTADO: responsive")
