from pyglet import font
from cocos.director import director

from start_scene.start_scene import StartScene
from test_scene.test_scene import TestScene
from public.defaults import Window


def run_game():
    # Load fonts
    try:
        # Warning:
        #   You should run this file at main directory('/CoreOOC/'), otherwise the font's dir cannot work
        font.add_directory("./res/font")
    except Exception as e:
        raise SystemExit(e)

    director.init(fullscreen=Window.FULLSCREEN,
                  resizable=Window.RESIZABLE,
                  vsync=Window.VSYNC,
                  width=Window.WIDTH,
                  height=Window.HEIGHT,
                  caption="Core OOC"
                  )
    # director.run(StartScene())
    director.run(TestScene())


if __name__ == '__main__':
    run_game()
