// -*-c++-*-

#ifndef TILE_H
#define TILE_H

#include <iostream>
#include "vc_structures.h"

#include "Mappable.h"

namespace client
{


///Represents a single tile on the map, can contain some amount of water.
class Tile : public Mappable {
  public:
  Tile(_Tile* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///X position of the object
  int x();
  ///Y position of the object
  int y();
  ///The owner of the tile.
  int owner();
  ///Determines if this tile is a part of a Pump Station.
  int pumpID();
  ///The amount of water contained on the tile.
  int waterAmount();
  ///The depth of the tile. Tile is a trench if depth is greater than zero.
  int depth();

  // Actions
  ///Attempt to spawn a unit of a type on this tile.
  int spawn(int type);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Tile ob);
};

}

#endif

