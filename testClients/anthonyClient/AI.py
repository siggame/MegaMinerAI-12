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

#Creates a list of all of my spawnable tiles
  def getSpawnTiles(self):
    self.spawnTiles = []
    for tile in self.tiles:
      if tile.owner == self.playerID:
        self.spawnTiles.append(tile)

#Attempt to spawn a random unit on a spawnable tile
  def spawnUnits(self):
    for tile in self.spawnTiles:
      tile.spawn(random.choice([0,1]))

#Make all units move randomly
  def moveUnits(self):
    for unit in self.units:
      if unit.owner == self.playerID:
        offsets = [(0,1),(0,-1),(1,0),(-1,0)]
        newx = unit.x+random.choice(offsets)[0]
        newy = unit.y+random.choice(offsets)[1]
        if (0 <= newx < self.mapWidth) and (0 <= newy < self.mapHeight):
          unit.move(newx, newy)

#Saves an instance or snapshot of the turn (Which will be printed in another function)
  def save_snapshot(self):
    tempGrid = [[[] for _ in range( self.mapHeight ) ] for _ in range( self.mapWidth ) ]

    for tile in self.tiles:
      if tile.waterAmount > 0:
        tempGrid[tile.x][tile.y].append('W')
      elif tile.isTrench == 1:
        tempGrid[tile.x][tile.y].append( 'T')
      elif tile.owner == 0:
        tempGrid[tile.x][tile.y].append('S')
      elif tile.owner == 1:
        tempGrid[tile.x][tile.y].append('s')

    for pump in self.pumpStations:
      tempGrid[pump.x][pump.y].append('P')

    for unit in self.units:
      if unit.owner == self.playerID:
        tempGrid[unit.x][unit.y].append('U')
      else:
        tempGrid[unit.x][unit.y].append('u')

    self.print_snapshot(tempGrid)
    self.history.append(tempGrid)
    return

#Prints out a single snapshot
  def print_snapshot(self, snapshot):
    print "--" * self.mapWidth
    for y in range(self.mapHeight):
      for x in range(self.mapWidth):
        if len(snapshot[x][y]) > 0:
          print(snapshot[x][y][0]),
        else:
          print(' '),  
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
