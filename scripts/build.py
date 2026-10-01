#!/usr/bin/env python3
"""
Genera el sitio estatico de ItemGuard, en ingles y en espanol. Sin npm,
sin Node, sin build step.

Que hace:
  - envuelve el contenido de cada pagina en la chrome (topbar, sidebar,
    toc, pager), de modo que el HTML queda corto y la navegacion vive en
    un solo sitio (assets/js/site.js);
  - anade ids a las cabeceras para el indice lateral;
  - construye search-index.json, uno por idioma, a partir del texto ya
    renderizado.

Los arboles que produce:
    /                      portada en ingles
    /docs/<slug>.html      documentacion en ingles
    /es/                   portada en espanol
    /es/docs/<slug>.html   documentacion en espanol

    python3 scripts/build.py
"""
import html
import json
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "/itemguard-web"

SLUGS = [
    "quickstart", "commands", "flags", "templates", "ownership", "seals",
    "permissions", "configuration", "translations", "screens", "database", "faq",
]

# El ingles vive en los docs/*.html ya generados; el espanol, en
# content/es/<slug>.html. Un solo punto de entrada por idioma.
# "base" son las URL de las paginas, que viven en un subdirectorio por
# idioma. "assets" es la raiz del sitio: los ficheros compartidos estan
# una sola vez, no duplicados bajo /es/.
LANGS = {
    "en": {
        "content": ROOT / "docs",
        "out": ROOT / "docs",
        "base": BASE + "/docs",
        "assets": BASE,
        "home": BASE + "/",
    },
    "es": {
        "content": ROOT / "content" / "es",
        "out": ROOT / "es" / "docs",
        "base": BASE + "/es/docs",
        "assets": BASE,
        "home": BASE + "/es/",
    },
}


def read_site_meta() -> tuple[dict, dict]:
    """Titulos y descripciones, leidos del unico sitio donde se declaran."""
    js = (ROOT / "assets" / "js" / "site.js").read_text(encoding="utf-8")
    titles: dict[str, str] = {}
    descs: dict[str, str] = {}
    for slug in SLUGS:
        m = re.search(rf'{slug}: \{{(.*?)\n    \}}', js, re.DOTALL)
        block = m.group(1) if m else ""
        t = re.search(r'title: \{ en: "([^"]+)"', block)
        d = re.search(r'en:\s*"([^"]+)",', block)
        titles[slug] = t.group(1) if t else slug
        descs[slug] = d.group(1) if d else ""
    return titles, descs


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = re.sub(r"[\u0300-\u036f]", "", text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:60]


