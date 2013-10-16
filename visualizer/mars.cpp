#include "mars.h"
#include "marsAnimatable.h"
#include "frame.h"
#include "version.h"
#include "animations.h"
#include <utility>
#include <time.h>
#include <list>

namespace visualizer
{

Mars::Mars()
{
	m_game = 0;
	m_suicide=false;
} // Mars::Mars()

Mars::~Mars()
{
	destroy();
}

void Mars::destroy()
{
	m_suicide=true;
	wait();
	animationEngine->registerGame(0, 0);

	clear();
	delete m_game;
	m_game = 0;

	// Clear your memory here

	programs.clear();

} // Mars::~Mars()

void Mars::GetSelectedRect(Rect &out) const
{
	const Input& input = gui->getInput();

	int x = input.x;
	int y = input.y /*- SEA_OFFSET*/;
	int width = input.sx - x;
	int height = input.sy - y;

	int right = x + width;
	int bottom = y + height /*- SEA_OFFSET*/;

	out.left = min(x,right);
	out.top = min(y,bottom);
	out.right = max(x,right);
	out.bottom = max(y,bottom);
}

void Mars::ProccessInput()
{
	const Input& input = gui->getInput();
	int unitsSelectable = gui->getDebugOptionState("Units Selectable");
	int tilesSelectable = gui->getDebugOptionState("Tiles Selectable");

	if( input.leftRelease )
	{
		int turn = timeManager->getTurn();

		Rect R;
		GetSelectedRect(R);

		m_selectedUnitIDs.clear();

        if(unitsSelectable)
        {
            for(auto& iter : m_game->states[ turn ].units)
            {
                const auto& unit = iter.second;

                // todo: move this logic into another function
                if(R.left <= unit.x && R.right >= unit.x && R.top <= unit.y && R.bottom >= unit.y)
                {
                    m_selectedUnitIDs.push_back(unit.id);
                }
            }
        }

        if(tilesSelectable)
        {
            for(auto& iterCol : m_Tiles)
            {
                for(auto& tile : iterCol)
                {
                    if(R.left <= tile.x && R.right >= tile.x && R.top <= tile.y && R.bottom >= tile.y)
                    {
                        m_selectedUnitIDs.push_back(tile.id);
                    }
                }
            }
        }

        gui->updateDebugWindow();
        gui->updateDebugUnitFocus();
		cout<<"Selected Units:" << m_selectedUnitIDs.size() << endl;
	}
}

void Mars::drawObjectSelection() const
{
	int turn = timeManager->getTurn();

	for(auto& iter : m_selectedUnitIDs)
	{
		drawQuadAroundObj(m_game->states[turn].units,iter);
	}

	for(auto& unitID : m_selectedUnitIDs)
	{
        for(auto& iterCol : m_Tiles)
            for(auto& tile : iterCol)
                if(tile.id == unitID)
                    drawQuadAroundObj(tile, glm::vec4(0.3, 0.0, 1.0, 0.6));
	}

	int focus = gui->getCurrentUnitFocus();

    if(focus >= 0)
    {
        auto iter = m_game->states[turn].units.find(focus);
        if(iter != m_game->states[turn].units.end())
            drawBoxAroundObj(m_game->states[turn].units.at(focus), glm::vec4(1.0f, 1.0f, 0.0f, 1.0f));

        for(auto& iterCol : m_Tiles)
            for(auto& tile : iterCol)
                if(focus == tile.id)
                    drawBoxAroundObj(tile, glm::vec4(1.0f, 1.0f, 0.0f, 1.0f));
    }
}

void Mars::drawBoxAroundObj(const parser::Mappable& obj, const glm::vec4& color) const
{
    renderer->setColor(Color(color.r, color.g, color.b, color.a));
    renderer->drawLine(obj.x + 0.1f, obj.y + 0.1f, obj.x + 0.9, obj.y + 0.1);
    renderer->drawLine(obj.x + 0.1f, obj.y + 0.1f, obj.x + 0.1, obj.y + 0.9);
    renderer->drawLine(obj.x + 0.9f, obj.y + 0.1f, obj.x + 0.9, obj.y + 0.9);
    renderer->drawLine(obj.x + 0.1f, obj.y + 0.9f, obj.x + 0.9, obj.y + 0.9);
}

void Mars::drawQuadAroundObj(const parser::Mappable& obj, const glm::vec4& color) const
{
    renderer->setColor( Color( color.r, color.g, color.b, color.a) );
    renderer->drawQuad(obj.x,obj.y,1,1);
}

void Mars::preDraw()
{
	ProccessInput();

    renderer->setColor(Color());
    renderer->drawTexturedQuad(0.0f,0.0f,m_game->states[0].mapWidth,m_game->states[0].mapHeight,"dirt");

	drawGrid();

// Handle player input here
}

void Mars::postDraw()
{
	drawObjectSelection();
}

void Mars::drawGrid()
{
      bool bEnableGrid = options->getNumber("Enable Grid") > 0;
      if(bEnableGrid)
      {
		unsigned int h = m_game->states[0].mapHeight;
		unsigned int w = m_game->states[0].mapWidth;

        //draw horizontal lines
        renderer->setColor(Color(0.0f,0.0f,0.0f,1.0f));
        for(unsigned int i = 0; i < h; i++)
        {
            renderer->drawLine(0,i,w,i,1.0f);
        }

        //draw vertical lines
        for(unsigned int i = 0; i < w; i++)
        {
            renderer->drawLine(i,0,i,h,1.0f);
        }
      }
}

PluginInfo Mars::getPluginInfo()
{
	PluginInfo i;
	i.searchLength = 1000;
	i.gamelogRegexPattern = "Mars";
	i.returnFilename = false;
	i.spectateMode = false;
	i.pluginName = "MegaMinerAI: Mars Plugin";


	return i;
} // PluginInfo Mars::getPluginInfo()

void Mars::setup()
{
	gui->checkForUpdate( "Mars", "./plugins/mars/checkList.md5", VERSION_FILE );
	options->loadOptionFile( "./plugins/mars/mars.xml", "mars" );
	resourceManager->loadResourceFile( "./plugins/mars/resources.r" );
}

// Give the Debug Info widget the selected object IDs in the Gamelog
list<int> Mars::getSelectedUnits()
{
	return m_selectedUnitIDs;
}

list<std::string> Mars::getDebugOptions()
{
    return std::list<std::string>({"Units Selectable", "Tiles Selectable"});
}

void Mars::loadGamelog( std::string gamelog )
{
	if(isRunning())
	{
		m_suicide = true;
		wait();
	}
	m_suicide = false;

	// BEGIN: Initial Setup
	setup();

	delete m_game;
	m_game = new parser::Game;

	if( !parser::parseGameFromString( *m_game, gamelog.c_str() ) )
	{
		delete m_game;
		m_game = 0;
		WARNING("Cannot load gamelog, %s",gamelog.c_str());
	}

	// END: Initial Setup

	// Setup the renderer as a 4 x 4 map by default
	// TODO: Change board size to something useful
	renderer->setCamera( 0, 0, m_game->states[0].mapWidth, m_game->states[0].mapHeight);
	renderer->setGridDimensions( m_game->states[0].mapWidth, m_game->states[0].mapHeight);

	m_selectedUnitIDs.clear();

	start();
} // Mars::loadGamelog()

void Mars::BuildWorld()
{
    // start by setting up the tiles in a multi-dimensional array
    m_Tiles.resize(m_game->states[0].mapWidth);
    for(auto& v: m_Tiles)
    {
        v.resize(m_game->states[0].mapHeight);
    }

    for(auto& tileIter: m_game->states[0].tiles)
    {
        std::cout << tileIter.second.x << ", " << tileIter.second.y << std::endl;
        m_Tiles[tileIter.second.x][tileIter.second.y] = tileIter.second;
    }

    // set up the unit map so that the index is it's id, the second is the unit itself
    for(auto& unitIter: m_game->states[0].units)
    {
        m_Units[unitIter.second.id] = unitIter.second;
    }
}

void Mars::UpdateWorld(int state)
{
    for(auto& tileIter: m_game->states[state].tiles)
    {
        m_Tiles[tileIter.second.x][tileIter.second.y] = tileIter.second;
    }

    for(auto& UnitIter: m_game->states[state].units)
    {
        m_Units[UnitIter.second.id] = UnitIter.second;
    }

}

void Mars::RenderWorld(int state, std::deque<glm::ivec2>& trail, vector<vector<int>>& trailMap, Frame& turn)
{
    for(auto& row : m_Tiles)
    {
        for(auto& tileIter : row)
        {
            std::string texture;

            // if there is water then render water
            if(tileIter.owner == 3) // if the tile is a glacier
            {
                texture = "glacier";
            }
            else if(tileIter.waterAmount != 0)
            {
                texture = "water";
            }
            else if(tileIter.isTrench == true) // if there is no water, but a trench then render a trench
            {
                texture = "trench";
            }

            if(!texture.empty())
            {
                SmartPointer<BaseSprite> pTile = new BaseSprite(glm::vec2(tileIter.x, tileIter.y), glm::vec2(1.0f, 1.0f), texture);
                pTile->addKeyFrame(new DrawSprite(pTile, glm::vec4(1.0f, 1.0f, 1.0f,0.8f)));
                turn.addAnimatable(pTile);

				// if there is water then render water
				if(tileIter.owner == 3) // if the tile is a glacier
				{
					texture = "glacier";
				}
				else if(tileIter.waterAmount != 0)
				{
					texture = "water";
				}
				else if(tileIter.isTrench == true) // if there is no water, but a trench then render a trench
				{
					texture = "trench";
				}

				if(!texture.empty())
				{
					SmartPointer<BaseSprite> pTile = new BaseSprite(glm::vec2(tileIter.x, tileIter.y), glm::vec2(1.0f, 1.0f), texture);
					pTile->addKeyFrame(new DrawSprite(pTile, glm::vec4(1.0f, 1.0f, 1.0f,0.8f)));
					turn.addAnimatable(pTile);
				}

                // Canal Overlays
				if(tileIter.isTrench == true && tileIter.owner != 3)
				{
					int surroundingTrenches = 0;
					bool North = false, South = false, East = false, West = false;
					bool NorthWest = false, NorthEast = false, SouthWest = false, SouthEast = false;
					std::string overlayTexture;
					int overlayRotation = 0;

                    // STEP 1: figure out if all the trenches adjacent to this one are also
                    //         trenches, INCLUDING diagonals.
                    //         If they are are directly adjacent, (not diagonal) AND also a
                    //         trench, then you will need a trench overlay with one less channel.
					if(tileIter.y > 0 &&
                      (GetTileAt(tileIter.x, tileIter.y - 1).isTrench == true ||
					   GetTileAt(tileIter.x, tileIter.y - 1).owner == 3))
					{
						surroundingTrenches++;
						North = true;
					}

					if(tileIter.y < m_game->states[state].mapHeight - 1 &&
                      (GetTileAt(tileIter.x, tileIter.y + 1).isTrench == true ||
					   GetTileAt(tileIter.x, tileIter.y + 1).owner == 3))
					{
						surroundingTrenches++;
						South = true;
					}

					if(tileIter.x > 0 &&
                      (GetTileAt(tileIter.x - 1, tileIter.y).isTrench == true ||
					   GetTileAt(tileIter.x - 1, tileIter.y).owner == 3))
					{
						surroundingTrenches++;
						West = true;
					}

					if(tileIter.x < m_game->states[state].mapWidth - 1 &&
                      (GetTileAt(tileIter.x + 1, tileIter.y).isTrench == true ||
					   GetTileAt(tileIter.x + 1, tileIter.y).owner == 3))
					{
						surroundingTrenches++;
						East = true;
					}

					if(tileIter.x > 0 && tileIter.y > 0 &&
                      (GetTileAt(tileIter.x - 1, tileIter.y - 1).isTrench == true  ||
                       GetTileAt(tileIter.x - 1, tileIter.y - 1).owner == 3))
					{
                        NorthWest = true;
					}

					if(tileIter.x < m_game->states[state].mapWidth - 1 && tileIter.y > 0 &&
                      (GetTileAt(tileIter.x + 1, tileIter.y - 1).isTrench == true ||
                       GetTileAt(tileIter.x + 1, tileIter.y - 1).owner == 3))
                    {
                        NorthEast = true;
                    }

                    if(tileIter.x > 0 && tileIter.y < m_game->states[state].mapHeight - 1 &&
                      (GetTileAt(tileIter.x - 1, tileIter.y + 1).isTrench == true ||
                       GetTileAt(tileIter.x - 1, tileIter.y + 1).owner == 3))
                    {
                        SouthWest = true;
                    }

                    if(tileIter.x < m_game->states[state].mapWidth - 1 &&
                       tileIter.y < m_game->states[state].mapHeight - 1 &&
                      (GetTileAt(tileIter.x + 1, tileIter.y + 1).isTrench == true ||
                       GetTileAt(tileIter.x + 1, tileIter.y + 1).owner == 3))
                    {
                        SouthEast = true;
                    }

                    // STEP 2: given the number of directly adjacent, (not diagonal),
                    //     trenches, figure which sprite you (number of channels), and
                    //     given which ones in particular, figure the directions the
                    //     sprite should be facing to meet adjoining trenches
					switch(surroundingTrenches)
					{
					case 0:
						overlayTexture = "trench_hole";
						overlayRotation = 0;
						break;
					case 1:
						overlayTexture = "trench_tail";
						if(North)
							overlayRotation = 0;
						else if(East)
							overlayRotation = 90;
						else if(South)
							overlayRotation = 180;
						else
							overlayRotation = 270;
						break;
					case 2:
						if((North && South) || (East && West))
						{
							overlayTexture = "trench_canal";
							if(North && South)
								overlayRotation = 0;
							else
								overlayRotation = 90;
						}
						else
						{
							overlayTexture = "trench_corner";
							if(East && South)
								overlayRotation = 0;
							else if(South && West)
								overlayRotation = 90;
							else if(West && North)
                                overlayRotation = 180;
							else
								overlayRotation = 270;
						}
						break;
					case 3:
						overlayTexture = "trench_wall";
						if(!North)
							overlayRotation = 90;
						else if(!West)
							overlayRotation = 0;
						else if(!South)
							overlayRotation = 270;
						else
							overlayRotation = 180;

						break;
					case 4:
						break;
					}

                    // STEP 3: If there is an overlay to render on the trench, (meaning there are less than 4 channels needed), then render
                    //     the overlay, given the rotation specified ealier.
					if(!overlayTexture.empty())
					{
						SmartPointer<BaseSprite> pTile = new BaseSprite(glm::vec2(tileIter.x, tileIter.y), glm::vec2(1.0f, 1.0f), overlayTexture);
						pTile->addKeyFrame(new DrawRotatedSprite(pTile, glm::vec4(1.0f, 1.0f, 1.0f,1.0f), overlayRotation));
						turn.addAnimatable(pTile);
					}

                    // STEP 4 (optional) :  if a little corner bit is required, (only needed for 3 2-channel-corner
                    // 3-channel and 4 channel overlay), then figure out which corners need to be rendered. For example
                    // if you have a trench to the north and east, but not a trench in the NorthEast, you will need a corner
                    // bit to make the turn smooth. Then you render that corner bit directly on the tile.
					if(overlayTexture == "trench_corner")
					{
                        float tipRotation = -1.0f;

                        if(overlayRotation == 0 && !SouthEast) // if south and east are trenches, AND SouthEast isn't a trench
                            tipRotation = 180;                 // then put a tip in the southeast corner
                        else if(overlayRotation == 90 && !SouthWest) // if south and west are trenches, AND SouthEast isn't a trench
                            tipRotation = 270;                       // then put a tip in the southwest corner
                        else if(overlayRotation == 180 && !NorthWest) // if north and west are trenches, AND NorthWest isn't a trench
                            tipRotation = 0;                          // then put a tip in northwest corner
                        else if(overlayRotation == 270 && !NorthEast) // if north and east are trenches, AND NorthEast isn't a trench
                            tipRotation = 90;                         // then put a tip in the northeast corner

                        if(tipRotation >= 0)
                        {
                            SmartPointer<BaseSprite> pTip = new BaseSprite(glm::vec2(tileIter.x, tileIter.y), glm::vec2(1.0f, 1.0f), "trench_tip");
                            pTip->addKeyFrame(new DrawRotatedSprite(pTip, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f), tipRotation));
                            turn.addAnimatable(pTip);
                        }
					}

					if(overlayTexture == "trench_wall")
					{
                        float tip1Rotation = -1.0f;
                        float tip2Rotation = -1.0f;

                        if(overlayRotation == 90)   // if the wall is to the north, then check southwest and southeast corners
                        {
                            if(!SouthEast)
                                tip1Rotation = 180;
                            if(!SouthWest)
                                tip2Rotation = 270;
                        }
                        else if(overlayRotation == 0) // if the wall is to the west, then check the northeast and southeast corners
                        {
                            if(!NorthEast)
                                tip1Rotation = 90;
                            if(!SouthEast)
                                tip2Rotation = 180;
                        }
                        else if(overlayRotation == 270) // if the wall is to the south, then check the northwest and southeast corners
                        {
                            if(!NorthWest)
                                tip1Rotation = 0;
                            if(!NorthEast)
                                tip2Rotation = 90;
                        }
                        else if(overlayRotation == 180) // if the wall is to the east, then check the northwest and southwest corners
                        {
                            if(!NorthWest)
                                tip1Rotation = 0;
                            if(!SouthWest)
                                tip2Rotation = 270;
                        }

                        if(tip1Rotation >= 0)
                        {
                            SmartPointer<BaseSprite> pTip = new BaseSprite(glm::vec2(tileIter.x, tileIter.y), glm::vec2(1.0f, 1.0f), "trench_tip");
                            pTip->addKeyFrame(new DrawRotatedSprite(pTip, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f), tip1Rotation));
                            turn.addAnimatable(pTip);
                        }

                        if(tip2Rotation >= 0)
                        {
                            SmartPointer<BaseSprite> pTip = new BaseSprite(glm::vec2(tileIter.x, tileIter.y), glm::vec2(1.0f, 1.0f), "trench_tip");
                            pTip->addKeyFrame(new DrawRotatedSprite(pTip, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f), tip2Rotation));
                            turn.addAnimatable(pTip);
                        }
					}

					if(surroundingTrenches == 4)
					{
                        float tip1Rotation = -1.0f;
                        float tip2Rotation = -1.0f;
                        float tip3Rotation = -1.0f;
                        float tip4Rotation = -1.0f;

                        if(!NorthWest) // if the northwest isn't a trench, then it needs a tip and so on...
                            tip1Rotation = 0;
                        if(!NorthEast)
                            tip2Rotation = 90;
                        if(!SouthEast)
                            tip3Rotation = 180;
                        if(!SouthWest)
                            tip4Rotation = 270;

                        if(tip1Rotation >= 0)
                        {
                            SmartPointer<BaseSprite> pTip = new BaseSprite(glm::vec2(tileIter.x, tileIter.y), glm::vec2(1.0f, 1.0f), "trench_tip");
                            pTip->addKeyFrame(new DrawRotatedSprite(pTip, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f), tip1Rotation));
                            turn.addAnimatable(pTip);
                        }

                        if(tip2Rotation >= 0)
                        {
                            SmartPointer<BaseSprite> pTip = new BaseSprite(glm::vec2(tileIter.x, tileIter.y), glm::vec2(1.0f, 1.0f), "trench_tip");
                            pTip->addKeyFrame(new DrawRotatedSprite(pTip, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f), tip2Rotation));
                            turn.addAnimatable(pTip);
                        }

                        if(tip3Rotation >= 0)
                        {
                            SmartPointer<BaseSprite> pTip = new BaseSprite(glm::vec2(tileIter.x, tileIter.y), glm::vec2(1.0f, 1.0f), "trench_tip");
                            pTip->addKeyFrame(new DrawRotatedSprite(pTip, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f), tip3Rotation));
                            turn.addAnimatable(pTip);
                        }

