from light_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html')

class Flowers:
    def __call__(self, request):
        return '200 OK', render('flowers.html', flowers={'Роза': 100, 'Лилия': 500, 'Тюльпан': 50, 'Хризонтема': 70, 'Составление букета': 500})
        
class Air:
    def __call__(self, request):
        return '200 OK', render('airs.html', airs={'Плюшевый мишка': 500, 'Набор воздушных шаров': 700, 'Собачка': 300, 'Кошечка': 200})

class Cake:
    def __call__(self, request):
        return '200 OK', render('cakes.html', cakes={'Раффаэлло': 500, 'Ферреро роше': 700, 'Мерси ассорти': 300, 'Коркунов': 200})

class Meeting:
    def __call__(self, request):
        return '200 OK', render('meeting.html')

class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html')

class NotFound404:
    def __call__(self, request):
        return '404 NOT FOUND', render('404.html')
