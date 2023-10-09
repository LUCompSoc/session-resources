import re

import lib


class HttpRequestHandler(lib.RequestHandler):
    def handle(self):
        """Handles a request from a client"""
        method, url, version = self.parse_control_data()
        print(f'[REQUEST CTRL] {method = }; {url = }; {version = }')

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


if __name__ == '__main__':
    exit(lib.main(HttpRequestHandler))

