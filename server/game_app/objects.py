import math

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

    self.totalUnits = 0

  def toList(self):
    return [self.id, self.playerName, self.time, self.waterStored, self.oxygen, self.maxOxygen, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, playerName = self.playerName, time = self.time, waterStored = self.waterStored, oxygen = self.oxygen, maxOxygen = self.maxOxygen, )
  
  def nextTurn(self):
    if self.id == self.game.playerID:
      #GET OXYGEN
      unitWorth = [0, 0]
      for unit in self.game.objects.units:
        unitWorth[unit.owner] += self.game.unitCost

      # Get value of fish in spawnQueue
      inSpawnQueue = len(self.spawnQueue) * self.game.unitCost
      #self.spawnQueue = []
      netWorth = unitWorth[self.id] + self.oxygen + inSpawnQueue
      oxyYouShouldHave = self.maxOxygen
      oxyYouGet = math.ceil((oxyYouShouldHave - netWorth) * self.game.oxygenRate)
      self.oxygen += oxyYouGet

      #SPAWN UNITS
      for newUnitStats in self.spawnQueue:
        newUnit = self.game.addObject(Unit, newUnitStats)
        self.game.grid[newUnit.x][newUnit.y].append(newUnit)
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
  game_state_attributes = ['id', 'owner', 'waterAmount', 'siegeAmount']
  def __init__(self, game, id, owner, waterAmount, siegeAmount):
    self.game = game
    self.id = id
    self.owner = owner
    self.waterAmount = waterAmount
    self.siegeAmount = siegeAmount
    self.updatedAt = game.turnNumber

    self.maxSiege = game.maxSiege

    self.siegeTiles = None

  def create_siegeTiles(self):
    self.siegeTiles = [tile for tile in self.game.objects.tiles if tile.pumpID == self.id]

  def toList(self):
    return [self.id, self.owner, self.waterAmount, self.siegeAmount, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, owner = self.owner, waterAmount = self.waterAmount, siegeAmount = self.siegeAmount, )
  
  def nextTurn(self):
    for siegeTile in self.siegeTiles:
      unit = [unit for unit in self.game.grid[siegeTile.x][siegeTile.y] if isinstance(unit, Unit)]

      if len(unit) <= 0:
        continue

      unit = unit[0]

      #Defending
      if unit.owner == self.owner:
        self.siegeAmount -= self.game.defensePower
      elif unit.owner == self.owner^1:
        self.siegeAmount += self.game.offensePower
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
  game_state_attributes = ['id', 'x', 'y', 'owner', 'type', 'hasAttacked', 'hasDug', 'hasFilled', 'healthLeft', 'maxHealth', 'movementLeft', 'maxMovement']
  def __init__(self, game, id, x, y, owner, type, hasAttacked, hasDug, hasFilled, healthLeft, maxHealth, movementLeft, maxMovement):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.type = type # 0 - Digger , 1 - Filler
    self.hasAttacked = hasAttacked
    self.hasDug = hasDug
    self.hasFilled = hasFilled
    self.healthLeft = healthLeft
    self.maxHealth = maxHealth
    self.movementLeft = movementLeft
    self.maxMovement = maxMovement
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.type, self.hasAttacked, self.hasDug, self.hasFilled, self.healthLeft, self.maxHealth, self.movementLeft, self.maxMovement, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, type = self.type, hasAttacked = self.hasAttacked, hasDug = self.hasDug, hasFilled = self.hasFilled, healthLeft = self.healthLeft, maxHealth = self.maxHealth, movementLeft = self.movementLeft, maxMovement = self.maxMovement, )

  @staticmethod
  def handleDeath(unit):
    if unit.healthLeft <= 0:
      unit.game.objects.players[unit.owner].totalUnits -= 1
      unit.game.grid[unit.x][unit.y].remove(unit)
      unit.game.removeObject(unit)

      unit.game.addAnimation(DeathAnimation(unit.id))


  def nextTurn(self):
    tile = self.game.getTile(self.x, self.y)
    # Damage for standing in water
    if tile.isTrench and tile.waterAmount > 0:
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
    elif self.movementLeft <= 0:
      return 'Turn {}: Your unit {} does not have any movements left. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif not (0 <= x < self.game.mapWidth) or not (0 <= y < self.game.mapHeight):
      return 'Turn {}: Your unit {} cannot move off the map. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif len(self.game.grid[x][y]) > 1:
      return 'Turn {}: Your unit {} is trying to run into something. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
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
    
    # Apply damage for moving into a trench
    tile = self.game.getTile(x, y)
    if tile.isTrench:
      # Damage for moving through water
      if tile.waterAmount > 0:
        self.healthLeft -= self.game.waterDamage + self.game.trenchDamage
      # Damage for moving into a trench
      elif not prevTile.isTrench:
        self.healthLeft -= self.game.trenchDamage
      self.handleDeath(self)
    # Damage for coming out of a trench
    elif prevTile.isTrench:
      self.healthLeft -= self.game.trenchDamage
      self.handleDeath(self)

    return True

  def fill(self, tile):
    x = tile.x
    y = tile.y

    #FILLERS ARE OF TYPE 1
    
    if self.owner != self.game.playerID:
      return 'Turn {}: You cannot control the opponent\'s {}.'.format(self.game.turnNumber, self.id)
    elif self.type != 1:
      return 'Turn {}: Your digger unit {} cannot fill.'.format(self.game.turnNumber, self.id)
    elif self.hasFilled == 1:
      return 'Turn {}: Your unit {} has already filled in a trench this turn.'.format(self.game.turnNumber, self.id)
    elif abs(self.x-x) + abs(self.y-y) != 1:
      return 'Turn {}: Your unit {} can only fill adjacent Tiles. ({},{}) fills ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.isTrench == 0:
      return 'Turn {}: Your unit {} cannot fill something that is not a trench. ({},{}) fills ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.waterAmount > 0:
      return 'Turn {}: Your unit {} cannot fill trenches with water in them."'.format(self.game.turnNumber, self.id)
    elif len(self.game.grid[x][y]) > 1:
      return 'Turn {}: Your unit {} cannot fill trenches with units in them.'.format(self.game.turnNumber, self.id)
    
    # Set the Tile to not be a trench
    tile.isTrench = 0
    # Unit can no longer move
    self.movementLeft = 0
    
    self.hasFilled = 1
    
    self.game.addAnimation(FillAnimation(self.id, tile.id))
    
    return True

  def dig(self, tile):
    x = tile.x
    y = tile.y

    # DIGGERS ARE TYPE 0
    
    if self.owner != self.game.playerID:
      return 'Turn {}: You cannot control the opponent\'s {}.'.format(self.game.turnNumber, self.id)
    elif self.type != 0:
      return 'Turn {}: Your filler {} cannot dig.'.format(self.game.turnNumber, self.id)
    elif self.hasDug == 1:
      return 'Turn {}: Your {} has already dug a trench this turn.'.format(self.game.turnNumber, self.id)
    elif abs(self.x-x) + abs(self.y-y) > 1:
      return 'Turn {}: Your {} can only dig adjacent or same tiles. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.isTrench == 1:
      return 'Turn {}: Your {} cannot dig a trench in a trench. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.pumpID != -1:
      return 'Turn {}: Your {} can not dig trenches on pump tiles. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.owner == 3:
      return 'Turn {}: Your {} can not dig trenches on ice tiles. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.owner == 0 or tile.owner == 1:
      return 'Turn {}: Your {} can not dig trenches on spawn tiles. ({},{}) digs ({},{})'.format(self.game.turn, self.id, self.x, self.y, x, y)
    elif len(self.game.grid[x][y]) > 1:
      return 'Turn {}: Your {} cannot dig under other units. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    
    # Set the Tile to be a trench
    tile.isTrench = 1
    # Unit can no longer move
    self.movementLeft = 0
    
    self.hasDug = 1
    
    self.game.addAnimation(DigAnimation(self.id, tile.id))
    
    return True

  def attack(self, target):
    x = target.x
    y = target.y
    
    if self.owner != self.game.playerID:
      return 'Turn {}: You cannot control the opponent\'s {}.'.format(self.game.turnNumber, self.id)
    elif abs(self.x-x) + abs(self.y-y) != 1:
      return 'Turn {}: Your {} can only attack adjacent Units. ({}, {}) -> ({}, {})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
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
    target.healthLeft -= self.game.attackDamage

    self.handleDeath(target)
    
    return True

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Tile(Mappable):
  game_state_attributes = ['id', 'x', 'y', 'owner', 'pumpID', 'waterAmount', 'isTrench']
  def __init__(self, game, id, x, y, owner, pumpID, waterAmount, isTrench):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.pumpID = pumpID
    self.waterAmount = waterAmount
    self.isTrench = isTrench
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.pumpID, self.waterAmount, self.isTrench, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, pumpID = self.pumpID, waterAmount = self.waterAmount, isTrench = self.isTrench, )
  def nextTurn(self):
    #TODO: Tile Next Turn (Possible Flow Logic?)
    pass

  def spawn(self, type):
    player = self.game.objects.players[self.game.playerID]

    if self.owner != self.game.playerID:
      return 'Turn {}: You cannot spawn a unit on a tile you do not own. ({},{})'.format(self.game.turnNumber, self.x, self.y)
    if player.oxygen < self.game.unitCost:
      return 'Turn {}: You do not have enough resources({}) to spawn this unit({}). ({},{})'.format(self.game.turnNumber, player.oxygen, self.game.unitCost, self.x, self.y)
    if type not in [0,1,2]:
      return 'Turn {}: You cannot spawn a unit with type {}. ({},{})'.format(self.game.turnNumber, type, self.x, self.y)
    if len(self.game.grid[self.x][self.y]) > 1:
      return 'Turn {} You cannot spawn a unit on top of another unit. ({},{})'.format(self.game.turnNumber, self.x, self.y)
    if player.totalUnits >= self.game.maxUnits:
      return 'Turn {} You cannot spawn a unit because you already have the maximum amount of units ({})'.format(self.game.turnNumber, self.game.maxUnits)

    player.oxygen -= self.game.unitCost

    #['id', 'x', 'y', 'owner', 'type', 'hasAttacked', 'hasDug', 'hasFilled', 'healthLeft', 'maxHealth', 'movementLeft', 'maxMovement']
    unit = self.unitStats
    newUnitStats = [self.x, self.y, self.owner, type, 0, 0, 0, self.unit.maxHealth, self.unit.maxHealth, self.unit.maxMovement, self.unit.maxMovement ]
    player.spawnQueue.append(newUnitStats)
    player.totalUnits += 1

    #TODO: Add spawning animation

    return True

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)


