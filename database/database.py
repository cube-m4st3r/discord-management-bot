import mysql.connector
from mysql.connector.cursor import MySQLCursor
from mysql.connector.cursor_cext import CMySQLCursor
import os
from itertools import chain

from classes.user_lesson_rating import User_lesson_grade

cursor: MySQLCursor | CMySQLCursor = NotImplemented
mydb = None

async def init_database():
    global mydb # declare mydb as global
    # Connect to the database
    mydb = mysql.connector.connect(
        host=os.getenv("DB.HOST"),
        user=os.getenv("DB.USER"),
        password=os.getenv("DB.PW"),
        port=os.getenv("DB.PORT"),
        database=os.getenv("DB")
    )

    global cursor
    cursor = mydb.cursor()

    # Check if the connection is stable
    if mydb.is_connected():
        print("Database connection successful")
    else:
        print("Database connection failed")

def get_user_by_ID(userID):
    return userID

def get_grade_list_from_userID(userID):
    sql = "SELECT idlesson, lesson_name, grade FROM lesson l JOIN student_has_lesson shl ON l.idlesson = shl.lesson_idlesson,\
          discord_user d JOIN student s ON d.iddiscord_user = s.discord_user_iddiscord_user WHERE s.idstudent = shl.student_idstudent AND d.iddiscord_user = %s"
    val = userID
    cursor.execute(sql, val)

    result = cursor.fetchall()
    gradesList = []
    for i in result:
        gradesList.append(User_lesson_grade(i[0], i[1], i[2]))

    return gradesList


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

def check_privacy(userid: str):
    studentid = select_student_id(userid)
    sql = "SELECT private FROM student_has_lesson WHERE student_idstudent = %s"
    val = studentid
    cursor.execute(sql, (val,))
    res = str(cursor.fetchone()).strip("(,)")

    if res == "1":
        bool_value = True
    else:
        bool_value = False

    return bool_value
    
    
