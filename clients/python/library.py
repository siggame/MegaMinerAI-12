# -*-python-*-

import os

from ctypes import *

try:
  if os.name == 'posix':
    library = CDLL("./libclient.so")
  elif os.name == 'nt':
    library = CDLL("./client.dll")
  else:
    raise Exception("Unrecognized OS: "+os.name)
except OSError:
  raise Exception("It looks like you didn't build libclient. Run 'make' and try again.")

# commands

library.createConnection.restype = c_void_p
library.createConnection.argtypes = []

library.serverConnect.restype = c_int
library.serverConnect.argtypes = [c_void_p, c_char_p, c_char_p]

library.serverLogin.restype = c_int
library.serverLogin.argtypes = [c_void_p, c_char_p, c_char_p]

library.createGame.restype = c_int
library.createGame.argtypes = [c_void_p]

library.joinGame.restype = c_int
library.joinGame.argtypes = [c_void_p, c_int, c_char_p]

library.endTurn.restype = None
library.endTurn.argtypes = [c_void_p]

library.getStatus.restype = None
library.getStatus.argtypes = [c_void_p]

library.networkLoop.restype = c_int
library.networkLoop.argtypes = [c_void_p]

#Functions
library.tileSpawn.restype = c_int
library.tileSpawn.argtypes = [c_void_p, c_int]

library.unitMove.restype = c_int
library.unitMove.argtypes = [c_void_p, c_int, c_int]

library.unitFill.restype = c_int
library.unitFill.argtypes = [c_void_p, c_void_p]

library.unitDig.restype = c_int
library.unitDig.argtypes = [c_void_p, c_void_p]

library.unitAttack.restype = c_int
library.unitAttack.argtypes = [c_void_p, c_void_p]

library.playerTalk.restype = c_int
library.playerTalk.argtypes = [c_void_p, c_char_p]

# accessors

#Globals
library.getMapWidth.restype = c_int
library.getMapWidth.argtypes = [c_void_p]

library.getMapHeight.restype = c_int
library.getMapHeight.argtypes = [c_void_p]

library.getMaxHealth.restype = c_int
library.getMaxHealth.argtypes = [c_void_p]

library.getTrenchDamage.restype = c_int
library.getTrenchDamage.argtypes = [c_void_p]

library.getWaterDamage.restype = c_int
library.getWaterDamage.argtypes = [c_void_p]

library.getTurnNumber.restype = c_int
library.getTurnNumber.argtypes = [c_void_p]

library.getAttackDamage.restype = c_int
library.getAttackDamage.argtypes = [c_void_p]

library.getOffensePower.restype = c_int
library.getOffensePower.argtypes = [c_void_p]

library.getDefensePower.restype = c_int
library.getDefensePower.argtypes = [c_void_p]

library.getMaxUnits.restype = c_int
library.getMaxUnits.argtypes = [c_void_p]

library.getUnitCost.restype = c_int
library.getUnitCost.argtypes = [c_void_p]

library.getPlayerID.restype = c_int
library.getPlayerID.argtypes = [c_void_p]

library.getGameNumber.restype = c_int
library.getGameNumber.argtypes = [c_void_p]

library.getMaxSiege.restype = c_int
library.getMaxSiege.argtypes = [c_void_p]

library.getMappable.restype = c_void_p
library.getMappable.argtypes = [c_void_p, c_int]

library.getMappableCount.restype = c_int
library.getMappableCount.argtypes = [c_void_p]

library.getTile.restype = c_void_p
library.getTile.argtypes = [c_void_p, c_int]

library.getTileCount.restype = c_int
library.getTileCount.argtypes = [c_void_p]

library.getUnit.restype = c_void_p
library.getUnit.argtypes = [c_void_p, c_int]

library.getUnitCount.restype = c_int
library.getUnitCount.argtypes = [c_void_p]

library.getPlayer.restype = c_void_p
library.getPlayer.argtypes = [c_void_p, c_int]

library.getPlayerCount.restype = c_int
library.getPlayerCount.argtypes = [c_void_p]

library.getPumpStation.restype = c_void_p
library.getPumpStation.argtypes = [c_void_p, c_int]

library.getPumpStationCount.restype = c_int
library.getPumpStationCount.argtypes = [c_void_p]

# getters

#Data
library.mappableGetId.restype = c_int
library.mappableGetId.argtypes = [c_void_p]

library.mappableGetX.restype = c_int
library.mappableGetX.argtypes = [c_void_p]

library.mappableGetY.restype = c_int
library.mappableGetY.argtypes = [c_void_p]

library.tileGetId.restype = c_int
library.tileGetId.argtypes = [c_void_p]

library.tileGetX.restype = c_int
library.tileGetX.argtypes = [c_void_p]

library.tileGetY.restype = c_int
library.tileGetY.argtypes = [c_void_p]

library.tileGetOwner.restype = c_int
library.tileGetOwner.argtypes = [c_void_p]

library.tileGetPumpID.restype = c_int
library.tileGetPumpID.argtypes = [c_void_p]

library.tileGetWaterAmount.restype = c_int
library.tileGetWaterAmount.argtypes = [c_void_p]

library.tileGetIsTrench.restype = c_int
library.tileGetIsTrench.argtypes = [c_void_p]

library.unitGetId.restype = c_int
library.unitGetId.argtypes = [c_void_p]

library.unitGetX.restype = c_int
library.unitGetX.argtypes = [c_void_p]

library.unitGetY.restype = c_int
library.unitGetY.argtypes = [c_void_p]

library.unitGetOwner.restype = c_int
library.unitGetOwner.argtypes = [c_void_p]

library.unitGetType.restype = c_int
library.unitGetType.argtypes = [c_void_p]

library.unitGetHasAttacked.restype = c_int
library.unitGetHasAttacked.argtypes = [c_void_p]

library.unitGetHasDug.restype = c_int
library.unitGetHasDug.argtypes = [c_void_p]

library.unitGetHasFilled.restype = c_int
library.unitGetHasFilled.argtypes = [c_void_p]

library.unitGetHealthLeft.restype = c_int
library.unitGetHealthLeft.argtypes = [c_void_p]

library.unitGetMaxHealth.restype = c_int
library.unitGetMaxHealth.argtypes = [c_void_p]

library.unitGetMovementLeft.restype = c_int
library.unitGetMovementLeft.argtypes = [c_void_p]

library.unitGetMaxMovement.restype = c_int
library.unitGetMaxMovement.argtypes = [c_void_p]

library.playerGetId.restype = c_int
library.playerGetId.argtypes = [c_void_p]

library.playerGetPlayerName.restype = c_char_p
library.playerGetPlayerName.argtypes = [c_void_p]

library.playerGetTime.restype = c_float
library.playerGetTime.argtypes = [c_void_p]

library.playerGetWaterStored.restype = c_int
library.playerGetWaterStored.argtypes = [c_void_p]

library.playerGetSpawnResources.restype = c_int
library.playerGetSpawnResources.argtypes = [c_void_p]

library.pumpStationGetId.restype = c_int
library.pumpStationGetId.argtypes = [c_void_p]

library.pumpStationGetOwner.restype = c_int
library.pumpStationGetOwner.argtypes = [c_void_p]

library.pumpStationGetWaterAmount.restype = c_int
library.pumpStationGetWaterAmount.argtypes = [c_void_p]

library.pumpStationGetSiegeAmount.restype = c_int
library.pumpStationGetSiegeAmount.argtypes = [c_void_p]


#Properties
