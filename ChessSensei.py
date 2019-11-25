#################################################
# Developer: Vishnu Pathmanaban
# Email: vpathman@andrew.cmu.edu
#################################################
'''
IGNORING:
- Castling
- Pawn Promotion
- En Passant
BUGS:
- None
TODO:
- Mode UI (TP2)
- Highlight Advice (TP3)
- Counter Check (TP3)
- Position Evaluation (TP3)
'''

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

class Board(object):
    #creates board
    def __init__(self, spritestrip, scale):
        self.size = int(132*scale)
        self.selected = (-1,-1)
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

    #determines if either king is in check (REVIEW)
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

    '''#determines if either king is in check
    def check(self):
        checked = 'N'
        for row in range(8):
            for col in range(8):
                item = self.board[row][col]
                if(item != None):
                    if(item.black and
                       self.whiteKingPosition in item.legalMoves(self.board)):
                        if(checked == 'BC'):
                            checked = 'BWC'
                        else:
                            checked = 'WC'
                    elif(self.blackKingPosition in item.legalMoves(self.board)):
                        if(checked == 'WC'):
                            checked = 'BWC'
                        else:
                            checked = 'BC'
        return checked'''

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

class GameMode(Mode):
    #model
    def appStarted(mode):
        scale = mode.app.width/1056
        url = 'http://i.imgur.com/zwF4Lyn.png'
        spritestrip = mode.loadImage(url)
        scaledSpritestrip = mode.scaleImage(spritestrip, scale)
        mode.board = Board(scaledSpritestrip, scale)
        mode.selectedPiece = None
        mode.blackTurn = False
        mode.checkExists = False
        
    #MAIN GAME (REVIEW)
    def mousePressed(mode, event):
        mode.board.cellSelection(event.x, event.y)
        row = mode.board.selected[0]
        col = mode.board.selected[1]
        if (mode.selectedPiece == None):
            mode.selectedPiece = mode.board.board[row][col]
        else:
            if(mode.selectedPiece.black==mode.blackTurn and
            (row,col) in mode.selectedPiece.legalMoves(mode.board.board)):
                #YOUR MOVE
                oldBoard = myDeepCopy(mode.board.board)
                GameMode.completeLegalMove(mode, row, col)
                #AI MOVE (IN PROGRESS)
                if(mode.board.board != oldBoard):
                    oldBoard = myDeepCopy(mode.board.board)
                    #minimax move
                    mode.board.board = myDeepCopy(
                        GameMode.pruningMinimax(mode, 3, True))
                    GameMode.updatePositions(mode)
                    #removes check if board updated legally
                    if(mode.checkExists and
                       mode.board.board != oldBoard):
                        mode.checkExists = False
                    mode.blackTurn = False
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

    #complete function that only moves piece if legal by check and chess laws (REVIEW)
    def completeLegalMove(mode, row, col):
        tempPiece = mode.board.board[row][col]
        (oldRow, oldCol) = mode.selectedPiece.position
        GameMode.movePiece(mode, row, col, oldRow, oldCol)
        #new check
        if(mode.board.check()!='none' and mode.checkExists==False):
            #check on player moving currently
            if((mode.board.check()=='black' and mode.blackTurn) or
               (mode.board.check()=='white' and mode.blackTurn==False)):
                GameMode.revertMove(mode, row, col, oldRow, oldCol,
                                    tempPiece)
            #check on opponent
            else:
                mode.checkExists = True
                GameMode.switchTurns(mode)
        #existing check not removed
        elif(mode.board.check()!='none' and mode.checkExists==True):
            GameMode.revertMove(mode, row, col, oldRow, oldCol,
                                    tempPiece)
        #chess legal move
        else:
            mode.checkExists = False
            GameMode.switchTurns(mode)

    '''#complete function that only moves piece if legal by check and chess laws 
    def completeLegalMove(mode, row, col):
        tempPiece = mode.board.board[row][col]
        (oldRow, oldCol) = mode.selectedPiece.position
        GameMode.movePiece(mode, row, col, oldRow, oldCol)
        #both kings in check
        if(len(mode.board.check())==3):
           GameMode.revertMove(mode, row, col, oldRow, oldCol,
                                    tempPiece)
        #one king in check
        elif(len(mode.board.check())==2):
            #check on player moving currently
            if((mode.board.check()=='BC' and mode.blackTurn) or
               (mode.board.check()=='WC' and mode.blackTurn==False)):
                GameMode.revertMove(mode, row, col, oldRow, oldCol,
                                    tempPiece)
            #check on opponent
            else:
                mode.checkExists = True
                GameMode.switchTurns(mode)
        #no king in check
        else:
            mode.checkExists = False
            GameMode.switchTurns(mode)'''

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
                            GameMode.completeLegalMove(mode,
                                                       targetRow, targetCol)
                            if (mode.board.board != oldBoard and
                                mode.checkExists == False):
                                possibleBoards.append(
                                    myDeepCopy(mode.board.board))
                                mode.blackTurn = blackSide
                                GameMode.revertMove(
                                    mode, targetRow, targetCol,
                                    row, col, tempPiece)
                                mode.checkExists = True
                        else:
                            GameMode.completeLegalMove(mode,
                                                       targetRow, targetCol)
                            if (mode.board.board != oldBoard):
                                possibleBoards.append(
                                    myDeepCopy(mode.board.board))
                                mode.blackTurn = blackSide
                                GameMode.revertMove(mode, targetRow, targetCol,
                                                row, col, tempPiece)
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
        
    #minimax no pruning
    def minimax(mode, searchDepth, blackSide, depth=0):
        if(blackSide): whiteSide=False
        else: whiteSide=True
        depth += 1
        #END NODES
        if(depth>searchDepth):
            return GameMode.boardValue(mode, mode.board.board, blackSide)
        #FINAL SELECTION
        elif(depth==1):
            bestValue = -9999
            bestBoard = None
            pathValues = {}
            possibleBoards = GameMode.boardGeneration(mode, blackSide)
            if(len(possibleBoards)==0):
                print('CHECKMATE FINAL')
            for board in possibleBoards:
                oldBoard = myDeepCopy(mode.board.board)
                #NEW BOARD
                mode.board.board = myDeepCopy(board)
                GameMode.updatePositions(mode)
                #NEXT LEVEL
                mode.blackTurn = whiteSide
                pathValues[str(board)]=GameMode.minimax(mode, searchDepth,
                                                        blackSide, depth)
                #REVERT
                mode.board.board = myDeepCopy(oldBoard)
                GameMode.updatePositions(mode)
            for path in pathValues:
                if pathValues[path] > bestValue:
                    bestValue = pathValues[path]
                    bestBoard = path
            for board in possibleBoards:
                if str(board) == bestBoard:
                    bestBoard = myDeepCopy(board)
            return bestBoard
        #MAX
        elif(depth%2==1):
            maxList=[]
            possibleBoards = GameMode.boardGeneration(mode, blackSide)
            if(len(possibleBoards)==0):
                print('AVOIDED SELF CHECKMATE')
                return 9999
            for board in possibleBoards:
                oldBoard = myDeepCopy(mode.board.board)
                #NEW BOARD
                mode.board.board = myDeepCopy(board)
                GameMode.updatePositions(mode)
                #NEXT LEVEL
                mode.blackTurn = whiteSide
                maxList.append(GameMode.minimax(mode, searchDepth,
                                                blackSide, depth))
                #REVERT
                mode.board.board = myDeepCopy(oldBoard)
                GameMode.updatePositions(mode)
            return max(maxList)
        #MIN
        else:
            minList=[]
            possibleBoards = GameMode.boardGeneration(mode, whiteSide)
            if(len(possibleBoards)==0):
                print('PREDICTED OPPONENT CHECKMATE')
                return -9999
            for board in possibleBoards:
                oldBoard = myDeepCopy(mode.board.board)
                #NEW BOARD
                mode.board.board = myDeepCopy(board)
                GameMode.updatePositions(mode)
                #NEXT LEVEL
                mode.blackTurn = blackSide
                minList.append(GameMode.minimax(mode, searchDepth,
                                                blackSide, depth))
                #REVERT
                mode.board.board = myDeepCopy(oldBoard)
                GameMode.updatePositions(mode)
            return min(minList)

    #minimax with alpha beta pruning
    def pruningMinimax(mode, searchDepth, blackSide, depth=0, alpha=-9999, beta=9999):
        if(blackSide): whiteSide=False
        else: whiteSide=True
        depth += 1
        #END NODES
        if(depth>searchDepth):
            return GameMode.boardValue(mode, mode.board.board, blackSide)
        #FINAL SELECTION
        elif(depth==1):
            finalChoices = []
            bestValue = -9999
            bestBoards = []
            pathValues = {}
            possibleBoards = GameMode.boardGeneration(mode, blackSide)
            if(len(possibleBoards)==0):
                print('CHECKMATE FINAL')
            for board in possibleBoards:
                oldBoard = myDeepCopy(mode.board.board)
                #NEW BOARD
                mode.board.board = myDeepCopy(board)
                GameMode.updatePositions(mode)
                #NEXT LEVEL
                mode.blackTurn = whiteSide
                value = GameMode.pruningMinimax(mode, searchDepth,
                                                blackSide, depth,
                                                alpha, beta)
                #REVERT
                mode.board.board = myDeepCopy(oldBoard)
                GameMode.updatePositions(mode)
                #UPDATE VALUES
                pathValues[str(board)] = value
                alpha = value
            for path in pathValues:
                if pathValues[path] > bestValue:
                    bestValue = pathValues[path]
                    bestBoards = [path]
                elif pathValues[path] == bestValue:
                    bestBoards.append(path)
            for board in possibleBoards:
                if str(board) in bestBoards:
                    finalChoices.append(board)
            return random.choice(finalChoices)
        #MAX
        elif(depth%2==1):
            maxList=[]
            possibleBoards = GameMode.boardGeneration(mode, blackSide)
            if(len(possibleBoards)==0):
                print('AVOIDED SELF CHECKMATE')
                return 9999
            for board in possibleBoards:
                oldBoard = myDeepCopy(mode.board.board)
                #NEW BOARD
                mode.board.board = myDeepCopy(board)
                GameMode.updatePositions(mode)
                #NEXT LEVEL
                mode.blackTurn = whiteSide
                value = GameMode.pruningMinimax(mode, searchDepth,
                                                blackSide, depth,
                                                alpha, beta)
                #REVERT
                mode.board.board = myDeepCopy(oldBoard)
                GameMode.updatePositions(mode)
                #PRUNING
                if(value>=beta):
                    return value
                maxList.append(value)
                alpha = value         
            return max(maxList)
        #MIN
        else:
            minList=[]
            possibleBoards = GameMode.boardGeneration(mode, whiteSide)
            if(len(possibleBoards)==0):
                print('PREDICTED OPPONENT CHECKMATE')
                return -9999
            for board in possibleBoards:
                oldBoard = myDeepCopy(mode.board.board)
                #NEW BOARD
                mode.board.board = myDeepCopy(board)
                GameMode.updatePositions(mode)
                #NEXT LEVEL
                mode.blackTurn = blackSide
                value = GameMode.pruningMinimax(mode, searchDepth,
                                                blackSide, depth,
                                                alpha, beta)
                #REVERT
                mode.board.board = myDeepCopy(oldBoard)
                GameMode.updatePositions(mode)
                #PRUNING
                if(value<=alpha):
                    return value
                minList.append(value)
                beta = value
            return min(minList)
                
    #key control
    def keyPressed(mode, event):
        #cancel selection
        if event.key == 'c':
            mode.board.selected = (-1,-1)
            mode.selectedPiece = None
        #debug function
        if event.key == 'd':
            pass
            
    #view
    def redrawAll(mode, canvas):
        mode.board.draw(canvas)
        if mode.selectedPiece != None:
            mode.board.drawLegalMoves(mode.selectedPiece, canvas)

#ModalApp from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
class ChessSensei(ModalApp):
    def appStarted(app):
        app.gameMode = GameMode()
        app.setActiveMode(app.gameMode)

#changeable size        
def runChessSensei():
    size = 800
    app = ChessSensei(width=size, height=size)

runChessSensei()
