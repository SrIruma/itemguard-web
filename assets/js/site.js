/* ============================================================
   ItemGuard docs — navegación y metadatos.

   Este archivo es la ÚNICA fuente de la sidebar, del breadcrumb, del
   anterior/siguiente y del índice de búsqueda. Las páginas HTML lo
   cargan por fetch y lo pintan al vuelo.

   Por qué: antes el sidebar y el footer estaban copiados en las once
   páginas. Añadir una página obligaba a editar once ficheros, y
   cualquier olvido dejaba la navegación desincronizada. Aquí se edita
   una vez.
   ============================================================ */

window.IG_SITE = {
  /* El repositorio del plugin es privado: nadie puede abrir un issue
     ahi ni ver el codigo. Asi que el sitio de reporte es el repo de
     esta misma web, que es publico y si tiene issues abiertos. */
  support: {
    issues: "https://github.com/SrIruma/itemguard-web/issues",
    newIssue: "https://github.com/SrIruma/itemguard-web/issues/new",
    email: "MrTsumugi@proton.me",
  },

  /* ---- BuiltByBit ---------------------------------------------
     Un solo sitio donde vive la URL de la ficha. El plugin esta en
     aprobacion, asi que published = false y los botones de compra no
     se dibujan: un enlace a una ficha que no existe lleva a un 404.

     Cuando se publique: pon la URL real en url y cambia published a
     true. build.py lee esto para las paginas; los dos index.html
     llevan el boton escrito dentro, asi que hay que tocarlos tambien.
     ------------------------------------------------------------- */
  listing: {
    published: false,
    url: "https://www.builtbybit.com/",
  },

  // El orden de los grupos y de las páginas dentro de cada grupo es el
  // que ve el lector, y también el que determina anterior/siguiente.
  groups: [
    {
      label: { en: "Start", es: "Empezar" },
      items: [{ slug: "quickstart" }],
    },
    {
      label: { en: "Essentials", es: "Esencial" },
      items: [
        { slug: "commands" },
        { slug: "flags" },
        { slug: "templates" },
        { slug: "ownership" },
        { slug: "seals" },
        { slug: "permissions" },
      ],
    },
    {
      label: { en: "Operation", es: "Operación" },
      items: [
        { slug: "configuration" },
        { slug: "translations" },
        { slug: "screens" },
        { slug: "database" },
      ],
    },
    {
      label: { en: "Reference", es: "Referencia" },
      items: [{ slug: "faq" }],
    },
  ],

  // Título y descripción por página. El título también sale del <title>
  // de cada HTML, pero se repite aquí para que la búsqueda y el índice
  // no tengan que ir a leer el DOM.
  pages: {
    quickstart: {
      title: { en: "Quick start", es: "Inicio rápido" },
      desc: {
        en: "Install ItemGuard on Paper 1.21+ and Java 21, and guard your first item in under a minute.",
        es: "Instala ItemGuard en Paper 1.21+ y Java 21, y protege tu primer objeto en menos de un minuto.",
      },
      icon: "rocket",
    },
    commands: {
      title: { en: "Commands", es: "Comandos" },
      desc: {
        en: "The full /ig reference: 22 subcommands, their arguments and what each one does.",
        es: "La referencia completa de /ig: 22 subcomandos, sus argumentos y qué hace cada uno.",
      },
      icon: "terminal",
    },
    flags: {
      title: { en: "Flags", es: "Flags y comportamiento" },
      desc: {
        en: "The seven behavioural switches applied to a tracked item, and their conservative defaults.",
        es: "Los siete interruptores de comportamiento de un objeto rastreado y sus valores por defecto.",
      },
      icon: "sliders",
    },
    templates: {
      title: { en: "Templates", es: "Plantillas" },
      desc: {
        en: "A template names a group of items and carries the flags they share.",
        es: "Una plantilla nombra un grupo de objetos y lleva las flags que comparten.",
      },
      icon: "layers",
    },
    ownership: {
      title: { en: "Ownership & transfer", es: "Propiedad y traspaso" },
      desc: {
        en: "Who owns a tracked item, how ownership moves, and what happens when an owner leaves.",
        es: "Quién es dueño de un objeto rastreado, cómo cambia de dueño y qué pasa si se va.",
      },
      icon: "user",
    },
    seals: {
      title: { en: "Seals & reclaim", es: "Sellos y reclamo" },
      desc: {
        en: "How a dropped item is sealed into the ground and how its owner takes it back.",
        es: "Cómo se sella un objeto caído y cómo su dueño lo recupera.",
      },
      icon: "lock",
    },
    permissions: {
      title: { en: "Permissions", es: "Permisos" },
      desc: {
        en: "The eighteen permission nodes and the admin wildcard that bundles them.",
        es: "Los dieciocho nodos de permiso y el comodín de administración que los agrupa.",
      },
      icon: "key",
    },
    configuration: {
      title: { en: "Configuration", es: "Configuración" },
      desc: {
        en: "Every option in config.yml, what it does and when you need to change it.",
        es: "Cada opción de config.yml, qué hace y cuándo hay que tocarla.",
      },
      icon: "sliders",
    },
    translations: {
      title: { en: "Translations", es: "Traducciones" },
      desc: {
        en: "Nine languages, one editable file each, with documented placeholders.",
        es: "Nueve idiomas, un archivo editable cada uno, con marcadores documentados.",
      },
      icon: "globe",
    },
    screens: {
      title: { en: "In-game screens", es: "Pantallas en el juego" },
      desc: {
        en: "Every tracked item has a record on screen: state, owner, location, flags and history.",
        es: "Cada objeto rastreado tiene su ficha en pantalla: estado, dueño, ubicación, flags e historial.",
      },
      icon: "grid",
    },
    database: {
      title: { en: "Database", es: "Base de datos" },
      desc: {
        en: "SQLite out of the box, MySQL or PostgreSQL when you outgrow a file.",
        es: "SQLite de serie, MySQL o PostgreSQL cuando un archivo se queda corto.",
      },
      icon: "database",
    },
    faq: {
      title: { en: "FAQ", es: "Preguntas" },
      desc: {
        en: "The questions that come up most, answered.",
        es: "Las preguntas que más salen, respondidas.",
      },
      icon: "help",
    },
  },

  // Textos de la interfaz. Todo lo visible pasa por aquí, para poder
  // cambiar de idioma sin tocar el HTML.
  i18n: {
    en: {
      search: "Search",
      searchPlaceholder: "Search the docs…",
      searchHint: "Type to search. Esc to close.",
      noResults: "Nothing found for",
      onThisPage: "On this page",
      previous: "Previous",
      next: "Next",
      overview: "Overview",
      docs: "Documentation",
      edit: "Edit this page",
      theme: "Toggle theme",
      menu: "Menu",
      languages: "Language",
      noIndex: "No index yet",
      report: "Report a problem",
      reportLead: "Something not working, or behaving in a way you did not expect?",
      reportIssue: "Open an issue",
      reportIssueDesc: "Public GitHub issues on the documentation site. Search first: it may already be known.",
      reportEmail: "Email us",
      reportEmailDesc: "Reaches both of us. Slow, but it works without an account.",
      searchFirst: "Search the issues first",
    },
    es: {
      search: "Buscar",
      searchPlaceholder: "Buscar en la documentación…",
      searchHint: "Escribe para buscar. Esc para cerrar.",
      noResults: "Sin resultados para",
      onThisPage: "En esta página",
      previous: "Anterior",
      next: "Siguiente",
      overview: "Resumen",
      docs: "Documentación",
      edit: "Editar esta página",
      theme: "Cambiar tema",
      menu: "Menú",
      languages: "Idioma",
      noIndex: "Sin índice",
      report: "Reporta un problema",
      reportLead: "¿Algo no funciona, o se comporta de una forma que no esperabas?",
      reportIssue: "Abrir un issue",
      reportIssueDesc: "Issues públicos de GitHub en el sitio de documentación. Busca antes: puede que ya esté conocido.",
      reportEmail: "Escríbenos",
      reportEmailDesc: "Llega a los dos. Más lento, pero funciona sin cuenta.",
      searchFirst: "Busca primero en los issues",
    },
  },
};
