import socket
import json


class RPCServer:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.methods = {}

    def registerMethod(self, func):
        """Register a function that can be called remotely."""
        self.methods[func.__name__] = func

    def run(self):
        """Run the RPC server loop."""
        print(f"Server running on {self.host}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen(1)
            while True:
                conn, addr = s.accept()
                print(f"Connection from {addr}")
                with conn:
                    data = conn.recv(1024)
                    if not data:
                        continue

                    try:
                        req = json.loads(data.decode())
                        method = req.get("method")
                        params = req.get("params", [])
                        if method in self.methods:
                            result = self.methods[method](*params)
                            resp = {"result": result}
                        else:
                            resp = {"error": f"Unknown method '{method}'"}
                    except Exception as e:
                        resp = {"error": str(e)}

                    conn.sendall(json.dumps(resp).encode())


class RPCClient:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        """Connect to the RPC server."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def disconnect(self):
        """Close the connection."""
        if self.sock:
            self.sock.close()
            self.sock = None

    def call(self, method, *params):
        """Send an RPC request and wait for the result."""
        if not self.sock:
            raise ConnectionError("Not connected to server")

        req = {"method": method, "params": params}
        self.sock.sendall(json.dumps(req).encode())

        data = self.sock.recv(1024)
        resp = json.loads(data.decode())

        if "result" in resp:
            return resp["result"]
        else:
            raise Exception(resp.get("error", "Unknown error"))

    # convenience wrappers
    def add(self, a, b):
        return self.call("add", a, b)

    def sub(self, a, b):
        return self.call("sub", a, b)

    def fibonacci(self, n):
        return self.call("fibonacci", n)

    def checksum(self, byte_array):
        return self.call("checksum", byte_array)
