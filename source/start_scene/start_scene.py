from cocos.scene import Scene
from public.defaults import Layers
from public.audio import music

# Import bottom layer & top layer
from .start_bg_layer import StartBackgroundLayer
from .start_menu import StartMenu

# Import other layers
from .start_component_layer import ComponentLayer


class StartScene(Scene):
    def __init__(self):
        super(StartScene, self).__init__()

        # Add bottom layer & top layer
        self.add(StartBackgroundLayer(), z=Layers.BOTTOM)
        self.add(StartMenu(), z=Layers.TOP)

        # Add other layers
        self.add(ComponentLayer())

    def on_enter(self):
        super(StartScene, self).on_enter()
        music.play('mild', 0.1, True)
