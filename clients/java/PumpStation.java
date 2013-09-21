import com.sun.jna.Pointer;

///
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
    for(int i = 0; i < BaseAI.speciesList.length; i++)
    {
      if(BaseAI.speciesList[i].ID == ID)
      {
        ptr = BaseAI.speciesList[i].ptr;
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
  public int getSeigeCount()
  {
    validify();
    return Client.INSTANCE.pumpStationGetSeigeCount(ptr);
  }

}
