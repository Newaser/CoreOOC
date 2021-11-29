from cocos.scene import Scene

from public.defaults import Layers

# Import bottom layer & top layer
from .options_bg_layer import OptionsBackgroundLayer


# Import other layers
from .options_shape_layer import OptionsShapeLayer
from public.audio import music


class OptionScene(Scene):
    def __init__(self):
        super(OptionScene, self).__init__()

        # Add bottom layer & top layer
        self.add(OptionsBackgroundLayer(), z=Layers.BOTTOM)

        # Add other layers
        self.add(OptionsShapeLayer())

    def on_enter(self):
        super(OptionScene, self).on_enter()
        music.volume_mul(0.5)
