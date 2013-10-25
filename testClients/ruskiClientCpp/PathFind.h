#ifndef RUSKI_PATHFIND_H
#define RUSKI_PATHFIND_H

#include "AI.h"
#include "Unit.h"
#include "Tile.h"

#include <vector>
#include <map>
#include <cmath>

// PROTOTYPES
class Coord;
class PathFinder;

typedef std::map<Coord, Tile*> CoordTileDict;
typedef std::vector<Tile*> TileList;


// COORD PROTOTYPE
class Coord
{
    int x, y;

    Coord();
    Coord(int t_x, int t_y)
}

//PATHFINDER PROTOTYPE
class PathFinder
{
public:
    AI* m_ai;
    CoordTileDict m_obstacles;

    PathFinder(AI* t_ai);
    Tile* getTile(int x, int y)
    TileList getNeighbors(Tile* tile)
    static int heuristic(Tile* start, Tile* end);
    TileList reconstructPath(CoordTileDict* parents, current);


}

// COORD DEFINITION
Coord::Coord()
{
    x = 0;
    y = 0;
}
Coord::Coord(int t_x, int t_y)
{
    x = t_x;
    y = t_y;
}

// PATHFINDER DEFINITION
PathFinder::PathFinder(AI* t_ai)
{
    m_ai = t_ai;
}

Tile* PathFinder::getTile(int x, int y)
{
    if(0 <= x && x < ai->mapWidth() && 0 <= y && y < ai->mapHeight())
        return ai->tiles[x * self.__ai.mapHeight + y];
    else
        return NULL;
}

TileList PathFinder::getNeighbors(Tile* tile)
{
    TileList neighbors;
    Tile* neighbor;
    int newx;
    int newy;
    int offsets[4][2] = {   {1,0},
                            {-1,0},
                            {0,1},
                            {0,-1}  };

    for(int i = 0; i < 4; i++)
        newx = tile->x() + offsets[i][0];
        newy = tile->y() + offsets[i][1];
        neighbor = getTile(newx, newy);
        if(neighbor == NULL)
            continue;
        else if(m_obstacle.find( Coord(newx, newy) ) != m_obstacle.end())
            continue;
        else
            neighbors.push_back(neighbor);
    }
}
int PathFinder::heuristic(Tile* start, Tile*, end)
{
    return abs(start->x() - end->x()) + abs(start->y() - end->y());
}

TileList PathFinder::reconstructPath(CoordTileDict* parents, current)
{
    if parents->find(current)
}

##endif

/*
import heapq
import GameObject

class path_finder:
  def __init__(self, ai):
    self.__ai = ai
    self.__obst = dict()

  def update_obstacles(self):
    for unit in self.__ai.units:
      self.__obst[(unit.x, unit.y)] = unit

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
      if neighbor is None:
        continue
      if (neighbor.x, neighbor.y) in self.__obst:
        continue
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
        if f_scores[current] > 100:
          print('PARTIAL PATH')
          return self.__reconstruct_path(parents, current)

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
*/
