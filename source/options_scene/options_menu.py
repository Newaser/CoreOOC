from cocos.menu import MenuItem, fixedPositionMenuLayout

from super.menu.text_menus import HorizontalMenu
from manager.z_manager import ZManager
from public.actions import *
from public.transitions import black_field_transition
from public.defaults import Font
from public.audio import sound

from .options_shape_layers import UpBarLayer


class OptionsMenu(HorizontalMenu):
    """
    Options included:
    'Fight' - Link to Fight module
    'Base' - Link to Core Space Military Base, which includes 'Inventory', 'Shop', 'Synthesizing'
    'Options' - Includes 'Settings', 'Tutorial', 'The Developers'
    """
    # Define sounds
    select_by = None
    activate_by = {
        'key': 'page_slide',
        'mouse': 'shrill_page_slide'
    }

    def __init__(self):
        super().__init__()

        # Add a manager of the menu's under layer
        self.zm = ZManager(UpBarLayer())

        # Set font style
        self.item_font_name = Font.FAMILY_NAME["庞门正道粗书体6.0"]
        self.font_item = {
            'font_name': self.item_font_name,
            'font_size': 22,
            'bold': True,
            'italic': False,
            'anchor_y': 'center',
            'anchor_x': 'center',
            'color': (0, 0, 0, 211),
            'dpi': 96,
        }
        self.font_item_selected = {
            'font_name': self.item_font_name,
            'font_size': 23,
            'bold': True,
            'italic': False,
            'anchor_y': 'center',
            'anchor_x': 'center',
            'color': (70, 130, 180, 211),
            'dpi': 96,
        }

        # Button items
        self.items = []
        self.items.append(MenuItem('设置', self.on_settings))
        self.items.append(MenuItem('游戏玩法', self.on_tutorial))
        self.items.append(MenuItem('开发者', self.on_developers))

        # Button Positions
        positions = [bar.anchor for bar in self.zm.get_nodes()]

        # Add the items above to this menu
        self.create_menu(
            items=self.items,
            unselected_effect=stop_highlight(),
            activated_effect=highlight(),
            layout_strategy=fixedPositionMenuLayout(positions),
        )

    def after_activate(self, idx, way=None):
        if way in ('key', 'mouse'):
            sound.play(self.activate_by[way])

        self.zm.stop()
        self.zm.do(stop_highlight())
        self.zm.set_top(idx)
        self.zm.do(highlight(), idx)

    def on_settings(self):
        pass

    def on_tutorial(self):
        pass

    def on_developers(self):
        pass

    def on_quit(self):
        sound.play('button_activate')
        black_field_transition()
