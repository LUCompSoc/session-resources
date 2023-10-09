import re

import lib


class HttpRequestHandler(lib.RequestHandler):
    def handle(self):
        """Handles a request from a client"""
        method, url, version = self.parse_control_data()
        print(f'[REQUEST CTRL] {method = }; {url = }; {version = }')
        if not self.is_supported_version(version):
            print('[ERROR] unsupported version')
            return
        if not self.is_supported_method(method):
            print('[ERROR] unsupported method')
            return

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

    def is_supported_version(self, version: str) -> bool:
        """Checks if the given version is supported by the server

        Supported versions are HTTP/1.0 and HTTP/1.1
        """
        return re.match(r'HTTP/1.[01]', version) is not None

    def is_supported_method(self, method: str) -> bool:
        """Checks if the given method is supported by the server

        Supported methods are GET and POST"""
        return method in {'GET', 'POST'}


if __name__ == '__main__':
    exit(lib.main(HttpRequestHandler))

