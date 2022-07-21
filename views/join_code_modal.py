import discord

from discord import ui


class JoinCodeModal(ui.Modal, title='Join the game via code'):
    code = ui.TextInput(label="Join code", placeholder="Insert 10 character long code", min_length=10, max_length=10)

    async def on_submit(self, interaction: discord.Interaction):
        # placeholder
        await interaction.response.send_message(f'Searching for code {self.code}', ephemeral=True)
