import json
import re
from pprint import pprint
from typing import Any

import lib
from lib import Request, RequestHandler


def parse_header_values(raw_headers: dict[str, str]) -> dict[str, Any]:
    """Converts headers to meaningful types"""
    # the conversions of fields to take place
    conversions = {
        'content-length': int,
    }
    # copy the headers in case the raw headers are used elsewhere
    headers: dict[str, Any] = raw_headers.copy()
    # convert all fields present
    for name, converter in conversions.items():
        if name in headers:
            headers[name] = converter(headers[name])
    return headers


class HttpRequestHandler(RequestHandler):
    def handle(self):
        """Handles a request from a client"""
        request = self.parse_request()
        print('[REQUEST]')
        pprint(request)
        self.send_response()

    def send_response(self) -> None:
        self.writelines([
            'HTTP/1.0 200 OK',
            'Server: my-http',
            '',
            'Hello from the server!',
            '',
        ])

    def parse_request(self) -> Request | None:
        method, url, version = self.parse_control_data()
        if not self.is_supported_version(version):
            print('[ERROR] unsupported version')
            return
        if not self.is_supported_method(method):
            print('[ERROR] unsupported method')
            return
        headers = self.parse_headers()
        if not self.is_allowed_host(headers):
            print('[ERROR] forbidden host')
            return
        body = self.parse_body(headers)
        return Request(
            method, url, version,
            headers,
            body,
        )

    def parse_control_data(self) -> tuple[str, str, str]:
        """Gets the method, url, and version from the control data"""
        # read a line, and convert all whitespace to single spaces
        ctrl_data = re.sub(r'[ \t]+', ' ', self.readline())
        # get the method and url
        method, url, *rest = ctrl_data.split(' ')
        if len(rest) == 0:
            # HTTP/0.9 won't give a version
            return method, url, 'HTTP/0.9'
        # Later versions will
        return method, url, rest[0]

    def parse_headers(self):
        # convert the headers to a dictionary
        headers = dict(self._read_headers())
        return parse_header_values(headers)

    def _read_headers(self):
        # read every line until a blank
        while (line := self.readline()).strip():
            # split the header into a name and value
            name, value = line.split(':', 1)
            # header names are case insensitive
            yield name.strip().lower(), value.strip()

    def parse_body(self, headers) -> Any:
        body = self._read_body(headers)
        if 'content-type' not in headers or body is None:
            return body
        if headers['content-type'] == 'application/json':
            return json.loads(body)
        return body

    def _read_body(self, headers: dict[str, Any]) -> str | None:
        if 'content-length' in headers:
            return self.read(headers['content-length'])
        return None

    def is_supported_version(self, version: str) -> bool:
        """Checks if the given version is supported by the server

        Supported versions are HTTP/1.0 and HTTP/1.1
        """
        return re.match(r'HTTP/1.[01]', version) is not None

    def is_supported_method(self, method: str) -> bool:
        """Checks if the given method is supported by the server

        Supported methods are GET and POST"""
        return method in {'GET', 'POST'}

    def is_allowed_host(self, headers: dict[str, Any]) -> bool:
        """Checks if the host header is set and if it matches the server address"""
        if 'host' not in headers:
            return True
        host: str = headers['host']
        return host in self.allowed_hosts

    @property
    def allowed_hosts(self):
        return self.hosts


if __name__ == '__main__':
    exit(lib.main(HttpRequestHandler))

