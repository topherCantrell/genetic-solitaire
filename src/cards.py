import random

SUIT_REV = {
    'h': 'hearts',
    'd': 'diamonds',
    'C': 'clubs',
    'S': 'spades'
}
SUITS = {
    'hearts': ['h', 'red'],
    'diamonds': ['d', 'red'],
    'clubs': ['C', 'black'],
    'spades': ['S', 'black']
}
VALUES = {
    1: 'A', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6',
    7: '7', 8: '8', 9: '9', 10: 'T', 11: 'J',
    12: 'Q', 13: 'K'
}


class Card:

    def __init__(self, value, suit):
        # value 1A,2,3,4 ... 11J,12Q,13K
        # suit hearts, diamonds, clubs, spades
        assert value >= 1 and value <= 13
        assert suit in ['hearts', 'diamonds', 'clubs', 'spades']
        self.value = value
        self.suit = suit
        self.short_name = VALUES[value] + SUITS[suit][0]
        self.color = SUITS[suit][1]

    def __repr__(self):
        return self.short_name

    def __str__(self):
        return self.short_name


def make_deck():
    deck = []
    for suit in SUITS:
        for value in range(1, 14):
            deck.append(Card(value, suit))
    return deck


def shuffle_deck(deck):
    random.shuffle(deck)
