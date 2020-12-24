from sboard import *
class Player:
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name
    def get_move_s(self, board):
        temp = None
        while temp == None:
            temp = self.get_coords_s(input(self.name + " please input your coordinates in x, y format: "), board)

        return temp
    def get_move_b(self, board):
        #if the spot where they should go is full
        if board.array[board.lastx][board.lasty].isfull:
            #at this point, we know where they should go is full
            b_coords = None
            while b_coords == None:
                b_coords = self.get_coords_b(input(self.name + " please input your board coordinates in x, y format: "), board)
        else:
            b_coords = (board.lastx, board.lasty)
        local_coords = None
        while local_coords == None:
            local_coords = self.get_coords_s(input(self.name + " please input your local coordinates in x, y format: "), board.array[b_coords[0]][b_coords[1]])
        return b_coords + local_coords


    def get_coordinates(self, input):
        """returns the coordinates if a valid input was given. Otherwise returns None
        does not check whether the spot is taken"""
        try:
            split_string = input.split(', ')
            x = int(split_string[0])-1
            y = int(split_string[1])-1
        except:
            print("that is not an integer")
            return None
        if x < 0 or x > 2 or y < 0 or y > 2:
            print("that is out of bounds")
            return None
        return (x, y)

    def get_coords_b(self, input, board):
        coords = self.get_coordinates(input)
        if board.array[coords[0]][coords[1]].isfull:
            print("That board is already full or won")
            return None
        return coords
    def get_coords_s(self, input, board):
        coords = self.get_coordinates(input)
        if board.array[coords[0]][coords[1]] != 0:
            print("That spot is taken")
            return None
        return coords
