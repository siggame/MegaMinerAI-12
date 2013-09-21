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
  int tileSpawn(Pointer object, int type);
  int unitMove(Pointer object, int x, int y);
  int unitAttack(Pointer object, int unit);
  int unitFill(Pointer object, int tile);
  int unitBuild(Pointer object, int tile);

    //accessors
  int getMaxHealth(Pointer connection);
  int getTrenchDamage(Pointer connection);
  int getWaterDamage(Pointer connection);
  int getTurnNumber(Pointer connection);
  int getAttackDamage(Pointer connection);
  int getOffenseCount(Pointer connection);
  int getDefenseCount(Pointer connection);
  int getMaxUnits(Pointer connection);

  Pointer getPumpStation(Pointer connection, int num);
  int getPumpStationCount(Pointer connection);
  Pointer getMappable(Pointer connection, int num);
  int getMappableCount(Pointer connection);
  Pointer getPlayer(Pointer connection, int num);
  int getPlayerCount(Pointer connection);
  Pointer getTile(Pointer connection, int num);
  int getTileCount(Pointer connection);
  Pointer getUnit(Pointer connection, int num);
  int getUnitCount(Pointer connection);


    //getters
  int pumpStationGetId(Pointer ptr);
  int pumpStationGetOwner(Pointer ptr);
  int pumpStationGetWaterAmount(Pointer ptr);
  int pumpStationGetSeigeCount(Pointer ptr);

  int mappableGetId(Pointer ptr);
  int mappableGetX(Pointer ptr);
  int mappableGetY(Pointer ptr);

  int playerGetId(Pointer ptr);
  String playerGetPlayerName(Pointer ptr);
  float playerGetTime(Pointer ptr);
  int playerGetWaterStored(Pointer ptr);
  int playerGetSpawnRate(Pointer ptr);

  int tileGetId(Pointer ptr);
  int tileGetX(Pointer ptr);
  int tileGetY(Pointer ptr);
  int tileGetOwner(Pointer ptr);
  int tileGetType(Pointer ptr);
  int tileGetResId(Pointer ptr);
  int tileGetWaterAmount(Pointer ptr);
  int tileGetIsTrench(Pointer ptr);

  int unitGetId(Pointer ptr);
  int unitGetX(Pointer ptr);
  int unitGetY(Pointer ptr);
  int unitGetOwner(Pointer ptr);
  int unitGetType(Pointer ptr);
  int unitGetCurHealth(Pointer ptr);
  int unitGetCurMovement(Pointer ptr);
  int unitGetMaxMovement(Pointer ptr);


    //properties

}
