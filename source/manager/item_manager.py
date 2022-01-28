from copy import copy

from cocos.text import Label

from db.item import ItemQuery, get_category_list
from db.unpacking import UnpackingQuery
from public.defaults import Player, Styles
from public.errors import UnaffordableError, ExcessiveRemovingError, ItemOverflowError, AlreadyDoneError


class ItemManager:
    """Manage items that the player possess with a given item_id-item_number dictionary.
    """

    def __init__(self, items, airplane_equipments):
        self.items = items
        self.airplane_equipments = airplane_equipments

    def add(self, item_id, num=1):
        """Add a specific amount of items
        If num is negative, add to the max

        :return: How much item has been added
        """
        # TODO: If num is negative, add the item to the max
        assert num >= 0
        self.items[item_id] += num

        return num

    def remove(self, item_id, num=1):
        """Remove a specific amount of items
        If num is negative, remove all items identified 'item_id'

        :return: How much item has been removed
        """
        if num < 0:
            num = self.items[item_id]
        if num > self.items[item_id]:
            raise ExcessiveRemovingError

        self.items[item_id] -= num

        return num

    def clear(self, item_id_list=None):
        """Set amount of items in batches
        """
        # Default: clear all items
        if item_id_list is None:
            item_id_list = self.items.keys()

        # Clear
        for key in item_id_list:
            self.items[key] = 0

    def has(self, item_id):
        """If there's any item identified 'item_id'
        """
        return self.items[item_id] > 0

    def airplane_full(self, player_name):
        """If a player's airplane has been fully equipped
        """
        return None not in self.airplane_equipments[player_name]

    def airplane_empty(self, player_name):
        """If a player's airplane doesn't have any equipments
        """
        for equip_id in self.airplane_equipments[player_name]:
            if equip_id is not None:
                return False
        return True

    def airplane_add(self, player_name, item_id):
        """Add an item to a player's airplane
        """
        if player_name not in Player.DEFAULT_MEMBERS:
            raise ValueError("Unknown player")
        # if the airplane has already been fully equipped
        if self.airplane_full(player_name):
            raise ItemOverflowError
        # if such equipment has already been equipped to the airplane
        if item_id in self.airplane_equipments[player_name]:
            raise AlreadyDoneError

        for idx, value in enumerate(self.airplane_equipments[player_name]):
            if value is None:
                self.airplane_equipments[player_name][idx] = item_id
                break

    def airplane_remove(self, player_name, idx):
        """Remove an item from a player's airplane via index

        Example::

            # remove the first equipment of player1's airplane
            removed_item_id = item_manager.airplane_remove('player1', 0)

        :return: the id of the removed item
        """
        if player_name not in Player.DEFAULT_MEMBERS:
            raise ValueError("Unknown player")
        if self.airplane_equipments[player_name][idx] is None:
            raise AlreadyDoneError(f"The slot indexed '{idx}' is already empty")

        removed_item_id = copy(self.airplane_equipments[player_name][idx])

        self.airplane_equipments[player_name][idx] = None

        return removed_item_id

    def goods(self):
        """Return a list of item_id of items that is buyable
        """
        return [key for key in self.items.keys() if ItemQuery(key).buyable]

    def get_item_triples(self, items=None, categories=None, sorting=True):
        """Return a list of triples about items that the player possess,
        each of the triples consists of:

            (item_id, icon_sprite, amount_label)

        :param items: The item list, default: all items
        :param categories: Restrict the categories, default: all categories(except 'coin')
        :param sorting: If the triple list will be sorted by 'item_id'
        :return: A triple list: [(item_id, icon_sprite, amount_label)] * n
        """
        # Set default values
        if items is None:
            items = self.items
        if categories is None:
            categories = get_category_list()

        # Construct the triple list
        triples = [
            (
                key,  # item_id
                ItemQuery(key).get_sprite(),  # item_icon
                Label(str(value), **Styles.ITEM_COUNTER_FONT),  # item_counter
            )
            for key, value in items.items()
            if value > 0 and ItemQuery(key).category in categories
        ]

        # Sorted by item_id
        if sorting:
            def by_item_id(ele):
                return ele[0]

            triples.sort(key=by_item_id)

        return triples

    def sell(self, item_id, num=1):
        """Sell a specific amount of items
        If num is negative, sell all items identified 'item_id'

        :return:
            1. If the items identified as 'item_id' sold out after selling, return False; else True;
            2. The amount of coins obtained via selling

        Example::

            # sell ten Gold Ingots
            item_manager.sell('MaM0', 10)

            # sell all Filbert Kernel(s)
            item_manager.sell('MaT0', -1)
        """
        if item_id == 'C0':
            raise ValueError("Coin cannot be traded as items")
        if self.items[item_id] < num:
            raise UnaffordableError

        remove_amount = self.remove(item_id, num)
        coin_obtained = remove_amount * ItemQuery(item_id).selling_price
        self.add('C0', coin_obtained)

        # RETURN
        # 1. whether the items identified as 'item_id' sold out
        # 2. the amount of coins obtained
        return self.has(item_id), coin_obtained

    def buy(self, item_id, num=1):
        """Buy a specific amount of items

        Example::

            # buy one Optical Reactor
            item_manager.buy('MaT5', 1)
        """
        if item_id == 'C0':
            raise ValueError("Coin cannot be traded as items")
        if num < 0:
            raise ValueError("A negative value of num is given on buying")
        if self.items['C0'] < num * ItemQuery(item_id).buying_price:
            raise UnaffordableError

        self.remove('C0', num * ItemQuery(item_id).buying_price)
        self.items[item_id] += num

    def unpack(self, item_id, num=1):
        """Unpack a specific amount of chests

        :return:
            1. If the items identified as 'item_id' runs out, return False; else True;
            2. A list [(obtained_item_icon0, amount0), (obtained_item_icon1, amount1), ...]

        Example::

            # unpack an equipment supply
            item_manager.unpack('Ch3', 1)
        """
        if num < 0:
            num = self.items[item_id]

        # RETURN value
        tuples = []

        # PERFORM an unpacking experiment
        obtained = UnpackingQuery(item_id).experiment(num)

        # If the experiment succeeds
        #: REMOVE the unpacked chests
        self.remove(item_id, num)

        #: ADD the treasures and APPEND the tuple list
        for treasure_id, amount in obtained.items():
            self.add(treasure_id, amount)
            tuples.append((ItemQuery(treasure_id).get_sprite(), amount))

        return self.has(item_id), tuples

    def equip(self, player_name, item_id):
        """Equip an equipment to a player's airplane

        Example::

            # equip a nuclear artillery to player1's airplane
            item_manager.equip('player1', 'Eq3')
        """
        # ERRORS
        if player_name not in Player.DEFAULT_MEMBERS:
            raise ValueError("Unknown player")
        if ItemQuery(item_id).category != 'equipment':
            raise ValueError("Only equipment can be equipped")
        if not self.has(item_id):
            raise ValueError("Such item not enough")

        # ADD the equipment to the airplane
        self.airplane_add(player_name, item_id)

        # REMOVE the equipment from the inventory
        self.remove(item_id)

    def unequip(self, player_name, idx):
        """Unequip the equipment in specific slot of a player's airplane

        Example::

            # unequip the equipment in the first slot of player1's airplane
            item_manager.unequip('player1', 0)
        """
        if player_name not in Player.DEFAULT_MEMBERS:
            raise ValueError("Unknown player")
        if not 0 <= idx < len(self.airplane_equipments[player_name]):
            raise IndexError(f"The index '{idx}' exceeds")

        # DROP the item at index 'idx' from the airplane
        dropped_item_id = self.airplane_remove(player_name, idx)

        # PICK the dropped item to the inventory
        self.add(dropped_item_id)
