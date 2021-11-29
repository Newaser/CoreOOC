from copy import deepcopy

from cocos.director import director
from cocos.scene import Scene
from cocos.scenes import *
from cocos.layer import ColorLayer
from cocos.actions import *

from .defaults import Window


def thump(maxsize=1.05, cycle=1):
    scale = ScaleBy(maxsize, duration=cycle / 2)
    return Repeat(scale + Reverse(scale))


def stop_thump(duration=0):
    return ScaleTo(1, duration)


def black_field_transition(new_scene=None, duration=0.5):
    if new_scene is None:
        try:
            director.pop()
        except Exception as e:
            raise e
    else:
        director.push(FadeTransition(new_scene, duration))
