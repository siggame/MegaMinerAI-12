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

const int MOVE = 0;

struct PumpStation
{
  int id;
  int owner;
  int waterAmount;
  int seigeCount;

  friend std::ostream& operator<<(std::ostream& stream, PumpStation obj);
};

struct Mappable
{
  int id;
  int x;
  int y;

  friend std::ostream& operator<<(std::ostream& stream, Mappable obj);
};

struct Player
{
  int id;
  char* playerName;
  float time;
  int waterStored;
  int spawnRate;

  friend std::ostream& operator<<(std::ostream& stream, Player obj);
};

struct Tile: public Mappable 
{
  int owner;
  int type;
  int resId;
  int waterAmount;
  int isTrench;

  friend std::ostream& operator<<(std::ostream& stream, Tile obj);
};

struct Unit: public Mappable 
{
  int owner;
  int type;
  int curHealth;
  int curMovement;
  int maxMovement;

  friend std::ostream& operator<<(std::ostream& stream, Unit obj);
};


struct Animation
{
  int type;
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


struct AnimOwner: public Animation
{
  int owner;
};

struct GameState
{
  std::map<int,PumpStation> speciesList;
  std::map<int,Mappable> mappables;
  std::map<int,Player> players;
  std::map<int,Tile> tiles;
  std::map<int,Unit> units;

  int maxHealth;
  int trenchDamage;
  int waterDamage;
  int turnNumber;
  int attackDamage;
  int offenseCount;
  int defenseCount;
  int maxUnits;

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
