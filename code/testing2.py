from player_ai import *
import timeit
import copy
from bboard import *
from des_tree import *
board = BBoard(3, 3)

def test():
    tree = DesTree(5, board, -1)

if __name__ == "__main__":
    time = timeit.timeit("test()", setup="from __main__ import test; from bboard import BBoard; board = BBoard(3, 3)", number=1)
    print(time)
    #print(node.gen_possible_moves())
