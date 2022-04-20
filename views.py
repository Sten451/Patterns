import json
from datetime import datetime
from light_framework.templator import render
from patterns.creational import CartCreational, Engine, Logger, Product, Client
from patterns.struct import AppRoute, Debug

#экземпляры классов
site = Engine()
logger = Logger('main')
mycart = CartCreational()
product = Product()
client_list = Client()

routes = {}

@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', active_user = client_list.active_client)


@AppRoute(routes=routes, url='/flowers/')
class Flowers:
    @Debug(name='Flowers')
    def __call__(self, request):
        return '200 OK', render('flowers.html', flowers = product.flowers, active_user = client_list.active_client)


@AppRoute(routes=routes, url='/air/')
class Air:
    @Debug(name='Airs')
    def __call__(self, request):
        return '200 OK', render('airs.html', airs = product.airs, active_user = client_list.active_client)


@AppRoute(routes=routes, url='/cake/')
class Cake:
    @Debug(name='Cakes')
    def __call__(self, request):
        return '200 OK', render('cakes.html', cakes = product.cakes, active_user = client_list.active_client)


@AppRoute(routes=routes, url='/meeting/')
class Meeting:
    @Debug(name='Meetings')
    def __call__(self, request):
        return '200 OK', render('meeting.html', active_user = client_list.active_client)


@AppRoute(routes=routes, url='/contact/')
class LK:
    @Debug(name='Contact')
    def __call__(self, request):
        return '200 OK', render('lk.html', active_user = client_list.active_client, cart = mycart.cart, status = mycart.status)


@AppRoute(routes=routes, url='/logout/')
class Logout:
    @Debug(name='Logout')
    def __call__(self, request):
        logger.log(f"{client_list.active_client} разлогинился.")
        client_list.active_client = ""
        mycart.status = "У Вас нет неотправленных заказов"
        # Очищаем корзину
        mycart.clear_cart(mycart.cart)
        return '200 OK', render('index.html', active_user = client_list.active_client)


@AppRoute(routes=routes, url='/contact/')
class Contact:
    @Debug(name='Contact')
    def __call__(self, request):
        if request['method'] == 'POST':
            with open('admin/question.txt', 'a', encoding="utf-8") as f:
                dict = site.decode_value(request['data'])
                str_dict = json.dumps(dict, ensure_ascii=False)
                current_date = str(datetime.now())
                f.write(current_date + ' ' + str_dict + '\n')
                logger.log(f"{client_list.active_client} направил сообщение в службу поддержки.")
        return '200 OK', render('contact.html', active_user = client_list.active_client)


@AppRoute(routes=routes, url='/login/')
class Login:
    @Debug(name='Login')
    def __call__(self, request):
        if request['method'] == 'POST':
            # Функция аутентификации передаем список клиентов, логин, пароль    
            if client_list.login_client(client_list.clients, request['data']['login'], request['data']['password']):
                logger.log(f"Пользователь {request['data']['login']} вошел в систему")
                client_list.active_client = request['data']['login']
                return '200 OK', render('index.html', active_user = client_list.active_client)
        return '200 OK', render('login.html')


@AppRoute(routes=routes, url='/registration/')
class Registration:
    @Debug(name='Registration')
    def __call__(self, request):
        if request['method'] == 'POST':
            if request['data']['password'] != request['data']['password2']:
                logger.log(f"Для пользователя {request['data']['login']} Пароли при регистрации не совпали.")
                return '200 OK', render('reg.html')    
            for client in client_list.clients:
                if request['data']['login'] == client['login']:
                    logger.log(f"Пользователь {request['data']['login']} уже зарегистрирован на сайте.")
                    return '200 OK', render('reg.html')
            client_list.clients.append({"login":request['data']['login'], "password":request['data']['password']})    
            logger.log(f"Пользователь {request['data']['login']} успешно зарегистрирован.")
            client_list.active_client = request['data']['login']
            return '200 OK', render('index.html', active_user = client_list.active_client)
        return '200 OK', render('reg.html')


class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 NOT FOUND', render('404.html')


@AppRoute(routes=routes, url='/cart/')
class Cart:
    @Debug(name='Cart')
    def __call__(self, request):
        dict = site.decode_value(request['request_params'])
        # вызывааем функцию добавления товара
        mycart.append_product(mycart.cart, dict)
        logger.log(f"{client_list.active_client} добавил товар {dict} в корзину")
        return '200 OK', render('lk.html', active_user = client_list.active_client, cart = mycart.cart)


@AppRoute(routes=routes, url='/order/')
class Order:
    @Debug(name='Order')
    def __call__(self, request):
        if request['method'] == 'POST':
            with open('admin/order.txt', 'a', encoding="utf-8") as f:
                dict = site.decode_value(request['data'])
                str_dict = json.dumps(dict, ensure_ascii=False)
                current_date = str(datetime.now())
                f.write(current_date + ' ' + str_dict + '\n')
                logger.log(f"{client_list.active_client} отправил заказ на оформление.")
                mycart.clear_cart(mycart.cart)
                mycart.status = "Заказ отправлен на оформление, ожидайте менеджер свяжется с Вами."
        return '200 OK', render('lk.html', active_user = client_list.active_client, cart = mycart.cart, status = mycart.status)


@AppRoute(routes=routes, url='/copy_cart/') 
class CopyCart:
    @Debug(name='CopyCart')
    def __call__(self, request):
        if request['method'] == 'POST':
            dict = site.decode_value(request['data'])
            new_cart = mycart.clone(dict)
            logger.log(f"{client_list.active_client} успешно продублировал заказ.")
            # Вызывем функцию клонирования путём слияния массивов            
            mycart.extend_cart(mycart.cart, new_cart)
        return '200 OK', render('lk.html', active_user = client_list.active_client, cart = mycart.cart, status = mycart.status)
    
