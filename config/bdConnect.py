from ..models.models import UserModel
from .bd import conn


class usersFunc:
    def __init__(self):
        self.bd = 'users'

    def send_DB(self, obj: UserModel) -> bool:
        try:
            conn[self.bd].insert_one(obj)
            return True
        except Exception as e:
            print(e)
            return False
