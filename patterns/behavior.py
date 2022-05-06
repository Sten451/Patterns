import json
from datetime import datetime
from light_framework.templator import render

class ConsoleWriter:
    def write(self, text):
        print(text)


class FileWriter:
    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            current_date = str(datetime.now())
            f.write(current_date + ' ' + text + '\n')


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj
        

    def save(self):
        #крякозябры остались
        return json.dumps(self.obj, ensure_ascii=False)

    @staticmethod
    def load(data):
        print("load")
        return json.loads(data)


class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context