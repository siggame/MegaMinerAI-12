// -*-c++-*-

#ifndef UNIT_H
#define UNIT_H

#include <iostream>
#include "vc_structures.h"

#include "Mappable.h"

namespace client
{


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
  ///The maximum number of moves this unit can move.
  int type();
  ///The current amount health this unit has remaining.
  int curHealth();
  ///The number of moves this unit has remaining.
  int curMovement();
  ///The maximum number of moves this unit can move.
  int maxMovement();

  // Actions
  ///Make the unit move to the respective x and y location.
  int move(int x, int y);
  ///Attack another unit!.
  int attack(int unit);
  ///Put dirt in a hole!
  int fill(int tile);
  ///Build something!
  int build(int tile);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Unit ob);
};

}

#endif

