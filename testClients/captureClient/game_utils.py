import copy
import time

import operator
import sys

from heapq import *

from AI import *

def getTile(ai, x, y):
  if x >= 0 and x < ai.mapWidth and y >= 0 and y < ai.mapHeight:
    return ai.tiles[x * ai.mapHeight + y]
  else:
    return None

def taxiDis(x1, y1, x2, y2):
  return abs(x1 - x2) + abs(y1 - y2)

def aStar(ai, start, goal, valid, cost):
  offsets = ((1,0),(0,1),(-1,0),(0,-1))

  closed_set = set()
  open_set = set()
  open_heap = []
  came_from = dict()
  
  g_scores = dict()
  f_scores = dict()
  thisAlgorithmBecomingSkynetCost = 9999999999
  
  g_scores[start] = 0
  f_scores[start] = g_scores[start] + taxiDis(start.x, start.x, goal.x, goal.y)

  heappush(open_heap, (f_scores[start], start))
  open_set.add(start)

  while open_set:
    f_score, current = heappop(open_heap)
    if current == goal:
      path = [current]
      while current in came_from:
        current = came_from[current]
        path.append(current)
      path.reverse()
      return path
    open_set.remove(current)
    closed_set.add(current)
    for offset in offsets:
      neighbor = getTile(ai, current.x + offset[0], current.y + offset[1])
      if neighbor is not None and (neighbor == goal or valid(current, neighbor)):
        tentative_g_score = g_scores[current] + cost(current, neighbor)
        tentative_f_score = tentative_g_score + taxiDis(neighbor.x, neighbor.y, goal.x, goal.y)
        if neighbor in closed_set and tentative_f_score >= f_scores[neighbor]:
          continue
        if neighbor not in open_set or tentative_f_score < f_scores[neighbor]:
          came_from[neighbor] = current
          g_scores[neighbor] = tentative_g_score
          f_scores[neighbor] = tentative_f_score
          if neighbor not in open_set:
            heappush(open_heap, (tentative_f_score, neighbor))
            open_set.add(neighbor)
  return None

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
        tempGrid[tile.x][tile.y].append([str(tile.owner), self.WHITE, self.GREEN])
        #tempGrid[tile.x][tile.y].append(self.colorText(str(tile.owner), self.WHITE, self.GREEN))

      #SPAWNS
      if tile.owner == 0:
        tempGrid[tile.x][tile.y].append(['S', self.WHITE, self.RED])
      elif tile.owner == 1:
        tempGrid[tile.x][tile.y].append(['S', self.WHITE, self.MAGENTA])

      #GLACIERS
      if tile.owner == 3 and tile.waterAmount > 0:
        tempGrid[tile.x][tile.y].append(['I', self.WHITE, self.CYAN])

      #WATER
      elif tile.waterAmount > 0:
        tempGrid[tile.x][tile.y].append([' ', self.WHITE, self.BLUE])

      #TRENCH
      elif tile.depth > 0:
        tempGrid[tile.x][tile.y].append([' ', self.WHITE, self.YELLOW])

    for unit in self.ai.units:
      symbol = ['W','S','T'][unit.type]
      color = [self.RED, self.MAGENTA][unit.owner]
      cell = tempGrid[unit.x][unit.y]
      if cell:
        cell[0][0] = symbol
        if cell[0][2] != color:
          cell[0][1] = color
      else:
        cell.append([symbol, color, self.BLACK])

    #self.print_snapshot(tempGrid)
    self.history.append(tempGrid)
    return

  def print_snapshot(self, snapshot):
    print('--' * self.ai.mapWidth)
    for y in range(self.ai.mapHeight):
      for x in range(self.ai.mapWidth):
        if snapshot[x][y]:
          str = self.colorText(snapshot[x][y][0][0], snapshot[x][y][0][1], snapshot[x][y][0][2])
          sys.stdout.write(str)
          sys.stdout.write(str)
        else:
          sys.stdout.write('  ')
      print
    return

  def print_history(self):
    turnNumber = 0
    for snapshot in self.history:
      print(turnNumber)
      turnNumber += 1
      self.print_snapshot(snapshot)
      time.sleep(.1)

