import discord
from discord import app_commands
from discord.ext import commands

import mysql.connector
import os

class Messages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="delete_messages", description="Delete Messages")
    @app_commands.checks.has_role("Leiter")
    async def deletemessages(self, interaction: discord.Interaction, number: int, member: discord.Member=None):
        delete_counter = 0
        await interaction.response.send_message(str("Wird gemacht!"), delete_after=3, ephemeral=True)
        async for message in interaction.channel.history():
            if message.author == member or member == None:
                await message.delete()
                delete_counter += 1
            if delete_counter == number:
                break

async def setup(bot):
    await bot.add_cog(Messages(bot))