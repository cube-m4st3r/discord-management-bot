import json

import mysql.connector

import config
import db
from Classes.address import Address
from Classes.location import Location
from Classes.person import Person
from Classes.postal_code import Postal_code
from Classes.user import User


async def init_database():
    global mydb
    mydb = mysql.connector.connect(
        host=config.botConfig["host"],
        user=config.botConfig["user"],
        password=config.botConfig["password"],
        port=config.botConfig["port"],
        database=config.botConfig["database"]
    )

    global cursor
    cursor = mydb.cursor(buffered=True)

    if mydb.is_connected():
        print("Database connection successful")
    else:
        print("Database connection failed")


def validate_user(idUser):
    if not does_user_exist(idUser=idUser):
        return False

    return True


def does_user_exist(idUser):
    sql = f"SELECT * FROM user u WHERE u.idUser = {idUser}"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return True
    else:
        return False


def get_person_with_idperson(idPerson):
    sql = f"SELECT idPerson, first_name, last_name, email FROM person WHERE idPerson={idPerson}"
    cursor.execute(sql)
    return cursor.fetchone()


def get_idperson_with_idstudent(idStudent):
    sql = f"SELECT p.idPerson FROM person p JOIN student s ON p.idPerson=s.idPerson AND s.idStudent={idStudent}"
    cursor.execute(sql)
    return cursor.fetchone()[0]


def load_teacher_as_person(idTeacher):
    sql = f"SELECT p.idPerson FROM person p JOIN teacher t ON p.idPerson=t.idPerson AND t.idTeacher={idTeacher}"
    cursor.execute(sql)
    res = cursor.fetchone()[0]

    if res:
        return


def load_address_of_person(idPerson):
    idAddress = get_idaddress_with_idperson(idPerson)
    if idAddress:
        sql = f"SELECT a.idAddress FROM address a JOIN person p ON a.idAddress = p.idAddress AND a.idAddress={idAddress} AND p.idPerson={idPerson}"
        cursor.execute(sql)
        res = cursor.fetchone()

        if res:
            return Address(res[0])
    else:
        return None


def get_address_with_idaddress(idAddress):
    sql = f"SELECT idAddress, street, house_number, idlocation, idpostal_code from address where idAddress={idAddress}"
    cursor.execute(sql)
    return cursor.fetchone()


def get_idaddress_with_idperson(idPerson):
    sql = f"SELECT idAddress FROM person WHERE idPerson={idPerson}"
    cursor.execute(sql)
    return cursor.fetchone()[0]


# check if address exists
def check_address_exists(address):
    # check location & postal_code if exists
    # check if the address exists already -> if not, create it within DB
    # if yes, then set the data for the object and return it
    # anything below is useless, select_missing_id is strong.
    if __check_if_exists(table="address", column="idAddress", value=address.get_id()):
        address.set_street(__select_data(table="address", column_data="street", column_condition="idAddress",
                                         condition=address.get_id()))
        address.set_house_number(
            __select_data(table="address", column_data="house_number", column_condition="idAddress",
                          condition=address.get_id()))
        address.set_location(Location(
            __select_data(table="address", column_data="idLocation", column_condition="idAddress",
                          condition=address.get_id())))
        address.set_postal_code(Postal_code(
            __select_data(table="address", column_data="idPostal_code", column_condition="idAddress",
                          condition=address.get_id())))
        return address
    else:
        address.set_id(__select_missing_id("address", "idAddress"))
        return address


def __check_if_exists(table, column, value):
    sql = f"SELECT * FROM {table} WHERE {column}={value}"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return True
    else:
        return False


def __select_missing_id(table, id_value):
    sql = f"SELECT t1.{id_value} + 1 AS missing_id FROM {table} t1 WHERE NOT EXISTS (SELECT * FROM {table} t2 WHERE t2.{id_value} = t1.{id_value} + 1) LIMIT 1"
    cursor.execute(sql)
    return cursor.fetchone()[0]


def get_location_with_id(idLocation):
    sql = f"SELECT idLocation, name FROM location WHERE idLocation={idLocation}"
    cursor.execute(sql)
    return cursor.fetchone()


def get_postal_code_with_id(idPostal_code):
    sql = f"SELECT idPostal_code, code FROM postal_code WHERE idPostal_code={idPostal_code}"
    cursor.execute(sql)
    return cursor.fetchone()


def __select_data(table, column_data, column_condition, condition):
    sql = f"SELECT {column_data} FROM {table} WHERE {column_condition}={condition}"
    cursor.execute(sql)
    res = cursor.fetchone()

    if res:
        return res[0]


def __insert_new_data(table, values, return_last_row_id=False):
    insertion_data = str()
    for i, value in enumerate(values, start=1):
        if len(values) == i:
            insertion_data += f"{value}"
        else:
            insertion_data += f"{value}, "

    sql = f"INSERT INTO {table} VALUE({insertion_data})"
    cursor.execute(sql)
    mydb.commit()

    if return_last_row_id:
        return cursor.lastrowid


def load_user(idStudent):
    sql = f"SELECT u.idUser, name FROM user u JOIN student s ON u.idUser = s.idUser WHERE s.idStudent={idStudent}"
    cursor.execute(sql)
    res = cursor.fetchone()

    if res:
        return User(res[0])


def get_user_with_id(idUser):
    sql = f"SELECT idUser, name FROM user WHERE idUser={idUser}"
    cursor.execute(sql)
    return cursor.fetchone()
