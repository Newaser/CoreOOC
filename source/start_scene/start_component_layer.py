from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.actions import *
from cocos.draw import Line

from public.image import GUI
from public.actions import *
from public import shapes


class ComponentLayer(Layer):
    def __init__(self):
        super().__init__()

        # Logo
        logo = Sprite(GUI.logo)
        logo.position = 980, 600
        logo.do(FadeTo(200, duration=0))
        logo.do(thump())
        self.add(logo)

        # Rectangle Frame
        rect_frame = shapes.Rectangle(400, 380, 1, 1, 350, (100, 200, 100, 200), (0, 100, 200, 200))
        rect_frame.do(thump())
        self.add(rect_frame)

        # A line
        a_line = Line((0, 0), (100, 100), (200, 200, 50, 180), 50)
        a_line.do(thump(2))
        self.add(a_line, z=1)

        self.schedule(self.update)

    def update(self, dt):
        pass
