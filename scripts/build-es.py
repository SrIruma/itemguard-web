#!/usr/bin/env python3
"""
Traduce las paginas de documentacion al espanol.

La traduccion vive en content/es/<slug>.html, una por pagina. El
generador de la pagina (build.py) la envuelve en la misma chrome que
usa el ingles, asi que el arbol español tiene exactamente la misma
estructura: /es/docs/<slug>.html y /es/ para la portada.

Este script se ejecuta una vez por idioma nuevo. Para retocar despues
basta con editar content/es/<slug>.html y volver a correr build.py.

    python3 scripts/build-es.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "es"

SLUGS = [
    "quickstart", "commands", "flags", "templates", "ownership", "seals",
    "permissions", "configuration", "translations", "screens", "database", "faq",
]

# Traduccion del contenido. Se conserva el marcado: <code>, <pre>, las
# tablas y los callouts son los mismos, solo cambia el texto.
TRANSLATIONS: dict[str, str] = {}

TRANSLATIONS["quickstart"] = """
<p class="lead">De un jar en <code>plugins/</code> a un objeto protegido en menos de un minuto.</p>
<p class="meta">Tiempo estimado: 3 minutos &#183; Paper 1.21+ &#183; Java 21</p>

<h2>1. Requisitos</h2>
<ul>
  <li><strong>Paper 1.21 o superior</strong> (o un fork con la misma API).</li>
  <li><strong>Java 21</strong>.</li>
  <li>Ningún otro plugin. Los drivers de SQLite, MySQL y PostgreSQL vienen dentro del jar.</li>
</ul>
<div class="note"><strong>Integraciones opcionales.</strong> LuckPerms se usa si resulta estar instalado y nunca es necesario. El único puente opcional es SmartSpawner; sin él, ItemGuard funciona exactamente igual.</div>

<h2>2. Coloca el jar</h2>
<pre><code>plugins/
  ItemGuard.jar   # déjalo aquí (o en plugins/ItemGuard/)</code></pre>
<p>Arranca el servidor. En la primera ejecución el plugin crea <code>plugins/ItemGuard/</code> con:</p>
<ul>
  <li><code>config.yml</code> — la configuración, completamente comentada.</li>
  <li><code>translations/</code> — un archivo de mensajes editable por idioma, nueve en total.</li>
  <li><code>itemguard.db</code> — el registro SQLite. Nada sale de la máquina.</li>
</ul>

<h2>3. Lee el informe de arranque</h2>
<p>Cada arranque imprime un bloque que lo dice todo &#8212; lo primero que hay que mirar cuando algo no funciona:</p>
<pre><code>ItemGuard v1.0.0 — by SrIruma &amp; SrPinkyy
State: ACTIVE | 7 tracked item(s)
Server: Paper 1.21.1 (build 133)
Java: 21.0.12.1
Database: SQLite (plugins/ItemGuard/itemguard.db)
Language: en
Loaded: 7 items, 2 template(s)
Integrations: none | SmartSpawner
Sealed ground: on, swept every 30s, 3 reclaim attempt(s)
Access: per-node (17 nodes)</code></pre>
<p>Cuando no puede arrancar, nombra el problema y la solución, en lugar de detenerse en una línea genérica:</p>
<pre><code>ItemGuard v1.0.0 — by SrIruma &amp; SrPinkyy
State: FAILED | the plugin was disabled
Server: Paper 1.21.1 (build 133)
Engine: MySQL
Problem: cannot open the database on MySQL 8: Access denied for user 'root'
Try: check the database block of config.yml</code></pre>
<div class="tip"><strong>El motor se nombra a propósito.</strong> Una contraseña mal, un esquema que falta y un host inalcanzable no tienen nada en común como solución. La línea de base de datos nombra el motor realmente en uso, con cualquier <code>password=</code> oculto.</div>

<h2>4. Protege tu primer objeto</h2>
<p>Sujeta una espada de diamante y ejecuta &#8212; con el operador, o con <code>itemguard.add</code> concedido:</p>
<pre><code>/ig create Sword</code></pre>
<p>Esto guarda el objeto como plantilla <code>Sword</code>. Entrega una copia protegida a un jugador:</p>
<pre><code>/ig give Steve Sword amount 64</code></pre>
<p>Esa copia ya tiene un id único y no puede soltarse ni recogerse por nadie salvo Steve. ¿Dónde está?</p>
<pre><code>/ig find TI-1a2b3c</code></pre>
<p>Suéltalo en el suelo y séllalo en su sitio &#8212; bedrock debajo, una etiqueta encima:</p>
<pre><code>/ig seal TI-1a2b3c
/ig reclaim                     # su dueño lo recupera</code></pre>

<div class="warn"><strong>¿Nadie puede ejecutar comandos todavía?</strong> Todos los permisos vienen en <code>false</code>, así que en un servidor real los operadores no tienen nada hasta que se conceda. Mira <a href="permissions.html">Permisos</a>. En un servidor de pruebas donde todo el mundo entra como operador, pon <code>console.ops-are-admins: true</code> y el estado de operador pasa a ser toda la política.</div>

<h2>5. ¿Y ahora?</h2>
<ul>
  <li><a href="commands.html">La referencia completa de <code>/ig</code></a></li>
  <li><a href="configuration.html">Todas las opciones de <code>config.yml</code></a></li>
  <li><a href="seals.html">Sellos, bedrock y el presupuesto de reclamo</a></li>
  <li><a href="permissions.html">Los dieciocho nodos y <code>itemguard.admin</code></a></li>
</ul>

<h2>Probarlo antes de comprarlo</h2>
<p>BuiltByBit tiene un <strong>servidor de prueba</strong> con el plugin ya instalado, para que puedas probarlo en el juego antes de decidir. Se entra desde la propia ficha del plugin.</p>
"""

TRANSLATIONS["commands"] = """
<p class="lead">Todo se hace con <code>/ig</code> (alias <code>/itemguard</code>). Un jugador ve el resultado en una pantalla; la consola recibe texto. Ejecuta <code>/ig help</code> dentro del juego para ver la misma lista, y <code>/ig help gui</code> para verla como menú.</p>
<p class="meta">22 subcomandos &#183; <code>info</code>, <code>list</code> y <code>flag</code> abren una pantalla al jugador</p>

