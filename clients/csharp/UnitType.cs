using System;
using System.Runtime.InteropServices;

/// <summary>
/// Represents type of unit.
/// </summary>
public class UnitType
{
  public IntPtr ptr;
  protected int ID;
  protected int iteration;

  public UnitType()
  {
  }

  public UnitType(IntPtr p)
  {
    ptr = p;
    ID = Client.unitTypeGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.unitTypes.Length; i++)
    {
      if(BaseAI.unitTypes[i].ID == ID)
      {
        ptr = BaseAI.unitTypes[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }

  #region Commands
  #endregion

  #region Getters
  /// <summary>
  /// Unique Identifier
  /// </summary>
  public int Id
  {
    get
    {
      validify();
      int value = Client.unitTypeGetId(ptr);
      return value;
    }
  }

  /// <summary>
  /// The name of this type of unit.
  /// </summary>
  public string Name
  {
    get
    {
      validify();
      IntPtr value = Client.unitTypeGetName(ptr);
      return Marshal.PtrToStringAuto(value);
    }
  }

  /// <summary>
  /// The UnitType specific id representing this type of unit.
  /// </summary>
  public int Type
  {
    get
    {
      validify();
      int value = Client.unitTypeGetType(ptr);
      return value;
    }
  }

  /// <summary>
  /// The oxygen cost to spawn this unit type into the game.
  /// </summary>
  public int Cost
  {
    get
    {
      validify();
      int value = Client.unitTypeGetCost(ptr);
      return value;
    }
  }

  /// <summary>
  /// The power of the attack of this type of unit.
  /// </summary>
  public int AttackPower
  {
    get
    {
      validify();
      int value = Client.unitTypeGetAttackPower(ptr);
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
      int value = Client.unitTypeGetDigPower(ptr);
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
      int value = Client.unitTypeGetFillPower(ptr);
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
      int value = Client.unitTypeGetMaxHealth(ptr);
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
      int value = Client.unitTypeGetMaxMovement(ptr);
      return value;
    }
  }

  /// <summary>
  /// The power of the unit type's offensive siege ability.
  /// </summary>
  public int OffensePower
  {
    get
    {
      validify();
      int value = Client.unitTypeGetOffensePower(ptr);
      return value;
    }
  }

  /// <summary>
  /// The power of the unit type's defensive siege ability.
  /// </summary>
  public int DefensePower
  {
    get
    {
      validify();
      int value = Client.unitTypeGetDefensePower(ptr);
      return value;
    }
  }

  /// <summary>
  /// The range of the unit type's attack.
  /// </summary>
  public int Range
  {
    get
    {
      validify();
      int value = Client.unitTypeGetRange(ptr);
      return value;
    }
  }

  #endregion

  #region Properties
  #endregion
}
