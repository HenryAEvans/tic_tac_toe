class SBoard:
    def __init__(self):
    #does not have to be efficient
        self.array = [[0 for i in range(3)] for j in range(3)]
        self.winner = 0
        self.isfull = False
        self.array1 = [0]*9
        self.win_paths = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        self.last_player = 0

    def __repr__(self):
        result = ""
        for y in range(3):
            result += ' '
            for x in range(3):
                result += self.num_to_char(self.array[x][y])
                if x != 2:
                    result += ' | '
            result += ' \n'
            if y != 2:
                result += "---+---+---\n"
        return result

    def array_out(self):
        """returns an array where each element is a string representing a column"""
        #does not have to be efficient
        result = []
        for y in range(3):
            #line = list(self.array[y])
            line = [self.num_to_char(self.array[x][y]) for x in range(3)]
            result.append(' ' + ' | '.join(line) + ' ')
            result.append('---+---+---')
        result.pop()
        return result

    def move(self, coords, player):
        """takes in 2 coordinates, and returns whether that space is available. If it is, it makes the move"""
        #needs to be efficient
        x = coords[0]
        y = coords[1]
        if self.array[x][y] != 0:
            if self.winner != 0:
                raise ValueError("This board has been won")
            raise ValueError("tried to move to full spot")
        self.array[x][y] = self.char_to_num(player)
        self.last_player = self.char_to_num(player)
        #see if the grid is full or won
        self.find_winner()
        #if there's a winner, fill the grid with their marker
        if self.winner != 0:
            for x in self.array:
                for y in range(len(x)):
                    x[y] = self.winner
        self.find_full()

    def update_array1(self):
        #calculate array1
        for num in range(9):
            self.array1[num] = self.array[num%3][(num-num%3)//3]

    def find_winner(self):
        """will only find winner if it is the last person to move"""
        #calculate array1
        for num in range(9):
            self.array1[num] = self.array[num%3][(num-num%3)//3]
        #check all the paths
        for path in self.win_paths:
            result = True
            for spot in path:
                #for each spot check if it matches the last player, and if not, move on to the next one
                if self.array1[spot] != self.last_player:
                    result = False
                    break
            if result:
                self.winner = self.last_player
                break

    def find_full(self):
        for x in self.array:
            for y in x:
                if y == 0:
                    return None
        self.isfull = True

    def num_to_char(self, num):
        if num == 0:
            return ' '
        if num == -1:
            return 'X'
        if num == 1:
            return 'O'
        else:
            raise ValueError("invalid number" + num)
    def char_to_num(self, char):
        if char == ' ':
            return 0
        if char == 'X':
            return -1
        if char == 'O':
            return 1
        else:
            raise ValueError("Invalid Character")
