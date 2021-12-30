from pyglet.window import key
from cocos.euclid import Vector2

from public.actions import *


class Color:
    # Gray Tone
    WHITE = 255, 255, 255
    WHITE_SMOKE = 245, 245, 245
    GAINSBORO = 220, 220, 220
    LIGHT_GRAY = 211, 211, 211
    SLIVER = 192, 192, 192
    DARK_GRAY = 169, 169, 169
    GRAY = 128, 128, 128
    DIM_GRAY = 105, 105, 105
    BLACK = 0, 0, 0

    # Yellow Tone
    KHAKI = 240, 230, 140
    GOLD = 255, 215, 0
    DARK_ORANGE = 255, 140, 0


class Font:
    FAMILY_NAME = {
        "黑体": "SimHei",
        "方正粗黑宋简体": "FZCuHeiSongS-B-GB",
        "楷体": "KaiTi",
        "庞门正道粗书体6.0": "PangMenZhengDao-Cu6.0",
        "站酷高端黑": "huxiaobo-gdh",
        '汉仪南宫体简': 'HYNanGongJ',
        "BRITANNIC": "Britannic Bold",
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

    NOTICE = 260
    WARNING = 300


class Player:
    # Forces
    UP_PUSH = Vector2(0, 1000)
    DOWN_PUSH = - UP_PUSH
    RIGHT_PUSH = Vector2(940, 0)
    LEFT_PUSH = - RIGHT_PUSH

    # Multiples
    SPEED_MUL = 3

    # Player
    DEFAULT_HP = 100


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

    VIDEO = {
        "fullscreen": False,
    }

    AUDIO = {
        "music_volume": 100,
        "sound_volume": 100,
    }

    DEFAULT = {
        "key_map": KEY_MAP,
        "video": VIDEO,
        "audio": AUDIO,
    }


class Progress:
    DEFAULT = {
        "high_score": [0] * 15,
        "accessible": [True] + [False] * 14
    }


SAVE_PATH = "./save/01.sav"


class Styles:
    # FONT STYLES
    WARNING_FONT = {
        'font_name': Font.FAMILY_NAME['黑体'],
        'font_size': 19,
        'bold': False,
        'italic': False,
        'anchor_y': 'center',
        'anchor_x': 'center',
        'color': (*Color.WHITE, 255),
        'dpi': 96,
    }
    RECEIPT_FONT = {
        'font_name': Font.FAMILY_NAME['庞门正道粗书体6.0'],
        'font_size': 22,
        'bold': False,
        'italic': True,
        'anchor_y': 'center',
        'anchor_x': 'left',
        'color': (*Color.WHITE_SMOKE, 255),
        'dpi': 96,
    }
    ITEM_COUNTER_FONT = {
        'font_name': Font.FAMILY_NAME['BRITANNIC'],
        'font_size': 25,
        'bold': True,
        'italic': False,
        'anchor_y': 'baseline',
        'anchor_x': 'right',
        'color': (*Color.BLACK, 255),
        'dpi': 96,
    }
    INFO_NAME_FONT = {
        'font_name': Font.FAMILY_NAME['方正粗黑宋简体'],
        'font_size': 14,
        'bold': True,
        'italic': False,
        'anchor_y': 'baseline',
        'anchor_x': 'center',
        'color': (*Color.DARK_ORANGE, 255),
        'dpi': 96,
    }
    INFO_DESCRIPTION_FONT = {
        'font_name': Font.FAMILY_NAME['汉仪南宫体简'],
        'font_size': 14,
        'bold': False,
        'italic': False,
        'color': (*Color.WHITE, 255),
        'x': 0,
        'y': 0,
        'width': 357,
        'height': 87,
        'anchor_y': 'top',
        'anchor_x': 'left',
        'align': 'left',
        'multiline': True,
        'dpi': 96,
    }

    # SHAPE STYLES
    WARNING_PANEL_RECT = {
        'border_thickness': 0,
        'body_rgba': (*Color.BLACK, 178),
        'border_rgba': (*Color.BLACK, 255),
    }
    RECEIPT_BG_RECT = {
        'border_thickness': 5,
        'body_rgba': (*Color.BLACK, 178),
        'border_rgba': (*Color.KHAKI, 255),
    }
    SLOT_SHAPE = {
        'shape_name': 'Rect',
        'position': (0, 0),
        'size': (67, 67),
        'border_thickness': 2,
        'body_rgba': (*Color.LIGHT_GRAY, 215),
        'border_rgba': (*Color.DARK_GRAY, 255),
    }
    INFO_FRAME_RECT = {
        'border_thickness': 2,
        'body_rgba': (*Color.BLACK, 178),
        'border_rgba': (*Color.BLACK, 255)
    }

    # EFFECTS
    INVENTORY_EFFECTS = {
        "selected":
            ShapeGraduateTo(Color.GAINSBORO, 0, 'body'),

        "unselected":
            ShapeGraduateTo(Color.LIGHT_GRAY, 0, 'body'),

        "activated":
            highlight() +
            ShapeGraduateTo(Color.WHITE_SMOKE, 0, 'body') +
            ShapeGraduateTo(Color.DARK_ORANGE, 0, 'border'),

        "inactivated":
            stop_highlight() +
            ShapeGraduateTo(Color.LIGHT_GRAY, 0, 'body') +
            ShapeGraduateTo(Color.DARK_GRAY, 0, 'border'),
    }
    CATEGORY_MENU_EFFECTS = {
        "selected": FadeTo(230, 0),
        "unselected": FadeTo(255, 0),
        "activated": FadeTo(211, 0) + highlight(),
        "inactivated": stop_highlight() + FadeTo(255, 0),
    }
