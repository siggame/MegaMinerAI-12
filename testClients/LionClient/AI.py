#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"

  ##This function is called once, before your first turn
  def init(self):
    pass

  ##This function is called once, after your last turn
  def end(self):
    pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    myPumpStation = [tile for tile in self.tiles if tile.owner==self.playerID and tile.pumpID != -1]
    unitAt = dict()
    for unit in self.units:
        unitAt [(unit.x, unit.y)] = unit
    for tile in myPumpStation:
        if (tile.x, tile.y) not in unitAt:
            tile.spawn (2)
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
