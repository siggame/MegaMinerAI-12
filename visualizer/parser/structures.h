//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef STRUCTURES_H
#define STRUCTURES_H

#include <iostream>
#include <vector>
#include <map>
#include <string>

#include "smartpointer.h"

namespace parser
{

const int FILL = 0;
const int DIG = 1;
const int SPAWN = 2;
const int MOVE = 3;
const int FLOW = 4;
const int ATTACK = 5;

struct Player
{
  int id;
  char* playerName;
  float time;
  int waterStored;
  int spawnResources;

  friend std::ostream& operator<<(std::ostream& stream, Player obj);
};

struct Mappable
{
  int id;
  int x;
  int y;

  friend std::ostream& operator<<(std::ostream& stream, Mappable obj);
};

struct Tile: public Mappable 
{
  int owner;
  int type;
  int pumpID;
  int waterAmount;
  int isTrench;

  friend std::ostream& operator<<(std::ostream& stream, Tile obj);
};

struct PumpStation
{
  int id;
  int owner;
  int waterAmount;
  int siegeCount;

  friend std::ostream& operator<<(std::ostream& stream, PumpStation obj);
};

struct Unit: public Mappable 
{
  int owner;
  int type;
  int hasAttacked;
  int hasDigged;
  int hasBuilt;
  int healthLeft;
  int maxHealth;
  int movementLeft;
  int maxMovement;

  friend std::ostream& operator<<(std::ostream& stream, Unit obj);
};


struct Animation
{
  int type;
};

struct fill : public Animation
{
  int actingID;
  int tileID;

  friend std::ostream& operator<<(std::ostream& stream, fill obj);
};

struct dig : public Animation
{
  int actingID;
  int tileID;

  friend std::ostream& operator<<(std::ostream& stream, dig obj);
};

struct spawn : public Animation
{
  int sourceID;
  int unitID;

  friend std::ostream& operator<<(std::ostream& stream, spawn obj);
};

struct move : public Animation
{
  int actingID;
  int fromX;
  int fromY;
  int toX;
  int toY;

  friend std::ostream& operator<<(std::ostream& stream, move obj);
};

struct flow : public Animation
{
  int sourceID;
  int destID;
  int waterAmount;

  friend std::ostream& operator<<(std::ostream& stream, flow obj);
};

struct attack : public Animation
{
  int actingID;
  int targetID;

  friend std::ostream& operator<<(std::ostream& stream, attack obj);
};


struct AnimOwner: public Animation
{
  int owner;
};

struct GameState
{
  std::map<int,Player> players;
  std::map<int,Mappable> mappables;
  std::map<int,Tile> tiles;
  std::map<int,PumpStation> pumpStations;
  std::map<int,Unit> units;

  int maxHealth;
  int trenchDamage;
  int waterDamage;
  int turnNumber;
  int attackDamage;
  int offenseCount;
  int defenseCount;
  int maxUnits;
  int unitCost;
  int playerID;

  std::map< int, std::vector< SmartPointer< Animation > > > animations;
  friend std::ostream& operator<<(std::ostream& stream, GameState obj);
};

struct Game
{
  std::vector<GameState> states;
  std::string players[2];
  int winner;
	std::string winReason;

  Game();
};

} // parser

#endif
