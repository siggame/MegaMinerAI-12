#ifndef MARS_ANIMATABLE_H
#define MARS_ANIMATABLE_H

//#include "marsAnimatable.h"
#include "irenderer.h"
#include "parser/structures.h"

#include "math.h"
#include <glm/glm.hpp>

namespace visualizer
{
	struct BaseSprite : public Animatable
	{
		BaseSprite(const glm::vec2& pos, const glm::vec2& scale, const string& sprite) :
			pos(pos), scale(scale), m_sprite(sprite)  {}

		glm::vec2 pos;
		glm::vec2 scale;
		string m_sprite;
	};
	
	struct MoveableSprite :
		public Animatable
	{
	public:
		MoveableSprite() {}
	
		struct Move
		{
			Move() {}
			Move(const glm::vec2& t, const glm::vec2&f) :
				to(t),
				from(f)
				{}
				
			glm::vec2 to;
			glm::vec2 from;
		};
		
		std::vector<Move> m_Moves;
	};

} // visualizer

#endif // MARS_ANIMATABLE_H
