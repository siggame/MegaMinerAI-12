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
import mapGenerator
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
        self.addObject(Player, [connection.screenName, self.startTime])
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

    #TODO: START STUFF
    self.turn = self.players[-1]
    self.turnNumber = -1
    
    self.grid = [[[ self.addObject(Tile,[x, y, 2, 0, 0, 0, 1]) ] for y in range(self.mapHeight)] for x in range(self.mapWidth)]
    set_tiles(self)

    self.nextTurn()
    return True

  def waterFlow(self):
      #TODO: Create water flow conditions to move water from icecaps to pump stations
      pass

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
          Units = [i.toJson() for i in self.objects.values() if i.__class__ is Unit],
          PumpStations = [i.toJson() for i in self.objects.values() if i.__class__ is PumpStation],
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
        p1h = player1.waterStored
        p2h = player2.waterStored
    
    if self.turnNumber >= self.turnLimit:
       if p1h>p2h:
           self.declareWinner(self.players[0], "Player 1 wins through more water stored")
       elif p2h>p1h:
           self.declareWinner(self.players[1], "Player 2 wins through more water storage")
       else:
           #TODO: Tie condition, number of bases owned might determine winner
           pass
       


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

    msg.append(["game", self.maxHealth, self.trenchDamage, self.waterDamage, self.turnNumber, self.attackDamage, self.offenseCount, self.defenseCount, self.maxUnits, self.unitCost, self.playerID, self.gameNumber])

    typeLists = []
    typeLists.append(["Player"] + [i.toList() for i in self.objects.values() if i.__class__ is Player])
    typeLists.append(["Mappable"] + [i.toList() for i in self.objects.values() if i.__class__ is Mappable])
    typeLists.append(["Unit"] + [i.toList() for i in self.objects.values() if i.__class__ is Unit])
    updated = [i for i in self.objects.values() if i.__class__ is PumpStation and i.updatedAt > self.turnNumber-3]
    if updated:
      typeLists.append(["PumpStation"] + [i.toList() for i in updated])
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

