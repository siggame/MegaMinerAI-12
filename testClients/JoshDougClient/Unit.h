// -*-c++-*-

#ifndef UNIT_H
#define UNIT_H

#include <iostream>
#include "structures.h"

#include "Mappable.h"
class Tile;
class Unit;

///Represents a single unit on the map.
class Unit : public Mappable {
  public:
  Unit(_Unit* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///X position of the object
  int x();
  ///Y position of the object
  int y();
  ///The owner of this unit.
  int owner();
  ///The type of this unit (digger/filler).
  int type();
  ///Whether current unit has attacked or not.
  int hasAttacked();
  ///Whether the current unit has digged or not.
  int hasDigged();
  ///Whether the current unit has built or not.
  int hasBuilt();
  ///The current amount health this unit has remaining.
  int healthLeft();
  ///The maximum amount of this health this unit can have
  int maxHealth();
  ///The number of moves this unit has remaining.
  int movementLeft();
  ///The maximum number of moves this unit can move.
  int maxMovement();

  // Actions
  ///Make the unit move to the respective x and y location.
  bool move(int x, int y);
  ///Put dirt in a hole!
  bool fill(Tile& tile);
  ///Dig out a tile
  bool dig(Tile& tile);
  ///Command to attack another Unit.
  bool attack(Unit& target);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Unit ob);
};

#endif
