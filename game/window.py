import tkinter as tk
import numpy as np

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
        self.player_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Player", menu=self.player_menu)

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
        self.buttons = []

        self.filemenu.add_command(label="Quit", command=self.window.quit)
        self.menubar.add_cascade(label="Options", menu=self.filemenu)
        self.menubar.add_cascade(label="Player", menu=self.filemenu)
        self.window.config(menu=self.menubar)
        self.canvas = tk.Canvas(self.window, width=width, height=height, bg="#d9d9d9")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.title = tk.Label(self.window, text=title, font=("Helvetica", 24))
        self.title.pack(pady=2)
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

    def setPlayer(self, player):
        self.current_player = player
        self.status.config(text="Player {} selected".format(player))

    def newGame(self):
        self.current_player = None
        self.status.config(text="")
        self.createGrid()
        for button in self.buttons:
            button.config(command=lambda button=button: self.takeTurn(button))
            self.status.config(text="Player {}'s turn".format(self.current_player.name))

    def takeTurn(self, button):
        if button["text"] == "":
            button["text"] = self.current_player.color
            x, y = self.getButtonPosition(button)
            self.board.play(self.current_player, x, y)

            if self.board.checkWin(x, y):
                self.status.config(text="Player {} wins!".format(self.current_player.name))
                for button in self.buttons:
                    button.config(state=tk.DISABLED)
            else:
                self.current_player = self.player2 if self.current_player == self.player1 else self.player1
                if self.current_player.is_human:
                    self.status.config(text="Player {}'s turn".format(self.current_player.name))
                else:
                    x, y = self.current_player.play(self.board)
                    button = self.buttons[x + y * self.size]
                    self.takeTurn(button)