import asyncio

import discord
import random

from components.ActionCard import cards
from components.Luckybox import select_random_box
from components.GameChoice import GameChoice
import components.GameSession as GS
from views.gameplay_view import GameplayView


def get_card_type(card):
    if card == 0:
        return "action_cards"

    elif card == 1:
        return "trap_cards"

    else:
        return "counter_cards"


def resolve_icon(index):
    if index == 0:
        return ":mage:"
    elif index == 1:
        return ":vampire:"
    elif index == 2:
        return ":genie:"


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
        self.traps = [False, False, False, False, False, False, False, False, False, False, False]  # 2, 3, 4 etc.
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
        self.session = session

    async def player_choice_gen(self):
        embed = discord.Embed(title=f"Round {self.round} COMPLETED!", description="What happened in this round?\n")
        for i in self.players:
            pdata = self.player_data[f"{i.id}"]
            final_string = ""
            if self.traps[pdata["field"] - 2] and random.uniform(0, 1) > 0.2:
                final_string += "Has encountered a trap, which makes him move few fields backwards"
                self.traps[pdata["field"] - 2] = False
                pdata["field"] -= random.randint(1, 6)
                pdata["cannot_move_for"] += 1
            else:
                if pdata["field"] == 6 or pdata["field"] == 11:
                    mapping = {
                        GameChoice.TRAP_CARD: "trap_cards",
                        GameChoice.ACTION_CARD: "action_cards",
                        GameChoice.COUNTER_CARD: "counter_cards"
                    }

                    if pdata["choice"] in mapping:
                        key = mapping[pdata["choice"]]
                        pdata[key] += 1
                    pdata["choice"] = GameChoice.CHECK

                if pdata["choice"] == GameChoice.PASS:
                    final_string += f"Has passed the luckybox"

                elif pdata["choice"] == GameChoice.CHECK:

                    if pdata["field"] - 2 < 0:
                        field = 0
                    else:
                        field = pdata["field"] - 2

                    if pdata["luckyboxes"][field] is False:
                        lb = select_random_box(self, f"{i.id}")
                        final_string += f"Has checked the luckybox. {lb.text}\n"
                        lb.on_check()
                        pdata["luckyboxes"][field] = True
                        card = random.randint(0, 2)
                        card_type = get_card_type(card)
                        pdata[card_type] += 1
                        final_string += f"{i.mention} also receives 1 {Game.card_types[card_type]}\n"

                    else:
                        final_string += "Has tried to check the luckybox, but it was already open!"

                elif pdata["choice"] == GameChoice.NONE:
                    final_string += "Is standing"

                elif pdata["choice"] == GameChoice.ACTION_CARD:
                    final_string += f"Uses action card on {pdata['action_target'].mention}"
                    card = random.choice(cards)
                    card.game = self
                    card.set_target_and_caster(f"{pdata['action_target'].id}", f"{i.id}")
                    final_string += f"{card.text}"
                    self.player_data[f"{pdata['action_target'].id}"]["action_pending"].append(card)

                elif pdata["choice"] == GameChoice.COUNTER_CARD:
                    final_string += "Used a counter card!"

                elif pdata["choice"] == GameChoice.TRAP_CARD:
                    final_string += "Did something sneaky ;)"

            embed.add_field(name=f"{i.name}", value=final_string, inline=False)

        footer = "Players waiting: "

        for p in self.players:
            footer += f"{p.name} : {self.player_data[f'{p.id}']['cannot_move_for']}, "

        embed.set_footer(text=footer)
        embed.colour = discord.Colour.random()
        return embed

    def square_color(self, who, counter):
        special_fields = {
            1: ":green_square:",
            6: ":red_square:",
            11: ":red_square:"
        }

        if counter in special_fields:
            return special_fields[counter]
        else:
            if self.player_data[who]["luckyboxes"][counter - 2] is True:
                return ":large_orange_diamond:"
            else:
                return ":black_large_square:"

    def create_message(self):
        embed = discord.Embed(title=f"Round {self.round}")
        embed.description = ":white_large_square::white_large_square::white_large_square: **12**\n"
        counter = 11

        for i in range(11):
            for index in range(3):
                if self.player_data[f"{self.players[index].id}"]["field"] == counter:
                    embed.description += resolve_icon(index)
                else:
                    embed.description += self.square_color(f"{self.players[index].id}", counter)

            num = 11 - i
            embed.description += f" **{num}**"

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

        self.t.cancel()
        ses_copy = GS.sessions.copy()
        for k, v in ses_copy.items():
            if v == self.session:
                del GS.sessions[k]
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
        else:

            for k in self.player_data:
                if self.player_data[k]["cannot_move_for"] == 0:
                    self.player_data[k]["moved"] = False
                self.player_data[k]["choice"] = GameChoice.NONE

            self.stopped = False
            await self.start_game()
