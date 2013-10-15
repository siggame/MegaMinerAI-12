import copy
import time

DIGGER = 0
FILLER = 1

offsets = ((1,0),(0,1),(-1,0),(0,-1))


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
    key=lambda tile: abs((ai.mapWidth / 2) - tile.x)):
    
def getEnemySpawnTilesSortedCenterFirst(ai):
  return sorted([tile for tile in ai.tiles if tile.owner != ai.playerID],
    key=lambda tile: abs((ai.mapWidth / 2) - tile.x)):

def calculateDistanceFromEnemySpawnsSum(ai):
  d = dict()
  for tile in ai.tiles:
    d[tile] = sum(taxiDis(tile.x, tile.y, spawn.x, spawn.y) for spawn in ai.enemySpawnTiles)
  return d
      
def calculateDistanceFromEnemySpawnsMinOnly(ai):
  d = dict()
  for tile in ai.tiles:
    d.[tile] = min(taxiDis(tile.x, tile.y, spawn.x, spawn.y) for spawn in ai.enemySpawnTiles)
  return d

def calculateSumInverseDistanceFromEnemyUnits(ai):
  d = dict()
  for tile in ai.tiles:
    d.[tile] = sum(taxiDis(tile.x, tile.y, unit.x, unit.y) for unit in ai.enemyUnits)
  return d
  
  
 
def findNearestTiles(x, y, tiles):
  return sorted(tile, key = lambda tile: taxiDis(x, y, tile.x, tile.y))

def findNearestTile(x, y, tiles):
  return min(tiles, key = lambda tile: taxiDis(x, y, tile.x, tile.y))
  
def getUnitsClosestTo(self, x, y):
  return sorted(myUnits, key=lambda unit: taxiDis(x, y, unit.x, unit.y))
  
def getUnitClosestTo(self, x, y):
  return max([()])
  closestUnits = sorted(
    [unit for unit in units if unit.owner == self.playerID],
    key=lambda unit: taxiDis(x, y, unit.x, unit.y))
  return closestUnits[0]
 
  
  
def getTile(ai, x, y):
  return ai.tiles[x * ai.mapHeight + y]
  
def taxiDis(x1, y1, x2, y2):
  return (abs(x2 - x1) + abs(y2 - y1))

def isOnMap(ai, x, y):
  return x >= 0 and x < ai.getMapWidth() and y >= 0 and y < ai.getMapHeight()
  
  
  
def validMove(ai, tile, healthLeft):
  if tile.owner != (self.getPlayerID()^1) and ai.getUnitAt(tile.x, tile.y) is None:
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

def costOfTrenchPath(ai, tile):
  if tile.isTrench:
    return 0.5 / (ai.dfes[tile]**2)
  return 1.0 / (ai.dfes[tile]**2)
  
    
  
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

