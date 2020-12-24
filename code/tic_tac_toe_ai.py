from sboard import *
from player import *
from player_ai import *
def main():
    board = SBoard()
    players = []
    players.append(Player('X', "human"))
    players.append(PlayerAI('O', "SkyNet"))
    while True:
        print(board)
        for player in players:
            board.move(player.get_move_s(board), player.symbol)
            if board.winner != 0:
                print(board)
                print(player.name, "is the winner!!")
                exit()
            if board.isfull:
                print("draw!")
                exit()

if __name__ == "__main__":
    main()
