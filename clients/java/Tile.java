import com.sun.jna.Pointer;

///Represents a single tile on the map, can contain some amount of water.
class Tile extends Mappable
{
  public Tile(Pointer p)
  {
    super(p);
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.tiles.length; i++)
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
  boolean spawn(int type)
  {
    validify();
    return (Client.INSTANCE.tileSpawn(ptr, type) == 0) ? false : true;
  }

    //getters

  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.INSTANCE.tileGetId(ptr);
  }
  ///X position of the object
  public int getX()
  {
    validify();
    return Client.INSTANCE.tileGetX(ptr);
  }
  ///Y position of the object
  public int getY()
  {
    validify();
    return Client.INSTANCE.tileGetY(ptr);
  }
  ///The owner of the tile.
  public int getOwner()
  {
    validify();
    return Client.INSTANCE.tileGetOwner(ptr);
  }
  ///The type of tile this tile represents.
  public int getType()
  {
    validify();
    return Client.INSTANCE.tileGetType(ptr);
  }
  ///Determines if this tile is a part of a Pump Station.
  public int getPumpID()
  {
    validify();
    return Client.INSTANCE.tileGetPumpID(ptr);
  }
  ///The amount of water contained on the tile.
  public int getWaterAmount()
  {
    validify();
    return Client.INSTANCE.tileGetWaterAmount(ptr);
  }
  ///Whether the tile is a trench or not.
  public int getIsTrench()
  {
    validify();
    return Client.INSTANCE.tileGetIsTrench(ptr);
  }

}
