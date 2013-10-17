#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import time
from time import sleep
import random
from game_utils import get_tile
import game_utils


class AI(BaseAI):

  history = None
  spawnTiles = []
  myPumpTiles = []
  theIceTiles = []
  foundice = False
  havespawned = False

  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Anthony"

  @staticmethod
  def password():
    return "password"

  def getSpawnTiles(self):
    for tile in self.tiles:
      if tile.owner == self.playerID:
        self.spawnTiles.append(tile)

  def spawnUnits(self):
    for tile in self.spawnTiles:
      if self.havespawned == False:
        tile.spawn(game_utils.DIGGER)
        self.havespawned = True
  def moveUnits(self):
    for unit in self.units:
      if unit.owner == self.playerID:
        if self.foundice == False:
          while unit.movementLeft > 0:
            if unit.x < self.theIceTiles[0].x:
              unit.move(unit.x+1, unit.y)
            elif unit.y > self.theIceTiles[0].y + 1:
              unit.move(unit.x, unit.y-1)
              myoffset = 1
            elif unit.x > self.theIceTiles[0].x:
              unit.move(unit.x-1, unit.y)
            elif unit.y < self.theIceTiles[0].y - 1:
              unit.move(unit.x, unit.y+1)
              myoffset = -1
            else:
              self.foundice = True
              tile = game_utils.get_tile(self, unit.x, unit.y + myoffset)
              unit.dig(tile)
              while unit.movementLeft > 0:
                if unit.x < self.myPumpTiles[0].x:
                  unit.move(unit.x+1, unit.y)
                elif unit.y > self.myPumpTiles[0].y :
                  unit.move(unit.x, unit.y)

                elif unit.x > self.myPumpTiles[0].x:
                  unit.move(unit.x-1, unit.y)
                elif unit.y < self.myPumpTiles[0].y :
                  unit.move(unit.x, unit.y)


  def findMyPumpTiles(self):
    pumpTiles = []
    for tile in self.tiles:
      if tile.pumpID != -1 and tile.owner == self.getPlayerID():
        pumpTiles.append(tile)
    return pumpTiles


  def findIce(self):
    ice = []
    for tile in self.tiles:
      if tile.owner == 3:
        if tile.x < getMapWidth() / 2:
          ice.append(tile)
    return ice

  ##This function is called once, before your first turn
  def init(self):
    self.getSpawnTiles()
    self.history = game_utils.game_history(self, True)
    self.myPumpTiles = self.findMyPumpTiles()
    self.theIceTiles = self.findIce()
    return

  ##This function is called once, after your last turn
  def end(self):
    self.history.print_history()
    return
  
  def path_find(self, unit, x, y):
    while unit.movementLeft > 0:
      if unit.x < x:
        unit.move(unit.x+1, unit.y)
      elif unit.y > y:
        unit.move(unit.x, unit.y-1)
      elif unit.x > x:
        unit.move(unit.x-1, unit.y)
      elif unit.y < y:
        unit.move(unit.x, unit.y+1)
       

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    print(self.turnNumber)
    #SNAPSHOT AT BEGINNING
    self.history.save_snapshot()

    self.spawnUnits()
    self.moveUnits()


    #SNAPSHOT AT END
    self.history.save_snapshot()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
