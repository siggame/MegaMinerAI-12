#ifndef MARS_ANIMATABLE_H
#define MARS_ANIMATABLE_H

//#include "marsAnimatable.h"
#include "irenderer.h"
#include "parser/structures.h"

#include "math.h"
#include <glm/glm.hpp>

namespace visualizer
{
    /** @name BaseSprite
      * @inherits Animatable
      * @purpose this object is a container for the sprite data of an immobile sprite.
      *      The position and scale vectors must be set for Anim interfaces to render
      *      correctly.
      */
	struct BaseSprite : public Animatable
	{
		BaseSprite(const glm::vec2& pos, const glm::vec2& scale, const string& sprite) :
			pos(pos), scale(scale), m_sprite(sprite)  {}

		glm::vec2 pos;
		glm::vec2 scale;
		string m_sprite;
	};


	/** @name BaseSprite
      * @inherits Animatable
      * @purpose this object is a container for the sprite data of a moving object.
      *      Each move between adjacent squares must be placed into the m_Moves
      *      vector.
      *      WARNING - at least 1 Move must be in the m_Moves vector for the Anim
      *      structures to render it correctly.
      */
	struct MoveableSprite :
		public Animatable
	{
		MoveableSprite(const string& sprite) :
			m_SpriteName(sprite)
			{}

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

		std::string m_SpriteName;
		std::vector<Move> m_Moves;
	};

	struct SplashScreen : public Animatable
	{
		SplashScreen(const string& reason, const string& nam, int w, int h) :
			winReason(reason), name(nam), width(w), height(h) {}

		string winReason;
		string name;
		int width;
		int height;
	};

} // visualizer

#endif // MARS_ANIMATABLE_H
