// -*-c++-*-

#ifndef UNITTYPE_H
#define UNITTYPE_H

#include <iostream>
#include "structures.h"


///Represents type of unit.
class UnitType {
  public:
  void* ptr;
  UnitType(_UnitType* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///The name of this type of unit.
  char* name();
  ///The UnitType specific id representing this type of unit.
  int type();
  ///The oxygen cost to spawn this unit type into the game.
  int cost();
  ///The power of the attack of this type of unit.
  int attackPower();
  ///The power of this unit types's digging ability.
  int digPower();
  ///The power of this unit type's filling ability.
  int fillPower();
  ///The maximum amount of this health this unit can have
  int maxHealth();
  ///The maximum number of moves this unit can move.
  int maxMovement();
  ///The power of the unit type's offensive siege ability.
  int offensePower();
  ///The power of the unit type's defensive siege ability.
  int defensePower();
  ///The range of the unit type's attack.
  int range();

  // Actions

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, UnitType ob);
};

#endif

