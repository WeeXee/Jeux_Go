import numpy as np

class Board:
    def __init__(self,size):
        self.size = size
        self.board = np.zeros((size,size),dtype=object)
        self.groups = []

    def get(self,x,y):
        return self.board[x][y]
    
    def getBoard(self):
        return self.board
    
    def getSize(self):
        return self.size
    
    def set(self,x,y,player):
        self.board[x][y] = player
        return self
    
    def search(self,points=[],point=None):
        if point != None:
            points.append(point)
        stones = []
        for point in points:
            if self.get(point[0],point[1]) != 0:
                stones.append(self.get(point[0],point[1]))
        return stones
    
    def updateLiberties(self,newStone=None):
        for group in self.groups:
            if newStone:
                if group == newStone.group:
                    continue
            group.updateLiberties()
        if newStone:
            newStone.group.updateLiberties()