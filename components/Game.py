import asyncio

import discord

from components.Luckybox import select_random_box
from components.GameChoice import GameChoice
from views.gameplay_view import GameplayView


class Game:
    def __init__(self, session, bot):
        self.__wait_time = 30
        self.stopped = False
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
        self.t: asyncio.Task = None

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
            elif choice == GameChoice.NONE:
                final_string += f"{user.mention} is standing in place.\n"
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
        while True:
            try:
                for i in self.player_data:
                    if self.player_data[i]["cannot_move_for"] == 0:
                        break
                else:
                    raise Exception

                await asyncio.sleep(1)
                if not self.stopped:
                    self.__wait_time -= 1
                if self.__wait_time<=0 and not self.stopped:
                    for k in self.player_data:
                        if self.player_data[k]["moved"] is False and self.player_data[k]["cannot_move_for"] == 0:
                            self.player_data[k]["field"] += 1
                            self.player_data[k]["moved"] = True
                            self.player_data[k]["choice"] = GameChoice.PASS
                            await self.round_completion()
            except Exception:
                pass
            finally:
                await self.message.edit(embed=self.create_message(), view=GameplayView(self))

    async def choice_made(self):
        try:
            for k in self.player_data:
                if self.player_data[k]["moved"] is False:
                    break
                if self.player_data[k]["field"] >= 11:
                    raise Exception(k)
            else:
                self.t.cancel()
                await self.round_completion()
        except Exception as e:
            self.t.cancel("Task canceled")
            await self.message.delete()
            user = self.bot.fetch_user(int(e.args[0]))
            await self.channel.send(f"{user.mention} have won the game!")
            await asyncio.sleep(5)
            await self.channel.delete()
            del self

    async def start_game(self):
        if self.message:
            await self.message.edit(content="", embed=self.create_message(), view=GameplayView(self))
        else:
            self.message = await self.channel.send(embed=self.create_message(), view=GameplayView(self))
        if self.t is None:
            self.t = asyncio.create_task(self.wait_for_choices())
        await self.t

    async def round_completion(self):
        self.stopped = True
        self.__wait_time = 30
        for i in self.player_data:
            if self.player_data[i]["cannot_move_for"] > 0:
                self.player_data[i]["cannot_move_for"] -= 1

        await self.message.edit(content=f"""**ROUND {self.round} FINISH**\n{await self.player_choice_gen()}
        """, view=None, embed=None)

        self.round += 1
        await asyncio.sleep(7)

        for k in self.player_data:
            if self.player_data[k]["cannot_move_for"] == 0:
                self.player_data[k]["moved"] = False
            self.player_data[k]["choice"] = GameChoice.NONE
        self.stopped = False
        await self.start_game()
