#include "animations.h"
#include "mars.h"

namespace visualizer
{
	void ColorSprite::animate(const float &t, AnimData*, IGame *game)
    {
		float alpha = m_color.a;
		if(m_fade != None)
		{
			alpha *= t;

			if(m_fade == FadeOut)
			{
				alpha = m_color.a - alpha;
			}
		}

		game->renderer->setColor( Color(m_color.r, m_color.g, m_color.b, alpha) );
    }

	void DrawSprite::animate(const float &t, AnimData *d, IGame *game)
	{
        ColorSprite::animate(t,d,game);
		game->renderer->drawTexturedQuad(m_sprite->pos.x, m_sprite->pos.y, m_sprite->scale.x, m_sprite->scale.y,m_sprite->m_sprite);
	}

	void DrawRotatedSprite::animate(const float &t, AnimData *d, IGame *game)
	{
        ColorSprite::animate(t,d,game);
        game->renderer->drawRotatedTexturedQuad(m_sprite->pos.x, m_sprite->pos.y,
                  m_sprite->scale.x, m_sprite->scale.y, m_rot, m_sprite->m_sprite);
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

	void DrawTextBox::animate(const float &, AnimData*, IGame* game)
	{
        game->renderer->setColor(Color(m_Color.r, m_Color.g, m_Color.b, m_Color.a));

        game->renderer->drawText(m_Pos.x, m_Pos.y, m_Font, m_Text, m_Size, IRenderer::Center);

	};

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
