using System;
using System.Runtime.InteropServices;

/// \brief A basic AI interface.

///This class implements most the code an AI would need to interface with the lower-level game code.
///AIs should extend this class to get a lot of builer-plate code out of the way
///The provided AI class does just that.
public abstract class BaseAI
{
  public static PumpStation[] speciesList;
  public static Mappable[] mappables;
  public static Player[] players;
  public static Tile[] tiles;
  public static Unit[] units;
  IntPtr connection;
  public static int iteration;
  bool initialized;

  public BaseAI(IntPtr c)
  {
    connection = c;
  }

  ///
  ///Make this your username, which should be provided.
  public abstract String username();
  ///
  ///Make this your password, which should be provided.
  public abstract String password();
  ///
  ///This is run on turn 1 before run
  public abstract void init();
  ///
  ///This is run every turn . Return true to end the turn, return false
  ///to request a status update from the server and then immediately rerun this function with the
  ///latest game status.
  public abstract bool run();

  ///
  ///This is run on after your last turn.
  public abstract void end();


  public bool startTurn()
  {
    iteration++;
    int count = 0;
    count = Client.getPumpStationCount(connection);
    speciesList = new PumpStation[count];
    for(int i = 0; i < count; i++)
    {
      speciesList[i] = new PumpStation(Client.getPumpStation(connection, i));
    }
    count = Client.getMappableCount(connection);
    mappables = new Mappable[count];
    for(int i = 0; i < count; i++)
    {
      mappables[i] = new Mappable(Client.getMappable(connection, i));
    }
    count = Client.getPlayerCount(connection);
    players = new Player[count];
    for(int i = 0; i < count; i++)
    {
      players[i] = new Player(Client.getPlayer(connection, i));
    }
    count = Client.getTileCount(connection);
    tiles = new Tile[count];
    for(int i = 0; i < count; i++)
    {
      tiles[i] = new Tile(Client.getTile(connection, i));
    }
    count = Client.getUnitCount(connection);
    units = new Unit[count];
    for(int i = 0; i < count; i++)
    {
      units[i] = new Unit(Client.getUnit(connection, i));
    }

    if(!initialized)
    {
      initialized = true;
      init();
    }
    return run();
  }


  ///The maximum amount of health a unit will have.
  public int maxHealth()
  {
    int value = Client.getMaxHealth(connection);
    return value;
  }
  ///The amount of damage walking over a trench.
  public int trenchDamage()
  {
    int value = Client.getTrenchDamage(connection);
    return value;
  }
  ///The amount of damage walking over water.
  public int waterDamage()
  {
    int value = Client.getWaterDamage(connection);
    return value;
  }
  ///The current turn number.
  public int turnNumber()
  {
    int value = Client.getTurnNumber(connection);
    return value;
  }
  ///The amount of damage a unit will deal.
  public int attackDamage()
  {
    int value = Client.getAttackDamage(connection);
    return value;
  }
  ///The count of offense.
  public int offenseCount()
  {
    int value = Client.getOffenseCount(connection);
    return value;
  }
  ///The count of defense.
  public int defenseCount()
  {
    int value = Client.getDefenseCount(connection);
    return value;
  }
  ///The maximum number of units allowed per player.
  public int maxUnits()
  {
    int value = Client.getMaxUnits(connection);
    return value;
  }
}
