#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

class AI(BaseAI):
  """The class implementing gameplay logic."""

  WORKER, SCOUT, TANK = range(3)

  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"

  ##This function is called once, before your first turn
  def init(self):
    pass

  ##This function is called once, after your last turn
  def end(self):
    pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    numberOfUnits = 0
    #get the number of units owned
    for u in self.units:
      #if I own this unit increase the count
      if u.owner == self.playerID:
        numberOfUnits += 1
    #look for my tiles
    for tile in self.tiles:
      #if this tile is my spawn tile or my pump station
      if tile.owner == self.playerID:
        #get the unit cost for a worker
        cost = 0
        for u in self.unitTypes:
          if u.type == self.WORKER:
            cost = u.cost
        #if there is enough oxygen to spawn the unit
        if self.players[self.playerID].oxygen >= cost:
          #if can spawn more units in
          if numberOfUnits < self.maxUnits:
            #if nothing is spawning on the tile
            if tile.isSpawning == 0:
              canSpawn = True
              #if it is a pump station and it's not being sieged
              if tile.pumpID != -1:
                #find the pump in the vector
                for pump in self.pumpStations:
                  if pump.id == tile.pumpID and pump.siegeAmount > 0:
                    canSpawn = False
              #if there is someone else on the tile, don't spawn
              for other in self.units:
                if tile.x == other.x and tile.y == other.y:
                  canSpawn = False
              if canSpawn:
                #spawn the unit
                tile.spawn(self.WORKER)
                numberOfUnits += 1
    moveDelta = 0
    if self.playerID == 0:
      moveDelta = 1
    else:
      moveDelta = -1

    #do stuff for each unit
    for unit in self.units:
      #if you own the unit
      if unit.owner != self.playerID:
        continue
      #try to move to the right or left movement times
      for i in range(unit.maxMovement):
        canMove = True
        #if there is no unit there
        for others in self.units:
          if unit.x + moveDelta == others.x and unit.y == others.y:
            canMove = False
        #if nothing's there and it's not moving off the edge of the map
        if canMove and (0 <= unit.x + moveDelta < self.mapWidth):
          #if the tile is not an enemy spawn point
          if (not (self.tiles[(unit.x + moveDelta) * self.mapHeight + unit.y].pumpID == -1 and \
                   self.tiles[(unit.x + moveDelta) * self.mapHeight + unit.y].owner == 1 - self.playerID)) or \
             self.tiles[(unit.x + moveDelta) * self.mapHeight + unit.y].owner == 2:
             #if the tile is not an ice tile
             if not (self.tiles[(unit.x + moveDelta) * self.mapHeight + unit.y].owner == 3 and
                     self.tiles[(unit.x + moveDelta) * self.mapHeight + unit.y].waterAmount > 0):
              #if the tile is not spawning anything
              if self.tiles[(unit.x + moveDelta) * self.mapHeight + unit.y].isSpawning == 0:
                #if the unit is alive
                if unit.healthLeft > 0:
                  #move the unit
                  unit.move(unit.x + moveDelta, unit.y)
      #if there is an enemy in the movement direction and the unit hasn't
      #attacked and it is alive
      if unit.hasAttacked == 0 and unit.healthLeft > 0:
        for other in self.units:
          #check if there is an enemy unit in the direction
          if unit.x + moveDelta == other.x and \
             unit.y == other.y and other.owner != self.playerID:
            #attack it
            unit.attack(other)
            break
      #if there is a space to dig below the unit and the unit hasn't dug
      #and the unit is alive
      if unit.y != self.mapHeight - 1 and \
         self.tiles[unit.x * self.mapHeight + unit.y + 1].pumpID == -1 and \
         self.tiles[unit.x * self.mapHeight + unit.y + 1].owner == 2 and \
         unit.hasDug == False and unit.healthLeft > 0:
        canDig = True
        #make sure there is no unit on that tile
        for other in self.units:
          if unit.x == other.x and unit.y + 1 == other.y:
            canDig = False
        #make sure the tile is not an ice tile
        if(canDig and \
           not (self.tiles[unit.x * self.mapHeight + unit.y + 1].owner == 3 and \
                self.tiles[unit.x * self.mapHeight + unit.y + 1].waterAmount > 0)):
          unit.dig(self.tiles[unit.x * self.mapHeight + unit.y + 1])
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
