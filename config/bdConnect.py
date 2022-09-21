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
            print(e, 'Send User Error')
            return False

    def read_User(self, obj: str) -> UserModel:
        try:
            ver = conn[self.bd].find_one({'_id': obj})
            return ver
        except Exception as e:
            print(e, 'Read User Error')
            return None

    def update_User(self, id: str, obj: dict) -> bool:
        try:
            conn[self.bd].update_one({'_id': id}, {'$set': obj})
            return True
        except Exception as e:
            print(e, 'Update User Error')
            return False

    def delete_User(self, id: str) -> bool:
        try:
            conn[self.bd].delete_one({'_id': id})
            return True
        except Exception as e:
            print(e, 'Delete User Error')
            return False
