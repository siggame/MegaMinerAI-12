import copy
import time

import operator

from heapq import *

from AI import *

DIGGER = 0
FILLER = 1

offsets = ((1,0),(0,1),(-1,0),(0,-1))


def cacheUnitIDs(ai):
  d = dict()
  for unit in ai.units:
    d[unit.id] = unit
  return d

def getMyPumpTiles(ai):
  return [tile for tile in ai.tiles if tile.pumpID != -1 and tile.owner == ai.playerID]

def getEnemyPumpTiles(ai):
  return [tile for tile in ai.tiles if tile.pumpID != -1 and tile.owner != ai.playerID]
  
def getMyUnits(ai):
  return [unit for unit in ai.units if unit.owner == ai.playerID]

def getEnemyUnits(ai):
  return [unit for unit in ai.units if unit.owner != ai.playerID]
  
def cacheUnitPositions(ai):
  d = dict()
  for unit in ai.units:
    d[(unit.x,unit.y)] = unit
  return d

def getMySpawnTilesSortedCenterFirst(ai):
  return sorted([tile for tile in ai.tiles if tile.owner == ai.playerID],
    key=lambda tile: abs((ai.mapWidth / 2) - tile.x))
    
def getEnemySpawnTilesSortedCenterFirst(ai):
  return sorted([tile for tile in ai.tiles if tile.owner != ai.playerID],
    key=lambda tile: abs((ai.mapWidth / 2) - tile.x))

def calculateDistanceFromEnemySpawnsSum(ai):
  d = dict()
  for tile in ai.tiles:
    d[tile] = sum(taxiDis(tile.x, tile.y, spawn.x, spawn.y) for spawn in ai.enemySpawnTiles)
  return d
      
def calculateDistanceFromEnemySpawnsMinOnly(ai):
  d = dict()
  for tile in ai.tiles:
    d[tile] = min(taxiDis(tile.x, tile.y, spawn.x, spawn.y) for spawn in ai.enemySpawnTiles)
  return d

def calculateSumInverseDistanceFromEnemyUnits(ai):
  d = dict()
  for tile in ai.tiles:
    d[tile] = sum(taxiDis(tile.x, tile.y, unit.x, unit.y) for unit in ai.enemyUnits)
  return d

def recordEnemyPositions(ai):
  ## Returns a dict of unit-position pairs
  d = dict()
  for unit in ai.enemyUnits:
    d[unit] = (unit.x, unit.y)
    

  
def calculateInterceptPosition(ai, hero, target):
  targetPos = (target.x, target.y)
  if len(ai.enemyUnitPositions) >= 1 and target in ai.enemyUnitPositions[-1]:
    if len(ai.enemyUnitPositions) >= 2 and target in ai.enemyUnitPositions[-2]:
      targetPos = 2 * target.x - ai.enemyUnitPositions[-2][target][0] , 2 * target.y - ai.enemyUnitPositions[-2][target][1]
    else:
      targetPos = 2 * target.x - ai.enemyUnitPositions[-1][target][0] , 2 * target.y - ai.enemyUnitPositions[-1][target][1]
  return targetPos

def vectorToGrid(x, y):
  if (abs(x) > abs(y)):
    return (cmp(x, 0), 0)
  else:
    return (0, cmp(y, 0))

def findNearestTiles(x, y, tiles):
  return sorted(tiles, key = lambda tile: taxiDis(x, y, tile.x, tile.y))

def findNearestTile(x, y, tiles):
  return min(tiles, key = lambda tile: taxiDis(x, y, tile.x, tile.y))
  
def getUnitsClosestTo(ai, x, y):
  return sorted(ai.myUnits, key=lambda unit: taxiDis(x, y, unit.x, unit.y))

def getUnitsClosestToFromList(units, x, y):
  return sorted(units, key=lambda unit: taxiDis(x, y, unit.x, unit.y))

def getUnitClosestTo(ai, x, y):
  return min(ai.myUnits, key=lambda unit: taxiDis(x, y, unit.x, unit.y))



