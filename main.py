import discord
from discord.ext import tasks, commands
import database
import os
from dotenv import load_dotenv
import asyncio
import logging

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)


async def load_cogs():
    for fileName in os.listdir('./cogs'):
        if fileName.endswith('.py'):
            await client.load_extension(f'cogs.{fileName[:-3]}')

async def load_follow_system():
    for fileName in os.listdir('./cogs/follow_system'):
        if fileName.endswith('.py'):
            await client.load_extension(f'cogs.follow_system.{fileName[:-3]}')

load_dotenv("settings.env")

logging.debug("Now logging...")

async def main():
    await load_cogs()
    await load_follow_system()
    await database.init_database()
    await client.start(os.getenv("TOKEN"))


asyncio.run(main())