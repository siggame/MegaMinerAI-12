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
    self.unitTypesByName = {unitType.name : unitType for unitType in self.unitTypes}
    self.unitTypeConfiguration = [self.unitTypesByName["Scout"], self.unitTypesByName["Scout"], self.unitTypesByName["Scout"],
      self.unitTypesByName["Worker"], self.unitTypesByName["Worker"], self.unitTypesByName["Tank"],
      self.unitTypesByName["Scout"], self.unitTypesByName["Scout"], self.unitTypesByName["Scout"]]
    #self.unitTypeConfiguration = [self.unitTypesByName["Scout"]]
      
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
    print('Memory : {}, {}, {}'.format(memory(), resident(), stacksize()))
    #SNAPSHOT AT BEGINNING
    self.history.save_snapshot()

    myPlayer = [player for player in self.players if player.id == self.playerID][0]

    start = time.clock()

    self.unitAt = dict()
    self.myUnitAt = dict()
    self.enemyUnitAt = dict()
    self.enemySpawnTilesSet = set()
    for unit in self.units:
      self.unitAt[(unit.x, unit.y)] = unit
      if unit.owner == self.playerID:
        self.myUnitAt[(unit.x, unit.y)] = unit
      else:
        self.enemyUnitAt[(unit.x, unit.y)] = unit

    spawnTiles = [tile for tile in self.tiles if tile.owner == self.playerID and (tile.x, tile.y) not in self.unitAt]
    spawnTiles.sort(key = lambda tile: -tile.x)
    self.enemySpawnTilesSet = set([tile for tile in self.tiles if tile.pumpID == -1 and tile.owner == (self.playerID^1)])

    availableEnemyPumpTiles = [tile for tile in self.tiles if tile.owner == self.playerID^1 and tile.pumpID != -1 and
        (tile.x, tile.y) not in self.myUnitAt]
    enemyUnits = [unit for unit in self.units if unit.owner == self.playerID^1]
    myUnits = [unit for unit in self.units if unit.owner == self.playerID]

    if time.clock() - start > 0.02:
      print('Time warning (pre) : {}'.format(time.clock() - start))

    if len(myUnits) < self.maxUnits:
      for tile in spawnTiles:
        type = random.choice(self.unitTypeConfiguration)
        if myPlayer.oxygen >= type.cost:
          if not tile.spawn(type.type):
            print('Error spawning ulnit, own units: {}'.format(len(myUnits)))

    if time.clock() - start > 0.05:
      print('Time warning (spawn) : {}'.format(time.clock() - start))

    for unit in myUnits:
      if not availableEnemyPumpTiles:
        break
      unitTile = getTile(self, unit.x, unit.y)
      if unitTile.owner != self.playerID^1:
        target = origTarget = min(availableEnemyPumpTiles, key = lambda tile: taxiDis(unit.x, unit.y, tile.x, tile.y))
        # Get nearest available tile to the one we want to get to
        if (target.x, target.y) in self.enemyUnitAt:
          target = getNearest(self, unitTile, target,
            lambda tile: (tile.x, tile.y) not in self.enemyUnitAt and not (tile.owner == (self.playerID^1) and tile.pumpID == -1))
        path = aStar(self, unitTile, target,
          lambda prev, tile: (tile.x, tile.y) not in self.unitAt and tile not in self.enemySpawnTilesSet and (tile.waterAmount <= 0 or unit.healthLeft > self.waterDamage),
          lambda prev, tile: 1 + (self.trenchDamage / unit.healthLeft) * ((prev.depth > 0) != (tile.depth > 0)) + 3 * (tile.waterAmount > 0) + (self.waterDamage / unit.healthLeft) * (tile.waterAmount > 0))
        if path is not None:
          if (unit.x, unit.y) not in self.unitAt:
            print('WTF')
            continue
          del self.unitAt[(unit.x, unit.y)]
          for m in xrange(0, min(unit.movementLeft, len(path) - 1)):
            if (path[m + 1].x, path[m + 1].y) in self.unitAt:
              print('Something blocking {}\'s path'.format(unit.id))
              break
            if (path[m + 1].owner == (self.playerID^1) and path[m + 1].pumpID == -1):
              print('Enemy Spawn blocking {}\'s path'.format(unit.id))
              break
            result = unit.move(path[m + 1].x, path[m + 1].y)
            if not result:
              print('Error {} moving'.format(result))
              break
            else:
              if unit.healthLeft <= 0:
                break
          if unit.healthLeft <= 0:
            break
          if unit.x == origTarget.x and unit.y == origTarget.y:
            availableEnemyPumpTiles.remove(origTarget)
          self.unitAt[(unit.x, unit.y)] = unit

    if time.clock() - start > 0.2:
      print('Time warning (move) : {}'.format(time.clock() - start))

    myUnits = [unit for unit in myUnits if unit.healthLeft > 0]

    if enemyUnits:
      for unit in myUnits:
        target = min(enemyUnits, key = lambda enemy: (taxiDis(unit.x, unit.y, enemy.x, enemy.y) > unit.range) * 1.0
            + (float(enemy.healthLeft) / enemy.maxHealth))
        if taxiDis(unit.x, unit.y, target.x, target.y) <= unit.range:
          result = unit.attack(target)
          if result == 1:
            if target.healthLeft <= 0:
              enemyUnits.remove(target)
              if not enemyUnits:
                break
          if result != 1:
            print('Attack error: {} for {}, r: {}, ({},{})->({},{})'.format(result, unit.id, unit.range, unit.x, unit.y, target.x, target.y))
    else:
      print('No enemies!')

    end = time.clock()
    print("Time : {}".format(end - start))

    #SNAPSHOT AT END
    self.history.save_snapshot()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
