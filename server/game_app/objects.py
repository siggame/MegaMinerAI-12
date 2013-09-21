class PumpStation(object):
  game_state_attributes = ['id', 'owner', 'waterAmount', 'seigeCount']
  def __init__(self, game, id, owner, waterAmount, seigeCount):
    self.game = game
    self.id = id
    self.owner = owner
    self.waterAmount = waterAmount
    self.seigeCount = seigeCount
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.owner, self.waterAmount, self.seigeCount, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, owner = self.owner, waterAmount = self.waterAmount, seigeCount = self.seigeCount, )
  
  def nextTurn(self):
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

class Player(object):
  game_state_attributes = ['id', 'playerName', 'time', 'waterStored', 'spawnRate']
  def __init__(self, game, id, playerName, time, waterStored, spawnRate):
    self.game = game
    self.id = id
    self.playerName = playerName
    self.time = time
    self.waterStored = waterStored
    self.spawnRate = spawnRate
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.playerName, self.time, self.waterStored, self.spawnRate, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, playerName = self.playerName, time = self.time, waterStored = self.waterStored, spawnRate = self.spawnRate, )
  
  def nextTurn(self):
    pass

  def talk(self, message):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Tile(Mappable):
  game_state_attributes = ['id', 'x', 'y', 'owner', 'type', 'resId', 'waterAmount', 'isTrench']
  def __init__(self, game, id, x, y, owner, type, resId, waterAmount, isTrench):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.type = type
    self.resId = resId
    self.waterAmount = waterAmount
    self.isTrench = isTrench
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.type, self.resId, self.waterAmount, self.isTrench, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, type = self.type, resId = self.resId, waterAmount = self.waterAmount, isTrench = self.isTrench, )
  
  def nextTurn(self):
    pass

  def spawn(self, type):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Unit(Mappable):
  game_state_attributes = ['id', 'x', 'y', 'owner', 'type', 'curHealth', 'curMovement', 'maxMovement']
  def __init__(self, game, id, x, y, owner, type, curHealth, curMovement, maxMovement):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.type = type
    self.curHealth = curHealth
    self.curMovement = curMovement
    self.maxMovement = maxMovement
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.type, self.curHealth, self.curMovement, self.maxMovement, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, type = self.type, curHealth = self.curHealth, curMovement = self.curMovement, maxMovement = self.maxMovement, )
  
  def nextTurn(self):
    pass

  def move(self, x, y):
    pass

  def attack(self, unit):
    pass

  def fill(self, tile):
    pass

  def build(self, tile):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)


# The following are animations and do not need to have any logic added
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

