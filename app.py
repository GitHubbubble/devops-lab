from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket

VERSION = os.getenv("APP_VERSION", "1.0.0")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.respond(200, "ok\n")
            return

        if self.path == "/readyz":
            self.respond(200, "ready\n")
            return

        if self.path != "/":
            self.respond(404, "not found\n")
            return

        message = os.getenv("MESSAGE", "Hello from bubernatkses!")

        body = (
            f"message: {message}\n"
            f"version: {VERSION}\n"
            f"hostname: {socket.gethostname()}\n"
        )
        self.respond(200, body)

    def respond(self, status, body):
        data = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

def main():
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print(f"Listening on port 8080, version {VERSION}", flush=True)
    server.serve_forever()  


if __name__ == "__main__":
    main()
