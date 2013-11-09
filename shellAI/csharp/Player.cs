using System;
using System.Runtime.InteropServices;


///
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

    //commands

  ///Allows a player to display messages on the screen
  public bool talk(string message)
  {
    validify();
    return (Client.playerTalk(ptr, message) == 0) ? false : true;
  }

    //getters


  ///Unique Identifier
  public int Id
  {
    get
    {
      validify();
      int value = Client.playerGetId(ptr);
      return value;
    }
  }

  ///Player's Name
  public string PlayerName
  {
    get
    {
      validify();
      IntPtr value = Client.playerGetPlayerName(ptr);
      return Marshal.PtrToStringAuto(value);
    }
  }

  ///Time remaining, updated at start of turn
  public float Time
  {
    get
    {
      validify();
      float value = Client.playerGetTime(ptr);
      return value;
    }
  }

  ///The amount of water a player has.
  public int WaterStored
  {
    get
    {
      validify();
      int value = Client.playerGetWaterStored(ptr);
      return value;
    }
  }

  ///Resource used to spawn in units.
  public int Oxygen
  {
    get
    {
      validify();
      int value = Client.playerGetOxygen(ptr);
      return value;
    }
  }

  ///The player's oxygen cap.
  public int MaxOxygen
  {
    get
    {
      validify();
      int value = Client.playerGetMaxOxygen(ptr);
      return value;
    }
  }

}

