import asyncio
import time

import discord

from components.Game import Game

sessions = {

}


def sessiontime_decrease(bot):
    while True:
        time.sleep(1)
        for k, v in list(sessions.items()):
            v.until -= 1
            if v.until == 0 and not v.more_than_one:
                id = v.players[0].id
                bot.dispatch("session_terminated", id, k, v.channel)
                print(f"deleted ses with id = {k}")


class GameSession:
    def __init__(self, bot, creator: discord.Member, guild: discord.Guild, channel: discord.TextChannel):
        self.bot = bot
        self.players = [creator]
        self.guild = guild
        self.until = 100
        self.channel = channel
        self.more_than_one = False

    async def join(self, user: discord.Member):
        if not len(self.players) == 3:
            self.players.append(user)
            self.more_than_one = True
            await self.channel.set_permissions(user, overwrite=discord.PermissionOverwrite(
                view_channel=True
            ))
            await self.players[0].send(f"{user.mention} joined to the session")

            if len(self.players) == 3:
                await self.channel.send(
                    f"Starting the game! {self.players[0].mention} {self.players[1].mention} {self.players[2].mention}")
                game = Game(self, self.bot)
                await game.start_game()

    async def leave(self, member):
        if self.players[0] == member:
            for i in self.players:
                await self.channel.set_permissions(i, overwrite=discord.PermissionOverwrite(
                    view_channel=False
                ))
                await self.channel.delete()
        else:
            self.players.remove(member)
            await self.channel.set_permissions(member, overwrite=discord.PermissionOverwrite(
                view_channel=False
            ))
            await self.players[0].send(f"{member.mention} left your game")
