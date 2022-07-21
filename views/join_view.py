import discord
from discord import ui

from views.join_code_modal import JoinCodeModal


class JoinView(ui.View):
    def __init__(self, *, timeout=200):
        super().__init__(timeout=timeout)

    @ui.button(label="Join via code!", style=discord.ButtonStyle.primary, emoji="🎉")
    async def join_game(self, interaction: discord.Interaction, button):
        await interaction.response.send_modal(JoinCodeModal())
        button.disabled = True
