"""Provides the Route class stub and the SimpleServer class."""
import json
import re
import http.server
import typing

import thread_runner


class Route:
    """A Route callback."""

    def exec(self):
        """Execute the route."""
        raise NotImplementedError


class _Router:
    def __init__(self, routes: typing.Dict[str, Route]):
        self.routes: typing.Dict[str, typing.Callable] =\
            {k: v.exec for k, v in routes.items()}

    def route(self, route: str) -> typing.Tuple[typing.Dict, int]:
        if route.startswith('/'):
            route = route[1:]

        if route.endswith('/'):
            route = route[:-1]

        for pattern, callback in self.routes.items():
            if re.match(pattern, route) is not None:
                return callback(), 200

        return {'status': 'not found'}, 404


class _SimpleRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        message, code = self.server.router.route(self.path)
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(message).encode('utf-8'))


class _RoutingServer(http.server.ThreadingHTTPServer):
    def __init__(self, server_address, handler, router: _Router):
        self.router = router
        super().__init__(server_address, handler)


class SimpleServer(thread_runner.Runnable):
    """Runnable class of a HTTP server with the specified routes."""

    DAEMON = True

    def __init__(
            self,
            port: int,
            routes: typing.Dict[str, Route]
    ):
        self.port = port
        self.router = _Router(routes)

    def run(self, runner) -> None:
        """Star the HTTP server."""
        server = _RoutingServer(
            ('', self.port),
            _SimpleRequestHandler,
            self.router
        )

        print('HTTP server running on port {}.'.format(self.port))
        server.serve_forever()
