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

        if "action_cards" in self.actions[variant]:
            for i in keys:
                self.game.player_data[i]["action_cards"] += self.actions[variant]["action_cards"]

        if "counter_cards" in self.actions[variant]:
            for i in keys:
                self.game.player_data[i]["counter_cards"] += self.actions[variant]["counter_cards"]

    def on_check(self):
        if "everyone" in self.actions:
            keys = list(self.game.player_data)
            self.key_actions("everyone", keys)

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
    }),
    Luckybox(
        "Suddenly, you hear a funky music, which makes you go craaazy 😛. You move one field ahead, HOWEVER you also need to wait for the music to finish (about one turn)",
        {
            "self": {
                "fields": 1,
                "timeout": 1
            }
        }),
    Luckybox(
        "You hit yourself in your pinky toe after you opened empty luckybox. Your entire nervous system is in pain, so you move 2 fields back to get some medicine or something???",
        {
            "self": {
                "fields": -2
            }
        }),
    Luckybox("A rocket emerges from the box which hits somebody. Nobody really knows what happens to that person", {
        "random": {
            "fields": random.randint(-2, 2),
            "timeout": 1
        }
    }),
    Luckybox("You find a bomb inside of the box. It explodes and you end up on the beginning", {
        "self": {
            "set_field": 1
        }
    }),
    Luckybox("You got your pair of shoes! It was filled with some paper and you find 2 action cards in them", {
        "self": {
            "action_cards": 2
        }
    }),
    Luckybox("You find a birthday cake in the box. Your enemies start singing \"Happy Birthday\" for 2 turns", {
        "enemies": {
            "timeout": 2
        }
    }),
    Luckybox(
        "You open a box, but you didn't saw what is inside, because an anvil has fallen on your head. You respawn and you're unable to move for 3 turns",
        {
            "self": {
                "timeout": 3,
                "set_field": 1
            }
        }
    ),
    Luckybox("You've created a giant force field, which pushes/pulls every player to the middle", {
        "everyone": {
            "set_field": 6
        }
    }),
    Luckybox("Inside, there's some cash. You hide it into your pocket", {}),
    Luckybox(
        "**NO WAY IT'S :exploding_head: :exploding_head: :exploding_head: THE UNO REVERSE CARD OMG :exploding_head: OMG**. You receive one counter card",
        {
            "self": {
                "counter_cards": 1
            }
        }),
    Luckybox("A cloud of darkness appears from the box, which........ *okay no one knows what it did*", {
        "random": {
            "set_field": random.randint(1, 7)
        }
    })

]


def select_random_box(game, player):
    lb = random.choice(luckyboxes)
    lb.game = game
    lb.player = player
    return lb
