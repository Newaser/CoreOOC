import pyglet.event
from cocos.scene import Scene
from public.defaults import Z
from public.audio import music

# Import _bottom layer & _top layer
from .start_bg_layer import StartBackgroundLayer
from .start_menu import StartMenu

# Import other layers
from .start_component_layer import ComponentLayer


class StartScene(Scene):
    def __init__(self):
        super(StartScene, self).__init__()

        # Add _bottom layer & _top layer
        self.add(StartBackgroundLayer(), z=Z.BOTTOM)
        self.add(StartMenu(), z=Z.TOP)

        # Add other layers
        self.add(ComponentLayer())

    def on_enter(self):
        super(StartScene, self).on_enter()

        music.play('mild', 0.1, True)
