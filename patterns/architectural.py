import copy
from create_database import Session
from patterns.creational import Category_product, User, Product_new, Order, Questions_users
from components.hash_password import salted_password


from datetime import datetime

local_session = Session()

class Database():
    #формирования словаря контекста товаров
    def get_quaryset(self, name, category):
        queryset = {}
        for item in local_session.query(name).filter(name.category == category):
            queryset[item.name] = item.price
        return queryset


    #логин
    def login_user(self, login, password):
        if local_session.query(User).filter((User.name==login) & (User.password==salted_password(password))).first():
            if local_session.query(User).filter((User.name==login) & (User.is_admin)).first():
                return True, True
            return True, False
        else:
            return False, False


    #Регистрация
    def registration(self, dict):
        match dict:
            case False if dict['password'] != dict['password2']:
                return False
            case False if local_session.query(User).filter(User.name==dict['login']).first:
                return False
            case _:
                new_user = User(dict['login'], dict['fullname'], dict['email'], salted_password(dict['password']))
                local_session.add(new_user)
                local_session.commit()
                return True
          

    def all_data_api(self):
        dict={}
        temp_list=[]
        for item in local_session.query(Product_new).all():
            dict['name'] = item.name
            dict['price'] = item.price
            dict['category'] = item.category
            temp_list.append(copy.deepcopy(dict))
        return temp_list


    def get_email_user(self, username):
        email = local_session.query(User.email).filter(User.name == username).first()
        return email[0]


    def send_order(self, client, data):
        product = data['order_param']
        id_user = local_session.query(User.id).filter(User.name == client).first()
        order = Order(id_user[0],product[1:-1], created_date=datetime.now())
        local_session.add(order)
        local_session.commit()


    def get_orders(self, client):
        id_user = local_session.query(User.id).filter(User.name == client).first()
        dict={}
        temp_list=[]
        for orders_user in local_session.query(Order).filter(Order.user_id == id_user[0]).all():
            dict['date'] = (orders_user.created_date).strftime('%d-%m-%Y %H:%M')
            dict['number'] = orders_user.number
            dict['status'] = orders_user.status
            temp_list.append(copy.deepcopy(dict))
        return temp_list    
            

    def send_question(self, client, dict):
        print(client, dict)
        id_user = local_session.query(User.id).filter(User.name == client).first()
        question = Questions_users(id_user[0], dict['email'], dict['theme'], dict['message'], created_date=datetime.now())
        local_session.add(question)
        local_session.commit()

    
    def get_user_question(self, client):
        id_user = local_session.query(User.id).filter(User.name == client).first()
        dict={}
        temp_list=[]
        for question_user in local_session.query(Questions_users).filter(Questions_users.user_id == id_user[0]).all():
            dict['date'] = (question_user.created_date).strftime('%d-%m-%Y %H:%M')
            dict['title'] = question_user.title
            dict['status'] = question_user.status
            temp_list.append(copy.deepcopy(dict))
        return temp_list        


    #admin zone
    def get_all_user(self):
        dict={}
        temp_list=[]
        for item in local_session.query(User).all():
            dict['name'] = item.name
            dict['fullname'] = item.fullname
            dict['email'] = item.email
            temp_list.append(copy.deepcopy(dict))
        return temp_list   


    def get_all_order(self):
        dict={}
        temp_list=[]
        for item in local_session.query(Order).all():
            dict['date'] = (item.created_date).strftime('%d-%m-%Y %H:%M')
            dict['number'] = item.number
            dict['status'] = item.status
            temp_list.append(copy.deepcopy(dict))
        return temp_list


    def get_all_question(self):
        dict={}
        temp_list=[]
        for item in local_session.query(Questions_users).all():
            dict['date'] = (item.created_date).strftime('%d-%m-%Y %H:%M')
            dict['title'] = item.title
            dict['status'] = item.status
            dict['id'] = item.id
            dict['question'] = item.question
            temp_list.append(copy.deepcopy(dict))
        return temp_list        


    def change_status_order(self, data):
        data = data.split(',')
        order = local_session.query(Order).filter(Order.number == int(data[0])).first()
        order.status = data[1].strip()
        local_session.commit()

    
    def change_status_question(self, data):
        data = data.split(',')
        question = local_session.query(Questions_users).filter(Questions_users.id == int(data[0])).first()
        question.status = data[1].strip()
        local_session.commit()
        


