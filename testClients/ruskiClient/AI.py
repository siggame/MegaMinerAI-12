#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import time
from time import sleep
import random
import game_utils

class AI(BaseAI):

  history = None
  spawnTiles = []

  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Ruski Malooski"

  @staticmethod
  def password():
    return "password"

  def getSpawnTiles(self):
    for tile in self.tiles:
      if tile.owner == self.playerID:
        self.spawnTiles.append(tile)

  def spawnUnits(self):
    for tile in self.spawnTiles:
      tile.spawn(random.choice([game_utils.DIGGER, game_utils.FILLER]))

  def moveUnits(self):
    for unit in self.units:
      if unit.owner == self.playerID:
        offset = random.choice( [(0,1),(0,-1),(1,0),(-1,0)] )
        if (0 <= unit.x+offset[0] < self.mapWidth) and (0 <= unit.y+offset[1] < self.mapHeight):
            unit.move(unit.x+offset[0], unit.y+offset[1])

        offset = random.choice( [(0,1),(0,-1),(1,0),(-1,0)] )
        #Check if off map
        if (0 <= unit.x+offset[0] < self.mapWidth) and (0 <= unit.y+offset[1] < self.mapHeight):
          tile = game_utils.get_tile(self, unit.x+offset[0], unit.y+offset[1])
          unit.dig(tile)
          unit.fill(tile)

  ##This function is called once, before your first turn
  def init(self):
    self.getSpawnTiles()
    self.history = game_utils.game_history(self, True)
    self.history.set_nonmoving_elements()
    return

  ##This function is called once, after your last turn
  def end(self):
    self.history.print_history()
    return


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
