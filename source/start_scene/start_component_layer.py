from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.actions import *

from public.image import StartImage


class ComponentLayer(Layer):
    def __init__(self):
        super().__init__()

        # Logo
        logo = Sprite(StartImage.logo)
        logo.position = 980, 600
        scale = ScaleBy(1.05, duration=0.5)
        thump = Repeat(scale + Reverse(scale))
        logo.do(FadeTo(200, duration=0))
        logo.do(thump)
        self.add(logo)

        self.schedule(self.update)

    def update(self, dt):
        pass
