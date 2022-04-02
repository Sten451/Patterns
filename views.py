from light_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('data', None))


class Flowers:
    def __call__(self, request):
        return '200 OK', render('flowers.html', flowers=request.get('flowers', None))
        
class Air:
    def __call__(self, request):
        return '200 OK', render('airs.html', airs=request.get('airs', None))

class Cake:
    def __call__(self, request):
        return '200 OK', render('cakes.html', cakes=request.get('cakes', None))

class Meeting:
    def __call__(self, request):
        return '200 OK', render('meeting.html')

class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html')

class NotFound404:
    def __call__(self, request):
        return '404 NOT FOUND', render('404.html')
