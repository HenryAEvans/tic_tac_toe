from sboard import *
class BBoard:
    def __init__(self, row, col):
        self.array = [[SBoard() for i in range(col)] for j in range(row)]
        self.col = col
        self.row = row
        #to do: make it so that you don't have to start in the upper left board everytime
        self.lastx = 0
        self.lasty = 0
        self.array1 = [0]*9
        #each tuple here represents the id's of the spots you need to win a 3x3 tic-tac-toe board
        self.win_paths = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        self.last_player = None
    def __repr__(self):
        result = ''
        for boardy in range(self.row):
            for line in range(5):
                for boardx in range(self.col):
                    result += self.array[boardx][boardy].array_out()[line]
                    if boardx != self.col - 1:
                        result += ' || '
                result += '\n'
            if boardy != self.row - 1:
                result += '============++=============++=============\n'
        return result
    def move(self, coords, player):
        x1 = coords[0]
        y1 = coords[1]
        x2 = coords[2]
        y2 = coords[3]
        self.array[x1][y1].move((x2, y2), player)
        self.last_player = self.char_to_num(player)
        self.lastx = x2
        self.lasty = y2
        self.update_array1()

    def update_array1(self):
        #calculate array1
        for num in range(9):
            self.array1[num] = self.array[num%3][(num - num%3)//3].winner

    def get_winner(self):
        #should only be run directly after update_array1()
        """returns the marker of the winning player. If there is no winner, returns None"""
        for path in self.win_paths:
            result = True
            for spot in path:
                if self.array1[spot] != self.last_player:
                    result = False
                    break
            if result:
                return self.last_player
        return None

    def is_full(self):
        #should only be run directly after update_array1()
        #returns whether the board is full or not
        for spot in range(9):
            if self.array1[spot] == 0:
                return False
        return True

    def char_to_num(self, char):
        if char == ' ':
            return 0
        if char == 'X':
            return -1
        if char == 'O':
            return 1
        else:
            raise ValueError("Invalid Character")

    def num_to_char(self, num):
        if num == 0:
            return ' '
        if num == -1:
            return 'X'
        if num == 1:
            return 'O'
        else:
            raise ValueError("invalid number")
