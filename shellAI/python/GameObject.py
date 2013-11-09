# -*- python -*-

from library import library

from ExistentialError import ExistentialError

class GameObject(object):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration


##
class Player(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.playerGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.players:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  ##Allows a player to display messages on the screen
  def talk(self, message):
    self.validify()
    return library.playerTalk(self._ptr, message)

  #\cond
  def getId(self):
    self.validify()
    return library.playerGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getPlayerName(self):
    self.validify()
    return library.playerGetPlayerName(self._ptr)
  #\endcond
  ##Player's Name
  playerName = property(getPlayerName)

  #\cond
  def getTime(self):
    self.validify()
    return library.playerGetTime(self._ptr)
  #\endcond
  ##Time remaining, updated at start of turn
  time = property(getTime)

  #\cond
  def getWaterStored(self):
    self.validify()
    return library.playerGetWaterStored(self._ptr)
  #\endcond
  ##The amount of water a player has.
  waterStored = property(getWaterStored)

  #\cond
  def getOxygen(self):
    self.validify()
    return library.playerGetOxygen(self._ptr)
  #\endcond
  ##Resource used to spawn in units.
  oxygen = property(getOxygen)

  #\cond
  def getMaxOxygen(self):
    self.validify()
    return library.playerGetMaxOxygen(self._ptr)
  #\endcond
  ##The player's oxygen cap.
  maxOxygen = property(getMaxOxygen)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "playerName: %s\n" % self.getPlayerName()
    ret += "time: %s\n" % self.getTime()
    ret += "waterStored: %s\n" % self.getWaterStored()
    ret += "oxygen: %s\n" % self.getOxygen()
    ret += "maxOxygen: %s\n" % self.getMaxOxygen()
    return ret

##A mappable object!
class Mappable(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.mappableGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.mappables:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  #\cond
  def getId(self):
    self.validify()
    return library.mappableGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getX(self):
    self.validify()
    return library.mappableGetX(self._ptr)
  #\endcond
  ##X position of the object
  x = property(getX)

  #\cond
  def getY(self):
    self.validify()
    return library.mappableGetY(self._ptr)
  #\endcond
  ##Y position of the object
  y = property(getY)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    return ret

##Represents a base to which you want to lead water.
class PumpStation(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.pumpStationGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.pumpStations:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  #\cond
  def getId(self):
    self.validify()
    return library.pumpStationGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getOwner(self):
    self.validify()
    return library.pumpStationGetOwner(self._ptr)
  #\endcond
  ##The owner of the PumpStation.
  owner = property(getOwner)

  #\cond
  def getSiegeAmount(self):
    self.validify()
    return library.pumpStationGetSiegeAmount(self._ptr)
  #\endcond
  ##The amount the PumpStation has been sieged.
  siegeAmount = property(getSiegeAmount)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "owner: %s\n" % self.getOwner()
    ret += "siegeAmount: %s\n" % self.getSiegeAmount()
    return ret

##Represents a single unit on the map.
class Unit(Mappable):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.unitGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.units:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  ##Make the unit move to the respective x and y location.
  def move(self, x, y):
    self.validify()
    return library.unitMove(self._ptr, x, y)

  ##Put dirt in a hole!
  def fill(self, tile):
    self.validify()
    if not isinstance(tile, Tile):
      raise TypeError('tile should be of [Tile]')
    tile.validify()
    return library.unitFill(self._ptr, tile._ptr)

  ##Dig out a tile
  def dig(self, tile):
    self.validify()
    if not isinstance(tile, Tile):
      raise TypeError('tile should be of [Tile]')
    tile.validify()
    return library.unitDig(self._ptr, tile._ptr)

  ##Command to attack another Unit.
  def attack(self, target):
    self.validify()
    if not isinstance(target, Unit):
      raise TypeError('target should be of [Unit]')
    target.validify()
    return library.unitAttack(self._ptr, target._ptr)

  #\cond
  def getId(self):
    self.validify()
    return library.unitGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getX(self):
    self.validify()
    return library.unitGetX(self._ptr)
  #\endcond
  ##X position of the object
  x = property(getX)

  #\cond
  def getY(self):
    self.validify()
    return library.unitGetY(self._ptr)
  #\endcond
  ##Y position of the object
  y = property(getY)

  #\cond
  def getOwner(self):
    self.validify()
    return library.unitGetOwner(self._ptr)
  #\endcond
  ##The owner of this unit.
  owner = property(getOwner)

  #\cond
  def getType(self):
    self.validify()
    return library.unitGetType(self._ptr)
  #\endcond
  ##The type of this unit. This type refers to list of UnitTypes.
  type = property(getType)

  #\cond
  def getHasAttacked(self):
    self.validify()
    return library.unitGetHasAttacked(self._ptr)
  #\endcond
  ##Whether current unit has attacked or not.
  hasAttacked = property(getHasAttacked)

  #\cond
  def getHasDug(self):
    self.validify()
    return library.unitGetHasDug(self._ptr)
  #\endcond
  ##Whether the current unit has dug or not.
  hasDug = property(getHasDug)

  #\cond
  def getHasFilled(self):
    self.validify()
    return library.unitGetHasFilled(self._ptr)
  #\endcond
  ##Whether the current unit has filled or not.
  hasFilled = property(getHasFilled)

  #\cond
  def getHealthLeft(self):
    self.validify()
    return library.unitGetHealthLeft(self._ptr)
  #\endcond
  ##The current amount health this unit has remaining.
  healthLeft = property(getHealthLeft)

  #\cond
  def getMaxHealth(self):
    self.validify()
    return library.unitGetMaxHealth(self._ptr)
  #\endcond
  ##The maximum amount of this health this unit can have
  maxHealth = property(getMaxHealth)

  #\cond
  def getMovementLeft(self):
    self.validify()
    return library.unitGetMovementLeft(self._ptr)
  #\endcond
  ##The number of moves this unit has remaining.
  movementLeft = property(getMovementLeft)

  #\cond
  def getMaxMovement(self):
    self.validify()
    return library.unitGetMaxMovement(self._ptr)
  #\endcond
  ##The maximum number of moves this unit can move.
  maxMovement = property(getMaxMovement)

  #\cond
  def getRange(self):
    self.validify()
    return library.unitGetRange(self._ptr)
  #\endcond
  ##The range of this unit's attack.
  range = property(getRange)

  #\cond
  def getOffensePower(self):
    self.validify()
    return library.unitGetOffensePower(self._ptr)
  #\endcond
  ##The power of the unit's offensive siege ability.
  offensePower = property(getOffensePower)

  #\cond
  def getDefensePower(self):
    self.validify()
    return library.unitGetDefensePower(self._ptr)
  #\endcond
  ##The power of the unit's defensive siege ability.
  defensePower = property(getDefensePower)

  #\cond
  def getDigPower(self):
    self.validify()
    return library.unitGetDigPower(self._ptr)
  #\endcond
  ##The power of this unit types's digging ability.
  digPower = property(getDigPower)

  #\cond
  def getFillPower(self):
    self.validify()
    return library.unitGetFillPower(self._ptr)
  #\endcond
  ##The power of this unit type's filling ability.
  fillPower = property(getFillPower)

  #\cond
  def getAttackPower(self):
    self.validify()
    return library.unitGetAttackPower(self._ptr)
  #\endcond
  ##The power of this unit type's attack.
  attackPower = property(getAttackPower)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "owner: %s\n" % self.getOwner()
    ret += "type: %s\n" % self.getType()
    ret += "hasAttacked: %s\n" % self.getHasAttacked()
    ret += "hasDug: %s\n" % self.getHasDug()
    ret += "hasFilled: %s\n" % self.getHasFilled()
    ret += "healthLeft: %s\n" % self.getHealthLeft()
    ret += "maxHealth: %s\n" % self.getMaxHealth()
    ret += "movementLeft: %s\n" % self.getMovementLeft()
    ret += "maxMovement: %s\n" % self.getMaxMovement()
    ret += "range: %s\n" % self.getRange()
    ret += "offensePower: %s\n" % self.getOffensePower()
    ret += "defensePower: %s\n" % self.getDefensePower()
    ret += "digPower: %s\n" % self.getDigPower()
    ret += "fillPower: %s\n" % self.getFillPower()
    ret += "attackPower: %s\n" % self.getAttackPower()
    return ret

##Represents a single tile on the map, can contain some amount of water.
class Tile(Mappable):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.tileGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.tiles:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  ##Attempt to spawn a unit of a type on this tile.
  def spawn(self, type):
    self.validify()
    return library.tileSpawn(self._ptr, type)

  #\cond
  def getId(self):
    self.validify()
    return library.tileGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getX(self):
    self.validify()
    return library.tileGetX(self._ptr)
  #\endcond
  ##X position of the object
  x = property(getX)

  #\cond
  def getY(self):
    self.validify()
    return library.tileGetY(self._ptr)
  #\endcond
  ##Y position of the object
  y = property(getY)

  #\cond
  def getOwner(self):
    self.validify()
    return library.tileGetOwner(self._ptr)
  #\endcond
  ##The owner of the tile.
  owner = property(getOwner)

  #\cond
  def getPumpID(self):
    self.validify()
    return library.tileGetPumpID(self._ptr)
  #\endcond
  ##Determines if this tile is a part of a Pump Station.
  pumpID = property(getPumpID)

  #\cond
  def getWaterAmount(self):
    self.validify()
    return library.tileGetWaterAmount(self._ptr)
  #\endcond
  ##The amount of water contained on the tile.
  waterAmount = property(getWaterAmount)

  #\cond
  def getDepth(self):
    self.validify()
    return library.tileGetDepth(self._ptr)
  #\endcond
  ##The depth of the tile. Tile is a trench if depth is greater than zero.
  depth = property(getDepth)

  #\cond
  def getTurnsUntilDeposit(self):
    self.validify()
    return library.tileGetTurnsUntilDeposit(self._ptr)
  #\endcond
  ##The number of turns until sediment is deposited on this tile.
  turnsUntilDeposit = property(getTurnsUntilDeposit)

  #\cond
  def getIsSpawning(self):
    self.validify()
    return library.tileGetIsSpawning(self._ptr)
  #\endcond
  ##Determines if this tile is attempting to spawn something or not.
  isSpawning = property(getIsSpawning)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "owner: %s\n" % self.getOwner()
    ret += "pumpID: %s\n" % self.getPumpID()
    ret += "waterAmount: %s\n" % self.getWaterAmount()
    ret += "depth: %s\n" % self.getDepth()
    ret += "turnsUntilDeposit: %s\n" % self.getTurnsUntilDeposit()
    ret += "isSpawning: %s\n" % self.getIsSpawning()
    return ret

##Represents type of unit.
class UnitType(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.unitTypeGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.unitTypes:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  #\cond
  def getId(self):
    self.validify()
    return library.unitTypeGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getName(self):
    self.validify()
    return library.unitTypeGetName(self._ptr)
  #\endcond
  ##The name of this type of unit.
  name = property(getName)

  #\cond
  def getType(self):
    self.validify()
    return library.unitTypeGetType(self._ptr)
  #\endcond
  ##The UnitType specific id representing this type of unit.
  type = property(getType)

  #\cond
  def getCost(self):
    self.validify()
    return library.unitTypeGetCost(self._ptr)
  #\endcond
  ##The oxygen cost to spawn this unit type into the game.
  cost = property(getCost)

  #\cond
  def getAttackPower(self):
    self.validify()
    return library.unitTypeGetAttackPower(self._ptr)
  #\endcond
  ##The power of the attack of this type of unit.
  attackPower = property(getAttackPower)

  #\cond
  def getDigPower(self):
    self.validify()
    return library.unitTypeGetDigPower(self._ptr)
  #\endcond
  ##The power of this unit types's digging ability.
  digPower = property(getDigPower)

  #\cond
  def getFillPower(self):
    self.validify()
    return library.unitTypeGetFillPower(self._ptr)
  #\endcond
  ##The power of this unit type's filling ability.
  fillPower = property(getFillPower)

  #\cond
  def getMaxHealth(self):
    self.validify()
    return library.unitTypeGetMaxHealth(self._ptr)
  #\endcond
  ##The maximum amount of this health this unit can have
  maxHealth = property(getMaxHealth)

  #\cond
  def getMaxMovement(self):
    self.validify()
    return library.unitTypeGetMaxMovement(self._ptr)
  #\endcond
  ##The maximum number of moves this unit can move.
  maxMovement = property(getMaxMovement)

  #\cond
  def getOffensePower(self):
    self.validify()
    return library.unitTypeGetOffensePower(self._ptr)
  #\endcond
  ##The power of the unit type's offensive siege ability.
  offensePower = property(getOffensePower)

  #\cond
  def getDefensePower(self):
    self.validify()
    return library.unitTypeGetDefensePower(self._ptr)
  #\endcond
  ##The power of the unit type's defensive siege ability.
  defensePower = property(getDefensePower)

  #\cond
  def getRange(self):
    self.validify()
    return library.unitTypeGetRange(self._ptr)
  #\endcond
  ##The range of the unit type's attack.
  range = property(getRange)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "name: %s\n" % self.getName()
    ret += "type: %s\n" % self.getType()
    ret += "cost: %s\n" % self.getCost()
    ret += "attackPower: %s\n" % self.getAttackPower()
    ret += "digPower: %s\n" % self.getDigPower()
    ret += "fillPower: %s\n" % self.getFillPower()
    ret += "maxHealth: %s\n" % self.getMaxHealth()
    ret += "maxMovement: %s\n" % self.getMaxMovement()
    ret += "offensePower: %s\n" % self.getOffensePower()
    ret += "defensePower: %s\n" % self.getDefensePower()
    ret += "range: %s\n" % self.getRange()
    return ret
