import com.sun.jna.Pointer;

///Represents a single unit on the map.
class Unit extends Mappable
{
  public Unit(Pointer p)
  {
    super(p);
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.units.length; i++)
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
  boolean move(int x, int y)
  {
    validify();
    return (Client.INSTANCE.unitMove(ptr, x, y) == 0) ? false : true;
  }
  ///Put dirt in a hole!
  boolean fill(Tile tile)
  {
    validify();
    tile.validify();
    return (Client.INSTANCE.unitFill(ptr, tile.ptr) == 0) ? false : true;
  }
  ///Dig out a tile
  boolean dig(Tile tile)
  {
    validify();
    tile.validify();
    return (Client.INSTANCE.unitDig(ptr, tile.ptr) == 0) ? false : true;
  }
  ///Command to attack another Unit.
  boolean attack(Unit target)
  {
    validify();
    target.validify();
    return (Client.INSTANCE.unitAttack(ptr, target.ptr) == 0) ? false : true;
  }

    //getters

  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.INSTANCE.unitGetId(ptr);
  }
  ///X position of the object
  public int getX()
  {
    validify();
    return Client.INSTANCE.unitGetX(ptr);
  }
  ///Y position of the object
  public int getY()
  {
    validify();
    return Client.INSTANCE.unitGetY(ptr);
  }
  ///The owner of this unit.
  public int getOwner()
  {
    validify();
    return Client.INSTANCE.unitGetOwner(ptr);
  }
  ///The type of this unit. This type refers to list of UnitTypes.
  public int getType()
  {
    validify();
    return Client.INSTANCE.unitGetType(ptr);
  }
  ///Whether current unit has attacked or not.
  public int getHasAttacked()
  {
    validify();
    return Client.INSTANCE.unitGetHasAttacked(ptr);
  }
  ///Whether the current unit has dug or not.
  public int getHasDug()
  {
    validify();
    return Client.INSTANCE.unitGetHasDug(ptr);
  }
  ///Whether the current unit has filled or not.
  public int getHasFilled()
  {
    validify();
    return Client.INSTANCE.unitGetHasFilled(ptr);
  }
  ///The current amount health this unit has remaining.
  public int getHealthLeft()
  {
    validify();
    return Client.INSTANCE.unitGetHealthLeft(ptr);
  }
  ///The maximum amount of this health this unit can have
  public int getMaxHealth()
  {
    validify();
    return Client.INSTANCE.unitGetMaxHealth(ptr);
  }
  ///The number of moves this unit has remaining.
  public int getMovementLeft()
  {
    validify();
    return Client.INSTANCE.unitGetMovementLeft(ptr);
  }
  ///The maximum number of moves this unit can move.
  public int getMaxMovement()
  {
    validify();
    return Client.INSTANCE.unitGetMaxMovement(ptr);
  }
  ///The range of this unit's attack.
  public int getRange()
  {
    validify();
    return Client.INSTANCE.unitGetRange(ptr);
  }
  ///The power of the unit's offensive siege ability.
  public int getOffensePower()
  {
    validify();
    return Client.INSTANCE.unitGetOffensePower(ptr);
  }
  ///The power of the unit's defensive siege ability.
  public int getDefensePower()
  {
    validify();
    return Client.INSTANCE.unitGetDefensePower(ptr);
  }
  ///The power of this unit types's digging ability.
  public int getDigPower()
  {
    validify();
    return Client.INSTANCE.unitGetDigPower(ptr);
  }
  ///The power of this unit type's filling ability.
  public int getFillPower()
  {
    validify();
    return Client.INSTANCE.unitGetFillPower(ptr);
  }

}
