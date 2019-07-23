'''

Terminology:

  Foundation - 4 columns of cards (the aces)
  Pile       - cards flipped 3 at a time
  Stacks     - 7 columns of cards

'''

import cards


def _make_card_run(cds, pos, sep):
    ret = ''
    for i in range(len(cds)):
        card = cds[i]
        if i == pos:
            ret = ret + sep + ' '
        ret = ret + CARDS.get_short_name(card) + ' '
    return ret.strip()


class SolitaireBoard:

    def __init__(self, draw_count=3):
        self.draw_count = draw_count
        self.pile = []
        self.pile_pos = 24 - draw_count  # Not 24 -- we start with some flipped
        self.stacks = [[] * 7]
        self.stacks_pos = [0, 1, 2, 3, 4, 5, 6]
        self.foundation = {'hearts': [], 'diamonds': [], 'clubs': [], 'spades': []}

        deck = cards.make_deck()
        cards.shuffle_deck(deck)

        # Make the stacks
        for i in range(1, 8):
            for x in range(i):
                self.stacks[i - 1].append(deck.pop())

        # The rest is the pile
        self.pile = deck

    def get_score(self):
        cnt = 0
        for i in ['hearts', 'diamonds', 'clubs', 'spades']:
            cnt = cnt + len(board.foundation[i])
        return cnt

    def __str__(self):
        ret = 'Foundation:'
        ret += '  Fh : ' + _make_card_run(board.foundation['hearts'], -1, '')
        ret += '  Fd : ', _make_card_run(board.foundation['diamonds'], -1, '')
        ret += '  FC : ', _make_card_run(board.foundation['clubs'], -1, '')
        ret += '  FS : ', _make_card_run(board.foundation['spades'], -1, '')

        ret += 'Stacks:'
        for j in range(len(board.stacks)):
            stk = board.stacks[j]
            num = str(j)
            ret += '  S' + num + ' : ' + _make_card_run(stk, board.stacks_pos[j], '||')

        ret += 'Pile:'
        ret += '   P : ', _make_card_run(board.pile, board.pile_pos, '>>')
