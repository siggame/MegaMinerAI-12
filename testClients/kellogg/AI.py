#-*-python-*-
from BaseAI import BaseAI
import random
import heapq
from GameObject import *

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"


  def removeGrid(self, target):
    self.grid[target.x][target.y].remove(target)
    
  def addGrid(self, x, y, target):
    self.grid[x][y].append(target)
      
  def adjacent(self, x, y):
    adj = []
    if x+1<self.mapWidth:
        adj.append((x+1,y))
    if y-1>=0:
        adj.append((x,y-1))
    if x-1>=0:
        adj.append((x-1,y))
    if y+1<self.mapHeight:
        adj.append((x,y+1))
    return adj
  
  def pathFind(self, startX, startY, goalX, goalY):
    closedSet = set();closedTup=set()
    # 0 = distance from goal, 1 = current (x,y), 2 = parent (x,y) 3 = distance from start
    open = [(self.distance(startX,startY,goalX,goalY),(startX,startY),(startX,startY),0)];openTup=[(startX,startY)]
    path = []
    while len(open)>0:
      current = heapq.heappop(open)
      if current[1] == (goalX,goalY):
        node = current
        path = []
        while node[2]!=(startX,startY):
          for closed in closedSet:
            if self.distance(node[1][0],node[1][1],closed[1][0],closed[1][1])==1 and node[2] == closed[1]:
              path.append(node[2])
              node = closed
        return path
      closedSet.add(current);closedTup.add(current[1])
      openTup.remove(current[1])
      for neighbor in self.adjacent(current[1][0],current[1][1]):#,[(startX,startY),(goalX,goalY)]):
       #game specific
       tile = self.getTile(neighbor[0],neighbor[1])
       unit = self.getUnit(neighbor[0],neighbor[1])
       ###
       if len(self.grid[neighbor[0]][neighbor[1]]) == 1 and tile.waterAmount < 1 and not(tile.pumpID == -1 and tile.owner == self.playerID^1):
        if neighbor in closedTup:
         continue
        g = current[3]+self.distance(neighbor[0],neighbor[1],current[1][0],current[1][1])
        if neighbor == (goalX,goalY) or self.distance(neighbor[0],neighbor[1],startX,startY)<=g+1 and neighbor not in openTup:
          neighborTup = (g+self.distance(neighbor[0],neighbor[1],goalX,goalY),(neighbor[0],neighbor[1]),(current[1]),g)
          heapq.heappush(open,neighborTup);openTup.append(neighbor)
    return None

  def moveTo(self, unit, target):
    next = None
    old = None
    path = self.pathFind(unit.x, unit.y, target.x, target.y)
    if path != None:
      while len(path) > 0 and unit.movementLeft > 0:
        old = next
        next = path.pop()
        if self.distance(unit.x, unit.y, next[0], next[1]) == 1:
          self.removeGrid(unit)
          unit.move(next[0], next[1])
          self.addGrid(unit.x, unit.y, unit)
      return True
    return False
  
  def findNearest(self,myDude, list):
    dis = 1000
    nearest = 1
    for mapp in list:
      if self.distance(myDude.x,myDude.y,mapp.x,mapp.y)<dis:
          nearest = mapp
    return nearest

  def takePump(self, unit, pumpStation):
    try:
      if isinstance(unit.missions["Siege"], Tile) and self.getUnit(unit.missions["Siege"]) is None:
        #print unit.missions
        self.moveTo(unit, unit.missions["Siege"])
    except AttributeError:
      #print "Unit hasn't been given a mission yet"
      unit.missions = {"Siege": None}

    if self.getTile(unit.x, unit.y).pumpID == pumpStation.id:
      return True
    tiles = [tile for tile in self.pumpTiles if tile.pumpID == pumpStation.id]
    target = None
    for tile in tiles:
      if self.getUnit(tile.x, tile.y) is None:
        target = tile

    if target is None:
      return False

    unit.missions["Siege"] = target
    self.moveTo(unit, target)
    return True
    
  def getTile(self, x, y):
    return self.grid[x][y][0]

  def getUnit(self, x, y):
    loc = self.grid[x][y]
    
    if len(loc) == 1:
      return None
    else:
     return loc[:1]

  def distance(self,x1,y1,x2,y2):
    return abs(x1-x2)+abs(y1-y2)

  ##This function is called once, before your first turn
  def init(self):
    self.myPlayer = self.players[self.playerID]
    self.pumpDict = {}
    self.myTiles = []
    self.enemyTiles = []
    self.pumpTiles = [tile for tile in self.tiles if tile.pumpID != -1]
    for tile in self.pumpTiles:
      self.pumpDict[tile.pumpID] = [pump for pump in self.pumpStations if pump.id == tile.pumpID][0]

    for tile in self.tiles:
      if tile.owner == self.playerID:
        self.myTiles.append(tile)
      elif tile.owner == self.playerID^1:
        self.enemyTiles.append(tile)

  ##This function is called once, after your last turn
  def end(self):
    pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    self.myTiles = []
    self.enemyTiles = []
    self.iceCaps = []
    self.myDudes = []
    self.enemyDudes = []
    self.myPumps = []
    self.enemyPumps = []
    self.grid = [[[] for x in range(self.mapHeight)] for y in range(self.mapWidth)]

    for thing in self.tiles + self.units:
      self.addGrid(thing.x, thing.y, thing)
      if isinstance(thing, Tile) and thing.waterAmount > 1:
        self.iceCaps.append(thing)
      elif isinstance(thing, Unit) and thing.owner == self.playerID:
        self.myDudes.append(thing)
      elif isinstance(thing, Unit) and thing.owner != self.playerID:
        self.enemyDudes.append(thing)
      elif isinstance(thing, Tile) and thing.pumpID != -1:
        pump = [pump for pump in self.pumpStations if pump.id == thing.pumpID][0]
        if pump.owner == self.playerID:
          self.myPumps.append(pump)
        else:
          self.enemyPumps.append(pump)

    for tile in self.tiles:
      if tile.owner == self.playerID:
        self.myTiles.append(tile)
      elif tile.owner == self.playerID^1:
        self.enemyTiles.append(tile)
    #use try catch for mission controls    
    for tile in self.myTiles:
      if self.myPlayer.oxygen >= self.unitTypes[0].cost:
        tile.spawn(0)

    for unit in self.myDudes:
      nearestPump = self.findNearest(unit, [tile for tile in self.pumpTiles if tile.owner == self.playerID^1 and self.getUnit(tile.x, tile.y) in [None, unit] ])
      #print nearestPump
      self.moveTo(unit, nearestPump)
#      self.takePump(unit, nearestPump)

    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
