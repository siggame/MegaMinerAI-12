#include "animations.h"
#include "mars.h"


namespace visualizer
{
	void DrawSprite::animate(const float &t, AnimData *d, IGame *game)
	{
		game->renderer->setColor( Color() );
		game->renderer->drawTexturedQuad(m_sprite->pos.x, m_sprite->pos.y, m_sprite->scale.x, m_sprite->scale.y,m_sprite->m_sprite);
	
	
	
	}
	
	void DrawSmoothMoveSprite::animate(const float &t, AnimData *d, IGame *game)
	{
		unsigned int index = (unsigned int)(m_Sprite->m_Moves.size() * t);
		float subT = m_Sprite->m_Moves.size() * t - index;
		MoveableSprite::Move& thisMove = m_Sprite->m_Moves[index];
		
		
		glm::vec2 diff = m_Sprite->m_Moves[index].to - m_Sprite->m_Moves[index].from;
		glm::vec2 pos = m_Sprite->m_Moves[index].from + diff * subT; 
		
		// TODO: give it the option of being flipped
		game->renderer->drawTexturedQuad(pos.x, pos.y, 1.0f, 1.0f,
										 m_Sprite->m_SpriteName, true);
		
	}

}
