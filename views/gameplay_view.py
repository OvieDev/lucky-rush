import discord
from discord import ui


class GameplayView(ui.View):

    def __init__(self, game, timeout=None):
        self.game = game
        super().__init__(timeout=timeout)

    @ui.button(label="Check", style=discord.ButtonStyle.danger, emoji="❓")
    async def check_button(self, interaction: discord.Interaction, button: ui.Button):
        if not self.game.moved[f"{interaction.user.id}"]:
            self.game.player_to_field[f"{interaction.user.id}"] += 1
            self.game.moved[f"{interaction.user.id}"] = True
            await interaction.response.edit_message(embed=self.game.create_message(), view=self)
            self.game.choice_made()
