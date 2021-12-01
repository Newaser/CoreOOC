from cocos.scene import Scene

from public.defaults import Z
from public.audio import music

# Import _bottom layer & _top layer
from .inventory_bg_layer import InventoryBackgroundLayer

# Import other layers
from .the_inventory import TheInventory


class InventoryScene(Scene):
    def __init__(self):
        super(InventoryScene, self).__init__()

        # Add _bottom layer & _top layer
        self.add(InventoryBackgroundLayer(), z=Z.BOTTOM)

        # Add other layers
        self.add(TheInventory(), z=Z.TOP-1)

    def on_enter(self):
        super(InventoryScene, self).on_enter()
        music.play('going_deep', 0.1, True)
