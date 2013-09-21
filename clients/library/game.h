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
  
  int maxHealth;
  int trenchDamage;
  int waterDamage;
  int turnNumber;
  int attackDamage;
  int offenseCount;
  int defenseCount;
  int maxUnits;

  _PumpStation* SpeciesList;
  int PumpStationCount;
  _Mappable* Mappables;
  int MappableCount;
  _Player* Players;
  int PlayerCount;
  _Tile* Tiles;
  int TileCount;
  _Unit* Units;
  int UnitCount;
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
  ///Attempt to spawn a unit of a type on this tile.
  DLLEXPORT int tileSpawn(_Tile* object, int type);
  ///Make the unit move to the respective x and y location.
  DLLEXPORT int unitMove(_Unit* object, int x, int y);
  ///Attack another unit!.
  DLLEXPORT int unitAttack(_Unit* object, int unit);
  ///Put dirt in a hole!
  DLLEXPORT int unitFill(_Unit* object, int tile);
  ///Build something!
  DLLEXPORT int unitBuild(_Unit* object, int tile);

//derived properties



//accessors

DLLEXPORT int getMaxHealth(Connection* c);
DLLEXPORT int getTrenchDamage(Connection* c);
DLLEXPORT int getWaterDamage(Connection* c);
DLLEXPORT int getTurnNumber(Connection* c);
DLLEXPORT int getAttackDamage(Connection* c);
DLLEXPORT int getOffenseCount(Connection* c);
DLLEXPORT int getDefenseCount(Connection* c);
DLLEXPORT int getMaxUnits(Connection* c);

DLLEXPORT _PumpStation* getPumpStation(Connection* c, int num);
DLLEXPORT int getPumpStationCount(Connection* c);

DLLEXPORT _Mappable* getMappable(Connection* c, int num);
DLLEXPORT int getMappableCount(Connection* c);

DLLEXPORT _Player* getPlayer(Connection* c, int num);
DLLEXPORT int getPlayerCount(Connection* c);

DLLEXPORT _Tile* getTile(Connection* c, int num);
DLLEXPORT int getTileCount(Connection* c);

DLLEXPORT _Unit* getUnit(Connection* c, int num);
DLLEXPORT int getUnitCount(Connection* c);



  DLLEXPORT int networkLoop(Connection* c);
#ifdef __cplusplus
}
#endif

#endif
