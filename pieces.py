#===============================================================================
# Developer: Vishnu Pathmanaban
# Email: vpathman@andrew.cmu.edu
#===============================================================================
# File Description: Piece Classes
#===============================================================================

#graphics framework from CMU 15-112
#https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import math, random, copy

#alias-breaking deepcopy from CMU 15-112
#https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
def myDeepCopy(a):
    if (isinstance(a, list) or isinstance(a, tuple)):
        return [myDeepCopy(element) for element in a]
    else:
        return copy.copy(a)

#modified print 2D list from CMU 15-112
#https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing
def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

def print2dList(a):
    if (a == []):
        print([])
        return
    rows = len(a)
    cols = len(a[0])
    fieldWidth = maxItemLength(a)
    print("[ ", end="")
    for row in range(rows):
        if (row > 0): print("\n  ", end="")
        print("[ ", end="")
        for col in range(cols):
            if (col > 0): print(", ", end="")
            formatSpec = "%" + str(fieldWidth) + "s"
            if a[row][col] == None:
                item = ''
            else:
                item = a[row][col]
            print(formatSpec % str(item), end="")
        print(" ]", end="")
    print("]")

#===============================================================================

class Piece(object):
    def __init__(self, black, position, spritestrip, size):
        self.size = size
        self.black = black
        self.position = position
        self.sprite = spritestrip.crop((0, 0, self.size, self.size))

    def draw(self, canvas):
        x = self.position[1]*self.size + self.size//2
        y = self.position[0]*self.size + self.size//2
        canvas.create_image(x, y, image=ImageTk.PhotoImage(self.sprite))

class Rook(Piece):
    def __init__(self, black, position, spritestrip, size):
        super().__init__(black, position, spritestrip, size)
        if(self.black):
            self.sprite = spritestrip.crop((0*self.size, 1*self.size,
                                            1*self.size, 2*self.size))
        else:
            self.sprite = spritestrip.crop((0*self.size, 0*self.size,
                                            1*self.size, 1*self.size))
        self.value = 50

    def __eq__(self, other):
        return (isinstance(other, Rook) and self.black==other.black
                and self.position==other.position)

    def __repr__(self):
        if(self.black):
            return f'BR'
        else:
            return f'WR'

    def legalMoves(self, board):
        legalMoves=set()
        oldRow=self.position[0]
        oldCol=self.position[1]
        #right
        target=[oldRow, oldCol+1]
        while target[1]<=7 and board[target[0]][target[1]]==None:
            legalMoves.add((target[0],target[1]))
            target[1]+=1
        if target[1]<=7 and board[target[0]][target[1]].black!=self.black:
            legalMoves.add((target[0],target[1]))
        #left
        target=[oldRow, oldCol-1]
        while target[1]>=0 and board[target[0]][target[1]]==None:
            legalMoves.add((target[0],target[1]))
            target[1]-=1
        if target[1]>=0 and board[target[0]][target[1]].black!=self.black:
            legalMoves.add((target[0],target[1]))
        #down
        target=[oldRow+1, oldCol]
        while target[0]<=7 and board[target[0]][target[1]]==None:
            legalMoves.add((target[0],target[1]))
            target[0]+=1
        if target[0]<=7 and board[target[0]][target[1]].black!=self.black:
            legalMoves.add((target[0],target[1]))
        #up
        target=[oldRow-1, oldCol]
        while target[0]>=0 and board[target[0]][target[1]]==None:
            legalMoves.add((target[0],target[1]))
            target[0]-=1
        if target[0]>=0 and board[target[0]][target[1]].black!=self.black:
            legalMoves.add((target[0],target[1]))
        return legalMoves
        
class Knight(Piece):
    def __init__(self, black, position, spritestrip, size):
        super().__init__(black, position, spritestrip, size)
        if(self.black):
            self.sprite = spritestrip.crop((1*self.size, 1*self.size,
                                            2*self.size, 2*self.size))
        else:
            self.sprite = spritestrip.crop((1*self.size, 0*self.size,
                                            2*self.size, 1*self.size))
        self.value = 30

    def __eq__(self, other):
        return (isinstance(other, Knight) and self.black==other.black
                and self.position==other.position)

    def __repr__(self):
        if(self.black):
            return f'BN'
        else:
            return f'WN'

    def legalMoves(self, board):
        legalMoves=set()
        oldRow=self.position[0]
        oldCol=self.position[1]
        moves = {(2,1),(1,2),(2,-1),(1,-2),(-2,1),(-1,2),(-2,-1),(-1,-2)}
        for move in moves:
            targetRow = oldRow+move[0]
            targetCol = oldCol+move[1]
            if (targetRow>=0 and targetRow<=7 and targetCol>=0 and targetCol<=7
                and (board[targetRow][targetCol] == None
                or board[targetRow][targetCol].black != self.black)):
                legalMoves.add((targetRow,targetCol))
        return legalMoves
    
