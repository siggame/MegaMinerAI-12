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
  int playerTalk(Pointer object, String message);
  int unitMove(Pointer object, int x, int y);
  int unitFill(Pointer object, Pointer tile);
  int unitDig(Pointer object, Pointer tile);
  int unitAttack(Pointer object, Pointer target);
  int tileSpawn(Pointer object, int type);

    //accessors
  int getMapWidth(Pointer connection);
  int getMapHeight(Pointer connection);
  int getMaxHealth(Pointer connection);
  int getTrenchDamage(Pointer connection);
  int getWaterDamage(Pointer connection);
  int getTurnNumber(Pointer connection);
  int getAttackDamage(Pointer connection);
  int getOffensePower(Pointer connection);
  int getDefensePower(Pointer connection);
  int getMaxSiege(Pointer connection);
  int getMaxUnits(Pointer connection);
  int getUnitCost(Pointer connection);
  int getPlayerID(Pointer connection);
  int getGameNumber(Pointer connection);

  Pointer getPlayer(Pointer connection, int num);
  int getPlayerCount(Pointer connection);
  Pointer getPumpStation(Pointer connection, int num);
  int getPumpStationCount(Pointer connection);
  Pointer getMappable(Pointer connection, int num);
  int getMappableCount(Pointer connection);
  Pointer getUnit(Pointer connection, int num);
  int getUnitCount(Pointer connection);
  Pointer getTile(Pointer connection, int num);
  int getTileCount(Pointer connection);


    //getters
  int playerGetId(Pointer ptr);
  String playerGetPlayerName(Pointer ptr);
  float playerGetTime(Pointer ptr);
  int playerGetWaterStored(Pointer ptr);
  int playerGetSpawnResources(Pointer ptr);

  int pumpStationGetId(Pointer ptr);
  int pumpStationGetOwner(Pointer ptr);
  int pumpStationGetWaterAmount(Pointer ptr);
  int pumpStationGetSiegeAmount(Pointer ptr);

  int mappableGetId(Pointer ptr);
  int mappableGetX(Pointer ptr);
  int mappableGetY(Pointer ptr);

  int unitGetId(Pointer ptr);
  int unitGetX(Pointer ptr);
  int unitGetY(Pointer ptr);
  int unitGetOwner(Pointer ptr);
  int unitGetType(Pointer ptr);
  int unitGetHasAttacked(Pointer ptr);
  int unitGetHasDug(Pointer ptr);
  int unitGetHasFilled(Pointer ptr);
  int unitGetHealthLeft(Pointer ptr);
  int unitGetMaxHealth(Pointer ptr);
  int unitGetMovementLeft(Pointer ptr);
  int unitGetMaxMovement(Pointer ptr);

  int tileGetId(Pointer ptr);
  int tileGetX(Pointer ptr);
  int tileGetY(Pointer ptr);
  int tileGetOwner(Pointer ptr);
  int tileGetPumpID(Pointer ptr);
  int tileGetWaterAmount(Pointer ptr);
  int tileGetIsTrench(Pointer ptr);


    //properties

}
