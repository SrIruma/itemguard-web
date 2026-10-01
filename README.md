# ItemGuard documentation site

The documentation website for [ItemGuard](https://github.com/SrIruma/itemguard),
published at <https://sriruma.github.io/itemguard-web/>.

Plain static files. **No npm, no Node, no build step, no dependencies.**
GitHub Pages serves the repository root, so a push is the deploy. The
two scripts that touch artwork need `sharp`, and nothing else needs
anything installed.

## Running it locally

Use the included server, which behaves like GitHub Pages:

```bash
python3 scripts/serve.py
# http://localhost:8000/itemguard-web/
# a 404 to try it: http://localhost:8000/itemguard-web/no-existe
```

It serves the repository under the `/itemguard-web` prefix and hands out
the site's own `404.html` with a 404 status, choosing the Spanish one for
paths under `/es/`.

A plain `python3 -m http.server` is not equivalent, and the difference
matters: it answers a missing path with its own "Error response" page and
never shows the site's 404, so you cannot tell a working 404 from a
broken one. It also serves the repository at the root, where every
absolute path on the site 404s because they all start with
`/itemguard-web/`.

There is nothing to install and nothing to compile.

## Layout

```
index.html              landing page, English
docs/*.html             documentation, English
404.html                not-found page, also the map of old URLs
search-index.json       English search index

es/index.html           landing page, Spanish
es/docs/*.html          documentation, Spanish
es/404.html             not-found page, Spanish
es/search-index.json    Spanish search index

content/es/*.html       the Spanish article bodies, before they are wrapped
sitemap.xml, robots.txt, .nojekyll

assets/css/style.css    the whole design system
assets/js/site.js       navigation, titles, and every interface string
assets/js/app.js        theme, search, table of contents, mobile nav
assets/img/logo.png     the mark, 256 px, 24 KB
assets/img/favicon.svg  the same mark as vector, for the tab
assets/img/favicon-32.png, apple-touch-icon.png   raster icons
assets/img/hero-bg.webp       hero background, night, 6 KB
assets/img/hero-bg-sm.webp    the same, 3 KB, for phones
assets/img/hero-bg-light.webp       the day version, 5 KB
assets/img/hero-bg-light-sm.webp    the same, 3 KB, for phones

scripts/build.py          regenerates both trees and both search indexes
scripts/build-es.py       writes content/es/ from the translations in it
scripts/serve.py          local server that mimics GitHub Pages
scripts/check-all.sh      every check, in order
scripts/check-html.py     the generated HTML
scripts/check-perf.py     paint cost and image weight
scripts/check-responsive.py  breakpoints, touch targets, the drawer
scripts/make-hero-bg.js   redraws the hero background, both themes
scripts/make-icons.js     recuts the icons from logo.png
```

The two generator scripts need `sharp`, and only when you change the
artwork:

```bash
npm install --no-save sharp
node scripts/make-icons.js
node scripts/make-hero-bg.js
```

Everything else is Python 3 and the standard library.

`logo.png` is the source of the mark. `favicon-32.png` and
`apple-touch-icon.png` are cut from it; regenerate them after replacing
it. The 1254 px original is 1.3 MB, which is why nothing loads it
directly: the header uses a 28 px copy, and the browser tab gets the
small ones.

The hero background is drawn pixel by pixel by `scripts/make-hero-bg.js`
and committed, in two versions: a night scene and a day one, with the
same composition and the same terrain silhouette and only the light
changed. The light theme needs its own, because the night one behind a
light veil goes to a flat white and the scene disappears. To change
either, edit the `NIGHT` or `DAY` palette at the top of that script and
re-run it.

It is original art on a block grid, not a Minecraft texture: Mojang's
assets are theirs, and this is the website of a paid plugin.

Text contrast on the hero is measured, not assumed: the veil density is
staggered so the sky stays visible at the top and the ground darkens
where the paragraph sits, and `.hero-lead` carries its own darker
`--muted` because the page's muted text drops to 3.2:1 on the day
ground. Every position clears AA.

### Performance

`python3 scripts/check-perf.py` guards three things that were real
problems here and are easy to reintroduce:

- **No stacked gradients in the hero.** It was six of them, which
  repaints on every frame. It is one 6 KB image now.
- **One `backdrop-filter` at most.** The search overlay had one over
  the whole viewport; it is an opaque veil now, which looks the same
  over a flat background and costs nothing.
- **Three infinite animations, and nothing animating the background.**
  Moving `background-position` repaints continuously; the drifting
  clouds that did that are gone, the image is static.

`logo.png` is the source of the mark. `favicon-32.png` and
`apple-touch-icon.png` are cut from it; regenerate them after replacing
it. The 1254 px original is 1.3 MB, which is why nothing loads it
directly: the header uses a 28 px copy, and the browser tab gets the
small ones.

## Languages

The site has two trees, and both are plain static files:

```
/                        landing page, English
/docs/<slug>.html        documentation, English
/es/                     landing page, Spanish
/es/docs/<slug>.html     documentation, Spanish
```

Each page is a real file in its own language, not a string swap at
runtime. The EN/ES control in the header navigates to the same page in
the other language, and the URL says which one you are reading. That
means the Spanish text is there for search engines, for readers with
JavaScript off, and for anyone who lands on it from a shared link.

Each tree has its own `search-index.json`, so searching `reclaim` in
English and `reclamo` in Spanish are two different searches over two
different files.

## Editing a page

**English.** `docs/<slug>.html` is a complete page: head, topbar,
sidebar, article, table of contents, previous/next. Write the content in
the `<article class="doc-body">` element and leave the rest alone.

**Spanish.** `content/es/<slug>.html` holds only the article body, the
same markup with the text translated. The page around it is generated.
After editing either language, regenerate:

```bash
python3 scripts/build.py
```

It rewraps both trees and rebuilds both search indexes.

Two things are generated, and both are committed, so you never need to
run anything to deploy a change:

- **The `id` on each `h2` and `h3`.** The table of contents is built from
  these in the browser. If you add a heading to an English page by hand,
  give it an `id` yourself, or re-run `python3 scripts/build.py` to add
  them.
- **Both `search-index.json` files.** Built from the text of the pages.
  If you change wording people will search for, re-run
  `python3 scripts/build.py`.

The `<h1>` is also generated, from the title in `site.js`, and the build
strips any `h1` found in the content. That is deliberate: the English
pages inherited theirs from the old hand-written site, the Spanish ones
were written without one, and a page whose title depends on which
translation you start from is a page that will lose its title. Add the
title to `site.js` and both languages get it.

### After any change

```bash
python3 scripts/build.py
python3 scripts/check-html.py
```

`check-html.py` catches what a diff will not: residual indentation from
a source file that was itself generated, a duplicate or missing `h1`, a
heading that stayed in the wrong language, a title that appears after a
section heading, an incomplete icon set, and unbalanced tags.

## Conventions when you edit

- **Titles and descriptions live in `assets/js/site.js`**, under `pages`.
  That file is the single source for the sidebar, the breadcrumb,
  previous/next, and the `<title>` of each page. Add a page there and it
  appears in the navigation everywhere at once. The old site copied the
  sidebar into all twelve pages, which is the thing this avoids.
- **Interface text is in `assets/js/site.js` too**, under `i18n`. The
  chrome decides the language from the URL, not from a stored
  preference, so the EN/ES control always lands on the same page in the
  other language.
- **Page titles and descriptions live in `assets/js/site.js`**, under
  `pages`, with an `en` and an `es` string each. Both trees read from
  there, so a title is written once in two languages.
- **The base path is `/itemguard-web`.** It is hardcoded in
  `scripts/build.py`, in `index.html`, in `es/index.html`, in both
  `404.html` files and in `assets/js/app.js`. If the repo is ever
  renamed, all of them change.

## Publishing the listing

The plugin is a paid one and the BuiltByBit listing is still in review.
The Buy button exists on both landing pages and is styled like one, but
it carries `aria-disabled="true"` and a `URL_DE_LA_FICHA` placeholder,
so it looks like the button that is coming without being a dead link.

When the listing goes live:

1. Replace `URL_DE_LA_FICHA` with the real URL in `index.html` and in
   `es/index.html` (the Buy button, the same two places).
2. Remove `aria-disabled="true"` from the Buy button in both.
3. `assets/js/site.js`, under `listing`: set `published: true` and put
   the URL in `url`.

`scripts/check-html.py` fails if the placeholder is left without the
disabled marker, so step 2 cannot be forgotten silently.

## Reporting problems

The plugin's own repository is private, so nothing on this site links
to it. Two places instead, and both reach the two of you:

- **A public GitHub issue** on this repository, which anyone can open.
- **An email** to MrTsumugi@proton.me, for anything that should not sit
  in a public, searchable record.

Both addresses live in `assets/js/site.js` under `support`, and in
`SUPPORT` in `scripts/build.py`. A section with the two of them is
generated at the bottom of every documentation page and of both 404s.
`check-html.py` fails if either disappears, or if a link to the private
repository reappears.
- **Callouts** are the existing `.note`, `.tip` and `.warn` divs. Keep
  the markup; the styling is already there.
- **Tables** go inside `<div class="table-wrap">` so they scroll sideways
  on a phone instead of dragging the page with them.

## Accessibility and behaviour notes

- Both themes clear WCAG AA for body text, muted text and links. The
  small uppercase labels were the tightest case and were adjusted to
  match; if you change a colour, re-check it.
- The theme is applied by an inline script in `<head>` before the first
  paint, so there is no flash of the wrong theme.
- Search opens with `/` or `Ctrl`/`Cmd`+`K`, navigates with the arrow
  keys, opens with `Enter`, closes with `Esc`.
- `prefers-reduced-motion` disables the smooth scrolling and the
  transitions.
- With JavaScript disabled the pages still render, the links still work,
  and the sidebar falls back to the plain list in its `<noscript>`.

## Deploying

Push to `main`. Pages is set to serve the branch, so the push is the
deploy, and there is no workflow to configure. `.nojekyll` has to stay
at the repository root: without it Jekyll runs, and Jekyll skips any
directory whose name starts with an underscore.

Before pushing:

```bash
./scripts/check-all.sh
```

It runs the three checks, regenerates the tree to confirm it matches
the generator, and looks for broken links.

On the 404: GitHub Pages serves the `404.html` at the repository root,
so `404.html` covers every missing path, including under `/es/`. The
Spanish 404 at `es/404.html` is there for review and for a future switch
to per-language handling, but Pages will not pick it automatically.
Serving `/es/…` to the English page is a real limitation, not a bug to
chase.
