#!/usr/bin/env python3
"""
Comprueba el HTML generado: sangria residual, jerarquia de titulos,
H1 duplicado, y estructura del landing.

El problema que comprueba: el contenido viene de ficheros que se
generaron en varias pasadas, y una linea con 4 espacios al principio la
interpreta Markdown o el navegador como bloque de codigo. No se ve en
un diff, se ve como un parrafo raro.
"""
import glob
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors: list[str] = []
warnings: list[str] = []

DOC_PAGES = sorted(glob.glob(str(ROOT / "docs/*.html")) + glob.glob(str(ROOT / "es/docs/*.html")))
LANDINGS = [ROOT / "index.html", ROOT / "es/index.html"]
NOT_FOUND = [ROOT / "404.html", ROOT / "es/404.html"]


def fail(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


print(f"1. Sangria residual en el contenido ({len(DOC_PAGES)} paginas)")
for f in DOC_PAGES:
    s = pathlib.Path(f).read_text(encoding="utf-8")
    m = re.search(r'<article class="doc-body">(.*?)</article>', s, re.DOTALL)
    if not m:
        fail(f"{pathlib.Path(f).name}: no hay article")
        continue
    body = m.group(1)
    in_pre = False
    for i, line in enumerate(body.split("\n"), 1):
        # Dentro de <pre> la sangria es parte del ejemplo: forma parte
        # de un YAML o de un bloque de consola y ahi se quiere.
        if "<pre>" in line:
            in_pre = True
        if in_pre:
            if "</pre>" in line:
                in_pre = False
            continue
        if line.strip() and line.startswith("    "):
            fail(f"{pathlib.Path(f).relative_to(ROOT)} linea {i}: sangria residual -> {line.strip()[:56]}")
print(f"   {'OK' if not errors else str(len(errors)) + ' problema(s)'}")

print("\n2. Un solo h1 por pagina, y es el primero")
for f in DOC_PAGES:
    s = pathlib.Path(f).read_text(encoding="utf-8")
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", s, re.DOTALL)
    if len(h1s) != 1:
        fail(f"{pathlib.Path(f).relative_to(ROOT)}: {len(h1s)} h1")
        continue
    # El h1 debe ir antes que cualquier h2.
    i1, i2 = s.find("<h1"), s.find("<h2")
    if i2 != -1 and i1 > i2:
        fail(f"{pathlib.Path(f).relative_to(ROOT)}: el h2 aparece antes que el h1")
print(f"   {'OK' if not errors else 'ver arriba'}")

print("\n3. Los titulos estan en el idioma correcto")
for f in DOC_PAGES:
    s = pathlib.Path(f).read_text(encoding="utf-8")
    is_es = "/es/" in str(f)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.DOTALL)
    if not h1:
        continue
    title = re.sub(r"<[^>]+>", "", h1.group(1)).strip()
    if not title:
        fail(f"{pathlib.Path(f).relative_to(ROOT)}: h1 vacio")
    # Un titulo en ingles en la pagina en español (o al reves) delata
    # que la traduccion se quedo a medias.
    if is_es and title in ("Commands", "Configuration", "Database", "Flags",
                           "Templates", "Permissions", "Translations", "Screens", "FAQ"):
        fail(f"{pathlib.Path(f).relative_to(ROOT)}: titulo en ingles -> {title}")
    if not is_es and title == "Preguntas":
        fail(f"{pathlib.Path(f).relative_to(ROOT)}: titulo en español -> {title}")
print(f"   {'OK' if not errors else 'ver arriba'}")

print("\n4. El TOC tiene entradas (h2 con id)")
for f in DOC_PAGES:
    s = pathlib.Path(f).read_text(encoding="utf-8")
    n = len(re.findall(r'<h2 id="', s))
    if n < 2:
        fail(f"{pathlib.Path(f).relative_to(ROOT)}: solo {n} h2 con id, el TOC quedaria vacio")
print(f"   {'OK' if not errors else 'ver arriba'}")

