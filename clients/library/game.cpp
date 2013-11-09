//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#pragma warning(disable : 4996)

#include <string>
#include <cstring>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <fstream>
#include <memory>
#include <cmath>

#include "game.h"
#include "network.h"
#include "structures.h"

#include "sexp/sfcompat.h"

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

#ifdef _WIN32
//Doh, namespace collision.
namespace Windows
{
    #include <Windows.h>
};
#else
#include <unistd.h>
#endif

#ifdef ENABLE_THREADS
#define LOCK(X) pthread_mutex_lock(X)
#define UNLOCK(X) pthread_mutex_unlock(X)
#else
#define LOCK(X)
#define UNLOCK(X)
#endif

using std::cout;
using std::cerr;
using std::endl;
using std::stringstream;
using std::string;
using std::ofstream;

DLLEXPORT Connection* createConnection()
{
  Connection* c = new Connection;
  c->socket = -1;
  #ifdef ENABLE_THREADS
  pthread_mutex_init(&c->mutex, NULL);
  #endif

  c->mapWidth = 0;
  c->mapHeight = 0;
  c->waterDamage = 0;
  c->turnNumber = 0;
  c->maxUnits = 0;
  c->playerID = 0;
  c->gameNumber = 0;
  c->maxSiege = 0;
  c->oxygenRate = 0;
  c->depositionRate = 0;
  c->Players = NULL;
  c->PlayerCount = 0;
  c->Mappables = NULL;
  c->MappableCount = 0;
  c->PumpStations = NULL;
  c->PumpStationCount = 0;
  c->Units = NULL;
  c->UnitCount = 0;
  c->Tiles = NULL;
  c->TileCount = 0;
  c->UnitTypes = NULL;
  c->UnitTypeCount = 0;
  return c;
}

DLLEXPORT void destroyConnection(Connection* c)
{
  #ifdef ENABLE_THREADS
  pthread_mutex_destroy(&c->mutex);
  #endif
  if(c->Players)
  {
    for(int i = 0; i < c->PlayerCount; i++)
    {
      delete[] c->Players[i].playerName;
    }
    delete[] c->Players;
  }
  if(c->Mappables)
  {
    for(int i = 0; i < c->MappableCount; i++)
    {
    }
    delete[] c->Mappables;
  }
  if(c->PumpStations)
  {
    for(int i = 0; i < c->PumpStationCount; i++)
    {
    }
    delete[] c->PumpStations;
  }
  if(c->Units)
  {
    for(int i = 0; i < c->UnitCount; i++)
    {
    }
    delete[] c->Units;
  }
  if(c->Tiles)
  {
    for(int i = 0; i < c->TileCount; i++)
    {
    }
    delete[] c->Tiles;
  }
  if(c->UnitTypes)
  {
    for(int i = 0; i < c->UnitTypeCount; i++)
    {
      delete[] c->UnitTypes[i].name;
    }
    delete[] c->UnitTypes;
  }
  delete c;
}

DLLEXPORT int serverConnect(Connection* c, const char* host, const char* port)
{
  c->socket = open_server_connection(host, port);
  return c->socket + 1; //false if socket == -1
}

DLLEXPORT int serverLogin(Connection* c, const char* username, const char* password)
{
  string expr = "(login \"";
  expr += username;
  expr += "\" \"";
  expr += password;
  expr +="\")";

  send_string(c->socket, expr.c_str());

  sexp_t* expression, *message;

  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;

  message = expression->list;
  if(message->val == NULL || strcmp(message->val, "login-accepted") != 0)
  {
    cerr << "Unable to login to server" << endl;
    destroy_sexp(expression);
    return 0;
  }
  destroy_sexp(expression);
  return 1;
}

DLLEXPORT int createGame(Connection* c)
{
  sexp_t* expression, *number;

  send_string(c->socket, "(create-game)");

  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;

  number = expression->list->next;
  c->gameNumber = atoi(number->val);
  destroy_sexp(expression);

  std::cout << "Creating game " << c->gameNumber << endl;

  c->playerID = 0;

  return c->gameNumber;
}

