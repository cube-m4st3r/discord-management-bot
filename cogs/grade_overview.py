import discord
from discord import app_commands
from discord.ext import commands

import mysql.connector
import os

import re

class RegisterMenuButton(discord.ui.Button):
    def __init__(self, text, buttonStyle, mode):
        super().__init__(label=text, style=buttonStyle)
        self.mode = mode

    async def callback(self, interaction: discord.Interaction):

        if self.mode == 0:
            await interaction.response.send_modal(RegisterUserModal())

        if self.mode == 1:
            await interaction.response.defer()
            await interaction.message.edit(content="Prozess abgebrochen!", delete_after=5)

class RegisterMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RegisterMenuButton("Registriere dich hier!", discord.ButtonStyle.primary, 0))
        self.add_item(RegisterMenuButton("Abbrechen", discord.ButtonStyle.red, 1))

class RegisterUserModal(discord.ui.Modal):

    def __init__(self):
        super().__init__(title="Registrierungsformular")

    first_name = discord.ui.TextInput(label="Vorname", style=discord.TextStyle.short, placeholder="Bitte Vornamen eintragen..", required=True)
    last_name = discord.ui.TextInput(label="Nachname", style=discord.TextStyle.short, placeholder="Bitte Nachnamen eintragen..", required=True)

    async def on_submit(self, interaction: discord.Interaction):

        mydb = mysql.connector.connect(
            host=os.getenv("DB.HOST"),
            user=os.getenv("DB.USER"),
            password=os.getenv("DB.PW"),
            database=os.getenv("DB")
        )

        user_discord_insert = mydb.cursor()

        user_discord_insert_sql = "INSERT INTO discord_user VALUES(%s, %s, %s)"
        user_discord_insert_val = (str(interaction.user.id), interaction.user.name, interaction.user.discriminator)
        user_discord_insert.execute(user_discord_insert_sql, user_discord_insert_val)

        mydb.commit()

        user_student_insert = mydb.cursor()

        user_student_insert_sql = "INSERT INTO student VALUES(NULL, %s, %s, %s)"
        user_student_insert_val = (self.first_name.value, self.last_name.value, str(interaction.user.id))
        user_student_insert.execute(user_student_insert_sql, user_student_insert_val)

        mydb.commit()

        await interaction.response.send_message(f'Du wurdest erfolgreich als: "{self.first_name.value} {self.last_name.value}",  registriert!', ephemeral=True)

class SelectLessonMenu(discord.ui.Select):
    def __init__(self, grade: int):
        super().__init__(placeholder="Wähle ein Lernfeld aus", max_values=1, min_values=1)
        self.grade = grade

        mydb = mysql.connector.connect(
            host=os.getenv("DB.HOST"),
            user=os.getenv("DB.USER"),
            password=os.getenv("DB.PW"),
            database=os.getenv("DB")
        )

        select_teachers = mydb.cursor()

        select_teachers_sql = "SELECT form_of_address, name, lesson_name FROM teacher, lesson WHERE teacher.idteacher = lesson.teacher_idteacher ORDER BY lesson_name"
        select_teachers.execute(select_teachers_sql)

        select_teachers_result = select_teachers.fetchall()

        for a, b, c in select_teachers_result:
            teacher = a + " " + b
            lesson = c
            self.add_option(label=lesson, description=teacher)

    async def callback(self, interaction: discord.Interaction):

        mydb = mysql.connector.connect(
            host=os.getenv("DB.HOST"),
            user=os.getenv("DB.USER"),
            password=os.getenv("DB.PW"),
            database=os.getenv("DB")
        )

        for a in self.values:

            select_lesson_id = mydb.cursor()

            select_lesson_id_sql = "SELECT idlesson FROM lesson WHERE lesson_name = %s"
            select_lesson_id.execute(select_lesson_id_sql, (a,))

            select_lesson_id_result = select_lesson_id.fetchall()

            for b in select_lesson_id_result:

                id_lesson = str(b).strip('(,)')

                select_student_id = mydb.cursor()

                select_student_id_sql = "SELECT idstudent FROM student st JOIN discord_user d ON st.discord_user_iddiscord_user = d.iddiscord_user WHERE d.iddiscord_user = %s"
                select_student_id_val = str(interaction.user.id)
                select_student_id.execute(select_student_id_sql, (select_student_id_val,))

                select_student_id_result = select_student_id.fetchall()

                for c in select_student_id_result:

                    id_student = str(c).strip('(,)')

                    insert_into_shl = mydb.cursor()

                    # shl = student_has_lesson
                    insert_into_shl_sql = "INSERT INTO student_has_lesson VALUES(null, %s, %s, %s)"
                    insert_into_shl_val = (id_student, id_lesson, self.grade)
                    insert_into_shl.execute(insert_into_shl_sql, insert_into_shl_val)

                    mydb.commit()

