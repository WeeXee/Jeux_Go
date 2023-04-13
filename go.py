import tkinter as tk
import numpy as np
from game.board import Board
from game.stone import Stone
from game.player import Player
from game.ia import IA

offset = 20

class Window:
    def __init__(self, size,width, height,title):
        self.size = size
        self.position = np.zeros((size,size),dtype=[('x',int),('y',int)]) # x: vertical | y: horizontal

        self.window = tk.Tk()
        self.window.title(title)

        self.canvas = tk.Canvas(self.window, width=width, height=height, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.createGrid)

        self.status = tk.Label(self.window,font=("Helvetica",16))

    def getWindow(self):
        return self.window

    def getCanvas(self):
        return self.canvas
    
    def getGrid(self):
        return self.position
    
    def getGrid(self,x,y):
        return self.position[x][y]
    
    def mainLoop(self):
        self.window.mainloop()

    def printGrid(self):
        print(self.position)

    def printGrid(self,x,y):
        print(self.position[x][y])

    def createGrid(self,event=None):
        c = self.getCanvas()
        w = c.winfo_width()
        h = c.winfo_height()
        c.delete("grid_line")
        size = self.size
        size = size + 1

        for i in range(size):
            c.create_line([(w/size)*i, (w/size)*1, (w/size)*i, h-(w/size)*1], tag="grid_line")
            c.create_line([(h/size)*1, (h/size)*i, w-(h/size)*1, (h/size)*i], tag="grid_line")
        for i in range(size-1):
            for j in range(size-1):
                self.position[i][j] = ((w/size)*(i+1)), ((h/size)*(j+1))
class Go:
    def __init__(self,size,windowSize):
        self.players = []
        self.player = None
        self.game_over = False
        self.board = Board(size)
        self.window = Window(size,windowSize,windowSize,"Go")
        self.ia = None

    def addPlayer(self,player):
        self.players.append(player)
        return self

    def mainLoop(self):
        self.window.mainLoop()

    def start(self):
        if len(self.players) < 2:
            return
        elif len(self.players) > 2:
            return
        self.window.getCanvas().bind("<Button-1>", self.callback)
        self.player = self.players[0]
        self.mainLoop()

    def round(self,x,y):
        if self.board.get(x,y) != 0:
            self.board.get(x,y).remove()
        self.board.set(x,y,Stone(self.board,self.player,x,y))
        self.board.updateLiberties(self.board.get(x,y))
        self.drawBoard()
        self.player = self.players[1] if self.player == self.players[0] else self.players[0]
        print(self.ia.possible_moves)
        print(self.ia.best_move)
        return self

    def drawBoard(self):
        for x in range(self.board.getSize()):
            for y in range(self.board.getSize()):
                if self.board.get(x,y) != 0:
                    player = self.board.get(x,y).player
                    grid = self.window.getGrid(x,y)
                    canva = self.window.getCanvas()
                    canva.create_oval(grid[0]-offset,grid[1]-offset,grid[0]+offset,grid[1]+offset,fill=player.color,tag=f"stone{x}{y}")
                else:
                    grid = self.window.getGrid(x,y)
                    canva = self.window.getCanvas()
                    canva.delete(f"stone{x}{y}")
        return self

    def callback(self,event):
        for x in range(self.board.getSize()):
            for y in range(self.board.getSize()):
                grid = self.window.getGrid(x,y)
                if grid[0]-offset <= event.x <= grid[0]+offset and grid[1]-offset <= event.y <= grid[1]+offset:
                    self.round(x,y)
                    return

if __name__ == "__main__":
    go = Go(size=9,windowSize=800)
    go.addPlayer(Player("Player 1","black")).addPlayer(Player("Player 2","white"))
    ia = IA(go.players[0],go.board)
    print(ia.possible_moves)
    print(ia.best_move)
    go.ia = ia
    go.start()
