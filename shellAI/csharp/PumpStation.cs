using System;
using System.Runtime.InteropServices;

/// <summary>
/// Represents a base to which you want to lead water.
/// </summary>
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
      int value = Client.pumpStationGetId(ptr);
      return value;
    }
  }

  /// <summary>
  /// The owner of the PumpStation.
  /// </summary>
  public int Owner
  {
    get
    {
      validify();
      int value = Client.pumpStationGetOwner(ptr);
      return value;
    }
  }

  /// <summary>
  /// The amount the PumpStation has been sieged.
  /// </summary>
  public int SiegeAmount
  {
    get
    {
      validify();
      int value = Client.pumpStationGetSiegeAmount(ptr);
      return value;
    }
  }

  #endregion

  #region Properties
  #endregion
}
