from components.Luckybox import Luckybox


class ActionCard(Luckybox):
    def __init__(self, text: str, actions: dict):
        super().__init__(text, actions)
        self.target = None
        self.active = False

    def on_check(self):
        self.key_actions("default", [self.target])

    def set_target_and_caster(self, t, c):
        self.target = t
        self.player = c
        self.text.replace("%", f"<@{self.target}>")

    def counter(self):
        temp = self.target
        self.target = self.player
        self.player = temp


cards = [
    ActionCard(f"You throw a rock at %. He will be stunned for 1 turn", {"default": {
        "timeout": 1
    }}),
    ActionCard("You use the card as a baseball bat, and you kick out % to the start line", {"default": {
        "set_field": 1
    }}),
    ActionCard("You do a backflip. It's sooo cool, that % must pay some respect and goes back 2 fields", {"default": {
        "fields": -2
    }})
]
