
class User:
    pass

# администратор
class Admin(User):
    pass

# клиент
class Client(User):
    pass


class Engine:
    def __init__(self):
        #self.teachers = []
        self.clients = [{"login": "sten", "password": "123"},{"login": "mad", "password": "123"}]
        self.active_user = ''
        #self.courses = []
        #self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)



class UserFactory:
    types = {
        'administrator': Admin,
        'client': Client
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()




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