class Bishop(Piece):
    def __init__(self, black, position, spritestrip, size):
        super().__init__(black, position, spritestrip, size)
        if(self.black):
            self.sprite = spritestrip.crop((2*self.size, 1*self.size,
                                            3*self.size, 2*self.size))
        else:
            self.sprite = spritestrip.crop((2*self.size, 0*self.size,
                                            3*self.size, 1*self.size))
        self.value = 30

    def __eq__(self, other):
        return (isinstance(other, Bishop) and self.black==other.black
                and self.position==other.position)

    def __repr__(self):
        if(self.black):
            return f'BB'
        else:
            return f'WB'

    def legalMoves(self, board):
        legalMoves=set()
        oldRow=self.position[0]
        oldCol=self.position[1]
        #up&right diagonal
        target=[oldRow-1, oldCol+1]
        while (target[0]>=0 and target[1]<=7 and
               board[target[0]][target[1]]==None):
            legalMoves.add((target[0],target[1]))
            target[0]-=1
            target[1]+=1
        if (target[0]>=0 and target[1]<=7 and
            board[target[0]][target[1]].black!=self.black):
            legalMoves.add((target[0],target[1]))
        #down&left diagonal
        target=[oldRow+1, oldCol-1]
        while (target[0]<=7 and target[1]>=0 and
               board[target[0]][target[1]]==None):
            legalMoves.add((target[0],target[1]))
            target[0]+=1
            target[1]-=1
        if (target[0]<=7 and target[1]>=0 and
            board[target[0]][target[1]].black!=self.black):
            legalMoves.add((target[0],target[1]))
        #up&left diagonal
        target=[oldRow-1, oldCol-1]
        while (target[0]>=0 and target[1]>=0 and
               board[target[0]][target[1]]==None):
            legalMoves.add((target[0],target[1]))
            target[0]-=1
            target[1]-=1
        if (target[0]>=0 and target[1]>=0 and
            board[target[0]][target[1]].black!=self.black):
            legalMoves.add((target[0],target[1]))
        #down&right diagonal
        target=[oldRow+1, oldCol+1]
        while (target[0]<=7 and target[1]<=7 and
               board[target[0]][target[1]]==None):
            legalMoves.add((target[0],target[1]))
            target[0]+=1
            target[1]+=1
        if (target[0]<=7 and target[1]<=7 and
            board[target[0]][target[1]].black!=self.black):
            legalMoves.add((target[0],target[1]))
        return legalMoves
    
class Queen(Piece):
    def __init__(self, black, position, spritestrip, size):
        super().__init__(black, position, spritestrip, size)
        if(self.black):
            self.sprite = spritestrip.crop((3*self.size, 1*self.size,
                                            4*self.size, 2*self.size))
        else:
            self.sprite = spritestrip.crop((3*self.size, 0*self.size,
                                            4*self.size, 1*self.size))
        self.value = 90

    def __eq__(self, other):
        return (isinstance(other, Queen) and self.black==other.black
                and self.position==other.position)

    def __repr__(self):
        if(self.black):
            return f'BQ'
        else:
            return f'WQ'

    def legalMoves(self, board):
        legalMoves=set()
        oldRow=self.position[0]
        oldCol=self.position[1]
        #right
        target=[oldRow, oldCol+1]
        while target[1]<=7 and board[target[0]][target[1]]==None:
            legalMoves.add((target[0],target[1]))
            target[1]+=1
        if target[1]<=7 and board[target[0]][target[1]].black!=self.black:
            legalMoves.add((target[0],target[1]))
        #left
        target=[oldRow, oldCol-1]
        while target[1]>=0 and board[target[0]][target[1]]==None:
            legalMoves.add((target[0],target[1]))
            target[1]-=1
        if target[1]>=0 and board[target[0]][target[1]].black!=self.black:
            legalMoves.add((target[0],target[1]))
        #down
        target=[oldRow+1, oldCol]
        while target[0]<=7 and board[target[0]][target[1]]==None:
            legalMoves.add((target[0],target[1]))
            target[0]+=1
        if target[0]<=7 and board[target[0]][target[1]].black!=self.black:
            legalMoves.add((target[0],target[1]))
        #up
        target=[oldRow-1, oldCol]
        while target[0]>=0 and board[target[0]][target[1]]==None:
            legalMoves.add((target[0],target[1]))
            target[0]-=1
        if target[0]>=0 and board[target[0]][target[1]].black!=self.black:
            legalMoves.add((target[0],target[1]))
        #up&right diagonal
        target=[oldRow-1, oldCol+1]
        while (target[0]>=0 and target[1]<=7 and
               board[target[0]][target[1]]==None):
            legalMoves.add((target[0],target[1]))
            target[0]-=1
            target[1]+=1
        if (target[0]>=0 and target[1]<=7 and
            board[target[0]][target[1]].black!=self.black):
            legalMoves.add((target[0],target[1]))
        #down&left diagonal
        target=[oldRow+1, oldCol-1]
        while (target[0]<=7 and target[1]>=0 and
               board[target[0]][target[1]]==None):
            legalMoves.add((target[0],target[1]))
            target[0]+=1
            target[1]-=1
        if (target[0]<=7 and target[1]>=0 and
            board[target[0]][target[1]].black!=self.black):
            legalMoves.add((target[0],target[1]))
        #up&left diagonal
        target=[oldRow-1, oldCol-1]
        while (target[0]>=0 and target[1]>=0 and
               board[target[0]][target[1]]==None):
            legalMoves.add((target[0],target[1]))
            target[0]-=1
            target[1]-=1
        if (target[0]>=0 and target[1]>=0 and
            board[target[0]][target[1]].black!=self.black):
            legalMoves.add((target[0],target[1]))
        #down&right diagonal
        target=[oldRow+1, oldCol+1]
        while (target[0]<=7 and target[1]<=7 and
               board[target[0]][target[1]]==None):
            legalMoves.add((target[0],target[1]))
            target[0]+=1
            target[1]+=1
        if (target[0]<=7 and target[1]<=7 and
            board[target[0]][target[1]].black!=self.black):
            legalMoves.add((target[0],target[1]))
        return legalMoves

