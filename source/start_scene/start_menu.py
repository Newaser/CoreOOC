from cocos.menu import *

from super.menu.text_menus import VerticalMenu
from public.actions import *
from public.transitions import black_field_transition
from public.defaults import Font

from inventory_scene.inventory_scene import InventoryScene
from options_scene.options_scene import OptionScene


class StartMenu(VerticalMenu):
    """
    Options included:
    'Fight' - Link to Fight module
    'Base' - Link to Core Space Military Base, which includes 'Inventory', 'Shop', 'Synthesizing'
    'Options' - Includes 'Settings', 'Tutorial', 'The Developers'
    """
    select_sound = 'button_selected'
    activate_sound = 'button_activate'

    def __init__(self):
        super().__init__()
        # Can switch menu items circularly
        self.circular_switch = True

        # Set font style
        self.item_font_name = Font.FAMILY_NAME["站酷高端黑"]
        self.font_item = {
            'font_name': self.item_font_name,
            'font_size': 48,
            'bold': True,
            'italic': False,
            'anchor_y': 'center',
            'anchor_x': 'center',
            'color': (0, 100, 180, 255),
            'dpi': 96,
        }
        self.font_item_selected = {
            'font_name': self.item_font_name,
            'font_size': 48,
            'bold': True,
            'italic': False,
            'anchor_y': 'center',
            'anchor_x': 'center',
            'color': (0, 180, 240, 200),
            'dpi': 96,
        }

        # Button items
        items = []
        items.append(MenuItem('·战斗·', on_fight))
        items.append(MenuItem('·基地·', on_base))
        items.append(MenuItem('·选项·', on_options))

        # Button Positions
        positions = [(160, 480), (160, 400), (160, 320)]

        # Add the items above to this menu
        self.create_menu(items, thump(), stop_thump(), layout_strategy=fixedPositionMenuLayout(positions))


def on_fight():
    pass


def on_base():
    black_field_transition(InventoryScene())


def on_options():
    black_field_transition(OptionScene())
