import com.sun.jna.Library;
import com.sun.jna.Pointer;
import com.sun.jna.Native;

public interface Client extends Library {
  Client INSTANCE = (Client)Native.loadLibrary("client", Client.class);
  Pointer createConnection();
  boolean serverConnect(Pointer connection, String host, String port);

  boolean serverLogin(Pointer connection, String username, String password);
  int createGame(Pointer connection);
  int joinGame(Pointer connection, int id, String playerType);

  void endTurn(Pointer connection);
  void getStatus(Pointer connection);

  int networkLoop(Pointer connection);


    //commands
  int unitMove(Pointer object, int x, int y);
  int unitFill(Pointer object, Pointer tile);
  int unitDig(Pointer object, Pointer tile);
  int unitAttack(Pointer object, Pointer target);
  int playerTalk(Pointer object, String message);
  int tileSpawn(Pointer object, int type);

    //accessors
  int getMaxHealth(Pointer connection);
  int getTrenchDamage(Pointer connection);
  int getWaterDamage(Pointer connection);
  int getTurnNumber(Pointer connection);
  int getAttackDamage(Pointer connection);
  int getOffenseCount(Pointer connection);
  int getDefenseCount(Pointer connection);
  int getMaxUnits(Pointer connection);
  int getUnitCost(Pointer connection);

  Pointer getMappable(Pointer connection, int num);
  int getMappableCount(Pointer connection);
  Pointer getUnit(Pointer connection, int num);
  int getUnitCount(Pointer connection);
  Pointer getPlayer(Pointer connection, int num);
  int getPlayerCount(Pointer connection);
  Pointer getTile(Pointer connection, int num);
  int getTileCount(Pointer connection);
  Pointer getPumpStation(Pointer connection, int num);
  int getPumpStationCount(Pointer connection);


    //getters
  int mappableGetId(Pointer ptr);
  int mappableGetX(Pointer ptr);
  int mappableGetY(Pointer ptr);

  int unitGetId(Pointer ptr);
  int unitGetX(Pointer ptr);
  int unitGetY(Pointer ptr);
  int unitGetOwner(Pointer ptr);
  int unitGetType(Pointer ptr);
  int unitGetCurHealth(Pointer ptr);
  int unitGetMaxHealth(Pointer ptr);
  int unitGetCurMovement(Pointer ptr);
  int unitGetMaxMovement(Pointer ptr);

  int playerGetId(Pointer ptr);
  String playerGetPlayerName(Pointer ptr);
  float playerGetTime(Pointer ptr);
  int playerGetWaterStored(Pointer ptr);
  int playerGetSpawnResources(Pointer ptr);

  int tileGetId(Pointer ptr);
  int tileGetX(Pointer ptr);
  int tileGetY(Pointer ptr);
  int tileGetOwner(Pointer ptr);
  int tileGetType(Pointer ptr);
  int tileGetPumpID(Pointer ptr);
  int tileGetWaterAmount(Pointer ptr);
  int tileGetIsTrench(Pointer ptr);

  int pumpStationGetId(Pointer ptr);
  int pumpStationGetOwner(Pointer ptr);
  int pumpStationGetWaterAmount(Pointer ptr);
  int pumpStationGetSiegeCount(Pointer ptr);


    //properties

}
