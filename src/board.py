'''
pile - cards flipped 3 at a time
stacks - 7 columns of cards
foundation - 4 columns of cards (the aces)
'''


def new_board(deck):
    ret = {
        'pile': [],
        'pile_pos': 0,
        'stacks': [[], [], [], [], [], [], []],
        'stacks_pos': [0, 1, 2, 3, 4, 5, 6],
        'foundation': [[], [], [], []]
    }

    for i in range(1, 8):
        for x in range(i):
            ret['stacks'][i - 1].append(deck.pop())

    ret['pile'] = deck

    return ret


def card_desc(card):
    return card[0][1] + '_' + card[1][0]


def show_board(board):
    print('Foundation:')
    for s in board['foundation']:
        print(': ', end='')
        for g in s:
            p = card_desc(g)
            print(p + ',', end='')
        print()

    print('Stacks:')
    for j in range(len(board['stacks'])):
        s = board['stacks'][j]
        print(': ', end='')
        for i in range(len(s)):
            if i == board['stacks_pos'][j]:
                print('|| ', end='')
            g = s[i]
            p = card_desc(g)
            print(p + ', ', end='')
        print()

    print('Pile:')
    for i in range(len(board['pile'])):
        if i == board['pile_pos']:
            print('<< ', end='')
        g = board['pile'][i]
        p = card_desc(g)
        print(p + ', ', end='')
    print()
