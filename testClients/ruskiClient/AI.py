#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import time
from time import sleep


class AI(BaseAI):

  history = []

  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"

  def save_snapshot(self):
    tempGrid = [[' ' for _ in range( self.mapWidth ) ] for _ in range( self.mapHeight ) ]
    for tile in self.tiles:
      if tile.waterAmount > 0:
        tempGrid[tile.x][tile.y] = 'W'
      elif tile.isTrench == 1:
        tempGrid[tile.x][tile.y] = 'T'
      elif tile.owner in [0, 1]:
        tempGrid[tile.x][tile.y] = tile.owner

      for pump in self.pumpstations:
        tempGrid[pump.x][pump.y] = 'P'

      for unit in self.units:
        if unit.owner == 0:
          tempGrid[pump.x][pump.y] = 'U'
        elif unit.owner == 1:
          tempGrid[pump.x][pump.y] = 'u'


    self.history.append(tempGrid)
    return


  def print_snapshot(self, snapshot):
    print('---------------------------------------------------------------------------------------------')
    for row in snapshot:
      for column in row:
        print(column),
      print()

  ##This function is called once, before your first turn
  def init(self):
    self.history = []
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


    #SNAPSHOT AT END
    self.save_snapshot()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