class King(Piece):
    def __init__(self, black, position, spritestrip, size):
        super().__init__(black, position, spritestrip, size)
        if(self.black):
            self.sprite = spritestrip.crop((4*self.size, 1*self.size,
                                            5*self.size, 2*self.size))
        else:
            self.sprite = spritestrip.crop((4*self.size, 0*self.size,
                                            5*self.size, 1*self.size))
        self.value = 900

    def __eq__(self, other):
        return (isinstance(other, King) and self.black==other.black
                and self.position==other.position)

    def __repr__(self):
        if(self.black):
            return f'BK'
        else:
            return f'WK'

    def legalMoves(self, board):
        legalMoves=set()
        oldRow=self.position[0]
        oldCol=self.position[1]
        moves = {(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)}
        for move in moves:
            targetRow = oldRow+move[0]
            targetCol = oldCol+move[1]
            if (targetRow>=0 and targetRow<=7 and targetCol>=0 and targetCol<=7
                and (board[targetRow][targetCol] == None
                or board[targetRow][targetCol].black != self.black)):
                legalMoves.add((targetRow,targetCol))
        return legalMoves

class Pawn(Piece):
    def __init__(self, black, position, spritestrip, size):
        super().__init__(black, position, spritestrip, size)
        if(self.black):
            self.sprite = spritestrip.crop((5*self.size, 1*self.size,
                                            6*self.size, 2*self.size))
        else:
            self.sprite = spritestrip.crop((5*self.size, 0*self.size,
                                            6*self.size, 1*self.size))
        self.value = 10

    def __eq__(self, other):
        return (isinstance(other, Pawn) and self.black==other.black
                and self.position==other.position)

    def __repr__(self):
        if(self.black):
            return f'BP'
        else:
            return f'WP'

    def legalMoves(self, board):
        legalMoves=set()
        oldRow=self.position[0]
        oldCol=self.position[1]
        if(self.black):
            moves = {(1,1),(1,-1)}
            for move in moves:
                targetRow = oldRow+move[0]
                targetCol = oldCol+move[1]
                if (targetRow>=0 and targetRow<=7
                    and targetCol>=0 and targetCol<=7
                    and board[targetRow][targetCol] != None and
                    board[targetRow][targetCol].black != self.black):
                    legalMoves.add((targetRow,targetCol))
            targetRow = oldRow+1
            targetCol = oldCol
            if (targetRow>=0 and targetRow<=7
                and targetCol>=0 and targetCol<=7
                and board[targetRow][targetCol] == None):
                legalMoves.add((targetRow,targetCol))
            if(oldRow==1):
                targetRow = oldRow+2
                targetCol = oldCol
                if (targetRow>=0 and targetRow<=7
                    and targetCol>=0 and targetCol<=7
                    and board[targetRow][targetCol] == None
                    and board[targetRow-1][targetCol] == None):
                    legalMoves.add((targetRow,targetCol))             
        else:
            moves = {(-1,1),(-1,-1)}
            for move in moves:
                targetRow = oldRow+move[0]
                targetCol = oldCol+move[1]
                if (targetRow>=0 and targetRow<=7
                    and targetCol>=0 and targetCol<=7
                    and board[targetRow][targetCol] != None and
                    board[targetRow][targetCol].black != self.black):
                    legalMoves.add((targetRow,targetCol))
            targetRow = oldRow-1
            targetCol = oldCol
            if (targetRow>=0 and targetRow<=7
                and targetCol>=0 and targetCol<=7
                and board[targetRow][targetCol] == None):
                legalMoves.add((targetRow,targetCol))
            if(oldRow==6):
                targetRow = oldRow-2
                targetCol = oldCol
                if (targetRow>=0 and targetRow<=7
                    and targetCol>=0 and targetCol<=7
                    and board[targetRow][targetCol] == None
                    and board[targetRow+1][targetCol] == None):
                    legalMoves.add((targetRow,targetCol))  
        return legalMoves

#===============================================================================