<h2>Referencia</h2>
<div class="table-wrap">
  <table>
    <thead><tr><th>Comando</th><th>Qué hace</th></tr></thead>
    <tbody>
      <tr><td><code>/ig create &lt;plantilla&gt; [force]</code></td><td>Crea o sobrescribe una plantilla a partir del objeto en la mano</td></tr>
      <tr><td><code>/ig delete &lt;plantilla&gt;</code></td><td>Elimina una plantilla guardada</td></tr>
      <tr><td><code>/ig unlink [id|hand]</code></td><td>Deja de rastrear un objeto; el objeto en sí no se toca</td></tr>
      <tr><td><code>/ig give &lt;jugador&gt; &lt;plantilla&gt; [amount &lt;n&gt;] [flags k=v] [raw] [quiet]</code></td><td>Construye y entrega un objeto</td></tr>
      <tr><td><code>/ig transfer &lt;jugador&gt; [id|hand]</code></td><td>Envía un objeto rastreado a otro jugador</td></tr>
      <tr><td><code>/ig owner &lt;jugador&gt; [id|hand] [raw]</code></td><td>Traspasa un objeto y su propiedad</td></tr>
      <tr><td><code>/ig flag &lt;plantilla|id|hand&gt; [flag=value ...]</code></td><td>Lee las flags en una pantalla, o las cambia</td></tr>
      <tr><td><code>/ig recover &lt;id&gt;</code></td><td>Recupera un objeto esté donde esté, entero</td></tr>
      <tr><td><code>/ig regenerate &lt;id&gt; [confirm]</code></td><td>Reconstruye un objeto perdido desde su copia guardada</td></tr>
      <tr><td><code>/ig reclaim [id]</code></td><td>El dueño recupera su propio objeto sellado</td></tr>
      <tr><td><code>/ig seal &lt;id|hand&gt;</code></td><td>Sella un objeto que está en el suelo</td></tr>
      <tr><td><code>/ig unseal &lt;id&gt;</code></td><td>Quita un sello sin mover el objeto</td></tr>
      <tr><td><code>/ig find &lt;id&gt;</code></td><td>Informa de dónde está un objeto</td></tr>
      <tr><td><code>/ig tp &lt;id&gt; [confirm]</code></td><td>Teletransporta al objeto: el bloque colocado, la copia en el suelo, un tenedor conectado, o un contenedor que ve. Si nada de eso es visible, nombra el motivo y espera <code>confirm</code></td></tr>
      <tr><td><code>/ig info &lt;id|hand&gt; [history]</code></td><td>La ficha en pantalla; <code>history</code> abre la lista de eventos</td></tr>
      <tr><td><code>/ig list &lt;plantillas|objetos&gt;</code></td><td>El catálogo o los objetos rastreados, en pantalla</td></tr>
      <tr><td><code>/ig version</code></td><td>Versiones de ItemGuard, del servidor y de Java</td></tr>
      <tr><td><code>/ig permissions</code></td><td>Cada nodo de ItemGuard que tienes, con un sí o un no</td></tr>
      <tr><td><code>/ig integrations</code></td><td>El motor de base de datos y las integraciones opcionales</td></tr>
      <tr><td><code>/ig reload</code></td><td>Recarga configuración, mensajes, plantillas y datos</td></tr>
      <tr><td><code>/ig help [gui]</code></td><td>La lista completa, como texto o como menú de solo lectura</td></tr>
    </tbody>
  </table>
</div>

<h2>La forma de los comandos</h2>
<p>Todos pasan por el mismo despachador. La diferencia entrejugador y consola no está en el comando sino en quién lo ejecuta:</p>
<ul>
  <li>Un <strong>jugador</strong> ve pantallas: el resultado, la lista, las flags. Es la interfaz normal.</li>
  <li>La <strong>consola</strong> ve texto, una línea por resultado. Pensado para scripts y para servidores gestionados.</li>
</ul>
<p>Ambos obtienen lo mismo del mismo sitio. No hay dos implementaciones que puedan discrepar.</p>
<div class="tip"><strong>El resultado importa más que el comando.</strong> Un <code>/ig give</code> que no puede completarse dice por qué y qué haría falta, en lugar de confirmar un entrega que no ocurrió.</div>

<h2>Un ejemplo de verdad</h2>
<p>Un jugador con permiso <code>itemguard.add</code>, un objeto en la mano y una plantilla sin definir:</p>
<pre><code>&gt; /ig create Sword
Template "Sword" created from diamond_sword
  drop=false pickup=false move=false hopper=false
  break=false explosion=false recovery=true</code></pre>
<p>La plantilla guarda las flags con sus valores por defecto. Cada objeto que salga de ella las hereda, y puede anular cualquiera de forma individual.</p>
"""

TRANSLATIONS["flags"] = """
<p class="lead">Siete interruptores que deciden qué se le permite hacer a un objeto rastreado. Cada uno tiene un valor por defecto prudente, y todos se pueden cambiar por objeto.</p>
<p class="meta">7 flags &#183; por objeto o por plantilla</p>

<h2>Las siete flags</h2>
<div class="table-wrap">
  <table>
    <thead><tr><th>Flag</th><th>Qué controla</th><th>Por defecto</th></tr></thead>
    <tbody>
      <tr><td><code>drop</code></td><td>Si el objeto puede soltarse al suelo</td><td><code>false</code></td></tr>
      <tr><td><code>pickup</code></td><td>Si otro jugador puede recogerlo</td><td><code>false</code></td></tr>
      <tr><td><code>move</code></td><td>Si puede arrastrarse de un sitio a otro</td><td><code>false</code></td></tr>
      <tr><td><code>hopper</code></td><td>Si una tolva puede extraerlo de un contenedor</td><td><code>false</code></td></tr>
      <tr><td><code>break</code></td><td>Si el bloque colocado puede romperse</td><td><code>false</code></td></tr>
      <tr><td><code>explosion</code></td><td>Si una explosión puede destruirlo</td><td><code>false</code></td></tr>
      <tr><td><code>recovery</code></td><td>Si se puede recuperar tras una pérdida</td><td><code>true</code></td></tr>
    </tbody>
  </table>
</div>

<div class="note"><strong>Por qué todas en false.</strong> Un objeto que un jugador puede soltar, que otro puede recoger y que una tolva puede llevarse no está protegido en ningún sentido que importe. La única que viene en true es <code>recovery</code>, porque poder recuperar lo tuyo es el comportamiento por defecto razonable, no una concesión.</div>

<h2>Dónde vive una flag</h2>
<p>En dos sitios, y el objeto gana al grupo:</p>
<ul>
  <li>En la <strong>plantilla</strong>, para todo lo que salga de ella.</li>
  <li>En el <strong>objeto</strong>, para ese caso concreto. Un objeto puede anular cualquier flag de su plantilla sin tocar los demás.</li>
</ul>
<p>Al crear un objeto desde una plantilla, se copian los valores. Después, cambiar la plantilla no cambia los objetos ya existentes: lo que se edita es el punto de partida para los siguientes.</p>
<div class="tip"><strong>Por qué no es una herencia viva.</strong> Si cambiar una plantilla alterara objetos ya repartidos por el mundo, un cambio de configuración podría weaken la protección de algo que alguien ya considera suyo. Copiar en la creación hace que la política de un objeto sea fija y predecible.</div>

<h2>Leer y cambiar flags</h2>
<p>En el juego, <code>/ig flag</code> abre una pantalla con las flags del objeto y casillas para cambiarlas. Desde consola imprime la misma información en texto.</p>
<pre><code>&gt; /ig flag hand
Template: Sword
  drop=false pickup=false move=false hopper=false
  break=false explosion=false recovery=true
Overrides on this item: none</code></pre>
<p>Para cambiar, se pasan pares <code>flag=valor</code>:</p>
<pre><code>&gt; /ig flag hand hopper=true
Set hopper=true on TI-1a2b3c
  hopper: false -> true
  (6 flags unchanged)</code></pre>
