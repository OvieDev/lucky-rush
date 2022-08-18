import discord
from discord import ui

from components.GameChoice import GameChoice


class TrapCardView(ui.View):
    choices = {
        2: discord.SelectOption(label="Field 2", value="2"),
        3: discord.SelectOption(label="Field 3", value="3"),
        4: discord.SelectOption(label="Field 4", value="4"),
        5: discord.SelectOption(label="Field 5", value="5"),
        6: discord.SelectOption(label="Field 6", value="6"),
        7: discord.SelectOption(label="Field 7", value="7"),
        8: discord.SelectOption(label="Field 8", value="8"),
        9: discord.SelectOption(label="Field 9", value="9"),
        10: discord.SelectOption(label="Field 10", value="10"),
        11: discord.SelectOption(label="Field 11", value="11"),
    }

    def __init__(self, game):
        super().__init__()
        self.copy = self.choices.copy()
        self.game = game
        for i in self.game.player_data:
            print(self.game.player_data[i]["field"])
            print(self.game.player_data[i]["field"] in TrapCardView.choices)
            if self.game.player_data[i]["field"] in TrapCardView.choices:
                del self.copy[self.game.player_data[i]["field"]]

        self.children[0].options = list(self.copy.values())

    @ui.select(placeholder="Select field", max_values=1, min_values=1)
    async def select(self, interaction: discord.Interaction, select: ui.Select):
        pdata = self.game.player_data[f"{interaction.user.id}"]

        pdata["choice"] = GameChoice.TRAP_CARD
        self.game.traps[int(select.values[0]) - 2] = True
        pdata["moved"] = True
        pdata["field"] += 1
        select.disabled = True
        await interaction.response.edit_message(content=f"Placed a trap on field {select.values[0]}", view=self)
        await self.game.choice_made()
