import heapq
import GameObject

class path_finder:
  def __init__(self, ai):
    self.__ai = ai

    self.__obstacles = dict()

  def refresh_obstacles(self):
    self.__obstacles = dict()

    #ICE
    for unit in self.__ai.units:
      self.__obstacles[(unit.x, unit.y)] = unit

    for tile in self.__ai.tiles:
      if tile.owner == 3 and tile.waterAmount > 0:
        self.__obstacles[(tile.x, tile.y)] = tile



  def __get_tile(self, x, y):
    if (0 <= x < self.__ai.mapWidth) and (0 <= y < self.__ai.mapHeight):
      return self.__ai.tiles[x * self.__ai.mapHeight + y]
    else:
      return None

  def __get_neighbors(self, tile):
    neighbors = []
    offsets = [(0,1),(1,0),(0,-1),(-1,0)]
    for offset in offsets:
      neighbor = self.__get_tile(tile.x+offset[0], tile.y+offset[1])
      if neighbor is not None and (neighbor.x, neighbor.y) not in self.__obstacles.keys():
        neighbors.append(neighbor)

    return neighbors

  @staticmethod
  def __heuristic(start, goal):
    return abs(start.x-goal.x) + abs(start.y-goal.y)

  def __reconstruct_path(self, parents, node):
    if node in parents.keys():
      p = self.__reconstruct_path(parents, parents[node])
      p.append(node)
      return p
    else:
      p = [node]
      return p

  def path_find(self, start, goal):
    print('START ({},{})'.format(start.x, start.y))
    print('GOAL ({},{})'.format(goal.x, goal.y))

    closed_set = []
    open_set = []
    #came_from := the empty map    // The map of navigated nodes.
    g_scores = dict()
    f_scores = dict()
    parents = dict()

    g_scores[start] = 0
    f_scores[start] = g_scores[start] + self.__heuristic(start, goal)

    heapq.heappush(open_set, (f_scores[start], start))

    while len(open_set) > 0:
      f_score, current = heapq.heappop(open_set)

      if current == goal:
        print('PATH FOUND')
        return self.__reconstruct_path(parents, current)

      closed_set.append(current)

      for neighbor in self.__get_neighbors(current):
        ten_g_score = g_scores[current] + 1
        ten_f_score = ten_g_score + self.__heuristic(neighbor, goal)
        if neighbor in closed_set and ten_f_score >= f_scores[neighbor]:
          continue

        if neighbor not in closed_set or ten_f_score < f_scores[neighbor]:
          parents[neighbor] = current
          g_scores[neighbor] = ten_g_score
          f_scores[neighbor] = ten_f_score

          if (f_scores[neighbor], neighbor) not in open_set:
            heapq.heappush(open_set, (f_scores[neighbor], neighbor))

    print('NO PATH FOUND')
    return None