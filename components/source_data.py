"""
Переменные
"""

DATABASE_NAME = 'wsgi.sqlite'
name_logfile = 'admin/log.txt'
salt = 'cfa2ab788a8d0a88e444d40ab4f5b3dfc65b13530046eea77c96cad8622e7c16'

# product
product = [
    {
        'name': 'Роза', 'price': 100, 'category': 'flowers'
    },
    {
        'name': 'Лилия', 'price': 500, 'category': 'flowers'
    },
    {
        'name': 'Тюльпан', 'price': 50, 'category': 'flowers'
    },
    {
        'name': 'Хризонтема', 'price': 70, 'category': 'flowers'
    },
    {
        'name': 'Плюшевый мишка', 'price': 500, 'category': 'gifts'
    },
    {
        'name': 'Набор воздушных шаров', 'price': 700, 'category': 'gifts'
    },
    {
        'name': 'Собачка', 'price': 300, 'category': 'gifts'
    },
    {
        'name': 'Кошечка', 'price': 200, 'category': 'gifts'
    },
    {
        'name': 'Раффаэлло', 'price': 500, 'category': 'cakes'
    },
    {
        'name': 'Ферреро роше', 'price': 700, 'category': 'cakes'
    },
    {
        'name': 'Мерси ассорти', 'price': 300, 'category': 'cakes'
    },
    {
        'name': 'Коркунов', 'price': 200, 'category': 'cakes'
    }
]

# categories
categories = [
    {
        'name': 'flowers'
    },
    {
        'name': 'gifts'
    },
    {
        'name': 'cakes'
    }
]

# users
users = [
    {
        'username': 'sten', 'second_name': 'lucky', 'password': '9fe52acf9f8e6e244fed54313a9d0dbce8197c058267875e80929c2004403811', 'email': 'r@123.ru', 'is_admin': True
    },
    {
        'username': 'mad', 'second_name': 'watslav', 'password': '9fe52acf9f8e6e244fed54313a9d0dbce8197c058267875e80929c2004403811', 'email': 't@345.ru', 'is_admin': False
    }
]

