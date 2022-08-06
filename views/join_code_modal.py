import discord

from discord import ui
from components.GameSession import sessions

class JoinCodeModal(ui.Modal, title='Join the game via code'):
    code = ui.TextInput(label="Join code", placeholder="Insert 10 character long code", min_length=10, max_length=10)

    async def on_submit(self, interaction: discord.Interaction):
        print(sessions)
        print(self.code)
        if self.code.value in sessions:
            if sessions[self.code.value].guild==interaction.guild:
                await interaction.response.send_message(content="Joining to the session", ephemeral=True)
                await sessions[self.code.value].join(interaction.user)
            else:
                await interaction.response.send_message(content=f"You're in the wrong server! This code is for: {sessions[self.code.value].guild.name}", ephemeral=True)
        else:
            await interaction.response.send_message(content="Nope", ephemeral=True)