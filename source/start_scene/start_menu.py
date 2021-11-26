from cocos.menu import *

from super.my_menu import MyMenu

from public.actions import *
from public.defaults import Font


class StartMenu(MyMenu):
    """
    Options included:
    'Fight' - Link to Fight module
    'Base' - Link to Core Space Military Base, which includes 'Inventory', 'Shop', 'Synthesizing'
    'Options' - Includes 'Settings', 'Tutorial', 'The Developers'
    """
    def __init__(self):
        super().__init__()

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
        items.append(MenuItem('·战斗·', self.on_fight))
        items.append(MenuItem('·基地·', self.on_base))
        items.append(MenuItem('·选项·', self.on_options))

        # Button Positions
        positions = [(160, 480), (160, 400), (160, 320)]

        # Add the items above to this menu
        # :Known bug:
        #   When an item's 'activated_effect' is set to 'shake()', it can rotate by a large angle with multiple clicks
        # in a short time.
        # :Solution:
        #   Create a class named MutexAction inherited from Action
        self.create_menu(items, thump(), stop_thump(), shake()+shake_back(),
                         fixedPositionMenuLayout(positions))

    def on_fight(self):
        pass

    def on_base(self):
        pass

    def on_options(self):
        pass
