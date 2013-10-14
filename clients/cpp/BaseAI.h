//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef BASEAI_H
#define BASEAI_H

#include <vector>
#include <ctime>
#include "game.h"

#include "Mappable.h"
#include "Tile.h"
#include "Unit.h"
#include "Player.h"
#include "PumpStation.h"

/// \brief A basic AI interface.

///This class implements most the code an AI would need to interface with the lower-level game code.
///AIs should extend this class to get a lot of boiler-plate code out of the way
///The provided AI class does just that.
class BaseAI
{
protected:
  Connection* c;
  std::vector<Mappable> mappables;
  std::vector<Tile> tiles;
  std::vector<Unit> units;
  std::vector<Player> players;
  std::vector<PumpStation> pumpStations;
public:
  ///The width of the total map.
  int mapWidth();
  ///The height of the total map.
  int mapHeight();
  ///The maximum amount of health a unit will have.
  int maxHealth();
  ///The amount of damage walking over a trench.
  int trenchDamage();
  ///The amount of damage walking over water.
  int waterDamage();
  ///The current turn number.
  int turnNumber();
  ///The amount of damage a unit will deal.
  int attackDamage();
  ///How quickly a unit will siege a PumpStation.
  int offensePower();
  ///The much a unit will slow a siege.
  int defensePower();
  ///The maximum siege value before the PumpStation is sieged.
  int maxSiege();
  ///The maximum number of units allowed per player.
  int maxUnits();
  ///The cost of spawning in a new unit
  int unitCost();
  ///The id of the current player.
  int playerID();
  ///What number game this is for the server
  int gameNumber();
  
  BaseAI(Connection* c);
  virtual ~BaseAI();
  ///
  ///Make this your username, which should be provided.
  virtual const char* username() = 0;
  ///
  ///Make this your password, which should be provided.
  virtual const char* password() = 0;
  ///
  ///This function is run once, before your first turn.
  virtual void init() = 0;
  ///
  ///This function is called each time it is your turn
  ///Return true to end your turn, return false to ask the server for updated information
  virtual bool run() = 0;
  ///
  ///This function is called after the last turn.
  virtual void end() = 0;


  bool startTurn();
};

#endif
