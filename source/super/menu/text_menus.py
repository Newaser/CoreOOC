from cocos.director import director
from cocos.menu import *
from pyglet.window import mouse

from public.stat import key_map
from public.audio import sound
from public.actions import *


class VerticalMenu(Menu):
    # If the menu can switch menu items circularly
    circular_switch = False

    def __init__(self):
        super(VerticalMenu, self).__init__()

        self.mouse_pressed = False
        self.switch_keys = key_map['up'], key_map['down']

    def _build_items(self, layout_strategy):
        super()._build_items(layout_strategy)

        # Undo the initialization that the superclass has done
        self.children[self.selected_index][1].is_selected = False
        self.selected_index = None

    def _select_item(self, new_idx, way=None):
        if self.selected_index is not None:
            # If the selected item is selected
            if new_idx == self.selected_index:
                return
            else:
                # Unselect the old item
                self.before_switch(self.selected_index, new_idx, way)
                self.children[self.selected_index][1].is_selected = False
                self.children[self.selected_index][1].on_unselected()

        # Play select sound
        if self.select_sound:
            sound.play(self.select_sound)

        # Select the new item, update selected index
        self.children[new_idx][1].is_selected = True
        self.children[new_idx][1].on_selected()
        self.selected_index = new_idx
        self.after_switch(self.selected_index, new_idx, way)

    def _activate_item(self, way=None):
        if self.selected_index is not None:
            self.before_activate(self.selected_index, way)

            if self.activate_sound:
                sound.play(self.activate_sound)

            self.children[self.selected_index][1].on_activated()
            self.children[self.selected_index][1].on_key_press(key_map["OK"][0], 0)

            self.after_activate(self.selected_index, way)

    def on_enter(self):
        super().on_enter()
        self.mouse_pressed = False

    def on_text(self, text):
        if self.selected_index is not None:
            super(VerticalMenu, self).on_text(text)

    def on_key_press(self, symbol, modifiers):
        if symbol in key_map["back"]:
            self.on_quit()
            return True
        elif symbol in key_map["OK"]:
            self._activate_item(way='key')
            return True
        elif symbol in self.switch_keys[0] or symbol in self.switch_keys[1]:
            old_idx = self.selected_index
            if old_idx is None:
                if symbol in self.switch_keys[0]:
                    new_idx = len(self.children) - 1
                else:
                    new_idx = 0
            else:
                if symbol in self.switch_keys[0]:
                    new_idx = old_idx - 1
                else:
                    new_idx = old_idx + 1

                if self.circular_switch:
                    if new_idx < 0:
                        new_idx = len(self.children) - 1
                    elif new_idx > len(self.children) - 1:
                        new_idx = 0
                else:
                    if new_idx < 0:
                        new_idx = 0
                    elif new_idx > len(self.children) - 1:
                        new_idx = len(self.children) - 1

            # Finally, select an item
            self._select_item(new_idx, way='key')
            return True
        else:
            if self.selected_index is not None:
                # send the menu item the rest of the keys
                ret = self.children[self.selected_index][1].on_key_press(symbol, modifiers)

                # play sound if key was handled
                if ret and self.activate_sound:
                    self.activate_sound.play()
                return ret

    def on_mouse_press(self, x, y, button, _):
        if button == mouse.LEFT:
            self.mouse_pressed = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            # If an item is selected
            if self.selected_index is not None:
                (x, y) = director.get_virtual_coordinates(x, y)
                if self.children[self.selected_index][1].is_inside_box(x, y):
                    self._activate_item(way='mouse')

            # Set mouse unpressed, then execute on_mouse_motion() with no movement
            self.mouse_pressed = False
            self.on_mouse_motion(x, y, 0, 0)

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.mouse_pressed:
            (x, y) = director.get_virtual_coordinates(x, y)
            for idx, i in enumerate(self.children):
                item = i[1]
                if item.is_inside_box(x, y):
                    self._select_item(idx, way='mouse')
                    break

    def on_quit(self):
        """
        When key_map['back'] pressed,
        event:
        """
        pass

    def before_switch(self, old_idx, new_idx, way=None):
        pass

    def after_switch(self, old_idx, new_idx, way=None):
        pass

    def before_activate(self, idx, way=None):
        pass

    def after_activate(self, idx, way=None):
        pass


class HorizontalMenu(VerticalMenu):
    def __init__(self):
        super(HorizontalMenu, self).__init__()

        self.selected_index = 0
        self.last_activated_index = None
        self.switch_keys = key_map['left'], key_map['right']

    def _activate_item(self, way=None):
        if self.last_activated_index == self.selected_index:
            return
        else:
            self.last_activated_index = self.selected_index
            super(HorizontalMenu, self)._activate_item(way)

    def on_enter(self):
        super(HorizontalMenu, self).on_enter()

        self.selected_index = 1
        self.last_activated_index = None
        self._select_item(0, way='enter')

    def after_switch(self, old_idx, new_idx, way=None):
        if way in ('key', 'enter'):
            self._activate_item(way=way)
