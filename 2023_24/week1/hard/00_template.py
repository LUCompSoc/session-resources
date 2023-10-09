import lib


class HttpRequestHandler(lib.RequestHandler):
    def handle(self):
        """Handles a request from a client"""
        raise NotImplementedError()


def main():
    # create the TCP server, using our request handler
    lib.start_server(HttpRequestHandler)


if __name__ == '__main__':
    exit(main())

