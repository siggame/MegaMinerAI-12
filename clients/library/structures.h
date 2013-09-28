//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef STRUCTURES_H
#define STRUCTURES_H

struct Connection;
struct _Player;
struct _Mappable;
struct _Tile;
struct _PumpStation;
struct _Unit;


struct _Player
{
  Connection* _c;
  int id;
  char* playerName;
  float time;
  int waterStored;
  int spawnResources;
};
struct _Mappable
{
  Connection* _c;
  int id;
  int x;
  int y;
};
struct _Tile
{
  Connection* _c;
  int id;
  int x;
  int y;
  int owner;
  int type;
  int pumpID;
  int waterAmount;
  int isTrench;
};
struct _PumpStation
{
  Connection* _c;
  int id;
  int owner;
  int waterAmount;
  int siegeCount;
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
  int hasDigged;
  int hasBuilt;
  int healthLeft;
  int maxHealth;
  int movementLeft;
  int maxMovement;
};

#endif
