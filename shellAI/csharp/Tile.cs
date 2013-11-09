using System;
using System.Runtime.InteropServices;


///Represents a single tile on the map, can contain some amount of water.
public class Tile: Mappable
{

  public Tile()
  {
  }

  public Tile(IntPtr p)
  {
    ptr = p;
    ID = Client.tileGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public override bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.tiles.Length; i++)
    {
      if(BaseAI.tiles[i].ID == ID)
      {
        ptr = BaseAI.tiles[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }

    //commands

  ///Attempt to spawn a unit of a type on this tile.
  public bool spawn(int type)
  {
    validify();
    return (Client.tileSpawn(ptr, type) == 0) ? false : true;
  }

    //getters


  ///Unique Identifier
  public new int Id
  {
    get
    {
      validify();
      int value = Client.tileGetId(ptr);
      return value;
    }
  }

  ///X position of the object
  public new int X
  {
    get
    {
      validify();
      int value = Client.tileGetX(ptr);
      return value;
    }
  }

  ///Y position of the object
  public new int Y
  {
    get
    {
      validify();
      int value = Client.tileGetY(ptr);
      return value;
    }
  }

  ///The owner of the tile.
  public int Owner
  {
    get
    {
      validify();
      int value = Client.tileGetOwner(ptr);
      return value;
    }
  }

  ///Determines if this tile is a part of a Pump Station.
  public int PumpID
  {
    get
    {
      validify();
      int value = Client.tileGetPumpID(ptr);
      return value;
    }
  }

  ///The amount of water contained on the tile.
  public int WaterAmount
  {
    get
    {
      validify();
      int value = Client.tileGetWaterAmount(ptr);
      return value;
    }
  }

  ///The depth of the tile. Tile is a trench if depth is greater than zero.
  public int Depth
  {
    get
    {
      validify();
      int value = Client.tileGetDepth(ptr);
      return value;
    }
  }

  ///The number of turns until sediment is deposited on this tile.
  public int TurnsUntilDeposit
  {
    get
    {
      validify();
      int value = Client.tileGetTurnsUntilDeposit(ptr);
      return value;
    }
  }

  ///Determines if this tile is attempting to spawn something or not.
  public bool IsSpawning
  {
    get
    {
      validify();
      int value = Client.tileGetIsSpawning(ptr);
      return value == 1;
    }
  }

}

