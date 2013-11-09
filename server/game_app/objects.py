import networking.config.config
import math

# Load unit types
cfgTypes = networking.config.config.readConfig("config/unitStats.cfg")

class Player(object):
  game_state_attributes = ['id', 'playerName', 'time', 'waterStored', 'oxygen', 'maxOxygen']
  def __init__(self, game, id, playerName, time, waterStored, oxygen, maxOxygen):
    self.game = game
    self.id = id
    self.playerName = playerName
    self.time = time
    self.waterStored = waterStored
    self.oxygen = oxygen
    self.maxOxygen = maxOxygen
    self.updatedAt = game.turnNumber

    self.spawnQueue = []
    self.spawnCostQueue = []
    self.totalUnits = 0

  def toList(self):
    return [self.id, self.playerName, self.time, self.waterStored, self.oxygen, self.maxOxygen, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, playerName = self.playerName, time = self.time, waterStored = self.waterStored, oxygen = self.oxygen, maxOxygen = self.maxOxygen, )
  
  def nextTurn(self):
    if self.id == self.game.playerID:
      unitWorth = [0, 0]
      for unit in self.game.objects.units:
        unitWorth[unit.owner] += self.game.unitTypesDict[unit.type].cost
      inSpawnQueue = sum(self.spawnCostQueue)
      self.spawnCostQueue = []
      netWorth = unitWorth[self.id] + self.oxygen + inSpawnQueue
      oxyYouShouldHave = self.maxOxygen
      oxyYouGet = math.ceil((oxyYouShouldHave - netWorth) * self.game.oxygenRate)
      self.oxygen += oxyYouGet

      #Make sure oxygen is never over the max oxygen.
      if self.oxygen > self.maxOxygen:
        self.oxygen = self.maxOxygen
      elif self.oxygen < 0:
        self.oxygen = 0

      #SPAWN UNITS
      for newUnitStats in self.spawnQueue:
        newUnit = self.game.addObject(Unit, newUnitStats)
        self.game.grid[newUnit.x][newUnit.y].append(newUnit)
        self.game.grid[newUnit.x][newUnit.y][0].isSpawning = 0
      self.spawnQueue = []

      #FLOW WATER
      self.game.waterFlow()

    return True

  def talk(self, message):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Mappable(object):
  game_state_attributes = ['id', 'x', 'y']
  def __init__(self, game, id, x, y):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, )
  
  def nextTurn(self):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class PumpStation(object):
  game_state_attributes = ['id', 'owner', 'siegeAmount']
  def __init__(self, game, id, owner, siegeAmount):
    self.game = game
    self.id = id
    self.owner = owner
    self.siegeAmount = siegeAmount
    self.updatedAt = game.turnNumber

    self.maxSiege = game.maxSiege

    self.siegeTiles = None

  def create_siegeTiles(self):
    self.siegeTiles = [tile for tile in self.game.objects.tiles if tile.pumpID == self.id]

  def toList(self):
    return [self.id, self.owner, self.siegeAmount, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, owner = self.owner, siegeAmount = self.siegeAmount, )
  
  def nextTurn(self):
    for siegeTile in self.siegeTiles:
      unit = [unit for unit in self.game.grid[siegeTile.x][siegeTile.y] if isinstance(unit, Unit)]

      if len(unit) <= 0:
        continue

      unit = unit[0]

      #Defending
      if unit.owner == self.owner:
        self.siegeAmount -= unit.defensePower
      elif unit.owner == self.owner^1:
        self.siegeAmount += unit.offensePower
      else:
        print('Unit owner not 0 or 1: {}'.format(self.owner))

    if self.siegeAmount < 0:
      self.siegeAmount = 0
    elif self.siegeAmount >= self.maxSiege:
      self.siegeAmount = 0
      self.owner ^= 1

      for siegeTile in self.siegeTiles:
        siegeTile.owner = self.owner

    return

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Unit(Mappable):
  game_state_attributes = ['id', 'x', 'y', 'owner', 'type', 'hasAttacked', 'hasDug', 'hasFilled', 'healthLeft', 'maxHealth', 'movementLeft', 'maxMovement', 'range', 'offensePower', 'defensePower', 'digPower', 'fillPower', 'attackPower']
  def __init__(self, game, id, x, y, owner, type, hasAttacked, hasDug, hasFilled, healthLeft, maxHealth, movementLeft, maxMovement, range, offensePower, defensePower, digPower, fillPower, attackPower):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.type = type
    self.hasAttacked = hasAttacked
    self.hasDug = hasDug
    self.hasFilled = hasFilled
    self.healthLeft = healthLeft
    self.maxHealth = maxHealth
    self.movementLeft = movementLeft
    self.maxMovement = maxMovement
    self.range = range
    self.offensePower = offensePower
    self.defensePower = defensePower
    self.digPower = digPower
    self.fillPower = fillPower
    self.attackPower = attackPower
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.type, self.hasAttacked, self.hasDug, self.hasFilled, self.healthLeft, self.maxHealth, self.movementLeft, self.maxMovement, self.range, self.offensePower, self.defensePower, self.digPower, self.fillPower, self.attackPower, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, type = self.type, hasAttacked = self.hasAttacked, hasDug = self.hasDug, hasFilled = self.hasFilled, healthLeft = self.healthLeft, maxHealth = self.maxHealth, movementLeft = self.movementLeft, maxMovement = self.maxMovement, range = self.range, offensePower = self.offensePower, defensePower = self.defensePower, digPower = self.digPower, fillPower = self.fillPower, attackPower = self.attackPower, )

  def handleDeath(self, unit):
    if unit.healthLeft <= 0:
      unit.game.objects.players[unit.owner].totalUnits -= 1
      unit.game.grid[unit.x][unit.y].remove(unit)
      unit.game.removeObject(unit)

      tile = self.game.getTile(unit.x, unit.y)

      unit.game.addAnimation(DeathAnimation(tile.id))

  def nextTurn(self):
    if self.owner == self.game.playerID:

      tile = self.game.getTile(self.x, self.y)
      # Damage for standing in water
      if tile.depth > 0 and tile.waterAmount > 0:
        self.healthLeft -= self.game.waterDamage

      # Reset flags if it is unit owner's turn
      if self.owner == self.game.playerID:
        self.movementLeft = self.maxMovement
        self.hasAttacked = 0
        self.hasFilled = 0
        self.hasDug = 0

      self.handleDeath(self)

    return True

  def move(self, x, y):
    if self.owner != self.game.playerID:
      return 'Turn {}: You cannot use the other player\'s unit {}. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.healthLeft <= 0:
      return 'Turn {}: Your unit {} does not have any health left. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.movementLeft <= 0:
      return 'Turn {}: Your unit {} does not have any movements left. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif not (0 <= x < self.game.mapWidth) or not (0 <= y < self.game.mapHeight):
      return 'Turn {}: Your unit {} cannot move off the map. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif len(self.game.grid[x][y]) > 1:
      return 'Turn {}: Your unit {} is trying to run into something. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.game.getTile(x, y).owner == 3:
      return 'Turn {}: Your unit {} is trying to move onto an ice tile. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.game.getTile(x, y).isSpawning == 1:
      return 'Turn {}: Your unit {} is trying to move onto a spawn tile that is spawning a unit. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.game.getTile(x, y).pumpID == -1 and self.game.getTile(x, y).owner == self.game.playerID^1:
      return 'Turn {}: Your unit {} is trying to move onto the enemy\'s spawn base. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif abs(self.x-x) + abs(self.y-y) != 1:
      return 'Turn {}: Your unit {} can only move one unit away. ({}.{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)

    prevTile = self.game.getTile(self.x, self.y)

    self.game.grid[self.x][self.y].remove(self)

    self.game.addAnimation(MoveAnimation(self.id,self.x,self.y,x,y))
    self.x = x
    self.y = y
    self.movementLeft -= 1
    self.game.grid[self.x][self.y].append(self)

    tile = self.game.getTile(x, y)

    if tile.waterAmount > 0 and tile.depth > 0:
      self.healthLeft -= self.game.waterDamage
    self.handleDeath(self)

    return True

  def fill(self, tile):
    x = tile.x
    y = tile.y

    if self.owner != self.game.playerID:
      return 'Turn {}: You cannot control the opponent\'s {}.'.format(self.game.turnNumber, self.id)
    elif self.fillPower <= 0:
      return 'Turn {}: Your unit {} cannot fill.'.format(self.game.turnNumber, self.id)
    elif self.healthLeft <= 0:
      return 'Turn {}: Your unit {} does not have any health left. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.owner != 2:
      return 'Turn {}: Your unit {} can only fill normal tiles. ({},{}) fills ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.hasFilled == 1:
      return 'Turn {}: Your unit {} has already filled in a trench this turn.'.format(self.game.turnNumber, self.id)
    elif abs(self.x-x) + abs(self.y-y) > 1:
      return 'Turn {}: Your unit {} can only fill adjacent Tiles. ({},{}) fills ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.depth <= 0:
      return 'Turn {}: Your unit {} cannot fill something that is not a trench. ({},{}) fills ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif len(self.game.grid[x][y]) > 1 and self not in self.game.grid[x][y]:
      return 'Turn {}: Your unit {} cannot fill trenches with other units in them.'.format(self.game.turnNumber, self.id)
    elif len(self.game.grid[x][y]) > 2:
      return 'Turn {}: Your unit {} cannot fill trenches with other objects in them.'.format(self.game.turnNumber, self.id)

    # Decrease the trenches depth
    tile.depth -= self.fillPower
    if tile.depth <= 0:
      tile.waterAmount = 0
      tile.depth = 0


    # Unit can no longer move
    self.movementLeft = 0

    #reset deposition rate
    tile.turnsUntilDeposit = self.game.depositionRate

    
    self.hasFilled = 1
    
    self.game.addAnimation(FillAnimation(self.id, tile.id))
    
    return True

  def dig(self, tile):
    x = tile.x
    y = tile.y
    
    if self.owner != self.game.playerID:
      return 'Turn {}: You cannot control the opponent\'s {}.'.format(self.game.turnNumber, self.id)
    elif self.digPower <= 0:
      return 'Turn {}: Your unit {} cannot dig.'.format(self.game.turnNumber, self.id)
    elif self.healthLeft <= 0:
      return 'Turn {}: Your unit {} does not have any health left. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.hasDug == 1:
      return 'Turn {}: Your unit {} has already dug a trench this turn.'.format(self.game.turnNumber, self.id)
    elif abs(self.x-x) + abs(self.y-y) > 1:
      return 'Turn {}: Your unit {} can only dig adjacent or same tiles. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.pumpID != -1:
      return 'Turn {}: Your unit {} can not dig trenches on pump tiles. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.owner != 2:
      return 'Turn {}: Your unit {} can only dig trenches on normal tiles. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif len(self.game.grid[x][y]) > 1 and self not in self.game.grid[x][y]:
        return 'Turn {}: Your unit {} cannot dig under other units. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif len(self.game.grid[x][y]) > 2:
      return 'Turn {}: Your unit {} cannot dig under multiple objects. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    
    # Increase the depth of the trench
    tile.depth += self.digPower
    tile.turnsUntilDeposit = self.game.depositionRate

    self.movementLeft = 0
    
    self.hasDug = 1
    
    self.game.addAnimation(DigAnimation(self.id, tile.id))
    
    return True

  def attack(self, target):
    x = target.x
    y = target.y
    
    if self.owner != self.game.playerID:
      return 'Turn {}: You cannot control the opponent\'s {}.'.format(self.game.turnNumber, self.id)
    elif self.healthLeft <= 0:
      return 'Turn {}: Your unit {} does not have any health left. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif abs(self.x-x) + abs(self.y-y) > self.range:
      return 'Turn {}: Your {} can only attack Units within range ({}). ({}, {}) -> ({}, {})'.format(self.game.turnNumber, self.id, self.range, self.x, self.y, x, y)
    elif self.hasAttacked == 1:
      return 'Turn {}: Your {} has already attacked this turn.'.format(self.game.turnNumber, self.id)
    elif not isinstance(target, Unit):
      return 'Turn {}: Your {} can only attack other units.'.format(self.game.turnNumber, self.id)
    elif target.owner == self.owner:
      return 'Turn {}: Your {} cannot attack a friendly unit {}.'.format(self.game.turnNumber, self.id, target.id)
      
    self.hasAttacked = 1
    
    # Unit can no longer move
    self.movementLeft = 0
    
    self.game.addAnimation(AttackAnimation(self.id, target.id))
    
    # Deal damage
    target.healthLeft -= self.attackPower

    self.handleDeath(target)
    
    return True

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Tile(Mappable):
  game_state_attributes = ['id', 'x', 'y', 'owner', 'pumpID', 'waterAmount', 'depth', 'turnsUntilDeposit', 'isSpawning']
  def __init__(self, game, id, x, y, owner, pumpID, waterAmount, depth, turnsUntilDeposit, isSpawning):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.pumpID = pumpID
    self.waterAmount = waterAmount
    self.depth = depth
    self.turnsUntilDeposit = turnsUntilDeposit
    self.isSpawning = isSpawning
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.pumpID, self.waterAmount, self.depth, self.turnsUntilDeposit, self.isSpawning, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, pumpID = self.pumpID, waterAmount = self.waterAmount, depth = self.depth, turnsUntilDeposit = self.turnsUntilDeposit, isSpawning = self.isSpawning, )

  def nextTurn(self):
    if self.depth > 0:
      if self.turnsUntilDeposit <= 0:
        self.turnsUntilDeposit = self.game.depositionRate
        self.depth -= 1
        if self.depth <= 0 and self.waterAmount > 0:
          self.waterAmount = 0
      else:
        self.turnsUntilDeposit -= 1
    if self.waterAmount <= 0 and self.owner == 3:
      self.owner = 2
      self.waterAmount = 0
    return

  def spawn(self, type):
    player = self.game.objects.players[self.game.playerID]

    if self.owner != self.game.playerID:
      return 'Turn {}: You cannot spawn a unit on a tile you do not own. ({},{})'.format(self.game.turnNumber, self.x, self.y)
    if len(self.game.grid[self.x][self.y]) > 1:
      return 'Turn {} You cannot spawn a unit on top of another unit. ({},{})'.format(self.game.turnNumber, self.x, self.y)
    if player.totalUnits >= self.game.maxUnits:
      return 'Turn {} You cannot spawn a unit because you already have the maximum amount of units ({})'.format(self.game.turnNumber, self.game.maxUnits)
    if self.isSpawning == 1:
      return 'Turn {} You cannot spawn a unit because you are already attempting to spawn here ({},{})'.format(self.game.turnNumber, self.x, self.y)
    if self.pumpID != -1:
      pump = next(pump for pump in self.game.objects.pumpStations if pump.id == self.pumpID)
      if pump.siegeAmount > 0:
        return 'Turn {} You cannot spawn a unit on pump station that is under seige. ({},{})'.format(self.game.turnNumber, self.x, self.y)
    unittype = self.game.typeToUnitType(type)
    if unittype is None:
      return 'Turn {}: You cannot spawn a unit with this type.'.format(self.game.turnNumber)
    if player.oxygen < unittype.cost:
      return 'Turn {}: You do not have enough resources({}) to spawn this unit({}). ({},{})'.format(self.game.turnNumber, player.oxygen, unittype.cost, self.x, self.y)

    player.oxygen -= unittype.cost

    #['id', 'x', 'y', 'owner', 'type', 'hasAttacked', 'hasDug', 'hasFilled', 'healthLeft', 'maxHealth', 'movementLeft', 'maxMovement', 'range', 'offensePower', 'defensePower', 'digpower', 'fillPower', 'attackPower']
    newUnitStats = [self.x, self.y, self.owner, type, 0, 0, 0, unittype.maxHealth, unittype.maxHealth, unittype.maxMovement, unittype.maxMovement, unittype.range, unittype.offensePower, unittype.defensePower, unittype.digPower, unittype.fillPower, unittype.attackPower]
    player.spawnQueue.append(newUnitStats)
    player.spawnCostQueue.append(unittype.cost)
    player.totalUnits += 1
    self.isSpawning = 1
    
    # Add spawn animation
    # NOTE: we are providing 0 for unit.id
    self.game.addAnimation(SpawnAnimation(self.id, 0))
    
    return True

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class UnitType(object):
  game_state_attributes = ['id', 'name', 'type', 'cost', 'attackPower', 'digPower', 'fillPower', 'maxHealth', 'maxMovement', 'offensePower', 'defensePower', 'range']
  def __init__(self, game, id, name, type, cost, attackPower, digPower, fillPower, maxHealth, maxMovement, offensePower, defensePower, range):
    self.game = game
    self.id = id
    self.name = name
    self.type = type
    self.cost = cost
    self.attackPower = attackPower
    self.digPower = digPower
    self.fillPower = fillPower
    self.maxHealth = maxHealth
    self.maxMovement = maxMovement
    self.offensePower = offensePower
    self.defensePower = defensePower
    self.range = range
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.name, self.type, self.cost, self.attackPower, self.digPower, self.fillPower, self.maxHealth, self.maxMovement, self.offensePower, self.defensePower, self.range, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, name = self.name, type = self.type, cost = self.cost, attackPower = self.attackPower, digPower = self.digPower, fillPower = self.fillPower, maxHealth = self.maxHealth, maxMovement = self.maxMovement, offensePower = self.offensePower, defensePower = self.defensePower, range = self.range, )
  
  def nextTurn(self):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)


