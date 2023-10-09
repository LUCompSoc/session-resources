import socket


def main():
    with open('address', 'r') as f:
        host, port = f.read().strip().split(':')
        port = int(port)

    data = '\r\n'.join([
        'GET /greet HTTP/1.0',
        f'Host: {host}:{port}',
        'Content-Type: application/json',
        'Content-Length: 19',
        '',
        '{ "name": "world" }',
        '',
    ])

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((host, port))
        sock.sendall(bytes(data, "utf-8"))

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")

    print("Sent:\n```\n{}```".format(data))
    print("Received:\n```\n{}```".format(received))


if __name__ == '__main__':
    exit(main())

