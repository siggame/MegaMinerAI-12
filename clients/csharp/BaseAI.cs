using System;
using System.Runtime.InteropServices;

/// <summary>
/// This class implements most the code an AI would need to interface with the lower-level game code.
/// AIs should extend this class to get a lot of builer-plate code out of the way. The provided AI class does just that.
/// </summary>
public abstract class BaseAI
{
  public static Player[] players;
  public static Mappable[] mappables;
  public static PumpStation[] pumpStations;
  public static Unit[] units;
  public static Tile[] tiles;
  public static UnitType[] unitTypes;

  IntPtr connection;
  public static int iteration;
  bool initialized;

  public BaseAI(IntPtr c)
  {
    connection = c;
  }

  /// <summary>
  /// Make this your username, which should be provided.
  /// </summary>
  /// <returns>Returns the username of the player.</returns>
  public abstract String username();

  /// <summary>
  /// Make this your password, which should be provided.
  /// </summary>
  /// <returns>Returns the password of the player.</returns>
  public abstract String password();

  /// <summary>
  /// This is run once on turn one before run().
  /// </summary>
  public abstract void init();

  /// <summary>
  /// This is run every turn.
  /// </summary>
  /// <returns>
  /// Return true to end turn, false to resynchronize with the 
  /// server and run again.
  /// </returns>
  public abstract bool run();

  /// <summary>
  /// This is run once after your last turn.
  /// </summary>
  public abstract void end();

  /// <summary>
  /// Synchronizes with the server, then calls run().
  /// </summary>
  /// <returns>
  /// Return true to end turn, false to resynchronize with the 
  /// server and run again.
  /// </returns>
  public bool startTurn()
  {
    int count = 0;
    iteration++;

    count = Client.getPlayerCount(connection);
    players = new Player[count];
    for(int i = 0; i < count; i++)
      players[i] = new Player(Client.getPlayer(connection, i));

    count = Client.getMappableCount(connection);
    mappables = new Mappable[count];
    for(int i = 0; i < count; i++)
      mappables[i] = new Mappable(Client.getMappable(connection, i));

    count = Client.getPumpStationCount(connection);
    pumpStations = new PumpStation[count];
    for(int i = 0; i < count; i++)
      pumpStations[i] = new PumpStation(Client.getPumpStation(connection, i));

    count = Client.getUnitCount(connection);
    units = new Unit[count];
    for(int i = 0; i < count; i++)
      units[i] = new Unit(Client.getUnit(connection, i));

    count = Client.getTileCount(connection);
    tiles = new Tile[count];
    for(int i = 0; i < count; i++)
      tiles[i] = new Tile(Client.getTile(connection, i));

    count = Client.getUnitTypeCount(connection);
    unitTypes = new UnitType[count];
    for(int i = 0; i < count; i++)
      unitTypes[i] = new UnitType(Client.getUnitType(connection, i));

    if(!initialized)
    {
      initialized = true;
      init();
    }

    return run();
  }

  /// <summary>
  /// The width of the total map.
  /// </summary>
  /// <returns>Returns the width of the total map.</returns>
  public int mapWidth()
  {
    int value = Client.getMapWidth(connection);
    return value;
  }

  /// <summary>
  /// The height of the total map.
  /// </summary>
  /// <returns>Returns the height of the total map.</returns>
  public int mapHeight()
  {
    int value = Client.getMapHeight(connection);
    return value;
  }

  /// <summary>
  /// The amount of damage walking over water.
  /// </summary>
  /// <returns>Returns the amount of damage walking over water.</returns>
  public int waterDamage()
  {
    int value = Client.getWaterDamage(connection);
    return value;
  }

  /// <summary>
  /// The current turn number.
  /// </summary>
  /// <returns>Returns the current turn number.</returns>
  public int turnNumber()
  {
    int value = Client.getTurnNumber(connection);
    return value;
  }

  /// <summary>
  /// The maximum number of units allowed per player.
  /// </summary>
  /// <returns>Returns the maximum number of units allowed per player.</returns>
  public int maxUnits()
  {
    int value = Client.getMaxUnits(connection);
    return value;
  }

  /// <summary>
  /// The id of the current player.
  /// </summary>
  /// <returns>Returns the id of the current player.</returns>
  public int playerID()
  {
    int value = Client.getPlayerID(connection);
    return value;
  }

  /// <summary>
  /// What number game this is for the server
  /// </summary>
  /// <returns>Returns what number game this is for the server</returns>
  public int gameNumber()
  {
    int value = Client.getGameNumber(connection);
    return value;
  }

  /// <summary>
  /// The maximum siege value before the PumpStation is sieged.
  /// </summary>
  /// <returns>Returns the maximum siege value before the PumpStation is sieged.</returns>
  public int maxSiege()
  {
    int value = Client.getMaxSiege(connection);
    return value;
  }

  /// <summary>
  /// The rate at which missing oxygen is regained.
  /// </summary>
  /// <returns>Returns the rate at which missing oxygen is regained.</returns>
  public float oxygenRate()
  {
    float value = Client.getOxygenRate(connection);
    return value;
  }

  /// <summary>
  /// The number of turns until sediment is deposited on the trenches.
  /// </summary>
  /// <returns>Returns the number of turns until sediment is deposited on the trenches.</returns>
  public int depositionRate()
  {
    int value = Client.getDepositionRate(connection);
    return value;
  }
}