DLLEXPORT int joinGame(Connection* c, int gameNum, const char* playerType)
{
  sexp_t* expression;
  stringstream expr;

  c->gameNumber = gameNum;

  expr << "(join-game " << c->gameNumber << " "<< playerType << ")";
  send_string(c->socket, expr.str().c_str());

  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;

  if(strcmp(expression->list->val, "join-accepted") == 0)
  {
    destroy_sexp(expression);
    c->playerID = 1;
    send_string(c->socket, "(game-start)");
    return 1;
  }
  else if(strcmp(expression->list->val, "create-game") == 0)
  {
    std::cout << "Game did not exist, creating game " << c->gameNumber << endl;
    destroy_sexp(expression);
    c->playerID = 0;
    return 1;
  }
  else
  {
    cerr << "Cannot join game "<< c->gameNumber << ": " << expression->list->next->val << endl;
    destroy_sexp(expression);
    return 0;
  }
}

DLLEXPORT void endTurn(Connection* c)
{
  LOCK( &c->mutex );
  send_string(c->socket, "(end-turn)");
  UNLOCK( &c->mutex );
}

DLLEXPORT void getStatus(Connection* c)
{
  LOCK( &c->mutex );
  send_string(c->socket, "(game-status)");
  UNLOCK( &c->mutex );
}

//#TODO: Are we going to do something about playerTalk?
DLLEXPORT int playerTalk(_Player* object, char* message)
{
  stringstream expr;
  expr << "(game-talk " << object->id
      << " \"" << escape_string(message) << "\""
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  return 1;
}




DLLEXPORT int unitMove(_Unit* object, int x, int y)
{
  stringstream expr;
  expr << "(game-move " << object->id
       << " " << x
       << " " << y
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
 
  Connection* c = object->_c;

  // Only owner can control unit
  if (object->owner != getPlayerID(c))
    return 0;
  // Must have moves left
  if (object->movementLeft <= 0)
    return 0;
  // Cannot move outside map
  if (0 > x || x >= getMapWidth(c) || 0 > y || y >= getMapHeight(c))
    return 0;
  
  // Get the tile we're trying to get to
  _Tile* tile = getTile(c, x * getMapHeight(c) + y);
  // Cannot move onto ice tiles
  if (tile->owner == 3)
    return 0;
  // Cannot move onto spawning tiles
  if (tile->isSpawning == 1)
    return 0;
  // Cannot move onto enemy spawn tiles
  if (tile->owner == (getPlayerID(c)^1) && tile->pumpID == -1)
    return 0;
  // Can only move to adjacent coords
  if (abs(object->x - x) + abs(object->y - y) != 1)
    return 0;
  
  // Cannot move onto another unit
  for (int i = 0; i < getUnitCount(c); ++i)
  {
    if (getUnit(c, i)->x == x && getUnit(c, i)->y == y)
      return 0;
  }
  
    
  _Tile* prevTile = getTile(c, object->x * getMapHeight(c) + object->y);
    
  // Move the unit
  object->x = x;
  object->y = y;
  
  // Decrement movement
  object->movementLeft -= 1;


  if( tile->waterAmount > 0 )
    object->healthLeft -= getWaterDamage(c);

  //Make sure not less than 0
  if(object->healthLeft < 0)
    object->healthLeft = 0;
  
  return 1;
}

DLLEXPORT int unitFill(_Unit* object, _Tile* tile)
{
  stringstream expr;
  expr << "(game-fill " << object->id
      << " " << tile->id
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  
  Connection* c = object->_c;
  int& x = tile->x;
  int& y = tile->y;
  
  // Only owner can control unit
  if (object->owner != getPlayerID(c))
    return 0;
  // Only workers can fill
  if (object->fillPower <= 0)
    return 0;
  if (object->healthLeft <= 0)
    return 0;
  // Can only fill once per turn
  if (object->hasFilled == 1)
    return 0;
  // Can only fill adjacent tiles
  if (abs(object->x - x) + abs(object->y - y) > 1)
    return 0;
  // Must fill in trenches
  if (tile->depth <= 0)
    return 0;
  // Only dig on normal tiles
  if (tile->owner != 2)
    return 0;
  // Can't fill in a trench with a unit on it
  for (int i = 0; i < getUnitCount(c); ++i)
  {
    //Look for units that are not itself, and have same x, and y
    if (getUnit(c, i)->id != object->id && getUnit(c, i)->x == x && getUnit(c, i)->y == y)
      return 0;
  }
  
  // Decrease the trench's depth
  tile->depth -= object->fillPower;
  if (tile->depth < 0)
    tile->depth = 0;
  // Unit can no longer move
  object->movementLeft = 0;
  
  object->hasFilled = 1;

  //Reset deposition
  tile->turnsUntilDeposit = getDepositionRate(c);
  
  return 1;
}

