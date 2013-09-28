# -*- python -*-

from library import library

class BaseAI:
  """@brief A basic AI interface.

  This class implements most the code an AI would need to interface with the lower-level game code.
  AIs should extend this class to get a lot of builer-plate code out of the way
  The provided AI class does just that.
  """
  #\cond
  initialized = False
  iteration = 0
  runGenerator = None
  connection = None
  #\endcond
  players = []
  mappables = []
  units = []
  pumpStations = []
  tiles = []
  #\cond
  def startTurn(self):
    from GameObject import Player
    from GameObject import Mappable
    from GameObject import Unit
    from GameObject import PumpStation
    from GameObject import Tile

    BaseAI.players = [Player(library.getPlayer(self.connection, i)) for i in xrange(library.getPlayerCount(self.connection))]
    BaseAI.mappables = [Mappable(library.getMappable(self.connection, i)) for i in xrange(library.getMappableCount(self.connection))]
    BaseAI.units = [Unit(library.getUnit(self.connection, i)) for i in xrange(library.getUnitCount(self.connection))]
    BaseAI.pumpStations = [PumpStation(library.getPumpStation(self.connection, i)) for i in xrange(library.getPumpStationCount(self.connection))]
    BaseAI.tiles = [Tile(library.getTile(self.connection, i)) for i in xrange(library.getTileCount(self.connection))]

    if not self.initialized:
      self.initialized = True
      self.init()
    BaseAI.iteration += 1;
    if self.runGenerator:
      try:
        return self.runGenerator.next()
      except StopIteration:
        self.runGenerator = None
    r = self.run()
    if hasattr(r, '__iter__'):
      self.runGenerator = r
      return r.next()
    return r
  #\endcond
  #\cond
  def getMaxHealth(self):
    return library.getMaxHealth(self.connection)
  #\endcond
  maxHealth = property(getMaxHealth)
  #\cond
  def getTrenchDamage(self):
    return library.getTrenchDamage(self.connection)
  #\endcond
  trenchDamage = property(getTrenchDamage)
  #\cond
  def getWaterDamage(self):
    return library.getWaterDamage(self.connection)
  #\endcond
  waterDamage = property(getWaterDamage)
  #\cond
  def getTurnNumber(self):
    return library.getTurnNumber(self.connection)
  #\endcond
  turnNumber = property(getTurnNumber)
  #\cond
  def getAttackDamage(self):
    return library.getAttackDamage(self.connection)
  #\endcond
  attackDamage = property(getAttackDamage)
  #\cond
  def getOffenseCount(self):
    return library.getOffenseCount(self.connection)
  #\endcond
  offenseCount = property(getOffenseCount)
  #\cond
  def getDefenseCount(self):
    return library.getDefenseCount(self.connection)
  #\endcond
  defenseCount = property(getDefenseCount)
  #\cond
  def getMaxUnits(self):
    return library.getMaxUnits(self.connection)
  #\endcond
  maxUnits = property(getMaxUnits)
  #\cond
  def getUnitCost(self):
    return library.getUnitCost(self.connection)
  #\endcond
  unitCost = property(getUnitCost)
  #\cond
  def getPlayerID(self):
    return library.getPlayerID(self.connection)
  #\endcond
  playerID = property(getPlayerID)
  #\cond
  def getGameNumber(self):
    return library.getGameNumber(self.connection)
  #\endcond
  gameNumber = property(getGameNumber)
  def __init__(self, connection):
    self.connection = connection
