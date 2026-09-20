import os
import http.server
import socketserver
import urllib.parse

PORT = 3000
SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../site'))

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        # Strip trailing slash except for root
        if path != '/' and path.endswith('/'):
            path = path[:-1]

        local_path = os.path.join(SITE_DIR, path.lstrip('/'))

        if os.path.isdir(local_path):
            index_html = os.path.join(local_path, 'index.html')
            if os.path.isfile(index_html):
                self.path = path + ('/' if not path.endswith('/') else '') + 'index.html'
        elif not os.path.isfile(local_path):
            if os.path.isfile(local_path + '.html'):
                query_str = f"?{parsed.query}" if parsed.query else ""
                self.path = path + '.html' + query_str

        return super().do_GET()

if __name__ == '__main__':
    handler = CleanURLHandler
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving OWGT Rewards at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
