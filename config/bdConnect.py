from models.models import UserModel
from .bd import conn


class usersFunc:
    def __init__(self):
        self.bd = 'users'

    def send_User(self, obj: UserModel) -> bool:
        dicti = obj.dict()
        try:
            dicti['_id'] = dicti['id']
            dicti.pop('id')
            conn[self.bd].insert_one(dicti)
            return True
        except Exception as e:
            print(e)
            return False

    def read_User(self, obj: str) -> UserModel:
        try:
            return conn[self.bd].find_one({'_id': obj})
        except Exception as e:
            print(e)
            return 'hola'

    def update_User(self, obj: str) -> bool:
        try:
            conn[self.bd].update_one({'_id': str}, {'$set': obj})
            return True
        except Exception as e:
            print(e)
            return False
