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
            return f'Black Rook @ Row:{self.position[0]} Col:{self.position[1]}'
        else:
            return f'White Rook @ Row:{self.position[0]} Col:{self.position[1]}'
    
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
            return f'Black Knight @ Row:{self.position[0]} Col:{self.position[1]}'
        else:
            return f'White Knight @ Row:{self.position[0]} Col:{self.position[1]}'
    
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
            return f'Black Bishop @ Row:{self.position[0]} Col:{self.position[1]}'
        else:
            return f'White Bishop @ Row:{self.position[0]} Col:{self.position[1]}'
    
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
            return f'Black Queen @ Row:{self.position[0]} Col:{self.position[1]}'
        else:
            return f'White Queen @ Row:{self.position[0]} Col:{self.position[1]}'

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
            return f'Black King @ Row:{self.position[0]} Col:{self.position[1]}'
        else:
            return f'White King @ Row:{self.position[0]} Col:{self.position[1]}'

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
            return f'Black Pawn @ Row:{self.position[0]} Col:{self.position[1]}'
        else:
            return f'White Pawn @ Row:{self.position[0]} Col:{self.position[1]}'

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

    def mousePressed(mode, event):
        mode.board.cellSelection(event.x, event.y)
        row = mode.board.selected[0]
        col = mode.board.selected[1]
        if (mode.selectedPiece == None):
            mode.selectedPiece = mode.board.board[row][col]
        else:
            (oldRow, oldCol) = mode.selectedPiece.position
            mode.board.board[oldRow][oldCol] = None
            mode.board.board[row][col] = mode.selectedPiece
            mode.selectedPiece.position = (row,col)
            mode.board.selected = (-1,-1)
            mode.selectedPiece = None

    def keyPressed(mode, event):
        if event.key == 'c':
            mode.board.selected = (-1,-1)
            mode.selectedPiece = None           

    def redrawAll(mode, canvas):
        mode.board.draw(canvas)

class ChessSensei(ModalApp):
    def appStarted(app):
        app.gameMode = GameMode()
        app.setActiveMode(app.gameMode)
        
def runChessSensei():
    size = 1000
    app = ChessSensei(width=size, height=size)

runChessSensei()
