#ifndef ANIMATIONS_H
#define ANIMATIONS_H

#include "marsAnimatable.h"

namespace visualizer
{
    // NOTE: consider combining color sprite and DrawSprite since they are
    //    essentially the same, except that DrawSprite is drawn with white.
    class ColorSprite : public Anim
    {
    public:

		enum Fade
		{
			None,
			FadeIn,
			FadeOut
		};

		ColorSprite(const glm::vec4& c, Fade f = None) : m_color(c), m_fade(f)
        {
        }

       void animate( const float& t, AnimData* d, IGame* game );

    private:
		glm::vec4 m_color;
		Fade m_fade;
    };

    /** @name DrawSprite
      * @inherits Anim
      * @purpose Draws an unmoving sprite at the grid coordinates specified in
      *     m_sprite.
      */
    class DrawSprite : public ColorSprite
	{
	public:
		DrawSprite( BaseSprite* sprite, const glm::vec4& c, Fade f = None) : ColorSprite(c,f), m_sprite(sprite) {}
		void animate( const float& t, AnimData* d, IGame* game );

	private:
		BaseSprite* m_sprite;
	};


	/** @name DrawSprite
      * @inherits Anim
      * @purpose Will draw any MoveableSprite. These sprites contain a list
      *     of moves to adjacent squares in a single turn. The animation engine
      *     will interpolate over all these moves to move the sprite smoothly
      *     in a single turn. These moves must be placed in
      *     MoveableSprite::m_Moves before you try to render the animation.
      *     WARNING - a MoveableSprite requires at least one valid move. This
      *     can be to and from the same position should the object not move at
      *     all that turn.
      */
	class DrawSmoothMoveSprite :
        public ColorSprite
	{
	public:
		DrawSmoothMoveSprite(MoveableSprite * sprite, const glm::vec4& c, Fade f = None) : ColorSprite(c,f),
			m_Sprite(sprite)
			{}

		void animate( const float& t, AnimData* d, IGame* game );

	private:
		MoveableSprite * m_Sprite;
	};

	class DrawSplashScreen : public Anim
	{
	public:

		DrawSplashScreen(SplashScreen* screen) : m_SplashScreen(screen) {}

		void animate(const float &t, AnimData *d, IGame *game);

	private:
		SplashScreen* m_SplashScreen;
	};

}

#endif // ANIMATION_H
