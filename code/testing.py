from sboard import *
from bboard import *
from player import *
from player_ai import *
def main():
    b = SBoard()
    players = []
    player1 = Player('X', "human")
    player2 = PlayerAI('O', "skynet")
    while True:
        print(b)
        print("X imp: ", player2.gen_importance_map_player(b.array1, -1))
        print("O imp: ", player2.gen_importance_map_player(b.array1, 1))
        b.move(player1.get_move_s(b), player1.symbol)
        print(b)
        print("X imp: ", player2.gen_importance_map_player(b.array1, -1))
        print("O imp: ", player2.gen_importance_map_player(b.array1, 1))
        b.move(player2.get_move_s(b), player2.symbol)


def playing(b):
    while True:
        print(b.__repr__())
        move = [None]*4
        move[0] = input("x of where you want to go: ")
        move[1] = input("y of where you want to go: ")
        move[2] = input("x2 of where you want to go: ")
        move[3] = input("y2 of where you want to go: ")
        print(b.move(move[0], move[1], move[2], move[3], 'X'))
def Splaying(b):
    while True:
        print(b.__repr__())
        move = [None]*2
        move[0] = int(input("x of where you want to go: "))
        move[1] = int(input("y of where you want to go: "))
        print(b.move(tuple(move), 'X'))
def full_game(board):
    players = []
    players.append(Player('X', "player1"))
    players.append(Player('O', "player2"))
    while True:
        for player in players:
            print(board)
            print(player.gen_importance_map(board))
            board.move(player.get_move_s(board), player.symbol)
            if board.winner != None:
                print(board)
                print(player.gen_importance_map())
                print(player.symbol, "is the winner!!")
                exit()
            if board.isfull:
                print("draw!")
                exit()

if __name__ == "__main__":
    main()
