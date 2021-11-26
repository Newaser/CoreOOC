from cocos.scene import Scene

from .start_bg_layer import StartBackgroundLayer
from .start_component_layer import ComponentLayer
from .start_menu import StartMenu


class StartScene(Scene):
    def __init__(self):
        super().__init__()
        self.add(StartBackgroundLayer(), z=0)
        self.add(ComponentLayer(), z=1)
        self.add(StartMenu(), z=2)
