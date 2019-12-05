#===============================================================================
# Developer: Vishnu Pathmanaban
# Email: vpathman@andrew.cmu.edu
#===============================================================================

'''
(Only used tkinter and pillow)
KEY FEATURES:
1. Menu user interface
2. Chess user interface
3. Highlights legal chess moves for beginners
4. Player versus player mode
5. Check and checkmate detection
6. Player versus custom AI mode
7. AI difficulty
8. Advice function
9. Advice explanation display
10. Scalable GUI for different devices
'''

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

class Board(object):
    #creates board
    def __init__(self, spritestrip, scale):
        self.size = int(132*scale)
        self.selected = (-1,-1)
        self.advice = []
        self.board = [[None] * 8 for i in range(8)]
        for i in range(8):
            self.board[1][i] = Pawn(True, (1,i), spritestrip, self.size)
            self.board[6][i] = Pawn(False, (6,i), spritestrip, self.size)
        self.board[0][0] = Rook(True, (0,0), spritestrip, self.size)
        self.board[7][0] = Rook(False, (7,0), spritestrip, self.size)
        self.board[0][1] = Knight(True, (0,1), spritestrip, self.size)
        self.board[7][1] = Knight(False, (7,1), spritestrip, self.size)
        self.board[0][2] = Bishop(True, (0,2), spritestrip, self.size)
        self.board[7][2] = Bishop(False, (7,2), spritestrip, self.size)
        self.board[0][3] = Queen(True, (0,3), spritestrip, self.size)
        self.board[7][3] = Queen(False, (7,3), spritestrip, self.size)
        self.board[0][4] = King(True, (0,4), spritestrip, self.size)
        self.board[7][4] = King(False, (7,4), spritestrip, self.size)
        self.board[0][5] = Bishop(True, (0,5), spritestrip, self.size)
        self.board[7][5] = Bishop(False, (7,5), spritestrip, self.size)
        self.board[0][6] = Knight(True, (0,6), spritestrip, self.size)
        self.board[7][6] = Knight(False, (7,6), spritestrip, self.size)
        self.board[0][7] = Rook(True, (0,7), spritestrip, self.size)
        self.board[7][7] = Rook(False, (7,7), spritestrip, self.size)
        self.blackKingPosition = (0,4)
        self.whiteKingPosition = (7,4)

    def __eq__(self, other):
        if isinstance(other, Board):
            equal = True
            for row in range(8):
                for col in range(8):
                    if(self.board[row][col]!=other.board[row][col]):
                        equal = False
        return isinstance(other, Board) and equal

    def __repr__(self):
        return str(print2dList(self.board))

    #determines if either king is in check 
    def check(self):
        for row in range(8):
            for col in range(8):
                item = self.board[row][col]
                if(item != None):
                    if(item.black and
                       self.whiteKingPosition in item.legalMoves(self.board)):
                        return 'white'
                    elif(self.blackKingPosition in item.legalMoves(self.board)):
                        return 'black'
        return 'none'

    #determines selected cell
    def cellSelection(self, x, y):
        for row in range(8):
            for col in range(8):
                x1 = col*self.size
                y1 = row*self.size
                x2 = col*self.size+self.size
                y2 = row*self.size+self.size
                if (x>x1 and x<x2 and y>y1 and y<y2):
                    self.selected = (row,col)

    #draws board
    def draw(self, canvas):
        for row in range(8):
            for col in range(8):
                x1 = col*self.size
                y1 = row*self.size
                x2 = col*self.size+self.size
                y2 = row*self.size+self.size
                if (row+col)%2==0:
                    canvas.create_rectangle(x1,y1,x2,y2,fill='white')
                else:
                    canvas.create_rectangle(x1,y1,x2,y2,fill='maroon')
                if self.board[row][col]!=None:
                    self.board[row][col].draw(canvas)
                if (row,col)==self.selected:
                    width=10*(self.size/132)
                    canvas.create_rectangle(x1+width//2,y1+width//2,
                                            x2-width//2,y2-width//2,
                                            outline='gold',width=width)
                if (row,col) in self.advice:
                    width=10*(self.size/132)
                    canvas.create_rectangle(x1+width//2,y1+width//2,
                                            x2-width//2,y2-width//2,
                                            outline='blue',width=width)

    #highlights legal moves in green                
    def drawLegalMoves(self, piece, canvas):
        moves = piece.legalMoves(self.board)
        for move in moves:
            row = move[0]
            col = move[1]
            x1 = col*self.size
            y1 = row*self.size
            x2 = col*self.size+self.size
            y2 = row*self.size+self.size
            width=10*(self.size/132)
            canvas.create_rectangle(x1+width//2,y1+width//2,
                                    x2-width//2,y2-width//2,
                                    outline='green',width=width)

