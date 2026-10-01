#!/usr/bin/env python3
"""
Servidor de previsualizacion que se parece a GitHub Pages.

Sirve el repositorio bajo /itemguard-web/ y, cuando una ruta no existe,
entrega el 404.html del sitio con codigo 404, que es lo que hace Pages.
El "python3 -m http.server" no lo hace: responde con su propia pagina de
error, y por eso el 404 del sitio nunca se ve en local.

    python3 scripts/serve.py [puerto]
"""
import sys
import pathlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = pathlib.Path(__file__).resolve().parent.parent
PREFIX = "/itemguard-web"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class PagesLikeHandler(SimpleHTTPRequestHandler):
    """Como GitHub Pages: prefijo de subdirectorio y 404 propio."""

    def translate_path(self, path: str) -> str:
        # SimpleHTTPRequestHandler sirve desde cwd; aqui se quita el
        # prefijo y se ancla en la raiz del repositorio.
        if path.startswith(PREFIX):
            path = path[len(PREFIX):] or "/"
        rel = path.lstrip("/")
        target = (ROOT / rel).resolve()
        # No se sale del repositorio.
        if ROOT not in target.parents and target != ROOT:
            return str(ROOT / "__out_of_tree__")
        return str(target)

    def send_error(self, code, message=None, explain=None):
        """En vez de la pagina de error del servidor, el 404 del sitio."""
        if code == 404:
            # Pages sirve un unico 404, el de la raiz. El arbol en
            # espanol tiene el suyo, asi que se elige segun la ruta
            # pedida: asi se revisa el 404 en el idioma que se lee.
            in_es = self.path.startswith(PREFIX + "/es/") or self.path.startswith(
                PREFIX + "/es"
            )
            page = ROOT / ("es/404.html" if in_es else "404.html")
            if page.exists():
                body = page.read_bytes()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(body)
                return
        super().send_error(code, message, explain)

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))


def main() -> int:
    server = ThreadingHTTPServer(("0.0.0.0", PORT), PagesLikeHandler)
    print(f"sirviendo {ROOT}")
    print(f"  http://localhost:{PORT}{PREFIX}/")
    print(f"  un 404 de prueba: http://localhost:{PORT}{PREFIX}/no-existe")
    print("  Ctrl+C para parar")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nparado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
