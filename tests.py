import unittest
import copy

from texas import Deck, Game, Hand
from cards import ClubCard, SpadeCard, HeartCard, DiamondCard

class TestDeck(unittest.TestCase):

    def setUp(self):
        self.deck = Deck()
        self.suits = {}
        for card in self.deck.deck:
            if card.suit not in self.suits:
                self.suits[card.suit] = [card.high]
            else:
                self.suits[card.suit].append(card.high)

    def test_deck(self):
        self.assertEqual(len(self.deck.deck), 52)
        for suit in self.suits:
            values = sorted(list(set(self.suits[suit])))
            self.assertEqual(len(values), 13)
            self.assertTrue(values[0] == 2)
            self.assertTrue(values[-1] == 14)


class TestHands(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.cards = [self.get_card(suit, value) for suit, value in [['s', 2], ['s', 9], ['h', 8], ['h', 11], ['c', 4]]]

    def get_card(self, suit, value):
        suits = {
            'c': ClubCard,
            'd': DiamondCard,
            's': SpadeCard,
            'h': HeartCard
        }
        return suits[suit](value)

    def test_highcard(self):
        g = Game(self.cards, blinds=3)
        player_hand = [self.get_card(suit, value) for suit, value in [['s', 14], ['d', 10],]]
        player = Hand(player_hand)
        play, hand_rank = player.play(g)
        self.assertEqual(hand_rank, 0)

    def test_pair(self):
        g = Game(self.cards, blinds=3)
        player_hand = [self.get_card(suit, value) for suit, value in [['s', 14], ['d', 9],]]
        player = Hand(player_hand)
        play, hand_rank = player.play(g)
        self.assertEqual(hand_rank, 1)

    def test_two_pairs(self):
        g = Game(self.cards, blinds=3)
        player_hand = [self.get_card(suit, value) for suit, value in [['s', 11], ['d', 9],]]
        player = Hand(player_hand)
        play, hand_rank = player.play(g)
        self.assertEqual(hand_rank, 2)

    def test_three_of_kind(self):
        g = Game(self.cards, blinds=3)
        player_hand = [self.get_card(suit, value) for suit, value in [['s', 11], ['d', 11],]]
        player = Hand(player_hand)
        play, hand_rank = player.play(g)
        self.assertEqual(hand_rank, 3)

    def test_straight(self):
        # test that straight works when straigh in the beginning
        cards = [self.get_card(suit, value) for suit, value in [['s', 2], ['s', 3], ['h', 4], ['h', 5], ['c', 6]]]
        g = Game(cards, blinds=3)
        player_hand = [self.get_card(suit, value) for suit, value in [['s', 11], ['d', 11],]]
        player = Hand(player_hand)
        play, hand_rank = player.play(g)
        self.assertEqual(hand_rank, 4)

        # now in the middle
        cards = [self.get_card(suit, value) for suit, value in [['s', 12], ['s', 3], ['h', 4], ['h', 5], ['c', 6]]]
        g = Game(cards, blinds=3)
        player_hand = [self.get_card(suit, value) for suit, value in [['s', 7], ['d', 11],]]
        player = Hand(player_hand)
        play, hand_rank = player.play(g)
        self.assertEqual(hand_rank, 4)

        # now in the end
        cards = [self.get_card(suit, value) for suit, value in [['s', 12], ['s', 13], ['h', 4], ['h', 5], ['c', 6]]]
        g = Game(cards, blinds=3)
        player_hand = [self.get_card(suit, value) for suit, value in [['s', 7], ['d', 8],]]
        player = Hand(player_hand)
        play, hand_rank = player.play(g)
        self.assertEqual(hand_rank, 4)

        # now mixed
        cards = [self.get_card(suit, value) for suit, value in [['s', 4], ['s', 13], ['h', 7], ['h', 6], ['c', 5]]]
        g = Game(cards, blinds=3)
        player_hand = [self.get_card(suit, value) for suit, value in [['s', 7], ['d', 8],]]
        player = Hand(player_hand)
        play, hand_rank = player.play(g)
        self.assertEqual(hand_rank, 4)

    def test_four_of_kind(self):
        cards = copy.deepcopy(self.cards)
        cards[0] = self.get_card('c', 11)
        g = Game(cards, blinds=3)
        player_hand = [self.get_card(suit, value) for suit, value in [['s', 11], ['d', 11],]]
        player = Hand(player_hand)
        play, hand_rank = player.play(g)
        self.assertEqual(hand_rank, 7)





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
