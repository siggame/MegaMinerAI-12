// -*-c++-*-

#include "structures.h"

#include <iostream>

namespace parser
{


std::ostream& operator<<(std::ostream& stream, Player ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "playerName: " << ob.playerName  <<'\n';
  stream << "time: " << ob.time  <<'\n';
  stream << "waterStored: " << ob.waterStored  <<'\n';
  stream << "oxygen: " << ob.oxygen  <<'\n';
  stream << "maxOxygen: " << ob.maxOxygen  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Mappable ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, PumpStation ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "owner: " << ob.owner  <<'\n';
  stream << "waterAmount: " << ob.waterAmount  <<'\n';
  stream << "siegeAmount: " << ob.siegeAmount  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Unit ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  stream << "owner: " << ob.owner  <<'\n';
  stream << "type: " << ob.type  <<'\n';
  stream << "hasAttacked: " << ob.hasAttacked  <<'\n';
  stream << "hasDug: " << ob.hasDug  <<'\n';
  stream << "hasFilled: " << ob.hasFilled  <<'\n';
  stream << "healthLeft: " << ob.healthLeft  <<'\n';
  stream << "maxHealth: " << ob.maxHealth  <<'\n';
  stream << "movementLeft: " << ob.movementLeft  <<'\n';
  stream << "maxMovement: " << ob.maxMovement  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Tile ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  stream << "owner: " << ob.owner  <<'\n';
  stream << "pumpID: " << ob.pumpID  <<'\n';
  stream << "waterAmount: " << ob.waterAmount  <<'\n';
  stream << "isTrench: " << ob.isTrench  <<'\n';
  return stream;
}



std::ostream& operator<<(std::ostream& stream, spawn ob)
{
  stream << "spawn" << "\n";
  stream << "sourceID: " << ob.sourceID  <<'\n';
  stream << "unitID: " << ob.unitID  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, move ob)
{
  stream << "move" << "\n";
  stream << "actingID: " << ob.actingID  <<'\n';
  stream << "fromX: " << ob.fromX  <<'\n';
  stream << "fromY: " << ob.fromY  <<'\n';
  stream << "toX: " << ob.toX  <<'\n';
  stream << "toY: " << ob.toY  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, fill ob)
{
  stream << "fill" << "\n";
  stream << "actingID: " << ob.actingID  <<'\n';
  stream << "tileID: " << ob.tileID  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, death ob)
{
  stream << "death" << "\n";
  stream << "sourceID: " << ob.sourceID  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, dig ob)
{
  stream << "dig" << "\n";
  stream << "actingID: " << ob.actingID  <<'\n';
  stream << "tileID: " << ob.tileID  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, flow ob)
{
  stream << "flow" << "\n";
  stream << "sourceID: " << ob.sourceID  <<'\n';
  stream << "destID: " << ob.destID  <<'\n';
  stream << "waterAmount: " << ob.waterAmount  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, attack ob)
{
  stream << "attack" << "\n";
  stream << "actingID: " << ob.actingID  <<'\n';
  stream << "targetID: " << ob.targetID  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, GameState ob)
{
  stream << "mapWidth: " << ob.mapWidth  <<'\n';
  stream << "mapHeight: " << ob.mapHeight  <<'\n';
  stream << "maxHealth: " << ob.maxHealth  <<'\n';
  stream << "trenchDamage: " << ob.trenchDamage  <<'\n';
  stream << "waterDamage: " << ob.waterDamage  <<'\n';
  stream << "turnNumber: " << ob.turnNumber  <<'\n';
  stream << "attackDamage: " << ob.attackDamage  <<'\n';
  stream << "offensePower: " << ob.offensePower  <<'\n';
  stream << "defensePower: " << ob.defensePower  <<'\n';
  stream << "maxUnits: " << ob.maxUnits  <<'\n';
  stream << "unitCost: " << ob.unitCost  <<'\n';
  stream << "playerID: " << ob.playerID  <<'\n';
  stream << "gameNumber: " << ob.gameNumber  <<'\n';
  stream << "maxSiege: " << ob.maxSiege  <<'\n';
  stream << "oxygenRate: " << ob.oxygenRate  <<'\n';

  stream << "\n\nPlayers:\n";
  for(std::map<int,Player>::iterator i = ob.players.begin(); i != ob.players.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nMappables:\n";
  for(std::map<int,Mappable>::iterator i = ob.mappables.begin(); i != ob.mappables.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nPumpStations:\n";
  for(std::map<int,PumpStation>::iterator i = ob.pumpStations.begin(); i != ob.pumpStations.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nUnits:\n";
  for(std::map<int,Unit>::iterator i = ob.units.begin(); i != ob.units.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nTiles:\n";
  for(std::map<int,Tile>::iterator i = ob.tiles.begin(); i != ob.tiles.end(); i++)
    stream << i->second << '\n';
  stream << "\nAnimation\n";
  for
    (
    std::map< int, std::vector< SmartPointer< Animation > > >::iterator j = ob.animations.begin(); 
    j != ob.animations.end(); 
    j++ 
    )
  {
  for(std::vector< SmartPointer< Animation > >::iterator i = j->second.begin(); i != j->second.end(); i++)
  {
//    if((*(*i)).type == SPAWN)
//      stream << *((spawn*)*i) << "\n";
//    if((*(*i)).type == MOVE)
//      stream << *((move*)*i) << "\n";
//    if((*(*i)).type == FILL)
//      stream << *((fill*)*i) << "\n";
//    if((*(*i)).type == DEATH)
//      stream << *((death*)*i) << "\n";
//    if((*(*i)).type == DIG)
//      stream << *((dig*)*i) << "\n";
//    if((*(*i)).type == FLOW)
//      stream << *((flow*)*i) << "\n";
//    if((*(*i)).type == ATTACK)
//      stream << *((attack*)*i) << "\n";
  }
  

  }
  return stream;
}

Game::Game()
{
  winner = -1;
}

} // parser
