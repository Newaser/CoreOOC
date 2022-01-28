from pyglet.window import mouse

from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.rect import Rect
from cocos.euclid import Vector2

from public.audio import sound
from public.stat import key_map
from public.shapes import BorderedShape


class GraphicalMenu(Layer):
    is_event_handler = True

    # Initialize sounds & effects dicts
    stats = ['selected', 'unselected', 'activated', 'inactivated']
    sounds = {key: None for key in stats}
    effects = {key: None for key in stats}

    def __init__(self):
        super(GraphicalMenu, self).__init__()
        # Create a list to point to menu items
        self.items = []

        # About layout -to be assigned
        self.max_column = 1
        self.spacings = (0, 0)
        self.start_position = (0, 0)

        # About behavior
        self.max_activated = 1
        self.default_activated = None
        self.call_func_on_enter = True

        # About layout -assigned automatically later
        self.number = 1
        self.rows = 0
        self.width = 0
        self.height = 0
        self.size = self.width, self.height

        # About Item -assigned automatically later
        self.item_width = 0
        self.item_height = 0
        self.item_size = self.item_width, self.item_height

        # Define which slot is currently selected, activated
        self.selected_idx = None
        self.activated_idx = None

        # Create the menu
        # self.create_menu()

    def create_menu(self):
        # Sizes of items in item list must be the same
        self.item_size = self.items[0].width, self.items[0].height
        for item in self.items:
            if Vector2(item.width, item.height) != Vector2(*self.item_size):
                raise ValueError('''
                Menu can't be created: subsequent images should be the same size as the first one
                ''')

        self._build_items()

    def _build_items(self):
        # Set item position and add them to the menu
        start_xy = tuple((Vector2(*self.start_position) + Vector2(self.item_width, -self.item_height) // 2)[:])
        for i, item in enumerate(self.items):
            x, y = start_xy
            x += i % self.max_column * item.width + i * self.spacings[0]  # X-coordinate
            y -= i // self.max_column * item.height + i * self.spacings[1] + item.height  # Y-coordinate
            item.position = x, y

            self.add(item)

    def _select_item(self, idx):
        if idx == self.selected_idx:
            return

        self.selected_idx = idx
        self.items[idx].on_selected()

    def _unselect_item(self):
        if self.selected_idx is None:
            return

        self.items[self.selected_idx].on_unselected()
        self.selected_idx = None

    def _activate_item(self, idx, enter=False):
        if idx == self.activated_idx:
            return

        self.activated_idx = idx
        self.items[idx].is_activated = True
        self.items[idx].on_activated(enter, self.call_func_on_enter)

    def _inactivate_item(self):
        if self.activated_idx is None:
            return

        self.items[self.activated_idx].is_activated = False
        self.items[self.activated_idx].on_inactivated()
        self.activated_idx = None

    def _on_any_items(self, point):
        """If the given point on any area of items
        """
        item_boxes = [item.get_rect() for item in self.items]

        for idx in range(self.number):
            if item_boxes[idx].contains(*point):
                return True, idx
        return False, None

    def on_enter(self):
        super(GraphicalMenu, self).on_enter()

        # Calculate the rows and size
        self.number = len(self.items)
        self.rows = self.number // self.max_column
        self.width = self.items[0].width * self.max_column + self.spacings[0] * (self.number - 1)
        self.height = self.items[0].height * self.rows + self.spacings[1] * (self.number - 1)

        # Reset
        self._unselect_item()
        self._inactivate_item()
        if self.default_activated is not None:
            self._activate_item(self.default_activated, enter=True)

    def on_key_press(self, symbol, _):
        if symbol in key_map["back"]:
            self.on_quit()
            return True

    def on_mouse_motion(self, x, y, dx, dy):
        p1 = (x - dx, y - dy)
        p2 = (x, y)

        p1_on_items, idx1 = self._on_any_items(p1)
        p2_on_items, idx2 = self._on_any_items(p2)

        # Move in
        if not p1_on_items and p2_on_items:
            self._select_item(idx2)
        # Move out
        elif p1_on_items and not p2_on_items:
            self._unselect_item()
        # Jump to another
        elif p1_on_items and p2_on_items and idx1 != idx2:
            self._unselect_item()
            self._select_item(idx2)

    def on_mouse_release(self, x, y, button, _):
        if button != mouse.LEFT:
            return

        on_items, idx = self._on_any_items((x, y))

        # Click another menu item
        if on_items and idx != self.activated_idx:
            self._inactivate_item()
            self._activate_item(idx)

    def on_quit(self):
        pass


class PicMenuItem(Sprite):
    def __init__(self, image, callback_func):
        super(PicMenuItem, self).__init__(image)

        self.image_anchor = 0, 0

        self.callback_func = callback_func
        self.is_activated = False

    def _sound_and_effect(self, when, enter=False):
        sd = self.parent.sounds[when]
        ef = self.parent.effects[when]

        if sd is not None and not enter:
            sound.play(sd)

        if ef is not None:
            self.stop()
            self.do(ef)

    def on_selected(self):
        if self.is_activated:
            return

        self._sound_and_effect('selected')

    def on_unselected(self):
        if self.is_activated:
            return

        self._sound_and_effect('unselected')

    def on_activated(self, enter=False, enter_call=True):
        self._sound_and_effect('activated', enter)

        if not enter or (enter and enter_call):
            self.callback_func()

    def on_inactivated(self):
        self._sound_and_effect('inactivated')


class ShapeMenuItem(BorderedShape):
    def __init__(self, callback_func, *args, **kwargs):
        super(ShapeMenuItem, self).__init__(*args, **kwargs)

        self.width = self.shape.width
        self.height = self.shape.hight

        self.callback_func = callback_func
        self.is_activated = False

    def _sound_and_effect(self, when, enter=False):
        sd = self.parent.sounds[when]
        ef = self.parent.effects[when]

        if sd is not None and not enter:
            sound.play(sd)

        if ef is not None:
            self.stop()
            self.do(ef)

    def on_selected(self):
        if self.is_activated:
            return

        self._sound_and_effect('selected')

    def on_unselected(self):
        if self.is_activated:
            return

        self._sound_and_effect('unselected')

    def on_activated(self, enter=False, enter_call=True):
        self._sound_and_effect('activated', enter)

        if not enter or (enter and enter_call):
            self.callback_func()

    def on_inactivated(self):
        self._sound_and_effect('inactivated')

    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)
