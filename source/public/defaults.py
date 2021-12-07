from pyglet.window import key
from cocos.rect import Rect

from .actions import *
from .image import GUI


class Font:
    FAMILY_NAME = {
        "方正粗黑宋简体": "FZCuHeiSongS-B-GB",
        "楷体": "KaiTi",
        "庞门正道粗书体6.0": "PangMenZhengDao-Cu6.0",
        "站酷高端黑": "huxiaobo-gdh",
        '汉仪南宫体简': 'HYNanGongJ',
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


class Styles:
    slot = {
            "image": GUI.slot,
            "valid_area": Rect(0, 80 - 67, 67, 67),
            "selected_effect": FadeTo(200, 0),
            "unselected_effect": FadeTo(255, 0),
            "activated_effect": FadeTo(150, 0) + highlight(),
            "inactivated_effect": stop_highlight() + FadeTo(255, 0),
        }