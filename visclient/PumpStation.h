// -*-c++-*-

#ifndef PUMPSTATION_H
#define PUMPSTATION_H

#include <iostream>
#include "vc_structures.h"


namespace client
{


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
  ///The length of time it takes to capture the PumpStation.
  int seigeCount();

  // Actions

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, PumpStation ob);
};

}

#endif