class SelectLessonView(discord.ui.View):
    def __init__(self, grade: int):
        super().__init__(timeout=None)
        self.add_item(SelectLessonMenu(grade))

class grade_overview(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="note_eintragen", description="Note eintragen")
    @app_commands.checks.has_role("MET 11")
    async def insert_grade(self, interaction: discord.Interaction, note: int):

        if note <= 6:

            mydb = mysql.connector.connect(
                host=os.getenv("DB.HOST"),
                user=os.getenv("DB.USER"),
                password=os.getenv("DB.PW"),
                database=os.getenv("DB")
            )

            mycursor = mydb.cursor()

            sql = "SELECT iddiscord_user FROM discord_user WHERE iddiscord_user = %s"
            val = str(interaction.user.id)

            mycursor.execute(sql, (val,)) # (val,) tuple
            myresult = mycursor.fetchall()
            if not myresult:
                await interaction.response.send_message("Das System konnte dich nicht finden, bist du nicht registriert? \n Wenn du dich registrieren möchtest, dann klicke auf den Button!", view=RegisterMenuView(), ephemeral=True, delete_after=15)
            else:
                await interaction.response.send_message(view=SelectLessonView(note), ephemeral=True)

        else:
            await interaction.response.send_message("Bitte gebe eine richtige Note an.", ephemeral=True, delete_after=3)

    @app_commands.command(name="noten_übersicht", description="Notenübersicht anzeigen")
    @app_commands.checks.has_role("MET 11")
    async def show_grade_overview(self, interaction: discord.Interaction):


        mydb = mysql.connector.connect(
            host=os.getenv("DB.HOST"),
            user=os.getenv("DB.USER"),
            password=os.getenv("DB.PW"),
            database=os.getenv("DB")
        )

        user = interaction.user

        grade_overview_embed = discord.Embed(title="Notenübersicht")
        grade_overview_embed.color = discord.Color.green()
        grade_overview_embed.set_thumbnail(url=user.display_avatar.url)
        grade_overview_embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        grade_overview_embed.set_footer(text=(f"Angefragt von: ", interaction.user.name))

        select_lesson = mydb.cursor()

        select_lesson_sql = "SELECT lesson_name FROM lesson l JOIN student_has_lesson shl ON l.idlesson = shl.lesson_idlesson JOIN student s ON s.idStudent = shl.student_idstudent JOIN discord_user d ON d.iddiscord_user = s.discord_user_iddiscord_user WHERE d.iddiscord_user = %s"
        select_lesson_val = str(interaction.user.id)
        select_lesson.execute(select_lesson_sql, (select_lesson_val,))

        select_lesson_result = select_lesson.fetchall() # returns a list

        lessons = []

        grades = []
        grades_ = ""

        # create a new list and strip the string
        for a in select_lesson_result:
            lesson = str(a).strip("'(,)'")

            if lesson not in lessons:

                lessons.append(lesson)

                select_lesson_id = mydb.cursor()

                select_lesson_id_sql = "SELECT idlesson FROM lesson WHERE lesson_name = %s"
                select_lesson_id.execute(select_lesson_id_sql, (lesson,))

                for aa in select_lesson_id:

                    select_grades = mydb.cursor()

                    select_grades_sql = "SELECT grade FROM lesson l JOIN student_has_lesson shl ON l.idlesson = shl.lesson_idlesson JOIN student s ON s.idStudent = shl.student_idstudent JOIN discord_user d ON d.iddiscord_user = s.discord_user_iddiscord_user WHERE d.iddiscord_user = %s AND l.idlesson = %s"
                    select_grades_val = (str(interaction.user.id), int(str(aa).strip("(,)")))
                    select_grades.execute(select_grades_sql, select_grades_val)

                    for b in select_grades:
                        grade = str(b).strip("['(,)']")

                        grades.append(grade)

                grades_converted = ', '.join(grades)

                res = 0
                for i in grades:
                    res+= int(i)

                avg = str(res/len(grades))

                grade_overview_embed.add_field(
                    name=lesson,
                    value=grades_converted,
                    inline=True
                )
                grade_overview_embed.add_field(
                    name="‎ ",
                    value="Durchschnitt: " + avg[0:4],
                    inline=True
                )
                grade_overview_embed.add_field(
                    name="‎ ",
                    value="‎ ",
                    inline=True
                )
                grades.clear()
        lessons.clear()


        await interaction.response.send_message(embed=grade_overview_embed)

async def setup(bot):
    await bot.add_cog(grade_overview(bot))