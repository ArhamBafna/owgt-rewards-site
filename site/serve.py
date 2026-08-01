import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = os.path.dirname(__file__)

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        req_path = self.path.split('?')[0].rstrip('/')
        path = self.translate_path(req_path)
        if os.path.exists(path + '.html') and os.path.isfile(path + '.html'):
            self.path = req_path + '.html'
        elif os.path.isdir(path) and os.path.exists(os.path.join(path, 'index.html')):
            if not self.path.endswith('/'):
                self.send_response(301)
                self.send_header('Location', self.path + '/')
                self.end_headers()
                return
        super().do_GET()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), CleanURLHandler) as httpd:
        print(f"Serving HTTP on 0.0.0.0 port {PORT} (http://localhost:{PORT}/)...")
        httpd.serve_forever()
