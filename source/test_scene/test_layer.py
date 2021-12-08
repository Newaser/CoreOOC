from cocos.layer import ColorLayer

from .actor import Actor, Vector2
from public.defaults import Window
from public.settings import current_settings

key_map = current_settings['key_map']


class TestLayer(ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(TestLayer, self).__init__(245, 222, 179, 255, Window.WIDTH, Window.HEIGHT)

        self.actor = Actor()
        self.add(self.actor)

        self.schedule(self.update_)

    def update_(self, dt):
        self.actor.phy.update(dt)
        self.actor.position = self.actor.phy.x

    def on_key_press(self, symbol, _):
        if symbol in key_map['battle_up']:
            self.actor.phy.force('F_up', Vector2(0, 1000))
        elif symbol in key_map['battle_down']:
            self.actor.phy.force('F_down', Vector2(0, -1000))
        elif symbol in key_map['battle_left']:
            self.actor.phy.force('F_left', Vector2(-940, 0))
        elif symbol in key_map['battle_right']:
            self.actor.phy.force('F_right', Vector2(940, 0))
        elif symbol in key_map['speed']:
            self.actor.phy.motion_scale *= 2

    def on_key_release(self, symbol, _):
        if symbol in key_map['battle_up']:
            self.actor.phy.release('F_up')
        elif symbol in key_map['battle_down']:
            self.actor.phy.release('F_down')
        elif symbol in key_map['battle_left']:
            self.actor.phy.release('F_left')
        elif symbol in key_map['battle_right']:
            self.actor.phy.release('F_right')
        elif symbol in key_map['speed']:
            self.actor.phy.motion_scale *= 0.5
