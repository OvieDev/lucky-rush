import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
bot = commands.Bot(command_prefix="rush!")



bot.start(os.getenv("TOKEN"))