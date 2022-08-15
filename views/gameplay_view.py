import discord
from discord import ui

from components.GameChoice import GameChoice


class GameplayView(ui.View):

    def __init__(self, game, timeout=None):
        self.game = game
        super().__init__(timeout=timeout)

    @ui.button(label="Check", style=discord.ButtonStyle.danger, emoji="❔")
    async def check_button(self, interaction: discord.Interaction, button: ui.Button):
        uid = interaction.user.id
        if not self.game.player_data[f"{uid}"]["moved"] and \
                self.game.player_data[f"{uid}"]["cannot_move_for"] == 0:
            self.game.player_data[f"{uid}"]["field"] += 1
            self.game.player_data[f"{uid}"]["moved"] = True
            self.game.player_data[f"{uid}"]["choice"] = GameChoice.CHECK
            await interaction.response.edit_message(embed=self.game.create_message(), view=self)
            await self.game.choice_made()
        else:
            if self.game.player_data[f"{uid}"]["cannot_move_for"] != 0:
                await interaction.response.send_message(
                    f"You cannot move for {self.game.player_data[f'{uid}']['cannot_move_for']}",
                    ephemeral=True)
            else:
                await interaction.response.send_message("You've already did your move! Wait for the next round!",
                                                        ephemeral=True)

    @ui.button(label="Pass", style=discord.ButtonStyle.gray, emoji="👟")
    async def pass_button(self, interaction: discord.Interaction, button: ui.Button):
        uid = interaction.user.id
        if not self.game.player_data[f"{uid}"]["moved"] and \
                self.game.player_data[f"{uid}"]["cannot_move_for"] == 0:
            self.game.player_data[f"{uid}"]["field"] += 1
            self.game.player_data[f"{uid}"]["moved"] = True
            self.game.player_data[f"{uid}"]["choice"] = GameChoice.PASS
            await interaction.response.edit_message(embed=self.game.create_message(), view=self)
            await self.game.choice_made()
        else:
            if self.game.player_data[f"{uid}"]["cannot_move_for"] != 0:
                await interaction.response.send_message(
                    f"You cannot move for {self.game.player_data[f'{uid}']['cannot_move_for']}",
                    ephemeral=True)
            else:
                await interaction.response.send_message("You've already did your move! Wait for the next round!",
                                                        ephemeral=True)

    @ui.button(label="Action Card", style=discord.ButtonStyle.blurple, emoji="<:action_card:1008726126220300358>")
    async def action_card_button(self, interaction: discord.Interaction, button):
        pass

    @ui.button(label="Counter Card", style=discord.ButtonStyle.green, emoji="<:counter_card:1008727843506765915>")
    async def counter_card_button(self, interaction: discord.Interaction, button):
        pass

    @ui.button(label="Trap Card", style=discord.ButtonStyle.danger, emoji="<:trap_card:1008729882974490735>")
    async def trap_card_button(self, interaction: discord.Interaction, button):
        pass
