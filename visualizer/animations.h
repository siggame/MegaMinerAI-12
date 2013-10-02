#ifndef ANIMATIONS_H
#define ANIMATIONS_H

#include "marsAnimatable.h"

namespace visualizer
{

	class DrawSprite : public Anim
	{
	public:
		DrawSprite( BaseSprite* sprite ) : m_sprite(sprite) {}
		void animate( const float& t, AnimData* d, IGame* game );

	private:
		BaseSprite* m_sprite;
	};

}

#endif // ANIMATION_H
