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
  def __init__(self, priority, ai, hero, target):
    Mission.__init__(self, priority)
    self.ai = ai
    self.hero = hero
    self.target = target
    self.targetPrev = getTile(ai, target.x, target.y)
    self.path = self.getPathToTarget()
    self.success = 0.0
    self.done = False
    
  def getPathToTarget(self):
    return aStar(self.ai, self.hero.x, self.hero.y, self.target.x, self.target.y,
      lambda tile: validMove(self.ai, tile, self.hero.healthLeft),
      lambda tile: costOfMove(self.ai, tile, self.hero.healthLeft))
    
  def step(self):
    success = False
    # Check if hero is still alive
    if (self.hero not in self.ai.units):
      self.done = True
      print('Hero died?')
      return False
    # Check if target is still alive
    if (self.target not in self.ai.units):
      self.done = True
      print('Target died?')
      return True
    self.path = self.getPathToTarget()
    # Move
    if len(self.path) > 2:
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
      
