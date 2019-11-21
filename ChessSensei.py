#################################################
# Developer: Vishnu Pathmanaban
# Email: vpathman@andrew.cmu.edu
#################################################
'''
TODO
- Move Generation
- King Management
'''

#graphics framework from CMU 15-112
#https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import math, random, copy

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

    def legalMove(self, board, row, col):
        target = board[row][col]
        if target != None and target.black==self.black:
            return False

class Rook(Piece):
    def __init__(self, black, position, spritestrip, size):
        super().__init__(black, position, spritestrip, size)
        if(self.black):
            self.sprite = spritestrip.crop((0*self.size, 1*self.size,
                                            1*self.size, 2*self.size))
        else:
            self.sprite = spritestrip.crop((0*self.size, 0*self.size,
                                            1*self.size, 1*self.size))

    def __repr__(self):
        if(self.black):
            return f'BR{self.position}'
        else:
            return f'WR{self.position}'

    def legalMove(self, board, row, col):
        if(super().legalMove(board, row, col)==False):
            return False
        oldRow=self.position[0]
        oldCol=self.position[1]
        if row==oldRow:
            if col<oldCol:
                for i in range(col+1, oldCol):
                    if board[row][i] != None:
                        return False
            elif col>oldCol:
                for i in range(col-1, oldCol, -1):
                    if board[row][i] != None:
                        return False
            return True
        elif col==oldCol:
            if row<oldRow:
                for i in range(row+1, oldRow):
                    if board[i][col] != None:
                        return False
            elif row>oldRow:
                for i in range(row-1, oldRow, -1):
                    if board[i][col] != None:
                        return False
            return True
        else:
            return False
        
class Knight(Piece):
    def __init__(self, black, position, spritestrip, size):
        super().__init__(black, position, spritestrip, size)
        if(self.black):
            self.sprite = spritestrip.crop((1*self.size, 1*self.size,
                                            2*self.size, 2*self.size))
        else:
            self.sprite = spritestrip.crop((1*self.size, 0*self.size,
                                            2*self.size, 1*self.size))

    def __repr__(self):
        if(self.black):
            return f'BN{self.position}'
        else:
            return f'WN{self.position}'

    def legalMove(self, board, row, col):
        if(super().legalMove(board, row, col)==False):
            return False
        oldRow=self.position[0]
        oldCol=self.position[1]
        return ((abs(col-oldCol)==2 and abs(row-oldRow)==1) or
                (abs(col-oldCol)==1 and abs(row-oldRow)==2))
    
class Bishop(Piece):
    def __init__(self, black, position, spritestrip, size):
        super().__init__(black, position, spritestrip, size)
        if(self.black):
            self.sprite = spritestrip.crop((2*self.size, 1*self.size,
                                            3*self.size, 2*self.size))
        else:
            self.sprite = spritestrip.crop((2*self.size, 0*self.size,
                                            3*self.size, 1*self.size))

    def __repr__(self):
        if(self.black):
            return f'BB{self.position}'
        else:
            return f'WB{self.position}'

    def legalMove(self, board, row, col):
        if(super().legalMove(board, row, col)==False):
            return False
        oldRow=self.position[0]
        oldCol=self.position[1]
        if(oldRow+oldCol == row+col):
            if row<oldRow:
                for i in range(1,oldRow-row):
                        if board[oldRow-i][oldCol+i] != None:
                            return False
            elif row>oldRow:
                for i in range(1,row-oldRow):
                        if board[oldRow+i][oldCol-i] != None:
                            return False
            return True
        elif(oldRow-oldCol == row-col):
            if row<oldRow:
                for i in range(1,oldRow-row):
                        if board[oldRow-i][oldCol-i] != None:
                            return False
            elif row>oldRow:
                for i in range(1,row-oldRow):
                        if board[oldRow+i][oldCol+i] != None:
                            return False
            return True
        else:
            return False
    
class Queen(Piece):
    def __init__(self, black, position, spritestrip, size):
        super().__init__(black, position, spritestrip, size)
        if(self.black):
            self.sprite = spritestrip.crop((3*self.size, 1*self.size,
                                            4*self.size, 2*self.size))
        else:
            self.sprite = spritestrip.crop((3*self.size, 0*self.size,
                                            4*self.size, 1*self.size))

    def __repr__(self):
        if(self.black):
            return f'BQ{self.position}'
        else:
            return f'WQ{self.position}'

    def legalMove(self, board, row, col):
        if(super().legalMove(board, row, col)==False):
            return False
        oldRow=self.position[0]
        oldCol=self.position[1]
        if row==oldRow:
            if col<oldCol:
                for i in range(col+1, oldCol):
                    if board[row][i] != None:
                        return False
            elif col>oldCol:
                for i in range(col-1, oldCol, -1):
                    if board[row][i] != None:
                        return False
            return True
        elif col==oldCol:
            if row<oldRow:
                for i in range(row+1, oldRow):
                    if board[i][col] != None:
                        return False
            elif row>oldRow:
                for i in range(row-1, oldRow, -1):
                    if board[i][col] != None:
                        return False
            return True
        elif(oldRow+oldCol == row+col):
            if row<oldRow:
                for i in range(1,oldRow-row):
                        if board[oldRow-i][oldCol+i] != None:
                            return False
            elif row>oldRow:
                for i in range(1,row-oldRow):
                        if board[oldRow+i][oldCol-i] != None:
                            return False
            return True
        elif(oldRow-oldCol == row-col):
            if row<oldRow:
                for i in range(1,oldRow-row):
                        if board[oldRow-i][oldCol-i] != None:
                            return False
            elif row>oldRow:
                for i in range(1,row-oldRow):
                        if board[oldRow+i][oldCol+i] != None:
                            return False
            return True
        else:
            return False

