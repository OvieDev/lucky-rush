import discord
from discord import ui

from components.GameChoice import GameChoice
from views.action_card_view import ActionCardView
from views.trap_card_view import TrapCardView


class GameplayView(ui.View):

    def __init__(self, game, timeout=None):
        self.game = game
        super().__init__(timeout=timeout)

    @ui.button(label="Check", style=discord.ButtonStyle.danger, emoji="❔")
    async def check_button(self, interaction: discord.Interaction, button: ui.Button):
        uid = interaction.user.id
        pdata = self.game.player_data[f"{uid}"]
        if not pdata["moved"] and pdata["cannot_move_for"] == 0:
            pdata["field"] += 1
            pdata["moved"] = True
            pdata["choice"] = GameChoice.CHECK
            await interaction.response.edit_message(embed=self.game.create_message(), view=self)
            await self.game.choice_made()
        else:
            if pdata["cannot_move_for"] != 0:
                await interaction.response.send_message(
                    f"You cannot move for {pdata['cannot_move_for']} turns",
                    ephemeral=True)
            else:
                await interaction.response.send_message("You've already did your move! Wait for the next round!",
                                                        ephemeral=True)

    @ui.button(label="Pass", style=discord.ButtonStyle.gray, emoji="👟")
    async def pass_button(self, interaction: discord.Interaction, button: ui.Button):
        uid = interaction.user.id
        pdata = self.game.player_data[f"{uid}"]
        if not pdata["moved"] and pdata["cannot_move_for"] == 0:
            pdata["field"] += 1
            pdata["moved"] = True
            pdata["choice"] = GameChoice.PASS
            await interaction.response.edit_message(embed=self.game.create_message(), view=self)
            await self.game.choice_made()
        else:
            if pdata["cannot_move_for"] != 0:
                await interaction.response.send_message(
                    f"You cannot move for {pdata['cannot_move_for']} turns",
                    ephemeral=True)
            else:
                await interaction.response.send_message("You've already did your move! Wait for the next round!",
                                                        ephemeral=True)

    @ui.button(label="Action Card", style=discord.ButtonStyle.blurple, emoji="<:action_card:1008726126220300358>")
    async def action_card_button(self, interaction: discord.Interaction, button):
        pdata = self.game.player_data[f"{interaction.user.id}"]
        if not pdata["moved"]:
            if pdata["action_cards"]>0:
                await interaction.response.send_message(view=ActionCardView(self.game, interaction.user), ephemeral=True)
            else:
                await interaction.response.send_message("You don't have any action cards",
                                                        ephemeral=True)
        else:
            await interaction.response.send_message("You've already did your move! Wait for the next round!",
                                                    ephemeral=True)

    @ui.button(label="Counter Card", style=discord.ButtonStyle.green, emoji="<:counter_card:1008727843506765915>")
    async def counter_card_button(self, interaction: discord.Interaction, button):
        pdata = self.game.player_data[f"{interaction.user.id}"]
        if not pdata["moved"]:
            if pdata["counter_cards"]>0 and len(pdata["action_pending"]) > 0:
                pdata["counter_cards"]-=1
                pdata["moved"] = True
                pdata["choice"] = GameChoice.COUNTER_CARD
                card = pdata["action_pending"].pop(0)
                card.active = False
                card.counter()
                self.game.player_data[f"{card.target}"]["action_pending"].append(card)
                await interaction.response.send_message("Successfully countered!", ephemeral=True)
                await self.game.choice_made()
            else:
                await interaction.response.send_message("You can't use counter cards right now", ephemeral=True)
        else:
            await interaction.response.send_message("You've already did your move! Wait for the next round!",
                                                    ephemeral=True)

    @ui.button(label="Trap Card", style=discord.ButtonStyle.danger, emoji="<:trap_card:1008729882974490735>")
    async def trap_card_button(self, interaction: discord.Interaction, button):
        pdata = self.game.player_data[f"{interaction.user.id}"]
        if not pdata["moved"]:
            if pdata["trap_cards"]>0:
                await interaction.response.send_message(content="Select field", view=TrapCardView(self.game), ephemeral=True)
            else:
                await interaction.response.send_message("You don't have any trap cards", ephemeral=True)
        else:
            await interaction.response.send_message("You've already did your move! Wait for the next round!",
                                                    ephemeral=True)

