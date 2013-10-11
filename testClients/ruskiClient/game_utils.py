import copy
import time

DIGGER = 0
FILLER = 1

def get_tile(ai, x, y):
  return ai.tiles[x * ai.mapHeight + y]

class game_history:
  def __init__(self, ai, use_colors = False):
    self.use_colors = use_colors
    self.history = []
    self.ai = ai

    self.notmoving = None

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
      print(turnNumber/2)
      turnNumber += 1
      self.print_snapshot(snapshot)
      time.sleep(.1)

