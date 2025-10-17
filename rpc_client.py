from rpc import RPCClient

if __name__ == "__main__":
    client = RPCClient('127.0.0.1', 8080)

    client.connect()

    print("add(5, 6) =", client.add(5, 6))
    print("sub(5, 6) =", client.sub(5, 6))
    print("fibonacci(10) =", client.fibonacci(10))
    print("checksum([1, 2, 3, 4]) =", client.checksum([1, 2, 3, 4]))

    client.disconnect()
