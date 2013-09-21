using System;
using System.Runtime.InteropServices;


///Represents a single unit on the map.
public class Unit: Mappable
{

  public Unit()
  {
  }

  public Unit(IntPtr p)
  {
    ptr = p;
    ID = Client.unitGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public override bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.units.Length; i++)
    {
      if(BaseAI.units[i].ID == ID)
      {
        ptr = BaseAI.units[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }

    //commands

  ///Make the unit move to the respective x and y location.
  public bool move(int x, int y)
  {
    validify();
    return (Client.unitMove(ptr, x, y) == 0) ? false : true;
  }
  ///Attack another unit!.
  public bool attack(int unit)
  {
    validify();
    return (Client.unitAttack(ptr, unit) == 0) ? false : true;
  }
  ///Put dirt in a hole!
  public bool fill(int tile)
  {
    validify();
    return (Client.unitFill(ptr, tile) == 0) ? false : true;
  }
  ///Build something!
  public bool build(int tile)
  {
    validify();
    return (Client.unitBuild(ptr, tile) == 0) ? false : true;
  }

    //getters


  ///Unique Identifier
  public new int Id
  {
    get
    {
      validify();
      int value = Client.unitGetId(ptr);
      return value;
    }
  }

  ///X position of the object
  public new int X
  {
    get
    {
      validify();
      int value = Client.unitGetX(ptr);
      return value;
    }
  }

  ///Y position of the object
  public new int Y
  {
    get
    {
      validify();
      int value = Client.unitGetY(ptr);
      return value;
    }
  }

  ///The owner of this unit.
  public int Owner
  {
    get
    {
      validify();
      int value = Client.unitGetOwner(ptr);
      return value;
    }
  }

  ///The maximum number of moves this unit can move.
  public int Type
  {
    get
    {
      validify();
      int value = Client.unitGetType(ptr);
      return value;
    }
  }

  ///The current amount health this unit has remaining.
  public int CurHealth
  {
    get
    {
      validify();
      int value = Client.unitGetCurHealth(ptr);
      return value;
    }
  }

  ///The number of moves this unit has remaining.
  public int CurMovement
  {
    get
    {
      validify();
      int value = Client.unitGetCurMovement(ptr);
      return value;
    }
  }

  ///The maximum number of moves this unit can move.
  public int MaxMovement
  {
    get
    {
      validify();
      int value = Client.unitGetMaxMovement(ptr);
      return value;
    }
  }

}

