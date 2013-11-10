from base import *
from matchUtils import *
from objects import *
import networking.config.config
from collections import defaultdict
from networking.sexpr.sexpr import *
import os
import itertools
import scribe
import jsonLogger
from mapGenerator import set_tiles
import random
#import set_tiles


Scribe = scribe.Scribe

def loadClassDefaults(cfgFile = "config/defaults.cfg"):
  cfg = networking.config.config.readConfig(cfgFile)
  for className in cfg.keys():
    for attr in cfg[className]:
      setattr(eval(className), attr, cfg[className][attr])

class Match(DefaultGameWorld):
  def __init__(self, id, controller):
    self.id = int(id)
    self.controller = controller
    DefaultGameWorld.__init__(self)
    self.scribe = Scribe(self.logPath())
    if( self.logJson ):
      self.jsonLogger = jsonLogger.JsonLogger(self.logPath())
      self.jsonAnimations = []
      self.dictLog = dict(gameName = "Mars", turns = [])
    self.addPlayer(self.scribe, "spectator")

    self.mapWidth = self.mapWidth
    self.mapHeight = self.mapHeight
    self.waterDamage = self.waterDamage
    self.turnNumber = -1
    self.maxUnits = self.maxUnits
    self.playerID = -1
    self.gameNumber = id
    self.turnLimit = self.turnLimit
    self.maxSiege = self.maxSiege
    self.oxygenRate = self.oxygenRate
    self.maxOxygen = self.maxOxygen
    self.depositionRate = self.depositionRate

    self.startingOxygen = self.maxOxygen

    self.ice = []

  #this is here to be wrapped
  def __del__(self):
    pass

  def addPlayer(self, connection, type="player"):
    connection.type = type
    if len(self.players) >= 2 and type == "player":
      return "Game is full"
    if type == "player":
      self.players.append(connection)
      try:
        #['id', 'playerName', 'time', 'waterStored', 'oxygen', 'maxOxygen']
        self.addObject(Player, [connection.screenName, self.startTime, 0, self.startingOxygen, self.maxOxygen])
      except TypeError:
        raise TypeError("Someone forgot to add the extra attributes to the Player object initialization")
    elif type == "spectator":
      self.spectators.append(connection)
      #If the game has already started, send them the ident message
      if (self.turn is not None):
        self.sendIdent([connection])
    return True

  def removePlayer(self, connection):
    if connection in self.players:
      if self.turn is not None:
        winner = self.players[1 - self.getPlayerIndex(connection)]
        self.declareWinner(winner, 'Opponent Disconnected')
      self.players.remove(connection)
    else:
      self.spectators.remove(connection)

  def start(self):
    if len(self.players) < 2:
      return "Game is not full"
    if self.winner is not None or self.turn is not None:
      return "Game has already begun"

    self.turn = self.players[-1]
    self.turnNumber = -1
    # ['id', 'x', 'y', 'owner', 'pumpID', 'waterAmount', 'depth', 'turnsUntilDeposit']
    # ['id', 'x', 'y', 'owner', 'pumpID', 'waterAmount', 'depth']
    self.grid = [[[ self.addObject(Tile,[x, y, 2, -1, 0, 0, 0, 0]) ] for y in range(self.mapHeight)] for x in range(self.mapWidth)]

    statList = ["name", "type", "cost", "attackPower", "digPower", "fillPower", "maxHealth", "maxMovement", "offensePower", "defensePower", "range"]
    unitTypes = cfgTypes.values()
    unitTypes.sort(key=lambda unitType: unitType['type'])
    for t in unitTypes:
      self.addObject(UnitType, [t[value] for value in statList])
    
    self.create_ice()
    self.create_spawns()
    self.create_pumps()

    for pump in self.objects.pumpStations:
      pump.create_siegeTiles()

    self.unitTypesDict = {units.type:units for units in self.objects.unitTypes}

    self.nextTurn()

    return True

  def getTile(self, x, y):
    if (0 <= x < self.mapWidth) and (0 <= y < self.mapHeight):
      return self.grid[x][y][0]
    else:
      return None
    
  def getPump(self, pumpID):
    return next((pump for pump in self.objects.pumpStations if pump.id == pumpID), None)

  def getPlayerFromId(self, playerID):
    return next((player for player in self.objects.players if player.id == playerID), None)
    
  def create_pumps(self):
    # Create randomly placed pump stations
    squareOffsets = [
      (0,0),(1,0),(0,1),(1,1)
    ]
    bigSquareOffsets = [
      (-1,0),(-1,-1),(0,-1),(1,-1),(2,-1),(2,0),(2,1),(2,2),(1,2),(0,2),(-1,2),(-1,1)
    ]
    for _ in xrange(self.numPumpStations):
      x = y = 0
      done = False
      while not done:
        x = random.randint(0, self.mapWidth / 2 - 3)
        y = random.randint(0, self.mapHeight - 2)
        valid = True
        # Check 2x2 square
        for tileOffset in squareOffsets:
          if self.getTile(x + tileOffset[0], y + tileOffset[1]).owner != 2:
            valid = False
            break
        if valid:
          # Check 4x4 Square
          for tileOffset in bigSquareOffsets:
            tile = self.getTile(x + tileOffset[0], y + tileOffset[1])
            if tile and tile.owner != 2:
              valid = False
              break
        done = valid
      pump = self.addObject(PumpStation,[0, 0])
      otherPump = self.addObject(PumpStation,[1, 0])
      for tileOffset in squareOffsets:
        tile = self.getTile(x + tileOffset[0], y + tileOffset[1])
        otherTile = self.getTile(self.mapWidth - tile.x - 1, tile.y)
        tile.pumpID = pump.id
        otherTile.pumpID = otherPump.id
        tile.owner = 0
        otherTile.owner = 1

    # Create paths to pump stations
    # All pumps on left side of map
    pumps = [pump for pump in self.objects.pumpStations if pump.owner == 0]
    # NOTE: make sure numPaths <= numPumpStations
    for _ in xrange(self.numPaths):
      # Select a random pump from left side
      pump = random.choice(pumps)
      # Remove that pump so that the next path doesn't go to same pump
      pumps.remove(pump)
      # Select a random tile from that pump
      pumpTile = random.choice([tile for tile in self.objects.tiles if tile.pumpID == pump.id])
      # Find the nearest ice tile on left side of map
      iceTile = min([tile for tile in self.objects.tiles if tile.owner == 3 and tile.x <= self.mapWidth / 2],
        key=lambda tile: abs(tile.x - pumpTile.x) + abs(tile.y - pumpTile.y))
      # Find path between them
      path = aStar(self, pumpTile, iceTile,
        lambda tile: (tile.owner == 2 or tile.owner == 3) and (tile.x < self.mapWidth / 2))
      # Dig it up on both sides of map
      if path is not None:
        for tile in path:
          if tile.owner == 2:
            otherTile = self.getTile((self.mapWidth - tile.x) - 1, tile.y)
            if otherTile is None:
              print('Bad trench path ? : ({},{})'.format(tile.x, tile.y))
            tile.depth = 100000
            otherTile.depth = 100000
            # TODO: add large dugness value to trench

  def create_ice(self):
    for _ in xrange(self.numIceTiles):
      x = y = 0
      done = False
      while not done:
        x = random.randint(0, self.mapWidth / 2 - 1)
        y = random.randint(0, self.mapHeight - 1)
        tile = self.getTile(x, y)
        if tile and tile.owner == 2:
          done = True
      randWaterAmount = random.randint(self.minWaterPerIceTile, self.maxWaterPerIceTile)
      tile = self.getTile(x, y)
      otherTile = self.getTile(self.mapWidth - x - 1, y)
      tile.owner = 3
      otherTile.owner = 3
      tile.waterAmount = randWaterAmount
      otherTile.waterAmount = randWaterAmount
      self.ice.append(tile)
      self.ice.append(otherTile)

  def typeToUnitType(self, type):
    for unittype in self.objects.unitTypes:
      if unittype.type == type:
        return unittype
    return None

  def create_spawns(self):
    # Create spawn point in back of base
    homeBaseOffsets = [(0,-1),(0,0),(0,1)]
    done = False
    while not done:
      y = self.mapHeight / 2 + random.randint(-7, 7)
      done = True
      for offset in homeBaseOffsets:
        tile = self.getTile(0 + offset[0], y + offset[1])
        if not tile or tile.owner != 2:
          done = False
    for offset in homeBaseOffsets:
      tile = self.getTile(0 + offset[0], y + offset[1])
      otherTile = self.getTile(self.mapWidth - tile.x - 1, tile.y)
      tile.owner = 0
      otherTile.owner = 1

    # Create random spawn points
    for _ in xrange(random.randint(self.minRandSpawnPoints, self.maxRandSpawnPoints)):
      done = False
      while not done:
        x = random.randint(0, self.mapWidth / 2 - self.spawnPointBufferSpace)
        y = random.randint(0, self.mapHeight - 1)
        tile = self.getTile(x, y)
        if tile and tile.owner == 2:
          done = True
      otherTile = self.getTile(self.mapWidth - tile.x - 1, tile.y)
      tile.owner = 0
      otherTile.owner = 1
    return



  def adjacent(self, tile):
    adj = []
    if tile.x+1 < self.mapWidth:
        adj.append(self.getTile(tile.x+1, tile.y))
    if tile.y-1 >= 0:
        adj.append(self.getTile(tile.x, tile.y-1))
    if tile.x-1 >= 0:
        adj.append(self.getTile(tile.x-1, tile.y))
    if tile.y+1 < self.mapHeight:
        adj.append(self.getTile(tile.x, tile.y+1))
    return adj 
  
  def waterFlow(self):
    for ice in self.ice:
      open = [ice]
      closed = set()
      flowTiles = set()
      while len(open) > 0:
        current = open.pop()
        closed.add(current)
        neighbors = self.adjacent(current)
        for neighbor in neighbors:
          if neighbor in closed or neighbor.pumpID in closed:
            continue
          #if it is a tile that needs water
          if neighbor.depth > 0 and neighbor.waterAmount == 0:
            closed.add(neighbor)
            flowTiles.add(neighbor)
          #if it is a pump station taking in water 
          elif neighbor.pumpID != -1 and self.objects[neighbor.pumpID].owner in [0, 1]:
            closed.add(neighbor.pumpID)
            flowTiles.add(self.objects[neighbor.pumpID])
          #if it is dug with water
          elif (neighbor.waterAmount > 0 and neighbor.depth > 0) and neighbor not in open:
            open.append(neighbor)          
            
      #if enough water is in ice to flow to all tiles
      if len(flowTiles) <= ice.waterAmount:
        for flowable in flowTiles:
          if isinstance(flowable, Tile):
            flowable.waterAmount += 1
            ice.waterAmount -= 1
          elif isinstance(flowable, PumpStation):
            self.objects.players[flowable.owner].waterStored += 1
            ice.waterAmount -= 1
    return    

   


  def nextTurn(self):
    self.turnNumber += 1
    if self.turn == self.players[0]:
      self.turn = self.players[1]
      self.playerID = 1
    elif self.turn == self.players[1]:
      self.turn = self.players[0]
      self.playerID = 0

    else:
      return "Game is over."

    for obj in self.objects.values():
      obj.nextTurn()

    self.checkWinner()
    if self.winner is None:
      self.sendStatus([self.turn] +  self.spectators)
    else:
      self.sendStatus(self.spectators)
    
    if( self.logJson ):
      self.dictLog['turns'].append(
        dict(
          mapWidth = self.mapWidth,
          mapHeight = self.mapHeight,
          waterDamage = self.waterDamage,
          turnNumber = self.turnNumber,
          maxUnits = self.maxUnits,
          playerID = self.playerID,
          gameNumber = self.gameNumber,
          maxSiege = self.maxSiege,
          oxygenRate = self.oxygenRate,
          depositionRate = self.depositionRate,
          Players = [i.toJson() for i in self.objects.values() if i.__class__ is Player],
          Mappables = [i.toJson() for i in self.objects.values() if i.__class__ is Mappable],
          PumpStations = [i.toJson() for i in self.objects.values() if i.__class__ is PumpStation],
          Units = [i.toJson() for i in self.objects.values() if i.__class__ is Unit],
          Tiles = [i.toJson() for i in self.objects.values() if i.__class__ is Tile],
          UnitTypes = [i.toJson() for i in self.objects.values() if i.__class__ is UnitType],
          animations = self.jsonAnimations
        )
      )
      self.jsonAnimations = []

    self.animations = ["animations"]
    return True

  def checkWinner(self):
    #TODO: Make this check if a player won, and call declareWinner with a player if they did
    # Get the players
    player1 = self.objects.players[0]
    player2 = self.objects.players[1]

    # Get the current water stored
    p1w = player1.waterStored
    p2w = player2.waterStored
        
    # Get the total water left in ice caps
    totalWater = 0
    for tile in self.objects.tiles:
        totalWater += tile.waterAmount

    earlyWin = abs(p1w-p2w) > totalWater

    #TODO:Condition for early win if difference in water levels is less than water remaining in icecap
    if self.turnNumber >= self.turnLimit or earlyWin:
      # Player 1 wins if they have more water stored
      if p1w > p2w:
          self.declareWinner(self.players[0], "Player 1 wins through more water stored")
      # Player 2 wins if they have more water stored
      elif p2w > p1w:
          self.declareWinner(self.players[1], "Player 2 wins through more water stored")
      #TIE CONDITIONS:
      else:
        #TODO: Tie condition, number of bases owned might determine winner
        # Get the total number of pump stations
        p1p = 0
        p2p = 0
        for pump in self.objects.pumpStations:
          if pump.owner == 0:
            p1p += 1
          else:
            p2p += 1
        # Player 1 wins if they own more pump stations
        if p1p > p2p:
          self.declareWinner(self.players[0], "Player 1 wins through more pump stations")
        # Player 2 wins if they own more pump stations
        elif p1p < p2p:
          self.declareWinner(self.players[1], "Player 2 wins through more pump stations")
        else:
          # Get the total number of units
          p1u = 0
          p2u = 0
          for unit in self.objects.units:
            if unit.owner == 0:
              p1u += 1
            else:
              p2u += 1
          # Player 1 wins if they have more units
          if p1u > p2u:
            self.declareWinner(self.players[0], "Player 1 wins through more units")
          elif p2u > p1u:
            self.declareWinner(self.players[1], "Player 2 wins through more units")
          else:
            # Get the total current health
            p1h = 0
            p2h = 0
            for unit in self.objects.units:
              if unit.owner == 0:
                p1h += unit.healthLeft
              else:
                p2h += unit.healthLeft
            # Player 1 wins if they have more health
            if p1h > p2h:
              self.declareWinner(self.players[0], "Player 1 wins through more total health")
            # Player 2 wins if they have more health
            elif p2h > p1h:
              self.declareWinner(self.players[1], "Player 2 wins through more total health")
            else:
              #Toss a coin to choose winner
              win = random.randint(0,1)
              if win == 0:
                self.declareWinner(self.players[0], "Player 1 wins through a coin toss")
              else:
                self.declareWinner(self.players[1], "Player 2 wins through a coin toss")
    return

  def declareWinner(self, winner, reason=''):
    print "Player", self.getPlayerIndex(self.winner), "wins game", self.id
    self.winner = winner

    msg = ["game-winner", self.id, self.winner.user, self.getPlayerIndex(self.winner), reason]
    
    if( self.logJson ):
      self.dictLog["winnerID"] =  self.getPlayerIndex(self.winner)
      self.dictLog["winReason"] = reason
      self.jsonLogger.writeLog( self.dictLog )
    
    self.scribe.writeSExpr(msg)
    self.scribe.finalize()
    self.removePlayer(self.scribe)

    for p in self.players + self.spectators:
      p.writeSExpr(msg)
    
    self.sendStatus([self.turn])
    self.playerID ^= 1
    self.sendStatus([self.players[self.playerID]])
    self.playerID ^= 1
    self.turn = None
    self.objects.clear()

  def logPath(self):
    return "logs/" + str(self.id)

  @derefArgs(Player, None)
  def talk(self, object, message):
    return object.talk(message, )

  @derefArgs(Unit, None, None)
  def move(self, object, x, y):
    return object.move(x, y, )

  @derefArgs(Unit, Tile)
  def fill(self, object, tile):
    return object.fill(tile, )

  @derefArgs(Unit, Tile)
  def dig(self, object, tile):
    return object.dig(tile, )

  @derefArgs(Unit, Unit)
  def attack(self, object, target):
    return object.attack(target, )

  @derefArgs(Tile, None)
  def spawn(self, object, type):
    return object.spawn(type, )


  def sendIdent(self, players):
    if len(self.players) < 2:
      return False
    list = []
    for i in itertools.chain(self.players, self.spectators):
      list += [[self.getPlayerIndex(i), i.user, i.screenName, i.type]]
    for i in players:
      i.writeSExpr(['ident', list, self.id, self.getPlayerIndex(i)])

  def getPlayerIndex(self, player):
    try:
      playerIndex = self.players.index(player)
    except ValueError:
      playerIndex = -1
    return playerIndex

  def sendStatus(self, players):
    for i in players:
      i.writeSExpr(self.status())
      i.writeSExpr(self.animations)
    return True


  def status(self):
    msg = ["status"]

    msg.append(["game", self.mapWidth, self.mapHeight, self.waterDamage, self.turnNumber, self.maxUnits, self.playerID, self.gameNumber, self.maxSiege, self.oxygenRate, self.depositionRate])

    typeLists = []
    typeLists.append(["Player"] + [i.toList() for i in self.objects.values() if i.__class__ is Player])
    typeLists.append(["Mappable"] + [i.toList() for i in self.objects.values() if i.__class__ is Mappable])
    updated = [i for i in self.objects.values() if i.__class__ is PumpStation and i.updatedAt > self.turnNumber-3]
    if updated:
      typeLists.append(["PumpStation"] + [i.toList() for i in updated])
    typeLists.append(["Unit"] + [i.toList() for i in self.objects.values() if i.__class__ is Unit])
    updated = [i for i in self.objects.values() if i.__class__ is Tile and i.updatedAt > self.turnNumber-3]
    if updated:
      typeLists.append(["Tile"] + [i.toList() for i in updated])
    updated = [i for i in self.objects.values() if i.__class__ is UnitType and i.updatedAt > self.turnNumber-3]
    if updated:
      typeLists.append(["UnitType"] + [i.toList() for i in updated])

    msg.extend(typeLists)

    return msg

  def addAnimation(self, anim):
    # generate the sexp
    self.animations.append(anim.toList())
    # generate the json
    if( self.logJson ):
      self.jsonAnimations.append(anim.toJson())
      
  


loadClassDefaults()

