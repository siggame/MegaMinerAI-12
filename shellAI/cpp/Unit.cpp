// -*-c++-*-

#include "Unit.h"
#include "game.h"

#include "Unit.h"
#include "Tile.h"

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

int Unit::hasAttacked()
{
  return ((_Unit*)ptr)->hasAttacked;
}

int Unit::hasDug()
{
  return ((_Unit*)ptr)->hasDug;
}

int Unit::hasFilled()
{
  return ((_Unit*)ptr)->hasFilled;
}

int Unit::healthLeft()
{
  return ((_Unit*)ptr)->healthLeft;
}

int Unit::maxHealth()
{
  return ((_Unit*)ptr)->maxHealth;
}

int Unit::movementLeft()
{
  return ((_Unit*)ptr)->movementLeft;
}

int Unit::maxMovement()
{
  return ((_Unit*)ptr)->maxMovement;
}

int Unit::range()
{
  return ((_Unit*)ptr)->range;
}

int Unit::offensePower()
{
  return ((_Unit*)ptr)->offensePower;
}

int Unit::defensePower()
{
  return ((_Unit*)ptr)->defensePower;
}

int Unit::digPower()
{
  return ((_Unit*)ptr)->digPower;
}

int Unit::fillPower()
{
  return ((_Unit*)ptr)->fillPower;
}

int Unit::attackPower()
{
  return ((_Unit*)ptr)->attackPower;
}


bool Unit::move(int x, int y)
{
  return unitMove( (_Unit*)ptr, x, y);
}

bool Unit::fill(Tile& tile)
{
  return unitFill( (_Unit*)ptr, (_Tile*) tile.ptr);
}

bool Unit::dig(Tile& tile)
{
  return unitDig( (_Unit*)ptr, (_Tile*) tile.ptr);
}

bool Unit::attack(Unit& target)
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
  stream << "hasAttacked: " << ((_Unit*)ob.ptr)->hasAttacked  <<'\n';
  stream << "hasDug: " << ((_Unit*)ob.ptr)->hasDug  <<'\n';
  stream << "hasFilled: " << ((_Unit*)ob.ptr)->hasFilled  <<'\n';
  stream << "healthLeft: " << ((_Unit*)ob.ptr)->healthLeft  <<'\n';
  stream << "maxHealth: " << ((_Unit*)ob.ptr)->maxHealth  <<'\n';
  stream << "movementLeft: " << ((_Unit*)ob.ptr)->movementLeft  <<'\n';
  stream << "maxMovement: " << ((_Unit*)ob.ptr)->maxMovement  <<'\n';
  stream << "range: " << ((_Unit*)ob.ptr)->range  <<'\n';
  stream << "offensePower: " << ((_Unit*)ob.ptr)->offensePower  <<'\n';
  stream << "defensePower: " << ((_Unit*)ob.ptr)->defensePower  <<'\n';
  stream << "digPower: " << ((_Unit*)ob.ptr)->digPower  <<'\n';
  stream << "fillPower: " << ((_Unit*)ob.ptr)->fillPower  <<'\n';
  stream << "attackPower: " << ((_Unit*)ob.ptr)->attackPower  <<'\n';
  return stream;
}
