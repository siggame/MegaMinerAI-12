#include "mars.h"
#include "marsAnimatable.h"
#include "frame.h"
#include "version.h"
#include "animations.h"
#include <utility>
#include <time.h>
#include <list>
#include <queue>
#include <set>
#include <iomanip>

#include <glm/glm.hpp>

namespace visualizer
{

void RenderProgressBar(const IRenderer& renderer,
						   float xPos, float yPos,
						   float width, float height,
						   float percent, const Color& col, bool bDrawText)
{
	// Render the health bars
	renderer.setColor(Color(0.4f,0.4f,0.4f,1.0f));
	renderer.drawQuad(xPos + width,yPos, -(1.0f - percent) * width, height); // height

	renderer.setColor(col);
	renderer.drawQuad(xPos,yPos, percent * width, height);

	if(bDrawText)
	{
		ostringstream stream;
		stream << fixed << setprecision(2) << percent * 100 << '%';

		float middle = (xPos + (width / 2.0f));
		renderer.setColor(Color(1.0f,1.0f,1.0f,1.0f));
		renderer.drawText(middle,yPos - 0.1f,"Roboto",stream.str(),5.0f*height,IRenderer::Center);
	}
}

Mars::Mars()
{
	m_game = 0;
	m_suicide=false;

	srand((unsigned int)time(0));
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

	int x = input.x - GRID_OFFSET;
	int y = input.y - GRID_OFFSET;
	int width = input.sx - x - GRID_OFFSET;
	int height = input.sy - y - GRID_OFFSET;

	int right = x + width;
	int bottom = y + height;

	out.left = min(x,right);
	out.top = min(y,bottom);
	out.right = max(x,right);
	out.bottom = max(y,bottom);
}

void Mars::ProccessInput()
{
	const Input& input = gui->getInput();
	int turn = timeManager->getTurn();
	int unitsSelectable = gui->getDebugOptionState("Units Selectable");
	int tilesSelectable = gui->getDebugOptionState("Tiles Selectable");

	if( input.leftRelease && turn < m_game->states.size())
	{
		Rect R;
		GetSelectedRect(R);

		m_selectedUnitIDs.clear();

		if(unitsSelectable)
		{
			for(auto& iter : m_game->states[ turn ].units)
			{
				const auto& unit = iter.second;

				// todo: move this logic into another function
				if(R.left <= unit->x && R.right >= unit->x && R.top <= unit->y && R.bottom >= unit->y)
				{
					m_selectedUnitIDs.push_back(unit->id);
				}
			}
		}

		if(tilesSelectable)
		{
			for(auto& iter : m_game->states[ turn].tiles)
			{
				const auto& tile = iter.second;

				if(R.left <= tile->x && R.right >= tile->x && R.top <= tile->y && R.bottom >= tile->y &&
				  (tile->depth >= 1 || tile->owner == 3 || tile->pumpID != -1))
				{
					m_selectedUnitIDs.push_back(tile->id);
				}
			}
		}

		gui->updateDebugWindow();
		gui->updateDebugUnitFocus();
	}
}

glm::vec3 Mars::GetTeamColor(int owner) const
{
	return owner == 1 ? glm::vec3(0.5f,1.0f,0.5f) : glm::vec3(0.5f,0.5f,1.0f);
}

void Mars::drawObjectSelection() const
{
	int turn = timeManager->getTurn();
	if(turn < m_game->states.size())
	{
		for(auto& iter : m_selectedUnitIDs)
		{
			if(m_game->states[turn].units.find(iter) != m_game->states[turn].units.end())
				drawQuadAroundObj(m_game->states[turn].units.at(iter), glm::vec4(1.0, 0.4, 0.4, 0.6 ));
		}

		for(auto& iter : m_selectedUnitIDs)
		{
			if(m_game->states[turn].tiles.find(iter) != m_game->states[turn].tiles.end())
				drawQuadAroundObj(m_game->states[turn].tiles.at(iter), glm::vec4(0.3, 0.0, 1.0, 0.6));
		}

		int focus = gui->getCurrentUnitFocus();

		if(focus >= 0)
		{
			if(m_game->states[turn].units.find(focus) != m_game->states[turn].units.end())
				drawBoxAroundObj(m_game->states[turn].units.at(focus), glm::vec4(1.0f, 1.0f, 0.0f, 1.0f));

			if(m_game->states[turn].tiles.find(focus) != m_game->states[turn].tiles.end())
				drawBoxAroundObj(m_game->states[turn].tiles.at(focus), glm::vec4(1.0f, 1.0f, 0.0f, 1.0f));
		}
	}
}

void Mars::drawBoxAroundObj(const SmartPointer<parser::Mappable> obj, const glm::vec4& color) const
{
	renderer->setColor(Color(color.r, color.g, color.b, color.a));
	renderer->drawLine(obj->x + 0.1f, obj->y + 0.1f, obj->x + 0.9, obj->y + 0.1);
	renderer->drawLine(obj->x + 0.1f, obj->y + 0.1f, obj->x + 0.1, obj->y + 0.9);
	renderer->drawLine(obj->x + 0.9f, obj->y + 0.1f, obj->x + 0.9, obj->y + 0.9);
	renderer->drawLine(obj->x + 0.1f, obj->y + 0.9f, obj->x + 0.9, obj->y + 0.9);
}

void Mars::drawQuadAroundObj(const SmartPointer<parser::Mappable> obj, const glm::vec4& color) const
{
	renderer->setColor( Color( color.r, color.g, color.b, color.a) );
	renderer->drawQuad(obj->x,obj->y,1,1);
}

void Mars::preDraw()
{

	//============== todo: fix this interesting code:
	static float t = 0.0f;
	static float tile = 4.0f;

	if(options->getNumber("Enable Star Animation") > 0)
	{
		t += 0.1f*timeManager->getDt();
		if(t > 15.7f)
		{
			t = 0.0f;
		}

		tile = 2.0f*sin(0.4f*t) + 4.0f;
	}

	//============== todo: fix this interesting code ^

	renderer->push();
	renderer->translate(GRID_OFFSET, GRID_OFFSET);

	ProccessInput();

	renderer->setColor(Color(1.0f, 1.0f, 1.0f, 1.0f));
	renderer->drawTexturedQuad(-1.0f, -1.0f, 77, 37 ,tile, "background");

	renderer->setColor(Color());
	//renderer->drawTexturedQuad(-2.0f,-2.0f,40.0f,40.0f,"stars");
	renderer->drawTexturedQuad(0.0f,0.0f,m_game->mapWidth,m_game->mapHeight,1.7f,"dirt"); // 1.7

	drawGrid();
	RenderHUD();

// Handle player input here
}

void Mars::postDraw()
{
	drawObjectSelection();

	renderer->pop();
}

void Mars::drawGrid()
{
	  bool bEnableGrid = options->getNumber("Enable Grid") > 0;
	  if(bEnableGrid)
	  {
		unsigned int h = m_game->mapHeight;
		unsigned int w = m_game->mapWidth;

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

list<IGUI::DebugOption> Mars::getDebugOptions()
{
	return std::list<IGUI::DebugOption>({{"Units Selectable", true},
										 {"Tiles Selectable", true},
										 {"Render Footprints", true}});
}

std::map<std::string, bool> Mars::getRenderTagState()
{
	return m_renderTagState;
}

void Mars::pruneSelection()
{
	int turn = timeManager->getTurn();
	bool changed = false;
	int focus = gui->getCurrentUnitFocus();


	if(turn < m_game->states.size())
	{
		auto iter = m_selectedUnitIDs.begin();
		while(iter != m_selectedUnitIDs.end())
		{
			// if it doesn't exist anymore, remove it from the selection.
			if(m_game->states[turn].units.find(*iter) == m_game->states[turn].units.end() &&
			  (m_game->states[turn].tiles.find(*iter) == m_game->states[turn].tiles.end() ||
			  (m_game->states[turn].tiles.at(*iter)->depth > 0 &&
			   m_game->states[turn].tiles.at(*iter)->owner != 3 &&
			   m_game->states[turn].tiles.at(*iter)->pumpID == -1)))
			{
				iter = m_selectedUnitIDs.erase(iter);
				changed = true;
			}
			else
				iter++;
		}

		if(changed == true)
		{
			gui->updateDebugWindow();
		}

		// if previous focus is dead/gone then reset it to the top of the table
		if(std::find(m_selectedUnitIDs.begin(), m_selectedUnitIDs.end(), focus) == m_selectedUnitIDs.end())
			gui->updateDebugUnitFocus();
	}
}

void Mars::optionStateChanged()
{
	int footprints = gui->getDebugOptionState("Render Footprints");

	std::cout << "options state changed\n";

	if(footprints > -1)
		m_renderTagState["footprints"] = footprints;
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

	parser::Game * game = new parser::Game;

	if( !parser::parseGameFromString( *game, gamelog.c_str() ) )
	{
		delete game;
		game = 0;
		WARNING("Cannot load gamelog, %s",gamelog.c_str());
	}

	if(m_game != NULL)
		delete m_game;

	m_game = new Game(game);

	delete game;


	renderer->setCamera( 0, 0, m_game->mapWidth + GRID_OFFSET*2, m_game->mapHeight + 4 + GRID_OFFSET*2);
	renderer->setGridDimensions( m_game->mapWidth + GRID_OFFSET*2, m_game->mapHeight + 4 + GRID_OFFSET*2);

	m_selectedUnitIDs.clear();

	m_rand[0] = rand() % 10;
	m_rand[1] = rand() % 10;

	start();
} // Mars::loadGamelog()


void Mars::RenderHUD()
{
	std::ostringstream waterInfo;
	int turn = timeManager->getTurn();
	float tankWidth = 21.0f;

	const float barWidth = 13.0f;  // <--- unlucky as shit

	float totalWater = m_game->states[turn].players[0]->waterStored + m_game->states[turn].players[1]->waterStored;


	float lengthBlue = 0.0f;
	float lengthRed = 0.0f;

	if(totalWater != 0)
	{
		lengthBlue = (m_game->states[turn].players[0]->waterStored / totalWater) * barWidth;
		lengthRed = barWidth - lengthBlue;
	}

	// Render the back of the tank
	renderer->setColor(Color(1.0f, 1.0f, 1.0f, 1.0f));
	renderer->drawTexturedQuad((m_game->mapWidth/2.0f) - (tankWidth/2.0f), m_game->mapHeight, tankWidth, tankWidth/4.0f,1.0f,"water_tank_back");

	// Render player #0 info
	float oxygenLevel = m_game->states[turn].players[0]->oxygen / (float)m_game->states[turn].players[0]->maxOxygen;

	glm::vec3 playerColor = GetTeamColor(0);
	renderer->setColor( Color(playerColor.r,playerColor.g,playerColor.b, 1.0f));
	renderer->drawText(0.0f, m_game->mapHeight + 1.0f, "Roboto", m_game->states[0].players[0]->playerName, 3.0f, IRenderer::Left);

	waterInfo << "Water Amount: " << m_game->states[turn].players[0]->waterStored;
	renderer->drawText(0.0f, m_game->mapHeight + 2.0f, "Roboto", waterInfo.str(), 2.0f, IRenderer::Left);
	waterInfo.str("");

	renderer->drawQuad((m_game->mapWidth/2.0f) - (barWidth/2.0f), m_game->mapHeight + 1.2f, lengthBlue, 2.0f);

	RenderProgressBar(*renderer,0.0f,m_game->mapHeight + 3.2f,4.0f, .5f,oxygenLevel,Color(0,0,1,1),true);

	// Render player #1
	oxygenLevel = m_game->states[turn].players[1]->oxygen / (float)m_game->states[turn].players[1]->maxOxygen;

	playerColor = GetTeamColor(1);
	renderer->setColor( Color(playerColor.r,playerColor.g,playerColor.b, 1.0f));
	renderer->drawText(40.0f, m_game->mapHeight + 1.0f, "Roboto", m_game->states[0].players[1]->playerName, 3.0f, IRenderer::Right);

	waterInfo << "Water Amount: " << m_game->states[turn].players[1]->waterStored;
	renderer->drawText(40.0f, m_game->mapHeight + 2.0f, "Roboto", waterInfo.str(), 2.0f, IRenderer::Right);

	renderer->drawQuad(((m_game->mapWidth/2.0f) - (barWidth/2.0f)) + lengthBlue, m_game->mapHeight + 1.2f, lengthRed, 2.0f);

	RenderProgressBar(*renderer,36.0f,m_game->mapHeight + 3.2f,4.0f, .5f,oxygenLevel,Color(0,0,1,1),true);

	// Render the divider between the players progress bar
	renderer->setColor(Color(0.2f, 0.2f, 0.2f, 1.0f));
	renderer->drawQuad(((m_game->mapWidth/2.0f) - (barWidth/2.0f)) + lengthBlue - 0.1f, m_game->mapHeight + 1.2f, 0.2f, 2.0f);

	// Render the front of the tank
	renderer->setColor(Color(1.0f, 1.0f, 1.0f, 1.0f));
	renderer->drawTexturedQuad((m_game->mapWidth/2.0f) - (tankWidth/2.0f), m_game->mapHeight, tankWidth, tankWidth/4.0f,1.0f,"water_tank");
}

bool Mars::IsWaterNearTilePos(int state, int xPosIn, int yPosIn) const
{
	const glm::ivec2 coords[] =
	{
		glm::ivec2(-1,0),
		glm::ivec2(1,0),
		glm::ivec2(0,-1),
		glm::ivec2(0,1)
	};

	for(auto& i : coords)
	{
		int xPos = i.x + xPosIn;
		int yPos = i.y + yPosIn;

		if((xPos < (int)m_game->states[state].tileGrid.size() && xPos >= 0) && (yPos < (int)m_game->states[state].tileGrid[xPos].size() && yPos >= 0))
		{
			const SmartPointer<Game::Tile> pTile = m_game->states[state].tileGrid[xPos][yPos];
			if((pTile->owner == 3) || (pTile->waterAmount > 0))
			{
				return true;
			}
		}
	}

	return false;
}

void Mars::RenderWorld(int state, Frame& turn)
{
	// todo: this could be moved elsewhere, it should be
	static std::map<int,int> counter;
	static std::queue<SmartPointer<Animatable>> deathList;
	std::queue<SmartPointer<Animatable>> animList;

	std::set<int> pumpStations;

	for(auto& iter : m_game->states[state].tiles)
	{
		auto& tileIter = iter.second;
		std::string texture;

		// if there is water then render water
		if(tileIter->owner == 3) // if the tile is a glacier
		{
			texture = "glacier";
		}
		else if(tileIter->waterAmount != 0)
		{
			texture = "water";
		}
		else if(tileIter->depth > 0) // if there is no water, but a trench then render a trench
		{
			texture = "trench";
		}
		else if(tileIter->pumpID > -1)
		{
			if(pumpStations.insert(tileIter->pumpID).second)
			{
				auto& pumps = m_game->states[state].pump;
				auto pumpIter = pumps.find(tileIter->pumpID);

				if(pumpIter != pumps.end())
				{
					float percent = (float)pumpIter->second->siegeAmount / (float)m_game->maxSiege;

					if(percent != 0.0f)
					{
						auto eastPumpIter = tileIter->x > 0 ? pumps.find(m_game->states[state].tileGrid[tileIter->x - 1][tileIter->y]->pumpID) : pumps.end();
						if(eastPumpIter == pumps.end() || (eastPumpIter->second->id != pumpIter->second->id))
						{
							SmartPointer<Animatable> pumpBar = new Animatable;
							pumpBar->addKeyFrame(new DrawProgressBar(glm::vec2(tileIter->x,tileIter->y),2.0f,0.3f,percent));

							animList.push(pumpBar);
						}
					}
				}


				int& counterValue = counter[tileIter->id];
				SmartPointer<AnimatedSprite> pPump = new AnimatedSprite(glm::vec2(tileIter->x, tileIter->y), glm::vec2(2.0f), "pump", counterValue);
				pPump->addKeyFrame(new DrawAnimatedSprite(pPump,glm::vec4(GetTeamColor(tileIter->owner),1.0f)));

				turn.addAnimatable(pPump);

				//  11
				// 1x01
				// 1001
				//  11

				if(IsWaterNearTilePos(state,tileIter->x,tileIter->y) ||
				   IsWaterNearTilePos(state,tileIter->x + 1,tileIter->y) ||
				   IsWaterNearTilePos(state,tileIter->x + 1,tileIter->y + 1) ||
				   IsWaterNearTilePos(state,tileIter->x,tileIter->y + 1))
				{
					counterValue = (counterValue + 1) % 10;
				}
			}
		}
		else if(tileIter->owner == 0 || tileIter->owner == 1)
		{
			texture = "tile";
		}


		if(!texture.empty())
		{
			if(texture == "tile")
			{
				SmartPointer<AnimatedSprite> pTile = new AnimatedSprite(glm::vec2(tileIter->x, tileIter->y), glm::vec2(1.0f, 1.0f), texture,m_rand[tileIter->owner]);
				pTile->addKeyFrame(new DrawAnimatedSprite(pTile, glm::vec4(GetTeamColor(tileIter->owner),0.8f)));
				turn.addAnimatable(pTile);
			}
			else
			{
				SmartPointer<BaseSprite> pTile = new BaseSprite(glm::vec2(tileIter->x, tileIter->y), glm::vec2(1.0f, 1.0f), texture);
				pTile->addKeyFrame(new DrawSprite(pTile, glm::vec4(1.0f, 1.0f, 1.0f,0.8f)));
				turn.addAnimatable(pTile);
			}

			// Canal Overlays
			if(tileIter->depth > 0 && tileIter->owner != 3)
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
				if(tileIter->y > 0 &&
				  (m_game->states[state].tileGrid[tileIter->x][tileIter->y - 1]->depth > 0 ||
				   m_game->states[state].tileGrid[tileIter->x][tileIter->y - 1]->owner == 3))
				{
					surroundingTrenches++;
					North = true;
				}

				if(tileIter->y < m_game->mapHeight - 1 &&
				  (m_game->states[state].tileGrid[tileIter->x][tileIter->y + 1]->depth > 0 ||
				   m_game->states[state].tileGrid[tileIter->x][tileIter->y + 1]->owner == 3))
				{
					surroundingTrenches++;
					South = true;
				}

				if(tileIter->x > 0 &&
				  (m_game->states[state].tileGrid[tileIter->x - 1][tileIter->y]->depth > 0 ||
				   m_game->states[state].tileGrid[tileIter->x - 1][tileIter->y]->owner == 3))
				{
					surroundingTrenches++;
					West = true;
				}

				if(tileIter->x < m_game->mapWidth - 1 &&
				  (m_game->states[state].tileGrid[tileIter->x + 1][tileIter->y]->depth > 0 ||
				   m_game->states[state].tileGrid[tileIter->x + 1][tileIter->y]->owner == 3))
				{
					surroundingTrenches++;
					East = true;
				}

				if(tileIter->x > 0 && tileIter->y > 0 &&
				  (m_game->states[state].tileGrid[tileIter->x - 1][tileIter->y - 1]->depth > 0  ||
				   m_game->states[state].tileGrid[tileIter->x - 1][tileIter->y - 1]->owner == 3))
				{
					NorthWest = true;
				}

				if(tileIter->x < m_game->mapWidth - 1 && tileIter->y > 0 &&
				  (m_game->states[state].tileGrid[tileIter->x + 1][tileIter->y - 1]->depth > 0 ||
				   m_game->states[state].tileGrid[tileIter->x + 1][tileIter->y - 1]->owner == 3))
				{
					NorthEast = true;
				}

				if(tileIter->x > 0 && tileIter->y < m_game->mapHeight - 1 &&
				  (m_game->states[state].tileGrid[tileIter->x - 1][tileIter->y + 1]->depth > 0 ||
				   m_game->states[state].tileGrid[tileIter->x - 1][tileIter->y + 1]->owner == 3))
				{
					SouthWest = true;
				}

				if(tileIter->x < m_game->mapWidth - 1 && tileIter->y < m_game->mapHeight - 1 &&
				  (m_game->states[state].tileGrid[tileIter->x + 1][tileIter->y + 1]->depth > 0 ||
				   m_game->states[state].tileGrid[tileIter->x + 1][tileIter->y + 1]->owner == 3))
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
					SmartPointer<BaseSprite> pTile = new BaseSprite(glm::vec2(tileIter->x, tileIter->y), glm::vec2(1.0f, 1.0f), overlayTexture);
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
						SmartPointer<BaseSprite> pTip = new BaseSprite(glm::vec2(tileIter->x, tileIter->y), glm::vec2(1.0f, 1.0f), "trench_tip");
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
						SmartPointer<BaseSprite> pTip = new BaseSprite(glm::vec2(tileIter->x, tileIter->y), glm::vec2(1.0f, 1.0f), "trench_tip");
						pTip->addKeyFrame(new DrawRotatedSprite(pTip, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f), tip1Rotation));
						turn.addAnimatable(pTip);
					}

					if(tip2Rotation >= 0)
					{
						SmartPointer<BaseSprite> pTip = new BaseSprite(glm::vec2(tileIter->x, tileIter->y), glm::vec2(1.0f, 1.0f), "trench_tip");
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
						SmartPointer<BaseSprite> pTip = new BaseSprite(glm::vec2(tileIter->x, tileIter->y), glm::vec2(1.0f, 1.0f), "trench_tip");
						pTip->addKeyFrame(new DrawRotatedSprite(pTip, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f), tip1Rotation));
						turn.addAnimatable(pTip);
					}

					if(tip2Rotation >= 0)
					{
						SmartPointer<BaseSprite> pTip = new BaseSprite(glm::vec2(tileIter->x, tileIter->y), glm::vec2(1.0f, 1.0f), "trench_tip");
						pTip->addKeyFrame(new DrawRotatedSprite(pTip, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f), tip2Rotation));
						turn.addAnimatable(pTip);
					}

					if(tip3Rotation >= 0)
					{
						SmartPointer<BaseSprite> pTip = new BaseSprite(glm::vec2(tileIter->x, tileIter->y), glm::vec2(1.0f, 1.0f), "trench_tip");
						pTip->addKeyFrame(new DrawRotatedSprite(pTip, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f), tip3Rotation));
						turn.addAnimatable(pTip);
					}

