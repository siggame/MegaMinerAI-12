#ifndef ANIMATIONS_H
#define ANIMATIONS_H

//TODO : Remove IOSTREAM just for testing
#include <iostream>

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
	
	class DrawSmoothMoveSprite : 
		public Anim
	{
	public:
		DrawSmoothMoveSprite(MoveableSprite * sprite) :
			m_Sprite(sprite)
			{}
		
		void animate( const float& t, AnimData* d, IGame* game );
		
	private:
		MoveableSprite * m_Sprite;
	};

}

#endif // ANIMATION_H
