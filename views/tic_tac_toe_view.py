import discord

from discord import ui


class TicTacToeView(ui.View):
    def __init__(self, difficulty):
        super().__init__()
        self.difficulty = difficulty
        self.lines = [[None, None, None], [None, None, None], [None, None, None]]

    def button_press(self, button):
        line = 0
        index = int(button.custom_id)
        while index > 2:
            line += 1
            index -= 3
        self.lines[line][index] = True
        button.disabled = True
        button.label = "X"

    @ui.button(label="-", custom_id="0", style=discord.ButtonStyle.blurple, row=1)
    async def button1(self, interaction: discord.Interaction, button: ui.Button):
        self.button_press(button)
        await interaction.response.edit_message(view=self)

    @ui.button(label="-", custom_id="1", style=discord.ButtonStyle.blurple, row=1)
    async def button2(self, interaction: discord.Interaction, button: ui.Button):
        self.button_press(button)
        await interaction.response.edit_message(view=self)

    @ui.button(label="-", custom_id="2", style=discord.ButtonStyle.blurple, row=1)
    async def button3(self, interaction: discord.Interaction, button: ui.Button):
        self.button_press(button)
        await interaction.response.edit_message(view=self)

    @ui.button(label="-", custom_id="3", style=discord.ButtonStyle.blurple, row=2)
    async def button4(self, interaction: discord.Interaction, button: ui.Button):
        self.button_press(button)
        await interaction.response.edit_message(view=self)

    @ui.button(label="-", custom_id="4", style=discord.ButtonStyle.blurple, row=2)
    async def button5(self, interaction: discord.Interaction, button: ui.Button):
        self.button_press(button)
        await interaction.response.edit_message(view=self)

    @ui.button(label="-", custom_id="5", style=discord.ButtonStyle.blurple, row=2)
    async def button6(self, interaction: discord.Interaction, button: ui.Button):
        self.button_press(button)
        await interaction.response.edit_message(view=self)

    @ui.button(label="-", custom_id="6", style=discord.ButtonStyle.blurple, row=3)
    async def button7(self, interaction: discord.Interaction, button: ui.Button):
        self.button_press(button)
        await interaction.response.edit_message(view=self)

    @ui.button(label="-", custom_id="7", style=discord.ButtonStyle.blurple, row=3)
    async def button8(self, interaction: discord.Interaction, button: ui.Button):
        self.button_press(button)
        await interaction.response.edit_message(view=self)

    @ui.button(label="-", custom_id="8", style=discord.ButtonStyle.blurple, row=3)
    async def button9(self, interaction: discord.Interaction, button: ui.Button):
        self.button_press(button)
        await interaction.response.edit_message(view=self)
