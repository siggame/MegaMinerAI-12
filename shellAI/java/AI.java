import com.sun.jna.Pointer;




///The class implementing gameplay logic.
public class AI extends BaseAI {
    //List for spawning units
    public static final int WORKER = 0, SCOUT = 1, TANK = 2;

    public String username() {
        return "Shell AI";
    }

    public String password() {
        return "password";
    }

    //This function is called once, before your first turn
    public void init() {
    }

    //This function is called each time it is your turn
    //Return true to end your turn, return false to ask the server for updated information
    public boolean run() {
        int numberOfUnits = 0;
        //get the number of units owned
        for(int i = 0; i < units.length; i++)
        {
            //if I own this unit increase the count
            if(units[i].getOwner() == playerID())
            {
                numberOfUnits++;
            }
        }
        //look for my tiles
        for(int i = 0; i < tiles.length; i++)
        {
            //if this tile is my spawn tile or my pump station
            if(tiles[i].getOwner() == playerID())
            {
                //get the unit cost for a worker
                int cost = Integer.MAX_VALUE;
                for(int j = 0; j < unitTypes.length; j++)
                {
                    if(unitTypes[j].getType() == WORKER)
                    {
                        cost = unitTypes[j].getCost();
                    }
                }
                //if there is enough oxygen to spawn the unit
                if(players[playerID()].getOxygen() >= cost)
                {
                    //if can spawn more units in
                    if(numberOfUnits < maxUnits())
                    {
                        //if nothing is spawning on the tile
                        if(tiles[i].getIsSpawning()==0)
                        {
                            boolean canSpawn = true;
                            //if it is a pump station and it's not being seiged
                            if(tiles[i].getPumpID() != -1)
                            {
                                //find the pump in the vector
                                for(int j = 0; j < pumpStations.length; j++)
                                {
                                    //if it's being sieged, don't spawn
                                    if(pumpStations[j].getId() == tiles[i].getPumpID() &&
                                            pumpStations[j].getSiegeAmount() > 0)
                                    {
                                        canSpawn = false;
                                    }
                                }
                            }
                            //if there is someone else on the tile, don't spawn
                            for(int j = 0; j < units.length; j++)
                            {
                                if(tiles[i].getX() == units[j].getX() &&
                                        tiles[i].getY() == units[j].getY())
                                {
                                    canSpawn = false;
                                }
                            }
                            if(canSpawn)
                            {
                                //spawn the unit
                                tiles[i].spawn(WORKER);
                                //increment unit count
                                numberOfUnits++;
                            }
                        }
                    }
                }
            }
        }
        int moveDelta = 0;
        //set to move left or right based on id; towards the center
        if(playerID() == 0)
        {
            moveDelta = 1;
        }
        else
        {
            moveDelta = -1;
        }
        //do stuff for each unit
        for(int i = 0; i < units.length; i++)
        {
            //if you own the unit
            if(units[i].getOwner() != playerID())
            {
                //ignore it if it isn't
                continue;
            }
            //try to move to the right or left movement times
            for(int z = 0; z < units[i].getMaxMovement(); z++)
            {
                boolean canMove = true;
                //if there is no unit there
                for(int j = 0; j < units.length; j++)
                {
                    if(units[i].getX() + moveDelta == units[j].getX() &&
                            units[i].getY() == units[j].getY())
                    {
                        canMove = false;
                    }
                }
                //if nothing's there and it's not moving off the edge of the map
                if(canMove &&
                        units[i].getX() + moveDelta >= 0 &&
                        units[i].getX() + moveDelta < mapWidth())
                {
                    //if the tile is not an enemy spawn point
                    if(!(tiles[(units[i].getX() + moveDelta) * mapHeight() + units[i].getY()].getPumpID() == -1 &&
                            tiles[(units[i].getX() + moveDelta) * mapHeight() + units[i].getY()].getOwner() == 1 - playerID()) ||
                            tiles[(units[i].getX() + moveDelta) * mapHeight() + units[i].getY()].getOwner() == 2)
                    {
                        //if the tile is not an ice tile
                        if(!(tiles[(units[i].getX() + moveDelta) * mapHeight() + units[i].getY()].getOwner() == 3 &&
                                tiles[(units[i].getX() + moveDelta) * mapHeight() + units[i].getY()].getWaterAmount() > 0))
                        {
                            //if the tile is not spawning anything
                            if((tiles[(units[i].getX() + moveDelta) * mapHeight() + units[i].getY()].getIsSpawning())==0)
                            {
                                //if the unit is alive
                                if(units[i].getHealthLeft() > 0)
                                {
                                    //move the unit
                                    units[i].move(units[i].getX() + moveDelta, units[i].getY());
                                }
                            }
                        }
                    }
                }
            }
            //if there is an enemy in the movement direction and the unit hasn't
            //attacked and it is alive
            if(units[i].getHasAttacked() == 0 && units[i].getHealthLeft() > 0)
            {
                for(int j = 0; j < units.length; j++)
                {
                    //check if there is a enemy unit in the direction
                    if(units[i].getX() + moveDelta == units[j].getX() &&
                            units[i].getY() == units[j].getY() &&
                            units[j].getOwner() != playerID())
                    {
                        //attack it
                        units[i].attack(units[j]);
                        break;
                    }
                }
            }
            //if there is a space to dig below the unit and the unit hasn't dug
            //and the unit is alive
            if(units[i].getY() != mapHeight() - 1 &&
                    tiles[units[i].getX() * mapHeight() + units[i].getY() + 1].getPumpID() == -1 &&
                    tiles[units[i].getX() * mapHeight() + units[i].getY() + 1].getOwner() == 2 &&
                    units[i].getHasDug() == 0 &&
                    units[i].getHealthLeft() > 0)
            {
                boolean canDig = true;
                //make sure there is no unit on that tile
                for(int j = 0; j < units.length; j++)
                {
                    if(units[i].getX() == units[j].getX() &&
                            units[i].getY() + 1 == units[j].getY())
                    {
                        canDig = false;
                    }
                }
                //make sure the tile is not an ice tile
                if(canDig &&
                        !(tiles[units[i].getX() * mapHeight() + units[i].getY() + 1].getOwner() == 3 &&
                                tiles[units[i].getX() * mapHeight() + units[i].getY() + 1].getWaterAmount() > 0))
                {
                    units[i].dig(tiles[units[i].getX() * mapHeight() + units[i].getY() + 1]);
                }
            }
        }
        return true;
    }


    //This function is called once, after your last turn
    public void end() {
    }


    public AI(Pointer c) {
        super(c);
    }
}