# The following are animations and do not need to have any logic added
class DigAnimation:
  def __init__(self, actingID, tileID):
    self.actingID = actingID
    self.tileID = tileID

  def toList(self):
    return ["dig", self.actingID, self.tileID, ]

  def toJson(self):
    return dict(type = "dig", actingID = self.actingID, tileID = self.tileID)

class AttackAnimation:
  def __init__(self, actingID, targetID):
    self.actingID = actingID
    self.targetID = targetID

  def toList(self):
    return ["attack", self.actingID, self.targetID, ]

  def toJson(self):
    return dict(type = "attack", actingID = self.actingID, targetID = self.targetID)

class SpawnAnimation:
  def __init__(self, sourceID, unitID):
    self.sourceID = sourceID
    self.unitID = unitID

  def toList(self):
    return ["spawn", self.sourceID, self.unitID, ]

  def toJson(self):
    return dict(type = "spawn", sourceID = self.sourceID, unitID = self.unitID)

class DeathAnimation:
  def __init__(self, sourceID):
    self.sourceID = sourceID

  def toList(self):
    return ["death", self.sourceID, ]

  def toJson(self):
    return dict(type = "death", sourceID = self.sourceID)

class MoveAnimation:
  def __init__(self, actingID, fromX, fromY, toX, toY):
    self.actingID = actingID
    self.fromX = fromX
    self.fromY = fromY
    self.toX = toX
    self.toY = toY

  def toList(self):
    return ["move", self.actingID, self.fromX, self.fromY, self.toX, self.toY, ]

  def toJson(self):
    return dict(type = "move", actingID = self.actingID, fromX = self.fromX, fromY = self.fromY, toX = self.toX, toY = self.toY)

class FlowAnimation:
  def __init__(self, sourceID, destID, waterAmount):
    self.sourceID = sourceID
    self.destID = destID
    self.waterAmount = waterAmount

  def toList(self):
    return ["flow", self.sourceID, self.destID, self.waterAmount, ]

  def toJson(self):
    return dict(type = "flow", sourceID = self.sourceID, destID = self.destID, waterAmount = self.waterAmount)

class FillAnimation:
  def __init__(self, actingID, tileID):
    self.actingID = actingID
    self.tileID = tileID

  def toList(self):
    return ["fill", self.actingID, self.tileID, ]

  def toJson(self):
    return dict(type = "fill", actingID = self.actingID, tileID = self.tileID)

