#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import time
from time import sleep
import random



class AI(BaseAI):

  history = []
  spawnTiles = []

  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"

  def getSpawnTiles(self):
    for tile in self.tiles:
      if tile.owner == self.playerID:
        self.spawnTiles.append(tile)

  def spawnUnits(self):
    for tile in self.spawnTiles:
      tile.spawn(random.choice([1,2]))

  def moveUnits(self):
    for unit in self.units:
      if unit.owner == self.playerID:
        unit.move(unit.x+1, unit.y)

  def save_snapshot(self):
    tempGrid = [[' ' for _ in range( self.mapHeight ) ] for _ in range( self.mapWidth ) ]

    for tile in self.tiles:
      if tile.waterAmount > 0:
        tempGrid[tile.x][tile.y] = 'W'
      elif tile.isTrench == 1:
        tempGrid[tile.x][tile.y] = 'T'
      elif tile.owner == 0:
        tempGrid[tile.x][tile.y] = 'S'
      elif tile.owner == 1:
        tempGrid[tile.x][tile.y] = 's'

    for pump in self.pumpStations:
      tempGrid[pump.x][pump.y] = 'P'

    for unit in self.units:
      if unit.owner == self.playerID:
        tempGrid[unit.x][unit.y] = 'U'
      else:
        tempGrid[unit.x][unit.y] = 'u'

    self.print_snapshot(tempGrid)
    self.history.append(tempGrid)
    return


  def print_snapshot(self, snapshot):
    print "--" * self.mapWidth
    for y in range(self.mapHeight):
      for x in range(self.mapWidth):
        print(snapshot[x][y]),
      print

  ##This function is called once, before your first turn
  def init(self):
    self.history = []
    self.getSpawnTiles()


    return

  ##This function is called once, after your last turn
  def end(self):
    for snapshot in self.history:
      self.print_snapshot(snapshot)
      sleep(.1)
    return


  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    print(self.turnNumber)
    #SNAPSHOT AT BEGINNING
    self.save_snapshot()

    self.spawnUnits()
    self.moveUnits()


    #SNAPSHOT AT END
    self.save_snapshot()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
