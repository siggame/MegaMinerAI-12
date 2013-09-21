// -*-c++-*-

#ifndef PLAYER_H
#define PLAYER_H

#include <iostream>
#include "vc_structures.h"


namespace client
{


class Player {
  public:
  void* ptr;
  Player(_Player* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///Player's Name
  char* playerName();
  ///Time remaining, updated at start of turn
  float time();
  ///The amount of water a player has.
  int waterStored();
  ///The speed at which a player can spawn units.
  int spawnRate();

  // Actions
  ///Allows a player to display messages on the screen
  int talk(char* message);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Player ob);
};

}

#endif

