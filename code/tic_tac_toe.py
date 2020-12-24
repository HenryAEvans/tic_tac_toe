from sboard import *
from player import *
def main():
    board = SBoard()
    players = []
    players.append(Player('X', "player1"))
    players.append(Player('O', "player2"))
    while True:
        for player in players:
            print(board)
            board.move(player.get_move_s(board), player.symbol)
            if board.winner != 0:
                print(board)
                print(player.symbol, "is the winner!!")
                exit()
            if board.isfull:
                print("draw!")
                exit()

if __name__ == "__main__":
    main()
