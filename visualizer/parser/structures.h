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
const int MOVE = 1;
const int FILL = 2;
const int DEATH = 3;
const int DIG = 4;
const int FLOW = 5;
const int ATTACK = 6;

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

struct fill : public Animation
{
  int actingID;
  int tileID;

  friend std::ostream& operator<<(std::ostream& stream, fill obj);
};

struct death : public Animation
{
  int sourceID;

  friend std::ostream& operator<<(std::ostream& stream, death obj);
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
  std::map<int,PumpStation> pumpStations;
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
  int maxUnits;
  int unitCost;
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
