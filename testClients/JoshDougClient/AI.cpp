#include "AI.h"
#include "util.h"

AI::AI(Connection* conn) : BaseAI(conn) {}

const char* AI::username()
{
  return "Shell AI";
}

const char* AI::password()
{
  return "password";
}

//This function is run once, before your first turn.
void AI::init(){}

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

void AI::spawnUnits()
{
  for(int i = 0; i < tiles.size(); i++) //spawn as many unit as possible
  {
    if (tiles[i].owner() == playerID())
    {
      tiles[i].spawn(0);
    }
  }
  return;
}

void AI::moveUnits()
{
  int xDir[] = {0,0,-1,1};  //up,down,left,right
  int yDir[] = {-1,1,0,0};
  int randomDir;
  for (int i = 0; i < units.size(); i++)
  {
    if (units[i].owner() == playerID() )
    {
      randomDir=rand()%4;
      units[i].move(units[i].x()+xDir[randomDir], units[i].y()+ yDir[randomDir] );
      if (units[i].y()+1 >= mapHeight())
      {
        units[i].dig(*getTile(units[i].x(), units[i].y()+1));
        units[i].fill(*getTile(units[i].x(), units[i].y()+1));
      }
    }
  }
}
