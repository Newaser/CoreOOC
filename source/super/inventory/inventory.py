from cocos.layer import Layer
from cocos.rect import Rect
from pyglet.window import mouse

from public.defaults import Z, SAVE_PATH
from public.errors import ItemOverflowError
from public.events import emitter
from public.stat import im, key_map, stat
from public.transitions import black_field_transition
from super.inventory.inventory_component import OptionCard, Slot, InfoCard


class Inventory(Layer):
    """Abstract base class for inventory layers.
    Inventory is used to store items.

    Normal usage is:

     - create a subclass
     - override __init__ to set all style attributes,
       and then call `create_inventory()`
     - Finally you shall add the inventory to an `Scene` or another `Layer`
    """
    is_event_handler = True

    # dictionary of sounds & effects happening on select, activate
    when = ['selected', 'unselected', 'activated', 'inactivated']
    sounds = {key: None for key in when}
    effects = {key: None for key in when}

    # category of the inventory items
    category = None

    def __init__(self):
        super(Inventory, self).__init__()
        # LAYOUT STUFF

        #: number of slots
        self.number = 1

        #: max number of columns in a line
        self.max_column = 1

        #: X, Y spacings between adjacent slots
        self.spacing = (0, 0)

        #: top left corner of the inventory(used in slot building)
        self.start_position = (0, 0)

        # COMPONENT STUFF

        #: list of slots
        self.slots = []

        #: list of triples concerning items: [(item_id, item_amount, item_sprite)] * n
        self.item_triples = []

        #: item info card
        self.info_card = InfoCard()

        # FUNCTIONAL STUFF

        #: define which slot is currently selected, activated
        self.selected_idx = None
        self.activated_idx = None

    @property
    def rows(self):
        """Amount of slot rows
        """
        return self.number // self.max_column

    @property
    def width(self):
        """Overall width of the inventory
        """
        return self.slots[0].width * self.max_column + self.spacing[0] * (self.number - 1)

    @property
    def height(self):
        """Overall height of the inventory
        """
        return self.slots[0].height * self.rows + self.spacing[1] * (self.number - 1)

    @property
    def size(self):
        """Overall size of the inventory
        """
        return self.width, self.height

    def on_enter(self):
        super(Inventory, self).on_enter()

        # ADD event handlers
        emitter.push_handlers(self)

        # RESET
        self._unselect_slot()
        self._inactivate_slot()
        self._update_items()

    def on_exit(self):
        super(Inventory, self).on_exit()

        # REMOVE event handlers
        emitter.remove_handlers(self)

        # CLOSE the info card
        self.info_card.close()

        # SAVE the records to the save file
        stat.recorder.write(SAVE_PATH)

    def create_inventory(self):
        """Create a basic inventory with slots. At the end of
        __init__ in subclasses of :class:`Inventory`, call this method.
        """
        # Add slots
        self._build_slots()

        # Add the info card
        self.info_card.position = 666, 110
        self.add(self.info_card)

    '''
    About slots
    '''
    def _build_slots(self):
        """Build the slot array starting at the left top corner
        From left to right, then from the top down

        Start
        v
        o-----------
        |          |
        |          |
        |          |
        ------------
        """
        for i in range(self.number):
            # CREATE a new slot
            slot = Slot()

            # SET position for the slot
            x, y = self.start_position
            x += (i % self.max_column) * (slot.width + self.spacing[0])
            y -= (i // self.max_column) * (slot.height + self.spacing[1]) + slot.height
            slot.position = x, y

            # ADD
            self.slots.append(slot)
            self.add(slot)

    def _select_slot(self, idx):
        if idx == self.selected_idx:
            return

        self.selected_idx = idx
        self.slots[idx].on_selected()

    def _unselect_slot(self):
        if self.selected_idx is None:
            return

        self.slots[self.selected_idx].on_unselected()
        self.selected_idx = None

    def _activate_slot(self, idx, click_position=None):
        """When the slot with index 'idx' is activated
        """
        if idx == self.activated_idx:
            return

        self.activated_idx = idx
        self.slots[idx].is_activated = True
        self.slots[idx].on_activated()

    def _inactivate_slot(self, click_position=None):
        """Inactivate the currently activated slot
        """
        if self.activated_idx is None:
            return

        self.slots[self.activated_idx].is_activated = False
        self.slots[self.activated_idx].on_inactivated()
        self.activated_idx = None

    def _in_any_slot(self, point):
        """Check if the given point in any area of slot.
        If in, find out in which slot
        """
        for idx, slot in enumerate(self.slots):
            if slot.get_rect().contains(*point):
                return True, idx
        return False, None

    '''
    About Items
    '''
    def _update_items(self):
        """Update arrangement of item icons and item amount counters,
        meanwhile update self.item_triples according to the statistics.

        - The order is:
            fetch_statistics -> kill_old_nodes -> update_triples -> add_new_nodes
        """
        # FETCH categorized item triples from the game statistics
        stat_triples = im.get_item_triples(categories=self.category)

        # if number of items EXCEEDS slot number, ERROR
        if len(stat_triples) > self.number:
            raise ItemOverflowError

        # KILL every item icon and item amount counter from the inventory if it exists
        for triple in self.item_triples:
            for i in [1, 2]:
                if triple[i].parent is not None:
                    triple[i].kill()

        # UPDATE self.item_triples
        self.item_triples = stat_triples

        # ADD all updated item icons and item amount counters to the inventory
        for idx, triple in enumerate(self.item_triples):
            # GET the slot, icon and counter from the triple
            slot = self.slots[idx]
            icon = triple[1]
            counter = triple[2]

            # SET POSITION of the icon and counter
            icon.position = slot.get_rect().center
            counter.position = slot.get_rect().right, slot.get_rect().bottom

            # ADD
            self.add(icon)
            self.add(counter)

    def _get_item_info(self, idx):
        # TODO: Get the info of item with index 'idx'
        pass

    '''
    About events
    '''
    def on_key_press(self, symbol, _):
        if symbol in key_map["back"]:
            self.on_quit()
            return True

    def on_mouse_motion(self, x, y, dx, dy):
        p1 = (x - dx, y - dy)
        p2 = (x, y)

        p1_in_areas, idx1 = self._in_any_slot(p1)
        p2_in_areas, idx2 = self._in_any_slot(p2)

        if not p1_in_areas and p2_in_areas:
            self._select_slot(idx2)
        elif p1_in_areas and not p2_in_areas:
            self._unselect_slot()
        elif p1_in_areas and p2_in_areas and idx1 != idx2:
            self._unselect_slot()
            self._select_slot(idx2)

    def on_mouse_release(self, x, y, button, modifier):
        if button not in (mouse.LEFT, mouse.RIGHT):
            return

        in_slots, idx = self._in_any_slot((x, y))

        if in_slots:
            # If the slot mouse in contains an item
            if idx < len(self.item_triples):
                self._activate_slot(idx, (x, y))
        else:
            self._inactivate_slot((x, y))

    @staticmethod
    def on_quit():
        black_field_transition()

    def on_check(self):
        # GET the ID of item to be sold
        activated_item_id = self.item_triples[self.activated_idx][0]

        # Open the info card with item_id
        self.info_card.open(activated_item_id)

    def on_sell(self, num):
        # GET the ID of item to be sold
        activated_item_id = self.item_triples[self.activated_idx][0]

        # SELL and UPDATE
        still_have = im.sell(activated_item_id, num)
        self._update_items()

        # if the type of item sold out
        if not still_have:
            self._inactivate_slot()

    def on_sell_all(self):
        # '-1' means sell all
        self.on_sell(-1)

    def on_equip(self):
        pass

    def on_forge(self):
        pass

    def on_unpack(self):
        pass


class CardInventory(Inventory):
    def __init__(self):
        super(CardInventory, self).__init__()

        # Create a option card
        self.card = OptionCard('')

    def _card_move_to(self, position):
        """Move Card to a certain spot
        """
        # Card move
        self.card.position = position

        self.card.is_open = True

    def _card_remove(self):
        self.card.is_open = False

    def _in_card(self, point):
        if not self.card.is_open:
            return False
        card_box = Rect(*self.card.position, *self.card.size)
        return card_box.contains(*point)

    def on_enter(self):
        super(CardInventory, self).on_enter()

        self.add(self.card, z=Z.TOP)
        self._card_remove()

    def _activate_slot(self, idx, click_position=None):
        in_new_area = self.activated_idx is None
        in_the_same_area = idx == self.activated_idx

        case = {
            '1': in_new_area,
            '2': in_the_same_area and not self.card.is_open,
            '3': in_the_same_area and self.card.is_open,
            '4': not in_the_same_area and self.card.is_open,
        }

        if case['1'] or case['2'] or case['4']:
            self._inactivate_slot()
            super(CardInventory, self)._activate_slot(idx)

            x = click_position[0] - \
                (click_position[0] > self.start_position[0] + self.width / 2) * self.card.body.shape.width
            y = click_position[1] - \
                (click_position[1] > self.start_position[1] - self.height / 2) * self.card.body.shape.height
            self._card_move_to((x, y))

        elif case['3']:
            self._inactivate_slot()

    def _inactivate_slot(self, click_position=None):
        super(CardInventory, self)._inactivate_slot()
        self._card_remove()

    activated_slot = property(fdel=_inactivate_slot)

    def on_mouse_motion(self, x, y, dx, dy):
        if self._in_card((x, y)):
            return 
        super(CardInventory, self).on_mouse_motion(x, y, dx, dy)
        
    def on_mouse_release(self, x, y, button, _):
        if self._in_card((x, y)):
            return
        super(CardInventory, self).on_mouse_release(x, y, button, _)
