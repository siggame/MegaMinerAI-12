// -*-c++-*-

#include "PumpStation.h"
#include "game.h"


PumpStation::PumpStation(_PumpStation* pointer)
{
    ptr = (void*) pointer;
}

int PumpStation::id()
{
  return ((_PumpStation*)ptr)->id;
}

int PumpStation::owner()
{
  return ((_PumpStation*)ptr)->owner;
}

int PumpStation::waterAmount()
{
  return ((_PumpStation*)ptr)->waterAmount;
}

int PumpStation::seigeCount()
{
  return ((_PumpStation*)ptr)->seigeCount;
}




std::ostream& operator<<(std::ostream& stream,PumpStation ob)
{
  stream << "id: " << ((_PumpStation*)ob.ptr)->id  <<'\n';
  stream << "owner: " << ((_PumpStation*)ob.ptr)->owner  <<'\n';
  stream << "waterAmount: " << ((_PumpStation*)ob.ptr)->waterAmount  <<'\n';
  stream << "seigeCount: " << ((_PumpStation*)ob.ptr)->seigeCount  <<'\n';
  return stream;
}
