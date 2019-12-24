#===============================================================================
# Developer: Vishnu Pathmanaban
# Email: vpathman@andrew.cmu.edu
#===============================================================================
# File Description: Board Class
#===============================================================================
from pieces import *
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
        self.board[7][2] = Bishop(False, (4,7), spritestrip, self.size)
        self.board[1][3] = Queen(True, (1,3), spritestrip, self.size)
        self.board[6][4] = Queen(False, (6,4), spritestrip, self.size)
        self.board[0][4] = King(True, (0,4), spritestrip, self.size)
        self.board[7][4] = King(False, (7,4), spritestrip, self.size)
        self.board[0][5] = Bishop(True, (0,5), spritestrip, self.size)
        self.board[3][1] = Bishop(False, (3,1), spritestrip, self.size)
        self.board[0][6] = Knight(True, (0,6), spritestrip, self.size)
        self.board[7][6] = Knight(False, (7,6), spritestrip, self.size)
        self.board[0][7] = Rook(True, (0,7), spritestrip, self.size)
        self.board[7][7] = Rook(False, (7,7), spritestrip, self.size)
        self.blackKingPosition = (0,4)
        self.whiteKingPosition = (7,4)
        self.board[2][3] = Pawn(True, (2,3), spritestrip, self.size)
        self.board[5][4] = Pawn(False, (5,4), spritestrip, self.size)

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
