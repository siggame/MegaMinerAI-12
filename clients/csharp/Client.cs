using System;
using System.Runtime.InteropServices;

public class Client {
  [DllImport("client")]
  public static extern IntPtr createConnection();
  [DllImport("client")]
  public static extern int serverConnect(IntPtr connection, string host, string port);

  [DllImport("client")]
  public static extern int serverLogin(IntPtr connection, string username, string password);
  [DllImport("client")]
  public static extern int createGame(IntPtr connection);
  [DllImport("client")]
  public static extern int joinGame(IntPtr connection, int id, string playerType);

  [DllImport("client")]
  public static extern void endTurn(IntPtr connection);
  [DllImport("client")]
  public static extern void getStatus(IntPtr connection);

  [DllImport("client")]
  public static extern int networkLoop(IntPtr connection);


    //commands
  [DllImport("client")]
  public static extern int playerTalk(IntPtr self, string message);
  [DllImport("client")]
  public static extern int tileSpawn(IntPtr self, int type);
  [DllImport("client")]
  public static extern int unitMove(IntPtr self, int x, int y);
  [DllImport("client")]
  public static extern int unitAttack(IntPtr self, int unit);
  [DllImport("client")]
  public static extern int unitFill(IntPtr self, int tile);
  [DllImport("client")]
  public static extern int unitBuild(IntPtr self, int tile);

    //accessors
  [DllImport("client")]
  public static extern int getMaxHealth(IntPtr connection);
  [DllImport("client")]
  public static extern int getTrenchDamage(IntPtr connection);
  [DllImport("client")]
  public static extern int getWaterDamage(IntPtr connection);
  [DllImport("client")]
  public static extern int getTurnNumber(IntPtr connection);
  [DllImport("client")]
  public static extern int getAttackDamage(IntPtr connection);
  [DllImport("client")]
  public static extern int getOffenseCount(IntPtr connection);
  [DllImport("client")]
  public static extern int getDefenseCount(IntPtr connection);
  [DllImport("client")]
  public static extern int getMaxUnits(IntPtr connection);

  [DllImport("client")]
  public static extern IntPtr getPumpStation(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getPumpStationCount(IntPtr connection);
  [DllImport("client")]
  public static extern IntPtr getMappable(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getMappableCount(IntPtr connection);
  [DllImport("client")]
  public static extern IntPtr getPlayer(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getPlayerCount(IntPtr connection);
  [DllImport("client")]
  public static extern IntPtr getTile(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getTileCount(IntPtr connection);
  [DllImport("client")]
  public static extern IntPtr getUnit(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getUnitCount(IntPtr connection);


    //getters
  [DllImport("client")]
  public static extern int pumpStationGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern int pumpStationGetOwner(IntPtr ptr);
  [DllImport("client")]
  public static extern int pumpStationGetWaterAmount(IntPtr ptr);
  [DllImport("client")]
  public static extern int pumpStationGetSeigeCount(IntPtr ptr);

  [DllImport("client")]
  public static extern int mappableGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern int mappableGetX(IntPtr ptr);
  [DllImport("client")]
  public static extern int mappableGetY(IntPtr ptr);

  [DllImport("client")]
  public static extern int playerGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern IntPtr playerGetPlayerName(IntPtr ptr);
  [DllImport("client")]
  public static extern float playerGetTime(IntPtr ptr);
  [DllImport("client")]
  public static extern int playerGetWaterStored(IntPtr ptr);
  [DllImport("client")]
  public static extern int playerGetSpawnRate(IntPtr ptr);

  [DllImport("client")]
  public static extern int tileGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern int tileGetX(IntPtr ptr);
  [DllImport("client")]
  public static extern int tileGetY(IntPtr ptr);
  [DllImport("client")]
  public static extern int tileGetOwner(IntPtr ptr);
  [DllImport("client")]
  public static extern int tileGetType(IntPtr ptr);
  [DllImport("client")]
  public static extern int tileGetResId(IntPtr ptr);
  [DllImport("client")]
  public static extern int tileGetWaterAmount(IntPtr ptr);
  [DllImport("client")]
  public static extern int tileGetIsTrench(IntPtr ptr);

  [DllImport("client")]
  public static extern int unitGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern int unitGetX(IntPtr ptr);
  [DllImport("client")]
  public static extern int unitGetY(IntPtr ptr);
  [DllImport("client")]
  public static extern int unitGetOwner(IntPtr ptr);
  [DllImport("client")]
  public static extern int unitGetType(IntPtr ptr);
  [DllImport("client")]
  public static extern int unitGetCurHealth(IntPtr ptr);
  [DllImport("client")]
  public static extern int unitGetCurMovement(IntPtr ptr);
  [DllImport("client")]
  public static extern int unitGetMaxMovement(IntPtr ptr);


    //properties

}
