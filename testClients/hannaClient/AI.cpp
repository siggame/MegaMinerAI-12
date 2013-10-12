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

Tile* AI::getTile(int x, int y)
{
  return & tiles[x*mapHeight() +y];
}

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
  for(int i = 0; i < tiles.size(); i++) //spawn as many unit as possible
  {
    if (tiles[i].owner() == playerID() )
    {
      tiles[i].spawn(0);
    }
  }
  for (int i = 0; i < units.size(); i++)
  {
    if (units[i].owner() == playerID() )
    {
      units[i].move(units[i].x()+1, units[i].y() );
      if (units[i].y()+1 >= mapHeight())
      {
        units[i].dig(*getTile(units[i].x(), units[i].y()+1));
        units[i].fill(*getTile(units[i].x(), units[i].y()+1));
      }
    }
  }
  
  return true;
}

//This function is run once, after your last turn.
void AI::end(){}
