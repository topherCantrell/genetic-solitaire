
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


def play_auto(num_games):
    for _ in range(num_games):

        deck = CARDS.make_deck()
        CARDS.shuffle_deck(deck)

        board = BOARD.new_board(deck)
        BOARD.show_board(board)

        for m in range(100):  # Limit to 100 moves
            moves = MOVES.find_moves(board)
            print(moves)
            if not moves:
                break
            MOVES.make_move(moves[0], board)
            BOARD.show_board(board)

        score = BOARD.get_score(board)
        print('Score', score)


def play_cli():
    deck = CARDS.make_deck()
    CARDS.shuffle_deck(deck)
    board = BOARD.new_board(deck)

    while True:
        moves = MOVES.find_moves(board)
        BOARD.show_board(board)
        print('------------')

        if not moves:
            print('No moves. Game over.')
            break

        for i in range(len(moves)):
            print('{}: {}'.format(i + 1, moves[i]))

        print()
        g = input('Move: ')

        MOVES.make_move(moves[int(g) - 1], board)
        print()


if __name__ == '__main__':

    # play_auto(1000)

    play_cli()
