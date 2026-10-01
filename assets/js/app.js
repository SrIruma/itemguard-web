/* ============================================================
   ItemGuard docs — behaviour.

   No framework, no build, no npm. Four jobs:

     1. theme       dark/light, applied before first paint
     2. chrome      sidebar, breadcrumb and previous/next, all
                    rendered from window.IG_SITE so the HTML files
                    stay free of duplicated navigation
     3. toc         the right-hand index that follows the scroll
     4. search      client-side, over a JSON index built at commit time

   Everything degrades: with JavaScript off the pages still render,
   the sidebar falls back to its noscript list, and links still work.
   ============================================================ */

(function () {
  "use strict";

  var site = window.IG_SITE;
  var LANG_KEY = "ig-lang";
  var THEME_KEY = "ig-theme";
  var BASE = "/itemguard-web";

  /* ---------- language ------------------------------------ */

  /* ---------- language ------------------------------------
     El idioma se resuelve una vez y se aplica a toda la pagina:
     el conmutador navega a la otra version, porque el texto vive en
     paginas distintas y no en un intercambio de cadenas. Asi el
     contenido en español existe aunque el visitante llegue con
     JavaScript desactivado, y la URL dice en que idioma esta. */

  var lang = "en";

  function resolveLang() {
    // La URL manda: /es/ es español aunque el navegador pida inglés.
    if (location.pathname.indexOf(BASE + "/es/") === 0) return "es";
    return document.documentElement.getAttribute("lang") === "es" ? "es" : "en";
  }

  /* Intercambia el prefijo de idioma de la ruta actual.
       /itemguard-web/docs/x.html  <->  /itemguard-web/es/docs/x.html
       /itemguard-web/             <->  /itemguard-web/es/
     El idioma se deduce de la URL, no de una variable guardada: asi el
     conmutador acierta aunque alguien llegue a una URL de español con
     el navegador en inglés. */
  function otherLangPath(to) {
    var path = location.pathname;
    var isEs = path.indexOf(BASE + "/es/") === 0;

    if (isEs) {
      return to === "en" ? path.replace(BASE + "/es/", BASE + "/") : path;
    }
    return to === "es" ? path.replace(BASE + "/", BASE + "/es/") : path;
  }

  function t(key) {
    var table = site.i18n[lang] || site.i18n.en;
    return table[key] || site.i18n.en[key] || key;
  }

  function pageMeta(slug) {
    var p = site.pages[slug];
    if (!p) return { title: slug, desc: "" };
    return {
      title: p.title[lang] || p.title.en,
      desc: p.desc[lang] || p.desc.en,
    };
  }

  /* ---------- theme --------------------------------------- */

  function currentTheme() {
    try {
      var s = localStorage.getItem(THEME_KEY);
      if (s === "light" || s === "dark") return s;
    } catch (e) {}
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches
      ? "light"
      : "dark";
  }

  function paintTheme() {
    var t = currentTheme();
    document.documentElement.setAttribute("data-theme", t);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", t === "dark" ? "#0d1117" : "#f7f8fa");
  }

  function initTheme() {
    paintTheme();
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var next =
        document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
      paintTheme();
    });
  }

  /* ---------- icons --------------------------------------- */

  var ICONS = {
    rocket: '<path d="M12 2c3 2 5 5.5 5 9l-2 2H9l-2-2c0-3.5 2-7 5-9z"/><path d="M9 15l-2 3 3-1M15 15l2 3-3-1"/><circle cx="12" cy="9" r="1.6"/>',
    terminal: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9l3 3-3 3M13 15h4"/>',
    sliders: '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
    layers: '<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>',
    user: '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
    lock: '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 018 0v3"/>',
    key: '<circle cx="8" cy="14" r="4"/><path d="M11 11l9-9M17 5l2 2M15 7l2 2"/>',
    globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 3 2.5 15 0 18M12 3c-2.5 3-2.5 15 0 18"/>',
    grid: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    database: '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6"/><path d="M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>',
    help: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 113.5 2.3c-.7.3-1 .9-1 1.7v.5"/><circle cx="12" cy="17" r=".6" fill="currentColor"/>',
  };

  function icon(name) {
    var d = ICONS[name] || ICONS.help;
    return (
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" ' +
      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + "</svg>"
    );
  }

  /* ---------- flat order, for previous/next ---------------- */

  function flatPages() {
    var out = [];
    site.groups.forEach(function (g) {
      g.items.forEach(function (it) { out.push(it.slug); });
    });
    return out;
  }

  var SLUG = document.body.getAttribute("data-page") || "";
  var ORDER = flatPages();

  // La URL de una pagina depende del idioma: el sitio tiene dos
  // arboles, /docs/ en ingles y /es/docs/ en español.
  function urlFor(slug) {
    return lang === "es"
      ? BASE + "/es/docs/" + slug + ".html"
      : BASE + "/docs/" + slug + ".html";
  }

  /* ---------- sidebar, breadcrumb, pager ------------------- */

  function buildSidebar() {
    var nav = document.getElementById("sidebar-nav");
    if (!nav) return;
    var html = "";
    site.groups.forEach(function (g) {
      html += '<div class="sidebar-group"><p class="sidebar-label">' +
        (g.label[lang] || g.label.en) + "</p>";
      g.items.forEach(function (it) {
        var p = site.pages[it.slug] || {};
        var m = pageMeta(it.slug);
        var cur = it.slug === SLUG;
        // El icono vive en pages[slug].icon, no en el item del grupo.
        // Sin esto salia el icono de interrogacion en toda la barra.
        html +=
          '<a href="' + urlFor(it.slug) + '"' +
          (cur ? ' aria-current="page"' : "") + ">" +
          icon(p.icon) + "<span>" + m.title + "</span></a>";
      });
      html += "</div>";
    });
    nav.innerHTML = html;
  }

  function buildBreadcrumb() {
    var el = document.getElementById("breadcrumb");
    if (!el) return;
    var m = pageMeta(SLUG);
    var group = "";
    site.groups.forEach(function (g) {
      g.items.forEach(function (it) { if (it.slug === SLUG) group = g.label[lang] || g.label.en; });
    });
    el.innerHTML =
      '<a href="' + (lang === "es" ? BASE + "/es/" : BASE + "/") + '">' +
      (lang === "es" ? t("docs") : "ItemGuard") + "</a>" +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
      'stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>' +
      (group ? "<span>" + group + "</span>" +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
        'stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>' : "") +
      "<span>" + m.title + "</span>";
  }

  function buildPager() {
    var el = document.getElementById("pager");
    if (!el) return;
    var i = ORDER.indexOf(SLUG);
    if (i === -1) { el.hidden = true; return; }
    var prev = i > 0 ? ORDER[i - 1] : null;
    var next = i < ORDER.length - 1 ? ORDER[i + 1] : null;

    var html = prev
      ? '<a href="' + urlFor(prev) + '"><span>' + t("previous") + "</span><strong>" +
        pageMeta(prev).title + "</strong></a>"
      : '<span class="pager-empty"></span>';
    html += next
      ? '<a class="pager-next" href="' + urlFor(next) + '"><span>' + t("next") +
        "</span><strong>" + pageMeta(next).title + "</strong></a>"
      : '<span class="pager-empty"></span>';
    el.innerHTML = html;
  }

  function buildLangSwitch() {
    var el = document.getElementById("lang-switch");
    if (!el) return;
    ["en", "es"].forEach(function (code) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = code.toUpperCase();
      b.setAttribute("aria-pressed", String(code === lang));
      if (code !== lang) {
        // Es un enlace de verdad: se ve la URL de destino, se puede
        // abrir en otra pestaña y funciona con el boton central.
        b.setAttribute("role", "link");
        b.setAttribute("href", otherLangPath(code));
        b.addEventListener("click", function (e) {
          e.preventDefault();
          try { localStorage.setItem(LANG_KEY, code); } catch (e) {}
          location.href = otherLangPath(code);
        });
      } else {
        b.setAttribute("aria-current", "true");
      }
      el.appendChild(b);
    });
  }

  /* ---------- table of contents --------------------------- */

  function slugify(text) {
    return text
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 60);
  }

  function initToc() {
    var body = document.querySelector(".doc-body");
    var toc = document.getElementById("toc-nav");
    if (!body || !toc) return;

    // Give every heading a stable id, then list h2 and h3.
    var heads = [];
    body.querySelectorAll("h2, h3").forEach(function (h, idx) {
      if (!h.id) h.id = slugify(h.textContent) || "section-" + idx;
      var a = document.createElement("a");
      a.href = "#" + h.id;
      a.textContent = h.textContent;
      if (h.tagName === "H3") a.className = "toc-h3";
      toc.appendChild(a);
      heads.push({ el: h, a: a });
    });

    if (!heads.length) {
      var host = document.getElementById("toc");
      if (host) host.hidden = true;
      return;
    }

    // Which heading is "current": the last one whose top has passed the
    // reading line. A single scroll listener, no rAF loop.
    var line = 120;
    var current = null;
    function update() {
      var next = heads[0];
      for (var i = 0; i < heads.length; i++) {
        if (heads[i].el.getBoundingClientRect().top <= line) next = heads[i];
        else break;
      }
      // At the very bottom, highlight the last heading: otherwise a short
      // final section can never become active.
      if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 8) {
        next = heads[heads.length - 1];
      }
      if (next !== current) {
        if (current) current.a.classList.remove("is-active");
        next.a.classList.add("is-active");
        current = next;
      }
    }
    var ticking = false;
    window.addEventListener(
      "scroll",
      function () {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function () { update(); ticking = false; });
      },
      { passive: true }
    );
    window.addEventListener("resize", update, { passive: true });
    update();
  }

  /* ---------- heading anchors ----------------------------- */

  function addHeadingAnchors() {
    var body = document.querySelector(".doc-body");
    if (!body) return;
    body.querySelectorAll("h2[id], h3[id]").forEach(function (h) {
      var a = document.createElement("a");
      a.className = "h-anchor";
      a.href = "#" + h.id;
      a.setAttribute("aria-label", h.textContent);
      a.textContent = "#";
      h.appendChild(a);
    });
  }

  /* ---------- search -------------------------------------- */

  var index = null;
  var indexPromise = null;

  /* El indice va con el idioma: buscar "reclaim" en la version inglesa
     y "reclamo" en la española son dos búsquedas sobre dos ficheros. */
  function indexUrl() {
    return lang === "es" ? BASE + "/es/search-index.json" : BASE + "/search-index.json";
  }

  function loadIndex() {
    if (indexPromise) return indexPromise;
    // El indice es un fichero estatico. Si falta, el sitio sigue
    // funcionando y el buscador lo dice en vez de fallar en silencio.
    indexPromise = fetch(indexUrl())
      .then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; });
    return indexPromise;
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function escapeRe(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  /* Score a document against the query terms. Title matches weigh more
     than heading matches, which weigh more than body text; an exact
     prefix on a title weighs most of all. */
  function score(doc, terms) {
    var title = doc.t.toLowerCase();
    var heads = doc.h.toLowerCase();
    var body = doc.b.toLowerCase();
    var total = 0;

    for (var i = 0; i < terms.length; i++) {
      var q = terms[i];
      if (!q) continue;
      var inTitle = title.indexOf(q);
      var inHeads = heads.indexOf(q);
      var inBody = body.indexOf(q);
      if (inTitle === -1 && inHeads === -1 && inBody === -1) return 0;

      if (inTitle === 0) total += 120;
      else if (inTitle > 0) total += 60 - Math.min(inTitle, 30);
      if (inHeads > -1) total += 26;
      if (inBody > -1) {
        // A term repeated in the body is a mild positive.
        var n = body.split(q).length - 1;
        total += 8 + Math.min(n, 4) * 2;
      }
      // Whole-word title match beats a substring one.
      if (new RegExp("\\b" + escapeRe(q)).test(title)) total += 24;
    }
    return total;
  }

  function excerpt(doc, terms) {
    var text = doc.b;
    var low = text.toLowerCase();
    var at = -1;
    for (var i = 0; i < terms.length; i++) {
      var p = low.indexOf(terms[i]);
      if (p > -1) { at = p; break; }
    }
    if (at === -1) at = 0;
    var start = Math.max(0, at - 60);
    var slice = text.slice(start, start + 190).trim();
    if (start > 0) slice = "… " + slice;
    if (start + 190 < text.length) slice += " …";

    var html = escapeHtml(slice);
    terms.forEach(function (q) {
      if (!q) return;
      html = html.replace(new RegExp("(" + escapeRe(escapeHtml(q)) + ")", "gi"), "<mark>$1</mark>");
    });
    return html;
  }

  function initSearch() {
    var overlay = document.getElementById("search-overlay");
    if (!overlay) return;
    var input = document.getElementById("search-input");
    var results = document.getElementById("search-results");
    var hint = document.getElementById("search-hint");
    var triggers = document.querySelectorAll("[data-search-open]");
    var cursor = -1;
    var current = [];

    hint.textContent = t("searchHint");

    function open() {
      overlay.classList.add("is-open");
      document.body.classList.add("search-open");
      loadIndex().then(function (data) {
        index = data && data.docs ? data.docs : null;
        if (!index) {
          results.innerHTML = '<div class="search-empty">' + t("noIndex") + "</div>";
        }
      });
      input.focus();
      input.select();
    }

    function close() {
      overlay.classList.remove("is-open");
      document.body.classList.remove("search-open");
      triggers.forEach(function (b) { b.blur(); });
    }

    triggers.forEach(function (b) {
      b.addEventListener("click", function (e) { e.preventDefault(); open(); });
    });

    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) close();
    });

    document.addEventListener("keydown", function (e) {
      if ((e.key === "k" || e.key === "K") && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        open();
        return;
      }
      if (e.key === "/" && !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) {
        e.preventDefault();
        open();
        return;
      }
      if (e.key === "Escape" && overlay.classList.contains("is-open")) close();
    });

    function render() {
      var q = input.value.trim();
      if (!q) {
        results.innerHTML = "";
        cursor = -1;
        return;
      }
      if (!index) {
        results.innerHTML = '<div class="search-empty">' + t("noIndex") + "</div>";
        return;
      }

      var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
      var hits = [];
      for (var i = 0; i < index.length; i++) {
        var s = score(index[i], terms);
        if (s > 0) hits.push({ doc: index[i], s: s });
      }
      hits.sort(function (a, b) { return b.s - a.s; });
      hits = hits.slice(0, 12);
      current = hits;

      if (!hits.length) {
        results.innerHTML =
          '<div class="search-empty">' + t("noResults") + ' "' + escapeHtml(q) + '"</div>';
        return;
      }

      results.innerHTML = hits
        .map(function (h, i) {
          return (
            '<a class="search-hit" href="' + urlFor(h.doc.s) + '">' +
            '<span class="search-hit-title">' + escapeHtml(h.doc.T || h.doc.t) +
            "</span>" +
            '<span class="search-hit-excerpt">' + excerpt(h.doc, terms) + "</span>" +
            "</a>"
          );
        })
        .join("");
      cursor = -1;
    }

    var debounce;
    input.addEventListener("input", function () {
      clearTimeout(debounce);
      debounce = setTimeout(render, 70);
    });

    input.addEventListener("keydown", function (e) {
      var hits = results.querySelectorAll(".search-hit");
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        if (!hits.length) return;
        if (cursor >= 0 && hits[cursor]) hits[cursor].classList.remove("is-cursor");
        cursor += e.key === "ArrowDown" ? 1 : -1;
        if (cursor < 0) cursor = hits.length - 1;
        if (cursor >= hits.length) cursor = 0;
        hits[cursor].classList.add("is-cursor");
        hits[cursor].scrollIntoView({ block: "nearest" });
      } else if (e.key === "Enter") {
        var target = cursor >= 0 && hits[cursor] ? hits[cursor] : hits[0];
        if (target) { e.preventDefault(); location.href = target.href; }
      }
    });
  }

  /* ---------- mobile nav ---------------------------------- */

  function initNav() {
    var btn = document.getElementById("menu-toggle");
    if (!btn) return;
    // Hay dos paneles posibles: la sidebar de la documentacion y el
    // menu de secciones del landing. Cada pagina tiene uno, y el boton
    // abre el que exista.
    var panel = document.getElementById("sidebar") || document.getElementById("home-menu");

    function setOpen(open) {
      document.body.classList.toggle("nav-open", open);
      btn.setAttribute("aria-expanded", String(open));
      // Al cerrarlo el foco vuelve al boton que lo abrio. Sin esto se
      // queda en un enlace que ya no se ve.
      if (!open) btn.focus();
    }

    btn.addEventListener("click", function () {
      setOpen(!document.body.classList.contains("nav-open"));
    });

    document.addEventListener("click", function (e) {
      if (!document.body.classList.contains("nav-open")) return;
      if (panel && panel.contains(e.target)) return;
      if (btn.contains(e.target)) return;
      setOpen(false);
    });

    // Un enlace a una seccion dentro del propio landing: se navega y
    // el cajon se cierra, si no el destino queda debajo del velo.
    if (panel && panel.id === "home-menu") {
      panel.addEventListener("click", function (e) {
        if (e.target.closest("a")) setOpen(false);
      });
    }

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) {
        setOpen(false);
      }
      // Tab dentro del cajon no se sale: si se sale, el foco viaja al
      // contenido que esta debajo del velo.
      if (e.key === "Tab" && document.body.classList.contains("nav-open") && panel) {
        var f = panel.querySelectorAll("a[href], button:not([disabled])");
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault(); last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault(); first.focus();
        }
      }
    });

    // Al volver a tamano de escritorio el cajon se queda abierto en el
    // DOM: aria-expanded en false y sin transform que lo esconda.
    window.addEventListener("resize", function () {
      if (window.innerWidth > 900 && document.body.classList.contains("nav-open")) {
        document.body.classList.remove("nav-open");
        btn.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---------- boot ---------------------------------------- */

  function boot() {
    lang = resolveLang();
    buildSidebar();
    buildBreadcrumb();
    buildPager();
    buildLangSwitch();
    initTheme();
    initNav();
    addHeadingAnchors();
    initToc();
    initSearch();
    loadIndex();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
