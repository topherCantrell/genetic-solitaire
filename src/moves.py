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
of cards can be flipped with the one character move 'P'. This is not a card move. No 
cards change position.

End of Game:

The game is over when there are no more moves or the maximum number of moves has been made.
We'll start with a high value and reduce it with collected stats.

'''

import cards as CARDS


def _does_fit(src_card, dst_list, is_stacks):
    # example card: [2, '2'], ['clubs', 'C', 'black']
    if is_stacks:
        # Special case for empty stacks: Kings can move here.
        if not dst_list:
            if src_card[0][0] == 13:
                return True
            else:
                # Nothing else can move to a empty stack
                return False
        dst_card = dst_list[-1]
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
        # Must be the foundation.
        # Special case for empty foundations: Aces can move here.
        if not dst_list:
            if src_card[0][0] == 1:
                return True
            else:
                return False
        dst_card = dst_list[-1]
        # Suits must match.
        if src_card[1][0] != dst_card[1][0]:
            return False
        # SRC value must be DST+1
        if src_card[0][0] == dst_card[0][0] + 1:
            return True
        return False


def find_moves(board):
    ret = []

    # Moving cards from the ends of the stacks to the foundation
    # 'S?e-F'
    for src in range(7):
        if not board['stacks'][src]:
            continue
        card = board['stacks'][src][-1]
        if _does_fit(card, board['foundation'][card[1][0]], False):
            ret.append('S{}e-F'.format(src))

    # Moving cards from foundation back to stacks
    # 'F?-S?
    for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
        if not board['foundation'][suit]:
            # No cards in this stack
            continue
        card = board['foundation'][suit][-1]
        for dst in range(7):
            if _does_fit(card, board['stacks'][dst], True):
                ret.append(
                    'F{}-S{}'.format(CARDS.get_short_suit_name(suit), dst))

    # Moving cards around the ends of the stacks
    for src in range(7):
        if not board['stacks'][src]:
            continue
        for dst in range(7):
            if src == dst:
                continue
            card = board['stacks'][src][-1]
            if _does_fit(card, board['stacks'][dst], True):
                ret.append('S{}e-S{}'.format(src, dst))

    # Moving groups of cards around the ends of stacks
    # 'S?h-S?'
    for src in range(7):
        pos = board['stacks_pos'][src]
        if pos == len(board['stacks'][src]) - 1:
            # The head and end are the same -- we've already done this one
            continue
        for dst in range(7):
            if src == dst:
                continue
            card = board['stacks'][src][pos]
            if _does_fit(card, board['stacks'][dst], True):
                ret.append('S{}h-S{}'.format(src, dst))

    # Moving cards from P to Foundation
    # 'P-F'
    if board['pile']:
        pos = board['pile_pos']
        card = board['pile'][pos]
        if _does_fit(card, board['foundation'][card[1][0]], False):
            ret.append('P-F')

    # Moving cards from P to Stacks
    # 'P-S?'
    for dst in range(7):
        if _does_fit(card, board['stacks'][dst], True):
            ret.append('P-S{}'.format(dst))

    # Flipping cards.
    # 'P'
    if len(board['pile']) < 3 and board['pile_pos'] == 0:
        pass
    else:
        ret.append('P')

    return ret


# Common action functions


def _remove_from_stacks(board, src, src_pos):
    # Pull one (or more) cards from the stack. Make sure the end
    # of the stack is flipped over.
    if src_pos == -1:
        # VM probably does the right thing, but just in case
        src_pos = len(board['stacks'][src]) - 1
    cards = board['stacks'][src][src_pos:]
    board['stacks'][src] = board['stacks'][src][:src_pos]
    if len(board['stacks'][src]) <= board['stacks_pos'][src]:
        board['stacks_pos'][src] -= 1
    return cards


def _add_to_stacks(board, dst, cards):
    # Put one (or more) cards on a stack.
    board['stacks'][dst] = board['stacks'][dst] + cards


def _remove_from_foundation(board, suit):
    # Pull a single card from the foundation.
    card = board['foundation'][suit].pop()
    return card


def _add_to_foundation(board, card):
    # Add a card to the foundation
    board['foundation'][card[1][0]].append(card)


def _remove_from_pile(board):
    # Remove a card from the head of the pile. Automatically flip the next three
    # if needed so we never run out of cards.
    pos = board['pile_pos']
    card = board['pile'][pos]
    board['pile'] = board['pile'][:pos] + board['pile'][pos + 1:]
    if pos == len(board['pile']):
        pos = len(board['pile']) - 3
        if pos < 0:
            pos = 0
        board['pile_pos'] = pos
    return card


def _flip_next_pile(board):
    # Flip the next three cards on the pile. Handle wrap around when we reach
    # the end.
    pos = board['pile_pos']
    if pos == 0:
        pos = len(board['pile'])
    pos = pos - 3
    if pos < 0:
        pos = 0
    board['pile_pos'] = pos


def make_move(move, board):

    # Moving a card from the ends of the stacks to the foundation
    # 'S?e-F'
    if move[0] == 'S' and move.endswith('e-F'):
        src = int(move[1])
        card = _remove_from_stacks(board, src, -1)
        _add_to_foundation(board, card[0])
        return

    # Moving a card from foundation back to stacks
    # 'F?-S?'
    if move[0] == 'F' and move[2:4] == '-S':
        print(move)
        suit = move[1]
        dst = int(move[4])
        card = _remove_from_foundation(board, CARDS.get_long_suit_name(suit))
        _add_to_stacks(board, dst, [card])
        return

    # Moving cards around the ends of the stacks
    # 'S?e-S?'
    if move[0] == 'S' and move[2:5] == 'e-S':
        src = int(move[1])
        dst = int(move[5])
        card = _remove_from_stacks(board, src, -1)
        _add_to_stacks(board, dst, card)
        return

    # Moving groups of cards around the ends of the stacks
    # 'S?h-S?'
    if move[0] == 'S' and move[2:5] == 'h-S':
        src = int(move[1])
        dst = int(move[5])
        cards = _remove_from_stacks(board, src, board['stacks_pos'][src])
        _add_to_stacks(board, dst, cards)
        return

    # Moving a card from the pile to the foundation
    # 'P-F'
    if move == 'P-F':
        card = _remove_from_pile(board)
        _add_to_foundation(board, card)
        return

    # Moving a card from the pile to the stacks
    # 'P-S?'
    if move.startswith('P-S'):
        dst = int(move[3])
        card = _remove_from_pile(board)
        _add_to_stacks(board, dst, [card])
        return

    # Flipping cards.
    # 'P'
    if move == 'P':
        _flip_next_pile(board)
        return

    raise Exception('Unimplemented move ' + move)