HEAD = """<!DOCTYPE html>
<html lang="{lang}" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · ItemGuard</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0d1117">
<meta property="og:title" content="{title} · ItemGuard">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
{alternate}<link rel="icon" href="{assets}/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{assets}/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{assets}/assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="{assets}/assets/css/style.css">
<script>
/* Se aplica el tema antes del primer pintado, para que no haya destello. */
(function () {{
  try {{
    var t = localStorage.getItem('ig-theme');
    if (t !== 'light' && t !== 'dark') {{
      t = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
    }}
    document.documentElement.setAttribute('data-theme', t);
  }} catch (e) {{
    document.documentElement.setAttribute('data-theme', 'dark');
  }}
}})();
</script>
<script src="{assets}/assets/js/site.js"></script>
</head>
<body data-page="{slug}">
<a class="skip-link" href="#main">{skip}</a>

<header class="topbar">
  <div class="topbar-inner">
    <button id="menu-toggle" class="icon-btn" aria-label="{menu}" aria-expanded="false">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <a class="brand" href="{home}">
      <img class="brand-mark" src="{assets}/assets/img/logo.png" alt="" width="28" height="28">
      <span class="brand-text">ItemGuard</span>
    </a>
    <div class="topbar-spacer"></div>
    <div class="topbar-actions">
      <button class="search-trigger" data-search-open aria-label="{search}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
        <span>{search}</span>
        <kbd>/</kbd>
      </button>
      <div class="lang-switch" id="lang-switch" role="group" aria-label="{languages}"></div>
      <a class="author-link" href="https://github.com/SrIruma" target="_blank" rel="noopener" title="{author_role}">
        <svg class="gh" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 00-3.16 19.49c.5.09.68-.22.68-.48l-.01-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.16-1.11-1.47-1.11-1.47-.9-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.9 1.52 2.34 1.08 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.56-1.11-4.56-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.64 0 0 .84-.27 2.75 1.02a9.5 9.5 0 015 0c1.91-1.29 2.75-1.02 2.75-1.02.55 1.37.2 2.39.1 2.64.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.69-4.57 4.94.36.31.68.92.68 1.85l-.01 2.75c0 .27.18.58.69.48A10 10 0 0012 2z"/></svg>
        <span class="name">SrIruma</span>
      </a>
      <button id="theme-toggle" class="icon-btn" aria-label="{theme}">
        <svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.4M12 19.1v2.4M2.5 12h2.4M19.1 12h2.4M5.3 5.3l1.7 1.7M17 17l1.7 1.7M18.7 5.3L17 7M7 17l-1.7 1.7"/></svg>
        <svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.5 14.2A8.5 8.5 0 019.8 3.5 8.5 8.5 0 1020.5 14.2z"/></svg>
      </button>
    </div>
  </div>
</header>

<div class="layout">
  <nav class="sidebar" aria-label="{docs}">
    <div id="sidebar-nav">
      <noscript>
        <p class="sidebar-label">{docs}</p>
{fallback}
      </noscript>
    </div>
  </nav>

  <main class="content" id="main">
    <nav class="breadcrumb" id="breadcrumb" aria-label="Breadcrumb"></nav>
    <div class="content-inner">
      <article class="doc-body">
<h1>{title}</h1>
{body}
      </article>
      <aside class="toc" id="toc" aria-label="{onthispage}">
        <p class="toc-label">{onthispage}</p>
        <nav id="toc-nav"></nav>
      </aside>
    </div>
    <section class="support">
      <h2>{report}</h2>
      <p class="support-lead">{reportlead}</p>
      <div class="support-grid">
        <a class="support-card" href="{support_issues}">
          <h3>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.2"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/></svg>
            {report_issue}
          </h3>
          <p>{report_issue_desc}</p>
          <span class="card-more">{search_first} →</span>
        </a>
        <a class="support-card" href="mailto:{support_email}">
          <h3>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6 8.5-6"/></svg>
            {report_email}
          </h3>
          <p>{report_email_desc}</p>
          <span class="card-more">{support_email} →</span>
        </a>
      </div>
    </section>

    <nav class="pager" id="pager" aria-label="{prev} / {next}"></nav>
  </main>
</div>

<div class="search-overlay" id="search-overlay" role="dialog" aria-modal="true" aria-label="{search}">
  <div class="search-box">
    <div class="search-field">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
      <input id="search-input" type="search" placeholder="{searchph}" autocomplete="off" spellcheck="false">
      <kbd>Esc</kbd>
    </div>
    <div class="search-hint" id="search-hint"></div>
    <div class="search-results" id="search-results"></div>
    <div class="search-foot">
      <span><kbd>&uarr;</kbd><kbd>&darr;</kbd> {navigate}</span>
      <span><kbd>Enter</kbd> {open}</span>
      <span><kbd>Esc</kbd> {close}</span>
    </div>
  </div>
</div>

<footer class="site-footer">
  <div class="footer-inner">
    <p>ItemGuard · by <a href="https://github.com/SrIruma" target="_blank" rel="noopener">SrIruma</a> &amp; SrPinkyy</p>
    <p class="footer-note">{footernote}</p>
  </div>
</footer>

<script src="{assets}/assets/js/app.js"></script>
</body>
</html>
"""

# Textos de la chrome, por idioma. El cuerpo de la pagina viene
# traducido aparte; aqui solo lo que la chrome muestra.
SUPPORT = {
    "issues": "https://github.com/SrIruma/itemguard-web/issues",
    "email": "MrTsumugi@proton.me",
}

