(function () {
    "use strict";

    /*
     * Community addons listed here are the ones present in the repository's
     * addons/ folder. To publish a new addon, add an entry to this array.
     */
    var ADDONS = [
        {
            file: "SmartSpawnerBridge.jar",
            name: "SmartSpawner Bridge",
            author: "SrIruma, SrPinkyy",
            description: "Protects SmartSpawner spawners with ItemGuard ownership.",
            version: "1.0.0",
            href: "addons/SmartSpawnerBridge.jar"
        }
    ];

    var pages = Array.prototype.slice.call(document.querySelectorAll(".page"));
    var navEl = document.getElementById("nav");
    var navEmpty = document.getElementById("nav-empty");
    var searchEl = document.getElementById("search");
    var menuToggle = document.getElementById("menu-toggle");
    var sidebar = document.getElementById("sidebar");
    var content = document.getElementById("content");

    var linksById = {};

    function escapeHtml(value) {
        return String(value).replace(/[&<>"']/g, function (ch) {
            return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[ch];
        });
    }

    /* ---------------------------------------------------------------- nav --- */

    function buildNav() {
        var groups = [];
        var byName = {};

        pages.forEach(function (page) {
            var groupName = page.dataset.group || "Other";
            var group = byName[groupName];
            if (!group) {
                group = { name: groupName, items: [] };
                byName[groupName] = group;
                groups.push(group);
            }

            var heading = page.querySelector("h1");
            var title = page.dataset.title || (heading ? heading.textContent : page.id);
            page.dataset.title = title;

            group.items.push({ page: page, title: title });
        });

        groups.forEach(function (group) {
            var wrap = document.createElement("div");
            wrap.className = "nav-group";

            var title = document.createElement("div");
            title.className = "nav-title";
            title.textContent = group.name;
            wrap.appendChild(title);

            group.items.forEach(function (item) {
                var link = document.createElement("a");
                link.className = "nav-link";
                link.href = "#" + item.page.id.replace(/^page-/, "");
                link.dataset.page = item.page.id.replace(/^page-/, "");
                link.dataset.title = item.title;
                link.dataset.search = item.title.toLowerCase();
                link.dataset.keywords = (item.page.dataset.keywords || "").toLowerCase();
                link.dataset.content = item.page.textContent.toLowerCase().replace(/\s+/g, " ");
                link.textContent = item.title;
                wrap.appendChild(link);
                linksById[link.dataset.page] = link;
            });

            navEl.appendChild(wrap);
        });
    }

    /* ------------------------------------------------------------ routing --- */

    function pageIdFromHash() {
        return (window.location.hash || "").replace(/^#/, "") || pages[0].id.replace(/^page-/, "");
    }

    function showPage(pageId) {
        var known = false;

        Object.keys(linksById).forEach(function (id) {
            if (id === pageId) known = true;
        });

        if (!known) {
            pageId = pages[0].id.replace(/^page-/, "");
        }

        pages.forEach(function (page) {
            page.classList.toggle("active", page.id === "page-" + pageId);
        });

        Object.keys(linksById).forEach(function (id) {
            linksById[id].classList.toggle("active", id === pageId);
        });

        var active = document.querySelector('.page.active');
        if (active) {
            document.title = "ItemGuard \u2014 " + (active.dataset.title || "Documentation");
        }

        if (window.innerWidth > 880 && content) {
            window.scrollTo({ top: 0, behavior: "auto" });
        }
        if (sidebar) {
            sidebar.classList.remove("open");
        }
    }

    function go(pageId) {
        history.pushState(null, "", "#" + pageId);
        showPage(pageId);
    }

    /* ------------------------------------------------------------- search --- */

    function highlight(el, query) {
        var title = el.dataset.title || el.textContent;
        el.textContent = title;
        if (!query) return;
        var idx = title.toLowerCase().indexOf(query);
        if (idx === -1) return;
        el.innerHTML = escapeHtml(title.slice(0, idx)) +
            "<mark>" + escapeHtml(title.slice(idx, idx + query.length)) + "</mark>" +
            escapeHtml(title.slice(idx + query.length));
    }

    function applySearch() {
        var query = (searchEl.value || "").trim().toLowerCase();
        var visible = 0;

        document.querySelectorAll(".nav-group").forEach(function (group) {
            var groupVisible = 0;

            group.querySelectorAll(".nav-link").forEach(function (link) {
                var hit = !query ||
                    link.dataset.search.indexOf(query) !== -1 ||
                    link.dataset.keywords.indexOf(query) !== -1 ||
                    link.dataset.content.indexOf(query) !== -1;

                link.style.display = hit ? "" : "none";
                highlight(link, query);
                if (hit) groupVisible++;
            });

            group.style.display = groupVisible ? "" : "none";
            visible += groupVisible;
        });

        if (navEmpty) navEmpty.hidden = visible !== 0;
    }

    /* ----------------------------------------------------------- flag filter */

    function applyFlagFilter() {
        var input = document.getElementById("flag-filter");
        if (!input) return;
        var query = (input.value || "").trim().toLowerCase();
        var anyVisible = false;

        document.querySelectorAll(".flag-group").forEach(function (group) {
            var groupVisible = false;

            group.querySelectorAll(".flag-table tbody tr").forEach(function (row) {
                var hit = !query || row.textContent.toLowerCase().indexOf(query) !== -1;
                row.style.display = hit ? "" : "none";
                if (hit) groupVisible = true;
            });

            group.classList.toggle("hidden", !groupVisible);
            if (groupVisible) anyVisible = true;
        });

        var empty = document.getElementById("flag-empty");
        if (empty) empty.hidden = anyVisible;
    }

    /* --------------------------------------------------------------- addons -- */

    function renderAddons() {
        var body = document.getElementById("addons-body");
        if (!body) return;

        if (!ADDONS.length) {
            body.innerHTML = '<tr><td colspan="4" class="muted">No addons published yet.</td></tr>';
            return;
        }

        body.innerHTML = ADDONS.map(function (addon) {
            var label = escapeHtml(addon.name) + ' <span class="muted">v' + escapeHtml(addon.version) + "</span>";
            return "<tr>" +
                "<td>" + label + "<br><code>" + escapeHtml(addon.file) + "</code></td>" +
                "<td>" + escapeHtml(addon.author) + "</td>" +
                "<td>" + escapeHtml(addon.description) + "</td>" +
                '<td><a class="btn" href="' + escapeHtml(addon.href) + '" download>Download</a></td>' +
                "</tr>";
        }).join("");
    }

    /* --------------------------------------------------------------- events -- */

    document.addEventListener("click", function (event) {
        var link = event.target.closest("a");
        if (!link) return;

        if (link.classList.contains("nav-link")) {
            event.preventDefault();
            go(link.dataset.page);
            return;
        }

        if (link.dataset && link.dataset.goto) {
            event.preventDefault();
            go(link.dataset.goto);
        }
    });

    if (searchEl) {
        searchEl.addEventListener("input", function () {
            if (window.innerWidth <= 880 && sidebar && searchEl.value.trim()) {
                sidebar.classList.add("open");
            }
            applySearch();
        });
        searchEl.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();
                var first = navEl.querySelector('.nav-link:not([style*="display: none"])');
                if (first) {
                    go(first.dataset.page);
                    searchEl.blur();
                }
            } else if (event.key === "Escape") {
                searchEl.value = "";
                applySearch();
                searchEl.blur();
            }
        });
    }

    var flagFilter = document.getElementById("flag-filter");
    if (flagFilter) {
        flagFilter.addEventListener("input", applyFlagFilter);
    }

    if (menuToggle && sidebar) {
        menuToggle.addEventListener("click", function () {
            sidebar.classList.toggle("open");
        });
    }

    window.addEventListener("popstate", function () {
        showPage(pageIdFromHash());
    });

    window.addEventListener("hashchange", function () {
        showPage(pageIdFromHash());
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "/" && document.activeElement.tagName !== "INPUT") {
            event.preventDefault();
            if (searchEl) searchEl.focus();
        }
    });

    /* ---------------------------------------------------------------- init --- */

    buildNav();
    renderAddons();
    showPage(pageIdFromHash());
    applySearch();
})();
