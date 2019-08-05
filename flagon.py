from webob import Request, Response
from parse import parse
import inspect
from webtest import TestApp


class FlagonTestClient(TestApp):

    def do_request(self, req, status=None, expect_errors=None):
        return super(FlagonTestClient, self).do_request(req, status, expect_errors=True)


class Flagon:

    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):

        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request.path)

        if handler is not None:
            self.get_handler_function(request, handler)(
                request, response, **kwargs)
            return response

        return self.default_response(response)

    def get_handler_function(self, request, handler):
        if inspect.isclass(handler):
            handler = getattr(handler(), request.method.lower(), None)

        if handler is None:
            raise AttributeError("Method not allowed.", request.method)

        return handler

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parsed_result = parse(path, request_path)
            if parsed_result is not None:
                return handler, parsed_result.named

        return None, None

    def route(self, path):
        assert path not in self.routes, f"A rota {path} já foi registrada"

        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found."

        return response

    def test_client(self):
        return FlagonTestClient(self)
