"""
This file created self-defined game events, and registered them to an emitter.

Explanation of the events defined here:
    - "on_check": A request of checking information of an item
    - "on_sell": A request of selling one item
    - "on_sell_all": A request of selling all items with a same id
    - "on_buy": A request of buying a certain item
    - "on_equip": A request of equipping an equipment to a player
    - "on_unequip": A request of removing an equipment from a player
    - "on_forge": A request of using one blueprint
    - "on_unpack": A request of opening one treasure chest
    - "on_unpack_all": A request of opening all treasure chests with a same id
"""


from pyglet.event import EventDispatcher


_event_type_list = ['on_check', 'on_sell', 'on_sell_all', 'on_buy', 'on_equip',
                    'on_unequip', 'on_forge', 'on_unpack', 'on_unpack_all']


class Emitter(EventDispatcher):
    def check(self):
        self.dispatch_event('on_check')

    def sell(self, num=1):
        self.dispatch_event('on_sell', num)

    def sell_all(self):
        self.dispatch_event('on_sell_all')

    def buy(self, num=1):
        self.dispatch_event('on_buy', num)

    def equip(self):
        self.dispatch_event('on_equip')

    def unequip(self):
        self.dispatch_event('on_unequip')

    def forge(self):
        self.dispatch_event('on_forge')

    def unpack(self):
        self.dispatch_event('on_unpack')

    def unpack_all(self):
        self.dispatch_event('on_unpack_all')


# ADD all even type to the Emitter
for event in _event_type_list:
    Emitter.register_event_type(event)


# Create a Emitter OBJECT
emitter = Emitter()