print("\n5. Landing: estructura y ritmo")
for f in LANDINGS:
    s = pathlib.Path(f).read_text(encoding="utf-8")
    rel = pathlib.Path(f).relative_to(ROOT)
    sections = s.count('class="home-section"')
    if sections < 2 or sections > 5:
        warn(f"{rel}: {sections} secciones, se esperaba entre 2 y 5")
    for req in ('class="hero"', "storefront", "card-grid", "hero-mark", "console-body", "<h1>"):
        if req not in s:
            fail(f"{rel}: falta {req}")
    # El boton de compra tiene que estar visible pero inactivo: asi se ve
    # que va a haber boton y nadie cae en un href sin destino.
    if 'class="btn btn-store"' not in s:
        fail(f"{rel}: falta el boton de compra")
    if 'aria-disabled="true"' not in s:
        fail(f"{rel}: el boton de compra deberia estar inactivo hasta que se publique")
print(f"   {'OK' if not [e for e in errors if 'landing' in e or 'storefront' in e or 'boton' in e] else 'ver arriba'}")

print("\n5b. Reporte de problemas: issues publicos y correo")
for f in DOC_PAGES + NOT_FOUND:
    s = pathlib.Path(f).read_text(encoding="utf-8")
    rel = pathlib.Path(f).relative_to(ROOT)
    if "itemguard-web/issues" not in s:
        fail(f"{rel}: no enlaza al rastreador de issues")
    if "MrTsumugi@proton.me" not in s:
        fail(f"{rel}: no ofrece el correo de contacto")
    # El repo del plugin es privado: no debe aparecer por ningun lado.
    if re.search(r"github\.com/SrIruma/itemguard(?!-web)", s):
        fail(f"{rel}: enlaza al repositorio privado del plugin")
print("   OK (issues + correo, sin repo privado)")

print("\n5c. Sin placeholders sin resolver")
for f in LANDINGS:
    s = f.read_text(encoding="utf-8")
    rel = pathlib.Path(f).relative_to(ROOT)
    if "URL_DE_LA_FICHA" in s and 'aria-disabled="true"' not in s:
        fail(f"{rel}: URL_DE_LA_FICHA sin marcar como inactivo")
    # {{ }} aparece en el script del tema como }}(); — cierre de funcion,
    # no un marcador sin sustituir. Solo se miran los marcadores que
    # aparecen sueltos, tipicos de una plantilla sin rellenar.
    for token in ("TODO", "FIXME", "undefined", "NaN"):
        if token in s:
            fail(f"{rel}: placeholder {token!r} sin resolver")
    if re.search(r"\{\{\s*[a-z_.]+\s*\}\}", s):
        fail(f"{rel}: marcador {{...}} sin sustituir")
print("   OK")

print("\n6. Los iconos y la marca en todas partes")
SKIP = ("/.git/", "/content/", "/node_modules/", "/dist/", "/.astro/")
alls = [pathlib.Path(p) for p in
        glob.glob(str(ROOT / "**/*.html"), recursive=True)
        if not any(s in p.replace("\\", "/") for s in SKIP)]
for f in alls:
    s = f.read_text(encoding="utf-8")
    if 'rel="icon"' not in s:
        fail(f"{f.relative_to(ROOT)}: sin icono")
    elif "favicon-32.png" not in s:
        fail(f"{f.relative_to(ROOT)}: set de iconos incompleto")
    if "brand" in s and "brand-mark" not in s and "author-link" not in s:
        fail(f"{f.relative_to(ROOT)}: la marca no es la imagen")
print(f"   OK ({len(alls)} paginas)")

print("\n7. Nada de HTML sin cerrar en el landing")
for f in LANDINGS:
    s = f.read_text(encoding="utf-8")
    for tag in ("section", "div", "main", "article"):
        o = len(re.findall(rf"<{tag}[\s>]", s))
        c = len(re.findall(rf"</{tag}>", s))
        if o != c:
            fail(f"{f.relative_to(ROOT)}: <{tag}> abre {o} veces y cierra {c}")
print(f"   {'OK' if not errors else 'ver arriba'}")

print()
for w in warnings:
    print(f"  aviso: {w}")
if errors:
    print(f"RESULTADO: {len(errors)} problema(s)")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("RESULTADO: HTML correcto")
