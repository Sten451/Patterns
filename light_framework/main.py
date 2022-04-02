import quopri
from tkinter import W
from light_framework.req import GetRequests, PostRequests
from views import NotFound404


class Framework:

    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    # мысли котороые не удалось реализовать
    def content_type(self, path):
        if path.endswith(".css"):
            return "text/css"
        else:
            return "text/html"

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']
        resource = path.split("/")[1]
        headers = []
        headers.append(("Content-Type", self.content_type(resource)))
        #print(headers)
        #resp_file = os.path.join("static", resource)


        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'
            #print(path)

        
        req ={}
        method = environ['REQUEST_METHOD']
        req['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            req['data'] = data
            #печатаем данные из формы
            print(Framework.decode_value(data))
    
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            req['request_params'] = request_params
            print(request_params)


        #  находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = NotFound404()
        request = {}
        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, headers)
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
