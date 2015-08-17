class CardClass:
    def __init__(self, value):
        if value == 14:
            self.low, self.high = 1, 14
        else:
            self.low = self.high = value

    def is_ace(self):
        if self.low == 1:
            return True
        return False

    def __str__(self):
        if self.is_ace():
            return "A - {suit}".format(suit=self.suit)
        return "{} - {}".format(self.high, self.suit)


class SpadeCard(CardClass):
    suit = "Spade"


class HeartCard(CardClass):
    suit = "Heart"


class DiamondCard(CardClass):
    suit = "Diamond"


class ClubCard(CardClass):
    suit = "Club"