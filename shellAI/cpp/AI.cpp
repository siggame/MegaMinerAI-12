#include "AI.h"
#include "util.h"

//Enum for spawning units
enum
{
    WORKER,
    SCOUT,
    TANK,
};

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
  int numberOfUnits = 0;
  //get the number of units owned
  for(int i = 0; i < units.size(); i++)
  {
    //if I own this unit increase the count
    if(units[i].owner() == playerID())
    {
      numberOfUnits++;
    }
  }
  //look for my tiles
  for(int i = 0; i < tiles.size(); i++)
  {
    //if this tile is my spawn tile or my pump station
    if(tiles[i].owner() == playerID())
    {
      //get the unit cost for a worker
      int cost;
      for(int j = 0; j < unitTypes.size(); j++)
      {
        if(unitTypes[j].type() == WORKER)
        {
          cost = unitTypes[j].cost();
        }
      }
      //if there is enough oxygen to spawn the unit
      if(players[playerID()].oxygen() >= cost)
      {
        //if can spawn more units in
        if(numberOfUnits < maxUnits())
        {
          //if nothing is spawning on the tile
          if(!tiles[i].isSpawning())
          {
            bool canSpawn = true;
            //if it is a pump station and it's not being seiged
            if(tiles[i].pumpID() != -1)
            {
              //find the pump in the vector
              for(int j = 0; j < pumpStations.size(); j++)
              {
                //if it's being sieged, don't spawn
                if(pumpStations[j].id() == tiles[i].pumpID() &&
                   pumpStations[j].siegeAmount() > 0)
                {
                  canSpawn = false;
                }
              }
            }
            //if there is someone else on the tile, don't spawn
            for(int j = 0; j < units.size(); j++)
            {
              if(tiles[i].x() == units[j].x() &&
                 tiles[i].y() == units[j].y())
              {
                canSpawn = false;
              }
            }
            if(canSpawn)
            {
              //spawn the unit
              tiles[i].spawn(WORKER);
              //increment unit count
              numberOfUnits++;
            }
          }
        }
      }
    }
  }
  int moveDelta = 0;
  //set to move left or right based on id; towards the center
  if(playerID() == 0)
  {
    moveDelta = 1;
  }
  else
  {
    moveDelta = -1;
  }
  //do stuff for each unit
  for(int i = 0; i < units.size(); i++)
  {
    //if you own the unit
    if(units[i].owner() != playerID())
    {
      //ignore it if it isn't
      continue;
    }
    //try to move to the right or left movement times
    for(int z = 0; z < units[i].maxMovement(); z++)
    {
      bool canMove = true;
      //if there is no unit there
      for(int j = 0; j < units.size(); j++)
      {
        if(units[i].x() + moveDelta == units[j].x() &&
           units[i].y() == units[j].y())
        {
          canMove = false;
        }
      }
      //if nothing's there and it's not moving off the edge of the map
      if(canMove &&
         units[i].x() + moveDelta >= 0 &&
         units[i].x() + moveDelta < mapWidth())
      {
        //if the tile is not an enemy spawn point
        if(!(tiles[(units[i].x() + moveDelta) * mapHeight() + units[i].y()].pumpID() == -1 &&
             tiles[(units[i].x() + moveDelta) * mapHeight() + units[i].y()].owner() == 1 - playerID()) ||
           tiles[(units[i].x() + moveDelta) * mapHeight() + units[i].y()].owner() == 2)
        {
          //if the tile is not an ice tile
          if(!(tiles[(units[i].x() + moveDelta) * mapHeight() + units[i].y()].owner() == 3 &&
               tiles[(units[i].x() + moveDelta) * mapHeight() + units[i].y()].waterAmount() > 0))
          {
            //if the tile is not spawning anything
            if(!(tiles[(units[i].x() + moveDelta) * mapHeight() + units[i].y()].isSpawning()))
            {
              //if the unit is alive
              if(units[i].healthLeft() > 0)
              {
                //move the unit
                units[i].move(units[i].x() + moveDelta, units[i].y());
              }
            }
          }
        }
      }
    }
    //if there is an enemy in the movement direction and the unit hasn't
    //attacked and it is alive
    if(!units[i].hasAttacked() && units[i].healthLeft() > 0)
    {
      for(int j = 0; j < units.size(); j++)
      {
        //check if there is a enemy unit in the direction
        if(units[i].x() + moveDelta == units[j].x() &&
           units[i].y() == units[j].y() &&
           units[j].owner() != playerID())
        {
          //attack it
          units[i].attack(units[j]);
          break;
        }
      }
    }
    //if there is a space to dig below the unit and the unit hasn't dug
    //and the unit is alive
    if(units[i].y() != mapHeight() - 1 &&
       tiles[units[i].x() * mapHeight() + units[i].y() + 1].pumpID() == -1 &&
       tiles[units[i].x() * mapHeight() + units[i].y() + 1].owner() == 2 &&
       units[i].hasDug() == false &&
       units[i].healthLeft() > 0)
    {
      bool canDig = true;
      //make sure there is no unit on that tile
      for(int j = 0; j < units.size(); j++)
      {
        if(units[i].x() == units[j].x() &&
           units[i].y() + 1 == units[j].y())
        {
          canDig = false;
        }
      }
      //make sure the tile is not an ice tile
      if(canDig &&
        !(tiles[units[i].x() * mapHeight() + units[i].y() + 1].owner() == 3 &&
          tiles[units[i].x() * mapHeight() + units[i].y() + 1].waterAmount() > 0))
      {
        units[i].dig(tiles[units[i].x() * mapHeight() + units[i].y() + 1]);
      }
    }
  }
  return true;
}

//This function is run once, after your last turn.
void AI::end(){}
