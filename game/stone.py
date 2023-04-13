from game.group import Group

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
