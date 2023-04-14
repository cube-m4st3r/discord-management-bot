import platform
import random
import time

import discord
from discord.ext import tasks, commands
from database import database
import os
from dotenv import load_dotenv
from colorama import Back, Fore, Style

load_dotenv("settings.env")

my_guild = discord.Object(id=os.getenv("GUILD-ID"))


@tasks.loop(minutes=5.0)
async def update_presence(self):
    presence_game_list = ['with Documents', 'with Papers', 'with Books']

    random_presence = random.choice(presence_game_list)
    await self.change_presence(status=discord.Status.dnd, activity=discord.Game(name=random_presence))


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents().all())

    async def setup_hook(self):
        for fileName in os.listdir('./cogs'):
            if fileName.endswith('.py'):
                await self.load_extension(f'cogs.{fileName[:-3]}')

        await self.tree.sync(guild=my_guild)

    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(f"{prfx} Logged in as {Fore.YELLOW + self.user.name}")
        print(f"{prfx} Bot ID: {Fore.YELLOW + str(self.user.id)}")
        print(f"{prfx} Discord Version: {Fore.YELLOW + discord.__version__}")
        print(f"{prfx} Python Version: {Fore.YELLOW + str(platform.python_version())}")
        self.tree.copy_global_to(guild=discord.Object(id=1076193627778326671))
        print(f"{prfx} Slash CMDs Synced: {Fore.YELLOW + str(len(await self.tree.fetch_commands(guild=my_guild)))} Commands")
        print(f"{prfx} Connected to: {Fore.YELLOW + str(len(self.guilds))} Guilds")
        if await database.init_database():
            print(f"{prfx} Database Connection:{Fore.YELLOW} successful.")
        await update_presence.start(self)


if __name__ == '__main__':
    client = Client()
    client.run(os.getenv("TOKEN"))