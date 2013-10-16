import heapq

class path_finder:
  def __init__(self, ai):
    self.__ai = ai
    self.__get_all_neighbors()

  def __get_tile(self, x, y):
    if (0 <= x < self.__ai.mapWidth) and (0 <= y < self.__ai.mapHeight):
      return self.__ai.tiles[x * self.__ai.mapHeight + y]
    else:
      return None

  def __get_all_neighbors(self):
    offsets = [(0,1),(0,-1),(1,0),(-1,0)]

    for tile in self.__ai.tiles:
      tile.__neighbors = []

    for tile in self.__ai.tiles:
      for offset in offsets:
        neighbor = self.__get_tile(tile.x+offset[0], tile.y+offset[1])
        if neighbor is not None:
          tile.__neighbors.append(neighbor)

    return

  @staticmethod
  def __heuristic(start, goal):
    return abs(start.x-goal.x) + abs(start.y-goal.y)

  @staticmethod
  def __node_to_list(node, start):
    path = [node]
    while node != start:
      node = node.__parent
      path.append(node)

    path.reverse()
    return path

  def path_find(self, start, goal):
    closed = []
    open_set = []

    start.__cost = 0
    start.__parent = None

    heapq.heappush( open_set, (self.__heuristic(start, goal), start) )

    while len(open_set) > 0:
      priority, node = heapq.heappop(open_set)

      if node == goal:
        print('GOAL REACHED')
        return self.__node_to_list(node, start)

      for neighbor in node.__neighbors:
        if neighbor in closed:
          continue
        neighbor.__parent = node
        neighbor.__cost = node.__cost + 1
        closed.append(neighbor)
        heapq.heappush(open_set, (self.__heuristic(neighbor, goal) + neighbor.__cost, neighbor))

    return None