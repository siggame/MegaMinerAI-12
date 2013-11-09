#include "AI.h"
#include "util.h"
#include <iostream>
#include "string"
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
  getUnits();
  spawnUnits();
  getUnits();
  controlUnits();  
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

void AI::getUnits()
{
  enemyUnits.clear();
  friendTankUnits.clear();
  friendSpyUnits.clear();
  friendWorkerUnits.clear();
  for (int i = 0; i < units.size(); i++)
  {
    if (units[i].owner() != playerID())
    {
      enemyUnits.push_back(& units[i]);
    }
    else if (units[i].owner() == playerID())
    {
      if(units[i].type()==0)
        friendWorkerUnits.push_back(& units[i]);
      else if(units[i].type()==1)
        friendSpyUnits.push_back(& units[i]);
      else if(units[i].type()==2)
        friendTankUnits.push_back(& units[i]);
    }
  }
}



Tile* AI::getNearestFriendlyPump(const int xCoord, const int yCoord)
{
  int minDist=10000;
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
    for(int j =0; j< pumpStations.size(); j++)
    {
      if(pumpStations[j].id()==pumpTiles[i]->pumpID()
         && pumpTiles[i]->owner() == playerID() && pumpStations[j].siegeAmount()>0)
        return pumpTiles[i];
    }
    
  }
  if(noFriendly)
    return NULL;
  else
    return getTile(xMin, yMin);
}

