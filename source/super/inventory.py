from copy import copy
from numpy import sign

from cocos.layer import Layer
from cocos.batch import BatchNode
from cocos.sprite import Sprite
from cocos.rect import Rect
from pyglet.window import mouse

from public.image import Items
from public.shapes import Shape
from public.settings import current_settings


class Inventory(Layer):
    is_event_handler = True

    def __init__(self):
        super(Inventory, self).__init__()

        # Create a batch to manage slots
        self.slot_batch = BatchNode()

        # Create lists to point to slots and its attributes
        self.slots = []
        self.valid_areas = []

        # About layout
        self.number = 1
        self.max_column = 1
        self.margin = (0, 0)
        self.start_position = (0, 0)

        # Rows & Size cannot be assigned currently
        self.rows = 0
        self.width = 0
        self.height = 0
        self.size = self.width, self.height

        # Define which slot is currently selected, activated
        self.selected_idx = None
        self.activated_idx = None

        # About style
        self.slot_style = {
            "image": None,
            "valid_area": Rect(0, 0, 0, 0),
            "selected_effect": None,
            "unselected_effect": None,
        }

        # Create thr inventory according to a given slot_style and layout
        # self.create_inventory(slot_style)

    def create_inventory(self, slot_style):
        self._build_slots(slot_style)

    def _build_slots(self, slot_style):
        # Create a batch to manage slots
        self.slot_batch = BatchNode()
        self.add(self.slot_batch)

        # Add slots to the batch
        for i in range(self.number):
            slot = Slot(**slot_style)
            slot.image_anchor = 0, 0

            x, y = self.start_position
            x += i % self.max_column * slot.width + sign(i) * self.margin[0]  # X-coordinate
            y -= i // self.max_column * slot.height + sign(i) * self.margin[1] + slot.height  # Y-coordinate
            slot.position = x, y

            self.slot_batch.add(slot)

        # Fill the list pointing to slots
        self.slots = self.slot_batch.get_children()

        # Fill valid area list with the coordinate to world
        for slot in self.slots:
            area = slot.valid_area
            world_position = self.slot_batch.point_to_world(slot.point_to_world(area.position))
            self.valid_areas.append(Rect(*world_position, *area.size))

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

    def _in_any_area(self, point):
        for idx in range(self.number):
            if self.valid_areas[idx].contains(*point):
                return True, idx
        return False, None

    def _update_items(self):
        # TODO: Update arrangement of items by remove all items and re-add all items according to item list
        pass

    def on_enter(self):
        super(Inventory, self).on_enter()

        # Calculate the rows and size
        self.rows = self.number // self.max_column
        self.width = self.slots[0].width * self.max_column + self.margin[0] * (self.number - 1)
        self.height = self.slots[0].height * self.rows + self.margin[1] * (self.number - 1)

        # Reset
        self._unselect_slot()
        self._inactivate_slot()
        self._update_items()

    def on_key_press(self, symbol, _):
        if symbol in current_settings["key_map"]["back"]:
            self.on_quit()
            return True

    def on_mouse_motion(self, x, y, dx, dy):
        p1 = (x - dx, y - dy)
        p2 = (x, y)

        p1_in_areas, idx1 = self._in_any_area(p1)
        p2_in_areas, idx2 = self._in_any_area(p2)

        if not p1_in_areas and p2_in_areas:
            self._select_slot(idx2)
        elif p1_in_areas and not p2_in_areas:
            self._unselect_slot()
        elif p1_in_areas and p2_in_areas and idx1 != idx2:
            self._unselect_slot()
            self._select_slot(idx2)

    def on_mouse_release(self, x, y, button, _):
        if not button == mouse.LEFT:
            return

        in_areas, idx = self._in_any_area((x, y))

        if in_areas:
            self._activate_slot(idx, (x, y))
        else:
            self._inactivate_slot((x, y))

    def on_quit(self):
        pass


class CardInventory(Inventory):
    def __init__(self):
        super(CardInventory, self).__init__()

        # Create a option card
        self.card = Shape(
            shape_name='Bordered Rect',
            position=(0, 0),
            size=(160, 225),
            border_thickness=2,
            body_rgba=(0, 0, 0, 178),
            border_rgba=(0, 0, 0, 255)
        )
        self.card_open = False

    def _card_move_to(self, position):
        # Card move
        self.card.position = position

        if not self.card_open:
            self.add(self.card)
            self.card_open = True

    def _card_remove(self):
        if self.card_open:
            self.card.kill()
            self.card_open = False

    def on_enter(self):
        super(CardInventory, self).on_enter()

        self._card_remove()

    def _activate_slot(self, idx, click_position=None):
        in_new_area = self.activated_idx is None
        in_the_same_area = idx == self.activated_idx

        case = {
            '1': in_new_area,
            '2': in_the_same_area and not self.card_open,
            '3': in_the_same_area and self.card_open,
            '4': not in_the_same_area and self.card_open,
        }

        if case['1'] or case['2'] or case['4']:
            self._inactivate_slot()
            super(CardInventory, self)._activate_slot(idx)

            x = click_position[0] - \
                (click_position[0] > self.start_position[0] + self.width / 2) * self.card.shape.width
            y = click_position[1] - \
                (click_position[1] > self.start_position[1] - self.height / 2) * self.card.shape.height
            self._card_move_to((x, y))

        elif case['3']:
            self._inactivate_slot()

    def _inactivate_slot(self, click_position=None):
        super(CardInventory, self)._inactivate_slot()
        self._card_remove()


class Slot(Sprite):
    """A slot of Inventory or Card
    """
    def __init__(self, image, valid_area=None, selected_effect=None,
                 unselected_effect=None, activated_effect=None, inactivated_effect=None):
        """Create a Slot with the 'image' and
        its valid clicking area 'valid_area'(use local position).
        """
        super(Slot, self).__init__(image)

        if valid_area is None:
            self.valid_area = Rect(0, 0, self.width, self.height)
        else:
            assert isinstance(valid_area, Rect)
            self.valid_area = valid_area

        self.is_activated = False
        self.selected_effect = selected_effect
        self.unselected_effect = unselected_effect
        self.activated_effect = activated_effect
        self.inactivated_effect = inactivated_effect

    def on_selected(self):
        if self.is_activated:
            return

        if self.selected_effect is not None:
            temp = copy(self.image_anchor)
            self.image_anchor = (self.width // 2, self.height // 2)

            self.stop()
            self.do(self.selected_effect)

            self.image_anchor = temp

    def on_unselected(self):
        if self.is_activated:
            return

        if self.unselected_effect is not None:
            temp = copy(self.image_anchor)
            self.image_anchor = (self.width // 2, self.height // 2)

            self.stop()
            self.do(self.unselected_effect)

            self.image_anchor = temp

    def on_activated(self):
        if self.activated_effect is not None:
            temp = copy(self.image_anchor)
            self.image_anchor = (self.width // 2, self.height // 2)

            self.stop()
            self.do(self.activated_effect)

            self.image_anchor = temp

    def on_inactivated(self):
        if self.inactivated_effect is not None:
            temp = copy(self.image_anchor)
            self.image_anchor = (self.width // 2, self.height // 2)

            self.stop()
            self.do(self.inactivated_effect)

            self.image_anchor = temp
