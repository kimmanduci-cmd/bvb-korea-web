from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import threading
import os

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

def serve_on_port(port):
    try:
        server_address = ('127.0.0.1', port)
        httpd = CustomThreadingServer(server_address, NoCacheHandler)
        print(f"BVB Server running at http://localhost:{port}/", flush=True)
        httpd.serve_forever()
    except Exception as e:
        print(f"Port {port} error: {e}", flush=True)

if __name__ == '__main__':
    threads = []
    for port in [8080, 8088]:
        t = threading.Thread(target=serve_on_port, args=(port,), daemon=False)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
