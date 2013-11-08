
class object_cache:

  def __init__(self, ai):
    self.ai = ai

    self.my_pump_tiles = dict()
    self.enemy_pump_tiles = dict()

    self.my_spawn_tiles = dict()
    self.enemy_spawn_tiles = dict()

    self.dry_trenches = dict()
    self.wet_trenches = dict()

    self.ice = dict()

    self.my_units = dict()
    self.enemy_units = dict()

  def update_all(self):
    self.update_tiles()
    self.update_units()

  def update_units(self):
    self.my_units = dict()
    self.enemy_units = dict()

    for unit in self.ai.units:
      if unit.owner == self.ai.playerID:
        self.my_units[(unit.x, unit.y)] = unit
      elif unit.owner == self.ai.playerID^1:
        self.enemy_units[(unit.x, unit.y)] = unit

    return True


  def update_tiles(self):
    self.my_pump_tiles = dict()
    self.enemy_pump_tiles = dict()

    self.dry_trenches = dict()
    self.wet_trenches = dict()

    self.ice = dict()

    self.my_spawn_tiles = dict()
    self.enemy_spawn_tiles = dict()

    for tile in self.ai.tiles:
      #IF A PUMP
      if tile.pumpID != -1:
        if tile.owner == self.ai.playerID:
          self.my_pump_tiles[(tile.x, tile.y)] = tile
        elif tile.owner == self.ai.playerID^1:
          self.enemy_pump_tiles[(tile.x, tile.y)] = tile

      #IF NOT A PUMP
      else:
        #IF A SPAWN
        if tile.owner == self.ai.playerID:
          self.my_spawn_tiles[(tile.x, tile.y)] = tile
        elif tile.owner == self.ai.playerID^1:
          self.enemy_spawn_tiles[(tile.x, tile.y)] = tile

        #NOT A SPAWN
        else:
          #IF TRENCH/WATER
          if tile.depth > 0:
            if tile.waterAmount > 0:
              self.wet_trenches[(tile.x, tile.y)] = tile
            elif tile.waterAmount <= 0:
              self.dry_trenches[(tile.x, tile.y)] = tile
          #NOT TRENCH/WATER
          else:
            if tile.owner == 3 and tile.waterAmount > 0:
              self.ice[(tile.x, tile.y)] = tile
    return True




