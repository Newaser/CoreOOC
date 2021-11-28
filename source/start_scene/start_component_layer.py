from cocos.layer import Layer
from cocos.sprite import Sprite

from public.image import GUI
from public.actions import *


class ComponentLayer(Layer):
    def __init__(self):
        super().__init__()

        # Logo
        logo = Sprite(GUI.logo)
        logo.position = 980, 600
        logo.do(FadeTo(200, duration=0))
        logo.do(thump())
        self.add(logo)

        self.schedule(self.update)

    def update(self, dt):
        pass
