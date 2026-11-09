"""Run the page on this PC at http://127.0.0.1:8000/ with the same headers Cloudflare sends."""
import http.server

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      ".mjs": "text/javascript", ".js": "text/javascript", ".wasm": "application/wasm"}

    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "credentialless")
        super().end_headers()

if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
