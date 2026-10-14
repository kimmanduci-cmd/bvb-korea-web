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

class CustomThreadingServer(ThreadingHTTPServer):
    allow_reuse_address = True

def serve_on_port(port):
    try:
        server_address = ('', port)
        httpd = CustomThreadingServer(server_address, NoCacheHandler)
        print(f"BVB Server running on port {port} (http://localhost:{port}/)", flush=True)
        httpd.serve_forever()
    except Exception as e:
        print(f"Port {port} error: {e}", flush=True)

if __name__ == '__main__':
    threads = []
    for port in [8080, 8088]:
        t = threading.Thread(target=serve_on_port, args=(port,), daemon=True)
        t.start()
        threads.append(t)
    
    print("BVB Server successfully running. Ready for browser connections!", flush=True)
    try:
        while True:
            threading.Event().wait(3600)
    except (KeyboardInterrupt, SystemExit):
        print("Server stopped.", flush=True)
