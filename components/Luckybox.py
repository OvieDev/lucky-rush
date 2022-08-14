import random


# Example on how actions variable should look like:
# {
# "random": {
#  "fields": -1,
#  "timeout": 2,
#  "set_field": 2
#  }
# }

class Luckybox:
    def __init__(self, text: str, actions: dict):
        self.text = text
        self.player = ""
        self.game = None
        self.actions = actions

    def key_actions(self, variant, keys):
        if "fields" in self.actions[variant]:
            for i in keys:
                self.game.player_data[i]["field"] += self.actions[variant]["fields"]
        if "timeout" in self.actions[variant]:
            for i in keys:
                self.game.player_data[i]["cannot_move_for"] += self.actions[variant]["timeout"]
        if "set_field" in self.actions[variant]:
            for i in keys:
                self.game.player_data[i]["field"] = self.actions[variant]["set_field"]

    def on_check(self):
        if "random" in self.actions:
            keys = list(self.game.player_data)
            key = random.choice(keys)
            self.key_actions("random", [key])
        if "enemies" in self.actions:
            keys = list(self.game.player_data)
            keys.remove(self.player)
            self.key_actions("enemies", keys)
        if "random_enemies" in self.actions:
            keys = list(self.game.player_data)
            keys.remove(self.player)
            key = random.choice(keys)
            self.key_actions("random_enemies", [key])
        if "self" in self.actions:
            self.key_actions("self", [self.player])


luckyboxes = [
    Luckybox("Inside there's an apple. What did ya expected?", {}),
    Luckybox("Inside there's a skeleton. You got scared and you need to wait 2 turns to overcome your mental problems",
             {
                 "self": {
                     "timeout": 2
                 }
             }),
    Luckybox("There are beans inside, which makes you fart and suddenly, you appear 1 field ahead", {
        "self": {
            "fields": 1
        }
    }),
    Luckybox("A gas cloud emerges from the box which poisons your enemies for 1 turn", {
        "enemies": {
            "timeout": 1
        }
    })
]


def select_random_box(game, player):
    lb = random.choice(luckyboxes)
    lb.game = game
    lb.player = player
    return lb
