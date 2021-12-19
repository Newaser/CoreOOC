from cocos.cocosnode import CocosNode
from cocos.menu import MenuItem, fixedPositionMenuLayout

from super.menu.text_menus import VerticalMenu
from public.actions import *
from public.defaults import Font, Z
from public.shapes import BorderedShape


class Card(CocosNode):
    def __init__(self, *options):
        super(Card, self).__init__()

        # Number of items
        self.number = len(options)

        # The spacings between frame and frame or between frame and body
        self.spacing = 13

        self.size = 160, 40 * self.number + self.spacing * (self.number + 1)
        self.body = BorderedShape(
            shape_name='Rect',
            position=(0, 0),
            size=self.size,
            border_thickness=2,
            body_rgba=(0, 0, 0, 178),
            border_rgba=(0, 0, 0, 255)
        )

        self.frames = []
        for i in range(self.number):
            frame = BorderedShape(
                shape_name='Rect',
                position=(self.spacing, self.body.shape.height - (self.spacing + 40) * (i + 1)),
                size=(160 - self.spacing * 2, 40),
                border_thickness=3,
                body_rgba=(0, 0, 0, 0),
                border_rgba=(255, 255, 255, 255)
            )

            self.frames.append(frame)
            self.body.add(frame)

        self.menu = CardMenu(options, self.frames)
        self.body.add(self.menu)

    def open(self):
        if self.body not in self.get_children():
            self.add(self.body, z=Z.TOP)

    def close(self):
        if self.body in self.get_children():
            self.remove(self.body)

    def _set_open(self, set_open):
        if set_open:
            self.open()
        else:
            self.close()

    is_open = property(lambda self: self.body in self.get_children(), _set_open)


class CardMenu(VerticalMenu):
    activate_sound = 'button_activate'

    def __init__(self, options, frames):
        super(CardMenu, self).__init__()

        # Option name -> Menu Item
        self._option_dict = {
            '': MenuItem('', None),
            '查看': MenuItem('查看', self.on_check),
            '出售': MenuItem('出售', self.on_sell),
            '装上': MenuItem('装上', self.on_install),
            '卸下': MenuItem('卸下', self.on_uninstall),
            '合成': MenuItem('合成', self.on_forge),
            '拆开': MenuItem('拆开', self.on_unpack),
        }

        # The frames from the parent
        self.parent_frames = frames

        # Can switch menu items circularly
        self.circular_switch = True

        # Set font style
        self.item_font_name = Font.FAMILY_NAME["汉仪南宫体简"]
        self.font_item = {
            'font_name': self.item_font_name,
            'font_size': 26,
            'bold': False,
            'italic': False,
            'anchor_y': 'center',
            'anchor_x': 'center',
            'color': (255, 255, 255, 255),
            'dpi': 96,
        }
        self.font_item_selected = {
            'font_name': self.item_font_name,
            'font_size': 26,
            'bold': False,
            'italic': False,
            'anchor_y': 'center',
            'anchor_x': 'center',
            'color': (255, 255, 255, 128),
            'dpi': 96,
        }

        # Button items & positions
        items = [self._option_dict[option] for option in options]
        positions = [frame.anchor for frame in self.parent_frames]

        # Add the items above to this menu
        self.create_menu(items, layout_strategy=fixedPositionMenuLayout(positions))

    def _reset_frames(self):
        for frame in self.parent_frames:
            frame.stop()
            frame.do(ShapeFadeTo(255, 0, 'border'))
            frame.do(ShapeGraduateTo((255, 255, 255), 0, 'border'))

    def on_enter(self):
        super(CardMenu, self).on_enter()

        # Unselect the previous menu item
        if self.selected_index is not None:
            self.children[self.selected_index][1].is_selected = False
            self.children[self.selected_index][1].on_unselected()
            self.selected_index = None

        # Reset all frames
        self._reset_frames()

    def after_switch(self, old_idx, new_idx, way=None):
        # Reset all frames
        self._reset_frames()

        # Set the selected frame translucent
        self.parent_frames[new_idx].do(ShapeFadeTo(128, 0, 'border'))

    def on_check(self):
        pass

    def on_sell(self):
        pass

    def on_install(self):
        pass

    def on_uninstall(self):
        pass

    def on_forge(self):
        pass

    def on_unpack(self):
        pass

    def on_quit(self):
        del self.parent.parent.parent.activated_slot
