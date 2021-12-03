from cocos.director import director
from cocos.scenes import *


def black_field_transition(new_scene=None, duration=0.5):
    if new_scene is None:
        try:
            director.pop()
        except Exception as e:
            raise e
    else:
        # director.push(FadeTransition(new_scene, duration))
        director.push(new_scene)
