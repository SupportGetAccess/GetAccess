from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

print("=" * 50)
print("Get Access - Frontend (HTTP)")
print("=" * 50)
print("PC: http://localhost:3000")
print("=" * 50)

http_server = HTTPServer(('0.0.0.0', 3000), CORSRequestHandler)
http_server.serve_forever()
