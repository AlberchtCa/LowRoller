class Player:
    def __init__(self):
        self.cards = []
        self.button = False
        self.blinds = 100
        self.hasAction = False
        self.AI = False

    @property
    def isAI(self):
        if self.AI:
            return True
        else:
            return False

    @property
    def isButton(self):
        if self.button:
            return True
        else:
            return False


class GameState:
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.cards = []
        self.felt = []
        self.street = []
        self.actions = []
        self.pot = 0
        self.round_done = False
        self.game_done = False
        self.last_action = "None"