#===============================================================================

    #check test
    def checkTest(self, spritestrip):
        self.selected = (-1,-1)
        self.advice = []
        self.board = [[None] * 8 for i in range(8)]
        for i in range(8):
            self.board[1][i] = Pawn(True, (1,i), spritestrip, self.size)
            self.board[6][i] = Pawn(False, (6,i), spritestrip, self.size)
        self.board[0][0] = Rook(True, (0,0), spritestrip, self.size)
        self.board[7][0] = Rook(False, (7,0), spritestrip, self.size)
        self.board[0][1] = Knight(True, (0,1), spritestrip, self.size)
        self.board[7][1] = Knight(False, (7,1), spritestrip, self.size)
        self.board[0][2] = Bishop(True, (0,2), spritestrip, self.size)
        self.board[7][2] = Bishop(False, (7,2), spritestrip, self.size)
        self.board[0][3] = Queen(True, (0,3), spritestrip, self.size)
        self.board[7][3] = Queen(False, (7,3), spritestrip, self.size)
        self.board[0][4] = King(True, (0,4), spritestrip, self.size)
        self.board[7][4] = King(False, (7,4), spritestrip, self.size)
        self.board[0][5] = Bishop(True, (0,5), spritestrip, self.size)
        self.board[7][5] = Bishop(False, (7,5), spritestrip, self.size)
        self.board[0][6] = Knight(True, (0,6), spritestrip, self.size)
        self.board[7][6] = Knight(False, (7,6), spritestrip, self.size)
        self.board[0][7] = Rook(True, (0,7), spritestrip, self.size)
        self.board[7][7] = Rook(False, (7,7), spritestrip, self.size)
        self.blackKingPosition = (0,4)
        self.whiteKingPosition = (7,4)
        self.board[1][5] = None
        self.board[6][4] = None

    #checkmate test
    def checkmateTest(self, spritestrip):
        self.selected = (-1,-1)
        self.advice = []
        self.board = [[None] * 8 for i in range(8)]
        for i in range(8):
            self.board[1][i] = Pawn(True, (1,i), spritestrip, self.size)
            self.board[6][i] = Pawn(False, (6,i), spritestrip, self.size)
        self.board[0][0] = Rook(True, (0,0), spritestrip, self.size)
        self.board[7][0] = Rook(False, (7,0), spritestrip, self.size)
        self.board[0][1] = Knight(True, (0,1), spritestrip, self.size)
        self.board[7][1] = Knight(False, (7,1), spritestrip, self.size)
        self.board[0][2] = Bishop(True, (0,2), spritestrip, self.size)
        self.board[7][2] = Bishop(False, (7,2), spritestrip, self.size)
        self.board[0][3] = Queen(True, (0,3), spritestrip, self.size)
        self.board[7][3] = Queen(False, (7,3), spritestrip, self.size)
        self.board[0][4] = King(True, (0,4), spritestrip, self.size)
        self.board[7][4] = King(False, (7,4), spritestrip, self.size)
        self.board[0][5] = Bishop(True, (0,5), spritestrip, self.size)
        self.board[7][5] = Bishop(False, (7,5), spritestrip, self.size)
        self.board[0][6] = Knight(True, (0,6), spritestrip, self.size)
        self.board[7][6] = Knight(False, (7,6), spritestrip, self.size)
        self.board[0][7] = Rook(True, (0,7), spritestrip, self.size)
        self.board[7][7] = Rook(False, (7,7), spritestrip, self.size)
        self.blackKingPosition = (0,4)
        self.whiteKingPosition = (7,4)
        self.board[1][5] = None
        self.board[1][6] = None
        self.board[6][4] = None

    #AI test
    def AITest(self, spritestrip):
        self.selected = (-1,-1)
        self.advice = []
        self.board = [[None] * 8 for i in range(8)]
        for i in range(8):
            self.board[1][i] = Pawn(True, (1,i), spritestrip, self.size)
            self.board[6][i] = Pawn(False, (6,i), spritestrip, self.size)
        self.board[0][0] = Rook(True, (0,0), spritestrip, self.size)
        self.board[7][0] = Rook(False, (7,0), spritestrip, self.size)
        self.board[0][1] = Knight(True, (0,1), spritestrip, self.size)
        self.board[7][1] = Knight(False, (7,1), spritestrip, self.size)
        self.board[0][2] = Bishop(True, (0,2), spritestrip, self.size)
        self.board[3][6] = Bishop(False, (3,6), spritestrip, self.size)
        self.board[0][3] = Queen(True, (0,3), spritestrip, self.size)
        self.board[7][2] = Queen(False, (7,2), spritestrip, self.size)
        self.board[0][4] = King(True, (0,4), spritestrip, self.size)
        self.board[7][4] = King(False, (7,4), spritestrip, self.size)
        self.board[0][5] = Bishop(True, (0,5), spritestrip, self.size)
        self.board[7][5] = Bishop(False, (7,5), spritestrip, self.size)
        self.board[0][6] = Knight(True, (0,6), spritestrip, self.size)
        self.board[7][6] = Knight(False, (7,6), spritestrip, self.size)
        self.board[0][7] = Rook(True, (0,7), spritestrip, self.size)
        self.board[7][7] = Rook(False, (7,7), spritestrip, self.size)
        self.blackKingPosition = (0,4)
        self.whiteKingPosition = (7,4)
        self.board[1][4] = None
        self.board[6][3] = None
        self.board[1][7] = None

    #advice explanation test
    def explanationTest(self, spritestrip):
        self.selected = (-1,-1)
        self.advice = []
        self.board = [[None] * 8 for i in range(8)]
        for i in range(8):
            self.board[1][i] = Pawn(True, (1,i), spritestrip, self.size)
            self.board[6][i] = Pawn(False, (6,i), spritestrip, self.size)
        self.board[0][0] = Rook(True, (0,0), spritestrip, self.size)
        self.board[7][0] = Rook(False, (7,0), spritestrip, self.size)
        self.board[0][1] = Knight(True, (0,1), spritestrip, self.size)
        self.board[7][1] = Knight(False, (7,1), spritestrip, self.size)
        self.board[0][2] = Bishop(True, (0,2), spritestrip, self.size)
        self.board[7][2] = Bishop(False, (7,2), spritestrip, self.size)
        self.board[0][4] = Queen(True, (0,4), spritestrip, self.size)
        self.board[7][3] = Queen(False, (7,3), spritestrip, self.size)
        self.board[0][3] = King(True, (0,3), spritestrip, self.size)
        self.board[7][4] = King(False, (7,4), spritestrip, self.size)
        self.board[3][7] = Bishop(True, (3,7), spritestrip, self.size)
        self.board[7][5] = Bishop(False, (7,5), spritestrip, self.size)
        self.board[0][6] = Knight(True, (0,6), spritestrip, self.size)
        self.board[7][6] = Knight(False, (7,6), spritestrip, self.size)
        self.board[0][7] = Rook(True, (0,7), spritestrip, self.size)
        self.board[7][7] = Rook(False, (7,7), spritestrip, self.size)
        self.blackKingPosition = (0,3)
        self.whiteKingPosition = (7,4)
        self.board[1][5] = None
        self.board[1][6] = None
        self.board[6][4] = None
        
