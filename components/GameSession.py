import discord


class GameSession:
    def __init__(self, creator: discord.User):
        self.players = [creator]

    def join(self, user: discord.User):
        if not len(self.players) > 3:
            self.players.append(user)

    def leave(self, index):
        del self.players[index]
