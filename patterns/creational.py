import copy
import ast
from datetime import datetime
import quopri

class User:
    pass

# администратор
class Admin(User):
    pass

# клиент
class Client(User):
    def __init__(self):
        self.active_client = ''
        self.clients = [{"login": "sten", "password": "123"},{"login": "mad", "password": "123"}]
    

    def login_client(self,  list_clients, login, password):
        for client in list_clients:
            if login == client['login'] and password == client['password']:
                return True
        return False    

class Product:
    def __init__(self):
        self.flowers = {'Роза': 100, 'Лилия': 500, 'Тюльпан': 50, 'Хризонтема': 70, 'Составление букета': 500}
        self.airs = {'Плюшевый мишка': 500, 'Набор воздушных шаров': 700, 'Собачка': 300, 'Кошечка': 200}
        self.cakes = {'Раффаэлло': 500, 'Ферреро роше': 700, 'Мерси ассорти': 300, 'Коркунов': 200}


class CartCreational:
    def __init__(self):
        self.cart = []
        self.status = "У Вас нет неотправленных заказов"

    def clone(self, dict):
        new_list = dict['copy_param']
        arr = ast.literal_eval(new_list)
        return copy.deepcopy(arr)

    def append_product(self, old_cart, new_data):
        return old_cart.append(new_data)

    def extend_cart(self, old_cart, new_data):
        return old_cart.extend(new_data)

    def clear_cart(self, data):
        return data.clear()


class Engine:
    def __init__(self):
        pass
        
    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data


# порождающий паттерн Синглтон
class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
        with open('admin/log.txt', 'a', encoding='utf-8') as f:
            current_date = str(datetime.now())
            f.write(current_date + ' ' + text + '\n')
            


