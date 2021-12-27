from copy import copy

from cocos.cocosnode import CocosNode
from cocos.menu import MenuItem, fixedPositionMenuLayout
from cocos.rect import Rect
from cocos.text import Label, RichLabel

from db.item import ItemQuery
from public.actions import *
from public.audio import sound
from public.defaults import Font, Z, Styles
from public.events import emitter
from public.shapes import BorderedShape
from super.menu.text_menus import VerticalMenu


class Slot(BorderedShape):
    """A slot of Inventory
    """

    @property
    def inventory(self):
        """The inventory on which me is based
        """
        return self.parent

    def __init__(self):
        super(Slot, self).__init__(**Styles.SLOT_SHAPE)

        self.width, self.height = self.shape.width, self.shape.height

        self.is_activated = False

    def _sound_and_effect(self, when, enter=False):
        sd = self.parent.sounds[when]
        ef = self.parent.effects[when]

        if sd is not None and not enter:
            sound.play(sd)

        if ef is not None:
            # do effect with the anchor == center
            origin = copy(self.transform_anchor)
            self.transform_anchor = self.get_rect().center
            self.stop()
            self.do(ef)
            self.transform_anchor = origin

    def on_selected(self):
        if self.is_activated:
            return

        self._sound_and_effect('selected')

    def on_unselected(self):
        if self.is_activated:
            return

        self._sound_and_effect('unselected')

    def on_activated(self):
        self._sound_and_effect('activated')

    def on_inactivated(self):
        self._sound_and_effect('inactivated')

    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)


class OptionCard(CocosNode):
    @property
    def inventory(self):
        """The inventory on which me is based
        """
        return self.parent

    def __init__(self, *options):
        super(OptionCard, self).__init__()

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

        self.menu = OptionCardMenu(options, self.frames)
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


class OptionCardMenu(VerticalMenu):
    activate_sound = 'button_activate'

    @property
    def inventory(self):
        """The inventory on which me is based
        """
        return self.parent.parent.parent

    def __init__(self, options, frames):
        super(OptionCardMenu, self).__init__()

        # Option name -> Menu Item
        self._option_dict = {
            '': MenuItem('', None),
            '查看': MenuItem('查看', emitter.check),
            '出售': MenuItem('出售', emitter.sell),
            '全售': MenuItem('全售', emitter.sell_all),
            '装上': MenuItem('装上', emitter.equip),
            '卸下': MenuItem('卸下', emitter.unequip),
            '合成': MenuItem('合成', emitter.forge),
            '拆开': MenuItem('拆开', emitter.unpack),
            '全拆': MenuItem('全拆', emitter.unpack_all),
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
        super(OptionCardMenu, self).on_enter()

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

    def on_quit(self):
        del self.inventory.activated_slot


class InfoCard(CocosNode):
    """A card contains text and graphical info of an item
    You can refer/change the item by its 'item_id'
    """

    @property
    def inventory(self):
        """The inventory on which me is based
        """
        return self.parent

    def __init__(self):
        super(InfoCard, self).__init__()

        # LAYOUT STUFF

        #: the center of icon sprite
        self.icon_center = 43, 71
        self.icon_scale = 1.8

        #: the bottom center of name label
        self.name_bottom_center = 43, 0

        #: about description frame
        self.frame_bottom_left = 105, 0
        self.frame_size = 357, 113

        #: the left top corner of description label
        self.description_top_left = 113, 100

        # COMPONENT STUFF

        #: a Sprite imaged with the item icon
        self.icon = None

        #: a Label texted with item name string
        self.name = None

        #: a BorderedShape frames the item description text
        self.frame = None

        #: a Label texted with item description string
        self.description = None

        # FUNCTIONAL STUFF

        #: if the Info Card visible
        self.visible = False

        # EXECUTE STUFF

        #: build static components
        self._build()

    def _build(self):
        """Build the static components
        Things to be built:
            - Frame BorderedShape
        """
        # BUILD FRAME
        self.frame = BorderedShape(
            shape_name='Rect',
            position=self.frame_bottom_left,
            size=self.frame_size,
            **Styles.INFO_FRAME_SHAPE,
        )

        # ADD static components
        self.add(self.frame)

    def _update(self, item_id):
        """Update the dynamic components
        Things to update:
            - Icon Sprite
            - Name Label
            - Description Label
        """
        # KILL old ones
        for node in [self.icon, self.name, self.description]:
            if isinstance(node, CocosNode):
                node.kill()

        # UPDATE ICON
        self.icon = ItemQuery(item_id).get_sprite()
        self.icon.position = self.icon_center
        self.icon.do(ScaleTo(self.icon_scale, 0))

        # UPDATE NAME
        name_str = ItemQuery(item_id).name
        self.name = Label(name_str, **Styles.INFO_NAME_FONT)
        self.name.position = self.name_bottom_center

        # UPDATE DESCRIPTION

        #: fetch description from DB
        description_str = "  " + ItemQuery(item_id).description

        #: insert a '\n' per 19 chars to the description_str
        str_list = list(description_str)
        for i in range(len(str_list)):
            if i % 19 == 0 and i != 0:
                str_list.insert(i, '\n')
        description_str = ''.join(str_list)

        #: create a multiline RichLabel
        self.description = RichLabel(description_str, **Styles.INFO_DESCRIPTION_FONT)

        #: set position
        self.description.position = self.description_top_left

        # ADD new ones
        for node in [self.icon, self.name, self.description]:
            self.add(node)

    def open(self, item_id=None):
        """Set the Info Card visible.
        If a index 'item_id' is given, update the info content to the corresponding item's
        """
        self.visible = True

        if item_id is not None:
            # update the dynamic components
            self._update(item_id)

    def close(self):
        """Set the Info Card invisible.
        """
        self.visible = False
