using System;
using System.Runtime.InteropServices;


///Represents type of unit.
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

    //commands


    //getters


  ///Unique Identifier
  public int Id
  {
    get
    {
      validify();
      int value = Client.unitTypeGetId(ptr);
      return value;
    }
  }

  ///The name of this type of unit.
  public string Name
  {
    get
    {
      validify();
      IntPtr value = Client.unitTypeGetName(ptr);
      return Marshal.PtrToStringAuto(value);
    }
  }

  ///The UnitType specific id representing this type of unit.
  public int Type
  {
    get
    {
      validify();
      int value = Client.unitTypeGetType(ptr);
      return value;
    }
  }

  ///The oxygen cost to spawn this unit type into the game.
  public int Cost
  {
    get
    {
      validify();
      int value = Client.unitTypeGetCost(ptr);
      return value;
    }
  }

  ///The power of the attack of this type of unit.
  public int AttackPower
  {
    get
    {
      validify();
      int value = Client.unitTypeGetAttackPower(ptr);
      return value;
    }
  }

  ///The power of this unit types's digging ability.
  public int DigPower
  {
    get
    {
      validify();
      int value = Client.unitTypeGetDigPower(ptr);
      return value;
    }
  }

  ///The power of this unit type's filling ability.
  public int FillPower
  {
    get
    {
      validify();
      int value = Client.unitTypeGetFillPower(ptr);
      return value;
    }
  }

  ///The maximum amount of this health this unit can have
  public int MaxHealth
  {
    get
    {
      validify();
      int value = Client.unitTypeGetMaxHealth(ptr);
      return value;
    }
  }

  ///The maximum number of moves this unit can move.
  public int MaxMovement
  {
    get
    {
      validify();
      int value = Client.unitTypeGetMaxMovement(ptr);
      return value;
    }
  }

  ///The power of the unit type's offensive siege ability.
  public int OffensePower
  {
    get
    {
      validify();
      int value = Client.unitTypeGetOffensePower(ptr);
      return value;
    }
  }

  ///The power of the unit type's defensive siege ability.
  public int DefensePower
  {
    get
    {
      validify();
      int value = Client.unitTypeGetDefensePower(ptr);
      return value;
    }
  }

  ///The range of the unit type's attack.
  public int Range
  {
    get
    {
      validify();
      int value = Client.unitTypeGetRange(ptr);
      return value;
    }
  }

}

