#ifndef AI_H
#define AI_H

#include "BaseAI.h"
#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>

///The class implementing gameplay logic.
class AI: public BaseAI
{
public:
  AI(Connection* c);
  virtual const char* username();
  virtual const char* password();
  virtual void init();
  virtual bool run();
  virtual void end();
  std::vector<Tile*> spawnTiles;
  Tile* getTile(const int x, const int y);
  
  void getSpawnTiles();
  void spawnUnits();
  void moveUnits();
};

#endif
