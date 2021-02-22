# Scotty Dog Starter File

# NOTE: You can run this file locally to test if your program is working.

#=============================================================================

# INPUT FORMAT: board

# board: A 15 x 15 2D array, where each element is:
#   0 - an empty square
#   1 - the current position of Scotty
#   2 - a naturally generated barrier
#   3 - a player placed barrier

# Example Input:

# board: See "SAMPLE_BOARD" below.

#=============================================================================

# OUTPUT FORMAT when scotty_bot is called:

# A list of two integers [dx, dy], designating in which
# direction you would like to move. Your output must satisfy

# -1 <= dx, dy <= 1

# and one of the following, where board[y][x] is Scotty's current position:

# max(x + dx, y + dy) >= 15 OR min(x + dx, y + dy) < 0 (move off the board)
# OR
# board[y + dy][x + dx] < 2 (move to an empty square or stay still)

# Invalid outputs will result in Scotty not moving.

#=============================================================================

# OUTPUT FORMAT when trapper_bot is called:

# A list of two integers [x, y], designating where you would
# like to place a barrier. The square must be currently empty, i.e.
# board[y][x] = 0

# Invalid outputs will result in no barrier being placed.

### WARNING: COMMENT OUT YOUR DEBUG/PRINT STATEMENTS BEFORE SUBMITTING !!!
### (this file uses standard IO to communicate with the grader!)

#=============================================================================

# Write your bots in the scotty_bot and trapper_bot classes. Helper functions
# and standard library modules are allowed, and can be written before/inside
# these classes.

# You can define as many different strategies as you like, but only the classes
# currently named "scotty_bot" and "trapper_bot" will be run officially.



import random

class scotty_bot:

    path = []
    # move = 0

    def __init__(self):
        # You can define global states (that last between moves) here
        pass  # Wut, idk how to use this funciton, it just says error

    def find_scotty(self, board):
        # Helper function that finds Scotty's location on the board
        for y in range(15):
            for x in range(15):
                if board[y][x] == 1:
                    return (x, y)
    
    def count(self, board, mode, x, y):
        blockades = 0
        # If the input is out of the board
        if x < 0 or x > 14 or y < 0 or y > 14:
            return 0
        # Count how many are above
        if mode == 'u':
            for i in range(y+1, 15):
                for j in range(15):
                    if board[i][j] > 1:
                        blockades += 1
        # Count how many are below
        elif mode == 'd':
            for i in range(0, y):
                for j in range(15):
                    if board[i][j] > 1:
                        blockades += 1
        # Count how many are on the left
        elif mode == 'l':
            for i in range(15):
                for j in range(0, x):
                    if board[i][j] > 1:
                        blockades += 1
        # Count how many are on the right
        elif mode == 'r':
            for i in range(15):
                for j in range(x+1, 15):
                    if board[i][j] > 1:
                        blockades += 1
        # Count how many are surrounding
        elif mode == 'o':
            xl = x-1
            xh = x+2
            yl = y-1
            yh = y+2
            if yl < 0:
                yl = y
            if yh > 15:
                yh = y+1
            if xl < 0:
                xl = x
            if xh > 15:
                xh = x+1
            for i in range(yl, yh):
                for j in range(xl, xh):
                    if board[i][j] > 1:
                        blockades += 1
        return blockades

    def move(self, board):
        # Strategy1: just go straight in one general direction and avoid high barrier count areas
        x, y = self.find_scotty(board)
        direction = [[0,0],[0,0],[0,0],[0,0]]
        direction[0][0] = self.count(board, 'u', x, y)  # 0 = up
        direction[0][1] = 0
        direction[1][0] = self.count(board, 'd', x, y)  # 1 = down
        direction[1][1] = 1
        direction[2][0] = self.count(board, 'l', x, y)  # 2 = left
        direction[2][1] = 2
        direction[3][0] = self.count(board, 'r', x, y)  # 3 = right
        direction[3][1] = 3

        table = [
            [(0, 1), (-1, 1), (1, 1)],  # 0 = up
            [(0, -1), (-1, -1), (1, -1)],  # 1 = down
            [(-1, 0), (-1, 1), (-1, -1)],  # 2 = left
            [(1, 0), (1, 1), (1, -1)]]  # 3 = right

        direction.sort()

        # Although this function may not return, if it doesn't, it means that we have already lost (surrounded on all adjacent sides)
        # We'd probably lose before such a situation occurs anyways
        for d in direction:
            o = []
            # Using the correct table value by using the old index (d[1])
            o.append(self.count(board, 'o', x + table[d[1]][0][0], y + table[d[1]][0][1]))
            o.append(self.count(board, 'o', x + table[d[1]][1][0], y + table[d[1]][1][1]))
            o.append(self.count(board, 'o', x + table[d[1]][2][0], y + table[d[1]][2][1]))

            for helper in range(3, 0, -1):
                for s in range(helper):
                    skip = False
                    dx = table[d[1]][s][0]
                    dy = table[d[1]][s][1]
                    # Don't repeat (don't go back to where came from, otherwise may cause infinite loop. However, it still may infinite loop anyways)
                    for i in self.path:
                        if (x + dx, y + dy) == i:
                            skip = True
                            break
                    if skip:
                        continue
                    # Find if we can win
                    if max(x + dx, y + dy) >= 15 or min(x + dx, y + dy) < 0:
                        return (dx, dy)
                    # Will return the minimum not blocked one out of the 3 options
                    # ***Will not return if all 3 are blocked***    
                    if board[y + dy][x + dx] == 0 and min(o) == o[s]:
                        self.path.append((x + dx, y + dy))
                        return (dx, dy)
                del o[0]



