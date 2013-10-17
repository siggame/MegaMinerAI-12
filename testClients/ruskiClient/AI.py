#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import time
from time import sleep
import random
import game_utils
import path_find

class AI(BaseAI):

  history = None
  pf = None

  spawn_tiles = []

  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Ruski Malooski"

  @staticmethod
  def password():
    return "password"

  def get_spawn_tiles(self):
    for tile in self.tiles:
      if tile.owner == self.playerID:
        self.spawn_tiles.append(tile)

  def spawn_units(self):
    for tile in self.spawn_tiles:
      tile.spawn(random.choice([game_utils.DIGGER, game_utils.FILLER]))

  def move_units(self):
    for unit in self.units:
      if unit.owner == self.playerID:
        pf_tiles = self.pf.path_find( game_utils.get_tile(self, unit.x,unit.y), game_utils.get_tile(self, 4,5) )
        if pf_tiles is not None:
          print('CAN MOVE ({},{}) -> ({},{})'.format(unit.x, unit.y, 4, 5))
          for tile in pf_tiles:
            unit.move(tile)
        else:
          print('CANNOT MOVE ({},{}) -> ({},{})'.format(unit.x, unit.y, 4, 5))


  ##This function is called once, before your first turn
  def init(self):
    self.get_spawn_tiles()
    self.history = game_utils.game_history(self, True)

    self.pf = path_find.path_finder(self)
    return

  ##This function is called once, after your last turn
  def end(self):
    self.history.print_history()
    return


  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    print(self.turnNumber)
    #SNAPSHOT AT BEGINNING
    #self.history.save_snapshot()

    self.spawn_units()
    self.move_units()


    #SNAPSHOT AT END
    #self.history.save_snapshot()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
