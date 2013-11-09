import com.sun.jna.Pointer;

///Represents a base to which you want to lead water.
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
  ///The amount the PumpStation has been sieged.
  public int getSiegeAmount()
  {
    validify();
    return Client.INSTANCE.pumpStationGetSiegeAmount(ptr);
  }

}
