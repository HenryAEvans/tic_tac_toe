from bboard import *
from player import *
from player_ai import *
from des_tree import *
import multiprocessing

def main():
    board = BBoard(3, 3)
    players = []
    players.append(Player('X', "human"))
    players.append(PlayerAI('O', "SkyNet"))
    while True:
        print(board)
        if board.array[board.lastx][board.lasty].isfull:
            #if the subboard is full
            print("you may choose any sub-board")
        else:
            print(f"sub-board: ({board.lastx+1}, {board.lasty+1})")
        for player in players:
            move = player.get_move_b(board)
            if player.name == "human":
                tree = DesTree(4, board, board.char_to_num(player.symbol))
                print(f"Importance of your move: {tree.get_move(move).acc_importance}")
            board.move(move, player.symbol)
            if board.get_winner() != None:
                print(board)
                print(player.name, "is the winner!")
                exit()
            if board.is_full():
                print("draw!")
                exit()

if __name__ == "__main__":
    #this is nessecary for pyinstaller to compile the code.
    multiprocessing.freeze_support()
    print("NOTE: multiprocessing is disabled in this verion.")
    print("To get the speedup associated with multiprocessing, run the python code found in the main branch of this repository.")
    main()
