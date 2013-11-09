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
  ///Put dirt in a hole!
  public bool fill(Tile tile)
  {
    validify();
    tile.validify();
    return (Client.unitFill(ptr, tile.ptr) == 0) ? false : true;
  }
  ///Dig out a tile
  public bool dig(Tile tile)
  {
    validify();
    tile.validify();
    return (Client.unitDig(ptr, tile.ptr) == 0) ? false : true;
  }
  ///Command to attack another Unit.
  public bool attack(Unit target)
  {
    validify();
    target.validify();
    return (Client.unitAttack(ptr, target.ptr) == 0) ? false : true;
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

  ///The type of this unit. This type refers to list of UnitTypes.
  public int Type
  {
    get
    {
      validify();
      int value = Client.unitGetType(ptr);
      return value;
    }
  }

  ///Whether current unit has attacked or not.
  public bool HasAttacked
  {
    get
    {
      validify();
      int value = Client.unitGetHasAttacked(ptr);
      return value == 1;
    }
  }

  ///Whether the current unit has dug or not.
  public bool HasDug
  {
    get
    {
      validify();
      int value = Client.unitGetHasDug(ptr);
      return value == 1;
    }
  }

  ///Whether the current unit has filled or not.
  public bool HasFilled
  {
    get
    {
      validify();
      int value = Client.unitGetHasFilled(ptr);
      return value == 1;
    }
  }

  ///The current amount health this unit has remaining.
  public int HealthLeft
  {
    get
    {
      validify();
      int value = Client.unitGetHealthLeft(ptr);
      return value;
    }
  }

  ///The maximum amount of this health this unit can have
  public int MaxHealth
  {
    get
    {
      validify();
      int value = Client.unitGetMaxHealth(ptr);
      return value;
    }
  }

  ///The number of moves this unit has remaining.
  public int MovementLeft
  {
    get
    {
      validify();
      int value = Client.unitGetMovementLeft(ptr);
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

  ///The range of this unit's attack.
  public int Range
  {
    get
    {
      validify();
      int value = Client.unitGetRange(ptr);
      return value;
    }
  }

  ///The power of the unit's offensive siege ability.
  public int OffensePower
  {
    get
    {
      validify();
      int value = Client.unitGetOffensePower(ptr);
      return value;
    }
  }

  ///The power of the unit's defensive siege ability.
  public int DefensePower
  {
    get
    {
      validify();
      int value = Client.unitGetDefensePower(ptr);
      return value;
    }
  }

  ///The power of this unit types's digging ability.
  public int DigPower
  {
    get
    {
      validify();
      int value = Client.unitGetDigPower(ptr);
      return value;
    }
  }

  ///The power of this unit type's filling ability.
  public int FillPower
  {
    get
    {
      validify();
      int value = Client.unitGetFillPower(ptr);
      return value;
    }
  }

  ///The power of this unit type's attack.
  public int AttackPower
  {
    get
    {
      validify();
      int value = Client.unitGetAttackPower(ptr);
      return value;
    }
  }

}

