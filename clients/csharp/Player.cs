using System;
using System.Runtime.InteropServices;

/// <summary>
/// 
/// </summary>
public class Player
{
  public IntPtr ptr;
  protected int ID;
  protected int iteration;

  public Player()
  {
  }

  public Player(IntPtr p)
  {
    ptr = p;
    ID = Client.playerGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.players.Length; i++)
    {
      if(BaseAI.players[i].ID == ID)
      {
        ptr = BaseAI.players[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }

  #region Commands
  /// <summary>
  /// Allows a player to display messages on the screen
  /// </summary>
  public bool talk(string message)
  {
    validify();
    return (Client.playerTalk(ptr, message) == 0) ? false : true;
  }
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
      int value = Client.playerGetId(ptr);
      return value;
    }
  }

  /// <summary>
  /// Player's Name
  /// </summary>
  public string PlayerName
  {
    get
    {
      validify();
      IntPtr value = Client.playerGetPlayerName(ptr);
      return Marshal.PtrToStringAuto(value);
    }
  }

  /// <summary>
  /// Time remaining, updated at start of turn
  /// </summary>
  public float Time
  {
    get
    {
      validify();
      float value = Client.playerGetTime(ptr);
      return value;
    }
  }

  /// <summary>
  /// The amount of water a player has.
  /// </summary>
  public int WaterStored
  {
    get
    {
      validify();
      int value = Client.playerGetWaterStored(ptr);
      return value;
    }
  }

  /// <summary>
  /// Resource used to spawn in units.
  /// </summary>
  public int Oxygen
  {
    get
    {
      validify();
      int value = Client.playerGetOxygen(ptr);
      return value;
    }
  }

  /// <summary>
  /// The player's oxygen cap.
  /// </summary>
  public int MaxOxygen
  {
    get
    {
      validify();
      int value = Client.playerGetMaxOxygen(ptr);
      return value;
    }
  }

  #endregion

  #region Properties
  #endregion
}
