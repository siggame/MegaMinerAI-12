import objects

class ObjectHolder(dict):
  def __init__(self, *args, **kwargs):
    dict.__init__(self, *args, **kwargs)
    self.players = []
    self.mappables = []
    self.pumpStations = []
    self.units = []
    self.tiles = []
    self.unitTypes = []

  def __setitem__(self, key, value):
    if key in self:
      self.__delitem__(key)
    dict.__setitem__(self, key, value)
    if isinstance(value, objects.Player):
      self.players.append(value)
    if isinstance(value, objects.Mappable):
      self.mappables.append(value)
    if isinstance(value, objects.PumpStation):
      self.pumpStations.append(value)
    if isinstance(value, objects.Unit):
      self.units.append(value)
    if isinstance(value, objects.Tile):
      self.tiles.append(value)
    if isinstance(value, objects.UnitType):
      self.unitTypes.append(value)

  def __delitem__(self, key):
    value = self[key]
    dict.__delitem__(self, key)
    if value in self.players:
      self.players.remove(value)
    if value in self.mappables:
      self.mappables.remove(value)
    if value in self.pumpStations:
      self.pumpStations.remove(value)
    if value in self.units:
      self.units.remove(value)
    if value in self.tiles:
      self.tiles.remove(value)
    if value in self.unitTypes:
      self.unitTypes.remove(value)

  def clear(self):
    for i in self.keys():
      del self[i]
