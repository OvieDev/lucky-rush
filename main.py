import asyncio
import os
import random
import string
from threading import Thread

import discord
from dotenv import load_dotenv
from discord.ext import commands

from components.GameSession import GameSession, sessions, sessiontime_decrease
from views.gameplay_view import GameplayView
from views.help_view import HelpView
from views.join_view import JoinView

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="rush!", intents=intents, help_command=None)

@bot.event
async def on_timeout(message: discord.Message, game):
    await message.edit(embed=game.create_message(), view=GameplayView(game))

@bot.event
async def on_session_terminated(u, k, c):
    user = await bot.fetch_user(u)
    await c.delete()
    del sessions[k]
    print(user)
    await user.send("Your session was terminated because no one joined")


@bot.event
async def on_guild_join(guild: discord.Guild):
    channel = guild.text_channels[0]
    embed = discord.Embed(title="Hi! :wave:",
                          description="""Thanks for adding me!
                                    I'm just your friendly discord bot that let's you play this game called **LUCKY RUSH**
                                    Although that's my main purpose, I have __**MUCH MORE**__ to offer. So type `rush!help` to see all commands
                                    """)
    await channel.send(embed=embed)


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.event
async def on_ready():
    await bot.tree.sync()
    for i in bot.guilds:
        for y in i.text_channels:
            if "luckyrush" in y.name:
                await y.delete()


@bot.hybrid_command(description="Display rules for Lucky Rush")
async def rules(ctx):
    print("xxx")
    embed = discord.Embed(title="Rules", description="""
    **GOAL:** Be the first person on the finish line

    -----------

    The game is divided on rounds. In each round you must pick, if
    you want to **CHECK** the luckybox or **PASS** it.
    Each luckybox contains many fortunate (and unfortunate) stuff that can help you win (or lose) the game.
    In rounds 5 and 10, you have to check the box sadly.
    The game is played with 3 other players
    """, colour=discord.Colour.blue())

    embed.set_footer(text=f"Sent in {int(round(bot.latency, 3) * 1000)}ms")
    await ctx.send(embed=embed)


@bot.hybrid_command(name="help", description="View all possible commands")
async def helpme(ctx: discord.TextChannel):
    embed = discord.Embed(title=f"Help - Page 1")
    embed.add_field(name="help", value="Shows all of commands", inline=False)
    embed.add_field(name="rules", value="Shows rules of the Lucky Rush", inline=False)
    embed.add_field(name="start", value="Starts a new game", inline=False)
    embed.add_field(name="join", value="Join a game via code", inline=False)
    embed.add_field(name="gameopt", value="Set options of the game", inline=False)
    embed.set_footer(text="Prefix: rush!")

    await ctx.send(embed=embed, view=HelpView())


@bot.hybrid_command(description="Get an invite link (if you couldn't just go to my profile lol)")
async def invite(ctx):
    await ctx.send("Here's my invite link: <https://tinyurl.com/rushinvite>")


@bot.hybrid_command(description="Get a link to my github (if you couldn't open my about me section lol)")
async def github(ctx):
    await ctx.send("Want to contribute? Sure, here's my github: <https://tinyurl.com/luckyrush>")


@bot.hybrid_command(description="Start a new lobby for Lucky Rush")
async def lobby(ctx):
    code = ''.join(random.choices(string.ascii_lowercase, k=10))
    while True:
        if code in sessions:
            code = ''.join(random.choices(string.ascii_lowercase, k=10))
        else:
            break

    embed = discord.Embed(title="Waiting for players...", description=f"""
    Invite some friends with this code: {code}
    """)
    embed.colour = discord.Colour.gold()

    guild: discord.Guild = ctx.guild
    c = await guild.create_text_channel(f"luckyrush-{len(sessions)}")
    sessions[code] = GameSession(bot, ctx.author, guild, c)
    await c.send(embed=embed)
    await c.set_permissions(guild.default_role, overwrite=discord.PermissionOverwrite(
        view_channel=False
    ))
    await c.set_permissions(ctx.author, overwrite=discord.PermissionOverwrite(
        view_channel=True
    ))


@bot.hybrid_command(description="Join to the Lucky Rush lobby via code")
async def join(ctx):
    await ctx.send(view=JoinView())


@bot.hybrid_command(description="Leave the lobby you're currently in")
async def leave(ctx):
    for i in sessions.values():
        if ctx.author in i.players:
            await i.leave(ctx.author)
t = Thread(target=sessiontime_decrease, args=[bot], daemon=True)
t.start()
bot.run(os.getenv("TOKEN"))


