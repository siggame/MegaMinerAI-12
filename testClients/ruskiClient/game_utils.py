import copy
import time
import sys

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
      
      if tile.owner == 0:
        if tile.pumpID == -1:
          self.notmoving[tile.x][tile.y].append(self.colorText('S', self.WHITE, self.RED))
        else:
          self.notmoving[tile.x][tile.y].append(self.colorText('P', self.GREEN, self.RED))
      elif tile.owner == 1:
        if tile.pumpID == -1:
          self.notmoving[tile.x][tile.y].append(self.colorText('S', self.WHITE, self.BLUE))
        else:
          self.notmoving[tile.x][tile.y].append(self.colorText('P', self.GREEN, self.BLUE))
        


    return

  def save_snapshot(self):
    tempGrid = copy.deepcopy(self.notmoving)

    for tile in self.ai.tiles:
      if tile.owner == 3:
        tempGrid[tile.x][tile.y].append(self.colorText('I', self.CYAN, self.WHITE))
      elif tile.waterAmount > 0:
        tempGrid[tile.x][tile.y].append(self.colorText(' ', self.WHITE, self.BLUE))
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
        else:
          sys.stdout.write(' ')
          sys.stdout.write(' ')
      print
    return

  def print_history(self):
    turnNumber = 0
    for snapshot in self.history:
      print(turnNumber/2)
      turnNumber += 1
      self.print_snapshot(snapshot)
      time.sleep(.1)

