from cocos.layer import ColorLayer
from cocos.collision_model import CollisionManagerGrid

from public.defaults import Window
from public.stat import key_map


class PhyField(ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(PhyField, self).__init__(245, 222, 179, 255, Window.WIDTH, Window.HEIGHT)

        # Actor list
        self.actors = {
            'player': [],
            'enemy': [],
            'other': [],
        }

        # Collision Manager
        self.cm = CollisionManagerGrid(0, Window.WIDTH, 0, Window.HEIGHT, 50 * 1.25, 50 * 1.25)

    def on_enter(self):
        super(PhyField, self).on_enter()

        self.refresh_cm()
        self.schedule(self.update)

    def update(self, dt):
        for actor_list in self.actors.values():
            for actor in actor_list:
                actor.move(dt)

        self.refresh_cm()
        self.detect_collision()

    def refresh_cm(self):
        self.cm.clear()
        for actor_list in self.actors.values():
            for actor in actor_list:
                self.cm.add(actor)

    def detect_collision(self):
        # Case 1: collision between players
        if self.actors['player'][1] in self.cm.objs_colliding(self.actors['player'][0]):
            self.actors['player'][0].phy.collide(self.actors['player'][1].phy)
            self.actors['player'][0].unify_positions()
            self.actors['player'][1].unify_positions()

    def add(self, actor, z=0, name=None):
        assert actor.category in self.actors.keys()

        super(PhyField, self).add(actor, z, name)
        self.actors[actor.category].append(actor)

    def on_key_press(self, symbol, _):
        for actor in self.actors['player']:
            actor.on_key_press(symbol, _)

    def on_key_release(self, symbol, _):
        if symbol in key_map['pause']:
            pass
        else:
            for actor in self.actors['player']:
                actor.on_key_release(symbol, _)
