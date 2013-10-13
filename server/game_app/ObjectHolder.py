import objects

class ObjectHolder(dict):
  def __init__(self, *args, **kwargs):
    dict.__init__(self, *args, **kwargs)
    self.players = []
    self.pumpStations = []
    self.mappables = []
    self.units = []
    self.tiles = []

  def __setitem__(self, key, value):
    if key in self:
      self.__delitem__(key)
    dict.__setitem__(self, key, value)
    if isinstance(value, objects.Player):
      self.players.append(value)
    if isinstance(value, objects.PumpStation):
      self.pumpStations.append(value)
    if isinstance(value, objects.Mappable):
      self.mappables.append(value)
    if isinstance(value, objects.Unit):
      self.units.append(value)
    if isinstance(value, objects.Tile):
      self.tiles.append(value)

  def __delitem__(self, key):
    value = self[key]
    dict.__delitem__(self, key)
    if value in self.players:
      self.players.remove(value)
    if value in self.pumpStations:
      self.pumpStations.remove(value)
    if value in self.mappables:
      self.mappables.remove(value)
    if value in self.units:
      self.units.remove(value)
    if value in self.tiles:
      self.tiles.remove(value)

  def clear(self):
    for i in self.keys():
      del self[i]
