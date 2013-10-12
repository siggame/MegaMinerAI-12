// -*-c++-*-

#ifndef TILE_H
#define TILE_H

#include <iostream>
#include "structures.h"

#include "Mappable.h"

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
  ///The type of tile this tile represents.
  int type();
  ///Determines if this tile is a part of a Pump Station.
  int pumpID();
  ///The amount of water contained on the tile.
  int waterAmount();
  ///Whether the tile is a trench or not.
  int isTrench();

  // Actions
  ///Attempt to spawn a unit of a type on this tile.
  bool spawn(int type);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Tile ob);
};

#endif

