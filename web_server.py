import mimetypes
import os
import socket
import sys
from threading import Thread

# --- CONFIGURATION ---
HOST = "127.0.0.1"
PORT = 8080
WEB_ROOT = "www"  # Directory where your HTML/CSS/JS files live


def create_mock_website():
    """Creates a simple web root folder and an index file for testing."""
    if not os.path.exists(WEB_ROOT):
        os.makedirs(WEB_ROOT)

    index_html = """<!DOCTYPE html>
<html>
<head>
    <title>Custom Python Server</title>
    <style>body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }</style>
</head>
<body>
    <h1 style="color: #4CAF50;">Success!</h1>
    <p>This page is being served by a custom multithreaded raw Python socket server.</p>
</body>
</html>
"""
    with open(os.path.join(WEB_ROOT, "index.html"), "w") as f:
        f.write(index_html)
    print(f"[+] Created mock environment directory: ./{WEB_ROOT}/index.html")


def handle_client(client_socket):
    """Processes an individual HTTP client connection request."""
    try:
        # Read the raw HTTP request data from the stream
        request_data = client_socket.recv(2048).decode("utf-8")
        if not request_data:
            return

        # Parse the HTTP Request Line (e.g., "GET /index.html HTTP/1.1\r\n")
        lines = request_data.split("\r\n")
        request_line = lines[0]
        parts = request_line.split(" ")

        if len(parts) < 2:
            return

        method, requested_path = parts[0], parts[1]
        print(f"[*] Incoming Request: {method} -> {requested_path}")

        # Basic path routing logic
        if requested_path == "/":
            requested_path = "/index.html"

        # Sanitize path to prevent Directory Traversal vulnerabilities (../)
        clean_path = os.path.normpath(requested_path.lstrip("/"))
        file_path = os.path.join(WEB_ROOT, clean_path)

        # Ensure the resolved file path remains strictly inside our WEB_ROOT
        if not file_path.startswith(WEB_ROOT):
            send_http_error(client_socket, 403, "Forbidden")
            return

        # Serve requested file if it exists, otherwise trigger a 404
        if os.path.exists(file_path) and os.path.isfile(file_path):
            serve_file(client_socket, file_path)
        else:
            send_http_error(client_socket, 404, "Not Found")

    except Exception as e:
        print(f"[!] Error processing request: {e}")
    finally:
        client_socket.close()


def serve_file(client_socket, file_path):
    """Reads a local file and constructs a valid HTTP/1.1 200 OK response."""
    with open(file_path, "rb") as f:
        content = f.read()

    # Dynamically determine the content type (e.g., text/html, image/png)
    content_type, _ = mimetypes.guess_type(file_path)
    if not content_type:
        content_type = "application/octet-stream"

    # Assemble raw HTTP response headers
    response_header = "HTTP/1.1 200 OK\r\n"
    response_header += f"Content-Type: {content_type}\r\n"
    response_header += f"Content-Length: {len(content)}\r\n"
    response_header += "Connection: close\r\n\r\n"

    # Send the headers, then the binary payload body
    client_socket.sendall(response_header.encode("utf-8"))
    client_socket.sendall(content)


def send_http_error(client_socket, status_code, status_message):
    """Sends a generic structured HTML error page to the client browser."""
    body = f"<html><body><h1>{status_code} {status_message}</h1></body></html>"
    header = f"HTTP/1.1 {status_code} {status_message}\r\n"
    header += "Content-Type: text/html\r\n"
    header += f"Content-Length: {len(body)}\r\n"
    header += "Connection: close\r\n\r\n"

    client_socket.sendall((header + body).encode("utf-8"))


def start_server():
    create_mock_website()

    # Initialize a TCP Socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allow prompt socket reuse after server restarts (prevents "Address already in use" errors)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print("=" * 60)
        print(f"[+] HTTP Web Server running live at: http://{HOST}:{PORT}")
        print("=" * 60)

        while True:
            # Main accept loop listens for browser requests
            client_sock, addr = server.accept()
            
            # Spin up a dedicated thread for every new client connection
            client_thread = Thread(target=handle_client, args=(client_sock,))
            client_thread.daemon = True
            client_thread.start()

    except KeyboardInterrupt:
        print("\n[-] Server shutting down cleanly.")
    finally:
        server.close()
        sys.exit(0)


if __name__ == "__main__":
    start_server()