<p>El resultado dice qué cambió y qué no. Un cambio que no hace nada se dice, en lugar de confirmar en silencio.</p>

<h2>Flags en plantillas</h2>
<p>Una plantilla lleva las flags que comparte todo lo que sale de ella. Se define al crearla:</p>
<pre><code>&gt; /ig create Sword flags=drop=false,recovery=true</code></pre>
<div class="warn"><strong>Un objeto puede contradecir a su plantilla.</strong> Es intencional: es lo que permite un objeto que sí puede soltarse dentro de un inventario privado, sin renunciar a la protección del resto. Si necesitas que la plantilla sea ley, revisa los objetos existentes con <code>/ig list items</code> y sus overrides.</div>
"""

TRANSLATIONS["templates"] = """
<p class="lead">Una plantilla nombra un grupo de objetos y lleva las flags que comparten. Todo lo que sale de ella hereda esas flags, y cada objeto puede anular cualquier flag de forma individual.</p>
<p class="meta">Un nombre, un grupo, las flags compartidas</p>

<h2>Qué es una plantilla</h2>
<p>No es un contenedor de objetos: es una definición. Dice qué clase de cosa es y cómo se comporta, y a partir de ahí el plugin construye objetos iguales.</p>
<p>El caso claro es el equipo caro. Una espada de diamante y una de netherita no son el mismo objeto, pero casi siempre quieres lo mismo: que no se suelten, que no las recoja un desconocido, que una tolva no se las lleve. Eso es una plantilla.</p>
<div class="note"><strong>Una plantilla no se puede editar en caliente.</strong> Crear y borrar son operaciones de administrador. Para cambiar cómo se comporta un grupo ya repartido, se cambian los objetos: una plantilla nueva no los toca.</div>

<h2>Crear una plantilla</h2>
<p>Se crea a partir del objeto en la mano:</p>
<pre><code>&gt; /ig create Sword
Template "Sword" created from diamond_sword
  drop=false pickup=false move=false hopper=false
  break=false explosion=false recovery=true</code></pre>
<p>El nombre es el que usarás después para entregar objetos de esa clase. Se pueden añadir flags al crearla, y sobrescribir una existente con <code>force</code>:</p>
<pre><code>&gt; /ig create Sword force flags=drop=false,pickup=false,recovery=true</code></pre>
<p>Los dos ejemplos dan el mismo resultado. La forma larga se usa cuando se quiere ser explícito.</p>

<h2>Ver las plantillas</h2>
<p><code>/ig list templates</code> las muestra en pantalla para un jugador, y en texto para consola.</p>
<pre><code>&gt; /ig list templates
Sword       diamond_sword      7 flags, 0 overrides
Ore         raw_gold_block     7 flags, 0 overrides
Totem       totem_of_undying   7 flags, 1 overrides</code></pre>
<p>La columna de overrides cuenta cuántos objetos de esa plantilla se apartan de ella. Un número alto ahí suele significar que la plantilla no describe bien el grupo.</p>

<h2>Borrar una plantilla</h2>
<pre><code>&gt; /ig delete Sword
Template "Sword" deleted
  0 items were using it</code></pre>
<p>Borrar una plantilla no toca los objetos que salieron de ella. Siguen rastreados, con sus propias flags, y siguen localizables por id. Lo que desaparece es la definición, no la historia de lo construido con ella.</p>
<div class="warn"><strong>Borrarla no libera nada.</strong> Un objeto creado desde una plantilla borrada no se convierte en un objeto normal: conserva sus flags. Si lo que quieres es dejar de proteger algo, usa <code>/ig flag</code> sobre el objeto, o <code>/ig unlink</code> para dejar de rastrearlo.</div>

<h2>Los flags que una plantilla lleva</h2>
<p>Los mismos siete de siempre: <code>drop</code>, <code>pickup</code>, <code>move</code>, <code>hopper</code>, <code>break</code>, <code>explosion</code> y <code>recovery</code>. Todos en <code>false</code> salvo <code>recovery</code>. La <a href="flags.html">página de flags</a> explica cada uno y por qué.</p>
"""

TRANSLATIONS["ownership"] = """
<p class="lead">Un objeto rastreado tiene un dueño. Se puede cambiar, transferir y consultar, y el plugin lo registra todo para que un reclamo sea demostrable.</p>
<p class="meta">18 objetos, un dueño cada uno</p>

<h2>Qué es la propiedad</h2>
<p>La propiedad es la relación entre un objeto rastreado y un jugador. No es un permiso: es un hecho que queda registrado. Un servidor puede estar lleno de operadores y aun así ningún operador es dueño de nada, porque los permisos por defecto son <code>false</code>.</p>
<p>La propiedad es lo que hace que <a href="seals.html">reclamar</a> funcione. Un objeto sellado en el suelo se lo lleva su dueño, y no un admin por mucho que pueda.</p>
<div class="note"><strong>La propiedad no caduca.</strong> Un objeto que nadie reclama sigue perteneciendo a su dueño. No hay temporizadores ni caducidad: es suya mientras exista el objeto.</div>

<h2>Ver el dueño</h2>
<pre><code>&gt; /ig info TI-1a2b3c
Item:   TI-1a2b3c  (diamond_sword)
Owner:  SrIruma
State:  SEALED
Where:  1284 64 -3027  (sealed in the ground)
Since:  2026-09-28 19:03:11
</code></pre>
<p>Para un jugador, <code>/ig info hand</code> abre la misma ficha en pantalla.</p>

<h2>Cambiar el dueño</h2>
<p>Se cambia con un comando, y el cambio queda en el historial del objeto:</p>
<pre><code>&gt; /ig owner Steve hand
Transferred TI-1a2b3c from SrIruma to Steve
  recorded: 2026-09-28 19:07:44</code></pre>
<p>Con <code>raw</code> se imprime solo el resultado, sin la línea de registro, para usar en scripts.</p>
<p>Un objeto que no tiene dueño, porque se creó con un bypass de administrador, se puede asignar a alguien con el mismo comando.</p>

<h2>Transferir a otro jugador</h2>
<p>Enviar el objeto es una cosa; cambiar su dueño, otra. Son comandos separados a propósito:</p>
<pre><code>/ig transfer Steve hand    # el objeto llega a Steve
/ig owner Steve hand       # ahora Steve es su dueño</code></pre>
<div class="tip"><strong>Por qué no se juntan.</strong> Transferir sin traspasar la propiedad es un regalo: el receptor tiene el objeto y tú conservas el derecho a reclamarlo. Es una decisión legítima, pero no debería ser la que ocurre por defecto cuando escribes un solo comando.</div>

<h2>Qué pasa cuando un dueño se va</h2>
<p>El objeto no se desvincula. Sigue siendo suyo, y si vuelve un día puede reclamarlo. La propiedad no depende de que el jugador esté conectado ni de que la cuenta siga existiendo.</p>
<p>Un objeto cuyo dueño se fue sí se puede recuperar con <code>/ig recover</code>, que es una operación de administración y queda registrada a nombre de quien la ejecuta. Es la excepción, no el norma.</p>

