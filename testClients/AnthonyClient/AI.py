#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import time
from time import sleep
import random
from game_utils import get_tile
import game_utils
import math


class AI(BaseAI):

  spawnTiles = []
  myPumpTiles = []
  pumpTiles = []
  theIceTiles = []
  foundpump = False
  whichice = 0
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
      tile.spawn(game_utils.DIGGER)

  @staticmethod
  def manDist(x1, y1, x2, y2):
      return abs(x1-x2) + abs(y1-y2)
  #array[start:end]


  def initPumpTiles(self):
      for tile in self.tiles:
          if tile.pumpID != -1:
              self.pumpTiles.append(tile)

  def nearestEnemyPumpTile(self, x, y):
      nearest_dist, nearest_tile = 10000000, None
      for tile in self.tiles:
          #is a pump
          if tile.pumpID != -1 and tile.owner != self.playerID:
              curdist = self.manDist(x, y, tile.x, tile.y)
              if curdist < nearest_dist:
                  nearest_tile = tile
                  nearest_dist = curdist
      return nearest_tile

  def nearestIceTile(self, x, y):
      nearest_dist, nearest_tile = 10000000, None
      for tile in self.tiles:
          #is a pump
          if tile.owner == 3 and tile.waterAmount > 0:
              curdist = self.manDist(x, y, tile.x, tile.y)
              if curdist < nearest_dist:
                  nearest_tile = tile
                  nearest_dist = curdist
      return nearest_tile


  def moveUnits2(self):
      for unit in self.units[0:len(self.units)/2]:
          neartile = self.nearestIceTile(unit.x, unit.y)
          if neartile is not None:
            self.path_find(unit, neartile.x, neartile.y)

      for unit in self.units[len(self.units)/2 +1:len(self.units)-1]:
          neartile = self.nearestEnemyPumpTile(unit.x, unit.y)
          if neartile is not None:
            self.path_find(unit, neartile.x, neartile.y)


  def moveUnits1(self):
    count = 0
    for unit in self.units:
      count += 1
      if unit.owner == self.playerID:
       #   while unit.movementLeft > 0:
        if self.foundpump == True & self.whichice < 4 & count < 500:
          if unit.x < self.theIceTiles[self.whichice].x:
              unit.move(unit.x+1, unit.y)
          elif unit.y > self.theIceTiles[self.whichice].y + 1:
            unit.move(unit.x, unit.y-1)

          elif unit.x > self.theIceTiles[self.whichice].x:
            unit.move(unit.x-1, unit.y)
          elif unit.y < self.theIceTiles[self.whichice].y - 1:
            unit.move(unit.x, unit.y+1)

          else:
            self.foundpump = False
            self.whichice+=1
            tile = game_utils.get_tile(self, unit.x, unit.y)
            unit.dig(tile)
          #    while unit.movementLeft > 0:
        if self.foundpump == False & count < 500:
          if unit.x < self.myPumpTiles[0].x:
            unit.move(unit.x+1, unit.y)
          elif unit.y > self.myPumpTiles[0].y :
            unit.move(unit.x, unit.y)

          elif unit.x > self.myPumpTiles[0].x:
            unit.move(unit.x-1, unit.y)
          elif unit.y < self.myPumpTiles[0].y :
            unit.move(unit.x, unit.y)
          else:
            self.foundpump = True

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
        ice.append(tile)
    return ice

  ##This function is called once, before your first turn
  def init(self):
    self.getSpawnTiles()
    self.history = game_utils.game_history(self, True)
    self.myPumpTiles = self.findMyPumpTiles()
    self.pumpTiles = self.initPumpTiles()
    self.theIceTiles = self.findIce()
    return

  ##This function is called once, after your last turn
  def end(self):
    self.history.print_history()
    return
  
  def path_find(self, unit, x, y):
    count = 0
    while unit.movementLeft > 0:
      if count > 50:
        return
      count += 1

      unit.dig(game_utils.get_tile(self, unit.x, unit.y))
      if unit.x < x-1:
        unit.move(unit.x+1, unit.y)
      elif unit.y > y+1:
        unit.move(unit.x, unit.y-1)
      elif unit.x > x+1:
        unit.move(unit.x-1, unit.y)
      elif unit.y < y-1:
        unit.move(unit.x, unit.y+1)
      elif unit.x < x:
        unit.move(unit.x+1, unit.y)
      elif unit.y > y:
        unit.move(unit.x, unit.y-1)
      elif unit.x > x:
        unit.move(unit.x-1, unit.y)
      elif unit.y < y:
        unit.move(unit.x, unit.y+1)

  def path_find2(self, unit, x, y):
    count = 0
    while unit.movementLeft > 0:
      if count > 20:
        unit.move(unit.x, unit.y+1)

      if count > 30:
        unit.move(unit.x, unit.y-1)

      if count > 40:
        unit.move(unit.x + 1, unit.y)

      if count > 50:
        unit.move(unit.x - 1, unit.y)

      if count > 60:
        unit.move(unit.x, unit.y+1)
        return
      count += 1

      
      if unit.x < x-1:
        unit.move(unit.x+1, unit.y)
      elif unit.y > y+1:
        unit.move(unit.x, unit.y-1)
      elif unit.x > x+1:
        unit.move(unit.x-1, unit.y)
      elif unit.y < y-1:
        unit.move(unit.x, unit.y+1)
      elif unit.x < x:
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

    self.spawnUnits()
    self.moveUnits2()

    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
