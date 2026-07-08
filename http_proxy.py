import socket
import sys
from threading import Thread

# --- CONFIGURATION ---
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 9999
BUFFER_SIZE = 4096


def handle_client(client_socket, client_address):
    """Processes incoming request strings from the local client."""
    print(f"[*] Intercepted connection handshake from: {client_address[0]}:{client_address[1]}")
    try:
        # 1. Receive the initial request header block from the client
        request = client_socket.recv(BUFFER_SIZE)
        if not request:
            return

        # Decode header selectively to parse destination host routing profile
        first_line = request.decode("utf-8", errors="ignore").split("\n")[0]
        print(f"    |_ Request Line: {first_line.strip()}")

        # 2. Extract destination web domain from the request line
        # Format typical: "GET http://www.example.com/index.html HTTP/1.1" or "CONNECT example.com:443"
        if " " not in first_line:
            return
            
        url_part = first_line.split(" ")[1]

        # Basic parsing matrix to isolate hostname and port configurations
        if "://" in url_part:
            url_part = url_part.split("://")[1]
            
        lines = url_part.split("/")
        host_and_port = lines[0]
        
        if ":" in host_and_port:
            target_host, target_port = host_and_port.split(":")
            target_port = int(target_port)
        else:
            target_host = host_and_port
            target_port = 80  # Default HTTP port standard

        print(f"    |_ Routing Target: {target_host} on Port: {target_port}")

        # 3. Establish upstream connection socket pipeline to the real server
        upstream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        upstream_socket.connect((target_host, target_port))

        # Handle HTTPS tunneling protocol (CONNECT request pattern)
        if "CONNECT" in first_line:
            # Tell the client that a structural secure bridge connection is established
            client_socket.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            # Spin off bidirectional traffic relays immediately for the encrypted tunnel
            t1 = Thread(target=bridge_relay, args=(client_socket, upstream_socket))
            t2 = Thread(target=bridge_relay, args=(upstream_socket, client_socket))
            t1.start()
            t2.start()
        else:
            # Handle cleartext HTTP modifications mid-stream
            # Modify headers or look at raw inputs here before passing upstream
            upstream_socket.sendall(request)
            
            # Capture the response returned from the real target and send back to client
            while True:
                response = upstream_socket.recv(BUFFER_SIZE)
                if len(response) > 0:
                    client_socket.sendall(response)
                else:
                    break
            upstream_socket.close()
            client_socket.close()

    except Exception as e:
        print(f"[!] Proxy processing exception: {e}")
        client_socket.close()


def bridge_relay(source, destination):
    """Continuously routes binary data streams between two linked sockets."""
    try:
        while True:
            data = source.recv(BUFFER_SIZE)
            if not data:
                break
            destination.sendall(data)
    except socket.error:
        pass
    finally:
        source.close()
        destination.close()


def start_proxy():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((PROXY_HOST, PROXY_PORT))
        server.listen(20)
        print("=" * 60)
        print(f"[+] HTTP Proxy running locally at: {PROXY_HOST}:{PROXY_PORT}")
        print("[*] Configure your browser or test with: curl -x http://127.0.0.1:9999 http://example.com")
        print("=" * 60)

        while True:
            client_sock, addr = server.accept()
            proxy_thread = Thread(target=handle_client, args=(client_sock, addr))
            proxy_thread.daemon = True
            proxy_thread.start()

    except KeyboardInterrupt:
        print("\n[-] Shutting down proxy core infrastructure.")
    finally:
        server.close()
        sys.exit(0)


if __name__ == "__main__":
    start_proxy()
