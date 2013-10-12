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
    self.maxHealth = self.maxHealth
    self.trenchDamage = self.trenchDamage
    self.waterDamage = self.waterDamage
    self.turnNumber = -1
    self.attackDamage = self.attackDamage
    self.offenseCount = self.offenseCount
    self.defenseCount = self.defenseCount
    self.maxUnits = self.maxUnits
    self.unitCost = self.unitCost
    self.playerID = -1
    self.gameNumber = id
    self.turnLimit = self.turnLimit

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
        #['id', 'playerName', 'time', 'waterStored', 'spawnResources']
        startingResources = 1000
        self.addObject(Player, [connection.screenName, self.startTime, 0, startingResources])
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

    # ['id', 'x', 'y', 'owner', 'type', 'pumpID', 'waterAmount', 'isTrench']
    self.grid = [[[ self.addObject(Tile,[x, y, 2, 0, -1, 0, 0]) ] for y in range(self.mapHeight)] for x in range(self.mapWidth)]

    self.create_ice()
    self.create_spawns()
    self.create_pumps()

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
    for i in range(10):
      x = random.randint(0, self.mapWidth / 2 - 1)
      y = random.randint(0, self.mapHeight - 1)
      tile = self.getTile(x, y)
      othertile = self.getTile(self.mapWidth - x - 1, y)
      # Check if it is an empty tile
      if tile and othertile and tile.owner == 2 and tile.pumpID == -1:
        pump = self.addObject(PumpStation,[0, 0, 0])
        tile.owner = 0
        tile.pumpID = pump.id

        otherpump = self.addObject(PumpStation,[1, 0, 0])
        othertile.owner = 1
        othertile.pumpID = otherpump.id
    
  def create_ice(self):
    #set_tiles(self)
    for i in range(10):
      x = random.randint(0, self.mapWidth / 2 - 1)
      y = random.randint(0, self.mapHeight - 1)

      tile = self.getTile(x, y)
      othertile = self.getTile(self.mapWidth - x - 1, y)

      if tile and othertile and tile.owner == 2 and tile.pumpID == -1:
        randwater = random.randint(10, 50)

        tile.owner = 3
        othertile.owner = 3

        tile.waterAmount = randwater
        othertile.waterAmount = randwater
      

  def create_spawns(self):
    #TODO: Better spawner spawning
    #Set Tiles on far sides as spawns
    for y in range(self.mapHeight):
      for x in range(self.mapWidth/2):
          tile = self.getTile(x, y)
          othertile = self.getTile(self.mapWidth - x - 1, y)
          rand = random.random()
          if tile and othertile and rand > .98 and tile.owner == 2 and othertile.owner == 2:
            tile.owner = 0
            othertile.owner = 1
    return

  def waterFlow(self):
    offsets = ([1,0],[0,1],[-1,0],[0,-1])
  
    closedIce = []
  
    # Find every ice tile
    for ice in self.objects.tiles:
      if ice.owner == 3 and ice.waterAmount > 0 and ice not in closedIce:
        open = []
        closed = []
        newTiles = []
        pumps = []
        iceTiles = []
    
        open.append(ice)
        iceTiles.append(ice)
        closedIce.append(ice)
        
        while len(open) > 0:
          # Get next tile in open[]
          tile = open[-1]
          
          # Check neighbors
          for offset in offsets:
            newx = tile.x + offset[0]
            newy = tile.y + offset[1]
            
            # Check if a valid tile
            neighbor = self.getTile(newx, newy)
            if neighbor != None:
              if neighbor not in closed and neighbor not in open:
                # Trench
                if neighbor.isTrench:
                  if neighbor.waterAmount > 0:
                    open.append(neighbor)
                  else:
                    closed.append(neighbor)
                    newTiles.append(neighbor)
                # Pump
                elif neighbor.pumpID != -1:
                  closed.append(neighbor)
                  if neighbor.pumpID not in pumps:
                    pumps.append(neighbor.pumpID)
                # Ice
                elif neighbor.owner == 3 and neighbor not in closedIce:
                  iceTiles.append(neighbor)
                  closedIce.append(neighbor)
                  open.append(neighbor)
          
          open.remove(tile)
          closed.append(tile)
          
        # Check if we need to expand water
        if len(newTiles) > 0:
          # Remove one water from every ice tile in system
          for iceTile in iceTiles:
            iceTile.waterAmount -= 1
            if iceTile.waterAmount <= 0:
              iceTile.owner = 2
              iceTile.waterAmount = 0
          # Fill new tiles with water
          for tile in newTiles:
            tile.waterAmount = 1
            
        # Check for pumps
        if len(pumps) > 0:
          # Remove one water from every ice tile in system
          for iceTile in iceTiles:
            if iceTile.waterAmount > 0:
              iceTile.waterAmount -= 1
              if iceTile.waterAmount <= 0:
                iceTile.owner = 2
                iceTile.waterAmount = 0
          # Give points to owners of pump stations
          for pumpID in pumps:
            self.getPlayerFromId(self.getPump(pumpID).owner).waterStored += 1
            
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
          maxHealth = self.maxHealth,
          trenchDamage = self.trenchDamage,
          waterDamage = self.waterDamage,
          turnNumber = self.turnNumber,
          attackDamage = self.attackDamage,
          offenseCount = self.offenseCount,
          defenseCount = self.defenseCount,
          maxUnits = self.maxUnits,
          unitCost = self.unitCost,
          playerID = self.playerID,
          gameNumber = self.gameNumber,
          Players = [i.toJson() for i in self.objects.values() if i.__class__ is Player],
          Mappables = [i.toJson() for i in self.objects.values() if i.__class__ is Mappable],
          PumpStations = [i.toJson() for i in self.objects.values() if i.__class__ is PumpStation],
          Units = [i.toJson() for i in self.objects.values() if i.__class__ is Unit],
          Tiles = [i.toJson() for i in self.objects.values() if i.__class__ is Tile],
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

    msg.append(["game", self.mapWidth, self.mapHeight, self.maxHealth, self.trenchDamage, self.waterDamage, self.turnNumber, self.attackDamage, self.offenseCount, self.defenseCount, self.maxUnits, self.unitCost, self.playerID, self.gameNumber])

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

    msg.extend(typeLists)

    return msg

  def addAnimation(self, anim):
    # generate the sexp
    self.animations.append(anim.toList())
    # generate the json
    if( self.logJson ):
      self.jsonAnimations.append(anim.toJson())
      
  


loadClassDefaults()

