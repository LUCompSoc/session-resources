import socketserver
from typing import Any, Iterable, NamedTuple, Optional

__all__ = [
    'RequestHandler', 'Request',
    'main', 'start_server',
]


class RequestHandler(socketserver.StreamRequestHandler):
    def read(self, count: int) -> str:
        """Reads `count` characters from the TCP stream"""
        return self.rfile.read(count).decode()

    def readline(self) -> str:
        """Reads a line from the TCP stream"""
        return self.rfile.readline().strip().decode()

    def write(self, data: str):
        """Writes a string to the TCP stream"""
        self.wfile.write(data.encode())

    def writeline(self, line: str):
        """Writes a line to the TCP stream, adding the appropriate line ending"""
        self.wfile.write(f'{line}\r\n'.encode())

    def writelines(self, lines: Iterable[str]):
        """Write multiple lines to the TCP stream, adding the appropriate line endings"""
        self.wfile.write(b'\r\n'.join(line.encode() for line in lines))

    @property
    def address(self) -> tuple[str, int]:
        return self.server.server_address  # type: ignore

    @property
    def hosts(self) -> set[str]:
        host, port = self.address
        hosts = {f'{host}:{port}'}
        if host == '127.0.0.1':
            hosts.add(f'localhost:{port}')
        return hosts


class Request(NamedTuple):
    method: str
    url: str
    version: str
    headers: dict[str, Any]
    body: Any


def start_server(handler, host: Optional[str] = None, port: int = 0):
    host = host or 'localhost'
    with socketserver.TCPServer((host, port), handler) as server:
        server.allow_reuse_port = True
        port = server.server_address[1]
        print(f'Starting server on {host}:{port}')
        with open('address', 'w') as f:
            f.write(f'{host}:{port}')
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('\nServer shutting down')
            server.shutdown()


main = start_server

