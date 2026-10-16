from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import threading
import os
import sys

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class NoCacheHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_POST(self):
        if self.path == '/api/save_editorial':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                json_path = os.path.join(DIRECTORY, 'editorial_posts.json')
                with open(json_path, 'wb') as f:
                    f.write(post_data)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"status":"ok"}')
                return
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
                return
        elif self.path == '/api/save_categories':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                json_path = os.path.join(DIRECTORY, 'editorial_categories.json')
                with open(json_path, 'wb') as f:
                    f.write(post_data)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"status":"ok"}')
                return
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
                return
        self.send_error(404, "Not Found")

import time

class CustomThreadingServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def handle_error(self, request, client_address):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_type in (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            return
        super().handle_error(request, client_address)

def serve_on_port(port):
    while True:
        try:
            server_address = ('', port)
            httpd = CustomThreadingServer(server_address, NoCacheHandler)
            print(f"BVB Server running on port {port} (http://localhost:{port}/)", flush=True)
            httpd.serve_forever()
        except (KeyboardInterrupt, SystemExit):
            print(f"Port {port} stopped.", flush=True)
            break
        except Exception as e:
            print(f"Port {port} error: {e}. Re-binding in 1 second...", flush=True)
            time.sleep(1)

if __name__ == '__main__':
    print("BVB Server initializing...", flush=True)
    t = threading.Thread(target=serve_on_port, args=(8088,), daemon=False)
    t.start()
    serve_on_port(8080)
