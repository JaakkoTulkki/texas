import random

from cards import SpadeCard, HeartCard, ClubCard, DiamondCard


class Deck:
    def __init__(self):
        self.deck = [suit(num) for suit in [SpadeCard, HeartCard, ClubCard, DiamondCard] for num in range(2, 15)]
        random.shuffle(self.deck)

    def __str__(self):
        return "{}".format([card.__str__() for card in self.deck])

    def hole_cards(self):
        return self.deck.pop(), self.deck.pop()

    def flop(self):
        flop = [self.deck.pop(), self.deck.pop(), self.deck.pop()]
        return flop


class Hand:
    def __init__(self, *args, **kwargs):
        self.card_one = args[0][0]
        self.card_two = args[0][1]
        self.cards = [self.card_one, self.card_two]

    def __str__(self):
        return "{}".format([e.__str__() for e in self.cards])

    def high_card(self):
        return max(self.cards, key=lambda x: x.high)

    def get_best_hand(self):
        return self.high_card()

    def play(self, game):
        # we have flop
        self.cards = self.cards + game.cards
        return self.get_best_hand()

class Game:
    def __init__(self, *args, **kwargs):
        self.cards = args[0]
        self.pot = kwargs.get("blinds")

    def __str__(self):
        return "{}".format([e.__str__() for e in self.cards])


blind = 1
d = Deck()
h_one = Hand(d.hole_cards())
h_two = Hand(d.hole_cards())
h_three = Hand(d.hole_cards())
g = Game(d.flop(), blinds=blind*3)
print("common cards", g)
print("own cards ", h_one)

s = h_one.play(g)
print(s)


