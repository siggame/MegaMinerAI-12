#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import time
from time import sleep
import random
import game_utils
import path_find

class AI(BaseAI):

  history = None
  pf = None

  spawnTiles = []
  myunits = []

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

  def get_myunits(self):
    self.myunits = []
    for unit in self.units:
      if unit.owner == self.playerID:
        self.myunits.append(unit)
    return

  def moveUnits(self):
    for unit in self.myunits:
      pf_tiles = self.pf.path_find( game_utils.get_tile(self, unit.x,unit.y), game_utils.get_tile(self, 4,5) )
      for tile in pf_tiles:
        unit.move(tile)


  ##This function is called once, before your first turn
  def init(self):
    self.getSpawnTiles()
    self.history = game_utils.game_history(self, True)

    self.pf = path_find.path_finder(self)
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

    self.get_myunits()

    self.spawnUnits()
    self.moveUnits()


    #SNAPSHOT AT END
    self.history.save_snapshot()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
