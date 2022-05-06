from light_framework.templator import render
from patterns.creational import CartCreational, Engine, Logger
from patterns.struct import AppRoute, Debug
from patterns.behavior import BaseSerializer, ListView
from patterns.architectural import Database

from create_database import Session
from create_database import Product_new


#экземпляры классов
site = Engine()# good
logger = Logger('main')
mycart = CartCreational()
database = Database()

local_session = Session()

routes = {}

@AppRoute(routes=routes, url='/')
class Index(ListView):
    queryset = ''
    template_name = 'index.html'
      
    def get_context_data(self):
        context = super().get_context_data()
        context['active_user'] = site.active_client
        return context


@AppRoute(routes=routes, url='/flowers/')
class Flowers(ListView):
    queryset = database.get_quaryset(name=Product_new, category='flowers')
    template_name = 'flowers.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['active_user'] = site.active_client
        return context
    

@AppRoute(routes=routes, url='/gifts/')
class Air(ListView):
    queryset = database.get_quaryset(name=Product_new, category='gifts')
    template_name = 'gifts.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['active_user'] = site.active_client
        return context


@AppRoute(routes=routes, url='/cake/')
class Cake(ListView):
    queryset = database.get_quaryset(name=Product_new, category='cakes')
    template_name = 'cakes.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['active_user'] = site.active_client
        return context


@AppRoute(routes=routes, url='/meeting/')
class Meeting(ListView):
    queryset = ''
    template_name = 'meeting.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['active_user'] = site.active_client
        return context


@AppRoute(routes=routes, url='/cabinet/')
class LK(ListView):
    queryset = ''
    template_name = 'lk.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['active_user'] = site.active_client
        context['cart'] = mycart.cart
        context['status'] = mycart.status
        context['admin'] = site.active_admin
        context['all_user'] = database.get_all_user()
        context['all_order'] = database.get_all_order()
        context['all_question'] = database.get_all_question()
        context['orders'] = database.get_orders(site.active_client)
        context['questions'] = database.get_user_question(site.active_client)
        return context


@AppRoute(routes=routes, url='/logout/')
class Logout:
    @Debug(name='Logout')
    def __call__(self, request):
        logger.log(f"{site.active_client} разлогинился.")
        logger.log_in_file(f"{site.active_client} разлогинился.")
        site.active_client = ""
        site.active_admin = False
        mycart.status = "Корзина пуста."
        # Очищаем корзину
        mycart.clear_cart(mycart.cart)
        return '200 OK', render('index.html', active_user = site.active_client)


@AppRoute(routes=routes, url='/contact/')
class Contact:
    @Debug(name='Contact')
    def __call__(self, request):
        if request['method'] == 'POST':
            dict = site.decode_value(request['data'])
            database.send_question(site.active_client, dict)
            logger.log(f"{site.active_client} направил сообщение в службу поддержки.")
            logger.log_in_file(f"{site.active_client} направил сообщение в службу поддержки.")
            return '200 OK', render('lk.html', active_user = site.active_client, cart = mycart.cart, \
            orders = database.get_orders(site.active_client), questions = database.get_user_question(site.active_client))
        return '200 OK', render('contact.html', active_user = site.active_client, email = database.get_email_user(site.active_client))


#ready
@AppRoute(routes=routes, url='/login/')
class Login:
    @Debug(name='Login')
    def __call__(self, request):
        if request['method'] == 'POST':
            verify = database.login_user(request['data']['login'], request['data']['password'])                
            if verify[0]:
                logger.log(f"Пользователь {request['data']['login']} вошел в систему")
                logger.log_in_file(f"Пользователь {request['data']['login']} вошел в систему")
                site.active_client = request['data']['login']
                if verify[1]:
                    site.active_admin = request['data']['login']
                return '200 OK', render('index.html', active_user = site.active_client, admin=site.active_admin)
        return '200 OK', render('login.html')


