// -*-c++-*-

#include "Tile.h"
#include "game.h"


namespace client
{

Tile::Tile(_Tile* pointer)
{
    ptr = (void*) pointer;
}

int Tile::id()
{
  return ((_Tile*)ptr)->id;
}

int Tile::x()
{
  return ((_Tile*)ptr)->x;
}

int Tile::y()
{
  return ((_Tile*)ptr)->y;
}

int Tile::owner()
{
  return ((_Tile*)ptr)->owner;
}

int Tile::type()
{
  return ((_Tile*)ptr)->type;
}

int Tile::pumpID()
{
  return ((_Tile*)ptr)->pumpID;
}

int Tile::waterAmount()
{
  return ((_Tile*)ptr)->waterAmount;
}

int Tile::isTrench()
{
  return ((_Tile*)ptr)->isTrench;
}


int Tile::spawn(int type)
{
  return tileSpawn( (_Tile*)ptr, type);
}



std::ostream& operator<<(std::ostream& stream,Tile ob)
{
  stream << "id: " << ((_Tile*)ob.ptr)->id  <<'\n';
  stream << "x: " << ((_Tile*)ob.ptr)->x  <<'\n';
  stream << "y: " << ((_Tile*)ob.ptr)->y  <<'\n';
  stream << "owner: " << ((_Tile*)ob.ptr)->owner  <<'\n';
  stream << "type: " << ((_Tile*)ob.ptr)->type  <<'\n';
  stream << "pumpID: " << ((_Tile*)ob.ptr)->pumpID  <<'\n';
  stream << "waterAmount: " << ((_Tile*)ob.ptr)->waterAmount  <<'\n';
  stream << "isTrench: " << ((_Tile*)ob.ptr)->isTrench  <<'\n';
  return stream;
}

}
