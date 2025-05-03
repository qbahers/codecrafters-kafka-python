import socket  # noqa: F401


UNSUPPORTED_VERSION = 35

def main():
    # You can use print statements as follows for debugging,
    # they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    connection, address = server.accept() # wait for client
    data = connection.recv(1024)
    request_api_key = data[4:6]
    request_api_version = int.from_bytes(data[6:8])
    correlation_id = data[8:12]
    error_code = (0 if 0 <= request_api_version <= 4 else UNSUPPORTED_VERSION).to_bytes(2, signed=True)
    min_version = (0).to_bytes(2, signed=True)
    max_version = (4).to_bytes(2, signed=True)
    _tagged_fields = (0).to_bytes(1, signed=True)
    api_keys = (2).to_bytes(1, signed=True) + request_api_key + min_version + max_version + _tagged_fields
    throttle_time_ms = (0).to_bytes(4, signed=True)
    response = correlation_id + error_code + api_keys + throttle_time_ms + _tagged_fields
    response_message_size = len(response).to_bytes(4, signed=True)
    connection.sendall(response_message_size + response)


if __name__ == "__main__":
    main()
