from db.item import ItemQuery, get_category_list


class ItemManager:
    """Manage items that the player possess with a given item_id-item_number dictionary.
    """
    def __init__(self, items):
        self.items = items

    def add(self, item_id, num=1):
        """Add a given amount of items
        """
        assert num >= 0
        self.items[item_id] += num

    def remove(self, item_id, num=1):
        """Remove a given amount of items
        """
        assert num >= 0
        assert self.items[item_id] - num >= 0
        self.items[item_id] -= num

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

    def get_sprite_triples(self, items=None, categories=None, sorting=True):
        """Return a list of triples about items the player possess,
        each of the triples consists of:
            (item_id, item_number, item_sprite)
        :param items: The item list, default: all items
        :param categories: Restrict the categories, default: all categories(except 'coin')
        :param sorting: If the triple list will be sorted by 'item_id'
        :return: A triple list: [(item_id, item_number, item_sprite)] * n
        """
        # Set default values
        if items is None:
            items = self.items
        if categories is None:
            categories = get_category_list()

        # Construct the triple list
        triples = [
            (key, value, ItemQuery(key).get_sprite())
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
        """Sell a given amount of items
        """
        assert item_id != 'C0'
        assert num >= 0
        assert self.items[item_id] - num >= 0

        self.items[item_id] -= num
        self.add('C0', num * ItemQuery(item_id).selling_price)

    def buy(self, item_id, num=1):
        """Buy a given amount of items
        If the money is insufficient, raise 'ValueError'
        """
        assert item_id != 'C0'
        assert num >= 0
        if self.items['C0'] < num * ItemQuery(item_id).buying_price:
            raise ValueError

        self.remove('C0', num * ItemQuery(item_id).buying_price)
        self.items[item_id] += num
