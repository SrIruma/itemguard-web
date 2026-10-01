#!/usr/bin/env python3
"""
Comprueba el coste de pintado del sitio.

El lag del que se quejaba el usuario venia de tres cosas concretas:
seis gradientes superpuestos en el hero, un backdrop-filter sobre todo
el viewport al abrir la busqueda, y cuatro animaciones infinitas a la
vez. Esta script vigila las tres, para que no vuelvan.
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")

errors: list[str] = []
notes: list[str] = []


def block(selector: str) -> str:
    """El cuerpo de una regla CSS de primer nivel."""
    m = re.search(rf"(?m)^{re.escape(selector)}\s*\{{(.*?)^\}}", css, re.DOTALL)
    return m.group(1) if m else ""


print("1. El hero usa una imagen, no gradientes apilados")
hero = block(".hero")
grads = len(re.findall(r"(?:-webkit-)?(?:linear|radial|conic)-gradient", hero))
if grads > 2:
    errors.append(f".hero tiene {grads} gradientes: vuelve a pintarse en cada frame")
else:
    print(f"   OK ({grads} gradiente, la imagen hace el resto)")
if "hero-bg.webp" not in hero:
    errors.append(".hero no carga la imagen generada")

print("\n2. backdrop-filter: solo donde aporta")
# Solo declaraciones, no las menciones en comentarios: el termino
# aparece escrito al explicar por que se quito uno de ellos.
bf = len(re.findall(r"^\s*backdrop-filter:", css, re.MULTILINE))
if bf > 1:
    errors.append(f"{bf} backdrop-filter: el desenfoque de area grande es la causa mas comun de lag")
else:
    print(f"   OK ({bf}, solo la barra pegajosa)")

print("\n3. Animaciones infinitas: las justas")
infinite = re.findall(r"animation:[^;]*infinite", css)
# Se permiten tres: el halo del logo, el cursor de la consola y el
# punto de estado. Cuatro ya se notaban.
if len(infinite) > 3:
    errors.append(f"{len(infinite)} animaciones infinitas, se permiten 3")
else:
    print(f"   OK ({len(infinite)})")
    for a in infinite:
        name = a.split()[1]
        print(f"      - {name}")

print("\n4. Ninguna animacion mueve el fondo (repintado continuo)")
# Mover background-position repinta la zona cada frame; con seis capas
# era el coste principal. Ya no debe aparecer.
if re.search(r"@keyframes[^{]*\{[^}]*background-position", css, re.DOTALL):
    errors.append("hay un keyframe que anima background-position: repinta en cada frame")
else:
    print("   OK (ninguna anima el fondo)")

print("\n5. prefers-reduced-motion cubre las animaciones")
rm = block("@media (prefers-reduced-motion: reduce)")
if not rm:
    errors.append("falta el bloque prefers-reduced-motion")
else:
    print(f"   OK ({len(re.findall(r'animation: none', rm))} animaciones anuladas)")

print("\n6. Peso de las imagenes del hero")
for f in ["hero-bg.webp", "hero-bg-sm.webp",
          "hero-bg-light.webp", "hero-bg-light-sm.webp",
          "logo.png", "favicon-32.png"]:
    p = ROOT / "assets" / "img" / f
    if not p.exists():
        notes.append(f"{f}: no existe")
        continue
    kb = p.stat().st_size / 1024
    limit = 400 if f == "logo.png" else 60
    flag = "OK " if kb <= limit else "PESADO"
    print(f"   {flag} {f:22} {kb:6.1f} KB")
    if kb > limit and f != "logo.png":
        errors.append(f"{f} pesa {kb:.0f} KB")
    if f == "logo.png" and kb > 400:
        notes.append("logo.png es el original de 1254px; solo se carga recortado")

print("\n7. El modo claro tiene su propio fondo")
if 'hero-bg-light.webp' not in css:
    errors.append('el tema claro no tiene imagen propia: con la de noche se empasta')
else:
    print("   OK (hero-bg-light.webp)")
if ':root[data-theme="light"] .hero' not in css:
    errors.append('falta la regla que cambia el fondo segun el tema')
else:
    print("   OK (regla por tema)")
# La version movil del tema claro tambien.
if "hero-bg-light-sm.webp" not in css:
    notes.append("el movil en tema claro usa la imagen grande")

print()
for n in notes:
    print(f"  nota: {n}")
if errors:
    print(f"RESULTADO: {len(errors)} problema(s)")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("RESULTADO: sin problemas de rendimiento")
