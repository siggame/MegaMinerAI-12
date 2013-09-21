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
library.playerTalk.restype = c_int
library.playerTalk.argtypes = [c_void_p, c_char_p]

library.tileSpawn.restype = c_int
library.tileSpawn.argtypes = [c_void_p, c_int]

library.unitMove.restype = c_int
library.unitMove.argtypes = [c_void_p, c_int, c_int]

library.unitAttack.restype = c_int
library.unitAttack.argtypes = [c_void_p, c_int]

library.unitFill.restype = c_int
library.unitFill.argtypes = [c_void_p, c_int]

library.unitBuild.restype = c_int
library.unitBuild.argtypes = [c_void_p, c_int]

# accessors

#Globals
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

library.getOffenseCount.restype = c_int
library.getOffenseCount.argtypes = [c_void_p]

library.getDefenseCount.restype = c_int
library.getDefenseCount.argtypes = [c_void_p]

library.getMaxUnits.restype = c_int
library.getMaxUnits.argtypes = [c_void_p]

library.getPumpStation.restype = c_void_p
library.getPumpStation.argtypes = [c_void_p, c_int]

library.getPumpStationCount.restype = c_int
library.getPumpStationCount.argtypes = [c_void_p]

library.getMappable.restype = c_void_p
library.getMappable.argtypes = [c_void_p, c_int]

library.getMappableCount.restype = c_int
library.getMappableCount.argtypes = [c_void_p]

library.getPlayer.restype = c_void_p
library.getPlayer.argtypes = [c_void_p, c_int]

library.getPlayerCount.restype = c_int
library.getPlayerCount.argtypes = [c_void_p]

library.getTile.restype = c_void_p
library.getTile.argtypes = [c_void_p, c_int]

library.getTileCount.restype = c_int
library.getTileCount.argtypes = [c_void_p]

library.getUnit.restype = c_void_p
library.getUnit.argtypes = [c_void_p, c_int]

library.getUnitCount.restype = c_int
library.getUnitCount.argtypes = [c_void_p]

# getters

#Data
library.pumpStationGetId.restype = c_int
library.pumpStationGetId.argtypes = [c_void_p]

library.pumpStationGetOwner.restype = c_int
library.pumpStationGetOwner.argtypes = [c_void_p]

library.pumpStationGetWaterAmount.restype = c_int
library.pumpStationGetWaterAmount.argtypes = [c_void_p]

library.pumpStationGetSeigeCount.restype = c_int
library.pumpStationGetSeigeCount.argtypes = [c_void_p]

library.mappableGetId.restype = c_int
library.mappableGetId.argtypes = [c_void_p]

library.mappableGetX.restype = c_int
library.mappableGetX.argtypes = [c_void_p]

library.mappableGetY.restype = c_int
library.mappableGetY.argtypes = [c_void_p]

library.playerGetId.restype = c_int
library.playerGetId.argtypes = [c_void_p]

library.playerGetPlayerName.restype = c_char_p
library.playerGetPlayerName.argtypes = [c_void_p]

library.playerGetTime.restype = c_float
library.playerGetTime.argtypes = [c_void_p]

library.playerGetWaterStored.restype = c_int
library.playerGetWaterStored.argtypes = [c_void_p]

library.playerGetSpawnRate.restype = c_int
library.playerGetSpawnRate.argtypes = [c_void_p]

library.tileGetId.restype = c_int
library.tileGetId.argtypes = [c_void_p]

library.tileGetX.restype = c_int
library.tileGetX.argtypes = [c_void_p]

library.tileGetY.restype = c_int
library.tileGetY.argtypes = [c_void_p]

library.tileGetOwner.restype = c_int
library.tileGetOwner.argtypes = [c_void_p]

library.tileGetType.restype = c_int
library.tileGetType.argtypes = [c_void_p]

library.tileGetResId.restype = c_int
library.tileGetResId.argtypes = [c_void_p]

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

library.unitGetCurHealth.restype = c_int
library.unitGetCurHealth.argtypes = [c_void_p]

library.unitGetCurMovement.restype = c_int
library.unitGetCurMovement.argtypes = [c_void_p]

library.unitGetMaxMovement.restype = c_int
library.unitGetMaxMovement.argtypes = [c_void_p]


#Properties
