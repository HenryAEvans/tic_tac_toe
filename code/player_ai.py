from sboard import *
from bboard import *
from des_tree import *
class PlayerAI:
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name
        self.win_paths = (((1, 2), (3, 6), (4, 8)), ((0, 2), (4, 7)), ((0, 1), (4, 6), (5, 8)), ((0, 6), (4, 5)), ((0, 8), (1, 7), (2, 6), (3, 5)), ((2, 8), (3, 4)), ((0, 3), (4, 2), (7, 8)), ((6, 8), (1, 4)), ((6, 7), (0, 4), (2, 5)))
        self.get_move_b = self.get_move_b_1

    def get_move_s(self, board):
        pass
        #generate a map of the importance of each space
        map = self.gen_importance_map(board.array1)
        #find the space with the max importance
        max_index = map.index(max(map))
        #return a tuple with the coordinates of that piece
        return (max_index%3, (max_index-max_index%3)//3)

    def get_move_b_1(self, board):
        #generate the desicion tree x moves deep
        tree = DesTree(5, board, board.char_to_num(self.symbol))
        #find the "max" move
        move = max(tree.children).move
        #return the move
        result = self.num_to_coords(move[0]) + self.num_to_coords(move[1])
        for child in tree.children:
            print(f"p_move: {child.move}, importance: {child.acc_importance}")
        print(f"best move: {move}, importance: {max(tree.children).acc_importance}")
        print(f"layer 0 importance: {max(tree.children).importance_value}")
        temp = max(tree.children)
        counter = 1
        while temp.children != []:
            print(f"layer {counter} importance: {temp.importance_value}")
            counter += 1
            temp = max(temp.children)
        return result
        #eliminate the branches where the opponent makes a bad move
        #add the importance of our moves, and subtract that of the opponent
        #pick the branch with the highest value

    def gen_importance_map(self, array1):
        #board must be a small board
        result = [0] * 9
        for spot in range(9):
            #if the spot is occupied, then assign it an importance of -1 and move along
            if array1[spot] != 0:
                result[spot] = -1
                continue
            #otherwise, iterate through self.win_paths
            for path in self.win_paths[spot]:
                spot1 = array1[path[0]]
                spot2 = array1[path[1]]
                #if none are occupied
                if spot1 == 0 and spot2 == 0:
                    result[spot] += 1
                    continue
                #if the spots are occupied by different players
                if spot1 == -spot2:
                    continue
                #if the spots are occupied by the same player
                if spot1 == spot2:
                    result[spot] = 5
                    continue
                #if only one of the spots is occupied
                if spot1 + spot2 != 0:
                    result[spot] += 2
                    continue
        return result

    def gen_importance_map_player(self, array1, marker):
        #marker should be -1 or 1, not X or O
        result = [0] * 9
        for spot in range(9):
            #if the spot is occupied, then assign it an importance of -1 and move along
            if array1[spot] != 0:
                result[spot] = -1
                continue
            for path in self.win_paths[spot]:
                spot1 = array1[path[0]]
                spot2 = array1[path[1]]
                #if none are occupied
                if spot1 == 0 and spot2 == 0:
                    result[spot] += 1
                    continue
                #if either of the spots is occupied by the other player
                if spot1 == -marker or spot2 == -marker:
                    continue
                if spot1 == spot2:
                    result[spot] += 5
                    continue
                if spot1 + spot2 != 0:
                    result[spot] += 2
        return result


    def num_to_coords(self, num):
        x = num % 3
        y = (num - num%3)//3
        return (x, y)
