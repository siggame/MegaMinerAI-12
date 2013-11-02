#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import time
from time import sleep
import random
import game_utils
from game_utils import get_tile
import path_find
import object_cache


class AI(BaseAI):
  WORKER, SCOUT, TANK = range(3)

  WAYTOOBIG = 100000

  pf = None
  cache = None


  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Ruski Malooski"

  @staticmethod
  def password():
    return "password"

  def spawn_units(self):
    types = [0,1,2]
    for tile in self.cache.my_pump_tiles.values():
      tile.spawn(random.choice(types))
    for tile in self.cache.my_spawn_tiles.values():
      tile.spawn(random.choice(types))
    return True

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
    self.cache = object_cache.object_cache(self)
    self.pf = path_find.path_finder(self, self.cache)
    return

  ##This function is called once, after your last turn
  def end(self):
    return

  @staticmethod
  def man_dist(x1, y1 ,x2, y2):
    return abs(x2-x1) + abs(y2-y1)

  def nearest_enemy_pump_tile(self, x, y):
    min_dist, min_enemy = self.WAYTOOBIG, None
    for cur_enemy in self.cache.enemy_pump_tiles.values():
      cur_dist = self.man_dist(x, y, cur_enemy.x, cur_enemy.y)
      if cur_dist < min_dist:
        min_dist, min_enemy = cur_dist, cur_enemy
    return min_enemy

  def nearest_friendly_pump_tile(self, x, y):
    min_dist, min_friendly = self.WAYTOOBIG, None
    for cur_friendly in self.cache.my_pump_tiles.values():
      cur_dist = self.man_dist(x, y, cur_friendly.x, cur_friendly.y)
      if cur_dist < min_dist:
        min_dist, min_friendly = cur_dist, cur_friendly
    return min_friendly

  def nearest_ice_tile(self, x, y):
    min_dist, min_ice = self.WAYTOOBIG, None
    for cur_ice in self.cache.enemy_units.values():
      cur_dist = self.man_dist(x, y, cur_ice.x, cur_ice.y)
      if cur_dist < min_dist:
        min_dist, min_ice = cur_dist, cur_ice
    return min_ice

  def nearest_enemy_unit(self, x, y):
    min_dist, min_enemy = self.WAYTOOBIG, None
    for cur_enemy in self.cache.enemy_units.values():
      cur_dist = self.man_dist(x, y, cur_enemy.x, cur_enemy.y)
      if cur_dist < min_dist:
        min_dist, min_enemy = cur_dist, cur_enemy
    return min_enemy

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    print('Turn Number: {}'.format(self.turnNumber))
    print('Water Stored: P1: {} || P2: {}'.format(self.players[0].waterStored, self.players[1].waterStored))
    print('Oxygen: P1: {} || P2: {}'.format(self.players[0].oxygen, self.players[1].oxygen))
    self.cache.update_all()
    self.spawn_units()

    for unit in self.cache.my_units.values():
      if unit.type == self.SCOUT:
        enemy_pump = self.nearest_enemy_pump_tile(unit.x, unit.y)
        if enemy_pump is not None:
          self.move_unit_to(unit, enemy_pump.x, enemy_pump.y)

        #ATTEMPT TO ATTACK
        enemy_unit = self.nearest_enemy_unit(unit.x, unit.y)
        if enemy_unit is not None:
          if self.man_dist(unit.x, unit.y, enemy_unit.x, enemy_unit.y) <= unit.range:
            unit.attack(enemy_unit)

      elif unit.type == self.TANK:
        friendly_pump = self.nearest_friendly_pump_tile(unit.x, unit.y)
        if friendly_pump is not None:
          self.move_unit_to(unit, friendly_pump.x, friendly_pump.y)

        #ATTEMPT TO ATTACK
        enemy_unit = self.nearest_enemy_unit(unit.x, unit.y)
        if enemy_unit is not None:
          if self.man_dist(unit.x, unit.y, enemy_unit.x, enemy_unit.y) <= unit.range:
            unit.attack(enemy_unit)

      elif unit.type == self.WORKER:
        #friendly_pump = self.nearest_friendly_pump_tile(unit.x, unit.y)
        #ice_tile = self.nearest_ice_tile(unit.x, unit.y)
        pass


    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
