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
  mySpawnTiles = []
  enemySpawnTiles = []
  myPumpTiles = []
  enemyPumpTiles = []
  myUnits = []
  enemyUnits = []
  # Distance from enemy spawn point
  dfes = dict()
  
  myCollectionTrenches = []
  
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

  def spawnUnitCenter(self, type):
    for tile in self.mySpawnTiles:
      if (tile.x, tile.y) not in unitAt:
        return tile.spawn(type)
    return False
        
  def spawnUnitClosestTo(self, type, x, y):
    closestTiles = findNearestTiles(self, x, y, self.mySpawnTiles)
    for tile in closestTiles:
      if (tile.x, tile.y) not in unitAt:
        return tile.spawn(type)
    return False
    
  def getEnoughToSpawn(self):
    return self.players[self.playerID].spawnResources < self.
    
  # Returns of list of tuples (threat, threatLevel), most important first
  def identifyThreats(self):
    enemyUnits = [unit for unit in self.units if unit.owner != self.playerID]
    threatLevel = dict()
    for unit in enemyUnits:
      nearestPump = self.findNearestTile(unit.x, unit.y, self.myPumpTiles)
      nearestSpawn = self.findNearestTile(unit.x, unit.y, self.mySpawnTiles)
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
    self.mySpawnTiles = getMySpawnTilesSortedCenterFirst(self)
    self.enemySpawnTiles = getEnemySpawnTilesSortedCenterFirst(self)
    self.dfes = calculateDistanceFromEnemySpawnsMinOnly(self)
    
    self.history = game_history(self, True)
    return

  ##This function is called once, after your last turn
  def end(self):
    self.history.print_history()
    return

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    print(self.turnNumber),
    #SNAPSHOT AT BEGINNING
    self.history.save_snapshot()

    self.myUnits = getMyUnits(self)
    self.enemyUnits = getEnemyUnits(self)
    self.myPumpTiles = getMyPumpTiles(self)
    self.enemyPumpTiles = getEnemyPumpTiles(self)
    
    self.unitAt = cacheUnitPositions(self)
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
      if self.spawnUnitCenter(DIGGER):
        print('Spawned Digger')
      
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
        if isOnMap(self, pos[0], pos[1] and (pos == goal or isValidTile(getTile(self, pos[0], pos[1])))):
          tentative_g_score = g_score[current] + tileCost(getTile(self, pos[0], pos[1]))
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
      return getTile(self, current_node[0], current_node[1])

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