Tile* AI::getNearestEnemyPump(const int xCoord, const int yCoord)
{
  int minDist=10000;
  int xMin, yMin;
  int distance;
  bool noEnemy=true;
  for(int i = 0; i < pumpTiles.size(); i++)
  {
    if(pumpTiles[i]->owner() != playerID())
    {
      distance = abs(pumpTiles[i]->x()-xCoord) + abs(pumpTiles[i]->y()-yCoord);
      if(distance<minDist)
      {
        minDist=distance;
        xMin=pumpTiles[i]->x();
        yMin=pumpTiles[i]->y();
      }
      noEnemy=false;
    }
    for(int j =0; j< pumpStations.size(); j++)
    {
      if(pumpStations[j].id()==pumpTiles[i]->pumpID()
         && pumpTiles[i]->owner() == playerID() && pumpStations[j].siegeAmount()>0)
        return pumpTiles[i];
    }
    
  }
  if(noEnemy)
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

bool AI::isTankAt(const int x, const int y)
{
  for(int i=0; i < friendTankUnits.size(); i++)
  {
    if(friendTankUnits[i]->x()==x && friendTankUnits[i]->y()==y)
      return true;
  }
  return false;
}

void AI::spawnUnits()
{
  getSpawnTiles();
  int temp;
  bool spawnedTank=false;
  if(friendTankUnits.size()==0 && !spawnedTank)
  {
    pumpTiles[rand()%pumpTiles.size()]->spawn(2);
    spawnedTank=true;
  }
  for(int i = spawnTiles.size()-1; i >=0; i--)
  {
    if(spawnTiles[i]->pumpID() > 0)
    {
      spawnTiles[i]->spawn(rand()%2);
    }
    else
      spawnTiles[i]->spawn(1);
  }
  return;
  
  /*
  getSpawnTiles();
  bool lookedAt=false;
  int temp, tempX, tempY, tempPumpId;
  std::vector<int> pumpsLookedAt;
  Tile* tile;
  //spawn tanks
  for(int i=0; i< pumpTiles.size(); i++)
  {
    tempPumpId = pumpTiles[i]->pumpID();
    for(int j=0; j<pumpsLookedAt.size(); j++)
    {
      if(tempPumpId == pumpsLookedAt[j])
        lookedAt=true;
      
    }
    
      if(!lookedAt)
      {
        
        tempX=pumpTiles[i]->x();
        tempY=pumpTiles[i]->y();
        
        if(getTile(tempX-1, tempY)->pumpID() != tempPumpId
           && getTile(tempX, tempY-1)->pumpID() != tempPumpId)
        {
          if(!isTankAt(tempX,tempY))
          {
           // if(players[playerID()].oxygen()<10)
              //return;
            getTile(tempX,tempY)->spawn(2);
          }
         // if(!isTankAt(tempX+1,tempY+1))
         // {
            //if(players[playerID()].oxygen()<10)
              //return;
          //  getTile(tempX+1,tempY+1)->spawn(2);
         // }
          pumpsLookedAt.push_back(tempPumpId);
        }
        
        
        
      }
      lookedAt=false;
      
  }
  
  for(int i = 0; i < spawnTiles.size(); i++)
  {
    if(spawnTiles[i]->pumpID() > 0)
    {
      spawnTiles[i]->spawn(0);
    }
    else
      spawnTiles[i]->spawn(1);
  }
  return;
  */

}

bool AI::pathFind(int x, int y, int xEnd, int yEnd, int xStart, int yStart)
{
  bool ask;
  if(x==xStart && y==yStart)
    path.clear();
  string choice[4]={"NORTH", "SOUTH", "EAST", "WEST"};
  int newX, newY;
  for(int choiceNum=0; choiceNum<4; choiceNum++)
  {
 
    if(choice[choiceNum]=="NORTH")
    {
      newX=x;
      newY=y-1;
    }
    else if(choice[choiceNum]=="SOUTH")
    {
      newX=x;
      newY=y+1;
    }
    else if(choice[choiceNum]=="EAST")
    {
      newX=x+1;
      newY=y;
    }
    else if(choice[choiceNum]=="WEST")
    {
      newX=x-1;
      newY=y;
    }
    
    if(getTile(newX,newY) != NULL && validMove(newX, newY))
    {
      path.push_back(getTile(newX, newY));
      if(newX==xEnd && newY==yEnd)
        return true;
      else
      {
        ask=pathFind(newX, newY, xEnd, yEnd, xStart, yStart);
        if(ask)
          return true;
        else if(path.size()>0)
          path.pop_back();
      }  
    }
  }
  return false;
}

void AI::moveTo(Unit & unit, int x, int y)
{
  /*
  int variable=0;
  if(pathFind(unit.x(), unit.y(), x, y, unit.x(), unit.y()))
  {
    while(unit.movementLeft()>0)
    {
      unit.move(path[variable]->x(), path[variable]->y());
      variable++;
    }
  }*/
  
  for(int i=0; i<unit.maxMovement(); i++)
  {
    tryToAttack(unit);
    if(unit.x()<x && validMove(unit.x()+1,unit.y()))
      unit.move(unit.x()+1,unit.y());
    else if(unit.x()>x && validMove(unit.x()-1,unit.y()))
      unit.move(unit.x()-1,unit.y());
    else if(unit.y()<y && validMove(unit.x(),unit.y()+1))
      unit.move(unit.x(),unit.y()+1);
    else if(unit.y()>y && validMove(unit.x(),unit.y()-1))
      unit.move(unit.x(),unit.y()-1);
    tryToAttack(unit);
  }
  
}

void AI::digTo(Unit & unit, int x, int y)
{
  int oldX, oldY;
  Tile* tile;
  for(int i=0; i<unit.maxMovement(); i++)
  {
    tryToAttack(unit);
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
    
    tile = getTile(oldX, oldY);
    if(tile != NULL && tile->depth()<3)
      unit.dig(*tile);
    tryToAttack(unit);
  }
  unit.dig(*tile);
  tryToAttack(unit);
}

void AI::controlUnits()
{
  Tile* moveTile=NULL;
  for (int i = 0; i < units.size(); i++)
  {
    if(units[i].owner() == playerID())
    {
      if(units[i].type()==0)  //worker
      {
        tryToAttack(units[i]);
        moveTile = getNearestIce(units[i].x(), units[i].y());
        if(moveTile != NULL)
        {
          digTo(units[i], moveTile->x(), moveTile->y());
        }
        tryToAttack(units[i]);
      }
      
      if(units[i].type()==1)  //scout
      {
        tryToAttack(units[i]);
        moveTile = getNearestEnemyPump(units[i].x(), units[i].y());
        if(moveTile != NULL)
        {
          moveTo(units[i], moveTile->x(), moveTile->y());
        }
        tryToAttack(units[i]);
      }
      
      if(units[i].type()==2)  //tank
      {
        tryToAttack(units[i]);
        moveTile = getNearestFriendlyPump(units[i].x(), units[i].y());
        if(moveTile != NULL)
        {
          moveTo(units[i], moveTile->x(), moveTile->y());
        }
        tryToAttack(units[i]);
      }
    }
  }
  return;
}

void AI::tryToAttack(Unit & unit)
{
  int dist;
  for(int i=0; i < enemyUnits.size(); i++)
  {
    dist= abs(enemyUnits[i]->x()-unit.x()) + abs(enemyUnits[i]->y()-unit.y());
    if(dist<= unit.range())
    {
      unit.attack(*enemyUnits[i]);
    }
  }
}

bool AI::validMove(const int x, const int y)
{
  Tile* tile = getTile(x, y);
  int player2ID;
  if(playerID()==1)
    player2ID=0;
  else if(playerID()==0)
    player2ID=1;
  if(x<0 || y<0 || x>39 || y>19)
    return false;
  if(tile->depth()==0 && tile->waterAmount()>0)
    return false;
  if(tile->owner()==player2ID && tile->pumpID()==-1)
    return false;
  for(int i = 0; i < units.size(); i++)
  {
    if(units[i].x()==x && units[i].y()==y)
      return false;
  }
  return true;
}

bool AI::validDig(const int x, const int y)
{
  Tile* tile = getTile(x, y);
  int player2ID;
  if(playerID()==1)
    player2ID=0;
  else if(playerID()==0)
    player2ID=1;
  if(x<0 || y<0 || x>39 || y>19)
    return false;
  if(tile->depth()==0 && tile->waterAmount()>0)
    return false;
  if(tile->owner()==player2ID && tile->pumpID()==-1)
    return false;
  for(int i = 0; i < units.size(); i++)
  {
    if(units[i].x()==x && units[i].y()==y)
      return false;
  }
  return true;
}
