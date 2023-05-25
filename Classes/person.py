import db


class Person:
    def __init__(self, idPerson):
        get_person = db.get_person_with_idperson(idPerson=idPerson)
        load_address = db.load_address_of_person(idPerson=idPerson)

        self.__idPerson = get_person[0]
        self.__first_name = get_person[1]
        self.__last_name = get_person[2]
        self.__address = load_address
        self.__email = get_person[3]

    def get_idperson(self):
        return self.__idPerson

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_address(self):
        return self.__address

    def get_email(self):
        return self.__email

