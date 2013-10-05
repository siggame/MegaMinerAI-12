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

void Mars::preDraw()
{
	const Input& input = gui->getInput();

	renderer->setColor(Color());
	renderer->drawTexturedQuad(0.0f,0.0f,m_game->states[0].mapWidth,m_game->states[0].mapHeight,"mars");

	drawGrid();

// Handle player input here
}

void Mars::postDraw()
{

}

void Mars::drawGrid()
{
      bool bEnableGrid = options->getNumber("Enable Grid") > 0;
      if(bEnableGrid)
      {
        int h = m_game->states[0].mapHeight;
        int w = m_game->states[0].mapWidth;

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
	// TODO Selection logic
	return list<int>();  // return the empty list
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

	start();
} // Mars::loadGamelog()

// The "main" function
void Mars::run()
{
	// Build the Debug Table's Headers
	QStringList header;
	header << "one" << "two" << "three";
	gui->setDebugHeader( header );
	timeManager->setNumTurns( 0 );

	animationEngine->registerGame(0, 0);

	// Look through each turn in the gamelog
	for(int state = 0; state < (int)m_game->states.size() && !m_suicide; state++)
	{
		Frame turn;  // The frame that will be drawn

		for(auto& unitIter : m_game->states[state].units)
		{
			SmartPointer<MoveableSprite> pUnit = new MoveableSprite("digger");
			pUnit->addKeyFrame(new DrawSmoothMoveSprite(pUnit));
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
