'''
Targets:

The last card in each of the 4 foundation sets is accessible. Moving cards to the foundation, the
target 'F' is used. Moving cards out of the foundation requires 'Fh','Fd', 'FC', or 'FS'.

The last card if each of the 7 stacks is accessible. The first card turned over in a stack
is accessible (the rest of the stack moves with it). The stacks are named 'S0', 'S1', 'S2',
'S3', 'S4', 'S5', and 'S6'. An extra letter 'e' targets the end of the stack. An extra
letter 'h' targets the head of the stack. Thus 'S3h' or 'S0e'. The target 'S' by itself means
the first empty stack.

The top flipped-over card of the pile is accessible. This target is 'P'. The next set
of cards can be flipped with the move 'P'. This is not a card move. No cards change position.

End of Game:

The game is over when there are no more moves or the maximum number of moves has been made.
We'll start with a high value and reduce it with collected stats.

'''
from _operator import pos


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

        if board['foundation'][card[1][0]]:
            # Stack on previous
            if _does_fit(card, board['foundation'][card[1][0]][-1], False):
                ret.append('S{}e-F'.format(src))
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
            card = board['stacks'][src][-1]
            if not board['stacks'][dst]:
                # Empty column ... we can move a King here
                if card[0][0] == 13:
                    ret.append('S{}e-S{}'.format(src, dst))
                continue
            if _does_fit(card, board['stacks'][dst][-1], True):
                ret.append('S{}e-S{}'.format(src, dst))

    # Moving groups of cards around the ends of stacks
    for src in range(7):
        pos = board['stacks_pos'][src]
        if pos == len(board['stacks'][src]) - 1:
            # The head and end are the same -- we've already done this one
            continue
        for dst in range(7):
            if src == dst:
                continue
            card = board['stacks'][src][pos]
            if not board['stacks'][dst]:
                # Empty column ... we can move a King here
                if card[0][0] == 13:
                    ret.append('S{}h-S{}'.format(src, dst))
                continue
            if _does_fit(card, board['stacks'][dst][-1], True):
                ret.append('S{}h-S{}'.format(src, dst))

    # Moving cards from P to Foundation
    pos = board['pile_pos']
    card = board['pile'][pos]
    if board['foundation'][card[1][0]]:
        # Stack on previous
        if _does_fit(card, board['foundation'][card[1][0]][-1], False):
            ret.append('P-F')
    else:
        # Aces to empty
        if card[0][0] == 1:
            ret.append('P-F')

    # TODO Moving cards from P to Stacks

    # Flipping cards.
    if len(board['pile']) < 3 and board['pile_pos'] == 0:
        pass
    else:
        ret.append('P')

    return ret


def make_move(move, board):

    # Moving cards from the ends of the stacks to the foundation
    if move[0] == 'S' and move.endswith('e-F'):
        src = int(move[1])
        card = board['stacks'][src].pop()
        if len(board['stacks'][src]) <= board['stacks_pos'][src]:
            board['stacks_pos'][src] -= 1
        board['foundation'][card[1][0]].append(card)
        return

    # Moving cards around the ends of the stacks
    if move[0] == 'S' and move[2:5] == 'e-S':
        src = int(move[1])
        dst = int(move[5])
        card = board['stacks'][src].pop()
        board['stacks'][dst].append(card)
        if len(board['stacks'][src]) <= board['stacks_pos'][src]:
            board['stacks_pos'][src] -= 1
        return

    # Moving groups of cards around the ends of the stacks
    if move[0] == 'S' and move[2:5] == 'h-S':
        src = int(move[1])
        src_pos = board['stacks_pos'][src]
        dst = int(move[5])
        cards = board['stacks'][src][src_pos:]
        board['stacks'][dst] = board['stacks'][dst] + cards
        board['stacks'][src] = board['stacks'][src][:src_pos]
        if len(board['stacks'][src]) <= board['stacks_pos'][src]:
            board['stacks_pos'][src] -= 1
        return

    # Moving a card from the pile to the foundation
    if move == 'P-F':
        pos = board['pile_pos']
        card = board['pile'][pos]
        board['pile'] = board['pile'][:pos] + board['pile'][pos + 1:]
        board['foundation'][card[1][0]].append(card)
        if pos == len(board['pile']):
            pos = len(board['pile']) - 3
            if pos < 0:
                pos = 0
            board['pile_pos'] = pos
        return

    # Flipping cards.
    if move == 'P':
        pos = board['pile_pos']
        if pos == 0:
            pos = len(board['pile'])
        pos = pos - 3
        if pos < 0:
            pos = 0
        board['pile_pos'] = pos
        return

    raise Exception('Unimplemented move ' + move)
