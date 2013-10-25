#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

from game_utils import *

from Missions import *

class AI(BaseAI):

  history = None
  mySpawnTiles = []
  enemySpawnTiles = []
  myPumpTiles = []
  myPumpTilesSet = set()
  enemyPumpTiles = []
  myUnits = []
  enemyUnits = []
  # Distance from enemy spawn point
  dfes = dict()
  
  myCollectionTrenches = []

  unitByID = dict()
  unitAt = dict()
  
  missions = []
  availableUnits = []
  
  threats = []
  threatThreshold = 0.4
  
  neededTrenches = []
  
  enemyHistory = 5
  enemyUnitPositions = []

  spawnEgg = set()



  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Trey Nickelsen"

  @staticmethod
  def password():
    return "password"

  def findWaterwaysNeeded(self):
    # Tuples iceTile: (pumpTile, aStarPath)
    iceToPump = dict()
    
    # Find all the distance from every ice tile to the nearest pump
    for iceTile in [tile for tile in self.tiles if tile.owner == 3]:
      shortestPath = uniformCostSearch(self, iceTile.x, iceTile.y, 6,
        lambda tile: tile in self.myPumpTilesSet, # GOAL - find any of my pumps
        lambda tile: tile.owner == 2 or tile.owner == 3 or tile in self.myPumpTilesSet, # VALID - dirt or trench or ice
        lambda tile: not (tile.depth > 0 or tile.owner == 3))  # COST - 0 = trench or ice
      if shortestPath is not None:
        iceToPump[iceTile] = shortestPath
        print("Length of iceToPump: {}".format(len(shortestPath)))
    # Go through the path
    for iceTile, path in iceToPump.iteritems():
      # Check every tile in the path and see if it needs to be dug
      for pos in path:
        tile = getTile(self, pos[0], pos[1])
        # Keep track of which tiles are being used to transport water MY pumps (in case we want to defend them)
        if tile.depth > 0 and tile not in self.myCollectionTrenches:
          self.myCollectionTrenches.append(tile)
        # Need to dig here?
        if not tile.depth > 0 and tile.owner == 2:
          self.neededTrenches.append(tile)

  def findWaterwayTrenchesNeeded(self):
    pass

  def findAvailableUnits(self):
    takenUnits = set()
    for mission in self.missions:
      if isinstance(mission, AttackMission):
        if mission.heroID in self.unitByID:
          takenUnits.add(self.unitByID[mission.heroID])
      elif isinstance(mission, DigMission):
        if mission.heroID in self.unitByID:
          takenUnits.add(self.unitByID[mission.heroID])
    return [unit for unit in self.myUnits if unit not in takenUnits]

  def spawnUnitCenter(self, type):
    for tile in self.mySpawnTiles:
      if (tile.x, tile.y) not in self.unitAt and tile not in self.spawnEgg:
        self.spawnEgg.add(tile)
        tile.spawn(type)
    return False
        
  def spawnUnitClosestTo(self, type, x, y):
    closestTiles = findNearestTiles(x, y, self.mySpawnTiles)
    for tile in closestTiles:
      if (tile.x, tile.y) not in self.unitAt and tile not in self.spawnEgg:
        self.spawnEgg.add(tile)
        tile.spawn(type)
    return False
    
  def getEnoughToSpawn(self):
    return self.players[self.playerID].spawnResources < self.unitCost
    
  # Returns of list of tuples (threat, threatLevel), most important first
  def identifyThreats(self):
    threatLevel = dict()
    threatsTakenCareOf = set([self.unitByID[mission.targetID] for mission in self.missions if isinstance(mission, AttackMission) and mission.targetID in self.unitByID])
    possibleThreats = [unit for unit in self.enemyUnits if unit not in threatsTakenCareOf]
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
    self.mySpawnTiles = getMySpawnTilesSortedCenterFirst(self)
    self.enemySpawnTiles = getEnemySpawnTilesSortedCenterFirst(self)
    self.dfes = calculateDistanceFromEnemySpawnsMinOnly(self)
    
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

    self.myUnits = getMyUnits(self)
    self.enemyUnits = getEnemyUnits(self)
    self.myPumpTiles = getMyPumpTiles(self)
    self.myPumpTilesSet = set(self.myPumpTiles)
    self.enemyPumpTiles = getEnemyPumpTiles(self)

    self.unitByID = cacheUnitIDs(self)
    #self.enemyUnitPositions.append(recordEnemyPositions)

    self.unitAt = cacheUnitPositions(self)

    self.findWaterwaysNeeded()
    
    self.spawnEgg = set()
    self.availableUnits = self.findAvailableUnits()
    # Identify threats
    self.threats = self.identifyThreats()
    # Go after threats
    if self.threats is not None:
      for threat in self.threats:
        if threat[1] > self.threatThreshold:
          heros = getUnitsClosestToFromList(self.availableUnits, threat[0].x, threat[0].y)
          for hero in heros:
            print('Assigned mission {} -> {}'.format(hero.id, threat[0].id))
            self.missions.append(AttackMission(threat[1] * 5.0, self, hero.id, threat[0].id))
            self.availableUnits.remove(hero)
            break

    # Dig trenches
    for trench in self.neededTrenches:
      heros = getUnitsClosestToFromList(self.availableUnits, trench.x, trench.y)
      for hero in heros:
        print('Assigned dig mission {} -> ({},{})'.format(hero.id, trench.x, trench.y))
        self.missions.append(DigMission(1.0, self, hero.id, trench))
        self.availableUnits.remove(hero)
        break
            
    # Perform missions
    for mission in self.missions:
      mission.step()
      if (isinstance(mission, AttackMission)):
        pass

    # Remove missions that are done
    self.missions[:] = [mission for mission in self.missions if not mission.done]
    
    # Spawn units if we can
    if len(self.myUnits) < self.maxUnits - 1:
      if self.spawnUnitCenter(DIGGER):
        print('Spawned Digger')
      else:
        print('Maxunits at : {}'.format(self.maxUnits))
      
    #SNAPSHOT AT END
    self.history.save_snapshot()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
