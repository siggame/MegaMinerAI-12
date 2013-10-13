// -*-c++-*-

#include "PumpStation.h"
#include "game.h"


namespace client
{

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

int PumpStation::siegeAmount()
{
  return ((_PumpStation*)ptr)->siegeAmount;
}




std::ostream& operator<<(std::ostream& stream,PumpStation ob)
{
  stream << "id: " << ((_PumpStation*)ob.ptr)->id  <<'\n';
  stream << "owner: " << ((_PumpStation*)ob.ptr)->owner  <<'\n';
  stream << "waterAmount: " << ((_PumpStation*)ob.ptr)->waterAmount  <<'\n';
  stream << "siegeAmount: " << ((_PumpStation*)ob.ptr)->siegeAmount  <<'\n';
  return stream;
}

}
