// -*-c++-*-

#include "Player.h"
#include "game.h"


Player::Player(_Player* pointer)
{
    ptr = (void*) pointer;
}

int Player::id()
{
  return ((_Player*)ptr)->id;
}

char* Player::playerName()
{
  return ((_Player*)ptr)->playerName;
}

float Player::time()
{
  return ((_Player*)ptr)->time;
}

int Player::waterStored()
{
  return ((_Player*)ptr)->waterStored;
}

int Player::oxygen()
{
  return ((_Player*)ptr)->oxygen;
}

int Player::maxOxygen()
{
  return ((_Player*)ptr)->maxOxygen;
}


bool Player::talk(char* message)
{
  return playerTalk( (_Player*)ptr, message);
}



std::ostream& operator<<(std::ostream& stream,Player ob)
{
  stream << "id: " << ((_Player*)ob.ptr)->id  <<'\n';
  stream << "playerName: " << ((_Player*)ob.ptr)->playerName  <<'\n';
  stream << "time: " << ((_Player*)ob.ptr)->time  <<'\n';
  stream << "waterStored: " << ((_Player*)ob.ptr)->waterStored  <<'\n';
  stream << "oxygen: " << ((_Player*)ob.ptr)->oxygen  <<'\n';
  stream << "maxOxygen: " << ((_Player*)ob.ptr)->maxOxygen  <<'\n';
  return stream;
}
