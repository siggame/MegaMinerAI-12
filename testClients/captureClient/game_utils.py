import time

import sys
import random

from heapq import *

from AI import *

def getTile(ai, x, y):
  if x >= 0 and x < ai.mapWidth and y >= 0 and y < ai.mapHeight:
    return ai.tiles[x * ai.mapHeight + y]
  else:
    return None

def taxiDis(x1, y1, x2, y2):
  return abs(x1 - x2) + abs(y1 - y2)

def getDir(x1, y1, x2, y2):
  if abs(x2 - x1) > abs(y2 - y1):
    return (cmp(x2 - x1, 0), 0)
  else:
    return (0, cmp(y2 - y1, 0))

def getNearest(ai, start, goal, valid):
  open_list = [goal]
  open_set = set()
  closed_set = set()
  open_set.add(goal)
  while open_list:
    tile = open_list.pop()
    open_set.remove(tile)
    closed_set.add(tile)
    if valid(tile):
      return tile
    dir = getDir(goal.x, goal.y, start.x, start.y)
    if random.random() < 0.5:
      sideDir = (dir[1], dir[0])
    else:
      sideDir = (-dir[1], -dir[0])
    backDir = (-dir[0], -dir[1])
    nextTile = getTile(ai, tile.x + dir[0], tile.y + dir[1])
    if nextTile is not None and nextTile not in closed_set and nextTile not in open_set:
      if valid(nextTile):
        return nextTile
      else:
        open_list.append(nextTile)
        open_set.add(nextTile)
  return None


def aStar(ai, start, goal, valid, cost):
  offsets = ((1,0),(0,1),(-1,0),(0,-1))

  genesis = time.clock()

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
    if time.clock() - genesis > 0.1:
      print('A* timed out')
      return None
    f_score, current = heappop(open_heap)
    if current == goal:
      path = [current]
      while current in came_from:
        if time.clock() - genesis > 0.1:
          print('A* restructure timed out')
          return None
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



import os
_proc_status = '/proc/%d/status' % os.getpid()

_scale = {'kB': 1024.0, 'mB': 1024.0*1024.0,
          'KB': 1024.0, 'MB': 1024.0*1024.0}

def _VmB(VmKey):
    '''Private.
    '''
    global _proc_status, _scale
     # get pseudo file  /proc/<pid>/status
    try:
        t = open(_proc_status)
        v = t.read()
        t.close()
    except:
        return 0.0  # non-Linux?
     # get VmKey line e.g. 'VmRSS:  9999  kB\n ...'
    i = v.index(VmKey)
    v = v[i:].split(None, 3)  # whitespace
    if len(v) < 3:
        return 0.0  # invalid format?
     # convert Vm value to bytes
    return float(v[1]) * _scale[v[2]]


def memory(since=0.0):
    '''Return memory usage in bytes.
    '''
    return _VmB('VmSize:') - since


def resident(since=0.0):
    '''Return resident memory usage in bytes.
    '''
    return _VmB('VmRSS:') - since


def stacksize(since=0.0):
    '''Return stack size in bytes.
    '''
    return _VmB('VmStk:') - since
