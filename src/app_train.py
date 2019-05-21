
import board
import cards


deck = cards.make_deck()
cards.shuffle_deck(deck)

brd = board.new_board(deck)

board.show_board(brd)
