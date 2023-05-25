import db
from Classes.person import Person


class Student(Person):
    def __init__(self, idStudent):
        super().__init__(db.get_idperson_with_idstudent(idStudent=idStudent))

