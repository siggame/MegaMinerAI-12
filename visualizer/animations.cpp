#include "animations.h"
#include "mars.h"
#include <iomanip>

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

	DrawProgressBar::DrawProgressBar(const glm::vec2& pos, float width, float height, float percent) :
		m_pos(pos), m_width(width), m_height(height), m_percent(percent)
	{
	}

	void DrawProgressBar::animate(const float &t, AnimData* d, IGame *game)
	{
		IRenderer& renderer = *game->renderer;

		renderer.setColor(Color(0.0f,0.0f,0.0f,0.7f));
		renderer.drawQuad(m_pos.x + m_width,m_pos.y, -(1.0f - m_percent) * m_width, m_height); // height

		renderer.setColor(Color(1.0f,0.0f,0.0f,0.5f));
		renderer.drawQuad(m_pos.x,m_pos.y, m_percent * m_width, m_height);

		// enable this to draw the % in the progress bar
		/*if(bDrawText)
		{
			ostringstream stream;
			stream << fixed << setprecision(2) << m_percent * 100 << '%';

			float middle = (m_pos.x + (m_width / 2.0f));
			renderer.setColor(Color(1.0f,1.0f,1.0f,1.0f));
			renderer.drawText(middle,m_pos.y - 0.1f,"Roboto",stream.str(),5.0f*m_height,IRenderer::Center);
		}*/
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

        ColorSprite::animate(t, d, game);
		game->renderer->drawTexturedQuad(pos.x, pos.y, 1.0f, 1.0f,
										 m_Sprite->m_SpriteName, m_Flipped);

	}

    void DrawAnimatedSprite::animate(const float &t, AnimData*d, IGame* game)
    {
        ColorSprite::animate(t, d, game);

        float animTime = m_Sprite->m_SingleFrame ? t : 1.0f;
        game->renderer->drawAnimQuad( m_Sprite->pos.x, m_Sprite->pos.y, m_Sprite->scale.x, m_Sprite->scale.y, m_Sprite->m_sprite , (int)(m_Sprite->m_Frames * animTime));

		//game->renderer->drawProgressBar()
	}

	void DrawTextBox::animate(const float &, AnimData*, IGame* game)
	{
        game->renderer->setColor(Color(m_Color.r, m_Color.g, m_Color.b, m_Color.a));

        game->renderer->drawText(m_Pos.x, m_Pos.y, "Roboto", m_Text, m_Size, m_Alignment);

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
