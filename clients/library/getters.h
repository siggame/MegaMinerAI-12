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

DLLEXPORT int playerGetId(_Player* ptr);
DLLEXPORT char* playerGetPlayerName(_Player* ptr);
DLLEXPORT float playerGetTime(_Player* ptr);
DLLEXPORT int playerGetWaterStored(_Player* ptr);
DLLEXPORT int playerGetOxygen(_Player* ptr);
DLLEXPORT int playerGetMaxOxygen(_Player* ptr);


DLLEXPORT int mappableGetId(_Mappable* ptr);
DLLEXPORT int mappableGetX(_Mappable* ptr);
DLLEXPORT int mappableGetY(_Mappable* ptr);


DLLEXPORT int pumpStationGetId(_PumpStation* ptr);
DLLEXPORT int pumpStationGetOwner(_PumpStation* ptr);
DLLEXPORT int pumpStationGetSiegeAmount(_PumpStation* ptr);


DLLEXPORT int unitGetId(_Unit* ptr);
DLLEXPORT int unitGetX(_Unit* ptr);
DLLEXPORT int unitGetY(_Unit* ptr);
DLLEXPORT int unitGetOwner(_Unit* ptr);
DLLEXPORT int unitGetType(_Unit* ptr);
DLLEXPORT int unitGetHasAttacked(_Unit* ptr);
DLLEXPORT int unitGetHasDug(_Unit* ptr);
DLLEXPORT int unitGetHasFilled(_Unit* ptr);
DLLEXPORT int unitGetHealthLeft(_Unit* ptr);
DLLEXPORT int unitGetMaxHealth(_Unit* ptr);
DLLEXPORT int unitGetMovementLeft(_Unit* ptr);
DLLEXPORT int unitGetMaxMovement(_Unit* ptr);
DLLEXPORT int unitGetRange(_Unit* ptr);
DLLEXPORT int unitGetOffensePower(_Unit* ptr);
DLLEXPORT int unitGetDefensePower(_Unit* ptr);
DLLEXPORT int unitGetDigPower(_Unit* ptr);
DLLEXPORT int unitGetFillPower(_Unit* ptr);
DLLEXPORT int unitGetAttackPower(_Unit* ptr);


DLLEXPORT int tileGetId(_Tile* ptr);
DLLEXPORT int tileGetX(_Tile* ptr);
DLLEXPORT int tileGetY(_Tile* ptr);
DLLEXPORT int tileGetOwner(_Tile* ptr);
DLLEXPORT int tileGetPumpID(_Tile* ptr);
DLLEXPORT int tileGetWaterAmount(_Tile* ptr);
DLLEXPORT int tileGetDepth(_Tile* ptr);
DLLEXPORT int tileGetTurnsUntilDeposit(_Tile* ptr);
DLLEXPORT int tileGetIsSpawning(_Tile* ptr);


DLLEXPORT int unitTypeGetId(_UnitType* ptr);
DLLEXPORT char* unitTypeGetName(_UnitType* ptr);
DLLEXPORT int unitTypeGetType(_UnitType* ptr);
DLLEXPORT int unitTypeGetCost(_UnitType* ptr);
DLLEXPORT int unitTypeGetAttackPower(_UnitType* ptr);
DLLEXPORT int unitTypeGetDigPower(_UnitType* ptr);
DLLEXPORT int unitTypeGetFillPower(_UnitType* ptr);
DLLEXPORT int unitTypeGetMaxHealth(_UnitType* ptr);
DLLEXPORT int unitTypeGetMaxMovement(_UnitType* ptr);
DLLEXPORT int unitTypeGetOffensePower(_UnitType* ptr);
DLLEXPORT int unitTypeGetDefensePower(_UnitType* ptr);
DLLEXPORT int unitTypeGetRange(_UnitType* ptr);



#ifdef __cplusplus
}
#endif

#endif
