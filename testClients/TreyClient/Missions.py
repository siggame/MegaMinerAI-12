from GameObject import *
from game_utils import *

from math import *

import operator

class Mission(object):
  def __init__(self, priority):
    self.priority = priority
    self.done = False
    
  def step(self):
    pass

class AttackMission(Mission):
  def __init__(self, priority, ai, heroID, targetID):
    Mission.__init__(self, priority)
    self.ai = ai
    self.heroID = heroID
    self.targetID = targetID
    
    self.hero = ai.unitByID[heroID]
    self.target = ai.unitByID[targetID]
    self.path = self.getPathToTarget()
    self.success = 0.0
    self.done = False
    
  def getPathToTarget(self):
    return aStar(self.ai, self.hero.x, self.hero.y, self.target.x, self.target.y,
      lambda tile: validMove(self.ai, tile, self.hero.healthLeft),
      lambda tile: costOfMove(self.ai, tile, self.hero.healthLeft))
    
  def step(self):
    success = False
    # Find our hero again (if he's not dead that is)
    if (self.heroID not in self.ai.unitByID):
      self.done = True
      print('Hero died?')
      return False
    self.hero = self.ai.unitByID[self.heroID]
    # Same with target
    if (self.targetID not in self.ai.unitByID):
      self.done = True
      print('Target died?')
      return True
    self.target = self.ai.unitByID[self.targetID]

    # Calculate path again
    self.path = self.getPathToTarget()
    # Move
    if self.path is None:
      success = False
    elif len(self.path) > 2:
      goalTile = self.path[1]
      success = self.hero.move(goalTile[0], goalTile[1])
      if len(self.path) == 3:
        goalTile = self.path[2]
        success = self.hero.attack(self.target)
    # Attack
    elif len(self.path) == 2:
      success = self.hero.attack(self.target)
    else:
      success = False
    # Update success of mission
    if success:
      self.success += 1.0
    else:
      self.success -= 2.0
    self.success *= 0.9
    return success
      
class DigPathMission(Mission):
  def __init__(self, priority, ai, heroID, sourceTile, endTile):
    Mission.__init__(self, priority)
    self.ai = ai
    self.heroID = heroID
    self.sourceTile = sourceTile
    self.endTile = endTile
    
    self.done = False
    self.path = None
    self.getPathFromSourceToEnd()
    
  def getPathFromSourceToEnd(self):
    self.trenchPath = aStar(self.ai, self.sourceTile.x, self.sourceTile.y, self.endTile.x, self.endTile.y,
      lambda tile: validTrench(self.ai, tile),
      lambda tile: costOfTrenchPath(self.ai, tile))
    if len(self.trenchPath) < 3:
      self.done = True
      return False
    self.trenchPath = map(lambda pos: self.ai.tiles[pos[0] * ai.mapHeight + pos[1]], self.path)
    # Remove first and last tile
    self.trenchPath[:] = self.trenchPath[1:-1]
  
  def getPathFromHeroToPath(self):
    closestTile = min(self.trenchPath, key = lambda tile: taxiDis(self.hero.x, self.hero.y, tile.x, tile.y))
    self.path = aStar(self.ai, self.hero.x, self.hero.y, closestTile.x, closestTile.y,
      lambda tile: validMove(self.ai, tile, self.hero.healthLeft),
      lambda tile: costOfMove(self.ai, tile, self.hero.healthLeft))
      
  def step(self):
    if self.done:
      return False
    success = False
    # Find our hero again (if he's not dead that is)
    if (self.heroID not in self.ai.unitByID):
      self.done = True
      print('Hero died?')
      return False
    self.hero = self.ai.unitByID[self.heroID]
    
    self.getPathFromHeroToPath()
    
    # Move
    if len(self.path) > 2:
      goal = self.path[1]
      success = self.hero.move(goal[0], goal[1])
      if len(self.path) == 3:
        goal = self.path[2]
        if (goal[0], goal[1]) not in self.ai.unitAt:
          success = self.hero.dig(goalTile)
        elif self.ai.unitAt[(goal[0], goal[1])] in self.enemyUnits:
          success = self.hero.attack(self.ai.unitAt[(goal[0], goal[1])])
    # Dig
    elif len(self.path) == 2:
      goal = self.path[1]
      if (goal[0], goal[1]) not in self.ai.unitAt:
        success = self.hero.dig(goalTile)
      elif self.ai.unitAt[(goal[0], goal[1])] in self.enemyUnits:
        success = self.hero.attack(self.ai.unitAt[(goal[0], goal[1])])
    else:
      success = False
    
    return success
      
class DigMission(Mission):
  def __init__(self, priority, ai, heroID, tile):
    Mission.__init__(self, priority)
    self.ai = ai
    self.heroID = heroID
    self.trenchTile = tile
    
    self.hero = ai.unitByID[heroID]
    self.done = False
    
  def getPathToTarget(self):
    return aStar(self.ai, self.hero.x, self.hero.y, self.trenchTile.x, self.trenchTile.y,
      lambda tile: validMove(self.ai, tile, self.hero.healthLeft),
      lambda tile: costOfMove(self.ai, tile, self.hero.healthLeft))
  
  def step(self):
    success = False
    # Find our hero again (if he's not dead that is)
    if (self.heroID not in self.ai.unitByID):
      self.done = True
      print('Hero died?')
      return False
    self.hero = self.ai.unitByID[self.heroID]
    
    # Calculate path again
    self.path = self.getPathToTarget()
    # Move
    if self.path is None:
      success = False
    elif len(self.path) > 2:
      goal = self.path[1]
      success = self.hero.move(goal[0], goal[1])
      if len(self.path) == 3:
        goal = self.path[2]
        if (goal[0], goal[1]) not in self.ai.unitAt:
          success = self.hero.dig(getTile(self.ai, goal[0], goal[1]))
        elif self.ai.unitAt[(goal[0], goal[1])] in self.ai.enemyUnits:
          success = self.hero.attack(self.ai.unitAt[(goal[0], goal[1])])
    # Dig
    elif len(self.path) == 2:
      goal = self.path[1]
      if (goal[0], goal[1]) not in self.ai.unitAt:
        success = self.hero.dig(getTile(self.ai, goal[0], goal[1]))
      elif self.ai.unitAt[(goal[0], goal[1])] in self.ai.enemyUnits:
        success = self.hero.attack(self.ai.unitAt[(goal[0], goal[1])])

    return success
    