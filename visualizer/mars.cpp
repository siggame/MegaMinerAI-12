#include "mars.h"
#include "marsAnimatable.h"
#include "frame.h"
#include "version.h"
#include "animations.h"
#include <utility>
#include <time.h>
#include <list>
#include <chrono>

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
	if( input.leftRelease )
	{
		int turn = timeManager->getTurn();

		Rect R;
		GetSelectedRect(R);

		m_selectedUnitIDs.clear();

		/*for(auto& iter : m_Trash[turn])
		{
			const auto& trash = iter.second;

			if(trash.amount > 0)
			{
				// todo: move this logic into another function
				if(R.left <= trash.x && R.right >= trash.x && R.top <= trash.y && R.bottom >= trash.y)
				{
					m_selectedUnitIDs.push_back(iter.first);
				}
			}
		}*/

		for(auto& iter : m_game->states[ turn ].units)
		{
			const auto& unit = iter.second;

			// todo: move this logic into another function
			if(R.left <= unit.x && R.right >= unit.x && R.top <= unit.y && R.bottom >= unit.y)
			{
				m_selectedUnitIDs.push_back(unit.id);
			}
		}

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
	/*for(auto iter = m_selectedUnitIDs.begin(); iter != m_selectedUnitIDs.end(); ++iter)
	{
	  if(!DrawQuadAroundObj(m_Trash[turn],*iter))
	  {
		DrawQuadAroundObj(m_game->states[turn].fishes,*iter);
	  }
	}*/
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

// The "main" function
void Mars::run()
{
	QStringList header;
	header<<"owner" << "hasAttacked" << "hasDigged" << "hasBuilt" << "healthLeft" << "maxHealth" << "movementLeft" << "maxMovement" <<"X" << "Y" ;

	gui->setDebugHeader( header );
	timeManager->setNumTurns( 0 );

	animationEngine->registerGame(0, 0);

	const char* playerName = m_game->states[0].players[m_game->winner].playerName;
	SmartPointer<SplashScreen> splashScreen = new SplashScreen(m_game->winReason,playerName,
															   m_game->states[0].mapWidth,
															   m_game->states[0].mapHeight
															   );

	splashScreen->addKeyFrame(new DrawSplashScreen(splashScreen));



	// Look through each turn in the gamelog
	for(int state = 0; state < (int)m_game->states.size() && !m_suicide; state++)
	{
		Frame turn;  // The frame that will be drawn

        // For each TILE in the frame
        for(auto& tileIter : m_game->states[state].tiles)
		{
			std::string texture;

            // if there is water then render water
			if(tileIter.second.owner == 3) // if the tile is a glacier
			{
				texture = "glacier";
			}
			else if(tileIter.second.waterAmount != 0)
            {
				texture = "water";
			}
			else if(tileIter.second.isTrench == true) // if there is no water, but a trench then render a trench
            {
				texture = "trench";
            }

			if(!texture.empty())
			{
				SmartPointer<BaseSprite> pTile = new BaseSprite(glm::vec2(tileIter.second.x, tileIter.second.y), glm::vec2(1.0f, 1.0f), texture);
				pTile->addKeyFrame(new DrawSprite(pTile, glm::vec4(1.0f, 1.0f, 1.0f,0.8f)));
				turn.addAnimatable(pTile);
			}

			if(tileIter.second.isTrench == true && tileIter.second.owner != 3)
			{
                int surroundingTrenches = 0;
                bool North = false, South = false, East = false, West = false;
                std::string overlayTexture;
                float overlayRotation;
                if(tileIter.second.x > 0 &&
                   m_game->states[state].tiles[tileIter.first - 1].isTrench == true &&
                   m_game->states[state].tiles[tileIter.first - 1].owner != 3)
                {
                    surroundingTrenches++;
                    North = true;
                }

                if(tileIter.second.x < m_game->states[state].mapWidth &&
                   m_game->states[state].tiles[tileIter.first + 1].isTrench == true &&
                   m_game->states[state].tiles[tileIter.first + 1].owner != 3)
                {
                    surroundingTrenches++;
                    South = true;
                }

                if(tileIter.second.y > 0 &&
                   m_game->states[state].tiles[tileIter.first - m_game->states[state].mapHeight].isTrench == true &&
                   m_game->states[state].tiles[tileIter.first - m_game->states[state].mapHeight].owner != 3)
                {
                    surroundingTrenches++;
                    West = true;
                }

                if(tileIter.second.y < m_game->states[state].mapWidth &&
                   m_game->states[state].tiles[tileIter.first + m_game->states[state].mapHeight].isTrench == true &&
                   m_game->states[state].tiles[tileIter.first + m_game->states[state].mapHeight].owner != 3)
                {
                    surroundingTrenches++;
                    East = true;
                }

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
                    if(North && South || East && West)
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

                if(overlayTexture != "")
                {
                    SmartPointer<BaseSprite> pTile = new BaseSprite(glm::vec2(tileIter.second.x, tileIter.second.y), glm::vec2(1.0f, 1.0f), overlayTexture);
                    pTile->addKeyFrame(new DrawRotatedSprite(pTile, glm::vec4(1.0f, 1.0f, 1.0f,1.0f), overlayRotation));
                    turn.addAnimatable(pTile);
                }
            }
        }

        // For each UNIT in the frame
		for(auto& unitIter : m_game->states[state].units)
		{

			SmartPointer<MoveableSprite> pUnit = new MoveableSprite("digger");
			pUnit->addKeyFrame(new DrawSmoothMoveSprite(pUnit, unitIter.second.owner == 1? glm::vec4(0.8f,0.2f,0.2f,1.0f) : glm::vec4(0.2f,0.2f,0.8f,1.0f) ));
			turn.addAnimatable(pUnit);

			for(auto& animationIter : m_game->states[state].animations[unitIter.second.id])
			{
				if(animationIter->type == parser::MOVE)
				{
					parser::move& move = (parser::move&)*animationIter;
					pUnit->m_Moves.push_back(MoveableSprite::Move(glm::vec2(move.toX, move.toY), glm::vec2(move.fromX, move.fromY)));
				}
			}

			if(pUnit->m_Moves.empty())
				pUnit->m_Moves.push_back(MoveableSprite::Move(glm::vec2(unitIter.second.x, unitIter.second.y), glm::vec2(unitIter.second.x, unitIter.second.y)));

			 turn[unitIter.second.id]["owner"] = unitIter.second.owner;
			 turn[unitIter.second.id]["hasAttacked"] = unitIter.second.hasAttacked;
			 turn[unitIter.second.id]["hasDigged"] = unitIter.second.hasDigged;
			 turn[unitIter.second.id]["hasBuilt"] = unitIter.second.hasBuilt;
			 turn[unitIter.second.id]["healthLeft"] = unitIter.second.healthLeft;
			 turn[unitIter.second.id]["maxHealth"] = unitIter.second.maxHealth;
			 turn[unitIter.second.id]["movementLeft"] = unitIter.second.movementLeft;
			 turn[unitIter.second.id]["maxMovement"] = unitIter.second.maxMovement;
			 turn[unitIter.second.id]["X"] = unitIter.second.x;
			 turn[unitIter.second.id]["Y"] = unitIter.second.y;
		}

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
