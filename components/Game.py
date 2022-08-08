import discord

from views.gameplay_view import GameplayView


class Game:
    def __init__(self, session):
        self.players = session.players
        self.player_to_field = {}
        self.channel = session.channel
        self.round = 1
        for i in self.players:
            self.player_to_field[f"{i.id}"] = 1

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

    async def round_progress(self):

        await self.channel.send(embed=self.create_message(), view=GameplayView(self))
