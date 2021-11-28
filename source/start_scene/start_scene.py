from cocos.scene import Scene


from .start_bg_layer import StartBackgroundLayer
from .start_component_layer import ComponentLayer
from .start_menu import StartMenu
from .shape_layer import ShapeLayer
from public.defaults import Layers


class StartScene(Scene):
    def __init__(self):
        super(StartScene, self).__init__()

        # Add bottom layer & top layer
        self.add(StartBackgroundLayer(), z=Layers.BOTTOM)
        self.add(StartMenu(), z=Layers.TOP)

        # Add other layers
        self.add(ComponentLayer())
        self.add(ShapeLayer())
