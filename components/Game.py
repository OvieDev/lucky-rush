import asyncio
import threading
import time

import discord

from components.Luckybox import select_random_box
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
        self.message: discord.Message = None
        for i in self.players:
            self.player_data[f"{i.id}"] = {
                "field": 1,
                "moved": False,
                "choice": GameChoice.NONE,
                "cannot_move_for": 0,
                "luckyboxes": [False, False, False, False, False, False, False, False, False, False]
            }
        self.t = None

    async def player_choice_gen(self):
        final_string = ""
        for k in self.player_data:
            choice = self.player_data[k]["choice"]
            user: discord.User = await self.bot.fetch_user(int(k))
            if choice == GameChoice.PASS:
                final_string += f"{user.mention} passed the luckybox.\n"
            elif choice == GameChoice.CHECK:
                lb = select_random_box(self, str(user.id))
                final_string += f"{user.mention} checked the luckybox. {lb.text}\n"
                lb.on_check()
        return final_string

    def create_message(self):
        embed = discord.Embed(title=f"Round {self.round}")
        embed.description = ":white_large_square::white_large_square::white_large_square:\n"
        counter = 11

        def square_color():
            if counter == 1:
                return ":green_square:"
            else:
                return ":black_large_square:"

        for i in range(11):
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
                self.player_data[k]["choice"] = GameChoice.PASS
        await self.message.edit(embed=self.create_message(), view=GameplayView(self))
        await self.round_completion()

    async def choice_made(self):
        for k in self.player_data:
            if self.player_data[k]["moved"] is False:
                break
        else:
            self.t.cancel("Task canceled")
            await self.round_completion()

    async def start_game(self):
        self.t = asyncio.create_task(self.wait_for_choices())
        if self.message:
            await self.message.edit(content="", embed=self.create_message(), view=GameplayView(self))
        else:
            self.message = await self.channel.send(embed=self.create_message(), view=GameplayView(self))
        await self.t

    async def round_completion(self):
        await self.message.edit(content=f"""**ROUND {self.round} FINISH**\n{await self.player_choice_gen()}
        """, view=None, embed=None)
        self.round += 1
        await asyncio.sleep(5)
        for k in self.player_data:
            self.player_data[k]["moved"] = False
            self.player_data[k]["choice"] = GameChoice.NONE
        await self.start_game()
