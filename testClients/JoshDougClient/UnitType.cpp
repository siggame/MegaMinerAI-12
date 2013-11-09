// -*-c++-*-

#include "UnitType.h"
#include "game.h"


UnitType::UnitType(_UnitType* pointer)
{
    ptr = (void*) pointer;
}

int UnitType::id()
{
  return ((_UnitType*)ptr)->id;
}

char* UnitType::name()
{
  return ((_UnitType*)ptr)->name;
}

int UnitType::type()
{
  return ((_UnitType*)ptr)->type;
}

int UnitType::cost()
{
  return ((_UnitType*)ptr)->cost;
}

int UnitType::attackPower()
{
  return ((_UnitType*)ptr)->attackPower;
}

int UnitType::digPower()
{
  return ((_UnitType*)ptr)->digPower;
}

int UnitType::fillPower()
{
  return ((_UnitType*)ptr)->fillPower;
}

int UnitType::maxHealth()
{
  return ((_UnitType*)ptr)->maxHealth;
}

int UnitType::maxMovement()
{
  return ((_UnitType*)ptr)->maxMovement;
}

int UnitType::offensePower()
{
  return ((_UnitType*)ptr)->offensePower;
}

int UnitType::defensePower()
{
  return ((_UnitType*)ptr)->defensePower;
}

int UnitType::range()
{
  return ((_UnitType*)ptr)->range;
}




std::ostream& operator<<(std::ostream& stream,UnitType ob)
{
  stream << "id: " << ((_UnitType*)ob.ptr)->id  <<'\n';
  stream << "name: " << ((_UnitType*)ob.ptr)->name  <<'\n';
  stream << "type: " << ((_UnitType*)ob.ptr)->type  <<'\n';
  stream << "cost: " << ((_UnitType*)ob.ptr)->cost  <<'\n';
  stream << "attackPower: " << ((_UnitType*)ob.ptr)->attackPower  <<'\n';
  stream << "digPower: " << ((_UnitType*)ob.ptr)->digPower  <<'\n';
  stream << "fillPower: " << ((_UnitType*)ob.ptr)->fillPower  <<'\n';
  stream << "maxHealth: " << ((_UnitType*)ob.ptr)->maxHealth  <<'\n';
  stream << "maxMovement: " << ((_UnitType*)ob.ptr)->maxMovement  <<'\n';
  stream << "offensePower: " << ((_UnitType*)ob.ptr)->offensePower  <<'\n';
  stream << "defensePower: " << ((_UnitType*)ob.ptr)->defensePower  <<'\n';
  stream << "range: " << ((_UnitType*)ob.ptr)->range  <<'\n';
  return stream;
}
