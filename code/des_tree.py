from player_ai import *
from multiprocessing import Pool

WIN_PATHS = (((1, 2), (3, 6), (4, 8)), ((0, 2), (4, 7)), ((0, 1), (4, 6), (5, 8)), ((0, 6), (4, 5)), ((0, 8), (1, 7), (2, 6), (3, 5)), ((2, 8), (3, 4)), ((0, 3), (4, 2), (7, 8)), ((6, 8), (1, 4)), ((6, 7), (0, 4), (2, 5)))
IMPORTANCE_CONST = 0.7
class Node:
    def __init__(self, num_moves, move, array1, player, b_array):
        self.move = move
        self.b_array = b_array
        self.array1 = array1
        self.player = player
        self.importance_value = self.importance()
        self.children = []
        self.array1 = self.get_new_array()
        #if the move results in a win, then terminate the tree
        if num_moves > 0 and self.importance_value != 100:
            #print(f"possible moves: {self.gen_possible_moves()}")
            for possibility in self.gen_possible_moves():
                self.children.append(Node(num_moves-1, possibility, self.array1, -player, self.update_b_array()))
        else:
            self.acc_importance = self.importance_value
            return None
        #print(f"children: {self.children}")
        selected_move = max(self.children)
        self.acc_importance = self.importance_value - selected_move.acc_importance * IMPORTANCE_CONST

    def __lt__(self, other):
        return self.acc_importance < other.acc_importance
    #tested
    def gen_possible_moves(self):
        """takes in a board configuration, and returns a list of possible spots the opponnent could occupy"""
        """outputs coords in the form: (spot1, spot2)"""
        #note for later: might be more efficient to store all of the spots that are occupied by a player in a single list OR
        #maintaining a seperate list w/ this info
        result = []
        curr_board = self.array1[self.move[1]]
        #print(f"current board: {curr_board}")
        #check if any of the spots in the board we landed in are available
        for index, cont in enumerate(curr_board):
            if cont == 0:
                result.append((self.move[1],) + (index,))
        #if not, then add all of the possibilities across the entire board
        if len(result) == 0:
            #return ALL of the possibilities
            for b_index, board in enumerate(self.array1):
                for s_index, spot in enumerate(board):
                    if spot == 0:
                        result.append((b_index,) + (s_index,))
        return result
    #tested
    def importance(self):
        AI_glob_imp = self.gen_importance_player(self.b_array, self.player, self.move[0])
        OP_glob_imp = self.gen_importance_player(self.b_array, -self.player, self.move[0])
        AI_loc_imp = self.gen_importance_player(self.array1[self.move[0]], self.player, self.move[1])
        OP_loc_imp = self.gen_importance_player(self.array1[self.move[0]], -self.player, self.move[1])
        #if the spot is taken, importance should be -1
        if AI_loc_imp == -1:
            return -1
        #if you can take the board to block, then do so
        if AI_loc_imp == 7:
            OP_loc_imp = 7
            #print("checkpoint 1")
        #same for the other way around
        if OP_loc_imp == 7:
            AI_loc_imp = 7
            #print("checkpoint 2")
        #if somebody is going to win then STOP THEM
        AI_imp = AI_glob_imp * AI_loc_imp
        if AI_imp >= 49:
            return 100
        return AI_imp + OP_glob_imp * OP_loc_imp

    #assume it works till is doesnt
    def get_new_array(self):
        #create the copy
        result = [self.array1[x][:] for x in range(len(self.array1))]
        #modify the result
        result[self.move[0]][self.move[1]] = self.player
        #pretty self explanatory
        return result

    #tested through the importance() function
    def gen_importance_player(self, array1, marker, spot):
        #marker should be -1 or 1, not X or O
        #array1 here is for a single board
        #spot is an int, not a tuple
        result = 0
        if array1[spot] != 0:
            return -1
        for spot1, spot2 in WIN_PATHS[spot]:
            spot1 = array1[spot1]
            spot2 = array1[spot2]
            #if none are occupied
            if spot1 == 0 and spot2 == 0:
                result += 1
                continue
            #if either of the spots is occupied by the other player
            if spot1 == -marker or spot2 == -marker:
                continue
            if spot1 == spot2:
                return 7
            result += 2
        return result

    def update_b_array(self):
        #can only be run once array1 has been updated
        #will return either a new copy of b_array if it has changed, or a reference to the old one if not
        board_won = False
        for spot1, spot2 in WIN_PATHS[self.move[0]]:
            spot1 = self.array1[spot1]
            spot2 = self.array1[spot2]
            if spot1 == self.player and spot2 == self.player:
                board_won = True
        if board_won:
            #create a copy of b_array
            result = self.b_array[:]
            #edit it with the nessecary changes
            result[self.move[0]] = self.player
            return result
        #if nothing changed, then don't make a copy and keep the old one
        else:
            return self.b_array





class DesTree:
    def __init__(self, num_moves, board, player):
        self.board = board
        self.last_move = board.lastx + board.lasty * 3
        self.num_moves = num_moves
        #self.n = Node(num_moves, (4, 4), self.gen_array1(), 1, self.gen_b_array())
        self.array1 = self.gen_array1()
        self.player = player
        self.children = []
        with Pool() as p:
            self.children = p.map(self.gen_node, self.gen_possible_moves(self.array1))
        #for move in self.gen_possible_moves(self.array1):
            #self.children.append(self.gen_node(move))

    def gen_node(self, move):
        #print(f"move: {move}")
        #print(f"array1: {self.array1}")
        return Node(self.num_moves-1, move, self.array1, self.player, self.gen_b_array())



    def gen_array1(self):
        result = [None]*9
        for y, line in enumerate(self.board.array):
            for x, sboard in enumerate(line):
                sboard.update_array1()
                result[3*x + y] = sboard.array1
        return result

    def gen_b_array(self):
        #-1 is an X win
        #0 is anyone's game
        #1 is an O win
        #-2 O has been blocked
        #2 X has been blocked
        return self.board.array1

    def gen_possible_moves(self, array1):
        """takes in a board configuration, and returns a list of possible spots the opponnent could occupy"""
        """outputs coords in the form: (spot1, spot2)"""
        #note for later: might be more efficient to store all of the spots that are occupied by a player in a single list OR
        #maintaining a seperate list w/ this info
        result = []
        curr_board = array1[self.last_move]
        #check if any of the spots in the board we landed in are available
        for index, cont in enumerate(curr_board):
            if cont == 0:
                result.append((self.last_move,) + (index,))
        #if not, then add all of the possibilities across the entire board
        if len(result) == 0:
            #return ALL of the possibilities
            for b_index, board in enumerate(array1):
                for s_index, spot in enumerate(board):
                    if spot == 0:
                        result.append((b_index,) + (s_index,))
        return result

    def get_move(self, move):
        #move is a four element tuple
        move_con = tuple(move[i] + 3*move[i+1] for i in range(0, 3, 2))
        for child in self.children:
            if child.move == move_con:
                return child
        raise ValueError("move does not exist")
