from bboard import *
from player import *
from player_ai import *

def main():
    board = BBoard(3, 3)
    players = []
    players.append(Player('X', "player1"))
    players.append(Player('O', "player2"))
    while True:
        for player in players:
            print(board)
            board.move(player.get_move_b(board), player.symbol)
            #board.array[0][2].update_array1()
            if board.get_winner() != None:
                print(board)
                print(player.symbol, "is the winner!")
                exit()
            if board.is_full():
                print("draw!")
                exit()

if __name__ == "__main__":
    main()
