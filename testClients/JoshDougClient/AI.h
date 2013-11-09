#ifndef AI_H
#define AI_H

#include "BaseAI.h"
#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>
#include <cmath>
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
  std::vector<Tile*> pumpTiles;
  std::vector<Tile*> iceTiles;
  std::vector<Unit*> enemyUnits;
  std::vector<Unit*> friendTankUnits;
  std::vector<Unit*> friendSpyUnits;
  std::vector<Unit*> friendWorkerUnits;
  Tile* getTile(const int x, const int y);
  void getSpawnTiles();
  void getPumpTiles();
  void getIceTiles();
  void getUnits(); 
  Tile* getNearestFriendlyPump(const int xCoord, const int yCoord);
  Tile* getNearestEnemyPump(const int xCoord, const int yCoord);
  Tile* getNearestIce(const int xCoord, const int yCoord);
  bool waterNear(const int xCoord, const int yCoord);
  bool isTankAt(const int x, const int y);
  void spawnUnits();
  void moveTo(Unit & unit, int x, int y);
  void digTo(Unit & unit, int x, int y);
  void controlUnits();
  void tryToAttack(Unit & unit);
  bool validMove(const int x, const int y);
};

#endif
