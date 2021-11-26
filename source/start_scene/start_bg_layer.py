from cocos.layer import Layer
from pyglet.gl import *

from public.image import StartImage


class StartBackgroundLayer(Layer):
    def __init__(self):
        super().__init__()

        self.img = StartImage.background

    def draw(self):
        glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        glPopMatrix()
