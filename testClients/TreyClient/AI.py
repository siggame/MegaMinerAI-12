#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

from game_utils import *

import time
import copy

WORKER, SCOUT, TANK = range(3)

class AI(BaseAI):

  history = None
  # Distance from enemy spawn point
  dfes = dict()
  
  myCollectionTrenches = []
  missions = []
  availableUnits = []
  threats = []
  threatThreshold = 0.4
  neededTrenches = []
  enemyHistory = 5
  enemyUnitPositions = []
  spawnEgg = set()

  # CONFIG
  numDiggers = 1
  numCapturers = 5
  numDefenderTanks = 4
  numDefenderScouts = 2


  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Trey Nickelsen"

  @staticmethod
  def password():
    return "password"

  def findWaterwaysNeeded(self):
    self.neededTrenches = []
    iceToPump = dict()
    genesis = time.clock()
    # Find all the distance from every ice tile to the nearest pump
    for iceTile in [tile for tile in self.tiles if tile.owner == 3]:
      shortestPath = uniformCostSearch(self, iceTile.x, iceTile.y, 6,
        lambda tile: tile in self.myPumpTilesSet, # GOAL - find any of my pumps
        lambda tile: tile.owner == 2 or tile.owner == 3 or tile in self.myPumpTilesSet, # VALID - dirt or trench or ice
        lambda tile: not (tile.depth > 0 or tile.owner == 3))  # COST - 0 = trench or ice
      if shortestPath is not None:
        iceToPump[iceTile] = shortestPath
    # Go through the path
    for iceTile, path in iceToPump.iteritems():
      # Check every tile in the path and see if it needs to be dug
      for pos in path:
        tile = getTile(self, pos[0], pos[1])
        # Keep track of which tiles are being used to transport water MY pumps (in case we want to defend them)
        if tile.depth > 0 and tile not in self.myCollectionTrenches:
          self.myCollectionTrenches.append(tile)
        # Need to dig here?
        if tile.depth <= 0 and tile.owner == 2 and tile not in self.neededTrenches:
          self.neededTrenches.append(tile)
    if time.clock() - genesis > 0.1:
      print('Waterway time warning {}'.format(time.clock() - genesis))

  def spawnUnitCenter(self, type):
    if self.players[self.playerID].oxygen < self.unitTypeIDToType[type].cost:
      return False
    for tile in self.mySpawnTiles:
      if (tile.x, tile.y) not in self.unitAt and tile not in self.spawnEgg:
        result = tile.spawn(type)
        if (result != 1):
          print('Error {} spawning unit'.format(result))
        else:
          self.spawnEgg.add(tile)
    return False
        
  def spawnUnitClosestTo(self, type, x, y):
    if self.players[self.playerID].oxygen < self.unitTypeIDToType[type].cost:
      return False
    closestTiles = findNearestTiles(x, y, self.mySpawnTiles)
    for tile in closestTiles:
      if (tile.x, tile.y) not in self.unitAt and tile not in self.spawnEgg:
        result = tile.spawn(type)
        if (result != 1):
          print('Error {} spawning unit'.format(result))
        else:
          self.spawnEgg.add(tile)
    return False
    
  # Returns of list of tuples (threat, threatLevel), most important first
  def identifyThreats(self):
    threatLevel = dict()
    possibleThreats = self.enemyUnits
    for unit in possibleThreats:
      nearestPump = findNearestTile(unit.x, unit.y, self.myPumpTiles)
      nearestSpawn = findNearestTile(unit.x, unit.y, self.mySpawnTiles)
      distToPump = taxiDis(unit.x, unit.y, nearestPump.x, nearestPump.y)
      distToSpawn = taxiDis(unit.x, unit.y, nearestSpawn.x, nearestSpawn.y)
      if (distToPump == 0 or distToSpawn == 0):
        threatLevel[unit] = 2.0
      else:
        threatLevel[unit] = 1.0 / distToPump + 1.0 / distToSpawn
    # Smallest threat first
    return sorted([(unit, threatLevel[unit]) for unit in possibleThreats], key=lambda threat: -threat[1])

  ##This function is called once, before your first turn
  def init(self):
    self.squatMission = [] # Sit on pump
    self.defendMission = [] # Go after enemies near our base
    self.digMission = [] # Connect Ice to pumps
    self.conquerMission = [] # Attack towards enemy Pump/Spawn
    self.infiltrateMission = [] # Sneak to enemy pump (Scouts)
    self.fillMission = [] # Fill in trench tile

    self.guessEnemySpawn = [] # Holds tiles of most likely enemy spawns (first most likely)
    self.guessEnemyTarget = [] # Holds tiles most likely to be targeted by enemy (first most likely), Usually pump tiles
    self.enemyPreviousPositions = dict() # {ID : tile} holds previous tile position for enemy units

    self.unitTypeToTypeName = dict()
    self.unitTypeNameToType = dict()
    self.unitTypeIDToType = dict()
    for unitType in self.unitTypes:
      self.unitTypeToTypeName[unitType] = unitType.name
      self.unitTypeNameToType[unitType.name] = unitType
      self.unitTypeIDToType[unitType.type] = unitType

    self.unitAt = dict() # {(x, y): unit} Cached unit positions
    self.unitByID = dict() # {id : unit} Cached unit ids
    self.myUnitAt = dict() # {(x, y): unit} Cached my unit positions
    self.enemyUnitAt = dict() # {(x, y): unit} Cached enemy unit positions
    self.myUnits = [] # List of my units
    self.myUnitsByType = {unitType:[] for unitType in self.unitTypes} # {unitType: []} Dict of lists of units of a certain unitType
    self.enemyUnits = [] # List of enemy units

    self.myPumpTiles = [] # List of my pump tiles
    self.myPumpTilesSet = set() # Set of my pump tiles
    self.enemyPumpTiles = [] # List of enemy pump tiles
    self.iceTiles = [] # List of ice tiles
    self.myOpenSpawnTiles = [] # List of my spawnable tiles
    self.pumpTilesByPumpID = {pump.id:[] for pump in self.pumpStations} # {pumpID: []} Dict of lists of tiles belonging to a pump
    self.trenchTiles = [] # List of trench tiles

    self.mySpawnTiles = getMySpawnTilesSortedCenterFirst(self)
    self.enemySpawnTiles = getEnemySpawnTilesSortedCenterFirst(self)
    self.dfes = calculateDistanceFromEnemySpawnsMinOnly(self)

    self.emptyGrid = [[0 for y in xrange(self.mapHeight)] for _ in xrange(self.mapWidth)]
    self.enemyDamageGrid = copy.copy(self.emptyGrid) # The maximum amount of damage the enemy could inflict on a unit at a given position on the enemy's next turn

    self.history = game_history(self, True)
    return

  ##This function is called once, after your last turn
  def end(self):
    self.history.print_history()
    return

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    print(self.turnNumber)
    #SNAPSHOT AT BEGINNING
    self.history.save_snapshot()

    self.unitAt = dict()
    self.unitByID = dict()
    self.myUnitAt = dict()
    self.enemyUnitAt = dict()
    self.enemyDamageGrid = copy.copy(self.emptyGrid)
    self.myUnits = []
    self.myUnitsByType = {unitType:[] for unitType in self.unitTypes}
    self.enemyUnits = []
    for unit in self.units:
      posTuple = (unit.x, unit.y)
      self.unitAt[posTuple] = unit
      self.unitByID[unit.id] = unit
      if unit.owner == self.playerID:
        self.myUnitAt[posTuple] = unit
        self.myUnits.append(unit)
        self.myUnitsByType[self.unitTypeIDToType[unit.type]].append(unit)
      elif unit.owner == (self.playerID^1):
        self.enemyUnitAt[posTuple] = unit
        self.enemyUnits.append(unit)
      # Calculate danger grid thingy
      for y in xrange(max(unit.y - unit.range - unit.maxMovement, 0), min(unit.y + unit.range + unit.maxMovement, self.mapHeight - 1)):
        for x in xrange(max(unit.x - unit.range - unit.maxMovement, 0), min(unit.x + unit.range + unit.maxMovement, self.mapWidth - 1)):
          if taxiDis(unit.x, unit.y, x, y) <= unit.range + unit.maxMovement:
            self.enemyDamageGrid[x][y] += unit.attackPower

    self.myPumpTiles = []
    self.myPumpTilesSet = set()
    self.enemyPumpTiles = []
    self.iceTiles = []
    self.myOpenSpawnTiles = []
    self.pumpTilesByPumpID = {pump.id:[] for pump in self.pumpStations}
    self.trenchTiles = []
    for tile in self.tiles:
      if tile.owner == self.playerID:
        if (tile.x, tile.y) not in self.unitAt:
          self.myOpenSpawnTiles.append(tile)
      if tile.pumpID != -1:
        self.pumpTilesByPumpID[tile.pumpID].append(tile)
        if tile.owner == self.playerID:
          self.myPumpTiles.append(tile)
          self.myPumpTilesSet.add(tile)
        elif tile.owner == (self.playerID^1):
          self.enemyPumpTiles.append(tile)
      elif tile.owner == 3:
        self.iceTiles.append(tile)
      elif tile.depth > 0:
        self.trenchTiles.append(tile)
    self.myOpenSpawnTiles.sort(key = lambda tile: abs(self.mapWidth / 2) - tile.x)

    self.findWaterwaysNeeded()
    self.badTrenchTiles = list(set(self.trenchTiles) - set(self.myCollectionTrenches)) # Weird

    self.spawnEgg = set()

    self.availableUnits = list(set(self.myUnits)
      - set(map(lambda unitID: self.unitByID[unitID], self.squatMission))
      - set(map(lambda unitID: self.unitByID[unitID], self.defendMission))
      - set(map(lambda unitID: self.unitByID[unitID], self.digMission))
      - set(map(lambda unitID: self.unitByID[unitID], self.conquerMission))
      - set(map(lambda unitID: self.unitByID[unitID], self.infiltrateMission))
      - set(map(lambda unitID: self.unitByID[unitID], self.fillMission)))
    self.threats = self.identifyThreats()

    


    self.enemyPreviousPositions = dict()
    for unit in self.units:
      if unit.owner == (self.playerID^1):
        self.enemyPreviousPositions[unit.id] = getTile(self, unit.x, unit.y)

    #SNAPSHOT AT END
    self.history.save_snapshot()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
