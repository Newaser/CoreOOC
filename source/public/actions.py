from copy import deepcopy

from cocos.director import director
from cocos.scenes import FadeTransition
from cocos.actions import *


def thump(maxsize=1.05, cycle=1):
    scale = ScaleBy(maxsize, duration=cycle / 2)
    return Repeat(scale + Reverse(scale))


def stop_thump(duration=0):
    return ScaleTo(1, duration)


def highlight(maxsize=1.05):
    return ScaleBy(maxsize, duration=0)


def stop_highlight():
    return ScaleTo(1, duration=0)


# def text_highlight(text, maxsize=1.05, fade=200)
#     new_text = deepcopy(text)


def black_field_transition(new_scene=None, duration=0.5):
    if new_scene is None:
        try:
            director.pop()
        except Exception as e:
            raise e
    else:
        director.push(FadeTransition(new_scene, duration))
        # director.push(new_scene)