def getTile(ai, x, y):
  return ai.tiles[x * ai.mapHeight + y]
  
def taxiDis(x1, y1, x2, y2):
  return (abs(x2 - x1) + abs(y2 - y1))

def isOnMap(ai, x, y):
  return x >= 0 and x < ai.mapWidth and y >= 0 and y < ai.mapHeight



def validMove(ai, tile, healthLeft):
  if tile.pumpID == -1 and tile.owner != (ai.getPlayerID()^1) and (tile.x, tile.y) not in ai.unitAt:
    if tile.isTrench:
      if (tile.waterAmount > 0):
        return healthLeft > ai.getWaterDamage()
      else:
        return healthLeft > ai.getTrenchDamage()
    else:
      return 1
  else:
    return 0

def costOfMove(ai, tile, healthLeft):
  if (tile.isTrench):
    if (tile.waterAmount > 0):
      return float(ai.getWaterDamage()) / healthLeft
    else:
      return float(ai.getTrenchDamage()) / healthLeft
  else:
    return 0.0

def validTrench(ai, tile):
  if tile.pumpID == -1 and tile.owner == 2:
    return 1
  return 0
    
def costOfTrenchPath(ai, tile):
  if tile.isTrench:
    return 0.5 / (ai.dfes[tile]**2)
  return 1.0 / (ai.dfes[tile]**2)
  


def aStar(ai, startX, startY, goalX, goalY, isValidTile, tileCost):
  offsets = ((1,0),(0,1),(-1,0),(0,-1))

  start = (startX, startY)
  goal = (goalX, goalY)
  
  closed = set()
  open = [start]
  cameFrom = dict()
  
  g_score = dict()
  f_score = dict()
  thisAlgorithmBecomingSkynetCost = 9999999999
  
  g_score[start] = 0 # Cost from start along best known path.
  # Estimated total cost from start to goal through y.
  f_score[start] = g_score[start] + taxiDis(startX, startY, goalX, goalY)
     
  while len(open) > 0:
    # Black Magic ahead
    current = min(open, key = lambda obj: f_score[obj]) # the node in open set having the lowest f_score[] value
    if current == goal:
      return reconstructPath(cameFrom, goal)
     
    open.remove(current) # remove current from open set
    closed.add(current)
    
    for offset in offsets:
      # Calculate neighbor
      pos = map(operator.add, current, offset)
      neighbor = tuple(pos)
      if isOnMap(ai, pos[0], pos[1]) and (neighbor == goal or isValidTile(getTile(ai, pos[0], pos[1]))):
        tentative_g_score = g_score[current] + tileCost(getTile(ai, pos[0], pos[1]))
        tentative_f_score = tentative_g_score + taxiDis(neighbor[0], neighbor[1], goal[0], goal[1])
        if neighbor in closed and tentative_f_score >= f_score[neighbor]:
          continue
        if neighbor not in open or tentative_f_score < f_score[neighbor]:
          cameFrom[neighbor] = current
          g_score[neighbor] = tentative_g_score
          f_score[neighbor] = tentative_f_score
          if neighbor not in open:
            open.append(neighbor)
  print('aStar failed!')
  return None

# Returns list of 2-tuples
def reconstructPath(came_from, current_node):
  if current_node in came_from:
    p = reconstructPath(came_from, came_from[current_node])
    p.append(current_node)
    return p
  else:
    return [current_node]

def uniformCostSearch(ai, startX, startY, goalCondition, isValidTile, tileCost):
  node = (0, (startX, startY))
  frontier = [] #:= priority queue containing node only
  heappush(frontier, node)
  explored = set()  # empty set
  cameFrom = dict()
  while len(frontier) > 0:
    node = heappop(frontier)   #node := frontier.pop()
    if goalCondition(getTile(ai, node[1][0], node[1][1])):
      return uniformCostSearchSolution(cameFrom, node)
    explored.add(node)
    for offset in offsets: #for each of node's neighbors n
      pos = (node[1][0] + offset[0], node[1][1] + offset[1])
      if isOnMap(ai, pos[0], pos[1]) and isValidTile(getTile(ai, pos[0], pos[1])):
        neighbor = (node[0] + tileCost(pos), pos)
        if neighbor not in explored:  #if n is not in explored
          if neighbor not in frontier:  #if n is not in frontier
            heappush(frontier, neighbor)#frontier.add(n)
          else:   #else if n is in frontier with higher cost
            for index, frontierNode in enumerate(frontier):
              if frontierNode[0] > neighbor[0]:
                frontier[index] = neighbor  #replace existing node with n
                break
  return None

