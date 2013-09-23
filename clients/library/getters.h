#ifndef GETTERS_H 
#define GETTERS_H
#include "structures.h"

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)
#else
#define DLLEXPORT
#endif

#ifdef __cplusplus
extern "C" {
#endif

DLLEXPORT int mappableGetId(_Mappable* ptr);
DLLEXPORT int mappableGetX(_Mappable* ptr);
DLLEXPORT int mappableGetY(_Mappable* ptr);


DLLEXPORT int unitGetId(_Unit* ptr);
DLLEXPORT int unitGetX(_Unit* ptr);
DLLEXPORT int unitGetY(_Unit* ptr);
DLLEXPORT int unitGetOwner(_Unit* ptr);
DLLEXPORT int unitGetType(_Unit* ptr);
DLLEXPORT int unitGetCurHealth(_Unit* ptr);
DLLEXPORT int unitGetMaxHealth(_Unit* ptr);
DLLEXPORT int unitGetCurMovement(_Unit* ptr);
DLLEXPORT int unitGetMaxMovement(_Unit* ptr);


DLLEXPORT int playerGetId(_Player* ptr);
DLLEXPORT char* playerGetPlayerName(_Player* ptr);
DLLEXPORT float playerGetTime(_Player* ptr);
DLLEXPORT int playerGetWaterStored(_Player* ptr);
DLLEXPORT int playerGetSpawnResources(_Player* ptr);


DLLEXPORT int tileGetId(_Tile* ptr);
DLLEXPORT int tileGetX(_Tile* ptr);
DLLEXPORT int tileGetY(_Tile* ptr);
DLLEXPORT int tileGetOwner(_Tile* ptr);
DLLEXPORT int tileGetType(_Tile* ptr);
DLLEXPORT int tileGetPumpID(_Tile* ptr);
DLLEXPORT int tileGetWaterAmount(_Tile* ptr);
DLLEXPORT int tileGetIsTrench(_Tile* ptr);


DLLEXPORT int pumpStationGetId(_PumpStation* ptr);
DLLEXPORT int pumpStationGetOwner(_PumpStation* ptr);
DLLEXPORT int pumpStationGetWaterAmount(_PumpStation* ptr);
DLLEXPORT int pumpStationGetSiegeCount(_PumpStation* ptr);



#ifdef __cplusplus
}
#endif

#endif