<h2>El historial</h2>
<p>Cada cambio de dueño, cada sello y cada recuperación se guarda con fecha. <code>/ig info id history</code> la muestra completa.</p>
<pre><code>&gt; /ig info TI-1a2b3c history
TI-1a2b3c  history
  2026-09-20 11:02  created from template Sword
  2026-09-20 11:03  given to SrPinkyy
  2026-09-21 09:44  owner: SrPinkyy -> SrIruma
  2026-09-28 19:03  sealed in the ground
  2026-09-29 20:15  reclaim attempt denied (wrong player)</code></pre>
<p>El último intento fallido también se registra. Un reclamo denegado deja rastro, que es justo lo que hace que un reclamo correcto sea creíble.</p>
"""

TRANSLATIONS["seals"] = """
<p class="lead">Un objeto que cae al suelo se sella en su sitio: bedrock debajo, una etiqueta encima. Solo su dueño puede sacarlo de ahí, y cada intento queda registrado.</p>
<p class="meta">Bedrock debajo, etiqueta encima, dueño dentro</p>

<h2>Qué hace un sello</h2>
<p>Sellar fija un objeto en un punto del mundo. Deja de ser un objeto suelto y pasa a ser algo anclado:</p>
<ul>
  <li>No se puede recoger, ni arrastrar, ni mover.</li>
  <li>No lo absorbe una tolva, ni lo rompe un pico, ni lo destruye una explosión.</li>
  <li>Su dueño puede reclamarlo con <code>/ig reclaim</code>.</li>
</ul>
<p>La etiqueta flotante sobre el objeto muestra su id, para que un dueño pueda encontrarlo sin recordar el código de memoria.</p>
<div class="note"><strong>Un sello es por posición, no por contenedor.</strong> El objeto queda en el mundo, no en un baúl. Eso significa que un sello sobrevive a que alguien rompa el baúl donde se guardaba.</div>

<h2>Sellar un objeto</h2>
<pre><code>&gt; /ig seal TI-1a2b3c
Sealed TI-1a2b3c at 1284 64 -3027
  bedrock placed underneath
  label: "TI-1a2b3c — SrIruma"</code></pre>
<p>También funciona sobre el objeto en la mano, para sellar algo que llevas encima:</p>
<pre><code>&gt; /ig seal hand</code></pre>
<p>Sellar algo que ya está sellado no hace nada y lo dice, en lugar de apilar bedrock encima.</p>

<h2>Reclamar un objeto sellado</h2>
<p>El dueño lo recoge con un comando. No se recoge andando, sino con intención explícita:</p>
<pre><code>&gt; /ig reclaim
Reclaimed TI-1a2b3c
  owner: SrIruma (verified)
  location: 1284 64 -3027
  returned to hand</code></pre>
<p>El reclamo verifica tres cosas antes de devolver el objeto: que quien lo pide es el dueño, que el objeto sigue donde se selló, y que el mundo sigue siendo el mismo. Si alguna falla, lo dice y no mueve nada.</p>
<div class="tip"><strong>El reclamo es una prueba, no un permiso.</strong> No depende de los permisos del jugador: depende de que sea el dueño. Un admin sin propiedad no puede reclamar el objeto de otro, y por eso no puede "quedárselo".</div>

<h2>El presupuesto de reclamos</h2>
<p>Reclamar genera bedrock y mueve un objeto, así que está limitado por servidor. En <code>config.yml</code>:</p>
<pre><code>seals:
  reclaim-attempts: 3
  reclaim-window: 30s
  sweep-interval: 30s</code></pre>
<p>El comportamiento es:</p>
<ul>
  <li>Un jugador tiene <code>reclaim-attempts</code> oportunidades cada <code>reclaim-window</code>.</li>
  <li>Cada reclamo<b>fallido</b> consume una. Un reclamo correcto también, porque mover un objeto cuenta igual.</li>
  <li>Al agotarse, el plugin responde con un mensaje que dice cuánto queda y cuándo se recupera.</li>
</ul>
<div class="warn"><strong>Un abuso aquí es un problema real.</strong> El límite existe para que el reclamo no se convierta en una forma de mover bedrock por el mundo. Si en tu servidor los jugadores reclaman con frecuencia, sube el presupuesto en vez de desactivar la comprobación.</div>

<h2>El barrido</h2>
<p>Los objetos sellados se comprueban cada <code>sweep-interval</code> segundos. El barrido:</p>
<ul>
  <li>Recoloca la etiqueta y el bedrock si alguien los movió.</li>
  <li>Quita sellos cuyo objeto ya no existe, para no dejar Basura.</li>
  <li>Avisa por consola si un sello quedó inválido, con el motivo.</li>
</ul>
<p>El barrido se puede desactivar con <code>seals.sweep: false</code> si interfiere con algo. En un servidor con mucho Treaty del Nether puede noticing; conviene mirar los avisos de consola la primera vez.</p>

<h2>Quitar un sello</h2>
<p>Un admin puede quitar el sello sin mover el objeto, dejándolo en el sitio como un objeto normal protegido por sus flags:</p>
<pre><code>&gt; /ig unseal TI-1a2b3c
Seal removed from TI-1a2b3c
  object left in place at 1284 64 -3027</code></pre>
<p>Esto no libera el objeto: sigue siendo rastreado y sigue siendo del mismo dueño. Lo único que se quita es el anclaje.</p>
"""

TRANSLATIONS["permissions"] = """
<p class="lead">Todos los permisos vienen en <code>false</code>, así que ni siquiera los operadores los tienen hasta que se concedan &#8212; con una única excepción deliberada.</p>
<p class="meta">18 nodos &#183; <code>itemguard.admin</code> los agrupa</p>

<h2>Los nodos</h2>
<div class="table-wrap">
  <table>
    <thead><tr><th>Permiso</th><th>Permite</th><th>Por defecto</th></tr></thead>
    <tbody>
      <tr><td><code>itemguard.add</code></td><td><code>/ig create</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.remove</code></td><td><code>/ig delete</code> y <code>/ig unlink</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.give</code></td><td><code>/ig give</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.send</code></td><td><code>/ig transfer</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.owner</code></td><td><code>/ig owner</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.flag</code></td><td><code>/ig flag</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.recover</code></td><td><code>/ig recover</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.regenerate</code></td><td><code>/ig regenerate</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.reclaim</code></td><td><code>/ig reclaim</code></td><td><code>true</code></td></tr>
      <tr><td><code>itemguard.seal</code></td><td><code>/ig seal</code> y <code>/ig unseal</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.find</code></td><td><code>/ig find</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.tp</code></td><td><code>/ig tp</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.info</code></td><td><code>/ig info</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.list</code></td><td><code>/ig list</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.break</code></td><td>Romper un bloque rastreado de otro</td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.version</code></td><td><code>/ig version</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.reload</code></td><td><code>/ig reload</code></td><td><code>false</code></td></tr>
      <tr><td><code>itemguard.admin</code></td><td>Todo lo anterior</td><td><code>false</code></td></tr>
    </tbody>
  </table>
</div>

