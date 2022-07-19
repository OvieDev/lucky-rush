import discord
from discord import ui


class HelpView(ui.View):

    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        self.pageid = 0

    # placeholder
    def updateMessage(self):
        embed = discord.Embed(title=f"Help {self.pageid + 1}")
        if self.pageid == 0:
            embed.add_field(name="help", value="Shows all of commands")
            embed.add_field(name="rules", value="Shows rules of the Lucky Rush")
            embed.add_field(name="start", value="Starts a new game")
            embed.add_field(name="join", value="Join a game via code")
            embed.add_field(name="gameopt", value="Set options of the game")
        else:
            embed.add_field(name="yes", value="yes")
        embed.set_footer(text="Prefix: rush!")
        return embed

    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def page(self, interaction, button):
        self.pageid += 1
        if self.pageid == 3:
            button.disabled = True
        await interaction.response.edit_message(embed=self.updateMessage(), view=self)
