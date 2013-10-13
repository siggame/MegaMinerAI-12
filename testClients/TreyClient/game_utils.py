import copy
import time

DIGGER = 0
FILLER = 1

<<<<<<< HEAD
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
 
=======
def get_tile(ai, x, y):
  return ai.tiles[x * ai.mapHeight + y]

>>>>>>> origin/TreyAI
class game_history:
  def __init__(self, ai, use_colors = False):
    self.use_colors = use_colors
    self.history = []
    self.ai = ai

<<<<<<< HEAD
=======
    self.notmoving = None

>>>>>>> origin/TreyAI
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

<<<<<<< HEAD
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
=======
  def set_nonmoving_elements(self):
    self.notmoving = [[[] for _ in range( self.ai.mapHeight ) ] for _ in range( self.ai.mapWidth ) ]

    for tile in self.ai.tiles:
      #Assume tile.type == 1 means ICE
      if tile.owner == 3:
        self.notmoving[tile.x][tile.y].append(self.colorText('I', self.CYAN, self.WHITE))
      elif tile.owner == 0:
        self.notmoving[tile.x][tile.y].append(self.colorText('S', self.WHITE, self.RED))
      elif tile.owner == 1:
        self.notmoving[tile.x][tile.y].append(self.colorText('S', self.WHITE, self.BLUE))

    for pump in self.ai.pumpStations:
      if pump.owner == 0:
        self.notmoving[pump.x][pump.y].append(self.colorText('P', self.GREEN))
      elif pump.owner == 1:
        self.notmoving[pump.x][pump.y].append(self.colorText('p', self.GREEN))

    return

  def save_snapshot(self):
    tempGrid = copy.deepcopy(self.notmoving)

    for tile in self.ai.tiles:
      if tile.waterAmount > 0:
        tempGrid[tile.x][tile.y].append(self.colorText(' ', self.WHITE, self.BLUE))
      if tile.isTrench == 1:
>>>>>>> origin/TreyAI
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
<<<<<<< HEAD
          print(snapshot[x][y][0]),
=======
            print(snapshot[x][y][0]),
>>>>>>> origin/TreyAI
        else:
          print(' '),
      print
    return

  def print_history(self):
    turnNumber = 0
    for snapshot in self.history:
<<<<<<< HEAD
      print(turnNumber)
=======
      print(turnNumber/2)
>>>>>>> origin/TreyAI
      turnNumber += 1
      self.print_snapshot(snapshot)
      time.sleep(.1)

