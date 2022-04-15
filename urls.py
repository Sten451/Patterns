from views import Index, Flowers, Cake, Login, Meeting, Air, Contact, Registration, Login, LK, Logout, Cart, Order, CopyCart


# front controller
def secret_front(request):
    request['data'] = "key"


def other_front(request):
    request['key'] = 'key'
 

fronts = [secret_front, other_front]


routes = {
    '/': Index(),
    '/flowers/': Flowers(),
    '/air/': Air(),
    '/cake/': Cake(),
    '/meeting/': Meeting(),
    '/contact/': Contact(),
    '/registration/': Registration(),
    '/login/': Login(),
    '/cabinet/': LK(),
    '/logout/': Logout(),
    '/cart/': Cart(),
    '/order/': Order(),
    '/copy_cart/': CopyCart(),



}
