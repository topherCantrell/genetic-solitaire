'''

Terminology:

  Foundation - 4 columns of cards (the aces)
  Pile       - cards flipped 3 at a time
  Stacks     - 7 columns of cards
  
Targets:

The last card in each of the 4 foundation sets is accessible. Cards can be removed from
the end or added to the end. The targets are named 'Fh', 'Fd', 'FC', 'FS'.

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