					if(tip4Rotation >= 0)
					{
						SmartPointer<BaseSprite> pTip = new BaseSprite(glm::vec2(tileIter->x, tileIter->y), glm::vec2(1.0f, 1.0f), "trench_tip");
						pTip->addKeyFrame(new DrawRotatedSprite(pTip, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f), tip4Rotation));
						turn.addAnimatable(pTip);
					}
				}
			}

			// Water amount display on water filled trenches
			if(tileIter->waterAmount != 0)
			{
				std::ostringstream waterAmountString;
				SmartPointer<Animatable> pText = new Animatable;
				waterAmountString << tileIter->waterAmount;
				DrawTextBox * textBox = new DrawTextBox(waterAmountString.str(),
														glm::vec2(tileIter->x + 0.5, tileIter->y + 0.15),
														glm::vec4(0.3f,0.0f,1.0f,1.0f),
														3.0f);

				pText->addKeyFrame(textBox);
				turn.addAnimatable(pText);
			}
		}

		turn[tileIter->id]["owner"] = tileIter->owner;
		turn[tileIter->id]["pumpID"] = tileIter->pumpID;
		turn[tileIter->id]["waterAmount"] = tileIter->waterAmount;
		turn[tileIter->id]["depth"] = tileIter->depth;
		turn[tileIter->id]["x"] = tileIter->x;
		turn[tileIter->id]["y"] = tileIter->y;
		turn[tileIter->id]["id"] = tileIter->id;

	}


	while(!deathList.empty())
	{
		turn.addAnimatable(deathList.front());
		deathList.pop();
	}

	// For each UNIT in the frame
	for(auto & unit : m_game->states[state].units)
	{
		auto& unitIter = unit.second;
		std::string texture;

		if(unitIter->type == 0)
			texture = "worker";
		else if (unitIter->type == 1)
			texture = "scout";
		else if (unitIter->type == 2)
			texture = "tank";

		SmartPointer<MoveableSprite> pUnit = new MoveableSprite(texture);

		for(auto& animationIter : unitIter->m_Animations)
		{
			if(animationIter->type == parser::MOVE)
			{
				parser::move& move = (parser::move&)*animationIter;
				pUnit->m_Moves.push_back(MoveableSprite::Move(glm::vec2(move.toX, move.toY), glm::vec2(move.fromX, move.fromY)));
			}
			else if(animationIter->type == parser::ATTACK)
			{
				parser::attack& attack = (parser::attack&)*animationIter;

				auto attackerIter = m_game->states[state].units.find(attack.actingID);
				auto targetIter = m_game->states[state].units.find(attack.targetID);

				if(attackerIter != m_game->states[state].units.end() && targetIter != m_game->states[state].units.end())
				{
					glm::vec2 from(attackerIter->second->x,attackerIter->second->y);
					glm::vec2 to(targetIter->second->x,targetIter->second->y);
					glm::vec2 diff = to - from;
					float angle = glm::degrees(std::atan2(diff.y,diff.x));

					SmartPointer<MoveableSprite> pLaser = new MoveableSprite("laser");
					pLaser->m_Moves.push_back(MoveableSprite::Move(to,from));
					pLaser->addKeyFrame(new DrawRotatedSmoothMoveSprite(pLaser, glm::vec4(1.0f,1.0f,1.0f,0.7f),angle));
					//turn.addAnimatable(pLaser);

					animList.push(pLaser);

				}
			}
		}

		if((state + 1) < (int)m_game->states.size())
		{
			if(m_game->states[state + 1].units.find(unitIter->id) == m_game->states[state + 1].units.end())
			{
				SmartPointer<AnimatedSprite> pDeathAnimation = new AnimatedSprite(glm::vec2(unitIter->x, unitIter->y), glm::vec2(1.0f), "death", 7,true);
				pDeathAnimation->addKeyFrame(new DrawAnimatedSprite(pDeathAnimation,glm::vec4(GetTeamColor(unitIter->owner),1.0f)));

				deathList.push(pDeathAnimation);
			}
		}

		if(pUnit->m_Moves.empty())
		{
			pUnit->m_Moves.push_back(MoveableSprite::Move(glm::vec2(unitIter->x, unitIter->y), glm::vec2(unitIter->x, unitIter->y)));

			if(state > 0 &&
			   m_game->states[state - 1].units.find(unitIter->id) != m_game->states[state - 1].units.end() &&
			   m_game->states[state - 1].units.at(unitIter->id)->m_Flipped)
			   unitIter->m_Flipped = true;
		}
		else
		{
			if(pUnit->m_Moves.back().to.x > pUnit->m_Moves.front().from.x)
				unitIter->m_Flipped = true;
			else if(pUnit->m_Moves.back().to.x == pUnit->m_Moves.front().from.x &&
					state > 0 &&
					m_game->states[state - 1].units.find(unitIter->id) != m_game->states[state - 1].units.end())
				unitIter->m_Flipped = m_game->states[state - 1].units.at(unitIter->id)->m_Flipped;

		}

		DrawProgressBar* pBar = new DrawProgressBar(1.0f,0.2f,unitIter->healthLeft / (float)unitIter->maxHealth);

		pUnit->addKeyFrame(new DrawSmoothSpriteProgressBar(pUnit, pBar , glm::vec4(GetTeamColor(unitIter->owner),1.0f), unitIter->m_Flipped));
		turn.addAnimatable(pUnit);

		turn[unitIter->id]["owner"] = unitIter->owner;
		turn[unitIter->id]["hasAttacked"] = unitIter->hasAttacked;
		turn[unitIter->id]["healthLeft"] = unitIter->healthLeft;
		turn[unitIter->id]["maxHealth"] = unitIter->maxHealth;
		turn[unitIter->id]["movementLeft"] = unitIter->movementLeft;
		turn[unitIter->id]["maxMovement"] = unitIter->maxMovement;
		turn[unitIter->id]["X"] = unitIter->x;
		turn[unitIter->id]["Y"] = unitIter->y;
	}

	while(!animList.empty())
	{
		turn.addAnimatable(animList.front());
		animList.pop();
	}

}


