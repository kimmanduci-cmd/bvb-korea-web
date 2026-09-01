from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import socketserver
import os

PORT = 8088
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class NoCacheHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

class CustomThreadingServer(ThreadingHTTPServer):
    allow_reuse_address = True

if __name__ == '__main__':
    server_address = ('127.0.0.1', PORT)
    httpd = CustomThreadingServer(server_address, NoCacheHandler)
    print(f"BVB Server running at http://localhost:{PORT}/", flush=True)
    httpd.serve_forever()
