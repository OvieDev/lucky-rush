import discord

from discord import ui

from components.GameChoice import GameChoice


class ActionCardView(ui.View):

    def __init__(self, game, player):
        super().__init__()
        self.game = game
        self.buttons = []
        self.player = player
        emojis = self.get_players_and_emojis()

        for i, e in enumerate(self.children):
            e.emoji = emojis[i]

    def get_players_and_emojis(self):
        player_index = self.game.players.index(self.player)

        if player_index == 0:
            self.buttons = [self.game.players[1], self.game.players[2]]
            return ["🧛", "🧞"]

        elif player_index == 1:
            self.buttons = [self.game.players[0], self.game.players[2]]
            return ["🧙", "🧞"]

        elif player_index == 2:
            self.buttons = [self.game.players[0], self.game.players[1]]
            return ["🧙", "🧛"]

    @ui.button(style=discord.ButtonStyle.green)
    async def target_player_1(self, interaction: discord.Interaction, button):
        caster_data = self.game.player_data[f"{self.player.id}"]
        caster_data["action_target"] = self.buttons[0]
        caster_data["moved"] = True
        caster_data["choice"] = GameChoice.ACTION_CARD
        await interaction.response.send_message(content=f"You used an action card on {self.buttons[0]}", ephemeral=True)

    @ui.button(style=discord.ButtonStyle.danger)
    async def target_player_2(self, interaction: discord.Interaction, button):
        caster_data = self.game.player_data[f"{self.player.id}"]
        caster_data["action_target"] = self.buttons[1]
        caster_data["moved"] = True
        caster_data["choice"] = GameChoice.ACTION_CARD
        await interaction.response.send_message(content=f"You used an action card on {self.buttons[1]}", ephemeral=True)