DLLEXPORT int unitDig(_Unit* object, _Tile* tile)
{
  stringstream expr;
  expr << "(game-dig " << object->id
      << " " << tile->id
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  
  Connection* c = object->_c;
  int& x = tile->x;
  int& y = tile->y;
  
  // Only owner can control unit
  if (object->owner != getPlayerID(c))
    return 0;
  // Only diggers can dig
  if (object->digPower <= 0)
    return 0;
  if (object->healthLeft <= 0)
    return 0;
  // Can only dig once per turn
  if (object->hasDug == 1)
    return 0;
  // Can only dig adjacent tiles and the tile underneath the digger
  if (abs(object->x - x) + abs(object->y - y) > 1)
    return 0;
  // Can only dig on normal tiles
  if (tile->owner != 2)
    return 0;
  // Can't dig a trench under another unit
  for (int i = 0; i < getUnitCount(c); ++i)
  {
    //Check for units that are not itself, and have same x and y
    if (getUnit(c, i)->id != object->id && getUnit(c, i)->x == x && getUnit(c, i)->y == y)
      return 0;
  }
  
  // Increase the tiles depth
  tile->depth += object->digPower;
  tile->turnsUntilDeposit = getDepositionRate(c);
  // Unit can no longer move
  object->movementLeft = 0;
  
  object->hasDug = 1;
  
  return 1;
}

DLLEXPORT int unitAttack(_Unit* object, _Unit* target)
{
  stringstream expr;
  expr << "(game-attack " << object->id
      << " " << target->id
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  
  Connection *c = object->_c;
  int& x = target->x;
  int& y = target->y;
  
  // Only owner can control unit
  if (object->owner != getPlayerID(c))
    return 0;
  if (object->healthLeft <= 0)
    return 0;
  // Target must be adjacent
  if (abs(object->x - x) + abs(object->y - y) > object->range)
    return 0;
  // Can only attack once per turn
  if (object->hasAttacked == 1)
    return 0;
  // Can only attack enemy units
  if (object->owner == target->owner)
    return 0;
    
  object->hasAttacked = 1;
  
  // Unit can no longer move
  object->movementLeft = 0;
  
  target->healthLeft -= object->attackPower;
  if(target->healthLeft < 0)
    target->healthLeft = 0;
  
  return 1;
}


DLLEXPORT int tileSpawn(_Tile* object, int type)
{
  stringstream expr;
  expr << "(game-spawn " << object->id
       << " " << type
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  
  Connection* c = object->_c;
  
  // Can only spawn on current player's spawn tiles
  if (object->owner != getPlayerID(c))
    return 0;
  // Find unit cost
  int unitCost = -1;
  for (int i = 0; i < getUnitTypeCount(c); ++i)
  {
    if (getUnitType(c, i)->type == type)
    {
      unitCost = getUnitType(c, i)->cost;
      break;
    }
  }
  // If a unit type with matching type was not found, then they entered an invalid unit type
  if (unitCost == -1)
    return 0;
  // Only spawn if player has enough resources
  if (getPlayer(c, object->owner)->oxygen < unitCost)
    return 0;

  int count = 0;
  
  // Cannot spawn unit on top of another unit
  for (int i = 0; i < getUnitCount(c); ++i)
  {
    if (getUnit(c, i)->owner == getPlayerID(c))
      count++;
    if (getUnit(c, i)->x == object->x && getUnit(c, i)->y == object->y)
      return 0;
  }
  
  // Cannot spawn more than MaxUnits units
  if (count >= getMaxUnits(c))
    return 0;

  if (object->isSpawning == 1)
    return 0;

  // Cannot spawn unit on seiged pump stations
  if (object->pumpID != -1)
  {
    for (int i = 0; i < getPumpStationCount(c); ++i)
    {
      if (getPumpStation(c, i)->id == object->pumpID && getPumpStation(c, i)->siegeAmount > 0)
        return 0;
    }
  }

  getPlayer(c, getPlayerID(c))->oxygen -= unitCost;
  object->isSpawning = 1;
  
  return 1;
}



