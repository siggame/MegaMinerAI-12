#include "animations.h"
#include "mars.h"

namespace visualizer
{
	void ColorSprite::animate(const float &, AnimData*, IGame *game)
    {
         game->renderer->setColor( Color(m_color.r, m_color.g, m_color.b, 1) );
    }

	void DrawSprite::animate(const float &t, AnimData *d, IGame *game)
	{
        ColorSprite::animate(t,d,game);
		game->renderer->drawTexturedQuad(m_sprite->pos.x, m_sprite->pos.y, m_sprite->scale.x, m_sprite->scale.y,m_sprite->m_sprite);
	}

	void DrawSmoothMoveSprite::animate(const float &t, AnimData *d, IGame *game)
	{
		unsigned int index = (unsigned int)(m_Sprite->m_Moves.size() * t);
		float subT = m_Sprite->m_Moves.size() * t - index;
		MoveableSprite::Move& thisMove = m_Sprite->m_Moves[index];


		glm::vec2 diff = thisMove.to - thisMove.from;
		glm::vec2 pos = thisMove.from + diff * subT;

		// TODO: give it the option of being flipped
        ColorSprite::animate(t, d, game);
		game->renderer->drawTexturedQuad(pos.x, pos.y, 1.0f, 1.0f,
										 m_Sprite->m_SpriteName, true);

	}

	void DrawSplashScreen::animate(const float &, AnimData*, IGame *game)
	{
		game->renderer->setColor(Color(1.0f,1.0f,1.0f,0.5f));

		game->renderer->drawQuad(0.0f,0.0f,m_SplashScreen->width,m_SplashScreen->height);

		game->renderer->setColor(Color(0.2f,1.0f,1.0f,1.0f));
		game->renderer->drawText(m_SplashScreen->width / 2.0f,
								 m_SplashScreen->height / 2.0f,
								 "Roboto",
								 m_SplashScreen->winReason,8.0f,
								 IRenderer::Center);
	}

}
