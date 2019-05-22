'''

Terminology:

  Foundation - 4 columns of cards (the aces)
  Pile       - cards flipped 3 at a time
  Stacks     - 7 columns of cards

Targets:

The last card in each of the 4 foundation sets is accessible. Moving cards to the foundation, the
target 'F' is used. Moving cards out of the foundation requires 'Fh','Fd', 'FC', or 'FS'.

The last card if each of the 7 stacks is accessible. The first card turned over in a stack
is accessible (the rest of the stack moves with it). The stacks are named 'S0', 'S1', 'S2',
'S3', 'S4', 'S5', and 'S6'. An extra letter 'e' targets the end of the stack. An extra
letter 'h' targets the head of the stack. Thus 'S3h' or 'S0e'. The target 'S' by itself means
the first empty stack.

The top flipped-over card of the pile is accessible. This target is 'Ph'. The next set
of cards can be flipped with the target 'Pf'. This is not a move. No cards change position.

End of Game:

The game is over when there are no more moves or the maximum number of moves has been made.
We'll start with a high value and reduce it with collected stats.

Game facts used to weigh moves:
  - Number of cards in the source pile
  - Number of cards in the destination pile
  - Number of cards in the foundation
  - Number of cards in the stacks
  - Length of target source stack
  - Length of target destination stack
  - Value of the target
  - Number of empty stacks
  - Number of kings in the top of the stacks

'''

import cards as CARDS

FOUNDATION_SUIT_ORDER = ['hearts', 'diamonds', 'clubs', 'spades']


def get_score(board):
    cnt = 0
    for i in range(4):
        cnt = cnt + len(board['foundation'][i])
    return cnt


def _does_fit(src_card, dst_card, is_stacks):
    # example card: [2, '2'], ['clubs', 'C', 'black']
    if is_stacks:
        # Special case for Aces ... no need to move them around the stacks
        if src_card[0][0] == 1:
            return False
        # Red/Black alternating
        if src_card[1][2] == dst_card[1][2]:
            return False
        # SRC value must be DST+1
        if src_card[0][0] == dst_card[0][0] - 1:
            return True
        return False
    else:
        # Must be the foundation. Suits must match.
        if src_card[1][0] != dst_card[1][0]:
            return False
        # SRC value must be DST+1
        if src_card[0][0] == dst_card[0][0] + 1:
            return True
        return False


def find_moves(board):
    ret = []

    # Moving cards from the ends of the stacks to the foundation
    for src in range(7):
        if not board['stacks'][src]:
            continue
        card = board['stacks'][src][-1]
        fid = FOUNDATION_SUIT_ORDER.index(card[1][0])

        if board['foundation'][fid]:
            # Stack on previous
            if _does_fit(card, board['foundation'][fid][-1], False):
                ret.append('S{}e-F'.format(src, card[1][1]))
        else:
            # Aces to empty
            if card[0][0] == 1:
                ret.append('S{}e-F'.format(src))

    # Moving cards around the ends of the stacks
    for src in range(7):
        if not board['stacks'][src]:
            continue
        for dst in range(7):
            if src == dst:
                continue
            if not board['stacks'][dst]:
                continue
            if _does_fit(board['stacks'][src][-1], board['stacks'][dst][-1], True):
                ret.append('S{}e-S{}e'.format(src, dst))

    return ret


def make_move(move, board):

    # Moving cards from the ends of the stacks to the foundation
    if move[0] == 'S' and move.endswith('e-F'):
        src = int(move[1])
        card = board['stacks'][src].pop()
        if len(board['stacks'][src]) <= board['stacks_pos'][src]:
            board['stacks_pos'][src] -= 1
        board['foundation'][FOUNDATION_SUIT_ORDER.index(
            card[1][0])].append(card)
        return

    # Moving cards around the ends of the stacks
    if move[0] == 'S' and move[-1] == 'e' and move[2:5] == 'e-S':
        src = int(move[1])
        dst = int(move[5])
        card = board['stacks'][src].pop()
        board['stacks'][dst].append(card)
        if len(board['stacks'][src]) <= board['stacks_pos'][src]:
            board['stacks_pos'][src] -= 1
        return

    raise Exception('Unimplemented move ' + move)


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
    print('  Fh :', _make_card_run(board['foundation'][0], -1, ''))
    print('  Fd :', _make_card_run(board['foundation'][1], -1, ''))
    print('  FC :', _make_card_run(board['foundation'][2], -1, ''))
    print('  FS :', _make_card_run(board['foundation'][3], -1, ''))

    print('Stacks:')
    for j in range(len(board['stacks'])):
        stk = board['stacks'][j]
        num = str(j)
        print('  S' + num + ' :',
              _make_card_run(stk, board['stacks_pos'][j], '||'))

    print('Pile:')
    print('   P :', _make_card_run(board['pile'], board['pile_pos'], '>>'))
