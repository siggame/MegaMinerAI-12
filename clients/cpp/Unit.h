// -*-c++-*-

#ifndef UNIT_H
#define UNIT_H

#include <iostream>
#include "structures.h"

#include "Mappable.h"
class Unit;
class Tile;

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
  ///The type of this unit. This type refers to list of UnitTypes.
  int type();
  ///Whether current unit has attacked or not.
  int hasAttacked();
  ///Whether the current unit has dug or not.
  int hasDug();
  ///Whether the current unit has filled or not.
  int hasFilled();
  ///The current amount health this unit has remaining.
  int healthLeft();
  ///The maximum amount of this health this unit can have
  int maxHealth();
  ///The number of moves this unit has remaining.
  int movementLeft();
  ///The maximum number of moves this unit can move.
  int maxMovement();
  ///The range of this unit's attack.
  int range();
  ///The power of the unit's offensive siege ability.
  int offensePower();
  ///The power of the unit's defensive siege ability.
  int defensePower();
  ///The power of this unit types's digging ability.
  int digPower();
  ///The power of this unit type's filling ability.
  int fillPower();
  ///The power of this unit type's attack.
  int attackPower();

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

