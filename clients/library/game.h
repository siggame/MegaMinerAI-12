//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef GAME_H
#define GAME_H

#include "network.h"
#include "structures.h"

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)

#ifdef ENABLE_THREADS
#include "pthread.h"
#endif

#else
#define DLLEXPORT

#ifdef ENABLE_THREADS
#include <pthread.h>
#endif

#endif

struct Connection
{
  int socket;
  
  #ifdef ENABLE_THREADS
  pthread_mutex_t mutex;
  #endif
  
  int mapWidth;
  int mapHeight;
  int waterDamage;
  int turnNumber;
  int maxUnits;
  int playerID;
  int gameNumber;
  int maxSiege;
  float oxygenRate;
  int depositionRate;

  _Player* Players;
  int PlayerCount;
  _Mappable* Mappables;
  int MappableCount;
  _PumpStation* PumpStations;
  int PumpStationCount;
  _Unit* Units;
  int UnitCount;
  _Tile* Tiles;
  int TileCount;
  _UnitType* UnitTypes;
  int UnitTypeCount;
};

#ifdef __cplusplus
extern "C"
{
#endif
  DLLEXPORT Connection* createConnection();
  DLLEXPORT void destroyConnection(Connection* c);
  DLLEXPORT int serverConnect(Connection* c, const char* host, const char* port);

  DLLEXPORT int serverLogin(Connection* c, const char* username, const char* password);
  DLLEXPORT int createGame(Connection* c);
  DLLEXPORT int joinGame(Connection* c, int id, const char* playerType);

  DLLEXPORT void endTurn(Connection* c);
  DLLEXPORT void getStatus(Connection* c);


//commands

  ///Allows a player to display messages on the screen
  DLLEXPORT int playerTalk(_Player* object, char* message);
  ///Make the unit move to the respective x and y location.
  DLLEXPORT int unitMove(_Unit* object, int x, int y);
  ///Put dirt in a hole!
  DLLEXPORT int unitFill(_Unit* object, _Tile* tile);
  ///Dig out a tile
  DLLEXPORT int unitDig(_Unit* object, _Tile* tile);
  ///Command to attack another Unit.
  DLLEXPORT int unitAttack(_Unit* object, _Unit* target);
  ///Attempt to spawn a unit of a type on this tile.
  DLLEXPORT int tileSpawn(_Tile* object, int type);

//derived properties



//accessors

DLLEXPORT int getMapWidth(Connection* c);
DLLEXPORT int getMapHeight(Connection* c);
DLLEXPORT int getWaterDamage(Connection* c);
DLLEXPORT int getTurnNumber(Connection* c);
DLLEXPORT int getMaxUnits(Connection* c);
DLLEXPORT int getPlayerID(Connection* c);
DLLEXPORT int getGameNumber(Connection* c);
DLLEXPORT int getMaxSiege(Connection* c);
DLLEXPORT float getOxygenRate(Connection* c);
DLLEXPORT int getDepositionRate(Connection* c);

DLLEXPORT _Player* getPlayer(Connection* c, int num);
DLLEXPORT int getPlayerCount(Connection* c);

DLLEXPORT _Mappable* getMappable(Connection* c, int num);
DLLEXPORT int getMappableCount(Connection* c);

DLLEXPORT _PumpStation* getPumpStation(Connection* c, int num);
DLLEXPORT int getPumpStationCount(Connection* c);

DLLEXPORT _Unit* getUnit(Connection* c, int num);
DLLEXPORT int getUnitCount(Connection* c);

DLLEXPORT _Tile* getTile(Connection* c, int num);
DLLEXPORT int getTileCount(Connection* c);

DLLEXPORT _UnitType* getUnitType(Connection* c, int num);
DLLEXPORT int getUnitTypeCount(Connection* c);



  DLLEXPORT int networkLoop(Connection* c);
#ifdef __cplusplus
}
#endif

#endif