# The following are animations and do not need to have any logic added
class SpawnAnimation:
  def __init__(self, sourceID, unitID):
    self.sourceID = sourceID
    self.unitID = unitID

  def toList(self):
    return ["spawn", self.sourceID, self.unitID, ]

  def toJson(self):
    return dict(type = "spawn", sourceID = self.sourceID, unitID = self.unitID)

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

class FillAnimation:
  def __init__(self, actingID, tileID):
    self.actingID = actingID
    self.tileID = tileID

  def toList(self):
    return ["fill", self.actingID, self.tileID, ]

  def toJson(self):
    return dict(type = "fill", actingID = self.actingID, tileID = self.tileID)

class DeathAnimation:
  def __init__(self, sourceID):
    self.sourceID = sourceID

  def toList(self):
    return ["death", self.sourceID, ]

  def toJson(self):
    return dict(type = "death", sourceID = self.sourceID)

class DigAnimation:
  def __init__(self, actingID, tileID):
    self.actingID = actingID
    self.tileID = tileID

  def toList(self):
    return ["dig", self.actingID, self.tileID, ]

  def toJson(self):
    return dict(type = "dig", actingID = self.actingID, tileID = self.tileID)

class FlowAnimation:
  def __init__(self, sourceID, destID, waterAmount):
    self.sourceID = sourceID
    self.destID = destID
    self.waterAmount = waterAmount

  def toList(self):
    return ["flow", self.sourceID, self.destID, self.waterAmount, ]

  def toJson(self):
    return dict(type = "flow", sourceID = self.sourceID, destID = self.destID, waterAmount = self.waterAmount)

class AttackAnimation:
  def __init__(self, actingID, targetID):
    self.actingID = actingID
    self.targetID = targetID

  def toList(self):
    return ["attack", self.actingID, self.targetID, ]

  def toJson(self):
    return dict(type = "attack", actingID = self.actingID, targetID = self.targetID)