class King(Piece):
    def __init__(self, black, position, spritestrip, size):
        super().__init__(black, position, spritestrip, size)
        if(self.black):
            self.sprite = spritestrip.crop((4*self.size, 1*self.size,
                                            5*self.size, 2*self.size))
        else:
            self.sprite = spritestrip.crop((4*self.size, 0*self.size,
                                            5*self.size, 1*self.size))

    def __repr__(self):
        if(self.black):
            return f'BK{self.position}'
        else:
            return f'WK{self.position}'

    def legalMove(self, board, row, col):
        if(super().legalMove(board, row, col)==False):
            return False
        oldRow=self.position[0]
        oldCol=self.position[1]
        return (abs(col-oldCol)<=1 and abs(row-oldRow)<=1)

class Pawn(Piece):
    def __init__(self, black, position, spritestrip, size):
        super().__init__(black, position, spritestrip, size)
        if(self.black):
            self.sprite = spritestrip.crop((5*self.size, 1*self.size,
                                            6*self.size, 2*self.size))
        else:
            self.sprite = spritestrip.crop((5*self.size, 0*self.size,
                                            6*self.size, 1*self.size))

    def __repr__(self):
        if(self.black):
            return f'BP{self.position}'
        else:
            return f'WP{self.position}'

    def legalMove(self, board, row, col):
        if(super().legalMove(board, row, col)==False):
            return False
        oldRow=self.position[0]
        oldCol=self.position[1]
        if(self.black):
            return((oldRow==1 and col==oldCol and row==oldRow+2
                    and board[oldRow+1][oldCol]==None) or
                    (row==oldRow+1 and col==oldCol and board[row][col]==None)
                    or (row==oldRow+1 and abs(oldCol-col)==1 and
                    board[row][col]!=None))
        else:
            return((oldRow==6 and col==oldCol and row==oldRow-2
                    and board[oldRow-1][oldCol]==None) or
                    (row==oldRow-1 and col==oldCol and board[row][col]==None)
                    or (row==oldRow-1 and abs(oldCol-col)==1 and
                    board[row][col]!=None))
            

class Board(object):
    def __init__(self, spritestrip, scale):
        self.size = int(132*scale)
        self.selected = (-1,-1)
        self.board = [[None] * 8 for i in range(8)]
        for i in range(0, 8):
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

    #determines selected cell
    def cellSelection(self, x, y):
        for row in range(0,8):
            for col in range(0,8):
                x1 = col*self.size
                y1 = row*self.size
                x2 = col*self.size+self.size
                y2 = row*self.size+self.size
                if (x>x1 and x<x2 and y>y1 and y<y2):
                    self.selected = (row,col)

    def draw(self, canvas):
        for row in range(0,8):
            for col in range(0,8):
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
                                            outline='green',width=width)

class GameMode(Mode):
    def appStarted(mode):
        scale = mode.app.width/1056
        url = 'http://i.imgur.com/zwF4Lyn.png'
        spritestrip = mode.loadImage(url)
        scaledSpritestrip = mode.scaleImage(spritestrip, scale)
        mode.board = Board(scaledSpritestrip, scale)
        mode.selectedPiece = None
        mode.blackTurn = False

    #basic piece movement and capture
    def mousePressed(mode, event):
        mode.board.cellSelection(event.x, event.y)
        row = mode.board.selected[0]
        col = mode.board.selected[1]
        if (mode.selectedPiece == None):
            mode.selectedPiece = mode.board.board[row][col]
        else:
            if(mode.selectedPiece.black==mode.blackTurn):
                if mode.selectedPiece.legalMove(mode.board.board, row, col):
                    (oldRow, oldCol) = mode.selectedPiece.position
                    mode.board.board[oldRow][oldCol] = None
                    mode.board.board[row][col] = mode.selectedPiece
                    mode.selectedPiece.position = (row,col)
                    mode.board.selected = (-1,-1)
                    mode.selectedPiece = None
                    if mode.blackTurn:
                        mode.blackTurn = False
                    else:
                        mode.blackTurn = True
                else:
                    mode.board.selected = (-1,-1)
                    mode.selectedPiece = None
            else:
                mode.board.selected = (-1,-1)
                mode.selectedPiece = None

    #clear selection
    def keyPressed(mode, event):
        if event.key == 'c':
            mode.board.selected = (-1,-1)
            mode.selectedPiece = None           

    def redrawAll(mode, canvas):
        mode.board.draw(canvas)

#ModalApp from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
class ChessSensei(ModalApp):
    def appStarted(app):
        app.gameMode = GameMode()
        app.setActiveMode(app.gameMode)
        
def runChessSensei():
    size = 800
    app = ChessSensei(width=size, height=size)

runChessSensei()