<div class="note"><strong>La única excepción.</strong> <code>itemguard.reclaim</code> viene en <code>true</code> para que ser dueño de un objeto baste para recuperarlo. Revócalo en un grupo y sus jugadores se remitirán a un admin en su lugar.</div>

<h2>Dos atajos</h2>
<p><code>itemguard.admin</code> llega de dos maneras, y ItemGuard resuelve las dos por su cuenta, así que funcionan incluso sin un plugin de permisos:</p>
<ul>
  <li>En <strong>LuckPerms</strong>: <code>/lp group default permission info itemguard.admin</code>.</li>
  <li>En <strong>el ops-are-admins de la consola</strong>: con <code>console.ops-are-admins: true</code>, ser operador equivale a <code>itemguard.admin</code>.</li>
</ul>
<p>El segundo es el camino corto para un servidor de pruebas donde todo el mundo entra como operador. En producción conviene lo contrario: permisos concretos, y solo a quien los necesita.</p>

<h2>Comprobar lo que tienes</h2>
<p>Sin adivinar:</p>
<pre><code>&gt; /ig permissions
You hold:
  itemguard.reclaim    yes   (default)
  itemguard.add        no
  itemguard.give       no
  itemguard.admin      no
Not held: 16 nodes</code></pre>
<p>El resultado separa lo concedido de lo por defecto, que es la confusion más habitual: un permiso puede estar activo sin que nadie lo haya concedido, y esa línea lo deja claro.</p>

<h2>Dar un permiso con LuckPerms</h2>
<pre><code>/lp user SrPinkyy permission set itemguard.add true
/lp user SrPinkyy permission set itemguard.give true
/lp group default permission set itemguard.find true</code></pre>
<p>El grupo por defecto con <code>itemguard.find</code> es razonable: poder preguntar dónde está un objeto no da derecho a moverlo.</p>
<div class="tip"><strong>Orden de concesión.</strong> Da primero el permiso concreto, y <code>itemguard.admin</code> después si hace falta. Con los eighteen concedidos a medias, es fácil creer que algo no funciona cuando en realidad falta un nodo.</div>

<h2>Sin plugin de permisos</h2>
<p>Si no usas LuckPerms ni nada parecido, el plugin acepta los permisos por el mecanismo de Paper, que es el mismo que usan los comandos vanilla. En la práctica, con un <code>permissions.yml</code> o con los permisos por defecto de Bukkit, los operadores tienen lo que sus permisos digan y nadie más.</p>
<p>ItemGuard no exige ningún plugin de permisos. LuckPerms es una comodidad, no un requisito, y SmartSpawner es un puente opcional que puedes no tener nunca.</p>
"""

TRANSLATIONS["configuration"] = """
<p class="lead">Todo lo que se puede cambiar está en <code>config.yml</code>, comentado y con el valor por defecto a la vista. La mayoría de los servidores no necesita tocarlo.</p>
<p class="meta">Generado en el primer arranque &#183; comentado línea por línea</p>

<h2>Dónde está</h2>
<p>En <code>plugins/ItemGuard/config.yml</code>, creado en el primer arranque. No se sobrescribe al actualizar: si una versión nueva añade opciones, se añaden con su valor por defecto y las tuyas se quedan.</p>
<div class="note"><strong>Recargar sin reiniciar.</strong> <code>/ig reload</code> vuelve a leer configuración, mensajes, plantillas y datos. No hace falta reiniciar el servidor para cambiar una opción.</div>

<h2>El bloque de base de datos</h2>
<div class="table-wrap">
  <table>
    <thead><tr><th>Opción</th><th>Qué hace</th><th>Por defecto</th></tr></thead>
    <tbody>
      <tr><td><code>type</code></td><td><code>sqlite</code>, <code>mysql</code> o <code>postgresql</code></td><td><code>sqlite</code></td></tr>
      <tr><td><code>host</code></td><td>Servidor de base de datos</td><td><code>localhost</code></td></tr>
      <tr><td><code>port</code></td><td>Puerto de conexión</td><td>el del motor</td></tr>
      <tr><td><code>name</code></td><td>Nombre de la base de datos</td><td><code>itemguard</code></td></tr>
      <tr><td><code>user</code></td><td>Usuario de conexión</td><td><code>root</code></td></tr>
      <tr><td><code>password</code></td><td>Contraseña de conexión</td><td>vacío</td></tr>
    </tbody>
  </table>
</div>
<p>Con SQLite no hay nada que configurar: el archivo se crea solo en <code>plugins/ItemGuard/itemguard.db</code> y nada sale de la máquina.</p>
<p>El motor se comprueba en el arranque. Si no puede abrirla, el plugin no arranca y dice por qué:</p>
<pre><code>ItemGuard v1.0.0 — by SrIruma &amp; SrPinkyy
State: FAILED | the plugin was disabled
Server: Paper 1.21.1 (build 133)
Engine: MySQL
Problem: cannot open the database on MySQL 8: Access denied for user 'root'
Try: check the database block of config.yml</code></pre>
<div class="tip"><strong>Una contraseña mal, un esquema que falta y un host inalcanzable.</strong> No tienen nada en común como solución, así que el mensaje los distingue en lugar de decir "error de base de datos". Cualquier <code>password=</code> aparece oculto en el informe.</div>

<h2>Una base de datos por servidor</h2>
<p>El motor se fija en el arranque y se comprueba contra el mundo. Si dos servidores apuntan al mismo archivo y a mundos distintos, el plugin se niega a arrancar en lugar de mezclar datos de dos mundos:</p>
<pre><code>Problem: this database already holds items from another world
Try: give each server its own database, or its own world</code></pre>
<p>Es una comprobación que se nota sólo cuando importa, y que evita un fallo muy difícil de diagnosticar después.</p>

<h2>Los sellos</h2>
<div class="table-wrap">
  <table>
    <thead><tr><th>Opción</th><th>Qué hace</th><th>Por defecto</th></tr></thead>
    <tbody>
      <tr><td><code>seals.sweep</code></td><td>Comprueba los sellos periódicamente</td><td><code>true</code></td></tr>
      <tr><td><code>seals.sweep-interval</code></td><td>Cada cuántos segundos</td><td><code>30</code></td></tr>
      <tr><td><code>seals.reclaim-attempts</code></td><td>Reclamos por ventana y jugador</td><td><code>3</code></td></tr>
      <tr><td><code>seals.reclaim-window</code></td><td>Duración de la ventana, en segundos</td><td><code>30</code></td></tr>
    </tbody>
  </table>
</div>
<p>El <a href="seals.html">apartado de sellos</a> explica el presupuesto y el barrido con más detalle.</p>

<h2>Consola y operadores</h2>
<div class="table-wrap">
  <table>
    <thead><tr><th>Opción</th><th>Qué hace</th><th>Por defecto</th></tr></thead>
    <tbody>
      <tr><td><code>console.ops-are-admins</code></td><td>Ser operador equivale a <code>itemguard.admin</code></td><td><code>false</code></td></tr>
      <tr><td><code>console.log-file</code></td><td>Escribe un registro en archivo</td><td><code>false</code></td></tr>
    </tbody>
  </table>
