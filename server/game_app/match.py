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
#from mapGenerator import set_tiles


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
          Mappables = [i.toJson() for i in self.objects.values() if i.__class__ is Mappable],
          Units = [i.toJson() for i in self.objects.values() if i.__class__ is Unit],
          Players = [i.toJson() for i in self.objects.values() if i.__class__ is Player],
          Tiles = [i.toJson() for i in self.objects.values() if i.__class__ is Tile],
          PumpStations = [i.toJson() for i in self.objects.values() if i.__class__ is PumpStation],
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
        for tile in self.object.tile:
            totalWater += tile.waterAmount

        earlyWin = abs(p1w-p2w) > totalWater

    #TODO:Condition for early win if difference in water levels is less than water remaining in icecap
        if self.turnNumber >= self.turnLimit or earlyWin:
            # Player 1 wins if they have more water stored
            if p1w > p2w:
                self.declareWinner(self.players[0], "Player 1 wins through more water stored")
            # Player 2 wins if they have more water stored
            elif p2w > p1w:
                self.declareWinner(self.players[0], "Player 2 wins through more water stored")
            #TIE CONDITIONS:
            else:
                #TODO: Tie condition, number of bases owned might determine winner
                # Get the total number of pump stations
                p1p = 0
                p2p = 0
                for pump in self.object.pumpstation:
                    if pump.owner == 0:
                        p1p += 1
                    else:
                        p2p += 1
                # Player 1 wins if they own more pump stations
                if p1p > p2p:
                    self.declareWinner(self.players[0], "Player 1 wins through more pump stations")
                # Player 2 wins if they own more pump stations
                elif p1p < p2p:
                    self.declareWinner(self.players[0], "Player 1 wins through more pump stations")
                else:
                    # Get the total number of units
                    p1u = 0
                    p2u = 0
                    for unit in self.mappable.unit:
                        if unit.owner == 0:
                            p1 += 1
                        else:
                            p2 += 1
                    # Player 1 wins if they have more units
                    if p1u > p2u:
                        self.declareWinner(self.players[0], "Player 2 wins through more units")
                    elif p2u > p1u:
                        self.declareWinner(self.players[0], "Player 2 wins through more units")
                    else:
                        # Get the total current health
                        p1h = 0
                        p2h = 0
                        for unit in self.mappable.unit:
                            if unit.owner == 0:
                                p1h += unit.curHealth
                            else:
                                p2h += unit.curHealth
                        # Player 1 wins if they have more health
                        if p1h > p2h:
                            self.declareWinner(self.players[0], "Player 1 wins through more total health")
                        # Player 2 wins if they have more health
                        elif p2h > p1h:
                            self.declareWinner(self.players[0], "Player 2 wins through more total health")
                        else:
                            # Get the number of trenches owned
                            p1t = 0
                            p2t = 0
                            for trench in self.mappable.tile:
                                if unit.isTrench and unit.owner == 0:
                                    p1t += 1
                                else:
                                    p2t += 1
                            # Player 1 wins if they have dug more trenches
                            if p1t > p2t:
                                self.declareWinner(self.players[0], "Player 2 wins through more trenches")
                            # Player 2 wins if they have dug more trenches
                            elif p2t > p1t:
                                self.declareWinner(self.players[0], "Player 2 wins through more trenches")
                            else:
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

  @derefArgs(Player, None)
  def talk(self, object, message):
    return object.talk(message, )

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

    msg.append(["game", self.maxHealth, self.trenchDamage, self.waterDamage, self.turnNumber, self.attackDamage, self.offenseCount, self.defenseCount, self.maxUnits, self.unitCost])

    typeLists = []
    typeLists.append(["Mappable"] + [i.toList() for i in self.objects.values() if i.__class__ is Mappable])
    typeLists.append(["Unit"] + [i.toList() for i in self.objects.values() if i.__class__ is Unit])
    typeLists.append(["Player"] + [i.toList() for i in self.objects.values() if i.__class__ is Player])
    updated = [i for i in self.objects.values() if i.__class__ is Tile and i.updatedAt > self.turnNumber-3]
    if updated:
      typeLists.append(["Tile"] + [i.toList() for i in updated])
    updated = [i for i in self.objects.values() if i.__class__ is PumpStation and i.updatedAt > self.turnNumber-3]
    if updated:
      typeLists.append(["PumpStation"] + [i.toList() for i in updated])

    msg.extend(typeLists)

    return msg

  def addAnimation(self, anim):
    # generate the sexp
    self.animations.append(anim.toList())
    # generate the json
    if( self.logJson ):
      self.jsonAnimations.append(anim.toJson())
      
  


loadClassDefaults()

