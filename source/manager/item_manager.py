from cocos.text import Label

from db.item import ItemQuery, get_category_list
from public.defaults import Styles
from public.errors import UnaffordableError, ExcessiveRemovingError


class ItemManager:
    """Manage items that the player possess with a given item_id-item_number dictionary.
    """

    def __init__(self, items):
        self.items = items

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

        :return: If the item identified 'item_id' sold out after
            selling, return False; else True

        Example::

            # sell ten Gold Ingots
            item_manager.sell('MaM0', 10)

            # sell all Filbert Kernel(s)
            item_manager.sell('MaT0', 10)
        """
        if item_id == 'C0':
            raise ValueError("Coin cannot be traded as items")
        if self.items[item_id] < num:
            raise UnaffordableError

        remove_amount = self.remove(item_id, num)
        self.add('C0', remove_amount * ItemQuery(item_id).selling_price)

        # return whether the player still has the type of items
        return self.items[item_id] > 0

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
