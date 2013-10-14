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
      * @inherits ColorSprite
      * @purpose Draws an unmoving sprite at the grid coordinates specified with
      *     the color added to the textures color.
      */
    class DrawSprite : public ColorSprite
	{
	public:
		DrawSprite( BaseSprite* sprite, const glm::vec4& c, Fade f = None) : ColorSprite(c,f), m_sprite(sprite) {}
		void animate( const float& t, AnimData* d, IGame* game );

	private:
		BaseSprite* m_sprite;
	};

    /** @name DrawRotatedSprite
      * @inherits ColorSprite
      * @purpose Draws an unmoving sprite at the grid coordinate with the color
      *     added to the textures color. The texture will also be rotated by
      *     the amount specified (in degrees).
      */
    class DrawRotatedSprite :
        public ColorSprite
    {
    public:
        DrawRotatedSprite( BaseSprite* sprite, const glm::vec4& c, const float& rot ) :
            m_sprite(sprite),
            ColorSprite(c),
            m_rot(rot)
            {}

		void animate( const float& t, AnimData* d, IGame* game);

    private:
        const float m_rot;
        BaseSprite* m_sprite;
    };

	/** @name DrawSmoothMoveSprite
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

	/** @name DrawTextBox
      * @inherits Anim
      * @purpose Draws the TextBox to the screen.
      */
    class DrawTextBox :
        public Anim
    {
    public:
        DrawTextBox(const std::string& text, const glm::vec2& pos, const glm::vec4& color,
                const float& size, const std::string& font) :
            m_Text(text),
            m_Pos(pos),
            m_Color(color),
            m_Size(size),
            m_Font(font)
            {}

        void animate(const float &t, AnimData *d, IGame *game);

    private:
        std::string m_Text;
        glm::vec2 m_Pos;
        glm::vec4 m_Color;
        float m_Size;
        std::string m_Font;
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
