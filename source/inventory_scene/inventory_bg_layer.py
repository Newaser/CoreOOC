from cocos.layer import Layer
from pyglet import gl

from public.image import GUI


class InventoryBackgroundLayer(Layer):
    def __init__(self):
        super().__init__()

        self.img = GUI.background_1

    def draw(self):
        gl.glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        gl.glPopMatrix()
