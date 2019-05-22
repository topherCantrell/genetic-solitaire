
import board as BOARD
import cards as CARDS

# Play several games (checking for exceptions)
for _ in range(1000):

    deck = CARDS.make_deck()
    CARDS.shuffle_deck(deck)

    board = BOARD.new_board(deck)
    BOARD.show_board(board)

    for m in range(100):
        moves = BOARD.find_moves(board)
        print(moves)
        if not moves:
            break
        BOARD.make_move(moves[0], board)
        BOARD.show_board(board)

    score = BOARD.get_score(board)
    print('Score', score)
    if score > 5:
        raise Exception('WOO HOO')
