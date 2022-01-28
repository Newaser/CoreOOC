"""
This file created self-defined game events, and registered them to an emitter.

Explanation of the events defined here:
    - "on_check": A request of checking information of an item
    - "on_remote_check": Check the information of an item remotely, which means
                            the one who provides the item's ID may not be the one
                            who displays the item's information
    - "on_sell": A request of selling one item
    - "on_sell_all": A request of selling all items with a same id
    - "on_buy": A request of buying a certain item
    - "on_equip": A request of equipping an equipment to a player
    - "on_equipped": Finish equipping an equipment
    - "on_unequip": A request of removing an equipment from a player
    - "on_unequipped": Finish unequipping an equipment from a player
    - "on_forge": A request of using one blueprint
    - "on_unpack": A request of opening one treasure chest
    - "on_unpack_all": A request of opening all treasure chests with a same id
"""


from pyglet.event import EventDispatcher


_event_type_list = ['on_check', 'on_remote_check', 'on_sell', 'on_sell_all', 'on_buy', 'on_equip', 'on_equipped',
                    'on_unequip', 'on_unequipped', 'on_forge', 'on_unpack', 'on_unpack_all']


class Emitter(EventDispatcher):
    """
    Emit different events
    """
    def check(self, item_id=None):
        self.dispatch_event('on_check', item_id)

    def remote_check(self):
        self.dispatch_event('on_remote_check')

    def sell(self, num=1):
        self.dispatch_event('on_sell', num)

    def sell_all(self):
        self.dispatch_event('on_sell_all')

    def buy(self, num=1):
        self.dispatch_event('on_buy', num)

    def equip(self):
        self.dispatch_event('on_equip')

    def finish_equip(self):
        self.dispatch_event('on_equipped')

    def unequip(self):
        self.dispatch_event('on_unequip')

    def finish_unequip(self):
        self.dispatch_event('on_unequipped')

    def forge(self):
        self.dispatch_event('on_forge')

    def unpack(self, num=1):
        self.dispatch_event('on_unpack', num)

    def unpack_all(self):
        self.dispatch_event('on_unpack_all')


# ADD all even type to the Emitter
for event in _event_type_list:
    Emitter.register_event_type(event)


# Create a Emitter OBJECT
emitter = Emitter()
