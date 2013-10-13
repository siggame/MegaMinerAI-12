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

const int DIG = 0;
const int DEATH = 1;
const int FLOW = 2;
const int SPAWN = 3;
const int MOVE = 4;
const int ATTACK = 5;
const int FILL = 6;

struct Player
{
  int id;
  char* playerName;
  float time;
  int waterStored;
  int spawnResources;

  friend std::ostream& operator<<(std::ostream& stream, Player obj);
};

struct PumpStation
{
  int id;
  int owner;
  int waterAmount;
  int siegeAmount;

  friend std::ostream& operator<<(std::ostream& stream, PumpStation obj);
};

struct Mappable
{
  int id;
  int x;
  int y;

  friend std::ostream& operator<<(std::ostream& stream, Mappable obj);
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

  friend std::ostream& operator<<(std::ostream& stream, Unit obj);
};

struct Tile: public Mappable 
{
  int owner;
  int pumpID;
  int waterAmount;
  int isTrench;

  friend std::ostream& operator<<(std::ostream& stream, Tile obj);
};


struct Animation
{
  int type;
};

struct dig : public Animation
{
  int actingID;
  int tileID;

  friend std::ostream& operator<<(std::ostream& stream, dig obj);
};

struct death : public Animation
{
  int sourceID;
  int unitID;

  friend std::ostream& operator<<(std::ostream& stream, death obj);
};

struct flow : public Animation
{
  int sourceID;
  int destID;
  int waterAmount;

  friend std::ostream& operator<<(std::ostream& stream, flow obj);
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

struct attack : public Animation
{
  int actingID;
  int targetID;

  friend std::ostream& operator<<(std::ostream& stream, attack obj);
};

struct fill : public Animation
{
  int actingID;
  int tileID;

  friend std::ostream& operator<<(std::ostream& stream, fill obj);
};


struct AnimOwner: public Animation
{
  int owner;
};

struct GameState
{
  std::map<int,Player> players;
  std::map<int,PumpStation> pumpStations;
  std::map<int,Mappable> mappables;
  std::map<int,Unit> units;
  std::map<int,Tile> tiles;

  int mapWidth;
  int mapHeight;
  int maxHealth;
  int trenchDamage;
  int waterDamage;
  int turnNumber;
  int attackDamage;
  int offensePower;
  int defensePower;
  int maxSiege;
  int maxUnits;
  int unitCost;
  int playerID;
  int gameNumber;

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