</div>
<div class="warn"><strong>ops-are-admins es para pruebas.</strong> Con <code>true</code>, cualquiera que entre como operador puede rastrear, mover y recuperar cualquier objeto del servidor. Está pensado para un servidor de pruebas donde todo el mundo entra como operador; en producción, concede los permisos a quien los necesita y déjalo en <code>false</code>.</div>

<h2>Traducciones</h2>
<p>El idioma se toma de <code>language</code> en el primer arranque, y a partir de ahí de los archivos de <code>translations/</code>. Cada idioma es un archivo aparte, con los marcadores documentados. La <a href="translations.html">página de traducciones</a> los explica uno a uno.</p>
"""

TRANSLATIONS["translations"] = """<p class="lead">Cada mensaje es editable en su propio archivo, con los marcadores documentados. Y una clave que añade una versión nueva sigue funcionando después de actualizar.</p>
<p class="meta">9 idiomas &#183; un archivo por idioma &#183; editable en caliente</p>

<h2>Dónde están</h2>
<p>En <code>plugins/ItemGuard/translations/</code>, un archivo por idioma, generado en el primer arranque:</p>
<pre><code>translations/
  en.yml    messages.yml   # inglés
  es.yml    messages.yml
  de.yml    messages.yml
  fr.yml    messages.yml
  pt.yml    messages.yml
  it.yml    messages.yml
  nl.yml    messages.yml
  pl.yml    messages.yml
  ru.yml    messages.yml</code></pre>
<p>El idioma se elige en el primer arranque y luego se puede cambiar en cualquier momento sin reiniciar.</p>

<h2>Los marcadores</h2>
<p>Cada mensaje tiene marcadores que se rellenan al mostrarse. Se documentan en el propio archivo:</p>
<pre><code># messages.yml
reclaim:
  success: "Reclaimed {item} — owner {owner} verified"
  wrong-player: "That item belongs to {owner}, not to you."
  too-many: "Reclaim limit reached. Try again in {seconds}s."
  not-sealed: "{item} is not sealed."</code></pre>
<table>
  <thead><tr><th>Marcador</th><th>Qué pone</th></tr></thead>
  <tbody>
    <tr><td><code>{item}</code></td><td>El id del objeto, por ejemplo <code>TI-1a2b3c</code></td></tr>
    <tr><td><code>{owner}</code></td><td>El nombre del dueño</td></tr>
    <tr><td><code>{player}</code></td><td>Quien ejecuta el comando</td></tr>
    <tr><td><code>{amount}</code></td><td>La cantidad, cuando el mensaje habla de una entrega</td></tr>
    <tr><td><code>{seconds}</code></td><td>Un número de segundos, para las esperas</td></tr>
  </tbody>
</table>
<div class="note"><strong>Un marcador mal escrito no rompe nada.</strong> Si un archivo tiene <code>{itemm}</code> en lugar de <code>{item}</code>, el mensaje sale con el marcador tal cual en vez de desaparecer. Es visible, que es preferible a un hueco silencioso.</div>

<h2>Editar y recargar</h2>
<p>Los mensajes se releen sin reiniciar:</p>
<pre><code>&gt; /ig reload
Reloaded: config, 9 translation(s), 2 template(s), 7 item(s)</code></pre>
<p>Un archivo con YAML inválido no se aplica y el anterior se queda. El error dice el archivo y la línea, porque un mensaje que no aparece por un error de sangría es difícil de encontrar si no te lo dicen.</p>
<div class="tip"><strong>Prueba antes de dar por bueno.</strong> Tras editar, ejecuta el comando afectado una vez. Es más rápido que leer el archivo buscando un error de sangría, y el resultado te dice si el marcador se rellenó.</div>

<h2>Añadir un idioma</h2>
<p>Copiar un archivo existente con el nombre de tu idioma es todo lo que hace falta. El plugin lo carga en el siguiente arranque:</p>
<pre><code>cp translations/en.yml translations/ca.yml</code></pre>
<p>La traducción inicial se puede dejar en inglés: el resultado es un idioma mixto, que es mejor que nada y no rompe nada. Luego se va traduciendo por claves.</p>

<h2>Claves nuevas al actualizar</h2>
<p>Una versión nueva puede añadir claves que no estaban en tu archivo. Al arrancar:</p>
<pre><code>ItemGuard v1.0.1 — by SrIruma &amp; SrPinkyy
State: ACTIVE | 7 tracked item(s)
Loaded: 7 items, 2 template(s)
Translations: 9 loaded, 3 new key(s) added to en.yml
  seal.dust-trail   (added with default)
  seal.break-denied (added with default)</code></pre>
<div class="warn"><strong>Las claves se añaden, no se sobrescriben.</strong> Tus textos están a salvo. Las claves nuevas entran con su valor por defecto en inglés, así que Translated un archivo al español antes de traducirlo, y los mensajes nuevos saldrán en inglés hasta que los completes.</div>
"""

TRANSLATIONS["screens"] = """
<p class="lead">Cada objeto rastreado tiene su ficha en pantalla: estado, dueño, dónde se vio por última vez, sus flags y su historial, con las acciones que puedes hacer a un clic.</p>
<p class="meta">4 pantallas &#183; jugador y consola</p>

<h2>La ficha de un objeto</h2>
<p>Es la pantalla principal. <code>/ig info id</code> la abre para un jugador:</p>
<div class="panel">
  <p><strong>TI-1a2b3c</strong> &nbsp; diamond_sword &nbsp; <em>SEALED</em></p>
  <p>Owner: SrIruma &nbsp;&middot;&nbsp; Since: 28 sep 2026<br>
  Where: 1284 64 -3027 &nbsp;(sealed in the ground)<br>
  Flags: drop off &middot; pickup off &middot; move off &middot; hopper off &middot; break off &middot; explosion off &middot; <strong>recovery on</strong></p>
</div>
<p>Debajo hay botones para lo que ese objeto concreto permite hacer. Un objeto sellado muestra reclamo; uno en el suelo, moverlo; uno cuyo dueño no eres, nada.</p>
<div class="note"><strong>Los botones son el permiso hecho visible.</strong> No hay un botón que aparezca y falle al pulsarlo. Si una acción no está, es porque el objeto no la admite o porque no tienes permiso.</div>

<h2>El catálogo</h2>
<p><code>/ig list templates</code> y <code>/ig list items</code> abren el catálogo. Es una rejilla, pensada para recorrerla con el ratón en vez de para leerla entera:</p>
<div class="panel">
  <p><strong>Templates (2)</strong><br>
  Sword &nbsp;&middot;&nbsp; 7 items &nbsp;&middot;&nbsp; 0 overrides<br>
  Ore &nbsp;&middot;&nbsp; 4 items &nbsp;&middot;&nbsp; 1 override</p>
</div>
<p>Al pulsar un objeto se abre su ficha. Al pulsar una plantilla, sus flags, que es lo que se edita desde ahí.</p>

