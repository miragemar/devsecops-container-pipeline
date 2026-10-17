
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            response = {
                "status": "healthy"
            }
            self.send_response(200)
        elif self.path == "/":
            response = {
                "app": "Secure Container Delivery Platform",
                "status": "running"
            }
            self.send_response(200)
        else:
            response = {
                "error": "Not found"
            }
            self.send_response(404)

        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), AppHandler)
    print("Application listening on port 8000")
    server.serve_forever()
