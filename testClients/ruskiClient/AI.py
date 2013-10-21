#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import time
from time import sleep
import random
import game_utils
from game_utils import get_tile
import path_find


class AI(BaseAI):

  WAYTOOBIG = 100000

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
    self.spawn_tiles = [tile for tile in self.tiles if tile.owner == self.playerID]

  def spawn_units(self):
    for tile in self.spawn_tiles:
      tile.spawn(random.choice([game_utils.DIGGER, game_utils.FILLER]))

  def move_unit_to(self, unit, x, y):
    unit_tile = get_tile(self, unit.x, unit.y)
    if unit_tile is None:
      print('Unit {} ({},{}) does not have a corresponding tile.'.format(unit.id, unit.x, unit.y))
      return False

    goal_tile = get_tile(self, x, y)
    if goal_tile is None:
      print('Goal Tile ({},{}) does not have a corresponding tile.'.format(x, y))
      return False

    pf_tiles = self.pf.path_find(unit_tile, goal_tile)
    if pf_tiles is None or len(pf_tiles) <= 1:
      print('Cannot travel from ({},{}) to ({},{}).'.format(unit.x, unit.y, x, y))
      return False

    #Remove very beginning tile
    pf_tiles = pf_tiles[1:]

    for tile in pf_tiles:
      unit.move(tile.x, tile.y)

    return True

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

  @staticmethod
  def man_dist(x1, y1 ,x2, y2):
    return abs(x2-x1) + abs(y2-y1)

  def nearest_enemy_pump_tile(self, x, y):
    pump, dist = None, self.WAYTOOBIG
    for tile in self.tiles:
      if tile.owner != self.playerID and tile.pumpID != -1:
        cur_dist = self.man_dist(x, y, tile.x, tile.y)
        if cur_dist < dist:
          pump, dist = tile, cur_dist
    return pump
  def greedy_enemy_pump_tile(self):
    for tile in self.tiles:
      if tile.owner != self.playerID and tile.pumpID != -1:
        return tile
    return None

  def nearest_friendly_pump_tile(self, x, y):
    pump, dist = None, self.WAYTOOBIG
    for tile in self.tiles:
      if tile.owner == self.playerID and tile.pumpID != -1:
        cur_dist = self.man_dist(x, y, tile.x, tile.y)
        if cur_dist < dist:
          pump, dist = tile, cur_dist
    return pump
  def greedy_friendly_pump_tile(self):
    for tile in self.tiles:
      if tile.owner == self.playerID and tile.pumpID != -1:
        return tile
    return None

  def nearest_enemy_unit(self, x, y):
    enemy, dist = None, self.WAYTOOBIG
    for unit in self.units:
      if unit.owner != self.playerID:
        cur_dist = self.man_dist(x, y, unit.x, unit.y)
        if cur_dist < dist:
          enemy, dist = unit, cur_dist
    return enemy
  def greedy_enemy_unit(self):
    for unit in self.units:
      if unit.owner != self.playerID:
        return unit
    return None


  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    print(self.turnNumber)
    #SNAPSHOT AT BEGINNING
    #self.history.save_snapshot()
    print('START UPDATE')
    self.pf.update_obstacles()
    print('END UPDATE')
    self.spawn_units()

    for unit in self.units:
      if unit.owner == self.playerID:
        enemy_pump = self.nearest_enemy_pump_tile(unit.x, unit.y)
        if enemy_pump is not None:
          self.move_unit_to(unit, enemy_pump.x, enemy_pump.y)

    #SNAPSHOT AT END
    #self.history.save_snapshot()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
