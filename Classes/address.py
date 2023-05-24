import db
from Classes.location import Location
from Classes.postal_code import Postal_code


class Address:
    def __init__(self, idAddress):
        if idAddress is not None:
            get_address = db.get_address_with_idaddress(idAddress=idAddress)
            self.__id = get_address[0]
            self.__street = get_address[1]
            self.__house_number = get_address[2]
            self.__location = Location(get_address[3])
            self.__postal_code = Postal_code(get_address[4])
        else:
            pass

    def get_id(self):
        return self.__id

    def get_street(self):
        return self.__street

    def get_house_number(self):
        return self.__house_number

    def get_location(self):
        return self.__location

    def get_postal_code(self):
        return self.__postal_code

    def set_id(self, id):
        self.__id = id

    def set_street(self, street):
        self.__street = street

    def set_house_number(self, house_number):
        self.__house_number = house_number

    def set_location(self, location):
        self.__location = location

    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code
