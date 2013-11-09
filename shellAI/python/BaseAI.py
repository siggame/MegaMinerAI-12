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
  pumpStations = []
  units = []
  tiles = []
  unitTypes = []
  #\cond
  def startTurn(self):
    from GameObject import Player
    from GameObject import Mappable
    from GameObject import PumpStation
    from GameObject import Unit
    from GameObject import Tile
    from GameObject import UnitType

    BaseAI.players = [Player(library.getPlayer(self.connection, i)) for i in xrange(library.getPlayerCount(self.connection))]
    BaseAI.mappables = [Mappable(library.getMappable(self.connection, i)) for i in xrange(library.getMappableCount(self.connection))]
    BaseAI.pumpStations = [PumpStation(library.getPumpStation(self.connection, i)) for i in xrange(library.getPumpStationCount(self.connection))]
    BaseAI.units = [Unit(library.getUnit(self.connection, i)) for i in xrange(library.getUnitCount(self.connection))]
    BaseAI.tiles = [Tile(library.getTile(self.connection, i)) for i in xrange(library.getTileCount(self.connection))]
    BaseAI.unitTypes = [UnitType(library.getUnitType(self.connection, i)) for i in xrange(library.getUnitTypeCount(self.connection))]

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
  def getMapWidth(self):
    return library.getMapWidth(self.connection)
  #\endcond
  mapWidth = property(getMapWidth)
  #\cond
  def getMapHeight(self):
    return library.getMapHeight(self.connection)
  #\endcond
  mapHeight = property(getMapHeight)
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
  def getMaxUnits(self):
    return library.getMaxUnits(self.connection)
  #\endcond
  maxUnits = property(getMaxUnits)
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
  #\cond
  def getMaxSiege(self):
    return library.getMaxSiege(self.connection)
  #\endcond
  maxSiege = property(getMaxSiege)
  #\cond
  def getOxygenRate(self):
    return library.getOxygenRate(self.connection)
  #\endcond
  oxygenRate = property(getOxygenRate)
  #\cond
  def getDepositionRate(self):
    return library.getDepositionRate(self.connection)
  #\endcond
  depositionRate = property(getDepositionRate)
  def __init__(self, connection):
    self.connection = connection
