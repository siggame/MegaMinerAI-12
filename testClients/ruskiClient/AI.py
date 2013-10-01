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
    return "Ruski Malooski"

  @staticmethod
  def password():
    return "password"

  #USEFUL FOR GETTING TILES
  def getTile(self, x, y):
    return self.tiles[x * self.mapHeight + y]

  def getSpawnTiles(self):
    for tile in self.tiles:
      if tile.owner == self.playerID:
        self.spawnTiles.append(tile)

  def spawnUnits(self):
    for tile in self.spawnTiles:
      tile.spawn(random.choice([0,1]))

  def moveUnits(self):
    for unit in self.units:
      if unit.owner == self.playerID:
        offset = random.choice( [(0,1),(0,-1),(1,0),(-1,0)] )
        if (0 <= unit.x+offset[0] < self.mapWidth) and (0 <= unit.y+offset[1] < self.mapHeight):
            unit.move(unit.x+offset[0], unit.y+offset[1])

        offset = random.choice( [(0,1),(0,-1),(1,0),(-1,0)] )
        if (0 <= unit.x+offset[0] < self.mapWidth) and (0 <= unit.y+offset[1] < self.mapHeight):
          tile = self.getTile(unit.x+offset[0], unit.y+offset[1])
          if tile:
            if unit.dig(tile):
              print('TILE WAS DIGGED ({},{})'.format(tile.x, tile.y))
            #if unit.fill(tile):
            #  print('TILE WAS FILLED ({},{})'.format(tile.x, tile.y))


  def save_snapshot(self):
    tempGrid = [[[] for _ in range( self.mapHeight ) ] for _ in range( self.mapWidth ) ]

    for tile in self.tiles:
      if tile.waterAmount > 0:
        tempGrid[tile.x][tile.y].append('W')
      if tile.isTrench == 1:
        tempGrid[tile.x][tile.y].append('T')
      if tile.owner == 0:
        tempGrid[tile.x][tile.y].append('S')
      if tile.owner == 1:
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


  def print_snapshot(self, snapshot):
    print('--' * self.mapWidth)
    for y in range(self.mapHeight):
      for x in range(self.mapWidth):
        if len(snapshot[x][y]) >= 1:
          if 'T' in snapshot[x][y]:
            print('T'),
          else:
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
