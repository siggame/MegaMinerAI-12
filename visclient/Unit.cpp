// -*-c++-*-

#include "Unit.h"
#include "game.h"

#include "Tile.h"
#include "Unit.h"

namespace client
{

Unit::Unit(_Unit* pointer)
{
    ptr = (void*) pointer;
}

int Unit::id()
{
  return ((_Unit*)ptr)->id;
}

int Unit::x()
{
  return ((_Unit*)ptr)->x;
}

int Unit::y()
{
  return ((_Unit*)ptr)->y;
}

int Unit::owner()
{
  return ((_Unit*)ptr)->owner;
}

int Unit::type()
{
  return ((_Unit*)ptr)->type;
}

int Unit::curHealth()
{
  return ((_Unit*)ptr)->curHealth;
}

int Unit::maxHealth()
{
  return ((_Unit*)ptr)->maxHealth;
}

int Unit::curMovement()
{
  return ((_Unit*)ptr)->curMovement;
}

int Unit::maxMovement()
{
  return ((_Unit*)ptr)->maxMovement;
}


int Unit::move(int x, int y)
{
  return unitMove( (_Unit*)ptr, x, y);
}

int Unit::fill(Tile& tile)
{
  return unitFill( (_Unit*)ptr, (_Tile*) tile.ptr);
}

int Unit::dig(Tile& tile)
{
  return unitDig( (_Unit*)ptr, (_Tile*) tile.ptr);
}

int Unit::attack(Unit& target)
{
  return unitAttack( (_Unit*)ptr, (_Unit*) target.ptr);
}



std::ostream& operator<<(std::ostream& stream,Unit ob)
{
  stream << "id: " << ((_Unit*)ob.ptr)->id  <<'\n';
  stream << "x: " << ((_Unit*)ob.ptr)->x  <<'\n';
  stream << "y: " << ((_Unit*)ob.ptr)->y  <<'\n';
  stream << "owner: " << ((_Unit*)ob.ptr)->owner  <<'\n';
  stream << "type: " << ((_Unit*)ob.ptr)->type  <<'\n';
  stream << "curHealth: " << ((_Unit*)ob.ptr)->curHealth  <<'\n';
  stream << "maxHealth: " << ((_Unit*)ob.ptr)->maxHealth  <<'\n';
  stream << "curMovement: " << ((_Unit*)ob.ptr)->curMovement  <<'\n';
  stream << "maxMovement: " << ((_Unit*)ob.ptr)->maxMovement  <<'\n';
  return stream;
}

}
