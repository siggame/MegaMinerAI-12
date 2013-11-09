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

int PumpStation::siegeAmount()
{
  return ((_PumpStation*)ptr)->siegeAmount;
}




std::ostream& operator<<(std::ostream& stream,PumpStation ob)
{
  stream << "id: " << ((_PumpStation*)ob.ptr)->id  <<'\n';
  stream << "owner: " << ((_PumpStation*)ob.ptr)->owner  <<'\n';
  stream << "siegeAmount: " << ((_PumpStation*)ob.ptr)->siegeAmount  <<'\n';
  return stream;
}
