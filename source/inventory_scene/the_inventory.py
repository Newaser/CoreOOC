from cocos.rect import Rect
from cocos.text import Label

from super.inventory import CardInventory
from public.defaults import Window
from public.image import GUI
from public.actions import *
from public.transitions import black_field_transition


class TheInventory(CardInventory):
    def __init__(self):
        super(TheInventory, self).__init__()

        # Init layout
        self.number = 15
        self.rows = 3
        self.max_column = 6
        self.margin = (0, 0)
        self.start_position = (666, Window.HEIGHT - 233)

        # Set slot sample
        slot_style = {
            "image": GUI.slot,
            "valid_area": Rect(0, 80 - 67, 67, 67),
            "selected_effect": FadeTo(200, 0),
            "unselected_effect": FadeTo(255, 0),
            "activated_effect": FadeTo(150, 0) + highlight(),
            "inactivated_effect": stop_highlight() + FadeTo(255, 0),
        }

        self.create_inventory(slot_style)

        self.text = Label(
            font_size=22,
        )
        self.text.position = 0, 10
        self.add(self.text)

    def on_mouse_motion(self, x, y, dx, dy):
        super(TheInventory, self).on_mouse_motion(x, y, dx, dy)
        self.text.element.text = str(x) + ', ' + str(y)
        if self.selected_idx is not None:
            self.text.element.text += ', ' + str(self.slots[self.selected_idx].opacity)

    def on_quit(self):
        black_field_transition()
