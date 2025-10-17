from rpc import RPCServer


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def fibonacci(n):
    """Return the n-th Fibonacci number, or raise ValueError if invalid."""
    if not isinstance(n, int) or n < 0:
        raise ValueError("Invalid input")

    if n == 0:
        return 0
    elif n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def checksum(byte_array):
    """Compute simple checksum of a list of byte values."""
    if not isinstance(byte_array, (list, bytes, bytearray)):
        raise ValueError("Invalid input type")

    try:
        return sum(byte_array) % 256
    except TypeError:
        raise ValueError("Invalid input content")


if __name__ == "__main__":
    server = RPCServer()

    server.registerMethod(add)
    server.registerMethod(sub)
    server.registerMethod(fibonacci)
    server.registerMethod(checksum)

    print("RPC server starting...")
    server.run()