# Example trapper bot that places a barrier randomly:

class trapper_bot:

    path = []
    turn = 0

    def __init__(self):
        # You can define global states (that last between moves) here
        pass

    def find_scotty(self, board):
        # Helper function that finds Scotty's location on the board
        for y in range(15):
            for x in range(15):
                if board[y][x] == 1:
                    return (x, y)

    def count(self, board, mode, x, y):
        blockades = 0
        # Check up
        if x < 0 or x > 14 or y < 0 or y > 14:
            return 0
        if mode == 'u':
            for i in range(y+1, 15):
                for j in range(15):
                    if board[i][j] > 1:
                        blockades += 1
        # Check down
        elif mode == 'd':
            for i in range(0, y):
                for j in range(15):
                    if board[i][j] > 1:
                        blockades += 1
        # Check left
        elif mode == 'l':
            for i in range(15):
                for j in range(0, x):
                    if board[i][j] > 1:
                        blockades += 1
        # Check right
        elif mode == 'r':
            for i in range(15):
                for j in range(x+1, 15):
                    if board[i][j] > 1:
                        blockades += 1
        # Check around
        elif mode == 'o':
            xl = x-1
            xh = x+2
            yl = y-1
            yh = y+2
            if yl < 0:
                yl = y
            if yh > 15:
                yh = y+1
            if xl < 0:
                xl = x
            if xh > 15:
                xh = x+1
            for i in range(yl, yh):
                for j in range(xl, xh):
                    if board[i][j] > 1:
                        blockades += 1
        return blockades

    def move(self, board):
        # You should write your code that moves every turn here
        # This is the placing them randomly, provided by the starter code
        # moves = [(x, y) for x in range(15) for y in range(15)]
        # while moves:
        #     x, y = moves.pop(random.randrange(len(moves)))
        #     if board[y][x] == 0:
        #         return (x, y)
        # return (0, 0)

        # *** UNFINISHED***
        # Strategy1: Find where Scotty is mostly heading and block in that direction
        # Make sure to block where block touches at least 2 sides (optimal position), 1 is ok, 0 is useless
        x, y = self.find_scotty(board)
        self.path.append((x,y))
        direction = []
        if self.turn == 0:
            direction.append([self.count(board, 'u', 7, 7), 0])
            direction.append([self.count(board, 'd', 7, 7), 1])
            direction.append([self.count(board, 'l', 7, 7), 2])
            direction.append([self.count(board, 'r', 7, 7), 3])
            table = [[(7,14),(1,0)],[(7,0),(0,1)],[(0,7),(1,0)],[(14,7),(0,1)]]
            direction.sort()
            for d in direction:
                dx = table[d][0][0]
                dy = table[d][0][1]
                mx = table[d][1][0]
                my = table[d][1][1]
                if board[dy][dx] == 0:
                    return (dx, dy)
                for i in range(1, 8):
                    if board[dy + i*my][dx + i*mx] == 0:
                        return (dx + i*mx, dy + i*my)
                    if board[dy - i*my][dx - i*mx] == 0:
                        return (dx - i*mx, dy - i*my)
        sdir = 0
        



