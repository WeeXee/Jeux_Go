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
