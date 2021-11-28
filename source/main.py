from pyglet import font
from cocos.director import director

from public.defaults import Window
from start_scene.start_scene import StartScene
from options_scene.options_scene import OptionScene


def run_game():
    # Load fonts
    try:
        # Whether './res/font' or '../res/font':
        #   It is because the inconsistency of a function being called: "os.listdir(path)":
        #   In PyCharm,the argument 'path' considers the project directory as the root directory; whereas, in the system
        # console, the argument 'path' considers the current directory of console as the root directory.
        font.add_directory("./res/font")
        # font.add_directory("../res/font")
    except Exception as e:
        raise SystemExit(e)

    director.init(fullscreen=Window.FULLSCREEN,
                  resizable=Window.RESIZABLE,
                  vsync=Window.VSYNC,
                  width=Window.WIDTH,
                  height=Window.HEIGHT,
                  caption="Core OOC")
    director.run(StartScene())
    # director.run(OptionScene())


if __name__ == '__main__':
    run_game()
