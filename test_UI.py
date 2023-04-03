import tkinter as tk
import numpy as np

offset = 20

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.score = 0

class MainMenu:
    def __init__(self,mainWindow):
        self.window = tk.Tk()
        self.window.title("Main Menu")
        self.menubar = tk.Menu(self.window)
        self.mainWindow = mainWindow

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Quit", command=self.window.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.window.config(menu=self.menubar)
        self.title = tk.Label(self.window, text="Main Menu", font=("Helvetica", 24))
        self.title.pack(pady=10)
        self.start_button = tk.Button(self.window, text="Start Game", command=self.start_game)
        self.start_button.pack()

    def start_game(self):
        self.mainWindow.getWindow().deiconify()

    def run(self):
        self.window.mainloop()

class Window:
    def __init__(self, size, width, height, title):
        self.size = size
        self.position = np.zeros((size,size),dtype=[('x',int),('y',int)]) # x: vertical | y: horizontal
        self.window = tk.Tk()
        self.window.title(title)
        self.menubar = tk.Menu(self.window)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)

        self.filemenu.add_command(label="Quit", command=self.window.quit)
        self.menubar.add_cascade(label="Options", menu=self.filemenu)
        self.menubar.add_cascade(label="Player", menu=self.filemenu)
        self.window.config(menu=self.menubar)
        self.canvas = tk.Canvas(self.window, width=width, height=height, bg="#d9d9d9")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.title = tk.Label(self.window, text=title, font=("Helvetica", 24))
        self.title.pack(pady=10)
        self.status = tk.Label(self.window, text="", font=("Helvetica", 16))
        self.status.pack(pady=10)
        self.canvas.bind("<Configure>", self.createGrid)
        self.window.withdraw()

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

    def newGame(self):
        self.current_player = None
        self.status.config(text="")
        self.createGrid()

    def setPlayer(self, player):
        self.current_player = player
        self.status.config(text="Player {} selected".format(player))

class Stone:
    def __init__(self, board ,player, x,y):
        self.position = (x,y)
        self.player = player
        self.board = board
        self.group = self.findGroup()

    def remove(self):
        self.group.stones.remove(self)
        self.board.set(self.position[0],self.position[1],0)
        del self

    @property
    def neighbors(self):
        neighboring = [(self.position[0] - 1, self.position[1]),
                       (self.position[0] + 1, self.position[1]),
                       (self.position[0], self.position[1] - 1),
                       (self.position[0], self.position[1] + 1)]
        for position in neighboring:
            if not (0 <= position[0] < self.board.size and 0 <= position[1] < self.board.size):
                neighboring.remove(position)
        for position in neighboring:
            if not (0 <= position[0] < self.board.size and 0 <= position[1] < self.board.size):
                neighboring.remove(position)
        return neighboring
    
    @property
    def liberties(self):
        liberties = self.neighbors
        stones = self.board.search(points=self.neighbors)
        for stone in stones:
            liberties.remove(stone.position)
        return liberties

    def findGroup(self):
        groups = []
        for stone in self.board.search(points=self.neighbors):
            if stone.player == self.player and stone.group not in groups:
                groups.append(stone.group)
        if not groups:
            group = Group(self.board,self.player,self)
            return group
        else: 
            if len(groups) > 1:
                for group in groups[1:]:
                    groups[0].merge(group)
            groups[0].stones.append(self)
            return groups[0]

class Group:
    def __init__(self, board, player, stone):
        self.player = player
        self.stones = [stone]
        self.liberties = None
        self.board = board
        self.board.groups.append(self)

    def merge(self, group):
        for stone in group.stones:
            stone.group = self
            self.stones.append(stone)
        self.board.groups.remove(group)
        del group

    def remove(self):
        while self.stones:
            self.stones[0].remove()
        self.board.groups.remove(self)
        del self

    def updateLiberties(self):
        liberties = []
        for stone in self.stones:
            for liberty in stone.liberties:
                liberties.append(liberty)
        self.liberties = set(liberties)
        if len(self.liberties) == 0:
            self.remove()

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
    
class Go:
    def __init__(self,size,windowSize):
        self.players = []
        self.player = None
        self.game_over = False
        self.board = Board(size)
        self.window = Window(size,windowSize,windowSize,"Go")
        self.mainMenu = MainMenu(self.window)

        self.mainMenu.filemenu.add_command(label="New Game", command=self.new_game)
        self.window.filemenu.add_command(label="New Game", command=self.new_game)
        self.mainMenu.run()

    def new_game(self):
        pass

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
    go = Go(size=9,windowSize=600)
    go.addPlayer(Player("Player 1","black")).addPlayer(Player("Player 2","white"))
