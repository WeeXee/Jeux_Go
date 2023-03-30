import tkinter as tk
import numpy as np

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.score = 0

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


class Board:
    def __init__(self,size):
        self.size = size
        self.board = [[None] * size ] * size

    def get(self,x,y):
        return self.board[x][y]
    
    def getBoard(self):
        return self.board
    
    def getSize(self):
        return self.size

class Go:
    def __init__(self,size,windowSize):
        self.players = []
        self.player = None
        self.game_over = False
        self.board = Board(size)
        self.window = Window(size,windowSize,windowSize,"Go")

    def addPlayer(self,player):
        self.players.append(player)

    def mainLoop(self):
        self.window.mainLoop()

    def start(self):
        self.window.getCanvas().bind("<Button-1>", self.callback)
        self.window.mainLoop()

    def callback(self,event):
        for x in range(self.board.getSize()):
            for y in range(self.board.getSize()):
                if self.window.getGrid(x,y)[0] - 20 <= event.x <= self.window.getGrid(x,y)[0] + 20 and self.window.getGrid(x,y)[1] - 20 <= event.y <= self.window.getGrid(x,y)[1] + 20:
                    print(f"clicked at ({x},{y})")

if __name__ == "__main__":
    go = Go(size=9,windowSize=800)
    go.start()
