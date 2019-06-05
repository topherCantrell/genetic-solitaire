'''

Terminology:

  Foundation - 4 columns of cards (the aces)
  Pile       - cards flipped 3 at a time
  Stacks     - 7 columns of cards

'''

import cards as CARDS


def get_score(board):
    cnt = 0
    for i in ['hearts', 'diamonds', 'clubs', 'spades']:
        cnt = cnt + len(board['foundation'][i])
    return cnt


def new_board(deck):
    ret = {
        'pile': [],
        'pile_pos': 21,  # Not 24 ... we start with the first flip
        'stacks': [[], [], [], [], [], [], []],
        'stacks_pos': [0, 1, 2, 3, 4, 5, 6],
        'foundation': {'hearts': [], 'diamonds': [], 'clubs': [], 'spades': []}
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
    print('  Fh :', _make_card_run(board['foundation']['hearts'], -1, ''))
    print('  Fd :', _make_card_run(board['foundation']['diamonds'], -1, ''))
    print('  FC :', _make_card_run(board['foundation']['clubs'], -1, ''))
    print('  FS :', _make_card_run(board['foundation']['spades'], -1, ''))

    print('Stacks:')
    for j in range(len(board['stacks'])):
        stk = board['stacks'][j]
        num = str(j)
        print('  S' + num + ' :',
              _make_card_run(stk, board['stacks_pos'][j], '||'))

    print('Pile:')
    print('   P :', _make_card_run(
        board['pile'], board['pile_pos'], '>>'))
