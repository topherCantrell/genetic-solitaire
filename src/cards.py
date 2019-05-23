import random

SUITS = [
    ['hearts',   'h', 'red'],
    ['diamonds', 'd', 'red'],
    ['clubs',    'C', 'black'],
    ['spades',   'S', 'black']
]

VALUES = [
    [1, 'A'],  # Ace
    [2, '2'], [3, '3'], [4, '4'], [5, '5'],
    [6, '6'], [7, '7'], [8, '8'], [9, '9'],
    [10, 'T'],  # Ten (to make it one digit like the rest)
    [11, 'J'],  # Jack
    [12, 'Q'],  # Queen
    [13, 'K']  # King
]


def get_long_suit_name(sname):
    if sname == 'h':
        return 'hearts'
    elif sname == 'd':
        return 'diamonds'
    elif sname == 'C':
        return 'clubs'
    elif sname == 'S':
        return 'spades'
    else:
        raise Exception(sname)


def get_short_suit_name(longname):
    if longname == 'hearts':
        return 'h'
    elif longname == 'diamonds':
        return 'd'
    elif longname == 'clubs':
        return 'C'
    elif longname == 'spades':
        return 'S'
    else:
        raise Exception(longname)


def get_short_name(card):
    return card[0][1] + card[1][1]


def make_deck():
    deck = []
    for suit in SUITS:
        for value in VALUES:
            deck.append([value, suit])
    return deck


def shuffle_deck(deck):
    random.shuffle(deck)
