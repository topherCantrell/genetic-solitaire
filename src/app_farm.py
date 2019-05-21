
import board as BOARD
import cards as CARDS


deck = CARDS.make_deck()
CARDS.shuffle_deck(deck)

board = BOARD.new_board(deck)

BOARD.show_board(board)
