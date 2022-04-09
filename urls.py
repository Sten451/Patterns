from datetime import date
from views import Index, Flowers, Cake, Meeting, Air, Contact 


# front controller
def secret_front(request):
    request['data'] = date.today()


def other_front(request):
    request['key'] = 'key'
    request['flowers'] = {'Роза': 100, 'Лилия': 500, 'Тюльпан': 50, 'Хризонтема': 70, 'Составление букета': 500}
    request['cakes'] = {'Раффаэлло': 500, 'Ферреро роше': 700, 'Мерси ассорти': 300, 'Коркунов': 200}
    request['airs'] = {'Плюшевый мишка': 500, 'Набор воздушных шаров': 700, 'Собачка': 300, 'Кошечка': 200}


fronts = [secret_front, other_front]


routes = {
    '/': Index(),
    '/flowers/': Flowers(),
    '/air/': Air(),
    '/cake/': Cake(),
    '/meeting/': Meeting(),
    '/contact/': Contact(),

}
