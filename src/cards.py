import random

SUITS = [
    ['diamonds', 'red'],
    ['hearts',   'red'],
    ['clubs',    'black'],
    ['spades',   'black']
]

VALUES = [
    [1, 'A'],  # Ace
    [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'],
    [7, '7'], [8, '8'], [9, '9'], [10, '10'],
    [11, 'J'],  # Jack
    [12, 'Q'],  # Queen
    [13, 'K']  # King
]


def make_deck():
    deck = []
    for suit in SUITS:
        for value in VALUES:
            deck.append([value, suit])
    return deck


def shuffle_deck(deck):
    random.shuffle(deck)
