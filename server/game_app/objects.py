class Player(object):
  game_state_attributes = ['id', 'playerName', 'time', 'waterStored', 'spawnResources']
  def __init__(self, game, id, playerName, time, waterStored, spawnResources):
    self.game = game
    self.id = id
    self.playerName = playerName
    self.time = time
    self.waterStored = waterStored
    self.spawnResources = spawnResources
    self.updatedAt = game.turnNumber
    self.spawnQueue = []

  def toList(self):
    return [self.id, self.playerName, self.time, self.waterStored, self.spawnResources, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, playerName = self.playerName, time = self.time, waterStored = self.waterStored, spawnResources = self.spawnResources, )
  
  def nextTurn(self):
    if self.id == self.game.playerID:
      for newUnitStats in self.spawnQueue:
        newUnit = self.game.addObject(Unit, newUnitStats)
        self.game.grid[newUnit.x][newUnit.y].append(newUnit)
      self.spawnQueue = []

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
  game_state_attributes = ['id', 'owner', 'waterAmount', 'siegeCount']
  def __init__(self, game, id, owner, waterAmount, siegeCount):
    self.game = game
    self.id = id
    self.owner = owner
    self.waterAmount = waterAmount
    self.siegeCount = siegeCount
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.owner, self.waterAmount, self.siegeCount, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, owner = self.owner, waterAmount = self.waterAmount, siegeCount = self.siegeCount, )
  
  def nextTurn(self):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Unit(Mappable):
  game_state_attributes = ['id', 'x', 'y', 'owner', 'type', 'hasAttacked', 'hasDigged', 'hasBuilt', 'healthLeft', 'maxHealth', 'movementLeft', 'maxMovement']
  def __init__(self, game, id, x, y, owner, type, hasAttacked, hasDigged, hasBuilt, healthLeft, maxHealth, movementLeft, maxMovement):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.type = type # 0 - Digger , 1 - Filler
    self.hasAttacked = hasAttacked
    self.hasDigged = hasDigged
    self.hasBuilt = hasBuilt
    self.healthLeft = healthLeft
    self.maxHealth = maxHealth
    self.movementLeft = movementLeft
    self.maxMovement = maxMovement
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.type, self.hasAttacked, self.hasDigged, self.hasBuilt, self.healthLeft, self.maxHealth, self.movementLeft, self.maxMovement, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, type = self.type, hasAttacked = self.hasAttacked, hasDigged = self.hasDigged, hasBuilt = self.hasBuilt, healthLeft = self.healthLeft, maxHealth = self.maxHealth, movementLeft = self.movementLeft, maxMovement = self.maxMovement, )
  
  def nextTurn(self):
    tile = self.game.grid[self.x][self.y][0]
  
    # Reset flags if it is unit owner's turn
    if self.owner == self.game.playerID:
      self.movementLeft = self.maxMovement
      self.hasAttacked = 0
      self.hasBuilt = 0
      self.hasDigged = 0
  
    # Apply damage if the unit is in a water filled trench
    if tile.isTrench and tile.waterAmount > 0:
      self.healthLeft -= self.game.waterDamage
      
      # Check if the unit died
      if self.healthLeft <= 0:
        self.game.grid[self.x][self.y].remove(self)
        self.game.removeObject(self)
      
    return True

  def move(self, x, y):
    if self.owner != self.game.playerID:
      return 'Turn {}: You cannot use the other player\'s unit {}. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.movementLeft <= 0:
      return 'Turn {}: Your unit {} does not have any movements left. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif not (0 <= x < self.game.mapWidth) or not (0 <= y < self.game.mapHeight):
      return 'Turn {}: Your unit {} cannot move off the map. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif abs(self.x-x) + abs(self.y-y) != 1:
      return 'Turn {}: Your unit {} can only move one unit away. ({}.{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)

    #Check for units running into each other
    if len(self.game.grid[x][y]) > 1:
        return 'Turn {}: Your unit {} is trying to run into something. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)


    self.game.grid[self.x][self.y].remove(self)

    self.game.addAnimation(MoveAnimation(self.id,self.x,self.y,x,y))
    self.x = x
    self.y = y
    self.movementLeft -= 1
    self.game.grid[self.x][self.y].append(self)


    return True

  def fill(self, tile):
    x = tile.x
    y = tile.y

    #FILLERS ARE OF TYPE 1
    
    if self.owner != self.game.playerID:
      return 'Turn {}: You cannot control the opponent\'s {}.'.format(self.game.turnNumber, self.id)
    elif self.type != 1:
      return 'Turn {}: Your digger unit {} cannot fill.'.format(self.game.turnNumber, self.id)
    elif self.hasBuilt == 1:
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
    
    self.hasBuilt = 1
    
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
    elif self.hasDigged == 1:
      return 'Turn {}: Your {} has already dug a trench this turn.'.format(self.game.turnNumber, self.id)
    elif abs(self.x-x) + abs(self.y-y) != 1:
      return 'Turn {}: Your {} can only dig adjacent Tiles. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.isTrench == 1:
      return 'Turn {}: Your {} cannot dig a trench in a trench. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.type != 0:
      return 'Turn {}: Your {} can only dig empty tiles. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.pumpID != -1:
      return 'Turn {}: Your {} can not dig trenches on pump tiles. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.waterAmount > 0:
      return 'Turn {}: Your {} can not dig trenches on ice cap tiles. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif tile.owner == 0 or tile.owner == 1:
      return 'Turn {}: Your {} can not dig trenches on spawn tiles. ({},{}) digs ({},{})'.format(self.game.turn, self.id, self.x, self.y, x, y)
    elif len(self.game.grid[x][y]) > 1:
      return 'Turn {}: Your {} cannot dig under other units. ({},{}) digs ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    
    # Set the Tile to be a trench
    tile.isTrench = 1
    # Unit can no longer move
    self.movementLeft = 0
    
    self.hasDigged = 1
    
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
    
    # Check if target is dead
    if target.healthLeft <= 0:
      self.game.grid[x][y].remove(target)
      self.game.removeObject(target)
    
    return True

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Tile(Mappable):
  game_state_attributes = ['id', 'x', 'y', 'owner', 'type', 'pumpID', 'waterAmount', 'isTrench']
  def __init__(self, game, id, x, y, owner, type, pumpID, waterAmount, isTrench):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.type = type
    self.pumpID = pumpID
    self.waterAmount = waterAmount
    self.isTrench = isTrench
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.type, self.pumpID, self.waterAmount, self.isTrench, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, type = self.type, pumpID = self.pumpID, waterAmount = self.waterAmount, isTrench = self.isTrench, )

  def nextTurn(self):
    #TODO: Tile Next Turn (Possible Flow Logic?)
    pass

  def spawn(self, type):
    player = self.game.objects.players[self.game.playerID]

    if self.owner != self.game.playerID:
      return 'Turn {}: You cannot spawn a unit on a tile you do not own. ({},{})'.format(self.game.turnNumber, self.x, self.y)
    if player.spawnResources < self.game.unitCost:
      return 'Turn {}: You do not have enough resources({}) to spawn this unit({}). ({},{})'.format(self.game.turnNumber, player.spawnResources, self.game.unitCost, tile.x, tile.y)
    if type not in [0,1]:
      return 'Turn {}: You cannot spawn a unit with type {}. ({},{})'.format(self.game.turnNumber, type, self.x, self.y)

    if len(self.game.grid[self.x][self.y]) > 1:
      return 'Turn {} You cannot spawn a unit on top of another unit. ({},{})'.format(self.game.turnNumber, self.x, self.y)

    count = 0
    for unit in self.game.objects.units:
      if unit.owner == self.game.playerID:
        count += 1
    
    if count >= self.game.maxUnits:
      return 'Turn {} You cannot spawn a unit because you already have the maximum amount of units ({})'.format(self.game.turnNumber, self.game.maxUnits)

    player.spawnResources -= self.game.unitCost

    #['id', 'x', 'y', 'owner', 'type', 'hasAttacked', 'hasDigged', 'hasBuilt', 'healthLeft', 'maxHealth', 'movementLeft', 'maxMovement']
    newUnitStats = [self.x, self.y, self.owner, type, 0, 0, 0, self.game.maxHealth, self.game.maxHealth, 1, 1 ]
    player.spawnQueue.append(newUnitStats)

    #TODO: Add spawning animation

    pass

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

class AttackAnimation:
  def __init__(self, actingID, targetID):
    self.actingID = actingID
    self.targetID = targetID

  def toList(self):
    return ["attack", self.actingID, self.targetID, ]

  def toJson(self):
    return dict(type = "attack", actingID = self.actingID, targetID = self.targetID)

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

class DigAnimation:
  def __init__(self, actingID, tileID):
    self.actingID = actingID
    self.tileID = tileID

  def toList(self):
    return ["dig", self.actingID, self.tileID, ]

  def toJson(self):
    return dict(type = "dig", actingID = self.actingID, tileID = self.tileID)
