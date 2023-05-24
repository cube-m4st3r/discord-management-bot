import db


class Postal_code:
    def __init__(self, idPostal_code):
        if idPostal_code is not None:
            get_postal_code = db.get_postal_code_with_id(idPostal_code=idPostal_code)
            self.__id = get_postal_code[0]
            self.__code = get_postal_code[1]
        else:
            pass

    def get_id(self):
        return self.__id

    def get_code(self):
        return self.__code

    def set_id(self, id):
        self.__id = id
