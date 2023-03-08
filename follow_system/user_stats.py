import discord
from discord import app_commands
from discord.ext import commands

import mysql.connector
import os


class user_statsMenu(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Wähle einen Nutzer aus")

    async def callback(self, interaction: discord.Interaction):

        mydb = mysql.connector.connect(
            host=os.getenv("DB.USER"),
            user=os.getenv("DB.USER"),
            password=os.getenv("DB.PW"),
            database=os.getenv("DB")
        )



class user_statsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(user_statsMenu())

class setup_user_stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="user_stats", description="Statistiken eines Nutzers anzeigen")
    async def user_stats(self, interaction: discord.Interaction):

        await interaction.response.send_message("test")

        #Method 1

        #members = interaction.guild.members

        #for a in members:
        #    print(a)

        #print("-------------")

        #Method 2
        async for member in interaction.guild.fetch_members(limit=3):
            print(member)



async def setup(bot):
    await bot.add_cog(setup_user_stats(bot))