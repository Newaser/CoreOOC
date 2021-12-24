from cocos.layer import Layer
from pyglet.gl import *

from public.transitions import black_field_transition
from public.image import GUI


class OptionsBackgroundLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()

        self.img = GUI.blurred_background_0

    def draw(self):
        glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        glPopMatrix()
