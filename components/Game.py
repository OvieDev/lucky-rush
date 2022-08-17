import asyncio

import discord
import random

from components.ActionCard import cards
from components.Luckybox import select_random_box
from components.GameChoice import GameChoice
from views.gameplay_view import GameplayView


class Game:
    card_types = {
        "action_cards": "<:action_card:1008726126220300358>",
        "counter_cards": "<:counter_card:1008727843506765915>",
        "trap_cards": "<:trap_card:1008729882974490735>"
    }

    def __init__(self, session, bot):
        self.__wait_time = 15
        self.stopped = False
        self.bot = bot
        self.players: list = session.players
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
                "luckyboxes": [False, False, False, False, False, False, False, False, False, False, True],
                "action_cards": 0,
                "counter_cards": 0,
                "trap_cards": 0,
                "action_pending": [],
                "action_target": None
            }
        self.t: asyncio.Task = None

    async def player_choice_gen(self):
        embed = discord.Embed(title=f"Round {self.round} COMPLETED!", description="What happened in this round?\n")
        for i in self.players:
            pdata = self.player_data[f"{i.id}"]
            final_string = ""

            if pdata["choice"] == GameChoice.PASS:
                final_string = f"Have passed the luckybox"

            elif pdata["choice"] == GameChoice.CHECK:

                if pdata["field"] - 2 < 0:
                    field = 0
                else:
                    field = pdata["field"] - 2

                if pdata["luckyboxes"][field] is False:
                    lb = select_random_box(self, f"{i.id}")
                    final_string = f"Have checked the luckybox. {lb.text}\n"
                    lb.on_check()
                    pdata["luckyboxes"][field] = True
                    card = random.randint(0, 2)

                    if card == 0:
                        card_type = "action_cards"

                    elif card == 1:
                        card_type = "trap_cards"

                    else:
                        card_type = "counter_cards"

                    pdata[card_type] += 1
                    final_string += f"{i.mention} also receives 1 {Game.card_types[card_type]}\n"

                else:
                    final_string = "Have tried to check the luckybox, but it was already open!"

            elif pdata["choice"] == GameChoice.NONE:
                final_string = "Is standing"

            elif pdata["choice"] == GameChoice.ACTION_CARD:
                final_string = f"Uses action card on {pdata['action_target'].mention}"
                card = random.choice(cards)
                card.game = self
                card.set_target_and_caster(f"{pdata['action_target'].id}", f"{i.id}")
                final_string += f"{card.text}"
                self.player_data[f"{pdata['action_target'].id}"]["action_pending"].append(card)

            elif pdata["choice"] == GameChoice.COUNTER_CARD:
                final_string = "Used a counter card!"
            embed.add_field(name=f"{i.name}", value=final_string, inline=False)

        footer = "Players waiting: "
        for p in self.players:
            footer += f"{p.name} : {self.player_data[f'{p.id}']['cannot_move_for']}, "
        embed.set_footer(text=footer)
        embed.colour = discord.Colour.random()
        return embed

    def create_message(self):
        embed = discord.Embed(title=f"Round {self.round}")
        embed.description = ":white_large_square::white_large_square::white_large_square:\n"
        counter = 11

        def square_color(who):
            if counter == 1:
                return ":green_square:"
            else:
                if self.player_data[who]["luckyboxes"][counter - 2] is True:
                    return ":large_orange_diamond:"
                else:
                    return ":black_large_square:"

        for i in range(11):
            if self.player_data[f"{self.players[0].id}"]["field"] == counter:
                embed.description += ":mage:"
            else:
                embed.description += square_color(f"{self.players[0].id}")

            if self.player_data[f"{self.players[1].id}"]["field"] == counter:
                embed.description += ":vampire:"
            else:
                embed.description += square_color(f"{self.players[1].id}")

            if self.player_data[f"{self.players[2].id}"]["field"] == counter:
                embed.description += ":genie:"
            else:
                embed.description += square_color(f"{self.players[2].id}")

            embed.description += "\n"
            counter -= 1

        embed.description += f"\n\n:mage: - {self.players[0].mention}, :vampire: - {self.players[1].mention}, :genie: - {self.players[2].mention}"
        return embed

    async def wait_for_choices(self):
        while True:
            try:
                for i in self.player_data:
                    if self.player_data[i]["cannot_move_for"] == 0:
                        break
                else:
                    raise Exception("Everyone is frozen :(")

                await asyncio.sleep(1)

                if not self.stopped:
                    self.__wait_time -= 1

                if self.__wait_time <= 0 and not self.stopped:
                    for k in self.player_data:
                        if self.player_data[k]["moved"] is False and self.player_data[k]["cannot_move_for"] == 0:
                            self.player_data[k]["field"] += 1
                            self.player_data[k]["moved"] = True
                            self.player_data[k]["choice"] = GameChoice.PASS
                    await self.round_completion()
            except Exception as e:
                await self.round_completion()

    async def end_game(self, users):
        await self.message.delete()
        mentions = ""

        for u in users:
            user = await self.bot.fetch_user(int(u))
            mentions += f"{user.mention}, "

        await self.channel.send(f"{mentions}you have won the game! <a:tada_blob:1008732078331936892>")
        await asyncio.sleep(7)
        await self.channel.delete()
        del self

    async def choice_made(self):
        for k in self.player_data:
            if self.player_data[k]["moved"] is False:
                break
        else:
            await self.round_completion()

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
        self.__wait_time = 15

        for i in self.player_data:
            if self.player_data[i]["cannot_move_for"] > 0:
                self.player_data[i]["cannot_move_for"] -= 1

        await self.message.edit(view=None, embed=await self.player_choice_gen())

        self.round += 1
        await asyncio.sleep(7)

        winner_list = []
        for i in self.player_data:
            for actions in self.player_data[i]["action_pending"]:
                if actions.active:
                    actions.on_check()
                    self.player_data[i]["action_pending"].remove(actions)
                else:
                    actions.active = True
            if self.player_data[i]["field"] < 1:
                self.player_data[i]["field"] = 1
            if self.player_data[i]["field"] >= 12:
                winner_list.append(i)

        if len(winner_list) > 0:
            await self.end_game(winner_list)

        for k in self.player_data:
            if self.player_data[k]["cannot_move_for"] == 0:
                self.player_data[k]["moved"] = False
            self.player_data[k]["choice"] = GameChoice.NONE

        self.stopped = False
        await self.start_game()
