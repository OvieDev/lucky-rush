import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
bot = commands.Bot(command_prefix="rush!")


@bot.command()
async def rules(ctx):
    embed = discord.Embed(title="Rules", description="""
    **GOAL:** Be the first person on the finish line
    
    -----------
    
    The game is divided on rounds. In each round you must pick, if
    you want to **CHECK** the luckybox or **PASS** it. 
    Each luckybox contains many fortunate (and unfortunate) stuff that can help you win (or lose) the game.
    In rounds 5 and 10, you have to check the box sadly.
    The game is played with 3 other players
    """, colour=discord.Colour.blue())

    embed.set_footer(text=f"Sent in {int(round(bot.latency, 3)*1000)}ms")
    await ctx.send(embed=embed)


bot.run(os.getenv("TOKEN"))
