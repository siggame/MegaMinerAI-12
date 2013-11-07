#ifndef MARS_H
#define MARS_H

#include <QObject>
#include <QThread>
#include "igame.h"
#include "animsequence.h"
#include "animations.h"
#include <map>
#include <string>
#include <list>
#include <deque>
#include <queue>
#include <glm/glm.hpp>

// The Codegen's Parser
#include "parser/parser.h"
#include "parser/structures.h"

using namespace std;

namespace visualizer
{

    class Mars: public QThread, public AnimSequence, public IGame
    {
        struct Rect
        {
            int left;
            int top;
            int right;
            int bottom;
        };

        Q_OBJECT;
        Q_INTERFACES( visualizer::IGame );
        private:
			struct Game
			{
                struct Animatable
                {
                    Animatable(const parser::GameState& state, const int& id)
                    {
                        if(state.animations.find(id) != state.animations.end())
                            m_Animations = state.animations.at(id);
                    }

                    std::vector<SmartPointer<parser::Animation> > m_Animations;
                };

                struct Unit : public parser::Unit, public Animatable
                {
                    Unit(const parser::GameState& state, const parser::Unit& unit) :
                        parser::Unit(unit),
                        Animatable(state, unit.id),
                        m_Flipped(false)
                        {}

                    bool m_Flipped;
                };

				struct Tile : public parser::Tile, public Animatable
				{
					Tile(const parser::GameState& state, const parser::Tile& tile) :
						parser::Tile(tile),
						Animatable(state, tile.id)
						{}
				};

				struct PumpStation : public parser::PumpStation, public Animatable
                {
					PumpStation(const parser::GameState& state, const parser::PumpStation& pump) :
						parser::PumpStation(pump),
						Animatable(state, pump.id)
                        {}
                };

				struct State
				{
                    std::map<int, SmartPointer<parser::Player> > players;
                    std::map<int, SmartPointer<Unit> > units;
                    std::map<int, SmartPointer<Tile> > tiles;
					std::map<int, SmartPointer<PumpStation> > pump;
                    std::vector<std::vector< SmartPointer<Tile> > > tileGrid;
					int playerID;
					int turnNumber;
				};

				Game(parser::Game* game);

				int mapWidth;
				int mapHeight;
				int trenchDamage;
				int waterDamage;
				int turnNumber;
				int maxUnits;
				int playerID;
				int gameNumber;
				int maxSiege;
				float oxygenRate;
				int winner;
			    std::string winReason;

			  	std::vector<State> states;
			};

        public:
            Mars();
            ~Mars();

            PluginInfo getPluginInfo();
            void loadGamelog( std::string gamelog );

            void run();
            void setup();
            void destroy();

            void preDraw();
            void postDraw();

            void addCurrentBoard();

            map<string, int> programs;

            list<int> getSelectedUnits();

            list<IGUI::DebugOption> getDebugOptions();

            std::map<std::string, bool> getRenderTagState();

            void pruneSelection();

            void optionStateChanged();

		private:
			Game *m_game;  // The Game Object from parser/structures.h that is generated by the Codegen
            bool m_suicide;
			list<int> m_selectedUnitIDs;
            std::map<std::string, bool> m_renderTagState;
			int m_rand[2]; // two random numbers

			static const unsigned int GRID_OFFSET = 1;

            glm::vec3 GetTeamColor(int) const;

			bool IsWaterNearTilePos(int state, int xPos, int yPos) const;

            void BuildWorld();
            void UpdateWorld(int state);
            void RenderHUD();

            void RenderWorld(int state, std::map<int,int>& pumpStationCounter, std::map<int,int>& depthCounter, std::queue<SmartPointer<Animatable>>& deathList, Frame& turn);

			void ProccessInput();

			void GetSelectedRect(Rect& out) const;

            void drawGrid();
			void drawObjectSelection() const;
            void drawBoxAroundObj(const SmartPointer<parser::Mappable> obj, const glm::vec4& color) const;
            void drawBoxAroundObj(const glm::vec2 topLeft, const int width, const int height, const glm::vec4 color) const;

            void drawQuadAroundObj(const SmartPointer<parser::Mappable> obj, const glm::vec4& color) const;
            void drawQuadAroundObj(const glm::vec2 topLeft, const int width, const int height, const glm::vec4 color) const;
    };

} // visualizer

#endif // MARS_H
