import random

from cards import SpadeCard, HeartCard, ClubCard, DiamondCard

HAND_RANK = {
    'high_card': 0,
    'pair': 1,
    'two-pairs': 2,
    'three-of-kind': 3,
    'straight': 4,
    'flush': 5,
    'full_house': 6,
    'four_of_kind': 7,
    'straight_flush': 8,
    'royal_flush': 9
}


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

    def turn(self):
        turn = self.deck.pop()
        return turn

    def river(self):
        river = self.deck.pop()
        return river

class Hand:
    def __init__(self, *args, **kwargs):
        self.card_one = args[0][0]
        self.card_two = args[0][1]
        self.cards = [self.card_one, self.card_two]

    def __str__(self):
        return "{}".format([e.__str__() for e in self.cards])

    def get_high_card(self):
        return [max(self.cards, key=lambda x: x.high)], HAND_RANK['high_card']

    def list_pairs(self):
        values = {}
        cards = [(e.high, e) for e in self.cards]
        for card in cards:
            if card[0] not in values:
                values[card[0]] = [card[1]]
            else:
                values[card[0]].append(card[1])
        return values

    def pair(self):
        rank = HAND_RANK['pair']
        values = self.list_pairs()
        if len(values) != 6:
            return False, rank
        else:
            for key in values:
                if len(values[key]) == 2:
                    return values[key], rank

    def two_pair(self):
        rank = HAND_RANK['two-pairs']
        values = self.list_pairs()
        to_be_returned = []
        if len(values) != 5:
            return False, rank
        else:
            for key in values:
                if len(values[key]) == 2:
                    to_be_returned += values[key]
        return to_be_returned, rank

    def three_of_kind(self):
        rank = HAND_RANK['three-of-kind']
        values = self.list_pairs()
        best_hand = 0
        for key in values:
            if len(values[key]) == 3 and key > best_hand:
                best_hand = key
        if best_hand:
            return values[best_hand], rank
        return False, rank

    def flush(self):
        rank = HAND_RANK['flush']
        suits = {}
        for card in self.cards:
            if card.suit not in suits:
                suits[card.suit] = [card]
            else:
                suits[card.suit].append(card)
        for suit in suits:
            if len(suits[suit]) >= 5:
                if len(suits[suit]) > 5:
                    while len(suits[suit]) > 5:
                        suits[suit].remove(min(suits[suit], key=lambda x: x.high))
                return suits[suit], rank
        return False, rank

    def straight(self, check_cards=[]):
        rank = HAND_RANK['straight']
        cards = []
        cards_to_use = check_cards if check_cards else self.cards
        for card in cards_to_use:
            if card.is_ace():
                cards.append([card.low, card])
                cards.append([card.high, card])
            else:
                cards.append([card.high, card])
        cards = sorted(cards, key=lambda x: x[0])
        # remove duplicates (make set)
        tracker = []
        new_cards = []
        for card in cards:
            if card[0] not in tracker:
                new_cards.append(card)
                tracker.append(card[0])
        cards = new_cards
        straight = False
        while not straight:
            for e in range(len(cards)-1, -1, -1):
                s = 0
                if e - 5 < -1:
                    straight = False
                    break
                check = cards[e-4:e+1]
                s = 0
                for c in range(len(check)-1):
                    if check[c+1][0] - check[c][0] != 1:
                        break
                    s += 1
                if s == 4:
                    straight = True
                    break
            break
        if straight:
            return check, rank
        else:
            return False, rank

    def full_house(self):
        rank = HAND_RANK['full_house']
        values = self.list_pairs()
        l = len(values)
        best_hand = [None, None]
        if l == 3 or l == 4:
            for key in values:
                if len(values[key]) == 3:
                    if not best_hand[1]:
                        best_hand[1] = (key, values[key])
                    else:
                        if best_hand[1][0] < key:
                            best_hand[1] = (key, values[key])
                if len(values[key]) == 2:
                    if not best_hand[0]:
                        best_hand[0] = (key, values[key])
                    else:
                        if best_hand[0][0] < key:
                            best_hand[0] = (key, values[key])
        if best_hand[0] and best_hand[1]:
            return best_hand[0][1] + best_hand[1][1], rank
        return False, rank

    def four_of_kind(self):
        rank = HAND_RANK['four_of_kind']
        values = self.list_pairs()
        for key in values:
            if len(values[key]) == 4:
                return values[key], rank
        return False, rank


    def straight_flush(self):
        rank = HAND_RANK['straight_flush']
        flush, f_rank = self.flush()
        if flush:
            # do the cards also create a straigh
            straight, s_rank = self.straight(check_cards=flush)
            if straight:
                return flush, rank
            else:
                return False, rank
        return None, rank

    def royal_flush(self):
        rank = HAND_RANK['royal_flush']
        sf, sf_rank = self.straight_flush()
        if sf and sf[-1].is_ace():
            return sf, rank
        return False, rank

    def get_best_hand(self):
        hands = [self.royal_flush, self.straight_flush, self.four_of_kind, self.full_house,
                 self.flush, self.straight, self.three_of_kind, self.two_pair, self.pair,
                 self.get_high_card]
        for hand in hands:
            # print("checking hand", hand.__name__)
            best, rank = hand()
            if best:
                return best, rank

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

    def turn(self, turn_card):
        self.cards.append(turn_card)

    def river(self, river_card):
        self.cards.append(river_card)

# blind = 1
# d = Deck()
# h_one = Hand(d.hole_cards())
# h_two = Hand(d.hole_cards())
# h_three = Hand(d.hole_cards())
# g = Game(d.flop(), blinds=blind*3)
# g.turn(d.turn())
# g.river(d.river())
# print("common cards", g)
# print("own cards ", h_one)
#
# s = h_one.play(g)
# print("{} - {}".format(s[1], [e.__str__() for e in s[0]]))


