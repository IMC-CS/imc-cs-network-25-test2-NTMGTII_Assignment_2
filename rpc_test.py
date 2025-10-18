import pytest
import time
from multiprocessing import Process

from rpc import RPCClient, RPCServer
from rpc_server import add, sub, fibonacci, checksum

@pytest.fixture
def setup_server():
    server = RPCServer()
    server.registerMethod(add)
    server.registerMethod(sub)
    server.registerMethod(fibonacci)
    server.registerMethod(checksum)

    server_process = Process(target=server.run)
    server_process.start()

    time.sleep(1)  # wait for server start

    yield '127.0.0.1'

    server_process.terminate()
    server_process.join()


def test_add_and_sub(setup_server):
    client = RPCClient(setup_server, 8080)
    client.connect()
    assert client.add(2, 8) == 10
    assert client.sub(6, 3) == 3
    client.disconnect()


def test_fibonacci(setup_server):
    client = RPCClient(setup_server, 8080)
    client.connect()
    assert client.fibonacci(10) == 55
    client.disconnect()


# def test_checksum(setup_server):
#     client = RPCClient(setup_server, 8080)
#     client.connect()
#     assert client.checksum([1, 2, 3, 4]) == 10
#     client.disconnect()

    
