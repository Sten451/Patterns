import copy
import ast
import quopri
from datetime import datetime
import random
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
from patterns.behavior import ConsoleWriter, FileWriter
from components.source_data import name_logfile

Base = declarative_base()

#класс Юзер
class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key = True)
    name = Column(String(20))
    fullname = Column(String(20))
    email = Column(String(20))
    password = Column(String())
    is_admin = Column(Boolean)


    def __init__(self, name, fullname, email, password, is_admin=False):
        self.name = name
        self.fullname = fullname
        self.email = email
        self.password = password
        self.is_admin = is_admin
        

    def __repr__(self):
        return f"<User {self.name}>"
        

#Класс категория продуктов
class Category_product(Base):
    __tablename__ = 'Category'

    id = Column(Integer, primary_key = True)
    category_name = Column(String(20))
        
    def __init__(self, category_name):
        self.category_name = category_name


#Класс продукты
class Product_new(Base):
    __tablename__ = 'Product'

    id = Column(Integer, primary_key = True)
    name = Column(String())
    price = Column(BigInteger())
    category = Column(Integer, ForeignKey('Category.id'))
    
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category



class CartCreational:
    def __init__(self):
        self.cart = []
        self.status = "Корзина пуста."

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


class Order(Base):
    __tablename__ = 'Order'
    id = Column(Integer, primary_key = True)
    number = Column(Integer())
    created_date = Column(DateTime)
    status = Column(String())
    cart = Column(String())
    user_id = Column(Integer, ForeignKey('Users.id'))
    
    def __init__(self, user_id, cart, created_date, status='В обработке'):
        self.number = random.randint(1, 5000)
        self.status = status
        self.user_id = user_id
        self.cart = cart
        self.created_date = created_date


class Questions_users(Base):
    __tablename__ = 'Questions'
    id = Column(Integer, primary_key = True)
    created_date = Column(DateTime)
    title = Column(String())
    question = Column(String())
    email = Column(String(20))
    status = Column(String())
    user_id = Column(Integer, ForeignKey('Users.id'))


    def __init__(self, user_id, email, title, question, created_date, status='Отправлено'):
        self.title = title
        self.status = status
        self.user_id = user_id
        self.email = email
        self.question = question
        self.created_date = created_date


class Engine:
    def __init__(self):
        self.active_client = ''
        self.active_admin = False 
    
    
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
    def __init__(self, name, writer=ConsoleWriter(), savelog = FileWriter(name_logfile)):
        self.name = name
        self.writer = writer
        self.savelog = savelog

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)
    
    def log_in_file(self, text):
        self.savelog.write(text)
