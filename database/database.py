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
    cursor = mydb.cursor(buffered=True)

    if mydb.is_connected():
        return True
    else:
        return False


def select_student_id(userid: str):
    sql = "SELECT idstudent FROM student st JOIN discord_user d ON st.discord_user_iddiscord_user = d.iddiscord_user WHERE d.iddiscord_user = %s"
    val = (userid,)
    cursor.execute(sql, val)
    return cursor.fetchone()


def select_student_name(memberid: str):
    sql = "SELECT first_name, last_name FROM student s \
                                   JOIN discord_user d ON s.discord_user_iddiscord_user = d.iddiscord_user WHERE d.iddiscord_user = %s"
    val = (memberid,)
    cursor.execute(sql, val)
    res = cursor.fetchall()
    name = list(chain(*res))
    return name


def discord_user_insert(userid, username, userdiscriminator):
    sql = "INSERT INTO discord_user VALUES(%s, %s, %s)"
    val = userid, username, userdiscriminator
    cursor.execute(sql, val)
    mydb.commit()


def check_user(userid):
    sql = "SELECT iddiscord_user FROM discord_user WHERE iddiscord_user = %s"
    val = (userid,)
    cursor.execute(sql, val)


def user_student_insert(firstname, lastname, userid):
    sql = "INSERT INTO student VALUES(NULL, %s, %s, %s)"
    val = userid, firstname, lastname
    cursor.execute(sql, val)

    mydb.commit()


def select_teacherid(form_of_address, name):
    sql = "SELECT idteacher FROM teacher WHERE form_of_address = %s AND name = %s"
    val = form_of_address, name
    cursor.execute(sql, val)
    return cursor.fetchall()


def list_teachers():
    sql = "SELECT form_of_address, name FROM teacher"
    cursor.execute(sql)

    list_teachers = cursor.fetchall()

    return list_teachers


def insert_teacher(form_of_address, name):
    sql = "INSERT INTO teacher VALUES(null, %s, %s)"
    val = form_of_address, name
    cursor.execute(sql, val)
    mydb.commit()


def select_lessonid(input):
    sql = "SELECT idlesson FROM lesson WHERE lesson_name = %s"
    cursor.execute(sql, input)
    return cursor.fetchall()


def select_lesson(userid):
    sql = "SELECT lesson_name FROM lesson l JOIN student_has_lesson shl ON l.idlesson = shl.lesson_idlesson JOIN \
            student s ON s.idStudent = shl.student_idstudent JOIN discord_user d ON d.iddiscord_user = s.discord_user_iddiscord_user WHERE d.iddiscord_user = %s"
    val = userid
    cursor.execute(sql, (val,))
    return cursor.fetchall()


def insert_lesson(teacherid, name):
    sql = "INSERT INTO lesson VALUES(null, %s, %s)"
    val = name, teacherid
    cursor.execute(sql, val)

    mydb.commit()


def select_teacher_lesson():
    sql = "SELECT form_of_address, name, lesson_name FROM teacher, lesson WHERE teacher.idteacher = lesson.teacher_idteacher ORDER BY lesson_name"
    cursor.execute(sql)
    return cursor.fetchall()


def insert_shl(studentid, lessonid, grade):
    sql = "INSERT INTO student_has_lesson VALUES(null, %s, %s, %s, 1)"
    val = studentid, lessonid, grade
    cursor.execute(sql, val)

    mydb.commit()


def select_grades(userid, lessonid):
    sql = "SELECT grade FROM lesson l JOIN student_has_lesson shl ON l.idlesson = shl.lesson_idlesson JOIN student \
            s ON s.idStudent = shl.student_idstudent JOIN discord_user d ON d.iddiscord_user = s.discord_user_iddiscord_user WHERE d.iddiscord_user = %s AND l.idlesson = %s"
    val = userid, lessonid
    cursor.execute(sql, val)