<h2>El historial</h2>
<p>Un botón en la ficha, o <code>/ig info id history</code>, y se abre la línea de tiempo del objeto:</p>
<div class="panel">
  <p><strong>TI-1a2b3c</strong> &nbsp; 7 events<br>
  20 sep 11:02 &nbsp; created from template Sword<br>
  20 sep 11:03 &nbsp; given to SrPinkyy<br>
  21 sep 09:44 &nbsp; owner: SrPinkyy &rarr; SrIruma<br>
  28 sep 19:03 &nbsp; sealed in the ground<br>
  29 sep 20:15 &nbsp; reclaim attempt denied (wrong player)</p>
</div>
<p>Los intentos fallidos están. Un reclamo denegado deja rastro, que es lo que hace que un reclamo correcto sea creíble delante de alguien que discute.</p>

<h2>Las flags</h2>
<p>Un botón en la ficha abre las siete flags con casillas. Cambiar una se aplica al instante y el resultado dice qué cambió y qué no:</p>
<pre><code>Set hopper=true on TI-1a2b3c
  hopper: false -> true
  (6 flags unchanged)</code></pre>
<p>Es la misma vista de <a href="flags.html">la página de flags</a>, en pantalla. La <a href="permissions.html">página de permisos</a> explica qué se necesita para llegar hasta aquí.</p>

<h2>Para la consola</h2>
<p>La consola no tiene pantallas, y no es una carencia: es lo que permite que un script lea el resultado. Cada comando que en el juego abre una pantalla, en consola imprime el mismo dato en texto.</p>
<pre><code>&gt; /ig info TI-1a2b3c
Item:   TI-1a2b3c  (diamond_sword)
Owner:  SrIruma
State:  SEALED
Where:  1284 64 -3027  (sealed in the ground)
Since:  2026-09-28 19:03:11</code></pre>
<div class="tip"><strong>Sin <code>raw</code> hay texto para humanos; con <code>raw</code>, una línea parseable.</strong> Los comandos que se usan en scripts aceptan <code>raw</code> para dar una sola línea, sin la cabecera ni las líneas de registro.</div>
"""

TRANSLATIONS["database"] = """
<p class="lead">SQLite de serie, sin configurar nada. MySQL o PostgreSQL cuando un archivo se queda corto. Y la comprobación que impide que dos servidores actúen sobre el mundo equivocado.</p>
<p class="meta">Un archivo, o un servidor &#183; comprobado en el arranque</p>

<h2>Qué guarda</h2>
<p>Una fila por objeto rastreado, y nada más:</p>
<div class="table-wrap">
  <table>
    <thead><tr><th>Campo</th><th>Qué es</th></tr></thead>
    <tbody>
      <tr><td><code>id</code></td><td>El identificador, el mismo que va en el NBT del objeto</td></tr>
      <tr><td><code>owner</code></td><td>El UUID del dueño</td></tr>
      <tr><td><code>state</code></td><td>Dónde está: colocado, en el suelo, en una mano, en un contenedor</td></tr>
      <tr><td><code>location</code></td><td>Coordenadas, mundo y, si está en un contenedor, su id</td></tr>
      <tr><td><code>template</code></td><td>La plantilla de la que salió, si salió de alguna</td></tr>
      <tr><td><code>flags</code></td><td>Las siete, tal como están en ese objeto</td></tr>
      <tr><td><code>history</code></td><td>Los eventos, con fecha</td></tr>
    </tbody>
  </table>
</div>
<p>La copia del objeto en sí, con su NBT completo, está en el mundo, no en la base de datos. Eso es lo que permite <a href="commands.html">regenerar</a> un objeto perdido: la base de datos sabe qué era, y el mundo tenía la pieza.</p>

<h2>SQLite</h2>
<p>Es el valor por defecto y no hay nada que configurar. El archivo se crea en el primer arranque:</p>
<pre><code>plugins/ItemGuard/itemguard.db</code></pre>
<p>Nada sale de la máquina. Para la mayoría de servidores un plugin de esto, el archivo es suficiente y es la opción que menos cosas puede salir mal.</p>
<div class="tip"><strong>Cuándo cambiar.</strong> SQLite aguanta bien un servidor de tamaño normal. Si guardas el mundo en un disco de red, o si el archivo empieza a ir lento con muchos objetos, ese es el momento.</div>

<h2>MySQL y PostgreSQL</h2>
<p>En <code>config.yml</code>:</p>
<pre><code>database:
  type: mysql
  host: 127.0.0.1
  port: 3306
  name: itemguard
  user: itemguard
  password: cambia-esto</code></pre>
<p>Los drivers vienen dentro del jar. No hay que instalar nada ni cargar un <code>Class.forName</code> a mano.</p>
<p>El esquema se crea solo si no existe. Si la base de datos ya tiene tablas de ItemGuard de otra versión, se migran y se dice por consola qué se cambió.</p>

<h2>Una base de datos por servidor</h2>
<p>El motor se fija en el arranque y se comprueba contra el mundo. Si la base de datos ya guarda objetos de otro mundo, el plugin se niega a arrancar:</p>
<pre><code>Problem: this database already holds items from another world
Try: give each server its own database, or its own world</code></pre>
<p>El fallo que evita es uno de los más difíciles de diagnosticar: dos servidores, un mundo dividido, y objetos que aparecen en el sitio equivocado. Mejor un arranque que se niega a continuar.</p>
<div class="warn"><strong>No compartas la base de datos entre servidores con mundos distintos.</strong> El plugin te lo va a impedir, y el mensaje está arriba. Si ves ese error, la solución es una base de datos por servidor, no borrar las tablas.</div>

<h2>Copias de seguridad</h2>
<p>Con SQLite, copia el archivo con el servidor parado. Con MySQL o PostgreSQL, usa el mecanismo de cada motor, no una copia del archivo.</p>
<p>Los datos son pequeños. Una copia de <code>itemguard.db</code> ocupa unos pocos cientos de kilobytes con un servidor con cientos de objetos, así que la copia es barata y la pérdida no lo es.</p>
"""

TRANSLATIONS["faq"] = """<p class="lead">Las preguntas que más salen, respondidas. Si la tuya no está, el buscador de arriba la encuentra por palabra clave.</p>

<h2>Instalación</h2>

<h3>¿Necesito LuckPerms?</h3>
<p>No. LuckPerms se usa si lo tienes instalado, y nunca es necesario. El único puente opcional es SmartSpawner, y sin él ItemGuard funciona exactamente igual. Los drivers de base de datos vienen dentro del jar.</p>

<h3>Nadie puede ejecutar comandos</h3>
<p>Porque todos los permisos vienen en <code>false</code>, incluidos los de los operadores. Es deliberado. Mira <a href="permissions.html">Permisos</a> para ver los dieciocho nodos y el atajo <code>itemguard.admin</code>.</p>
<p>En un servidor de pruebas donde todo el mundo entra como operador, pon <code>console.ops-are-admins: true</code> y el estado de operador pasa a ser toda la política. En producción, deja eso en <code>false</code>.</p>

<h3>¿Paper 1.21 y Java 21 exactos?</h3>
<p>1.21 o superior, y Java 21. Cualquier fork de Paper con la misma API de plugins funciona. El plugin comprueba la versión al arrancar y dice qué espera si no coincide.</p>

