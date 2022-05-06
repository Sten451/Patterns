"""
Данный файл необходим только для первоначального наполнения БД
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from components.source_data import product, users, categories, DATABASE_NAME
from patterns.creational import Product_new, Category_product, User, Order, Questions_users, Base

engine = create_engine(f'sqlite:///{DATABASE_NAME}', future=True)
Session = sessionmaker(bind=engine, future=True)


def create_db():
    Base.metadata.create_all(engine)
    init_database()

def init_database():
    local_session = Session()

    #user
    for item in users:
        new_item = User(item['username'], item['second_name'], item['email'], item['password'], item['is_admin'])
        local_session.add(new_item)

    #categories
    for item in categories:
        new_item = Category_product(item['name'])
        local_session.add(new_item)

    #product
    for item in product:
        new_item = Product_new(item['name'], item['price'], item['category'])
        local_session.add(new_item)

    local_session.commit()
    local_session.close()    


def first_create():    
    #Проверяем при запуске на наличие базы данных, если нет, то создаём
    path = os.path.join(os.getcwd(), DATABASE_NAME)

    if os.path.exists(path):
        print("Найдена база данных. Создание не требуется.")
    else:
        print("База данных не найдена. Создаём.")
        create_db()# Создаём базу данных
        print("База данных успешно создана и наполнена.")


if __name__ == "__main__":
	first_create()