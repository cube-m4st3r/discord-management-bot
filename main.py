import platform
import time

import discord
from discord import app_commands
from discord.ext import tasks, commands
from database import database
import os
from dotenv import load_dotenv
import asyncio
import logging
from colorama import Back, Fore, Style
class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents().all())
    async def load_cogs(self):
        for fileName in os.listdir('./cogs'):
            if fileName.endswith('.py'):
                await self.load_extension(f'cogs.{fileName[:-3]}')

    async def load_follow_system(self):
        for fileName in os.listdir('./cogs/follow_system'):
            if fileName.endswith('.py'):
                await self.load_extension(f'cogs.follow_system.{fileName[:-3]}')

    load_dotenv("settings.env")
    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        synced = await self.tree.sync()
        print(prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")
        await database.init_database()

client = Client()
client.run(os.getenv("TOKEN"))