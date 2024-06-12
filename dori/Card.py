class Card:
    score = int()
    img = str()
    light = bool()

    def __init__(self, sc, i):
        self.score = sc
        self.img = i
        self.light = False
