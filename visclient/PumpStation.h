// -*-c++-*-

#ifndef PUMPSTATION_H
#define PUMPSTATION_H

#include <iostream>
#include "vc_structures.h"


namespace client
{


///Represents a base to which you want to lead water.
class PumpStation {
  public:
  void* ptr;
  PumpStation(_PumpStation* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///The owner of the PumpStation.
  int owner();
  ///The amount of water the PumpStation pumps.
  int waterAmount();
  ///The amount the PumpStation has been sieged.
  int siegeAmount();

  // Actions

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, PumpStation ob);
};

}

#endif