// The "main" function
void Mars::run()
{
	gui->setDebugOptions(this);

	timeManager->setNumTurns( 0 );

	animationEngine->registerGame(0, 0);

	const char* playerName = m_game->states[0].players[m_game->winner]->playerName;
	SmartPointer<SplashScreen> splashScreen = new SplashScreen(m_game->winReason,playerName,
															   m_game->mapWidth,
															   m_game->mapHeight
															   );

	splashScreen->addKeyFrame(new DrawSplashScreen(splashScreen));

	// Look through each turn in the gamelog
	for(int state = 0; state < (int)m_game->states.size() && !m_suicide; state++)
	{
		Frame turn;  // The frame that will be drawn

		RenderWorld(state, turn);

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

Mars::Game::Game(parser::Game* game) :
	mapWidth(game->states[0].mapWidth),
	mapHeight(game->states[0].mapHeight),
	trenchDamage(game->states[0].trenchDamage),
	waterDamage(game->states[0].waterDamage),
	turnNumber(game->states[0].turnNumber),
	maxUnits(game->states[0].maxUnits),
	playerID(game->states[0].playerID),
	gameNumber(game->states[0].gameNumber),
	maxSiege(game->states[0].maxSiege),
	winner(game->winner),
	winReason(game->winReason)
{
	states.resize(game->states.size());

	for(auto& player : game->states[0].players)
	{
		states[0].players[player.second.id] = SmartPointer<parser::Player>(new parser::Player(player.second));
	}

	for(auto& unit : game->states[0].units)
	{
		states[0].units[unit.second.id] = SmartPointer<Unit>(new Unit(game->states[0], unit.second));
	}

	for(auto& tile : game->states[0].tiles)
	{
		states[0].tiles[tile.second.id] = SmartPointer<Tile>(new Tile(game->states[0], tile.second));
	}

	for(auto& pumpStation : game->states[0].pumpStations)
	{
		states[0].pump[pumpStation.second.id] = SmartPointer<PumpStation>(new PumpStation(game->states[0], pumpStation.second));
	}

	states[0].tileGrid.resize(mapWidth);
	for(auto& col : states[0].tileGrid)
		col.resize(mapHeight);

	for(auto& tile : states[0].tiles)
		states[0].tileGrid[tile.second->x][tile.second->y] = tile.second;

	for(int i = 1; i < (int) game->states.size(); i++)
	{
		for(auto& player : game->states[i].players)
			states[i].players[player.second.id] = SmartPointer<parser::Player>(new parser::Player(player.second));

		for(auto& unit : game->states[i].units)
			states[i].units[unit.second.id] = SmartPointer<Unit>(new Unit(game->states[i], unit.second));

		// set all pointer this frame to the one before
		for(auto& tileBefore : states[i-1].tiles)
			states[i].tiles[tileBefore.second->id] = tileBefore.second;

		// if there is a new entry, to overwrite that pointer with a new object
		for(auto& tile : game->states[i].tiles)
			states[i].tiles[tile.second.id] = SmartPointer<Tile>(new Tile(game->states[i], tile.second));

		states[i].tileGrid.resize(mapWidth);
		for(auto& col : states[i].tileGrid)
			col.resize(mapHeight);

		for(auto& tile : states[i].tiles)
			states[i].tileGrid[tile.second->x][tile.second->y] = tile.second;

		for(auto& pump : game->states[i].pumpStations)
		{
			states[i].pump[pump.second.id] = SmartPointer<PumpStation>(new PumpStation(game->states[i],pump.second));
		}
	}
}

} // visualizer

Q_EXPORT_PLUGIN2( mars, visualizer::Mars );
