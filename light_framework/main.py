from importlib.resources import path
from os import path
import quopri
from light_framework.req import GetRequests, PostRequests
from views import NotFound404
from components.content_types import CONTENT_TYPES_MAP


class Framework:

    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj, settings):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj
        self.settings = settings

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
                   

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'
            
        req ={}
        method = environ['REQUEST_METHOD']
        req['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            req['data'] = data
            
            
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            req['request_params'] = request_params
        

        # Находим нужный контроллер
        if path in self.routes_lst:
            view = self.routes_lst[path]
            content_type = self.get_content_type(path)
            code, body = view(req)
            body = body.encode('utf-8')

        elif path.startswith(self.settings.STATIC_URL):
            file_path = path[len(self.settings.STATIC_URL):len(path)-1]
            content_type = self.get_content_type(file_path)
            code, body = self.get_static(self.settings.STATIC_FILES_DIR, file_path)

        else:
            view = NotFound404()
            content_type = self.get_content_type(path)
            code, body = view(req)
            body = body.encode('utf-8')
        
        request = {}
        for front in self.fronts_lst:
            front(request)
        start_response(code, [('Content-Type', content_type)])
        return [body]

    @staticmethod
    def get_content_type(file_path, content_types_map=CONTENT_TYPES_MAP):
        file_name = path.basename(file_path).lower()
        extension = path.splitext(file_name)[1]
        return content_types_map.get(extension, "text/html")

    @staticmethod
    def get_static(static_dir, file_path):
        path_to_file = path.join(static_dir, file_path)
        with open(path_to_file, 'rb') as f:
            file_content = f.read()
        status_code = '200 OK'
        return status_code, file_content

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
