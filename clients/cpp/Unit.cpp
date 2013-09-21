// -*-c++-*-

#include "Unit.h"
#include "game.h"


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

int Unit::curMovement()
{
  return ((_Unit*)ptr)->curMovement;
}

int Unit::maxMovement()
{
  return ((_Unit*)ptr)->maxMovement;
}


bool Unit::move(int x, int y)
{
  return unitMove( (_Unit*)ptr, x, y);
}

bool Unit::attack(int unit)
{
  return unitAttack( (_Unit*)ptr, unit);
}

bool Unit::fill(int tile)
{
  return unitFill( (_Unit*)ptr, tile);
}

bool Unit::build(int tile)
{
  return unitBuild( (_Unit*)ptr, tile);
}



std::ostream& operator<<(std::ostream& stream,Unit ob)
{
  stream << "id: " << ((_Unit*)ob.ptr)->id  <<'\n';
  stream << "x: " << ((_Unit*)ob.ptr)->x  <<'\n';
  stream << "y: " << ((_Unit*)ob.ptr)->y  <<'\n';
  stream << "owner: " << ((_Unit*)ob.ptr)->owner  <<'\n';
  stream << "type: " << ((_Unit*)ob.ptr)->type  <<'\n';
  stream << "curHealth: " << ((_Unit*)ob.ptr)->curHealth  <<'\n';
  stream << "curMovement: " << ((_Unit*)ob.ptr)->curMovement  <<'\n';
  stream << "maxMovement: " << ((_Unit*)ob.ptr)->maxMovement  <<'\n';
  return stream;
}