<h2>Objetos</h2>

<h3>¿Puede perder o duplicar un objeto?</h3>
<p>No. El plugin nunca suelta un objeto al suelo por su cuenta ni lo duplica. Un objeto cae al suelo si un jugador lo suelta y su flag <code>drop</code> lo permite; en otro caso la acción se cancela y se avisa.</p>

<h3>Funciona con objetos de otros plugins</h3>
<p>Sí, mientras el objeto pueda llevar NBT. Se rastrean objetos de cualquier plugin que lleve el id en su NBT, incluidos los de ItemEdit.</p>

<h3>¿Y los objetos con enchantments?</h3>
<p>Se guardan tal cual, con sus encantamientos y sus nombres. El id va en un campo propio del NBT y no pisa nada que el objeto ya trajera.</p>

<h2>Protección</h2>

<h3>Una tolva se lleva mi objeto</h3>
<p>La flag <code>hopper</code> lo impide por defecto. Si has puesto <code>hopper=true</code> en esa plantilla, ya no lo impide: cámbiala con <code>/ig flag</code> o quítala de la plantilla.</p>
<p>La <a href="flags.html">página de flags</a> explica los siete interruptores y sus valores por defecto.</p>

<h3>Alguien lo mina de su bloque</h3>
<p>La flag <code>break</code> lo impide. El permiso <code>itemguard.break</code> es lo que permite a un administrador hacerlo de todas formas, y queda registrado.</p>

<h3>Una explosión lo destruye</h3>
<p>La flag <code>explosion</code> lo impide. Está en <code>false</code> por defecto, y es una de las razones por las que los sellos sobreviven a un TNT.</p>

<h2>Sellos y reclamos</h2>

<h3>¿Cómo recupera su dueño un objeto?</h3>
<p>Con <code>/ig reclaim</code>, desde donde esté. El reclamo verifica que quien pide es el dueño, que el objeto sigue donde se selló y que el mundo es el mismo. Si algo falla, lo dice y no mueve nada. La <a href="seals.html">página de sellos</a> lo explica paso a paso.</p>

<h3>Un admin puede quedarse con un objeto</h3>
<p>No. El reclamo depende de la propiedad, no de los permisos. Un admin sin propiedad no puede reclamar el objeto de otro. Lo que sí puede es <code>/ig recover</code>, que es una operación de administración y queda registrada a su nombre.</p>

<h3>Un intento fallido aparece en el historial</h3>
<p>Sí, con el motivo. Un reclamo denegado deja rastro, que es justo lo que hace que un reclamo correcto sea creíble delante de alguien que lo discute.</p>

<h2>Configuración</h2>

<h3>¿Puedo cambiar las opciones sin reiniciar?</h3>
<p>Sí. <code>/ig reload</code> vuelve a leer configuración, mensajes, plantillas y datos. El único valor que no se puede cambiar en caliente es el motor de base de datos, que se fija en el arranque; para cambiarlo hay que reiniciar.</p>

<h3>Perdí mi config.yml</h3>
<p>Se regenera al borrar el archivo y arrancar, con los valores por defecto. Tus comentarios se pierden, pero no tus objetos: están en la base de datos, que es un archivo aparte.</p>

<h3>Dos servidores, un archivo</h3>
<p>El plugin lo impide, porque dos servidores con mundos distintos sobre un mismo archivo acabarían con objetos en el sitio equivocado. El error de arranque te lo dice, y la solución es una base de datos por servidor. La <a href="database.html">página de base de datos</a> lo explica.</p>

<h2>Traducciones</h2>

<h3>¿Cómo cambio el idioma?</h3>
<p>El idioma se elige en el primer arranque y luego se cambia en <code>config.yml</code>. Los mensajes están en <code>plugins/ItemGuard/translations/</code>, un archivo por idioma, editables y recargables con <code>/ig reload</code>. La <a href="translations.html">página de traducciones</a> documenta cada marcador.</p>

<h3>Añadí una versión y mis textos siguen ahí</h3>
<p>Sí. Las claves nuevas se añaden a tu archivo con su valor por defecto; las tuyas no se tocan. Los mensajes que no hayas traducido salen en inglés hasta que los completes.</p>

<h2>Compra</h2>

<h3>¿Es gratis y dónde lo consigo?</h3>
<p>ItemGuard es un plugin de pago, vendido en BuiltByBit. Si prefieres verlo funcionar antes de gastar nada, BuiltByBit tiene un servidor de prueba con el plugin ya instalado; se entra desde la ficha del plugin.</p>

<h3>¿Puedo probarlo antes de comprarlo?</h3>
<p>Sí. El <a href="quickstart.html">inicio rápido</a> de arriba es la instalación entera; el servidor de prueba es para jugar con el plugin en el juego. Se entra desde la ficha en BuiltByBit.</p>

<h2>Reportar un problema</h2>

<h3>¿Se rompió algo? ¿Qué leo primero?</h3>
<p>El bloque de arranque, que imprime los datos: el estado, el motor en uso con las credenciales ocultas, y un problema nombrado con su solución cuando no puede arrancar. Todo eso va también a <code>plugins/ItemGuard/logs/</code> cuando el registro en archivo está activo. Luego esta página. Luego el <a href="https://github.com/SrIruma/itemguard-web/issues">rastreador de issues</a>, o el correo del final de la página si prefieres no usar una cuenta.</p>

<h3>¿Cómo reporto un problema?</h3>
<p>De las dos formas que aparecen al final de esta página:</p>
<ul>
<li><strong>Un issue</strong> en <a href="https://github.com/SrIruma/itemguard-web/issues">el repositorio de la documentación</a>. Es público, cualquiera puede abrir uno, y no hace falta una cuenta más allá de GitHub. Busca primero entre los issues abiertos: muchos reportes son el mismo error de configuración, y encontrarlo ya resuelto es más rápido que esperar.</li>
<li><strong>Un correo</strong> a MrTsumugi@proton.me, que llega a los dos. Más lento, y sin registro público, así que sirve para lo que no prefieras postear abierto.</li>
</ul>
<p>Como sea, lo primero que merece adjuntarse es el bloque de arranque y <code>plugins/ItemGuard/logs/</code>: la mayoría de los problemas los responde la línea que nombra el motor en uso y el problema que encontró.</p>
<div class="note"><strong>Los reportes de abuso y de seguridad no van en público.</strong> Si el reporte es sobre alguien abusando del plugin en vez de sobre el plugin fallando, usa el correo. Un issue público es un registro permanente y buscable.</div>
"""


def main() -> int:
    CONTENT.mkdir(parents=True, exist_ok=True)
    missing = []
    for slug in SLUGS:
        text = TRANSLATIONS.get(slug)
        if not text:
            missing.append(slug)
            continue
        body = text.strip() + "\n"
        # Se comprueba que no queden restos en ingles sin querer.
        (CONTENT / f"{slug}.html").write_text(body, encoding="utf-8")
        print(f"OK content/es/{slug}.html  ({len(body)} bytes)")

    if missing:
        print(f"\nSIN TRADUCIR: {', '.join(missing)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
