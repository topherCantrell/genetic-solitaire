'''
pile - cards flipped 3 at a time
stacks - 7 columns of cards
foundation - 4 columns of cards (the aces)
'''

import cards as CARDS


def new_board(deck):
    ret = {
        'pile': [],
        'pile_pos': 24,
        'stacks': [[], [], [], [], [], [], []],
        'stacks_pos': [0, 1, 2, 3, 4, 5, 6],
        'foundation': [[], [], [], []]
    }

    for i in range(1, 8):
        for x in range(i):
            ret['stacks'][i - 1].append(deck.pop())

    ret['pile'] = deck

    return ret


def _make_card_run(cds, pos, sep):
    ret = ''
    for i in range(len(cds)):
        card = cds[i]
        if i == pos:
            ret = ret + sep + ' '
        ret = ret + CARDS.get_short_name(card) + ' '
    return ret.strip()


def show_board(board):

    print('Foundation:')
    for fds in board['foundation']:
        print('  :', _make_card_run(fds, -1, ''))

    print('Stacks:')
    for j in range(len(board['stacks'])):
        stk = board['stacks'][j]
        print('  :', _make_card_run(stk, board['stacks_pos'][j], '||'))

    print('Pile:')
    print('  :', _make_card_run(board['pile'], board['pile_pos'], '>>'))
