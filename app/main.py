import socket  # noqa: F401


UNSUPPORTED_VERSION = 35

def main():
    # You can use print statements as follows for debugging,
    # they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    connection, address = server.accept() # wait for client
    data = connection.recv(1024)
    request_api_version = int.from_bytes(data[6:8])
    correlation_id = data[8:12]
    response_message_size = (0).to_bytes(4, signed=True)
    error_code = (0 if 0 <= request_api_version <= 4 else UNSUPPORTED_VERSION).to_bytes(2, signed=True)
    connection.sendall(response_message_size + correlation_id + error_code)


if __name__ == "__main__":
    main()
