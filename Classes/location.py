import db


class Location:
    def __init__(self, idLocation):
        if idLocation is not None:
            get_location = db.get_location_with_id(idLocation=idLocation)
            self.__id = get_location[0]
            self.__name = get_location[1]
        else:
            pass

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def set_id(self, id):
        self.__id = id