#===============================================================================

class PvP(Mode):
    #model
    def appStarted(mode):
        scale = (mode.app.width-(mode.app.width//16))/1056
        #image from http://i.imgur.com/zwF4Lyn.png
        url = 'http://i.imgur.com/zwF4Lyn.png'
        spritestrip = mode.loadImage(url)
        mode.scaledSpritestrip = mode.scaleImage(spritestrip, scale)
        mode.board = Board(mode.scaledSpritestrip, scale)
        mode.selectedPiece = None
        mode.blackTurn = False
        mode.checkExists = False
        mode.message = 'WHITE MAY MOVE'
        mode.columns = ['A','B','C','D','E','F','G','H']
        mode.rows = ['8','7','6','5','4','3','2','1']
        mode.gameOver = False
        
    #player moves
    def mousePressed(mode, event):
        mode.board.advice = []
        mode.board.cellSelection(event.x, event.y)
        row = mode.board.selected[0]
        col = mode.board.selected[1]
        if (mode.selectedPiece == None):
            mode.selectedPiece = mode.board.board[row][col]
        else:
            if(mode.selectedPiece.black==mode.blackTurn and
            (row,col) in mode.selectedPiece.legalMoves(mode.board.board)):
                PvP.completeLegalMove(mode, row, col)
                if mode.blackTurn:
                    mode.message = 'BLACK MAY MOVE'
                else:
                    mode.message = 'WHITE MAY MOVE'
            #checkmate display
            PvP.checkmateDetection(mode, mode.blackTurn)
            #remove selection
            mode.board.selected = (-1,-1)
            mode.selectedPiece = None

    #updates positions
    def updatePositions(mode):
        for row in range(8):
            for col in range(8):
                item = mode.board.board[row][col]
                if(item != None):
                    item.position = (row,col)
                    if isinstance(item, King):
                        if item.black:
                            mode.board.blackKingPosition = (row,col)
                        else:
                            mode.board.whiteKingPosition = (row,col)

    #moves piece if legal by chess laws 
    def completeLegalMove(mode, row, col):
        tempPiece = mode.board.board[row][col]
        (oldRow, oldCol) = mode.selectedPiece.position
        PvP.movePiece(mode, row, col, oldRow, oldCol)
        #new check
        if(mode.board.check()!='none' and mode.checkExists==False):
            #check on player moving currently
            if((mode.board.check()=='black' and mode.blackTurn) or
               (mode.board.check()=='white' and mode.blackTurn==False)):
                PvP.revertMove(mode, row, col, oldRow, oldCol,
                                    tempPiece)
            #check on opponent
            else:
                mode.checkExists = True
                PvP.switchTurns(mode)
        #existing check not removed
        elif(mode.board.check()!='none' and mode.checkExists==True):
            PvP.revertMove(mode, row, col, oldRow, oldCol,
                                    tempPiece)
        #chess legal move
        else:
            mode.checkExists = False
            PvP.switchTurns(mode)

    #moves piece 
    def movePiece(mode, row, col, oldRow, oldCol):
        mode.board.board[oldRow][oldCol] = None
        mode.board.board[row][col] = mode.selectedPiece
        mode.selectedPiece.position = (row,col)
        if isinstance(mode.selectedPiece, King):
            if mode.blackTurn:
                mode.board.blackKingPosition = (row,col)
            else:
                mode.board.whiteKingPosition = (row,col)

    #reverts move
    def revertMove(mode, row, col, oldRow, oldCol, tempPiece):
        mode.selectedPiece.position = (oldRow, oldCol)
        mode.board.board[oldRow][oldCol] = mode.selectedPiece
        mode.board.board[row][col] = tempPiece
        if isinstance(mode.selectedPiece, King):
            if mode.blackTurn:
                mode.board.blackKingPosition = (oldRow,oldCol)
            else:
                mode.board.whiteKingPosition = (oldRow,oldCol)

    #switches turn                
    def switchTurns(mode):
        if mode.blackTurn:
            mode.blackTurn = False
        else:
            mode.blackTurn = True

    #updates check status
    def checkUpdate(mode):
        if(mode.board.check() == 'none'):
            mode.checkExists = False
        else:
            mode.checkExists = True
                
    #key control
    def keyPressed(mode, event):
        #reset
        if event.key == 'r':
            PvP.appStarted(mode)
        #menu function
        if event.key == 'm':
            PvP.appStarted(mode)
            mode.app.setActiveMode(mode.app.mainMenu)
        #advice function
        if event.key == 'a' and mode.gameOver == False:
            PvAI.giveAdvice(mode, mode.blackTurn)
        #clear
        if event.key == 'c':
            mode.message = ''
            mode.board.selected = (-1,-1)
            mode.board.advice = []
        #check test case
        if event.key == '1':
            mode.board.checkTest(mode.scaledSpritestrip)
            PvP.updatePositions(mode)
            PvP.checkUpdate(mode)
        #checkmate test case
        if event.key == '2':
            mode.board.checkmateTest(mode.scaledSpritestrip)
            PvP.updatePositions(mode)
            PvP.checkUpdate(mode)
        #AI test case
        if event.key == '3':
            mode.board.AITest(mode.scaledSpritestrip)
            PvP.updatePositions(mode)
            PvP.checkUpdate(mode)
        #explanation test case
        if event.key == '4':
            mode.board.explanationTest(mode.scaledSpritestrip)
            PvP.updatePositions(mode)
            PvP.checkUpdate(mode)

    #checkmate detection
    def checkmateDetection(mode, blackSide):
        possibleBoards = PvAI.boardGeneration(mode, blackSide)
        if len(possibleBoards) == 0:
            mode.gameOver = True
            if blackSide:
                mode.message = 'WHITE WINS. PRESS M FOR NEW GAME.'
            else:
                mode.message = 'BLACK WINS. PRESS M FOR NEW GAME.'

    #drawPositionKeys
    def drawPositionKeys(mode, canvas):
        for index in range(len(mode.columns)):
            canvas.create_text(((((mode.width-(mode.width//17))//8)*index)+
                                ((mode.width-(mode.width//17))//8)*0.5),
                                mode.height-(mode.height//5),
                                text = mode.columns[index], fill = 'white',
                                font = f'Times {mode.width//100}')
            canvas.create_text(mode.width-(mode.width//17),
                               ((((mode.height-(mode.height//5))//8)*index)+
                                ((mode.height-(mode.height//5))//8)*0.5),
                                text = mode.rows[index], fill = 'white',
                                font = f'Times {mode.width//100}')
    #view
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,
                                fill='maroon',outline='black',
                                width=mode.width//100)
        mode.board.draw(canvas)
        PvP.drawPositionKeys(mode, canvas)
        canvas.create_text(mode.width/2, mode.height*9//10,
                           text=mode.message,
                           fill='white', font=f'Times {mode.width//50}')
        if mode.selectedPiece != None:
            mode.board.drawLegalMoves(mode.selectedPiece, canvas)

#===============================================================================

difficulty = 0

class PvAI(Mode):
    #model
    def appStarted(mode):
        scale = (mode.app.width-(mode.app.width//16))/1056
        url = 'http://i.imgur.com/zwF4Lyn.png'
        spritestrip = mode.loadImage(url)
        mode.scaledSpritestrip = mode.scaleImage(spritestrip, scale)
        mode.board = Board(mode.scaledSpritestrip, scale)
        mode.selectedPiece = None
        mode.blackTurn = False
        mode.checkExists = False
        mode.oldBoard = mode.board.board
        mode.message = 'WHITE MAY MOVE'
        mode.columns = ['A','B','C','D','E','F','G','H']
        mode.rows = ['8','7','6','5','4','3','2','1']
        mode.gameOver = False
        
    #your move
    def mousePressed(mode, event):
        mode.board.advice = []
        mode.board.cellSelection(event.x, event.y)
        row = mode.board.selected[0]
        col = mode.board.selected[1]
        if (mode.selectedPiece == None):
            mode.selectedPiece = mode.board.board[row][col]
        else:
            if(mode.selectedPiece.black==mode.blackTurn and
            (row,col) in mode.selectedPiece.legalMoves(mode.board.board)):
                mode.oldBoard = myDeepCopy(mode.board.board)
                PvP.completeLegalMove(mode, row, col)
            #remove selection
            mode.board.selected = (-1,-1)
            mode.selectedPiece = None
            if(mode.blackTurn and mode.oldBoard != mode.board.board):
                mode.message = 'AI IS THINKING...'

    #AI move
    def mouseReleased(mode, event):
        if(mode.blackTurn and mode.oldBoard != mode.board.board):
            mode.oldBoard = myDeepCopy(mode.board.board)
            #minimax move
            mode.board.board = myDeepCopy(
                PvAI.pruningMinimax(mode, difficulty, True))
            #manual updates
            PvP.updatePositions(mode)
            PvP.checkUpdate(mode)
            mode.blackTurn = False   
            #remove selection
            mode.board.selected = (-1,-1)
            mode.selectedPiece = None
            mode.message = 'AI HAS MOVED. YOUR MOVE.'

    #generates all possible boards for one state
    def boardGeneration(mode, blackSide=True):
        possibleBoards = []
        oldBoard = myDeepCopy(mode.board.board)
        for row in range(8):
            for col in range(8):
                piece = mode.board.board[row][col]
                if(piece != None and piece.black==blackSide):
                    mode.selectedPiece = piece
                    for move in mode.selectedPiece.legalMoves(mode.board.board):
                        targetRow = move[0]
                        targetCol = move[1]
                        tempPiece = mode.board.board[targetRow][targetCol]
                        if(mode.checkExists):
                            PvP.completeLegalMove(mode,
                                                       targetRow, targetCol)
                            if (mode.board.board != oldBoard and
                                mode.checkExists == False):
                                possibleBoards.append(
                                    myDeepCopy(mode.board.board))
                                mode.blackTurn = blackSide
                                PvP.revertMove(
                                    mode, targetRow, targetCol,
                                    row, col, tempPiece)
                                mode.checkExists = True
                        else:
                            PvP.completeLegalMove(mode,
                                                       targetRow, targetCol)
                            if (mode.board.board != oldBoard):
                                possibleBoards.append(
                                    myDeepCopy(mode.board.board))
                                mode.blackTurn = blackSide
                                PvP.revertMove(mode, targetRow, targetCol,
                                                row, col, tempPiece)
                                mode.checkExists = False
        return possibleBoards

    #returns board value
    def boardValue(mode, board, blackSide=True):
        boardCopy = myDeepCopy(board)
        boardValue = 0
        for row in range(8):
            for col in range(8):
                piece = boardCopy[row][col]
                if piece != None:
                    if ((piece.black and blackSide) or
                        (piece.black==False and blackSide==False)):
                        boardValue += piece.value
                    else:
                        boardValue -= piece.value
        return boardValue

    #minimax with alpha beta pruning and unique selection
    def pruningMinimax(mode, searchDepth, blackSide, depth=0,
                       alpha=-9999, beta=9999):
        if(blackSide): whiteSide=False
        else: whiteSide=True
        depth += 1
        #END NODES
        if(depth>searchDepth):
            return PvAI.boardValue(mode, mode.board.board, blackSide)
        #FINAL SELECTION
        elif(depth==1):
            finalChoices = []
            bestValue = -9999
            bestBoards = []
            pathValues = {}
            possibleBoards = PvAI.boardGeneration(mode, blackSide)
            if(len(possibleBoards)==0):
                mode.message = 'YOU WIN'
            for board in possibleBoards:
                oldBoard = myDeepCopy(mode.board.board)
                #NEW BOARD
                mode.board.board = myDeepCopy(board)
                PvP.updatePositions(mode)
                PvP.checkUpdate(mode)
                #NEXT LEVEL
                mode.blackTurn = whiteSide
                value = PvAI.pruningMinimax(mode, searchDepth,
                                                blackSide, depth,
                                                alpha, beta)
                #REVERT
                mode.board.board = myDeepCopy(oldBoard)
                PvP.updatePositions(mode)
                PvP.checkUpdate(mode)
                #UPDATE VALUES
                pathValues[str(board)] = value
                alpha = max(alpha,value)
            #UNIQUE SELECTION
            for path in pathValues:
                if pathValues[path] > bestValue:
                    bestValue = pathValues[path]
                    bestBoards = [path]
                elif pathValues[path] == bestValue:
                    bestBoards.append(path)
            for board in possibleBoards:
                if str(board) in bestBoards:
                    finalChoices.append(myDeepCopy(board))
            return random.choice(finalChoices)
        #MAX
        elif(depth%2==1):
            maxList=[]
            possibleBoards = PvAI.boardGeneration(mode, blackSide)
            if(len(possibleBoards)==0):
                return 9999
            for board in possibleBoards:
                oldBoard = myDeepCopy(mode.board.board)
                #NEW BOARD
                mode.board.board = myDeepCopy(board)
                PvP.updatePositions(mode)
                PvP.checkUpdate(mode)
                #NEXT LEVEL
                mode.blackTurn = whiteSide
                value = PvAI.pruningMinimax(mode, searchDepth,
                                                blackSide, depth,
                                                alpha, beta)
                #REVERT
                mode.board.board = myDeepCopy(oldBoard)
                PvP.updatePositions(mode)
                PvP.checkUpdate(mode)
                #PRUNING
                if(value>=beta):
                    return value
                maxList.append(value)
                alpha = max(alpha,value)         
            return max(maxList)
        #MIN
        elif(depth%2==0):
            minList=[]
            possibleBoards = PvAI.boardGeneration(mode, whiteSide)
            if(len(possibleBoards)==0):
                return 9999
            for board in possibleBoards:
                oldBoard = myDeepCopy(mode.board.board)
                #NEW BOARD
                mode.board.board = myDeepCopy(board)
                PvP.updatePositions(mode)
                PvP.checkUpdate(mode)
                #NEXT LEVEL
                mode.blackTurn = blackSide
                value = PvAI.pruningMinimax(mode, searchDepth,
                                                blackSide, depth,
                                                alpha, beta)
                #REVERT
                mode.board.board = myDeepCopy(oldBoard)
                PvP.updatePositions(mode)
                PvP.checkUpdate(mode)
                #PRUNING
                if(value<=alpha):
                    return value
                minList.append(value)
                beta = min(beta,value)
            return min(minList)

    #advice function
    def giveAdvice(mode, blackSide=False):
        if(blackSide): whiteSide=False
        else: whiteSide=True
        mode.board.advice = []
        advisedBoard = myDeepCopy(PvAI.pruningMinimax(mode, 2, blackSide))
        currentBoard = myDeepCopy(mode.board.board)
        for row in range(8):
            for col in range(8):
                if currentBoard[row][col] != advisedBoard[row][col]:
                    mode.board.advice.append((row, col))
        #checkmate advice
        currentCheck = mode.checkExists
        mode.board.board = myDeepCopy(advisedBoard)
        PvP.checkUpdate(mode)
        possibleBoards = PvAI.boardGeneration(mode, whiteSide)
        mode.board.board = myDeepCopy(currentBoard)
        mode.checkExists = currentCheck
        if len(possibleBoards) == 0:
            mode.message = ('''You can checkmate your opponent.\n
   Always watch the enemy king!''')
            mode.blackTurn = blackSide
            mode.board.selected = (-1,-1)
            mode.selectedPiece = None
            return None
        #obvious move with no long term harm
        beginnerBoard = myDeepCopy(PvAI.pruningMinimax(mode, 1, blackSide))
        mode.blackTurn = blackSide
        if beginnerBoard != advisedBoard:
            PvAI.adviceExplanation(mode, blackSide)
        else:
            mode.message = 'I foresee no immediate losses with this move.'
        mode.board.selected = (-1,-1)
        mode.selectedPiece = None

    #advice explanation
    def adviceExplanation(mode, blackSide=False):
        mode.blackTurn = blackSide
        if(blackSide): whiteSide=False
        else: whiteSide=True
        yourMove = []
        originalBoard = myDeepCopy(mode.board.board)
        mode.board.board = myDeepCopy(PvAI.pruningMinimax(mode, 1, blackSide))
        for row in range(8):
            for col in range(8):
                if (mode.board.board[row][col] != originalBoard[row][col]
                    and mode.board.board[row][col] != None):
                    yourMove.append((row, col))
                elif (mode.board.board[row][col] != originalBoard[row][col]
                    and originalBoard[row][col] != None):
                    yourMove.insert(0, (row, col))
        opponentMove = []
        middleBoard = myDeepCopy(mode.board.board)
        mode.board.board = myDeepCopy(PvAI.pruningMinimax(mode, 1, whiteSide))
        for row in range(8):
            for col in range(8):
                if (mode.board.board[row][col] != middleBoard[row][col]
                    and mode.board.board[row][col] != None):
                    opponentMove.append((row, col))
                elif (mode.board.board[row][col] != middleBoard[row][col]
                    and middleBoard[row][col] != None):
                    opponentMove.insert(0, (row, col))
        mode.board.board = myDeepCopy(originalBoard)
        yourMoveStart = (mode.columns[yourMove[0][1]],
                         mode.rows[yourMove[0][0]])
        yourMoveEnd = (mode.columns[yourMove[1][1]],
                         mode.rows[yourMove[1][0]])
        opponentMoveStart = (mode.columns[opponentMove[0][1]],
                         mode.rows[opponentMove[0][0]])
        opponentMoveEnd = (mode.columns[opponentMove[1][1]],
                         mode.rows[opponentMove[1][0]])
        mode.message = (f'''
  If you move {yourMoveStart[0]}{yourMoveStart[1]} to {yourMoveEnd[0]}{yourMoveEnd[1]} for the short term benefit,\n
then your opponent will move {opponentMoveStart[0]}{opponentMoveStart[1]} to {opponentMoveEnd[0]}{opponentMoveEnd[1]} to counter.\n
                          Always think ahead!''')
        
    #key control
    def keyPressed(mode, event):
        #reset
        if event.key == 'r':
            PvP.appStarted(mode)
        #menu function
        if event.key == 'm':
            PvAI.appStarted(mode)
            mode.app.setActiveMode(mode.app.mainMenu)
        #advice function
        if event.key=='a' and mode.blackTurn==False and mode.gameOver==False:
            PvAI.giveAdvice(mode)
        #clear
        if event.key == 'c':
            mode.message = ''
            mode.board.selected = (-1,-1)
            mode.board.advice = []
        #check test case
        if event.key == '1':
            mode.board.checkTest(mode.scaledSpritestrip)
            PvP.updatePositions(mode)
            PvP.checkUpdate(mode)
        #checkmate test case
        if event.key == '2':
            mode.board.checkmateTest(mode.scaledSpritestrip)
            PvP.updatePositions(mode)
            PvP.checkUpdate(mode)
        #AI test case
        if event.key == '3':
            mode.board.AITest(mode.scaledSpritestrip)
            PvP.updatePositions(mode)
            PvP.checkUpdate(mode)
        #explanation test case
        if event.key == '4':
            mode.board.explanationTest(mode.scaledSpritestrip)
            PvP.updatePositions(mode)
            PvP.checkUpdate(mode)
            
    #view
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,
                                fill='maroon',outline='black',
                                width=mode.width//100)
        mode.board.draw(canvas)
        PvP.drawPositionKeys(mode, canvas)
        canvas.create_text(mode.width/2, mode.height*9//10,
                           text=mode.message,
                           fill='white', font=f'Times {mode.width//50}')
        if mode.selectedPiece != None:
            mode.board.drawLegalMoves(mode.selectedPiece, canvas)

#===============================================================================

class DifficultyMenu(Mode):
    def appStarted(mode):
        mode.easy = (mode.width//4, mode.height//2-mode.height//4,
                     (mode.width*3)//4, mode.height//2-mode.height//8)
        mode.medium = (mode.width//4, mode.height//2-mode.height//16,
                     (mode.width*3)//4, mode.height//2+mode.height//16)
        mode.hard = (mode.width//4, mode.height//2+mode.height//8,
                     (mode.width*3)//4, mode.height//2+mode.height//4)
    
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,
                                fill='maroon',outline='black',
                                width=mode.width//100)
        canvas.create_rectangle(mode.easy[0],mode.easy[1],
                                mode.easy[2],mode.easy[3],
                                fill='black',outline='white',
                                width=mode.width//200)
        canvas.create_text(mode.width/2, mode.height//2-(mode.height*3)//16,
                           text='Easy',
                           fill='white', font=f'Times {mode.width//35}')
        canvas.create_rectangle(mode.medium[0],mode.medium[1],
                                mode.medium[2],mode.medium[3],
                                fill='black',outline='white',
                                width=mode.width//200)
        canvas.create_text(mode.width/2, mode.height//2,
                           text='Medium',
                           fill='white', font=f'Times {mode.width//35}')
        canvas.create_rectangle(mode.hard[0],mode.hard[1],
                                mode.hard[2],mode.hard[3],
                                fill='black',outline='white',
                                width=mode.width//200)
        canvas.create_text(mode.width/2, mode.height//2+(mode.height*3)//16,
                           text='Hard',
                           fill='white', font=f'Times {mode.width//35}')

    #Difficulty buttons
    def mousePressed(mode, event):
        global difficulty
        if (event.x>mode.easy[0] and event.x<mode.easy[2] and
            event.y>mode.easy[1] and event.y<mode.easy[3]):
            difficulty = 1
            mode.app.setActiveMode(mode.app.PvAI)
        if (event.x>mode.medium[0] and event.x<mode.medium[2] and
            event.y>mode.medium[1] and event.y<mode.medium[3]):
            difficulty = 2
            mode.app.setActiveMode(mode.app.PvAI)
        if (event.x>mode.hard[0] and event.x<mode.hard[2] and
            event.y>mode.hard[1] and event.y<mode.hard[3]):
            difficulty = 3
            mode.app.setActiveMode(mode.app.PvAI)

    def keyPressed(mode, event):
        if event.key == 'm':
            mode.app.setActiveMode(mode.app.mainMenu)

#===============================================================================

class MainMenu(Mode):
    def appStarted(mode):
        mode.title = (mode.width//4, mode.height//2-mode.height//4,
                     (mode.width*3)//4, mode.height//2-mode.height//8)
        mode.PvPButton = (mode.width//4, mode.height//2-mode.height//16,
                     (mode.width*3)//4, mode.height//2+mode.height//16)
        mode.PvAIButton = (mode.width//4, mode.height//2+mode.height//8,
                     (mode.width*3)//4, mode.height//2+mode.height//4)
    
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,
                                fill='maroon',outline='black',
                                width=mode.width//100)
        canvas.create_rectangle(mode.title[0],mode.title[1],
                                mode.title[2],mode.title[3],
                                fill='black',outline='white',
                                width=mode.width//200)
        canvas.create_text(mode.width/2, mode.height//2-(mode.height*3)//16,
                           text='ChessSensei',
                           fill='white',
                           font=f'Times {mode.width//27} bold underline')
        canvas.create_rectangle(mode.PvPButton[0],mode.PvPButton[1],
                                mode.PvPButton[2],mode.PvPButton[3],
                                fill='black',outline='white',
                                width=mode.width//200)
        canvas.create_text(mode.width/2, mode.height//2,
                           text='Player vs Player',
                           fill='white', font=f'Times {mode.width//35}')
        canvas.create_rectangle(mode.PvAIButton[0],mode.PvAIButton[1],
                                mode.PvAIButton[2],mode.PvAIButton[3],
                                fill='black',outline='white',
                                width=mode.width//200)
        canvas.create_text(mode.width/2, mode.height//2+(mode.height*3)//16,
                           text='Player vs AI',
                           fill='white', font=f'Times {mode.width//35}')
        canvas.create_text(mode.width/2, mode.height//2+(mode.height*3)//8,
                           text='PRESS M TO RETURN TO MENU',
                           fill='black', font=f'Times {mode.width//53}')
        canvas.create_text(mode.width/2, mode.height//2+(mode.height*7)//17,
                           text='PRESS A FOR MOVE ADVICE',
                           fill='black', font=f'Times {mode.width//53}')

    #Mode buttons
    def mousePressed(mode, event):
        if (event.x>mode.PvPButton[0] and event.x<mode.PvPButton[2] and
            event.y>mode.PvPButton[1] and event.y<mode.PvPButton[3]):
            mode.app.setActiveMode(mode.app.PvP)
        if (event.x>mode.PvAIButton[0] and event.x<mode.PvAIButton[2] and
            event.y>mode.PvAIButton[1] and event.y<mode.PvAIButton[3]):
            mode.app.setActiveMode(mode.app.difficultyMenu)

#===============================================================================

#ModalApp from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
class ChessSensei(ModalApp):
    def appStarted(app):
        app.mainMenu = MainMenu()
        app.difficultyMenu = DifficultyMenu()
        app.PvP = PvP()
        app.PvAI = PvAI()
        app.setActiveMode(app.mainMenu)

#changeable size        
def runChessSensei():
    size = 800
    app = ChessSensei(width=size+(size//16), height=size+(size//4))

runChessSensei()
