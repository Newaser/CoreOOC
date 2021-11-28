from cocos.layer import Layer
from pyglet.gl import *

from public.actions import black_field_transition
from public.image import GUI
from public.settings import current_settings


key_map = current_settings["key_map"]


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

    def on_key_press(self, symbol, _):
        if symbol in key_map['back']:
            black_field_transition()
