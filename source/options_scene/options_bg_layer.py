from cocos.layer import Layer
from pyglet.gl import *

from public.image import GUI


class OptionsBackgroundLayer(Layer):
    def __init__(self):
        super().__init__()

        self.img = GUI.background_0

    def draw(self):
        glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        glPopMatrix()
