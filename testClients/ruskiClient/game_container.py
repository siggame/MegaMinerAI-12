class game_container:
  ICEOWNER = 3

  def __init__(self, ai):
    self.__ai = ai

    self.my_spawnable_tiles = dict()
    self.enemy_spawnable_tiles = dict()
    self.my_units = dict()
    self.enemy_units = dict()
    self.ice_tiles = dict()
    self.my_pumpstations = dict()
    self.my_pumptiles = dict()
    self.enemy_pumpstations = dict()
    self.enemy_pumptiles = dict()

  def update_pumpstations(self):
    for pumpstation in self.__ai.pumpStations:
      if pumpstation.owner == self.__ai.playerID:
        self.my_pumpstations[pumpstation.id] = pumpstation
      else:
        self.enemy_pumpstations[pumpstation.id] = pumpstation

  def update_tiles(self):
    self.my_spawnable_tiles = dict()
    self.ice_tiles = dict()
    self.my_pumptiles = dict()
    self.enemy_pumptiles = dict()

    for tile in self.__ai.tiles:
      if tile.owner == self.__ai.playerID:
        if tile.pumpID != -1:
          self.my_pumptiles[(tile.x, tile.y)] = tile
        else:
          self.my_spawnable_tiles[(tile.x, tile.y)] = tile
      elif tile.owner == self.__ai.playerID^1:
        if tile.pumpID != -1:
          self.enemy_pumptiles[(tile.x, tile.y)] = tile
        else:
          self.enemy_spawnable_tiles[(tile.x, tile.y)] = tile
      elif tile.owner == self.ICEOWNER and tile.waterAmount > 0:
        self.ice_tiles[(tile.x, tile.y)] = tile

  def update_units(self):
    self.my_units = dict()
    self.enemy_units = dict()
    for unit in self.__ai.units:
      if unit.owner == self.__ai.playerID:
        self.my_units[(unit.x, unit.y)] = unit
      else:
        self.enemy_units[(unit.x, unit.y)] = unit
    return