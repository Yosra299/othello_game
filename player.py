'''
player.py
This module defines several player class, including Human, Computer, Human(Server), Human(Client).
'''


class Player:

    def __init__(self, color):
        self.color = color
        self.gui = self.board = None

    def setGuiAndBoard(self, gui, board):
        self.gui = gui
        self.board = board

class Human(Player):

    def __init__(self, color):
        Player.__init__(self, color)
        self.type = 'Human'

    def getNextMove(self, lastrow, lastcol):
        avlbMoves = self.board.getAvlbMoves(self.color)
        if not avlbMoves:
            self.gui.showPassInfo(self.color)
            return None, None
        self.gui.showAvlbMoves(avlbMoves)
        row, col = self.gui.getInput(avlbMoves)
        self.gui.clearAvlbMoves(avlbMoves)
        return row, col


class Computer(Player):

    def __init__(self, color):
        Player.__init__(self, color)
        self.type = 'Computer'
        self.useOpenBook = True

    def getNextMove(self, lastrow, lastcol):
        if self.useOpenBook:
            row, col = self.board.getFromOpenBook(chr(lastcol+97)+str(lastrow+1))
            if row == None and col == None:
                self.useOpenBook = False
                row, col = self.board.getFromCmptr(self.color)
                if  row == None and col == None:
                    self.gui.showPassInfo(self.color)
        else:
            row, col = self.board.getFromCmptr(self.color)
            if row == None and col == None:
                self.gui.showPassInfo(self.color)
        return row, col
