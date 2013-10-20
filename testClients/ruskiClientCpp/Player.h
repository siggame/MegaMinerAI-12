// -*-c++-*-

#ifndef PLAYER_H
#define PLAYER_H

#include <iostream>
#include "structures.h"


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
  ///Resource used to spawn in units.
  int oxygen();
  ///The player's oxygen cap.
  int maxOxygen();

  // Actions
  ///Allows a player to display messages on the screen
  bool talk(char* message);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Player ob);
};

#endif

