from pyglet.window import key


class Font:
    FAMILY_NAME = {
        "方正粗黑宋简体": "FZCuHeiSongS-B-GB",
        "楷体": "KaiTi",
        "庞门正道粗书体6.0": "PangMenZhengDao-Cu6.0",
        "站酷高端黑": "huxiaobo-gdh",
    }


class Window:
    """
    Concerning: Window
    """
    FULLSCREEN = False
    RESIZABLE = False
    VSYNC = False
    WIDTH = 1280
    HEIGHT = 720
    SIZE = WIDTH, HEIGHT


class Z:
    BOTTOM = -255
    TOP = 255


class Settings:
    """
    Concerning: Settings
    """
    KEY_MAP = {
        # On menu
        "up": [key.UP],
        "down": [key.DOWN],
        "left": [key.LEFT],
        "right": [key.RIGHT],
        "OK": [key.ENTER, key.SPACE],
        "back": [key.Q],

        # In battle
        "battle_up": [key.W],
        "battle_down": [key.S],
        "battle_left": [key.A],
        "battle_right": [key.D],
        "pause": [key.ESCAPE, key.SPACE],
        "attack": [key.J, key.SPACE],
        "speed": [key.K],
        "rescue": [key.L],
        "skill_1": [key.U],
        "skill_2": [key.I],
        "skill_3": [key.O],
    }

    DEFAULT_SETTINGS = {
        "key_map": KEY_MAP
    }
