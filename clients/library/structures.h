//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef STRUCTURES_H
#define STRUCTURES_H

struct Connection;
struct _Player;
struct _Mappable;
struct _PumpStation;
struct _Unit;
struct _Tile;
struct _UnitType;


struct _Player
{
  Connection* _c;
  int id;
  char* playerName;
  float time;
  int waterStored;
  int oxygen;
  int maxOxygen;
};
struct _Mappable
{
  Connection* _c;
  int id;
  int x;
  int y;
};
struct _PumpStation
{
  Connection* _c;
  int id;
  int owner;
  int siegeAmount;
};
struct _Unit
{
  Connection* _c;
  int id;
  int x;
  int y;
  int owner;
  int type;
  int hasAttacked;
  int hasDug;
  int hasFilled;
  int healthLeft;
  int maxHealth;
  int movementLeft;
  int maxMovement;
  int range;
  int offensePower;
  int defensePower;
  int digPower;
  int fillPower;
  int attackPower;
};
struct _Tile
{
  Connection* _c;
  int id;
  int x;
  int y;
  int owner;
  int pumpID;
  int waterAmount;
  int depth;
  int turnsUntilDeposit;
  int isSpawning;
};
struct _UnitType
{
  Connection* _c;
  int id;
  char* name;
  int type;
  int cost;
  int attackPower;
  int digPower;
  int fillPower;
  int maxHealth;
  int maxMovement;
  int offensePower;
  int defensePower;
  int range;
};

#endif
