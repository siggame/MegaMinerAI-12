//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef STRUCTURES_H
#define STRUCTURES_H

struct Connection;
struct _PumpStation;
struct _Mappable;
struct _Player;
struct _Tile;
struct _Unit;


struct _PumpStation
{
  Connection* _c;
  int id;
  int owner;
  int waterAmount;
  int seigeCount;
};
struct _Mappable
{
  Connection* _c;
  int id;
  int x;
  int y;
};
struct _Player
{
  Connection* _c;
  int id;
  char* playerName;
  float time;
  int waterStored;
  int spawnRate;
};
struct _Tile
{
  Connection* _c;
  int id;
  int x;
  int y;
  int owner;
  int type;
  int resId;
  int waterAmount;
  int isTrench;
};
struct _Unit
{
  Connection* _c;
  int id;
  int x;
  int y;
  int owner;
  int type;
  int curHealth;
  int curMovement;
  int maxMovement;
};

#endif
