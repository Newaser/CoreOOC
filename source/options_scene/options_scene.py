from cocos.scene import Scene

from public.defaults import Z
from public.audio import music

# Import _bottom layer & _top layer
from .options_bg_layer import OptionsBackgroundLayer
from .options_menu import OptionsMenu


# Import other layers
from .options_shape_layers import MainPanelLayer


class OptionScene(Scene):
    def __init__(self):
        super(OptionScene, self).__init__()

        # Add _bottom layer & _top layer
        self.add(OptionsBackgroundLayer(), z=Z.BOTTOM)
        menu = OptionsMenu()
        self.add(menu, z=Z.TOP)

        # Add other layers
        self.add(menu.zm.get_parent(), z=Z.TOP-1)
        self.add(MainPanelLayer(), z=Z.TOP-2)

    def on_enter(self):
        super(OptionScene, self).on_enter()
        music.volume_mul(0.5)