                        if(tip4Rotation >= 0)
                        {
                            SmartPointer<BaseSprite> pTip = new BaseSprite(glm::vec2(tileIter.x, tileIter.y), glm::vec2(1.0f, 1.0f), "trench_tip");
                            pTip->addKeyFrame(new DrawRotatedSprite(pTip, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f), tip4Rotation));
                            turn.addAnimatable(pTip);
                        }
					}
				}

                // Water amount display on water filled trenches
				if(tileIter.waterAmount != 0)
				{
                    std::ostringstream waterAmountString;
                    SmartPointer<Animatable> pText = new Animatable;
                    waterAmountString << tileIter.waterAmount;
                    DrawTextBox * textBox = new DrawTextBox(waterAmountString.str(),
                                                            glm::vec2(tileIter.x + 0.5, tileIter.y + 0.25),
                                                            glm::vec4(0.0f,0.0f,0.0f,1.0f),
                                                            2.0f,
                                                            "Roboto");

                    pText->addKeyFrame(textBox);
                    turn.addAnimatable(pText);
				}
            }

            turn[tileIter.id]["owner"] = tileIter.owner;
            turn[tileIter.id]["type"] = tileIter.type;
            turn[tileIter.id]["pumpID"] = tileIter.pumpID;
            turn[tileIter.id]["waterAmount"] = tileIter.waterAmount;
            turn[tileIter.id]["isTrench"] = tileIter.isTrench;
            turn[tileIter.id]["x"] = tileIter.x;
            turn[tileIter.id]["y"] = tileIter.y;
            turn[tileIter.id]["id"] = tileIter.id;
        }
    }

	// todo: clean this up
	for(auto iter = trail.begin(); iter != trail.end();)
	{
		ColorSprite::Fade fade = ColorSprite::None;
		if(trailMap[iter->y][iter->x] == 0)
		{
			fade = ColorSprite::FadeOut;
		}

		// First Draw trail at iter->second
		SmartPointer<BaseSprite> pTile = new BaseSprite(glm::vec2(iter->x, iter->y), glm::vec2(1.0f, 1.0f), "trail");
		pTile->addKeyFrame(new DrawSprite(pTile, glm::vec4(1.0f, 1.0f, 1.0f,0.3f),fade));
		turn.addAnimatable(pTile);

		// Then pop them if turnDiff > n
		if(trailMap[iter->y][iter->x] == 0)
		{
			iter = trail.erase(iter);
		}
		else
		{
			--trailMap[iter->y][iter->x];
			++iter;
		}
	}

    // For each UNIT in the frame
	auto unitIter = m_Units.begin();
	while(unitIter != m_Units.end())
	{
        SmartPointer<MoveableSprite> pUnit = new MoveableSprite("digger");
		pUnit->addKeyFrame(new DrawSmoothMoveSprite(pUnit, unitIter->second.owner == 1? glm::vec4(0.8f,0.2f,0.2f,1.0f) : glm::vec4(0.2f,0.2f,0.8f,1.0f) ));
        turn.addAnimatable(pUnit);

		for(auto& animationIter : m_game->states[state].animations[unitIter->second.id])
        {
            if(animationIter->type == parser::MOVE)
            {
                parser::move& move = (parser::move&)*animationIter;
                pUnit->m_Moves.push_back(MoveableSprite::Move(glm::vec2(move.toX, move.toY), glm::vec2(move.fromX, move.fromY)));

				if(trailMap[move.toY][move.toX] == 0)
				{
					trail.push_back(glm::ivec2(move.toX, move.toY));
				}

				// todo: move the path length var into a const
				trailMap[move.toY][move.toX] = 5;
            }
        }

        if(pUnit->m_Moves.empty())
		{
			pUnit->m_Moves.push_back(MoveableSprite::Move(glm::vec2(unitIter->second.x, unitIter->second.y), glm::vec2(unitIter->second.x, unitIter->second.y)));
			trailMap[unitIter->second.y][unitIter->second.x] = 5;
		}

		turn[unitIter->second.id]["owner"] = unitIter->second.owner;
		turn[unitIter->second.id]["hasAttacked"] = unitIter->second.hasAttacked;
		turn[unitIter->second.id]["hasDigged"] = unitIter->second.hasDigged;
		turn[unitIter->second.id]["hasBuilt"] = unitIter->second.hasBuilt;
		turn[unitIter->second.id]["healthLeft"] = unitIter->second.healthLeft;
		turn[unitIter->second.id]["maxHealth"] = unitIter->second.maxHealth;
		turn[unitIter->second.id]["movementLeft"] = unitIter->second.movementLeft;
		turn[unitIter->second.id]["maxMovement"] = unitIter->second.maxMovement;
		turn[unitIter->second.id]["X"] = unitIter->second.x;
		turn[unitIter->second.id]["Y"] = unitIter->second.y;

		// todo: this line of code could be simplified
		if((state < (int)(m_game->states.size() - 1)) && (m_game->states[state + 1].units.find(unitIter->first) == m_game->states[state + 1].units.end()))
		//if(unitIter->second.healthLeft <= 0)
		{
			cout << "Die at: " << unitIter->second.healthLeft << endl;
			unitIter = m_Units.erase(unitIter);
		}
		else
		{
			++unitIter;
		}

    }
}

