import discord
from discord import ui


class HelpView(ui.View):

    def __init__(self, *, timeout=100):
        super().__init__(timeout=timeout)
        self.pageid = 0

    # placeholder
    def updateMessage(self):
        embed = discord.Embed(title=f"Help - Page {self.pageid + 1}")
        if self.pageid == 0:
            embed.add_field(name="help", value="Shows all of commands", inline=False)
            embed.add_field(name="rules", value="Shows rules of the Lucky Rush", inline=False)
            embed.add_field(name="start", value="Starts a new game", inline=False)
            embed.add_field(name="join", value="Join a game via code", inline=False)
            embed.add_field(name="gameopt", value="Set options of the game", inline=False)
        elif self.pageid==1:
            embed.add_field(name="ranked", value="Play ranked version of the game", inline=False)
            embed.add_field(name="leave", value="Leave current lobby", inline=False)
            embed.add_field(name="blackjack", value="Play a game of blackjack", inline=False)
            embed.add_field(name="roulette", value="Play a game of roulette", inline=False)
            embed.add_field(name="badgebuy", value="Buy the server badge", inline=False)
        else:
            embed.add_field(name="github", value="Get bot's GitHub", inline=False)
            embed.add_field(name="invite", value="Get invite link to the bot", inline=False)
        embed.set_footer(text="Prefix: rush!")
        embed.colour = discord.Colour.random()
        return embed

    def updateButtons(self):
        if self.pageid == 2:
            self.children[1].disabled = True
        else:
            self.children[1].disabled = False

        if self.pageid == 0:
            self.children[0].disabled = True
        else:
            self.children[0].disabled = False

    @discord.ui.button(label="Back", style=discord.ButtonStyle.blurple, disabled=True)
    async def pageback(self, interaction, button):
        self.pageid -= 1
        self.updateButtons()
        await interaction.response.edit_message(embed=self.updateMessage(), view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def page(self, interaction, button):
        self.pageid += 1
        self.updateButtons()
        await interaction.response.edit_message(embed=self.updateMessage(), view=self)
