#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import time
from time import sleep
import random
from pathing import Pathfinder, first


WORKER, SCOUT, TANK = range(3)

class AI(BaseAI):

    """The class implementing gameplay logic."""
    @staticmethod
    def username():
        return "Conquest"

    @staticmethod
    def password():
        return "password"

    def getSpawnTiles(self):
        self.spawnTiles = [i for i in self.tiles if i.owner == self.playerID]

    def spawnUnits(self):
        units = len([i for i in self.units if i.owner == self.playerID])
        for tile in self.spawnTiles:
            if self.player.oxygen >= self.unitTypes[TANK].cost:
                tile.spawn(TANK)

    def moveUnits(self):
        for unit in self.ourUnits:
            self.pathfinder.populate()
            options = self.pathfinder.path(unit)
            target = first(options, self.hostilePump)
            if target:
                print 'Coming to conquer pump %s' % target.tile.pumpID
                self.moveToward(unit, target)

    ##This function is called once, before your first turn
    def init(self):
        self.pathfinder = Pathfinder(self)
        self.player = self.players[self.playerID]

    ##This function is called once, after your last turn
    def end(self):
        pass


    ##This function is called each time it is your turn
    ##Return true to end your turn, return false to ask the server for updated information
    def run(self):
        print(self.turnNumber)
        self.getSpawnTiles()


        self.ourUnits = [i for i in self.units if i.owner == self.playerID]
        self.moveUnits()
        self.spawnUnits()


        return 1

    def __init__(self, conn):
        BaseAI.__init__(self, conn)

    def distance(self, source, dest):
        return abs(source.x - dest.x) + abs(source.y - dest.y)

    def moveToward(self, unit, tile):
        path = [tile]
        while path[-1].source:
            path.append(path[-1].source)
        path = path[-unit.movementLeft - 1:]
        hitList = []
        for place in path:
            hitList += [i for i in self.units if self.distance(i,place) == 1 and i not in hitList and
                    i.healthLeft > 0 and i.owner != self.playerID]
        hitList = hitList[:1]
        for target in hitList[:]:
            if self.distance(unit,target) == 1:
                unit.attack(target)
                hitList.remove(target)
        while path:
            next = path.pop()
            if unit.x != next.x or unit.y != next.y:
                unit.move(next.x, next.y)
                for target in hitList[:]:
                    if self.distance(unit,target) == 1:
                        unit.attack(target)
                        hitList.remove(target)
    
    def hostilePump(self, tile):
        if tile.tile.pumpID == -1:
            return False
        pump = [i for i in self.pumpStations if i.id == tile.tile.pumpID][0]
        if pump.owner == self.playerID:
            return False
        if tile.item and tile.item.owner == self.playerID:
            return False
        return True

