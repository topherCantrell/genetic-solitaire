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
        ret = ret + str(card) + ' '
    return ret.strip()


class SolitaireBoard:

    def __init__(self, draw_count=3):
        self.draw_count = draw_count
        self.pile = []
        self.pile_pos = 24 - draw_count  # Not 24 -- we start with some flipped
        self.stacks = [[], [], [], [], [], [], []]
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
            cnt = cnt + len(self.foundation[i])
        return cnt

    def __str__(self):
        ret = 'Foundation:\n'
        ret += '  Fh : ' + _make_card_run(self.foundation['hearts'], -1, '') + '\n'
        ret += '  Fd : ' + _make_card_run(self.foundation['diamonds'], -1, '') + '\n'
        ret += '  FC : ' + _make_card_run(self.foundation['clubs'], -1, '') + '\n'
        ret += '  FS : ' + _make_card_run(self.foundation['spades'], -1, '') + '\n'

        ret += 'Stacks:\n'
        for j in range(len(self.stacks)):
            stk = self.stacks[j]
            num = str(j)
            ret += '  S' + num + ' : ' + _make_card_run(stk, self.stacks_pos[j], '||') + '\n'

        ret += 'Pile:\n'
        ret += '   P : ' + _make_card_run(self.pile, self.pile_pos, '>>') + '\n'
        return ret
