import asyncio
import time

import discord

sessions = {

}

def sessiontime_decrease(bot):

        global sessions
        while True:
            try:
                time.sleep(1)
                for k, v in list(sessions.items()):
                    v.until-=1
                    if v.until==0 and not v.more_than_one:
                        id = v.players[0].id
                        bot.dispatch("session_terminated", id, k, v.channel)
            except Exception as e:
                print(e)


class GameSession:
    def __init__(self, creator: discord.User, guild: discord.Guild, channel: discord.TextChannel):
        self.players = [creator]
        self.guild = guild
        self.until = 10
        self.channel = channel
        self.more_than_one = False

    def join(self, user: discord.User):
        if not len(self.players) > 3:
            self.players.append(user)

    def leave(self, index):
        del self.players[index]
