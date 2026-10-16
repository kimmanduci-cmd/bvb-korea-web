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

    def log_message(self, format, *args):
        try:
            sys.stderr.write("%s - - [%s] %s\n" %
                             (self.address_string(),
                              self.log_date_time_string(),
                              format % args))
            sys.stderr.flush()
        except Exception:
            pass

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

def log_safe(msg):
    try:
        sys.stderr.write(str(msg) + '\n')
        sys.stderr.flush()
    except Exception:
        pass

class CustomThreadingServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def handle_error(self, request, client_address):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_type in (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            return
        try:
            super().handle_error(request, client_address)
        except Exception:
            pass

def serve_on_port(port):
    while True:
        try:
            server_address = ('', port)
            httpd = CustomThreadingServer(server_address, NoCacheHandler)
            log_safe(f"BVB Server running on port {port} (http://localhost:{port}/)")
            httpd.serve_forever()
        except (KeyboardInterrupt, SystemExit):
            log_safe(f"Port {port} stopped.")
            break
        except Exception as e:
            log_safe(f"Port {port} error: {e}. Re-binding in 1 second...")
            time.sleep(1)

if __name__ == '__main__':
    log_safe("BVB Server initializing...")
    t = threading.Thread(target=serve_on_port, args=(8088,), daemon=False)
    t.start()
    serve_on_port(8080)
