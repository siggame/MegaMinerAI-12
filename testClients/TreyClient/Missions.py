from BaseAI import BaseAI
from GameObject import *

from math import *

import operator

def validMove(self, tile):
  return tile.owner != (1 - self.getPlayerID())

def costOfMove(self, tile):
  if (tile.isTrench):
    if (tile.waterAmount > 0):
      return float(self.getWaterDamage()) / self.getMaxHealth()
    else:
      return float(self.getTrenchDamage()) / self.getMaxHealth()
  else:
    return 1.0
     
def validTrench(self, tile):
  return tile.owner == 2
  
def costOfTrench(self, tile)

def getTile(self, x, y):
  return self.tiles[x * self.getMapHeight() + y]

def taxiDis(x1, y1, x2, y2):
  return (abs(x2 - x1) + abs(y2 - y1))

def findIce(self):
  ice = []
  for tile in self.tiles:
    if tile.owner == 3:
      if tile.x < getMapWidth() / 2:
        ice.append(tile)
  return ice
  
def findMyPumpTiles(self):
  pumpTiles = []
  for tile in self.tiles:
    if tile.pumpID != -1 and tile.owner == self.getPlayerID():
      pumpTiles.append(tile)
  return pumpTiles    
      
def findEnemyPumpTiles(self):
  pumpTiles = []
  for tile in self.tiles:
    if tile.pumpID != -1 and tile.owner != self.getPlayerID():
      pumpTiles.append(tile)
  return pumpTiles
  
def findNearestTile(x, y, tiles):
  nearest = None
  minDis = 100;
  for tile in tiles:
    if taxiDis(tile.x, tile.y, x, y) < minDis:
      minDis = taxiDis(tile.x, tile.y, x, y)
      nearest = tile
  return nearest
  
def findMySpawnTiles(self):
  spawnTiles = []
  for tile in self.tiles:
    if tile.owner == self.getplayerID():
      spawnTiles.append(tile)
  return spawnTiles
 
def collectStart(self, unit):
  unit.targetIceTile = findNearestTile(self, unit.x, unit.y, self.remainingIceTiles):
  unit.targetPumpTile = findNearestTile(self, unit.targetIceTile.x, unit.targetIceTile.y, self.myPumps)
  unit.trenchPath = self.aStar(unit.targetIceTile.x, unit.targetIceTile.y,
    unit.targetPumpTile.x, unit.targetPumpTile.y,
    # Spawn tiles are invalid
    # pumps are invalid
    lambda tile: tile.pumpID == -1 and tile.owner != 0 and tile.owner != 1,
    # Trenches cost 0
    # Ice cost 0
    lambda tile: tile.isTrench == 0 and tile.owner != 3)
  unit.trenchPath[:] = [tile for tile in unit.trenchPath if tile.isTrench == 0 and tile.owner == 2]
  unit.goalTrench = findNearestTile(unit.x, unit.y, unit.trenchPath)
  unit.path = self.aStar(unit.x, unit.y, unit.goalTrench.x, unit.goalTrench.y,
    lambda tile: tile.owner != (1 - self.getPlayerID),
    lambda tile: tile.isTrench * self.getTrenchDamage() + (tile.waterAmount > 0) * self.getWaterDamage())
    
  
  
def aStar(self, startX, startY, goalX, goalY, isValidTile, tileCost):
  offsets = ((1,0),(0,1),(-1,0),(0,-1))

  start = (startX, startY)
  goal = (goalX, goalY)
  
  closed = set()
  open = [start]
  cameFrom = dict()
  
  g_score = dict()
  f_score = dict()
  
  g_score[start] = 0 # Cost from start along best known path.
  # Estimated total cost from start to goal through y.
  f_score[start] = g_score[start] + taxiDis(startX, startY, goalX, goalY)
     
  while len(open) > 0:
    # Black Magic ahead
    current = max(open, key = lambda obj: f_score[obj]) # the node in openset having the lowest f_score[] value
    if current == goal:
      return reconstructPath(cameFrom, goal)
     
    open.remove(current) # remove current from openset
    closed.add(current)
    
    for offset in offsets:
      pos = map(operator.add, current, offset)
      if self.isOnMap(pos[0], pos[1] and isValidTile(self.getTile(pos[0], pos[1]))):
        neighbor = tuple(pos)
        tentative_g_score = g_score[current] + tileCost(self.getTile(pos[0], pos[1]))
        tentative_f_score = tentative_g_score + taxiDis(neighbor[0], neighbor[1], goal[0], goal[1])
        if neighbor in closed and tentative_f_score >= f_score[neighbor]:
          continue
        if neighbor not in open or tentative_f_score < f_score[neighbor]:
          cameFrom[neighbor] = current
          g_score[neighbor] = tentative_g_score
          f_score[neighbor] = tentative_f_score
          if neighbor not in open:
            open.append(neighbor)

    return start
  
def reconstructPath(self, came_from, current_node)
  if current_node in came_from:
    p = [reconstruct_path(came_from, came_from[current_node])]
    return p.append(current_node)
  else:
    return self.getTile(current_node[0], current_node[1])
  
def isOnMap(self, x, y):
  return x >= 0 and x < self.getMapWidth() and y >= 0 and y < self.getMapHeight()

#
  