import com.sun.jna.Pointer;

/// \brief A basic AI interface.

///This class implements most the code an AI would need to interface with the lower-level game code.
///AIs should extend this class to get a lot of builer-plate code out of the way
///The provided AI class does just that.
public abstract class BaseAI
{
  static Mappable[] mappables;
  static Tile[] tiles;
  static PumpStation[] pumpStations;
  static Unit[] units;
  static Player[] players;
  Pointer connection;
  static int iteration;
  boolean initialized;

  public BaseAI(Pointer c)
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
  public abstract boolean run();

  ///
  ///This is run on after your last turn.
  public abstract void end();


  public boolean startTurn()
  {
    iteration++;
    int count = 0;
    count = Client.INSTANCE.getMappableCount(connection);
    mappables = new Mappable[count];
    for(int i = 0; i < count; i++)
    {
      mappables[i] = new Mappable(Client.INSTANCE.getMappable(connection, i));
    }
    count = Client.INSTANCE.getTileCount(connection);
    tiles = new Tile[count];
    for(int i = 0; i < count; i++)
    {
      tiles[i] = new Tile(Client.INSTANCE.getTile(connection, i));
    }
    count = Client.INSTANCE.getPumpStationCount(connection);
    pumpStations = new PumpStation[count];
    for(int i = 0; i < count; i++)
    {
      pumpStations[i] = new PumpStation(Client.INSTANCE.getPumpStation(connection, i));
    }
    count = Client.INSTANCE.getUnitCount(connection);
    units = new Unit[count];
    for(int i = 0; i < count; i++)
    {
      units[i] = new Unit(Client.INSTANCE.getUnit(connection, i));
    }
    count = Client.INSTANCE.getPlayerCount(connection);
    players = new Player[count];
    for(int i = 0; i < count; i++)
    {
      players[i] = new Player(Client.INSTANCE.getPlayer(connection, i));
    }

    if(!initialized)
    {
      initialized = true;
      init();
    }
    return run();
  }


  ///The width of the total map.
  int mapWidth()
  {
    return Client.INSTANCE.getMapWidth(connection);
  }
  ///The height of the total map.
  int mapHeight()
  {
    return Client.INSTANCE.getMapHeight(connection);
  }
  ///The maximum amount of health a unit will have.
  int maxHealth()
  {
    return Client.INSTANCE.getMaxHealth(connection);
  }
  ///The amount of damage walking over a trench.
  int trenchDamage()
  {
    return Client.INSTANCE.getTrenchDamage(connection);
  }
  ///The amount of damage walking over water.
  int waterDamage()
  {
    return Client.INSTANCE.getWaterDamage(connection);
  }
  ///The current turn number.
  int turnNumber()
  {
    return Client.INSTANCE.getTurnNumber(connection);
  }
  ///The amount of damage a unit will deal.
  int attackDamage()
  {
    return Client.INSTANCE.getAttackDamage(connection);
  }
  ///How quickly a unit will siege a PumpStation.
  int offensePower()
  {
    return Client.INSTANCE.getOffensePower(connection);
  }
  ///How much a unit will slow a siege.
  int defensePower()
  {
    return Client.INSTANCE.getDefensePower(connection);
  }
  ///The maximum number of units allowed per player.
  int maxUnits()
  {
    return Client.INSTANCE.getMaxUnits(connection);
  }
  ///The cost of spawning in a new unit
  int unitCost()
  {
    return Client.INSTANCE.getUnitCost(connection);
  }
  ///The id of the current player.
  int playerID()
  {
    return Client.INSTANCE.getPlayerID(connection);
  }
  ///What number game this is for the server
  int gameNumber()
  {
    return Client.INSTANCE.getGameNumber(connection);
  }
  ///The maximum siege value before the PumpStation is sieged.
  int maxSiege()
  {
    return Client.INSTANCE.getMaxSiege(connection);
  }
}
