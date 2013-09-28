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
DLLEXPORT int playerGetSpawnResources(_Player* ptr)
{
  return ptr->spawnResources;
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
DLLEXPORT int tileGetType(_Tile* ptr)
{
  return ptr->type;
}
DLLEXPORT int tileGetPumpID(_Tile* ptr)
{
  return ptr->pumpID;
}
DLLEXPORT int tileGetWaterAmount(_Tile* ptr)
{
  return ptr->waterAmount;
}
DLLEXPORT int tileGetIsTrench(_Tile* ptr)
{
  return ptr->isTrench;
}
DLLEXPORT int pumpStationGetId(_PumpStation* ptr)
{
  return ptr->id;
}
DLLEXPORT int pumpStationGetOwner(_PumpStation* ptr)
{
  return ptr->owner;
}
DLLEXPORT int pumpStationGetWaterAmount(_PumpStation* ptr)
{
  return ptr->waterAmount;
}
DLLEXPORT int pumpStationGetSiegeCount(_PumpStation* ptr)
{
  return ptr->siegeCount;
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
DLLEXPORT int unitGetHasDigged(_Unit* ptr)
{
  return ptr->hasDigged;
}
DLLEXPORT int unitGetHasBuilt(_Unit* ptr)
{
  return ptr->hasBuilt;
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

