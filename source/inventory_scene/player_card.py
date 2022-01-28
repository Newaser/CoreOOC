from cocos.euclid import Vector2
from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.text import Label
from pyglet.window import mouse

from db.item import ItemQuery
from public.audio import sound
from public.defaults import Styles, Player
from public.events import emitter
from public.image import GUI
from public.shapes import BorderedShape
from public.stat import im, stat
from super.inventory.inventory import CardInventory
from super.inventory.inventory_components import OptionCard


class PlayerCard(Layer):
    """A card that contains the present player's information:
        1. The player's name
        1. The airplane's status
        2. The airplane's inventory
    """

    def __init__(self):
        super(PlayerCard, self).__init__()
        # LAYOUT STUFF

        #: about the body panel
        self.body_bottom_left = 213, 193
        self.body_size = 300, 390

        #: about the name bar
        self.name_bar_top_center = \
            self.body_bottom_left[0] + self.body_size[0] / 2, \
            self.body_bottom_left[1] + self.body_size[1] - 20

        #: about the frame of the airplane drawing
        self.frame_size = 200, 200
        self.frame_bottom_left = \
            self.body_bottom_left[0] + (self.body_size[0] - self.frame_size[0]) / 2, \
            self.body_bottom_left[1] + 110

        #: about the airplane drawing
        self.drawing_center = \
            tuple((Vector2(*self.frame_bottom_left) + Vector2(*self.frame_size) / 2)[:])

        # COMPONENT STUFF

        #: the body panel Shape
        self.body = None

        #: a name bar Label
        self.name_bar = None

        #: a frame Shape contains the airplane drawing
        self.drawing_frame = None

        #: a drawing Sprite of the airplane
        self.drawing = None

        #: an Inventory of equipments attached
        self.equipments = None

        # EXECUTIONS
        self._build()

    def _build(self):
        """Build components
        """
        # BUILD body panel
        self.body = BorderedShape(
            shape_name='Rect',
            position=self.body_bottom_left,
            size=self.body_size,
            **Styles.PLAYER_CARD_BODY_RECT,
        )

        # BUILD name bar
        self.name_bar = Label(Player.NICKNAME[stat.present_player], **Styles.PLAYER_CARD_NAME_FONT)
        self.name_bar.position = self.name_bar_top_center

        # BUILD drawing frame
        self.drawing_frame = BorderedShape(
            shape_name='Rect',
            position=self.frame_bottom_left,
            size=self.frame_size,
            **Styles.PLAYER_CARD_FRAME_RECT,
        )

        # BUILD drawing
        self.drawing = Sprite(GUI.DICT[Player.DEFAULT_AIRPLANE[stat.present_player]])
        self.drawing.position = self.drawing_center

        # BUILD equipments Inventory
        self.equipments = AirplaneInventory()
        self.equipments.start_position =\
            self.frame_bottom_left[0] + (self.frame_size[0] - self.equipments.width) / 2, \
            self.frame_bottom_left[1] - 20
        self.equipments.create_inventory()

        # ADD
        self.add(self.body)
        self.add(self.name_bar)
        self.add(self.drawing)
        self.add(self.drawing_frame)
        self.add(self.equipments)

    def switch_player(self):
        # TODO: Switch the present player
        pass


class AirplaneInventory(CardInventory):
    effects = Styles.INVENTORY_EFFECTS
    sounds = Styles.INVENTORY_SOUNDS

    def __init__(self):
        super(AirplaneInventory, self).__init__()

        # Category
        self.category = 'equipment'

        # Init layout
        self.number = 3
        self.max_column = 5
        self.spacing = (13, 13)
        self.start_position = (213, 193 + 67)

        # Set card
        # "*查看" means checking remotely
        self.card = OptionCard('*查看', '卸下')

        # DEPRECATE 'item_triples'
        del self.item_triples

        # USE 'icon_list'(records the icon sprite of items)
        self.icon_list = []

    @property
    def activated_item_id(self):
        return im.airplane_equipments[stat.present_player][self.activated_idx]

    def _update_items(self, given_triples=None):
        """Rewrite the item updating method
        - The order is:
            kill_old_icons -> update_icon_list -> add_new_icons
        """
        # KILL old icons
        for icon in self.icon_list:
            if icon is not None:
                icon.kill()

        # UPDATE the icon list
        self.icon_list.clear()
        for equipment_id in im.airplane_equipments[stat.present_player]:
            if equipment_id is None:
                self.icon_list.append(None)
            else:
                self.icon_list.append(ItemQuery(equipment_id).get_sprite())

        # ADD new icons to the inventory
        for idx, icon in enumerate(self.icon_list):
            if icon is not None:
                # SET POSITION for the icon
                icon.position = self.slots[idx].get_rect().center

                # ADD
                self.add(icon)

    def on_mouse_release(self, x, y, button, modifier):
        if button not in (mouse.LEFT, mouse.RIGHT):
            return

        in_slots, idx = self._in_any_slot((x, y))

        if in_slots:
            # If the slot mouse in contains an item
            if im.airplane_equipments[stat.present_player][idx] is not None:
                self._activate_slot(idx, (x, y))
        else:
            self._inactivate_slot()

    def on_check(self, _):
        pass

    def on_sell(self, num):
        pass

    def on_sell_all(self):
        pass

    def on_remote_check(self):
        """Check a item's info remotely.
        The item's ID will be provided by this inventory, but
        the request 'check' will be handled by another inventory
        """
        # Inform another inventory to handle 'check' event
        emitter.check(self.activated_item_id)

        # INACTIVATE the slot
        self._inactivate_slot()

    def on_unequip(self):
        if self.activated_idx is None:
            return

        # UNEQUIP and UPDATE
        im.unequip(stat.present_player, self.activated_idx)
        self._update_items()

        # SOUND
        sound.play('drop_equip')

        # INACTIVE slot, and EMIT EVENT
        self._inactivate_slot()
        emitter.finish_unequip()

    def on_equipped(self):
        """After an equipment is equipped
        """
        self._update_items()

