using System;
using System.Runtime.InteropServices;

/// <summary>
/// Represents a single unit on the map.
/// </summary>
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

  #region Commands
  /// <summary>
  /// Make the unit move to the respective x and y location.
  /// </summary>
  public bool move(int x, int y)
  {
    validify();
    return (Client.unitMove(ptr, x, y) == 0) ? false : true;
  }
  /// <summary>
  /// Put dirt in a hole!
  /// </summary>
  public bool fill(Tile tile)
  {
    validify();
    tile.validify();
    return (Client.unitFill(ptr, tile.ptr) == 0) ? false : true;
  }
  /// <summary>
  /// Dig out a tile
  /// </summary>
  public bool dig(Tile tile)
  {
    validify();
    tile.validify();
    return (Client.unitDig(ptr, tile.ptr) == 0) ? false : true;
  }
  /// <summary>
  /// Command to attack another Unit.
  /// </summary>
  public bool attack(Unit target)
  {
    validify();
    target.validify();
    return (Client.unitAttack(ptr, target.ptr) == 0) ? false : true;
  }
  #endregion

  #region Getters
  /// <summary>
  /// Unique Identifier
  /// </summary>
  public new int Id
  {
    get
    {
      validify();
      int value = Client.unitGetId(ptr);
      return value;
    }
  }

  /// <summary>
  /// X position of the object
  /// </summary>
  public new int X
  {
    get
    {
      validify();
      int value = Client.unitGetX(ptr);
      return value;
    }
  }

  /// <summary>
  /// Y position of the object
  /// </summary>
  public new int Y
  {
    get
    {
      validify();
      int value = Client.unitGetY(ptr);
      return value;
    }
  }

  /// <summary>
  /// The owner of this unit.
  /// </summary>
  public int Owner
  {
    get
    {
      validify();
      int value = Client.unitGetOwner(ptr);
      return value;
    }
  }

  /// <summary>
  /// The type of this unit. This type refers to list of UnitTypes.
  /// </summary>
  public int Type
  {
    get
    {
      validify();
      int value = Client.unitGetType(ptr);
      return value;
    }
  }

  /// <summary>
  /// Whether current unit has attacked or not.
  /// </summary>
  public bool HasAttacked
  {
    get
    {
      validify();
      int value = Client.unitGetHasAttacked(ptr);
      return value == 1;
    }
  }

  /// <summary>
  /// Whether the current unit has dug or not.
  /// </summary>
  public bool HasDug
  {
    get
    {
      validify();
      int value = Client.unitGetHasDug(ptr);
      return value == 1;
    }
  }

  /// <summary>
  /// Whether the current unit has filled or not.
  /// </summary>
  public bool HasFilled
  {
    get
    {
      validify();
      int value = Client.unitGetHasFilled(ptr);
      return value == 1;
    }
  }

  /// <summary>
  /// The current amount health this unit has remaining.
  /// </summary>
  public int HealthLeft
  {
    get
    {
      validify();
      int value = Client.unitGetHealthLeft(ptr);
      return value;
    }
  }

  /// <summary>
  /// The maximum amount of this health this unit can have
  /// </summary>
  public int MaxHealth
  {
    get
    {
      validify();
      int value = Client.unitGetMaxHealth(ptr);
      return value;
    }
  }

  /// <summary>
  /// The number of moves this unit has remaining.
  /// </summary>
  public int MovementLeft
  {
    get
    {
      validify();
      int value = Client.unitGetMovementLeft(ptr);
      return value;
    }
  }

  /// <summary>
  /// The maximum number of moves this unit can move.
  /// </summary>
  public int MaxMovement
  {
    get
    {
      validify();
      int value = Client.unitGetMaxMovement(ptr);
      return value;
    }
  }

  /// <summary>
  /// The range of this unit's attack.
  /// </summary>
  public int Range
  {
    get
    {
      validify();
      int value = Client.unitGetRange(ptr);
      return value;
    }
  }

  /// <summary>
  /// The power of the unit's offensive siege ability.
  /// </summary>
  public int OffensePower
  {
    get
    {
      validify();
      int value = Client.unitGetOffensePower(ptr);
      return value;
    }
  }

  /// <summary>
  /// The power of the unit's defensive siege ability.
  /// </summary>
  public int DefensePower
  {
    get
    {
      validify();
      int value = Client.unitGetDefensePower(ptr);
      return value;
    }
  }

  /// <summary>
  /// The power of this unit types's digging ability.
  /// </summary>
  public int DigPower
  {
    get
    {
      validify();
      int value = Client.unitGetDigPower(ptr);
      return value;
    }
  }

  /// <summary>
  /// The power of this unit type's filling ability.
  /// </summary>
  public int FillPower
  {
    get
    {
      validify();
      int value = Client.unitGetFillPower(ptr);
      return value;
    }
  }

  /// <summary>
  /// The power of this unit type's attack.
  /// </summary>
  public int AttackPower
  {
    get
    {
      validify();
      int value = Client.unitGetAttackPower(ptr);
      return value;
    }
  }

  #endregion

  #region Properties
  #endregion
}