parser::Tile& Mars::GetTileAt(int x, int y)
{
    return m_Tiles[x][y];
}

// The "main" function
void Mars::run()
{
    gui->setDebugOptions(this);

	timeManager->setNumTurns( 0 );

	animationEngine->registerGame(0, 0);

	const char* playerName = m_game->states[0].players[m_game->winner].playerName;
	SmartPointer<SplashScreen> splashScreen = new SplashScreen(m_game->winReason,playerName,
															   m_game->states[0].mapWidth,
															   m_game->states[0].mapHeight
															   );
	
	splashScreen->addKeyFrame(new DrawSplashScreen(splashScreen));

    BuildWorld();

	std::deque<glm::ivec2> trail;

	// todo: maybe flip this so that x is first, then y
	std::vector<std::vector<int>> trailMap(m_game->states[0].mapHeight);
	for(auto& idMapiter : trailMap)
	{
		idMapiter.resize(m_game->states[0].mapWidth,0);
	}

	// Look through each turn in the gamelog
	for(int state = 0; state < (int)m_game->states.size() && !m_suicide; state++)
	{
		Frame turn;  // The frame that will be drawn

        UpdateWorld(state);
		RenderWorld(state, trail, trailMap, turn);

		if(state >= (int)(m_game->states.size() - 10))
		{
			turn.addAnimatable(splashScreen);
		}

        animationEngine->buildAnimations(turn);
        addFrame(turn);

        // Register the game and begin playing delayed due to multithreading
        if(state > 5)
        {
            timeManager->setNumTurns(state - 5);
            animationEngine->registerGame( this, this );
            if(state == 6)
            {
                animationEngine->registerGame(this, this);
                timeManager->setTurn(0);
                timeManager->play();
            }
        }
        else
        {
            timeManager->setNumTurns(state);
            animationEngine->registerGame( this, this );
            animationEngine->registerGame(this, this);
            timeManager->setTurn(0);
            timeManager->play();
        }
	}

	if(!m_suicide)
	{
		timeManager->setNumTurns( m_game->states.size() );
		timeManager->play();
	}

} // Mars::run()

} // visualizer

Q_EXPORT_PLUGIN2( Mars, visualizer::Mars );
