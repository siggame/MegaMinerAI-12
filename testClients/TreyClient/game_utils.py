import copy
import time
import sys

DIGGER = 0
FILLER = 1

offsets = ((1,0),(0,1),(-1,0),(0,-1))

def taxiDis(x1, y1, x2, y2):
  return (abs(x2 - x1) + abs(y2 - y1))

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

def isOnMap(ai, x, y):
  return x >= 0 and x < ai.getMapWidth() and y >= 0 and y < ai.getMapHeight()

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
          sys.stdout.write(snapshot[x][y][0])
          sys.stdout.write(snapshot[x][y][0])
          #print(snapshot[x][y][0]),
        else:
          sys.stdout.write(' ')
          sys.stdout.write(' ')
          #print(' '),
      print
    return

  def print_history(self):
    turnNumber = 0
    for snapshot in self.history:
      print(turnNumber)
      turnNumber += 1
      self.print_snapshot(snapshot)
      time.sleep(.1)