//Utility functions for parsing data
void parsePlayer(Connection* c, _Player* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->playerName = new char[strlen(sub->val)+1];
  strncpy(object->playerName, sub->val, strlen(sub->val));
  object->playerName[strlen(sub->val)] = 0;
  sub = sub->next;
  object->time = atof(sub->val);
  sub = sub->next;
  object->waterStored = atoi(sub->val);
  sub = sub->next;
  object->oxygen = atoi(sub->val);
  sub = sub->next;
  object->maxOxygen = atoi(sub->val);
  sub = sub->next;

}
void parseMappable(Connection* c, _Mappable* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;

}
void parsePumpStation(Connection* c, _PumpStation* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->owner = atoi(sub->val);
  sub = sub->next;
  object->siegeAmount = atoi(sub->val);
  sub = sub->next;

}
void parseUnit(Connection* c, _Unit* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;
  object->owner = atoi(sub->val);
  sub = sub->next;
  object->type = atoi(sub->val);
  sub = sub->next;
  object->hasAttacked = atoi(sub->val);
  sub = sub->next;
  object->hasDug = atoi(sub->val);
  sub = sub->next;
  object->hasFilled = atoi(sub->val);
  sub = sub->next;
  object->healthLeft = atoi(sub->val);
  sub = sub->next;
  object->maxHealth = atoi(sub->val);
  sub = sub->next;
  object->movementLeft = atoi(sub->val);
  sub = sub->next;
  object->maxMovement = atoi(sub->val);
  sub = sub->next;
  object->range = atoi(sub->val);
  sub = sub->next;
  object->offensePower = atoi(sub->val);
  sub = sub->next;
  object->defensePower = atoi(sub->val);
  sub = sub->next;
  object->digPower = atoi(sub->val);
  sub = sub->next;
  object->fillPower = atoi(sub->val);
  sub = sub->next;
  object->attackPower = atoi(sub->val);
  sub = sub->next;

}
void parseTile(Connection* c, _Tile* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;
  object->owner = atoi(sub->val);
  sub = sub->next;
  object->pumpID = atoi(sub->val);
  sub = sub->next;
  object->waterAmount = atoi(sub->val);
  sub = sub->next;
  object->depth = atoi(sub->val);
  sub = sub->next;
  object->turnsUntilDeposit = atoi(sub->val);
  sub = sub->next;
  object->isSpawning = atoi(sub->val);
  sub = sub->next;

}
void parseUnitType(Connection* c, _UnitType* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->name = new char[strlen(sub->val)+1];
  strncpy(object->name, sub->val, strlen(sub->val));
  object->name[strlen(sub->val)] = 0;
  sub = sub->next;
  object->type = atoi(sub->val);
  sub = sub->next;
  object->cost = atoi(sub->val);
  sub = sub->next;
  object->attackPower = atoi(sub->val);
  sub = sub->next;
  object->digPower = atoi(sub->val);
  sub = sub->next;
  object->fillPower = atoi(sub->val);
  sub = sub->next;
  object->maxHealth = atoi(sub->val);
  sub = sub->next;
  object->maxMovement = atoi(sub->val);
  sub = sub->next;
  object->offensePower = atoi(sub->val);
  sub = sub->next;
  object->defensePower = atoi(sub->val);
  sub = sub->next;
  object->range = atoi(sub->val);
  sub = sub->next;

}