@AppRoute(routes=routes, url='/registration/')
class Registration:
    @Debug(name='Registration')
    def __call__(self, request):
        if request['method'] == 'POST':
            # надо так сделать иначе проблема с "@"
            verify = database.registration(site.decode_value(request['data']))
            if not verify:
                logger.log(f"Для пользователя {request['data']['login']} Пароли при регистрации не совпали или такой пользователь уже зарегистрирован на сайте.")
                logger.log_in_file(f"Для пользователя {request['data']['login']} Пароли при регистрации не совпали или такой пользователь уже зарегистрирован на сайте.")
                return '200 OK', render('reg.html')
            else:
                logger.log(f"Пользователь {request['data']['login']} успешно зарегистрирован.")
                logger.log_in_file(f"Пользователь {request['data']['login']} успешно зарегистрирован.")
                site.active_client = request['data']['login']
                return '200 OK', render('index.html', active_user = site.active_client)
        return '200 OK', render('reg.html')


class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 NOT FOUND', render('404.html')


@AppRoute(routes=routes, url='/cart/')
class Cart():
    @Debug(name='Cart')
    def __call__(self, request):
        dict = site.decode_value(request['request_params'])
        # вызывааем функцию добавления товара
        mycart.append_product(mycart.cart, dict)
        logger.log(f"{site.active_client} добавил товар {dict} в корзину")
        logger.log_in_file(f"{site.active_client} добавил товар {dict} в корзину")
        return '200 OK', render('lk.html', active_user = site.active_client, cart = mycart.cart, \
            orders = database.get_orders(site.active_client), questions = database.get_user_question(site.active_client))


@AppRoute(routes=routes, url='/order/')
class Order:
    @Debug(name='Order')
    def __call__(self, request):
        if request['method'] == 'POST':
            dict = site.decode_value(request['data'])
            database.send_order(site.active_client, dict)
            logger.log(f"{site.active_client} отправил заказ на оформление.")
            logger.log_in_file(f"{site.active_client} отправил заказ на оформление.")
            mycart.clear_cart(mycart.cart)
            mycart.status = "Заказ отправлен на оформление, ожидайте менеджер свяжется с Вами."
        return '200 OK', render('lk.html', active_user = site.active_client, cart = mycart.cart, status = mycart.status, \
            orders = database.get_orders(site.active_client), questions = database.get_user_question(site.active_client))


@AppRoute(routes=routes, url='/copy_cart/') 
class CopyCart:
    @Debug(name='CopyCart')
    def __call__(self, request):
        if request['method'] == 'POST':
            dict = site.decode_value(request['data'])
            new_cart = mycart.clone(dict)
            logger.log(f"{site.active_client} успешно продублировал заказ.")
            logger.log_in_file(f"{site.active_client} успешно продублировал заказ.")
            mycart.extend_cart(mycart.cart, new_cart)
        return '200 OK', render('lk.html', active_user = site.active_client, cart = mycart.cart, \
            status = mycart.status, orders = database.get_orders(site.active_client), questions = database.get_user_question(site.active_client))
    

@AppRoute(routes=routes, url='/api/')
class ProductApi:
    @Debug(name='ProductApi')
    def __call__(self, request):
        all_category = database.all_data_api()
        return '200 OK', BaseSerializer(all_category).save()


@AppRoute(routes=routes, url='/change_status_order/')
class Change_status_order:
    def __call__(self, request):
        if request['method'] == 'POST':
            dict = site.decode_value(request['data'])
            database.change_status_order(dict['theme'])
            return '200 OK', render('lk.html', active_user = site.active_client, admin=site.active_admin, \
            status = mycart.status, all_order = database.get_all_order(), \
                all_question = database.get_all_question(), all_user = database.get_all_user())


@AppRoute(routes=routes, url='/change_status_question/')
class Change_status_question:
    def __call__(self, request):
        if request['method'] == 'POST':
            dict = site.decode_value(request['data'])
            database.change_status_question(dict['theme'])
            return '200 OK', render('lk.html', active_user = site.active_client, admin=site.active_admin, \
            status = mycart.status, all_order = database.get_all_order(), \
                all_question = database.get_all_question(), all_user = database.get_all_user())