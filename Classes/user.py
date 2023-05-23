import db


class User:
    def __init__(self, idUser):
        load_user = db.get_user_with_idUser(idUser=idUser)
        self.__id = load_user[0]
        self.__name = load_user[1]

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name
