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

const int SPAWN = 0;
const int FILL = 1;
const int DIG = 2;
const int FLOW = 3;
const int MOVE = 4;
const int ATTACK = 5;
const int DEATH = 6;

struct Player
{
  int id;
  char* playerName;
  float time;
  int waterStored;
  int oxygen;
  int maxOxygen;

  friend std::ostream& operator<<(std::ostream& stream, Player obj);
};

struct Mappable
{
  int id;
  int x;
  int y;

  friend std::ostream& operator<<(std::ostream& stream, Mappable obj);
};

struct PumpStation
{
  int id;
  int owner;
  int waterAmount;
  int siegeAmount;

  friend std::ostream& operator<<(std::ostream& stream, PumpStation obj);
};

struct Unit: public Mappable 
{
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

  friend std::ostream& operator<<(std::ostream& stream, Unit obj);
};

struct Tile: public Mappable 
{
  int owner;
  int pumpID;
  int waterAmount;
  int depth;

  friend std::ostream& operator<<(std::ostream& stream, Tile obj);
};

struct UnitType
{
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

  friend std::ostream& operator<<(std::ostream& stream, UnitType obj);
};


struct Animation
{
  int type;
};

struct spawn : public Animation
{
  int sourceID;
  int unitID;

  friend std::ostream& operator<<(std::ostream& stream, spawn obj);
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

struct flow : public Animation
{
  int sourceID;
  int destID;
  int waterAmount;

  friend std::ostream& operator<<(std::ostream& stream, flow obj);
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

struct attack : public Animation
{
  int actingID;
  int targetID;

  friend std::ostream& operator<<(std::ostream& stream, attack obj);
};

struct death : public Animation
{
  int sourceID;

  friend std::ostream& operator<<(std::ostream& stream, death obj);
};


struct AnimOwner: public Animation
{
  int owner;
};

struct GameState
{
  std::map<int,Player> players;
  std::map<int,Mappable> mappables;
  std::map<int,PumpStation> pumpStations;
  std::map<int,Unit> units;
  std::map<int,Tile> tiles;
  std::map<int,UnitType> unitTypes;

  int mapWidth;
  int mapHeight;
  int trenchDamage;
  int waterDamage;
  int turnNumber;
  int maxUnits;
  int playerID;
  int gameNumber;
  int maxSiege;
  float oxygenRate;

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
