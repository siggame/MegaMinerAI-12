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

int PumpStation::siegeCount()
{
  return ((_PumpStation*)ptr)->siegeCount;
}




std::ostream& operator<<(std::ostream& stream,PumpStation ob)
{
  stream << "id: " << ((_PumpStation*)ob.ptr)->id  <<'\n';
  stream << "owner: " << ((_PumpStation*)ob.ptr)->owner  <<'\n';
  stream << "waterAmount: " << ((_PumpStation*)ob.ptr)->waterAmount  <<'\n';
  stream << "siegeCount: " << ((_PumpStation*)ob.ptr)->siegeCount  <<'\n';
  return stream;
}
