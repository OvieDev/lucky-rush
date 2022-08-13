import asyncio
import threading
import time

import discord

from components.GameChoice import GameChoice
from views.gameplay_view import GameplayView


class Game:
    def __init__(self, session, bot):
        self.bot = bot
        self.players = session.players
        self.player_data = {}
        self.channel = session.channel
        self.round = 1
        self.moved = {}
        self.player_choice = {}
        self.message : discord.Message = None
        for i in self.players:
            self.player_data[f"{i.id}"] = {
                "field": 1,
                "moved": False,
                "choice": GameChoice.NONE
            }
        self.t = None

    def create_message(self):
        embed = discord.Embed(title=f"Round {self.round}")
        embed.description = ":white_large_square::white_large_square::white_large_square:\n"
        counter = 9

        def square_color():
            if counter == 1:
                return ":green_square:"
            else:
                return ":black_large_square:"

        for i in range(9):
            if self.player_data[f"{self.players[0].id}"]["field"] == counter:
                embed.description += ":mage:"
            else:
                embed.description += square_color()
            if self.player_data[f"{self.players[1].id}"]["field"] == counter:
                embed.description += ":vampire:"
            else:
                embed.description += square_color()
            if self.player_data[f"{self.players[2].id}"]["field"] == counter:
                embed.description += ":genie:"
            else:
                embed.description += square_color()
            embed.description += "\n"
            counter -= 1
        return embed

    async def wait_for_choices(self):
        await asyncio.sleep(30)
        for k in self.player_data:
            if self.player_data[k]["moved"] is False:
                self.player_data[k]["field"] += 1
                self.player_data[k]["moved"] = True
        await self.message.edit(embed=self.create_message(), view=GameplayView(self))

    def choice_made(self):
        for k in self.player_data:
            if self.player_data[k]["moved"] is False:
                break
        else:
            self.t.cancel("Task canceled")

    async def start_game(self):
        self.t = asyncio.create_task(self.wait_for_choices())
        self.message = await self.channel.send(embed=self.create_message(), view=GameplayView(self))
        await self.t
    # async def round_completion(self):

