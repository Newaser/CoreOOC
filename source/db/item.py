from cocos.sprite import Sprite
from public.image import Items as ItemPic


def get_id_list():
    # TODO: Get all item IDs from DB
    return []


def get_category_list(except_coin=True):
    # TODO: Get all categories(RESTRICT) from DB
    #   If except_coin == True, do not include 'coin' category
    return []


def get_formatted_item_dict():
    """Get a default item dictionary maps item_id with item number
    Item numbers are all 0
    """
    item_dict = {}
    for item_id in get_id_list():
        item_dict[item_id] = 0

    return item_dict


class ItemQuery:
    """
    Query data of a item with a given 'item_id' from DB.
    """
    def __init__(self, item_id):
        # Item ID corresponding to item_id from DB
        self.item_id = item_id

    def get_sprite(self):
        """Get a sprite with the corresponding image
        """
        return Sprite(ItemPic.DICT[self.item_id])

    # TODO: Finish "properties" down below using DB
    #   For example: func 'name()' returns the name of item whose item_id == self.item_id
    @property
    def name(self):
        return

    @property
    def raw_name(self):
        return

    @property
    def category(self):
        return

    @property
    def description(self):
        return

    @property
    def buyable(self):
        return

    @property
    def buying_price(self):
        return

    @property
    def selling_price(self):
        return
