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
void AI::init()
{
  srand(time(NULL));
  getSpawnTiles();
  getPumpTiles();
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
            spawnTiles.push_back( & tiles[i] );
        }
    }
    return;
}

void AI::getPumpTiles()
{
  spawnTiles.clear();
  for(int i = 0; i < tiles.size(); i++)
  {
    if(tiles[i].pumpID() == -1)
    {
      pumpTiles.push_back(& tiles[i]);
    }
  }
}

void AI::spawnUnits()
{
  for(int i = 0; i < spawnTiles.size(); i++)
    {
        spawnTiles[i]->spawn(rand()%2);
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
      units[i].move(units[i].x()+xDir[randomDir], units[i].y()+ yDir[randomDir]);
      
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