DLLEXPORT int networkLoop(Connection* c)
{
  while(true)
  {
    sexp_t* base, *expression, *sub, *subsub;

    char* message = rec_string(c->socket);
    string text = message;
    base = extract_sexpr(message);
    delete[] message;
    expression = base->list;
    if(expression->val != NULL && strcmp(expression->val, "game-winner") == 0)
    {
      expression = expression->next->next->next;
      int winnerID = atoi(expression->val);
      if(winnerID == c->playerID)
      {
        cout << "You win!" << endl << expression->next->val << endl;
      }
      else
      {
        cout << "You lose. :(" << endl << expression->next->val << endl;
      }
      stringstream expr;
      expr << "(request-log " << c->gameNumber << ")";
      send_string(c->socket, expr.str().c_str());
      destroy_sexp(base);
      return 0;
    }
    else if(expression->val != NULL && strcmp(expression->val, "log") == 0)
    {
      ofstream out;
      stringstream filename;
      expression = expression->next;
      filename << expression->val;
      filename << ".gamelog";
      expression = expression->next;
      out.open(filename.str().c_str());
      if (out.good())
        out.write(expression->val, strlen(expression->val));
      else
        cerr << "Error : Could not create log." << endl;
      out.close();
      destroy_sexp(base);
      return 0;
    }
    else if(expression->val != NULL && strcmp(expression->val, "game-accepted")==0)
    {
      char gameID[30];

      expression = expression->next;
      strcpy(gameID, expression->val);
      cout << "Created game " << gameID << endl;
    }
    else if(expression->val != NULL && strstr(expression->val, "denied"))
    {
      cout << expression->val << endl;
      cout << expression->next->val << endl;
    }
    else if(expression->val != NULL && strcmp(expression->val, "status") == 0)
    {
      while(expression->next != NULL)
      {
        expression = expression->next;
        sub = expression->list;
        if(string(sub->val) == "game")
        {
          sub = sub->next;
          c->mapWidth = atoi(sub->val);
          sub = sub->next;

          c->mapHeight = atoi(sub->val);
          sub = sub->next;

          c->waterDamage = atoi(sub->val);
          sub = sub->next;

          c->turnNumber = atoi(sub->val);
          sub = sub->next;

          c->maxUnits = atoi(sub->val);
          sub = sub->next;

          c->playerID = atoi(sub->val);
          sub = sub->next;

          c->gameNumber = atoi(sub->val);
          sub = sub->next;

          c->maxSiege = atoi(sub->val);
          sub = sub->next;

          c->oxygenRate = atof(sub->val);
          sub = sub->next;

          c->depositionRate = atoi(sub->val);
          sub = sub->next;

        }
        else if(string(sub->val) == "Player")
        {
          if(c->Players)
          {
            for(int i = 0; i < c->PlayerCount; i++)
            {
              delete[] c->Players[i].playerName;
            }
            delete[] c->Players;
          }
          c->PlayerCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Players = new _Player[c->PlayerCount];
          for(int i = 0; i < c->PlayerCount; i++)
          {
            sub = sub->next;
            parsePlayer(c, c->Players+i, sub);
          }
        }
        else if(string(sub->val) == "Mappable")
        {
          if(c->Mappables)
          {
            for(int i = 0; i < c->MappableCount; i++)
            {
            }
            delete[] c->Mappables;
          }
          c->MappableCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Mappables = new _Mappable[c->MappableCount];
          for(int i = 0; i < c->MappableCount; i++)
          {
            sub = sub->next;
            parseMappable(c, c->Mappables+i, sub);
          }
        }
        else if(string(sub->val) == "PumpStation")
        {
          if(c->PumpStations)
          {
            sub = sub->next;
            for(int i = 0; i < c->PumpStationCount; i++)
            {
              if(!sub)
              {
                break;
              }
              int id = atoi(sub->list->val);
              if(id == c->PumpStations[i].id)
              {
                parsePumpStation(c, c->PumpStations+i, sub);
                sub = sub->next;
              }
            }
          }
          else
          {
            c->PumpStationCount =  sexp_list_length(expression)-1; //-1 for the header
            c->PumpStations = new _PumpStation[c->PumpStationCount];
            for(int i = 0; i < c->PumpStationCount; i++)
            {
              sub = sub->next;
              parsePumpStation(c, c->PumpStations+i, sub);
            }
          }
        }
        else if(string(sub->val) == "Unit")
        {
          if(c->Units)
          {
            for(int i = 0; i < c->UnitCount; i++)
            {
            }
            delete[] c->Units;
          }
          c->UnitCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Units = new _Unit[c->UnitCount];
          for(int i = 0; i < c->UnitCount; i++)
          {
            sub = sub->next;
            parseUnit(c, c->Units+i, sub);
          }
        }
        else if(string(sub->val) == "Tile")
        {
          if(c->Tiles)
          {
            sub = sub->next;
            for(int i = 0; i < c->TileCount; i++)
            {
              if(!sub)
              {
                break;
              }
              int id = atoi(sub->list->val);
              if(id == c->Tiles[i].id)
              {
                parseTile(c, c->Tiles+i, sub);
                sub = sub->next;
              }
            }
          }
          else
          {
            c->TileCount =  sexp_list_length(expression)-1; //-1 for the header
            c->Tiles = new _Tile[c->TileCount];
            for(int i = 0; i < c->TileCount; i++)
            {
              sub = sub->next;
              parseTile(c, c->Tiles+i, sub);
            }
          }
        }
        else if(string(sub->val) == "UnitType")
        {
          if(c->UnitTypes)
          {
            sub = sub->next;
            for(int i = 0; i < c->UnitTypeCount; i++)
            {
              if(!sub)
              {
                break;
              }
              int id = atoi(sub->list->val);
              if(id == c->UnitTypes[i].id)
              {
                delete[] c->UnitTypes[i].name;
                parseUnitType(c, c->UnitTypes+i, sub);
                sub = sub->next;
              }
            }
          }
          else
          {
            c->UnitTypeCount =  sexp_list_length(expression)-1; //-1 for the header
            c->UnitTypes = new _UnitType[c->UnitTypeCount];
            for(int i = 0; i < c->UnitTypeCount; i++)
            {
              sub = sub->next;
              parseUnitType(c, c->UnitTypes+i, sub);
            }
          }
        }
      }
      destroy_sexp(base);
      return 1;
    }
    else
    {
#ifdef SHOW_WARNINGS
      cerr << "Unrecognized message: " << text << endl;
#endif
    }
    destroy_sexp(base);
  }
}

