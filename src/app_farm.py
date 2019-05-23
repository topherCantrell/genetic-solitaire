
import board as BOARD
import cards as CARDS
import moves as MOVES

'''
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

# Play several games (checking for exceptions)
for _ in range(1000):

    deck = CARDS.make_deck()
    CARDS.shuffle_deck(deck)

    board = BOARD.new_board(deck)
    BOARD.show_board(board)

    for m in range(100):
        moves = MOVES.find_moves(board)
        print(moves)
        if not moves:
            break
        MOVES.make_move(moves[0], board)
        BOARD.show_board(board)

    score = BOARD.get_score(board)
    print('Score', score)
    if score > 7:
        raise Exception('WOO HOO')
