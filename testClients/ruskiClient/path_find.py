import heapq
import GameObject

class path_finder:
  def __init__(self, ai):
    self.__ai = ai
    self.__get_all_neighbors()

    GameObject.Tile.__neighbors = []
    GameObject.Tile.__parent = None
    GameObject.Tile.__g_score = 0
    GameObject.Tile.__f_score = 0

  def __get_tile(self, x, y):
    if (0 <= x < self.__ai.mapWidth) and (0 <= y < self.__ai.mapHeight):
      return self.__ai.tiles[x * self.__ai.mapHeight + y]
    else:
      return None

  def __get_all_neighbors(self):
    offsets = [(0,1),(0,-1),(1,0),(-1,0)]

    for tile in self.__ai.tiles:
      tile.__neighbors = []
      tile.__parent = None
      tile.__g_score = 0
      tile.__f_score = 0

    for tile in self.__ai.tiles:
      for offset in offsets:
        nx = tile.x + offset[0]
        ny = tile.y + offset[1]
        neighbor = self.__get_tile(nx, ny)
        if neighbor is not None:
          tile.__neighbors.append(neighbor)

    return

  @staticmethod
  def __heuristic(start, goal):
    return abs(start.x-goal.x) + abs(start.y-goal.y)

  def __print_tile_scores(self):
    for y in range(self.__ai.mapHeight):
      for x in range(self.__ai.mapWidth):
        score = self.__get_tile(x, y).__cost
        if score == 0 or score is None:
          print(' ')
        else:
          print(score)
      print


  def path_find(self, start, goal):
    print('START ({},{})'.format(start.x, start.y))
    print('GOAL ({},{})'.format(goal.x, goal.y))

    closed_set = []
    open_set = []
    #came_from := the empty map    // The map of navigated nodes.

    start.__g_score = 0
    start.__f_score = start.__g_score + self.__heuristic(start, goal)

    heapq.heappush(open_set, (start.__f_score, start))

    while len(open_set) > 0:
      print('OPEN_SET LENGTH: {}'.format(len(open_set)))
      f_score, current = heapq.heappop(open_set)

      print('CURRENT: ({},{})'.format(current.x, current.y))

      if current == goal:
        print('PATH FOUND')
        return current

      closed_set.append(current)

      for neighbor in current.__neighbors:
        ten_g_score = current.__g_score + 1
        ten_f_score = ten_g_score + self.__heuristic(neighbor, goal)

        if neighbor in closed_set and ten_f_score >= neighbor.__f_score:
          continue

        if neighbor not in closed_set or ten_f_score < neighbor.__f_score:
          neighbor.__parent = current
          neighbor.__g_score = ten_g_score
          neighbor.__f_score = ten_f_score

          if (neighbor.__f_score, neighbor) not in open_set:
            heapq.heappush(open_set, (neighbor.__f_score, neighbor))

    print('NO PATH FOUND')
    return None