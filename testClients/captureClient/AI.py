#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

from game_utils import *
import time
import random

class AI(BaseAI):

  unitAt = dict()

  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "All your base are belong to us"

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
    print(self.turnNumber)
    #SNAPSHOT AT BEGINNING
    self.history.save_snapshot()

    myPlayer = [player for player in self.players if player.id == self.playerID][0]

    start = time.clock()

    self.unitAt = dict()
    for unit in self.units:
        self.unitAt[(unit.x, unit.y)] = unit

    spawnTiles = [tile for tile in self.tiles if tile.owner == self.playerID and (tile.x, tile.y) not in self.unitAt]
    spawnTiles.sort(key = lambda tile: -tile.x)

    availableEnemyPumpTiles = [tile for tile in self.tiles if tile.owner == self.playerID^1 and tile.pumpID != -1 and
        (tile.x, tile.y) not in self.unitAt]
    enemyUnits = [unit for unit in self.units if unit.owner == self.playerID^1]
    myUnits = [unit for unit in self.units if unit.owner == self.playerID]

    if len(myUnits) < self.maxUnits:
      for tile in spawnTiles:
        type = random.choice(self.unitTypes)
        if myPlayer.oxygen >= type.cost:
          tile.spawn(type.type)

    for unit in myUnits:
      if not availableEnemyPumpTiles:
        break
      unitTile = getTile(self, unit.x, unit.y)
      if unitTile.owner != self.playerID^1:
        target = min(availableEnemyPumpTiles, key = lambda tile: taxiDis(unit.x, unit.y, tile.x, tile.y))
        path = aStar(self, unitTile, target,
          lambda prev, tile: (tile.x, tile.y) not in self.unitAt and (tile.owner != self.playerID^1 or tile.pumpID == -1),
          lambda prev, tile: 1 + ((prev.depth > 0) != (tile.depth > 0)))
        if path is not None:
          del self.unitAt[(unit.x, unit.y)]
          for m in xrange(0, min(unit.movementLeft, len(path) - 1)):
            if (path[m + 1].x, path[m + 1].y) in self.unitAt:
              print('Something blocking {}\'s path'.format(unit.id))
              break
            if (path[m + 1].owner == self.playerID^1 and path[m + 1].pumpID == -1):
              print('Enemy Spawn blocking {}\'s path'.format(unit.id))
              break
            if not unit.move(path[m + 1].x, path[m + 1].y):
              break
          self.unitAt[(path[m + 1].x, path[m + 1].y)] = unit
          if unit.x == target.x and unit.y == target.y:
            availableEnemyPumpTiles.remove(target)
          self.unitAt[(unit.x, unit.y)] = unit

    if enemyUnits:
      for unit in myUnits:
        target = min(enemyUnits, key = lambda enemy: taxiDis(unit.x, unit.x, enemy.x, enemy.y)
            + (float(enemy.healthLeft) / enemy.maxHealth))
        if taxiDis(unit.x, unit.y, target.x, target.y) <= unit.range:
          result = unit.attack(target)
          if result != 1:
            print('Attack error: {} for {}, r: {}, ({},{})->({},{})'.format(result, unit.id, unit.range, unit.x, unit.y, target.x, target.y))

    end = time.clock()
    print("Time : {}".format(end - start))

    #SNAPSHOT AT END
    self.history.save_snapshot()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
