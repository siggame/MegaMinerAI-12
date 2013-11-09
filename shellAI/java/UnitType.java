import com.sun.jna.Pointer;

///Represents type of unit.
class UnitType
{
  Pointer ptr;
  int ID;
  int iteration;
  public UnitType(Pointer p)
  {
    ptr = p;
    ID = Client.INSTANCE.unitTypeGetId(ptr);
    iteration = BaseAI.iteration;
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.unitTypes.length; i++)
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
  public int getId()
  {
    validify();
    return Client.INSTANCE.unitTypeGetId(ptr);
  }
  ///The name of this type of unit.
  public String getName()
  {
    validify();
    return Client.INSTANCE.unitTypeGetName(ptr);
  }
  ///The UnitType specific id representing this type of unit.
  public int getType()
  {
    validify();
    return Client.INSTANCE.unitTypeGetType(ptr);
  }
  ///The oxygen cost to spawn this unit type into the game.
  public int getCost()
  {
    validify();
    return Client.INSTANCE.unitTypeGetCost(ptr);
  }
  ///The power of the attack of this type of unit.
  public int getAttackPower()
  {
    validify();
    return Client.INSTANCE.unitTypeGetAttackPower(ptr);
  }
  ///The power of this unit types's digging ability.
  public int getDigPower()
  {
    validify();
    return Client.INSTANCE.unitTypeGetDigPower(ptr);
  }
  ///The power of this unit type's filling ability.
  public int getFillPower()
  {
    validify();
    return Client.INSTANCE.unitTypeGetFillPower(ptr);
  }
  ///The maximum amount of this health this unit can have
  public int getMaxHealth()
  {
    validify();
    return Client.INSTANCE.unitTypeGetMaxHealth(ptr);
  }
  ///The maximum number of moves this unit can move.
  public int getMaxMovement()
  {
    validify();
    return Client.INSTANCE.unitTypeGetMaxMovement(ptr);
  }
  ///The power of the unit type's offensive siege ability.
  public int getOffensePower()
  {
    validify();
    return Client.INSTANCE.unitTypeGetOffensePower(ptr);
  }
  ///The power of the unit type's defensive siege ability.
  public int getDefensePower()
  {
    validify();
    return Client.INSTANCE.unitTypeGetDefensePower(ptr);
  }
  ///The range of the unit type's attack.
  public int getRange()
  {
    validify();
    return Client.INSTANCE.unitTypeGetRange(ptr);
  }

}
