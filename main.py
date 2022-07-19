import os

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="rush!")

bot.start(os.getenv("TOKEN"))