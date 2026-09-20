import http.server
import functools
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "site"))

class CleanUrlHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            super().do_GET()
        except Exception as e:
            import traceback
            print("ERROR IN do_GET:")
            traceback.print_exc()

    def translate_path(self, path):
        res = super().translate_path(path)
        if not os.path.exists(res) and os.path.exists(res + ".html") and not os.path.isdir(res + ".html"):
            return res + ".html"
        return res

def run():
    handler = functools.partial(CleanUrlHandler, directory=SITE_DIR)
    with http.server.ThreadingHTTPServer(("", PORT), handler) as server:
        print(f"Serving rewards site from {SITE_DIR}")
        print(f"Local URL: http://localhost:{PORT}")
        print(f"Clean URLs enabled (e.g. /rewards, /items/bundles/bundle-content-creation)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run()
