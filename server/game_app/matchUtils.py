from functools import wraps
import heapq

def verifyReferences(self, expression, references):
  for i in range(0, len(references)):
    if references[i] is not None:
      if expression[i] not in self.objects:
        return str(expression[i]) + " does not exist"
      if not isinstance(self.objects[expression[i]], references[i]):
        return str(expression[i]) + " does not reference a " + references[i].__name__
  return True


def requireReferences(*n):
  def dec(f):
    @wraps(f)
    def wrapper(self, *expression):
      errMsg = verifyReferences(self, expression, n)
      if not (errMsg == True):
        return errMsg
      return f(self, *expression)
    return wrapper
  return dec

def deref(self, type, id):
  if type is None:
    return id
  if id not in self.objects:
    raise LookupError(str(id) + " does not exist")
  if not isinstance(self.objects[id], type):
    raise LookupError(str(id) + " does not reference a " + type.__name__)
  return self.objects[id]

def derefArgs(*types):
  def dec(f):
    @wraps(f)
    def wrapper(self, *values):
      try:
        args = [deref(self, i, j) for i, j in zip(types, values)]
      except LookupError as e:
        return e.message
      else:
        return f(self, *args)
    return wrapper
  return dec

def aStar(self, start, goal, validTile):
  offsets = [(1,0),(0,1),(-1,0),(0,-1)]

  closed_set = set()
  open_set = set()
  open_heap = []

  g_scores = dict()
  f_scores = dict()
  parents = dict()

  g_scores[start] = 0
  f_scores[start] = g_scores[start] + (abs(goal.x - start.x) + abs(goal.y - start.y))

  heapq.heappush(open_heap, (f_scores[start], start))
  while open_heap:
    f_score, current = heapq.heappop(open_heap)
    if current == goal:
      path = [current]
      while current in parents:
        current = parents[current]
        path.append(current)
      path.reverse()
      return path
    closed_set.add(current)
    for offset in offsets:
      neighbor = self.getTile(current.x + offset[0], current.y + offset[1])
      if neighbor is not None and validTile(neighbor):
        ten_g_score = g_scores[current] + 1
        ten_f_score = ten_g_score + abs(neighbor.x - goal.x) + abs(neighbor.y - goal.y)
        if neighbor not in closed_set or ten_f_score < f_scores[neighbor]:
          parents[neighbor] = current
          g_scores[neighbor] = ten_g_score
          f_scores[neighbor] = ten_f_score
          if (f_scores[neighbor], neighbor) not in open_set:
            heapq.heappush(open_heap, (f_scores[neighbor], neighbor))
            open_set.add(neighbor)
  return None
