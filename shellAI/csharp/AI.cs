using System;
using System.Runtime.InteropServices;

///The class implementing gameplay logic.
class AI : BaseAI
{
  // Enum for types of units you can spawn.
  enum Types { Worker, Scout, Tank };

  public override string username()
  {
    return "Shell AI";
  }
  public override string password()
  {
    return "password";
  }

  //This function is called each time it is your turn
  //Return true to end your turn, return false to ask the server for updated information
  public override bool run()
  {
    int numberOfUnits = 0;

    // Get the number of units owned.
    for(int i = 0; i < units.Length; i++)
      if(units[i].Owner == playerID())
        numberOfUnits++;

    // Look for tiles I own.
    for(int i = 0; i < tiles.Length; i++)
    {
      // If this tile is my spawn tile or my pump station...
      if(tiles[i].Owner == playerID())
      {
        // Get the unit cost for a worker.
        int cost = Int32.MaxValue;
        for(int j = 0; j < unitTypes.Length; j++)
          if(unitTypes[j].Type == (int)Types.Worker)
            cost = unitTypes[j].Cost;

        // If there is enough oxygen to spawn the unit...
        if(players[playerID()].Oxygen >= cost)
        {
          // ...and if we can spawn more units...
          if(numberOfUnits < maxUnits())
          {
            // ...and nothing is spwning on the tile...
            if(!tiles[i].IsSpawning)
            {
              bool canSpawn = true;

              // If it's a pump station and it's not being seiged...
              if(tiles[i].PumpID != -1)
              {
                // ...find the pump in the vector.
                for(int j = 0; j < pumpStations.Length; j++)
                {
                  // If it's being sieged, don't spawn.
                  if(pumpStations[j].Id == tiles[i].PumpID && pumpStations[j].SiegeAmount > 0)
                    canSpawn = false;
                }
              }

              // If there is someone else on the tile, don't spawn.
              for(int j = 0; j < units.Length; j++)
                if(tiles[i].X == units[j].X && tiles[i].Y == units[j].Y)
                  canSpawn = false;

              // If possible, spawn!
              if(canSpawn)
              {
                tiles[i].spawn((int)Types.Worker);
                numberOfUnits++;
              }
            }
          }
        }
      }
    }

    int moveDelta = 0;

    // Set to move left or right based on ID; towards the center.
    moveDelta = playerID() == 0 ? 1 : -1;

    // Do some stuff for each unit.
    for(int i = 0; i < units.Length; i++)
    {
      // If you don't own the unit, ignore it.
      if(units[i].Owner != playerID())
        continue;

      // Try to move to the right or left movement times.
      for(int z = 0; z < units[i].MaxMovement; z++)
      {
        bool canMove = true;

        // If there's a unit there, don't move.
        for(int j = 0; j < units.Length; j++)
        {
          if(units[i].X + moveDelta == units[j].X && units[i].Y == units[j].Y)
            canMove = false;
        }

        // If nothing is there, and it's not moving off the edge of the map...
        if(canMove && units[i].X + moveDelta >= 0 && units[i].X + moveDelta < mapWidth())
        {
          // If the tile is not an enemy spawn point...
          if(!(tiles[(units[i].X + moveDelta) * mapHeight() + units[i].Y].PumpID == -1 &&
            tiles[(units[i].X + moveDelta) * mapHeight() + units[i].Y].Owner == 1 - playerID()) ||
            tiles[(units[i].X + moveDelta) * mapHeight() + units[i].Y].Owner == 2)
          {
            // If the tile is not an ice tile...
            if(!(tiles[(units[i].X + moveDelta) * mapHeight() + units[i].Y].Owner == 3 &&
              tiles[(units[i].X + moveDelta) * mapHeight() + units[i].Y].WaterAmount > 0))
            {
              // If the tile is not spawning anything...
              if(!(tiles[(units[i].X + moveDelta) * mapHeight() + units[i].Y].IsSpawning))
              {
                // If the unit is alive...
                if(units[i].HealthLeft > 0)
                {
                  // Move the unit!
                  units[i].move(units[i].X + moveDelta, units[i].Y);
                }
              }
            }
          }
        }
      }

      // If there's an enemy in the movement direction and the unit hasn't attacked and is alive.
      if(!units[i].HasAttacked && units[i].HealthLeft > 0)
      {
        for(int j = 0; j < units.Length; j++)
        {
          // Check if there is a enemy unit in the direction.
          if(units[i].X + moveDelta == units[j].X && units[i].Y == units[j].Y &&
            units[j].Owner != playerID())
          {
            // Attack it!
            units[i].attack(units[j]);
            break;
          }
        }
      }

      // If there's a space to dig below the unit and the unit hasn't dug, and the unit is alive.
      if(units[i].Y != mapHeight() - 1 &&
        tiles[units[i].X * mapHeight() + units[i].Y + 1].PumpID == -1 &&
        tiles[units[i].X * mapHeight() + units[i].Y + 1].Owner == 2 &&
        units[i].HasDug == false &&
        units[i].HealthLeft > 0)
      {
        bool canDig = true;

        // Make sure there's no unit on that tile.
        for(int j = 0; j < units.Length; j++)
          if(units[i].X == units[j].X && units[i].Y + 1 == units[j].Y)
            canDig = false;

        // Make sure the tile is not an ice tile.
        if(canDig && !(tiles[units[i].X * mapHeight() + units[i].Y + 1].Owner == 3 &&
          tiles[units[i].X * mapHeight() + units[i].Y + 1].WaterAmount > 0))
        {
          units[i].dig(tiles[units[i].X * mapHeight() + units[i].Y + 1]);
        }
      }
    }

    return true;
  }

  //This function is called once, before your first turn
  public override void init() {}

  //This function is called once, after your last turn
  public override void end() {}
  
  
  public AI(IntPtr c) : base(c)
  {}
}
