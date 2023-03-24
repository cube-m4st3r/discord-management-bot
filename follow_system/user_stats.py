import discord
from discord import app_commands
from discord.ext import commands

import mysql.connector
import os

from itertools import chain

def connect_to_db():

    mydb = mysql.connector.connect(
        host=os.getenv("DB.HOST"),
        user=os.getenv("DB.USER"),
        password=os.getenv("DB.PW"),
        database=os.getenv("DB"),
        port=os.getenv("DB.PORT")
    )

    return mydb

def select_studentid(userid: str):
    connector = connect_to_db()

    selectid = connector.cursor()
    selectid_sql = "SELECT idstudent FROM student WHERE discord_user_iddiscord_user = %s"
    selectid.execute(selectid_sql, (userid,))

    return str(selectid.fetchone()).strip("(,)")

def check_privacy(userid: str):
    connector = connect_to_db()

    studentid = select_studentid(userid)

    cursor = connector.cursor()
    cursor_sql = "SELECT private FROM student_has_lesson WHERE student_idstudent = %s"
    cursor.execute(cursor_sql, (studentid,))

    cursor_output = str(cursor.fetchone()).strip("(,)")

    if cursor_output == "1":
        bool_value = True
    else:
        bool_value = False

    return bool_value

class FollowMenuButton(discord.ui.Button):
    def __init__(self, text, buttonStyle, mode):
        super().__init__(label=text, style=buttonStyle)
        self.mode = mode

    async def callback(self, interaction: discord.Interaction):
        interaction.response.defer()

class FollowMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(FollowMenuButton("Folgen", discord.ButtonStyle.primary, 0))

class setup_user_stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="user_stats", description="Statistiken eines Nutzers anzeigen")
    async def user_stats(self, interaction: discord.Interaction, member: discord.Member=None):

        user_stats_embed = discord.Embed()
        user_stats_embed.color = discord.Color.gold()
        user_stats_embed.set_footer(text=f"requested by: {interaction.user.name}")

        connector = connect_to_db()

        userid = ""

        if member:
            select_student_name = connector.cursor()

            select_student_name_sql = "SELECT first_name, last_name FROM student s \
                                   JOIN discord_user d ON s.discord_user_iddiscord_user = d.iddiscord_user WHERE d.iddiscord_user = %s"
            select_student_name.execute(select_student_name_sql, (str(member.id),))

            select_student_name_result = select_student_name.fetchall()

            student_name = list(chain(*select_student_name_result))

            user_stats_embed.title = str(f"{student_name[0]} {student_name[1]}")

            if check_privacy(str(member.id)) == False:
                print(check_privacy(str(member.id)))
                await interaction.response.send_message(embed=user_stats_embed)
            else:
                await interaction.response.send_message("User profile is set to private!")

        else:
            select_student_name = connector.cursor()

            select_student_name_sql = "SELECT first_name, last_name FROM student s \
                                               JOIN discord_user d ON s.discord_user_iddiscord_user = d.iddiscord_user WHERE d.iddiscord_user = %s"
            select_student_name.execute(select_student_name_sql, (str(interaction.user.id),))

            select_student_name_result = select_student_name.fetchall()

            student_name = list(chain(*select_student_name_result))

            user_stats_embed.title = str(f"{student_name[0]} {student_name[1]}")

            if check_privacy(str(interaction.user.id)) == False:
                await interaction.response.send_message(embed=user_stats_embed)
            else:
                await interaction.response.send_message(embed=user_stats_embed, ephemeral=True)

        #await interaction.response.send_message(view=user_statsView(interaction))

async def setup(bot):
    await bot.add_cog(setup_user_stats(bot))