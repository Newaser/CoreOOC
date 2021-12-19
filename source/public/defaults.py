from pyglet.window import key
from cocos.rect import Rect
from cocos.euclid import Vector2

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


class Vectors:
    # Forces
    UP_PUSH = Vector2(0, 1000)
    DOWN_PUSH = - UP_PUSH
    RIGHT_PUSH = Vector2(940, 0)
    LEFT_PUSH = - RIGHT_PUSH

    # Multiple
    SPEED_MUL = 3


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
        "pause": [key.ESCAPE, key.P],

        "battle_up_p1": [key.W],
        "battle_down_p1": [key.S],
        "battle_left_p1": [key.A],
        "battle_right_p1": [key.D],
        "attack_p1": [key.J, key.SPACE],
        "speed_p1": [key.K],
        "rescue_p1": [key.L],
        "skill_1_p1": [key.U],
        "skill_2_p1": [key.I],
        "skill_3_p1": [key.O],

        "battle_up_p2": [key.UP],
        "battle_down_p2": [key.DOWN],
        "battle_left_p2": [key.LEFT],
        "battle_right_p2": [key.RIGHT],
        "attack_p2": [key.NUM_1, key.NUM_ENTER],
        "speed_p2": [key.NUM_2],
        "rescue_p2": [key.NUM_3],
        "skill_1_p2": [key.NUM_4],
        "skill_2_p2": [key.NUM_5],
        "skill_3_p2": [key.NUM_6],
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
