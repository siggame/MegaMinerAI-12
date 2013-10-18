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


  def findAvailableUnits(self):
    takenUnits = set()
    for mission in self.missions:
      if isinstance(mission, AttackMission):
        takenUnits.add(mission.hero)
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
    threatsTakenCareOf = set([mission.target for mission in self.missions if isinstance(mission, AttackMission)])
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
    return sorted([(unit, threatLevel[unit]) for unit in self.enemyUnits], key=lambda threat: -threat[1])



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
    self.enemyPumpTiles = getEnemyPumpTiles(self)

    self.unitByID = cacheUnitIDs(self)
    #self.enemyUnitPositions.append(recordEnemyPositions)

    self.unitAt = cacheUnitPositions(self)

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
            self.missions.append(AttackMission(threat[1] * 5.0, self, hero, threat[0]))
            self.availableUnits.remove(hero)
            break

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
      
    #SNAPSHOT AT END
    self.history.save_snapshot()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
