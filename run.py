from light_framework.main import Framework
from urls import routes, fronts
from wsgiref.simple_server import make_server
from components import settings

application = Framework(routes, fronts, settings)

with make_server('', 8000, application) as httpd:
    print(f"Запуск на порту 8000...")
    httpd.serve_forever()
