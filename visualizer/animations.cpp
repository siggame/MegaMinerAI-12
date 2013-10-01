#include "animations.h"
#include "mars.h"

namespace visualizer
{
	void DrawSprite::animate(const float &t, AnimData *d, IGame *game)
	{
		game->renderer->setColor( Color(1.0f,1.0f,1.0f,1.0f) );
		game->renderer->drawTexturedQuad(m_sprite->pos.x, m_sprite->pos.y, m_sprite->scale.x, m_sprite->scale.y,m_sprite->m_sprite);
	}

}