# Returns list of 2-tuples
def uniformCostSearchSolution(cameFrom, current):
  if current in cameFrom:
    p = uniformCostSearchSolution(cameFrom, cameFrom[current])
    p.append(current[1])
  else:
    return [current[1]]

class game_history:
  def __init__(self, ai, use_colors = False):
    self.use_colors = use_colors
    self.history = []
    self.ai = ai

    self.BLACK = 0
    self.RED = 1
    self.GREEN = 2
    self.YELLOW = 3
    self.BLUE = 4
    self.MAGENTA = 5
    self.CYAN = 6
    self.WHITE = 7

    #SET UP THE PARTS THAT ARE NOT MOVING
  def colorText(self, text, fgcolor = None, bgcolor = None):
    if self.use_colors and fgcolor and bgcolor:
      return '\x1b[3{};4{};1m'.format(fgcolor, bgcolor) + text + '\x1b[0m'
    elif self.use_colors and fgcolor:
      return '\x1b[3{};1m'.format(fgcolor) + text + '\x1b[0m'
    else:
      return text

  def save_snapshot(self):
    tempGrid = [[[] for _ in range( self.ai.mapHeight ) ] for _ in range( self.ai.mapWidth ) ]

    for tile in self.ai.tiles:

      #PUMPS
      if tile.pumpID != -1:
        tempGrid[tile.x][tile.y].append(self.colorText(str(tile.owner), self.WHITE, self.GREEN))

      #SPAWNS
      if tile.owner == 0:
        tempGrid[tile.x][tile.y].append(self.colorText('S', self.WHITE, self.RED))
      elif tile.owner == 1:
        tempGrid[tile.x][tile.y].append(self.colorText('S', self.WHITE, self.BLUE))

      #GLACIERS
      if tile.owner == 3 and tile.waterAmount > 0:
        tempGrid[tile.x][tile.y].append(self.colorText('I', self.CYAN, self.WHITE))

      #WATER
      elif tile.waterAmount > 0:
        tempGrid[tile.x][tile.y].append(self.colorText(' ', self.WHITE, self.BLUE))

      #TRENCH
      elif tile.isTrench == 1:
        tempGrid[tile.x][tile.y].append(self.colorText(' ', self.WHITE, self.YELLOW))

    for unit in self.ai.units:
      if unit.owner == 0:
        if unit.type == DIGGER:
          tempGrid[unit.x][unit.y].append(self.colorText('D', self.RED, self.BLACK))
        elif unit.type == FILLER:
          tempGrid[unit.x][unit.y].append(self.colorText('F', self.RED, self.BLACK))
      elif unit.owner == 1:
        if unit.type == DIGGER:
          tempGrid[unit.x][unit.y].append(self.colorText('D', self.BLUE, self.BLACK))
        elif unit.type == FILLER:
          tempGrid[unit.x][unit.y].append(self.colorText('F', self.BLUE, self.BLACK))

    #self.print_snapshot(tempGrid)
    self.history.append(tempGrid)
    return

  def print_snapshot(self, snapshot):
    print('--' * self.ai.mapWidth)
    for y in range(self.ai.mapHeight):
      for x in range(self.ai.mapWidth):
        if len(snapshot[x][y]) > 0:
          print(snapshot[x][y][0]),
        else:
          print(' '),
      print
    return

  def print_history(self):
    turnNumber = 0
    for snapshot in self.history:
      print(turnNumber)
      turnNumber += 1
      self.print_snapshot(snapshot)
      time.sleep(.1)

