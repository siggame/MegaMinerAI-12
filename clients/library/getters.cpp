#include "getters.h"

DLLEXPORT int playerGetId(_Player* ptr)
{
  return ptr->id;
}
DLLEXPORT char* playerGetPlayerName(_Player* ptr)
{
  return ptr->playerName;
}
DLLEXPORT float playerGetTime(_Player* ptr)
{
  return ptr->time;
}
DLLEXPORT int playerGetWaterStored(_Player* ptr)
{
  return ptr->waterStored;
}
DLLEXPORT int playerGetOxygen(_Player* ptr)
{
  return ptr->oxygen;
}
DLLEXPORT int playerGetMaxOxygen(_Player* ptr)
{
  return ptr->maxOxygen;
}
DLLEXPORT int mappableGetId(_Mappable* ptr)
{
  return ptr->id;
}
DLLEXPORT int mappableGetX(_Mappable* ptr)
{
  return ptr->x;
}
DLLEXPORT int mappableGetY(_Mappable* ptr)
{
  return ptr->y;
}
DLLEXPORT int pumpStationGetId(_PumpStation* ptr)
{
  return ptr->id;
}
DLLEXPORT int pumpStationGetOwner(_PumpStation* ptr)
{
  return ptr->owner;
}
DLLEXPORT int pumpStationGetSiegeAmount(_PumpStation* ptr)
{
  return ptr->siegeAmount;
}
DLLEXPORT int unitGetId(_Unit* ptr)
{
  return ptr->id;
}
DLLEXPORT int unitGetX(_Unit* ptr)
{
  return ptr->x;
}
DLLEXPORT int unitGetY(_Unit* ptr)
{
  return ptr->y;
}
DLLEXPORT int unitGetOwner(_Unit* ptr)
{
  return ptr->owner;
}
DLLEXPORT int unitGetType(_Unit* ptr)
{
  return ptr->type;
}
DLLEXPORT int unitGetHasAttacked(_Unit* ptr)
{
  return ptr->hasAttacked;
}
DLLEXPORT int unitGetHasDug(_Unit* ptr)
{
  return ptr->hasDug;
}
DLLEXPORT int unitGetHasFilled(_Unit* ptr)
{
  return ptr->hasFilled;
}
DLLEXPORT int unitGetHealthLeft(_Unit* ptr)
{
  return ptr->healthLeft;
}
DLLEXPORT int unitGetMaxHealth(_Unit* ptr)
{
  return ptr->maxHealth;
}
DLLEXPORT int unitGetMovementLeft(_Unit* ptr)
{
  return ptr->movementLeft;
}
DLLEXPORT int unitGetMaxMovement(_Unit* ptr)
{
  return ptr->maxMovement;
}
DLLEXPORT int unitGetRange(_Unit* ptr)
{
  return ptr->range;
}
DLLEXPORT int unitGetOffensePower(_Unit* ptr)
{
  return ptr->offensePower;
}
DLLEXPORT int unitGetDefensePower(_Unit* ptr)
{
  return ptr->defensePower;
}
DLLEXPORT int unitGetDigPower(_Unit* ptr)
{
  return ptr->digPower;
}
DLLEXPORT int unitGetFillPower(_Unit* ptr)
{
  return ptr->fillPower;
}
DLLEXPORT int unitGetAttackPower(_Unit* ptr)
{
  return ptr->attackPower;
}
DLLEXPORT int tileGetId(_Tile* ptr)
{
  return ptr->id;
}
DLLEXPORT int tileGetX(_Tile* ptr)
{
  return ptr->x;
}
DLLEXPORT int tileGetY(_Tile* ptr)
{
  return ptr->y;
}
DLLEXPORT int tileGetOwner(_Tile* ptr)
{
  return ptr->owner;
}
DLLEXPORT int tileGetPumpID(_Tile* ptr)
{
  return ptr->pumpID;
}
DLLEXPORT int tileGetWaterAmount(_Tile* ptr)
{
  return ptr->waterAmount;
}
DLLEXPORT int tileGetDepth(_Tile* ptr)
{
  return ptr->depth;
}
DLLEXPORT int tileGetTurnsUntilDeposit(_Tile* ptr)
{
  return ptr->turnsUntilDeposit;
}
DLLEXPORT int tileGetIsSpawning(_Tile* ptr)
{
  return ptr->isSpawning;
}
DLLEXPORT int unitTypeGetId(_UnitType* ptr)
{
  return ptr->id;
}
DLLEXPORT char* unitTypeGetName(_UnitType* ptr)
{
  return ptr->name;
}
DLLEXPORT int unitTypeGetType(_UnitType* ptr)
{
  return ptr->type;
}
DLLEXPORT int unitTypeGetCost(_UnitType* ptr)
{
  return ptr->cost;
}
DLLEXPORT int unitTypeGetAttackPower(_UnitType* ptr)
{
  return ptr->attackPower;
}
DLLEXPORT int unitTypeGetDigPower(_UnitType* ptr)
{
  return ptr->digPower;
}
DLLEXPORT int unitTypeGetFillPower(_UnitType* ptr)
{
  return ptr->fillPower;
}
DLLEXPORT int unitTypeGetMaxHealth(_UnitType* ptr)
{
  return ptr->maxHealth;
}
DLLEXPORT int unitTypeGetMaxMovement(_UnitType* ptr)
{
  return ptr->maxMovement;
}
DLLEXPORT int unitTypeGetOffensePower(_UnitType* ptr)
{
  return ptr->offensePower;
}
DLLEXPORT int unitTypeGetDefensePower(_UnitType* ptr)
{
  return ptr->defensePower;
}
DLLEXPORT int unitTypeGetRange(_UnitType* ptr)
{
  return ptr->range;
}

