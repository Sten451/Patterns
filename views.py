import json
from datetime import datetime
import quopri
from threading import active_count
from light_framework.templator import render
from patterns.creational import Engine, Logger


site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', active_user = site.active_user)

class Flowers:
    def __call__(self, request):
        return '200 OK', render('flowers.html', flowers = site.flowers, active_user = site.active_user)
        
class Air:
    def __call__(self, request):
        return '200 OK', render('airs.html', airs = site.airs, active_user = site.active_user)

class Cake:
    def __call__(self, request):
        return '200 OK', render('cakes.html', cakes=site.cakes, active_user = site.active_user)

class Meeting:
    def __call__(self, request):
        return '200 OK', render('meeting.html', active_user = site.active_user)

class LK:
    def __call__(self, request):
        for client in site.clients:
            if client['login'] == site.active_user:
                return '200 OK', render('lk.html', active_user = site.active_user, client=client['order'])


class Logout:
    def __call__(self, request):
        site.active_user = ""
        return '200 OK', render('index.html', active_user = site.active_user)

class Contact:
    def __call__(self, request):
        if request['method'] == 'POST':
            #печатаем данные из формы
            with open('question.txt', 'a', encoding="utf-8") as f:
                # получаем словарь
                dict = Contact.decode_value(request['data'])
                str_dict = json.dumps(dict, ensure_ascii=False)
                current_date = str(datetime.now())
                f.write(current_date + str_dict + '\n')
        return '200 OK', render('contact.html', active_user = site.active_user)
    
    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data


class Login:
    def __call__(self, request):
        if request['method'] == 'POST':
            for client in site.clients:
                if request['data']['login'] == client['login'] and request['data']['password'] == client['password']:
                    logger.log(f"Пользователь {request['data']['login']} вошел в систему")
                    site.active_user = client['login']
                    return '200 OK', render('index.html', active_user = site.active_user)

        return '200 OK', render('login.html')

class Registration:
    def __call__(self, request):
        if request['method'] == 'POST':
            if request['data']['password'] != request['data']['password2']:
                logger.log('Пароли не совпадают.')
                return '200 OK', render('reg.html')    
            for client in site.clients:
                if request['data']['login'] == client['login']:
                    logger.log('Такой Пользователь уже существует')
                    return '200 OK', render('reg.html')
            site.clients.append({"login":request['data']['login'], "password":request['data']['password']})    
            logger.log(f"Пользователь {request['data']['login']} успешно зарегистрирован.")
            site.active_user = request['data']['login']
            return '200 OK', render('index.html', active_user = site.active_user)
         
        return '200 OK', render('reg.html')

class NotFound404:
    def __call__(self, request):
        return '404 NOT FOUND', render('404.html')
