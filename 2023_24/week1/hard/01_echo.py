import lib


class HttpRequestHandler(lib.RequestHandler):
    def handle(self):
        """Handles a request from a client"""
        while (data := self.readline()).strip():
            print('[REQUEST]', data)
            self.write(data)


if __name__ == '__main__':
    exit(lib.main(HttpRequestHandler))

