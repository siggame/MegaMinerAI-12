using System;
using System.Runtime.InteropServices;


///Represents a base to which you want to lead water, and a spawn location for new units.
public class PumpStation
{
  public IntPtr ptr;
  protected int ID;
  protected int iteration;

  public PumpStation()
  {
  }

  public PumpStation(IntPtr p)
  {
    ptr = p;
    ID = Client.pumpStationGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.pumpStations.Length; i++)
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
  public int Id
  {
    get
    {
      validify();
      int value = Client.pumpStationGetId(ptr);
      return value;
    }
  }

  ///The owner of the PumpStation.
  public int Owner
  {
    get
    {
      validify();
      int value = Client.pumpStationGetOwner(ptr);
      return value;
    }
  }

  ///The amount of water the PumpStation pumps.
  public int WaterAmount
  {
    get
    {
      validify();
      int value = Client.pumpStationGetWaterAmount(ptr);
      return value;
    }
  }

  ///The length of time it takes to capture the PumpStation.
  public int SiegeCount
  {
    get
    {
      validify();
      int value = Client.pumpStationGetSiegeCount(ptr);
      return value;
    }
  }

}

