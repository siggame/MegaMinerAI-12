#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
from game_utils import *

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
    self.history = game_history(self, True)
    return

  ##This function is called once, after your last turn
  def end(self):
    self.history.print_history()
    return

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    self.history.save_snapshot()
    myPumpStation = [tile for tile in self.tiles if tile.owner == self.playerID and tile.pumpID != -1]
    enemyUnits = [unit for unit in self.units if unit.owner != self.playerID]
    unitAt = dict()
    for unit in self.units:
        unitAt [(unit.x, unit.y)] = unit
    for unit in self.units:
        if unit.owner == self.playerID:
            if enemyUnits:
                enemy = min(enemyUnits, key = lambda lionsTarget: abs(lionsTarget.x - unit.x) + abs(lionsTarget.y - unit.y))
                if taxiDis(enemy.x, enemy.y, unit.x , unit.y) <= unit.range:
                    unit.attack(enemy)
                    print ("Lion has mauled the enemy aka trey")
    for tile in myPumpStation:
        if (tile.x, tile.y) not in unitAt:
            tile.spawn (2)
    self.history.save_snapshot()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
