#ifndef MARS_H
#define MARS_H

#include <QObject>
#include <QThread>
#include "igame.h"
#include "animsequence.h"
#include <map>
#include <string>
#include <list>
#include <deque>
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
        private:
            parser::Game *m_game;  // The Game Object from parser/structures.h that is generated by the Codegen
            bool m_suicide;

			list<int> m_selectedUnitIDs;
			std::vector< std::vector<parser::Tile> > m_Tiles;
			std::map<int, parser::Unit> m_Units;

            void BuildWorld();
            void UpdateWorld(int state);
			void RenderWorld(int state, std::deque<glm::ivec2>& trail, vector<vector<int>>& turnMap, Frame& turn);
            parser::Tile& GetTileAt(int x, int y);

			void ProccessInput();

			void GetSelectedRect(Rect& out) const;

            void drawGrid();
			void drawObjectSelection() const;

			template< class T >
			bool drawQuadAroundObj(const T& datastruct, const typename T::key_type& key) const
			{
			  auto iter = datastruct.find(key);

			  if(iter != datastruct.end())
			  {
				const auto& obj = iter->second;

				renderer->setColor( Color( 1.0, 0.4, 0.4, 0.6 ) );
				renderer->drawQuad(obj.x,obj.y,1,1);
				return true;
			  }

			  return false;
			}
    };

} // visualizer

#endif // MARS_H
