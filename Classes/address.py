import db
from Classes.location import Location
from Classes.postal_code import Postal_code


class Address:
    def __init__(self, idAddress):
        if not idAddress:
            get_address = db.get_address_with_idaddress(idAddress=idAddress)
            self.__id = get_address[0]
            self.__location = Location(get_address[1])
            self.__postal_code = Postal_code(get_address[2])
        else:
            pass

    def get_id(self):
        return self.__id

    def get_location(self):
        return self.__location

    def get_postal_code(self):
        return self.__postal_code


    def set_id(self):

    def set_location(self, location):
        self.__location = location

    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code
