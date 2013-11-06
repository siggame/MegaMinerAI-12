#include "AI.h"
#include "util.h"
#include <iostream>
using namespace std;

AI::AI(Connection* conn) : BaseAI(conn) {}

const char* AI::username()
{
  return "Herman";
}

const char* AI::password()
{
  return "password";
}

//This function is run once, before your first turn.
void AI::init()
{
  srand(time(NULL));
  getSpawnTiles();
  getPumpTiles();
  getIceTiles();
}

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
  spawnUnits();
  moveUnits();  
  return true;
}

//This function is run once, after your last turn.
void AI::end(){}

Tile* AI::getTile(const int x, const int y)
{
    if(0 <= x && x < mapWidth() && 0 <= y && y < mapHeight())
        return &tiles[x * mapHeight() + y];
    else
        return NULL;
}

void AI::getSpawnTiles()
{
    spawnTiles.clear();
    for(int i = 0; i < tiles.size(); i++)
    {
      if(tiles[i].owner() == playerID())
      {
        spawnTiles.push_back(& tiles[i]);
      }
    }
    return;
}

void AI::getPumpTiles()
{
  pumpTiles.clear();
  for(int i = 0; i < tiles.size(); i++)
  {
    if(tiles[i].pumpID() != -1)
    {
      pumpTiles.push_back(& tiles[i]);
    }
  }
}

void AI::getIceTiles()
{
  iceTiles.clear();
  for(int i = 0; i < tiles.size(); i++)
  {
    if(tiles[i].pumpID() == -1 && tiles[i].depth() == 0
       && tiles[i].waterAmount() > 0)
    {
      iceTiles.push_back(& tiles[i]);
    }
  }
}

Tile* AI::getNearestFriendlyPump(const int xCoord, const int yCoord)
{
  int minDist=1000;
  int xMin, yMin;
  int distance;
  bool noFriendly=true;
  for(int i = 0; i < pumpTiles.size(); i++)
  {
    if(pumpTiles[i]->owner() == playerID())
    {
      distance = abs(pumpTiles[i]->x()-xCoord) + abs(pumpTiles[i]->y()-yCoord);
      if(distance<minDist)
      {
        minDist=distance;
        xMin=pumpTiles[i]->x();
        yMin=pumpTiles[i]->y();
      }
      noFriendly=false;
    }
  }
  if(noFriendly)
    return NULL;
  else
    return getTile(xMin, yMin);
}

Tile* AI::getNearestIce(const int xCoord, const int yCoord)
{
  int minDist=1000;
  int xMin, yMin;
  int distance;
  bool noIce=true;
  for(int i = 0; i < iceTiles.size(); i++)
  {
    if(iceTiles[i] != NULL && iceTiles[i]->waterAmount() > 0
       && !(waterNear(iceTiles[i]->x(),iceTiles[i]->y())))
    {
      distance = abs(iceTiles[i]->x()-xCoord) + abs(iceTiles[i]->y()-yCoord);
      if(distance<minDist)
      {
        minDist=distance;
        xMin=iceTiles[i]->x();
        yMin=iceTiles[i]->y();
      }
      noIce=false;
    }
  }
  if(noIce)
    return NULL;
  else
    return getTile(xMin, yMin);
}

bool AI::waterNear(const int xCoord, const int yCoord)
{
  Tile* checkTile;
  checkTile=getTile(xCoord+1, yCoord);
  if(checkTile != NULL && (checkTile->waterAmount() > 0) && checkTile->depth()>0)
    return true;
  checkTile=getTile(xCoord-1, yCoord);
  if(checkTile != NULL && (checkTile->waterAmount() > 0) && checkTile->depth()>0)
    return true;
  checkTile=getTile(xCoord, yCoord+1);
  if(checkTile != NULL && (checkTile->waterAmount() > 0) && checkTile->depth()>0)
    return true;
  checkTile=getTile(xCoord, yCoord-1);
  if(checkTile != NULL && (checkTile->waterAmount() > 0) && checkTile->depth()>0)
    return true;
  
  return false;
}

void AI::spawnUnits()
{
  for(int i = 0; i < spawnTiles.size(); i++)
  {
    if(spawnTiles[i]->pumpID() > 0)
      spawnTiles[i]->spawn(0);
    else
      spawnTiles[i]->spawn(rand()%2+1);
  }
  return;
}

void AI::moveTo(Unit & unit, int x, int y)
{
  for(int i=0; i<unit.maxMovement(); i++)
  {
    if(unit.x()<x)
      unit.move(unit.x()+1,unit.y());
    else if(unit.x()>x)
      unit.move(unit.x()-1,unit.y());
    else if(unit.y()<y)
      unit.move(unit.x(),unit.y()+1);
    else if(unit.y()>y)
      unit.move(unit.x(),unit.y()-1);
  }
}

void AI::digTo(Unit & unit, int x, int y)
{
  int oldX, oldY;
  for(int i=0; i<unit.maxMovement(); i++)
  {
    oldX=unit.x();
    oldY=unit.y();
    if(unit.x()<x)
      unit.move(unit.x()+1,unit.y());
    else if(unit.x()>x)
      unit.move(unit.x()-1,unit.y());
    else if(unit.y()<y)
      unit.move(unit.x(),unit.y()+1);
    else if(unit.y()>y)
      unit.move(unit.x(),unit.y()-1);
    
    Tile* tile = getTile(oldX, oldY);
    if(tile != NULL)
      unit.dig(*tile);
    
  }
}

void AI::moveUnits()
{
  Tile* moveTile=NULL;
  for (int i = 0; i < units.size(); i++)
  {
    if(units[i].owner() == playerID())
    {
      if(units[i].type()==0)  //worker
      {
        moveTile = getNearestIce(units[i].x(), units[i].y());
        if(moveTile != NULL)
        {
          digTo(units[i], moveTile->x(), moveTile->y());
        }
      }
    }
  }
  return;
}
//Random movement
/*
void AI::moveUnits()
{
  int xDir[] = {0,0,-1,1};  //up,down,left,right
  int yDir[] = {-1,1,0,0};
  int newX, newY;
  int randomDir;
  for (int i = 0; i < units.size(); i++)
  {
    if (units[i].owner() == playerID() )
    {
      randomD8ir=rand()%4;
      int newX=units[i].x()+xDir[randomDir];
      int newY=units[i].y()+ yDir[randomDir];
      Tile* moveTile = getTile(newX, newY);
      if(moveTile != NULL && (moveTile->waterAmount()==0))
        units[i].move(newX, newY);
      randomDir = rand()%4;
      int digfillx = units[i].x()+xDir[randomDir];
      int digfilly = units[i].y()+yDir[randomDir];
      Tile* tile = getTile(digfillx, digfilly);

      if(tile != NULL)
      {
        units[i].dig(*tile);
        units[i].fill(*tile);
      }
    }
  }
}
*/