#=============================================================================

# Local testing parameters

# If you would like to view a turn by turn game display while testing locally,
# set this parameter to True

LOCAL_VIEW = True

# Sample board your game will be run on (flipped vertically)
# This file will display 0 as ' ', 1 as '*', 2 as 'X', and 3 as 'O'

SAMPLE_BOARD = [
    [0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 0, 0, 2, 2, 2],
    [0, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 2, 0, 0, 2, 0, 2, 2, 0, 0, 2, 0, 2, 0, 2],
    [0, 0, 2, 2, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 2],
    [0, 2, 0, 2, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 2, 0, 2, 2, 2, 0, 2, 0, 0],
    [2, 2, 0, 2, 2, 2, 0, 1, 0, 0, 2, 0, 0, 2, 0],
    [2, 2, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0],
    [2, 0, 0, 0, 2, 0, 2, 2, 0, 2, 0, 2, 2, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 0, 2],
    [0, 2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 2, 2, 0, 2, 0]]

#=============================================================================












































# You don't need to change any code below this point

import json
import sys

def WAIT():
    return json.loads(input())

def SEND(data):
    print(json.dumps(data), flush=True)

def dispboard_for_tester(board):
    print()
    print('\n'.join(''.join(map(lambda x:' *XO'[x],i))for i in reversed(board)))
    print()

def find_scotty_for_tester(board):
    for y in range(15):
        for x in range(15):
            if board[y][x] == 1:
                return (x, y)

def trapped_for_tester(board):
    pos = find_scotty_for_tester(board)
    moves = [*zip([0,1,1,1,0,-1,-1,-1],[1,1,0,-1,-1,-1,0,1])]
    trap = True
    for i in moves:
        if 0 <= pos[0] + i[0] < 15 and 0 <= pos[1] + i[1] < 15:
            if board[pos[1] + i[1]][pos[0] + i[0]] == 0:
                trap = False
                break
        else:
            trap = False
            break
    return trap

def PLAY(scotty, trapper, board):
    result = -1
    while True:
        try:
            val = trapper.move(board)
            if not (val[0] == int(val[0]) and 0 <= val[0] < 15
                and val[1] == int(val[1]) and 0 <= val[1] < 15
                and board[val[1]][val[0]] == 0):
                raise Exception('invalid move')
            board[val[1]][val[0]] = 3
        except Exception as e:
            print(f'Your trapper has an error: {e}! Doing nothing instead.')
            val = -1
        if trapped_for_tester(board):
            result = 1
            break
        if LOCAL_VIEW:
            dispboard_for_tester(board)
            input("Enter to continue (change LOCAL_VIEW to toggle this)")
        try:
            val = scotty.move(board)
            if not (val[0] == int(val[0]) and -1 <= val[0] <= 1
                and val[1] == int(val[1]) and -1 <= val[1] <= 1):
                    raise Exception('invalid move')
        except Exception as e:
            print(f'Your Scotty has an error: {e}! Doing nothing instead.')
            val = (0, 0)
        pos = find_scotty_for_tester(board)
        if 0 <= pos[0] + val[0] < 15 and 0 <= pos[1] + val[1] < 15:
            if board[pos[1] + val[1]][pos[0] + val[0]] == 0:
                board[pos[1] + val[1]][pos[0] + val[0]] = 1
                board[pos[1]][pos[0]] = 0
        else:
            board[pos[1]][pos[0]] = 0
            result = 0
            break
        if LOCAL_VIEW:
            dispboard_for_tester(board)
            input("Enter to continue (change LOCAL_VIEW to toggle this)")
    print(["Scotty", "Trapper"][result], "won!")
    if not LOCAL_VIEW:
        print("Change LOCAL_VIEW to True to see a turn by turn replay")

if len(sys.argv) < 2 or sys.argv[1] != 'REAL':
    PLAY(scotty_bot(), trapper_bot(), SAMPLE_BOARD)
    input()

else:
    scotty = scotty_bot()
    trapper = trapper_bot()
    while True:
        data = WAIT()
        board = data["board"]
        role = data["role"]
        if role == "trapper":
            SEND(trapper.move(board))
        else:
            SEND(scotty.move(board))