CHROME = {
    "en": {
        "skip": "Skip to content", "menu": "Menu", "search": "Search",
        "searchph": "Search the docs…", "languages": "Language",
        "author_role": "author &amp; maintainer", "theme": "Toggle theme",
        "docs": "Documentation", "onthispage": "On this page",
        "prev": "Previous", "next": "Next", "navigate": "navigate",
        "open": "open", "close": "close",
        "footernote": "Documentation for the Paper 1.21 plugin.",
        "report": "Report a problem",
        "reportlead": "Something not working, or behaving in a way you did not expect?",
        "report_issue": "Open an issue",
        "report_issue_desc": "Public GitHub issues on the documentation site. Search first: it may already be known.",
        "report_email": "Email us",
        "report_email_desc": "Reaches both of us. Slow, but it works without an account.",
        "search_first": "Search the issues first",
    },
    "es": {
        "skip": "Ir al contenido", "menu": "Menú", "search": "Buscar",
        "searchph": "Buscar en la documentación…", "languages": "Idioma",
        "author_role": "autor y mantenedor", "theme": "Cambiar tema",
        "docs": "Documentación", "onthispage": "En esta página",
        "prev": "Anterior", "next": "Siguiente", "navigate": "moverse",
        "open": "abrir", "close": "cerrar",
        "footernote": "Documentación del plugin para Paper 1.21.",
        "report": "Reporta un problema",
        "reportlead": "¿Algo no funciona, o se comporta de una forma que no esperabas?",
        "report_issue": "Abrir un issue",
        "report_issue_desc": "Issues públicos de GitHub en el sitio de documentación. Busca antes: puede que ya esté conocido.",
        "report_email": "Escríbenos",
        "report_email_desc": "Llega a los dos. Más lento, pero funciona sin cuenta.",
        "search_first": "Busca primero en los issues",
    },
}


def read_body(path: pathlib.Path) -> str:
    """El cuerpo de la pagina: en ingles es el <article>, en espanol el fichero."""
    if path.suffix == ".html" and "content" not in path.parts:
        raw = path.read_text(encoding="utf-8")
        m = re.search(r'<article class="doc-body">(.*?)</article>', raw, re.DOTALL)
        if m:
            return m.group(1).strip()
        m = re.search(r"<article>(.*?)</article>", raw, re.DOTALL)
        if m:
            return m.group(1).strip()
    return path.read_text(encoding="utf-8").strip()


def label_table_cells(body: str) -> str:
    """
    Copia el texto de cada <th> a las <td> correspondientes, como
    data-label.

    Es lo que permite apilar la tabla en movil sin scroll horizontal:
    en una pantalla estrecha cada fila se convierte en una tarjeta y
    cada celda muestra el nombre de su columna delante. Una tabla de
    cuatro columnas con comandos largos no se lee desplazandola de
    lado; se lee, simplemente no cabe.
    """
    def fix(m: re.Match) -> str:
        table = m.group(0)
        head = re.search(r"<thead>(.*?)</thead>", table, re.DOTALL)
        if not head:
            return table
        labels = [
            re.sub(r"<[^>]+>", "", h).strip()
            for h in re.findall(r"<th[^>]*>(.*?)</th>", head.group(1), re.DOTALL)
        ]
        if len(labels) < 2:
            return table

        def row(r: re.Match) -> str:
            cells = re.findall(r"<td[^>]*>(.*?)</td>", r.group(1), re.DOTALL)
            if len(cells) != len(labels):
                return r.group(0)  # fila con menos celdas: no se toca
            out = r.group(0)
            for i, cell in enumerate(cells):
                out = out.replace(
                    f"<td>{cell}",
                    f'<td data-label="{html.escape(labels[i], quote=True)}">{cell}',
                    1,
                )
            return out

        body_rows = re.search(r"<tbody>(.*?)</tbody>", table, re.DOTALL)
        if not body_rows:
            return table
        new_body = re.sub(r"<tr>(.*?)</tr>", row, body_rows.group(1), flags=re.DOTALL)
        return table[: body_rows.start(1)] + new_body + table[body_rows.end(1) :]

    return re.sub(r"<table>.*?</table>", fix, body, flags=re.DOTALL)


