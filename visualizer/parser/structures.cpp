// -*-c++-*-

#include "structures.h"

#include <iostream>

namespace parser
{


std::ostream& operator<<(std::ostream& stream, PumpStation ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "owner: " << ob.owner  <<'\n';
  stream << "waterAmount: " << ob.waterAmount  <<'\n';
  stream << "seigeCount: " << ob.seigeCount  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Mappable ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Player ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "playerName: " << ob.playerName  <<'\n';
  stream << "time: " << ob.time  <<'\n';
  stream << "waterStored: " << ob.waterStored  <<'\n';
  stream << "spawnRate: " << ob.spawnRate  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Tile ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  stream << "owner: " << ob.owner  <<'\n';
  stream << "type: " << ob.type  <<'\n';
  stream << "resId: " << ob.resId  <<'\n';
  stream << "waterAmount: " << ob.waterAmount  <<'\n';
  stream << "isTrench: " << ob.isTrench  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Unit ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  stream << "owner: " << ob.owner  <<'\n';
  stream << "type: " << ob.type  <<'\n';
  stream << "curHealth: " << ob.curHealth  <<'\n';
  stream << "curMovement: " << ob.curMovement  <<'\n';
  stream << "maxMovement: " << ob.maxMovement  <<'\n';
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


std::ostream& operator<<(std::ostream& stream, GameState ob)
{
  stream << "maxHealth: " << ob.maxHealth  <<'\n';
  stream << "trenchDamage: " << ob.trenchDamage  <<'\n';
  stream << "waterDamage: " << ob.waterDamage  <<'\n';
  stream << "turnNumber: " << ob.turnNumber  <<'\n';
  stream << "attackDamage: " << ob.attackDamage  <<'\n';
  stream << "offenseCount: " << ob.offenseCount  <<'\n';
  stream << "defenseCount: " << ob.defenseCount  <<'\n';
  stream << "maxUnits: " << ob.maxUnits  <<'\n';

  stream << "\n\nPumpStations:\n";
  for(std::map<int,PumpStation>::iterator i = ob.speciesList.begin(); i != ob.speciesList.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nMappables:\n";
  for(std::map<int,Mappable>::iterator i = ob.mappables.begin(); i != ob.mappables.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nPlayers:\n";
  for(std::map<int,Player>::iterator i = ob.players.begin(); i != ob.players.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nTiles:\n";
  for(std::map<int,Tile>::iterator i = ob.tiles.begin(); i != ob.tiles.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nUnits:\n";
  for(std::map<int,Unit>::iterator i = ob.units.begin(); i != ob.units.end(); i++)
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
//    if((*(*i)).type == MOVE)
//      stream << *((move*)*i) << "\n";
  }
  

  }
  return stream;
}

Game::Game()
{
  winner = -1;
}

} // parser
