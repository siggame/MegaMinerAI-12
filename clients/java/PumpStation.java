import com.sun.jna.Pointer;

///Represents a base to which you want to lead water, and a spawn location for new units.
class PumpStation
{
  Pointer ptr;
  int ID;
  int iteration;
  public PumpStation(Pointer p)
  {
    ptr = p;
    ID = Client.INSTANCE.pumpStationGetId(ptr);
    iteration = BaseAI.iteration;
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.pumpStations.length; i++)
    {
      if(BaseAI.pumpStations[i].ID == ID)
      {
        ptr = BaseAI.pumpStations[i].ptr;
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
    return Client.INSTANCE.pumpStationGetId(ptr);
  }
  ///The owner of the PumpStation.
  public int getOwner()
  {
    validify();
    return Client.INSTANCE.pumpStationGetOwner(ptr);
  }
  ///The amount of water the PumpStation pumps.
  public int getWaterAmount()
  {
    validify();
    return Client.INSTANCE.pumpStationGetWaterAmount(ptr);
  }
  ///The length of time it takes to capture the PumpStation.
  public int getSiegeCount()
  {
    validify();
    return Client.INSTANCE.pumpStationGetSiegeCount(ptr);
  }

}