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

class Unit(Mappable):
  game_state_attributes = ['id', 'x', 'y', 'owner', 'type', 'curHealth', 'maxHealth', 'curMovement', 'maxMovement']
  def __init__(self, game, id, x, y, owner, type, curHealth, maxHealth, curMovement, maxMovement):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.type = type
    self.curHealth = curHealth
    self.maxHealth = maxHealth
    self.curMovement = curMovement
    self.maxMovement = maxMovement
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.type, self.curHealth, self.maxHealth, self.curMovement, self.maxMovement, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, type = self.type, curHealth = self.curHealth, maxHealth = self.maxHealth, curMovement = self.curMovement, maxMovement = self.maxMovement, )
  
  def nextTurn(self):
    pass

  def move(self, x, y):
    pass

  def fill(self, tile):
    pass

  def dig(self, tile):
    pass

  def attack(self, target):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

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

  def toList(self):
    return [self.id, self.playerName, self.time, self.waterStored, self.spawnResources, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, playerName = self.playerName, time = self.time, waterStored = self.waterStored, spawnResources = self.spawnResources, )
  
  def nextTurn(self):
    pass

  def talk(self, message):
    pass

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
    pass

  def spawn(self, type):
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

class FillAnimation:
  def __init__(self, actingID, tileID):
    self.actingID = actingID
    self.tileID = tileID

  def toList(self):
    return ["fill", self.actingID, self.tileID, ]

  def toJson(self):
    return dict(type = "fill", actingID = self.actingID, tileID = self.tileID)

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

class FlowAnimation:
  def __init__(self, sourceID, destID, waterAmount):
    self.sourceID = sourceID
    self.destID = destID
    self.waterAmount = waterAmount

  def toList(self):
    return ["flow", self.sourceID, self.destID, self.waterAmount, ]

  def toJson(self):
    return dict(type = "flow", sourceID = self.sourceID, destID = self.destID, waterAmount = self.waterAmount)