DLLEXPORT _Player* getPlayer(Connection* c, int num)
{
  return c->Players + num;
}
DLLEXPORT int getPlayerCount(Connection* c)
{
  return c->PlayerCount;
}

DLLEXPORT _Mappable* getMappable(Connection* c, int num)
{
  return c->Mappables + num;
}
DLLEXPORT int getMappableCount(Connection* c)
{
  return c->MappableCount;
}

DLLEXPORT _PumpStation* getPumpStation(Connection* c, int num)
{
  return c->PumpStations + num;
}
DLLEXPORT int getPumpStationCount(Connection* c)
{
  return c->PumpStationCount;
}

DLLEXPORT _Unit* getUnit(Connection* c, int num)
{
  return c->Units + num;
}
DLLEXPORT int getUnitCount(Connection* c)
{
  return c->UnitCount;
}

DLLEXPORT _Tile* getTile(Connection* c, int num)
{
  return c->Tiles + num;
}
DLLEXPORT int getTileCount(Connection* c)
{
  return c->TileCount;
}

DLLEXPORT _UnitType* getUnitType(Connection* c, int num)
{
  return c->UnitTypes + num;
}
DLLEXPORT int getUnitTypeCount(Connection* c)
{
  return c->UnitTypeCount;
}


DLLEXPORT int getMapWidth(Connection* c)
{
  return c->mapWidth;
}
DLLEXPORT int getMapHeight(Connection* c)
{
  return c->mapHeight;
}
DLLEXPORT int getWaterDamage(Connection* c)
{
  return c->waterDamage;
}
DLLEXPORT int getTurnNumber(Connection* c)
{
  return c->turnNumber;
}
DLLEXPORT int getMaxUnits(Connection* c)
{
  return c->maxUnits;
}
DLLEXPORT int getPlayerID(Connection* c)
{
  return c->playerID;
}
DLLEXPORT int getGameNumber(Connection* c)
{
  return c->gameNumber;
}
DLLEXPORT int getMaxSiege(Connection* c)
{
  return c->maxSiege;
}
DLLEXPORT float getOxygenRate(Connection* c)
{
  return c->oxygenRate;
}
DLLEXPORT int getDepositionRate(Connection* c)
{
  return c->depositionRate;
}
