import os.path
from light_framework.main import Framework
from urls import fronts
from views import routes
from wsgiref.simple_server import make_server
from components import settings


# class FrameworkDebug(Framework):
#     def __init__(self, routes, fronts):
#         super().__init__(routes, fronts)
#         self.application = Framework(routes, fronts)
#
#     def __call__(self, environ, start_response):
#         print('Framework - Debug: ', environ)
#         return self.application(environ, start_response)


class FakeApp:
    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake!']


application = Framework(routes, fronts, settings)
# app = FrameworkDebug(routes, fronts)
# app = FakeApp()

with make_server('', 8000, application) as httpd:
    print(f"Запуск на порту 8000...")
    httpd.serve_forever()

"""with make_server('', 9000, app) as httpd:
    print(f"Запуск на порту 9000...")
    httpd.serve_forever()"""