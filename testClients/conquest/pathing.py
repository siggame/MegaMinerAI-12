class Tile(object):
    def __init__(self, x, y):
        self.item = None
        self.source = None
        self.tile = None
        self.distance = 10000
        self.x = x
        self.y = y

class Pathfinder(object):
    def __init__(self, ai):
        self.ai = ai
        self.tiles = [
                [Tile(i, j) for j in xrange(ai.mapHeight)]
                for i in xrange(ai.mapWidth)]
        for i in self.ai.tiles:
            tile = self.tiles[i.x][i.y]
            tile.tile = i


    def populate(self):
        for i in self.tiles:
            for j in i:
                j.distance = 10000
                j.source = None
                j.item = None

        for i in self.ai.units:
            tile = self.tiles[i.x][i.y]
            tile.item = i

    def path(self, unit, max=200):
        start = self.tiles[unit.x][unit.y]
        start.distance = 0
        open = [start]
        closed = []
        while open:
            i = open.pop(0)
            closed.append(i)
            if i.distance >= max:
                continue
            if self.blocked(unit, i):
                continue
            adjacent = self.adjacentTiles(i)
            for j in adjacent:
                if j.distance > i.distance + 1:
                    j.distance = i.distance+1
                    j.source = i
                    open.append(j)

        return closed

    def blocked(self, unit, tile):
        if tile.tile.owner not in [unit.owner, 2]:
            return True
        if tile.tile.waterAmount > 0:
            return True
        if tile.item and tile.item.id != unit.id:
            return True
        return False


    def adjacentTiles(self, tile):
        x = tile.x
        y = tile.y
        locations = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        tiles = []
        for i, j in locations:
            if i < 0 or i >= self.ai.mapWidth or j < 0 or j >= self.ai.mapHeight:
                continue
            tiles.append(self.tiles[i][j])

        return tiles

def first(closed, test):
    for i in closed:
        if test(i):
            return i
    return None

