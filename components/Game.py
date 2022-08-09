import threading
import time

import discord

from components.GameChoice import GameChoice
from views.gameplay_view import GameplayView


class Game:
    def __init__(self, session, bot):
        self.bot = bot
        self.players = session.players
        self.player_to_field = {}
        self.channel = session.channel
        self.round = 1
        self.moved = {}
        self.player_choice = {}
        self.message : discord.Message = None
        for i in self.players:
            self.player_to_field[f"{i.id}"] = 1
            self.moved[f"{i.id}"] = False
            self.moved[f"{i.id}"] = GameChoice.NONE
        self.t = threading.Thread(target=self.wait_for_choices, daemon=True)

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
            if self.player_to_field[f"{self.players[0].id}"] == counter:
                embed.description += ":mage:"
            else:
                embed.description += square_color()
            if self.player_to_field[f"{self.players[1].id}"] == counter:
                embed.description += ":vampire:"
            else:
                embed.description += square_color()
            if self.player_to_field[f"{self.players[2].id}"] == counter:
                embed.description += ":genie:"
            else:
                embed.description += square_color()
            embed.description += "\n"
            counter -= 1
        return embed

    def wait_for_choices(self):
        time.sleep(30)
        for k, v in self.moved.items():
            if v is False:
                self.player_to_field[k] += 1
                self.moved[k] = True
        self.bot.dispatch("timeout", self.message, self)

    def choice_made(self):
        for v in self.moved.values():
            if v is False:
                break
        else:
            self.t.join()

    async def start_game(self):
        self.t.start()
        self.message = await self.channel.send(embed=self.create_message(), view=GameplayView(self))

    # async def round_completion(self):

