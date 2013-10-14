#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import time
from time import sleep
import random
from game_utils import *

from Missions import *

class AI(BaseAI):

  history = None
  spawnTiles = []
  ourCollectionTrenches = []
  myPumpTiles = []
  myUnits = []
  
  unitAt = dict()
  
  missions = []
  
  threats = []
  threatThreshold = 0.5

  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Trey Nickelsen"

  @staticmethod
  def password():
    return "password"
  
  def getMyUnits(self):
    self.myUnits = [unit for unit in self.units if unit.owner == self.playerID]
  
  def cacheUnitPositions(self):
    self.unitAt = dict()
    for unit in self.units:
      self.unitAt[(unit.x,unit.y)] = unit
  
  def getUnitAt(self, x, y):
    if (x,y) in self.unitAt:
      return self.unitAt[(x,y)]
    else:
      return None
  
  def getTile(self, x, y):
    return self.tiles[x * self.mapHeight + y]
  
  def getSpawnTiles(self):
    for tile in self.tiles:
      if tile.owner == self.playerID:
        self.spawnTiles.append(tile)
    # Sort, closest to center first
    self.spawnTiles.sort(key=lambda tile: (self.mapWidth / 2) - tile.x)

  def findMyPumpTiles(self):
    pumpTiles = []
    for tile in self.tiles:
      if tile.pumpID != -1 and tile.owner == self.getPlayerID():
        pumpTiles.append(tile)
    return pumpTiles
    
  def findIce(self):
    ice = []
    for tile in self.tiles:
      if tile.owner == 3:
        if tile.x < getMapWidth() / 2:
          ice.append(tile)
    return ice
    
  def findNearestTile(self, x, y, tiles):
    return min(tiles, key = lambda tile: taxiDis(x, y, tile.x, tile.y))
    
  def spawnUnitCenter(self, type):
    for tile in self.spawnTiles:
      if tile.spawn(type):
        return True
      else:
        print('Spawn failed')
    return False
        
  def spawnUnitClosestTo(self, type, x, y):
    closestTile = sorted(tile.spawnTiles, key=lambda tile: taxiDis(x, y, tile.x, tile.y))
    for tile in closestTile:
      if tile.spawn(type):
        return True
    return False

  def getUnitClosestTo(self, x, y):
    closestUnits = sorted(
      [unit for unit in units if unit.owner == self.playerID],
      key=lambda unit: taxiDis(x, y, unit.x, unit.y))
    return closestUnits[0]
  
  # Returns of list of tuples (threat, threatLevel), most important first
  def identifyThreats(self):
    enemyUnits = [unit for unit in self.units if unit.owner != self.playerID]
    threatLevel = dict()
    for unit in enemyUnits:
      nearestPump = self.findNearestTile(unit.x, unit.y, self.myPumpTiles)
      nearestSpawn = self.findNearestTile(unit.x, unit.y, self.spawnTiles)
      distToPump = taxiDis(unit.x, unit.y, nearestPump.x, nearestPump.y)
      distToSpawn = taxiDis(unit.x, unit.y, nearestSpawn.x, nearestSpawn.y)
      if (distToPump == 0 or distToSpawn == 0):
        threatLevel[unit] = 2.0
      else:
        threatLevel[unit] = 1.0 / distToPump + 1.0 / distToSpawn
    # Smallest threat first
    return sorted([(unit, threatLevel[unit]) for unit in enemyUnits], key=lambda threat: threat[1]).reverse()

  ##This function is called once, before your first turn
  def init(self):
    self.getSpawnTiles()
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

    # Find my pumps, (in case they changed?)
    self.getSpawnTiles();
    self.myPumpTiles = self.findMyPumpTiles();
    self.getMyUnits()
    self.cacheUnitPositions()
    # Identify threats
    self.threats = self.identifyThreats()
    # Go after threats
    if self.threats is not None:
      for threat in self.threats:
        if threat[1] > self.threatThreshold:
          hero = self.getUnitClosestTo(threat[0].x, threat[0].y)
          self.missions.append(AttackMission(threat[1] * 5.0, self, hero, threat[0]))
           
    for mission in self.missions:
      mission.step()
      if (isinstance(mission, AttackMission)):
        pass

    # Remove missions that are done
    self.missions[:] = [mission for mission in self.missions if not mission.done]
    
    # Spawn units if we can
    if len(self.myUnits) < self.maxUnits - 1:
      self.spawnUnitCenter(DIGGER)

    #SNAPSHOT AT END
    self.history.save_snapshot()
    return 1

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
        # Calculate neighbor
        pos = map(operator.add, current, offset)
        neighbor = tuple(pos)
        if isOnMap(self, pos[0], pos[1] and (pos == goal or isValidTile(self.getTile(pos[0], pos[1])))):
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
  
  # Returns list of tiles
  def reconstructPath(self, came_from, current_node):
    if current_node in came_from:
      p = [reconstruct_path(came_from, came_from[current_node])]
      return p.append(current_node)
    else:
      return self.getTile(current_node[0], current_node[1])

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
