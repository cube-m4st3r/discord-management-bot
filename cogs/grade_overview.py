import discord
from discord import app_commands
from discord.ext import commands

import mysql.connector
import os

import database.database as db


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

    first_name = discord.ui.TextInput(label="Vorname", style=discord.TextStyle.short,
                                      placeholder="Bitte Vornamen eintragen..", required=True)
    last_name = discord.ui.TextInput(label="Nachname", style=discord.TextStyle.short,
                                     placeholder="Bitte Nachnamen eintragen..", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        db.user_student_insert(self.first_name.value, self.last_name.value, interaction.user.id)
        db.discord_user_insert(interaction.user.id, interaction.user.name, interaction.user.discriminator)

        await interaction.response.send_message(
            f'Du wurdest erfolgreich als: "{self.first_name.value} {self.last_name.value}",  registriert!',
            ephemeral=True)

class SelectLessonMenu(discord.ui.Select):
    def __init__(self, grade: int):
        super().__init__(placeholder="Wähle ein Lernfeld aus", max_values=1, min_values=1)
        self.grade = grade

        for form_of_address, name, lesson in db.select_teacher_lesson():
            teacher = form_of_address + " " + name
            lesson = lesson
            self.add_option(label=lesson, description=teacher)

    async def callback(self, interaction: discord.Interaction):

        for a in self.values:
            for b in db.select_lessonid(a):
                id_lesson = str(b).strip('(,)')
                for c in db.select_student_id():
                    id_student = str(c).strip('(,)')
                    db.insert_shl(id_student, id_lesson, self.grade)
                    await interaction.response.send_message(f"Die Note: {str(self.grade)} wurde in {a} eingetragen!", delete_after=5, ephemeral=True)

class SelectTeacherMenu(discord.ui.Select):
    def __init__(self, lesson_name: str):
        super().__init__(placeholder="Wähle einen Lehrer aus.")
        self.lesson_name = lesson_name

        for form_of_address, name in db.list_teachers():
            self.add_option(label=str(f"{form_of_address} {name}"))

    async def callback(self, interaction: discord.Interaction):

        form_of_address, name = self.values[0].split(' ', 1)

        for IDTEACHER in db.select_teacherid(form_of_address, name):

            db.insert_lesson(int(str(IDTEACHER).strip("(,)")), self.lesson_name)
            await interaction.message.edit(content=f"Das Lernfeld: {self.lesson_name} wurde erfolgreich dem Lehrer: {self.values[0]} zugewiesen.", view=None)

class SelectTeacherView(discord.ui.View):
    def __init__(self, lesson_name: str):
        super().__init__(timeout=None)
        self.add_item(SelectTeacherMenu(lesson_name))

class SelectLessonView(discord.ui.View):
    def __init__(self, grade: int):
        super().__init__(timeout=None)
        self.add_item(SelectLessonMenu(grade))

class grade_overview(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="registrieren", description="Registriere dich hiermit!")
    @app_commands.checks.has_role("MET 11")
    async def register_student(self, interaction: discord.Interaction):

        if not db.check_user(interaction.user.id):
            await interaction.response.send_message(content="*Diese Nachricht wird in 15 Sekunden gelöscht*",
                                                    view=RegisterMenuView(), ephemeral=True, delete_after=15)
        else:
            await interaction.response.send_message(content="Du bist bereits registriert!", ephemeral=True, delete_after=5)


    @app_commands.command(name="note_eintragen", description="Note eintragen")
    @app_commands.checks.has_role("MET 11")
    async def insert_grade(self, interaction: discord.Interaction, note: int):

        if note <= 6:
            if not db.check_user(str(interaction.user.id)):
                await interaction.response.send_message(
                    "Das System konnte dich nicht finden, bist du nicht registriert? \n Wenn du dich registrieren möchtest, dann klicke auf den Button!",
                    view=RegisterMenuView(), ephemeral=True, delete_after=15)
            else:
                await interaction.response.send_message(content="Diese Nachricht wird in 15 Sekunden gelöscht!", view=SelectLessonView(note), ephemeral=True, delete_after=15)

        else:
            await interaction.response.send_message("Bitte gebe eine richtige Note an.", ephemeral=True, delete_after=3)

    @app_commands.command(name="noten_übersicht", description="Notenübersicht anzeigen")
    @app_commands.checks.has_role("MET 11")
    async def show_grade_overview(self, interaction: discord.Interaction):
        user = interaction.user

        grade_overview_embed = discord.Embed(title="Notenübersicht")
        grade_overview_embed.color = discord.Color.green()
        grade_overview_embed.set_thumbnail(url=user.display_avatar.url)
        grade_overview_embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        grade_overview_embed.set_footer(text=(f"Angefragt von: " + interaction.user.name))

        select_lesson_result = db.select_lesson(user.id)

        lessons = []

        grades = []

        # create a new list and strip the string
        for a in select_lesson_result:
            lesson = str(a).strip("'(,)'")

            if lesson not in lessons:
                lessons.append(lesson)
                for aa in db.select_lessonid(lesson):
                    for b in db.select_grades(user.id, aa):
                        grade = str(b).strip("['(,)']")

                        grades.append(grade)

                grades_converted = ', '.join(grades)

                res = 0
                for i in grades:
                    res += int(i)

                avg = str(res / len(grades))

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

    @app_commands.command(name="lehrer_eintragen", description="Lehrer eintragen")
    @app_commands.checks.has_role("Leiter")
    async def insert_teacher(self, interaction: discord.Interaction, anrede: str, name: str):

        db.insert_teacher(anrede, name)

        await interaction.response.send_message("Der Lehrer wurde erfolgreich eingetragen!")

    @app_commands.command(name="lernfeld_eintragen", description="Lernfeld eintragen")
    @app_commands.checks.has_role("Leiter")
    async def insert_lesson(self, interaction: discord.Interaction, name: str):

        await interaction.response.send_message(view=SelectTeacherView(name))


async def setup(bot) -> None:
    await bot.add_cog(grade_overview(bot), guild=discord.Object(id=1076193627778326671))
