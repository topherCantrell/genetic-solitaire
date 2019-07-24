import random

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

    best_score = 0

    for _ in range(num_games):

        board = BOARD.SolitaireBoard()
        print(board)

        for m in range(5000):  # Limit to 100 moves
            moves = MOVES.find_moves(board)
            print(moves)
            if not moves:
                break
            m = random.choice(moves)
            print('Move:', m)
            MOVES.make_move(m, board)
            print(board)

        score = board.get_score()
        print('Score', score)

        if score > best_score:
            best_score = score

    print(best_score)


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

    play_auto(1000)

    # play_cli()
