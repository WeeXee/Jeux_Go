import tkinter as tk

from game.board import Board
from game.stone import Stone
from game.window import Window
from game.player import Player
from game.window import MainMenu

offset = 20

    
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
        self.window.buttons.append(tk.Button(text ="Skip Turn", command = self.skipTurn).pack(side = tk.TOP, padx = 10, pady = 5))
        self.addPlayer(Player("Player 1","black")).addPlayer(Player("Player 2","white")).start()
        self.mainMenu.run()

    def skipTurn(self):
        pass

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
        print(event.x,event.y)
        for x in range(self.board.getSize()):
            for y in range(self.board.getSize()):
                grid = self.window.getGrid(x,y)
                if grid[0]-offset <= event.x <= grid[0]+offset and grid[1]-offset <= event.y <= grid[1]+offset:
                    self.round(x,y)
                    return

if __name__ == "__main__":
    go = Go(size=9,windowSize=600)
    go.addPlayer(Player("Player 1","black")).addPlayer(Player("Player 2","white"))
