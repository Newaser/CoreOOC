from cocos.director import director
from cocos.menu import *
from pyglet.window import mouse

from public.settings import current_settings


key_map = current_settings["key_map"]


class MyMenu(Menu):

    def __init__(self):
        super(MyMenu, self).__init__()

        self.mouse_pressed = False

    def _select_item(self, new_idx):
        # If 'selected_index' remains uninitialized, init it
        if self.selected_index is None:
            if self.select_sound:
                self.select_sound.play()

            self.children[new_idx][1].is_selected = True
            self.children[new_idx][1].on_selected()

            self.selected_index = new_idx

        super()._select_item(new_idx)

    def _build_items(self, layout_strategy):
        super()._build_items(layout_strategy)

        # Undo the initialization that the superclass has done
        self.children[self.selected_index][1].is_selected = False
        self.selected_index = None

    def _activate_item(self):
        try:
            super(MyMenu, self)._activate_item()
        except TypeError:
            pass

    def on_key_press(self, symbol, modifiers):
        if symbol in key_map["back"]:
            # self.on_exit()
            return True
        elif symbol in key_map["OK"]:
            self._activate_item()
            return True
        elif symbol in key_map["down"] or symbol in key_map["up"]:
            if self.selected_index is None:
                new_idx = 0
            else:
                if symbol in key_map["down"]:
                    new_idx = self.selected_index + 1
                else:
                    new_idx = self.selected_index - 1

                if new_idx < 0:
                    new_idx = len(self.children) - 1
                elif new_idx > len(self.children) - 1:
                    new_idx = 0

            self._select_item(new_idx)
            return True
        else:
            try:
                # send the menu item the rest of the keys
                ret = self.children[self.selected_index][1].on_key_press(symbol, modifiers)

                # play sound if key was handled
                if ret and self.activate_sound:
                    self.activate_sound.play()
                return ret
            except TypeError:
                return False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            (x, y) = director.get_virtual_coordinates(x, y)
            try:
                if self.children[self.selected_index][1].is_inside_box(x, y):
                    self.mouse_pressed = True
                    self._activate_item()
            except TypeError:
                pass

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            try:
                super().on_mouse_release(x, y, button, modifiers)
            except TypeError:
                pass
            self.mouse_pressed = False
            self.on_mouse_motion(x, y, 0, 0)

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.mouse_pressed:
            super().on_mouse_motion(x, y, dx, dy)