def normalise_indent(body: str) -> str:
    """
    Quita la sangria residual de las lineas que vienen de un fichero
    con sangria propia.

    Cuatro espacios al principio hacen que Markdown y algunos
    navegadores lean la linea como bloque de codigo, y en una tabla se
    traduce en filas que se salen de sitio. Solo se toca lo que no es
    contenido de <pre>, donde la sangria es parte del ejemplo.
    """
    out = []
    in_pre = False
    for line in body.split("\n"):
        if "<pre>" in line:
            in_pre = True
        if in_pre:
            out.append(line)
            if "</pre>" in line:
                in_pre = False
            continue
        out.append(line.lstrip(" \t") if line.strip() else "")
    text = "\n".join(out)
    # Las lineas en blanco de mas se van: dentro del article producen
    # separacion visible entre parrafos que no esta en el original.
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def add_ids(body: str) -> str:
    """Pone ids a las cabeceras y quita el h1 del cuerpo.

    El h1 lo pone la plantilla desde el titulo de site.js, no el
    contenido. Asi los dos idiomas lo tienen siempre, y no puede
    pasar que una traduccion lo traiga y otra no.
    """
    body = re.sub(r"\s*<h1[^>]*>.*?</h1>\s*", "\n", body, count=1, flags=re.DOTALL)
    body = normalise_indent(body)
    used: set[str] = set()

    def repl(m: re.Match) -> str:
        tag, inner = m.group(1), m.group(2)
        text = re.sub(r"<[^>]+>", "", inner).strip()
        base = slugify(text) or "section"
        sid = base
        n = 2
        while sid in used:
            sid = f"{base}-{n}"
            n += 1
        used.add(sid)
        return f'<{tag} id="{sid}">{inner}</{tag}>'

    return re.sub(r"<(h[23])>(.*?)</\1>", repl, body, flags=re.DOTALL)


def strip_text(body: str) -> str:
    s = re.sub(r"<script.*?</script>", " ", body, flags=re.DOTALL)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.DOTALL)
    s = re.sub(r"<(h[1-6])[^>]*>(.*?)</\1>", r" \2 ", s, flags=re.DOTALL)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def extract_headings(body: str) -> str:
    return " ".join(
        re.sub(r"<[^>]+>", "", m.group(2)).strip()
        for m in re.finditer(r"<(h[23])[^>]*>(.*?)</\1>", body, re.DOTALL)
    )


def main() -> int:
    titles, descs = read_site_meta()
    js = (ROOT / "assets" / "js" / "site.js").read_text(encoding="utf-8")

    for lang, cfg in LANGS.items():
        ch = CHROME[lang]
        out_dir = cfg["out"]
        out_dir.mkdir(parents=True, exist_ok=True)

        fallback = "\n".join(
            f'        <a href="{cfg["base"]}/{s}.html">{html.escape(titles[s])}</a>'
            for s in SLUGS
        )

        search_docs = []
        written = []

        for slug in SLUGS:
            src = cfg["content"] / f"{slug}.html"
            if not src.exists():
                print(f"  AVISO falta {src}", file=sys.stderr)
                continue

            body = add_ids(read_body(src))
            body = label_table_cells(body)
            title = titles[slug]
            desc = descs[slug]

            # El titulo y la descripcion traducidos salen de site.js.
            if lang == "es":
                m = re.search(
                    rf'{slug}: \{{(.*?)\n    \}}', js, re.DOTALL
                )
                block = m.group(1) if m else ""
                tm = re.search(r'es: "([^"]+)"', block)
                dm = re.search(r'es:\s*"([^"]+)"', block)
                if tm:
                    title = tm.group(1)
                if dm:
                    desc = dm.group(1)

            other = "es" if lang == "en" else "en"
            alt_base = LANGS[other]["base"]
            home = cfg["home"]
            alternate = (
                f'<link rel="alternate" hreflang="{other}" '
                f'href="https://sriruma.github.io{alt_base}/{slug}.html">\n'
                f'<link rel="alternate" hreflang="x-default" '
                f'href="https://sriruma.github.io{BASE}/docs/{slug}.html">\n'
            )

            out = HEAD.format(
                base=cfg["base"],
                assets=cfg["assets"],
                home=home,
                support_issues=SUPPORT["issues"],
                support_email=SUPPORT["email"],
                lang=lang,
                slug=slug,
                title=html.escape(title),
                desc=html.escape(desc, quote=True),
                alternate=alternate,
                body=body,
                fallback=fallback,
                **ch,
            )
            (out_dir / f"{slug}.html").write_text(out, encoding="utf-8")
            written.append(slug)

            search_docs.append({
                "s": slug,
                "t": title.lower(),
                "T": title,
                "h": extract_headings(body).lower(),
                "b": strip_text(body).lower()[:4000],
            })

        (out_dir.parent / "search-index.json").write_text(
            json.dumps({"lang": lang, "docs": search_docs},
                       ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        print(f"{lang}: {len(written)} paginas en {out_dir.relative_to(ROOT)}/")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
