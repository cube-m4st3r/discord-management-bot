import mysql.connector
from mysql.connector.cursor import MySQLCursor
from mysql.connector.cursor_cext import CMySQLCursor
import os
from itertools import chain

from classes.user_lesson_rating import User_lesson_grade

cursor: MySQLCursor | CMySQLCursor = NotImplemented
mydb = None


async def init_database():
    global mydb
    mydb = mysql.connector.connect(
        host=os.getenv("DB.HOST"),
        user=os.getenv("DB.USER"),
        password=os.getenv("DB.PW"),
        port=os.getenv("DB.PORT"),
        database=os.getenv("DB")
    )

    global cursor
    cursor = mydb.cursor()

    if mydb.is_connected():
        return True
    else:
        return False


def get_grade_list_from_userid(userid):
    sql = "SELECT idlesson, lesson_name, grade FROM lesson l JOIN student_has_lesson shl ON l.idlesson = shl.lesson_idlesson,\
          discord_user d JOIN student s ON d.iddiscord_user = s.discord_user_iddiscord_user WHERE s.idstudent = shl.student_idstudent AND d.iddiscord_user = %s"
    val = userid
    cursor.execute(sql, val)

    result = cursor.fetchall()
    gradeslist = []
    for i in result:
        gradeslist.append(User_lesson_grade(i[0], i[1], i[2]))

    return gradeslist


def select_student_id(userid: str):
    sql = "SELECT idstudent FROM student WHERE discord_user_iddiscord_user = %s"
    val = (userid,)
    cursor.execute(sql, val)
    return str(cursor.fetchone()).strip("(,)")


def select_student_name(memberid: str):
    sql = "SELECT first_name, last_name FROM student s \
                                   JOIN discord_user d ON s.discord_user_iddiscord_user = d.iddiscord_user WHERE d.iddiscord_user = %s"
    val = (memberid,)
    cursor.execute(sql, val)
    res = cursor.fetchall()
    name = list(chain(*res))
    return name

def list_teachers():
    sql = "SELECT form_of_address, name FROM teacher"
    cursor.execute(sql)

    list_teachers = cursor.fetchall()

    return list_teachers


def discord_user_insert(userid, username, userdiscriminator):
    sql = "INSERT INTO discord_user VALUES(%s, %s, %s)"
    val = userid, username, userdiscriminator
    cursor.execute(sql, val)

    mydb.commit()


def user_student_insert(firstname, lastname, userid):
    sql = "INSERT INTO student VALUES(NULL, %s, %s, %s)"
    val = firstname, lastname, userid
    cursor.execute()

    mydb.commit()