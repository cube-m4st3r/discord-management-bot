import discord
from discord import app_commands
from discord.ext import commands
from Classes.student import Student


class Test(commands.Cog):

    @app_commands.command(name="test", description="test")
    @app_commands.checks.has_role("MET 11")
    async def insert_grade(self, interaction: discord.Interaction):
        student = Student(3)
        print(student.get_first_name())
        print(student.get_last_name())
        print(student.get_address().get_location_name())


async def setup(bot) -> None:
    await bot.add_cog(Test(bot), guild=discord.Object(id=1076193627778326671))
