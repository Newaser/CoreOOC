from cocos.text import Label
from cocos.sprite import Sprite

from db import db
from public.image import Items as ItemPic


def get_id_list():
    """Get all item IDs from DB
    """
    sql = "SELECT item_id FROM item"
    data = db.fetch(db.DEFAULT_CONNECT, sql)

    # Transform query result to list
    return [ele[0] for ele in data]


def get_category_list(except_coin=True):
    """Get all categories(DISTINCT) from DB
    If except_coin == True, do not include 'coin' category
    """
    sql = "SELECT DISTINCT category FROM item"
    if except_coin:
        sql += " WHERE category NOT IN ('coin')"
    data = db.fetch(db.DEFAULT_CONNECT, sql)
    return [ele[0] for ele in data]


def get_formatted_item_dict():
    """Get a default item dictionary maps item_id with item number
    Item numbers are all 0
    """

    return {item_id: 0 for item_id in get_id_list()}


class ItemQuery:
    """
    Query data of a item with a given 'item_id' from DB.
    """

    def __init__(self, item_id):
        # Item ID corresponding to item_id from DB
        self.item_id = item_id

    def __repr__(self):
        # Get all field names of table 'item'
        fields = db.get_field_list(db.DEFAULT_CONNECT, 'item')

        # A dictionary maps field names with values
        info_dict = {field: getattr(self, field) for field in fields}

        return str(info_dict)

    def _field_query(self, field):
        """Get the value of a given field
        """
        sql = f"SELECT {field} FROM item " \
              f"WHERE item_id = '{self.item_id}'"
        data = db.fetch(db.DEFAULT_CONNECT, sql)

        return data[0][0]

    def get_sprite(self):
        """Get a sprite with the corresponding image
        """
        return Sprite(ItemPic.DICT[self.item_id])

    @property
    def name(self):
        return self._field_query('name')

    @property
    def raw_name(self):
        return self._field_query('raw_name')

    @property
    def category(self):
        return self._field_query('category')

    @property
    def description(self):
        return self._field_query('description')

    @property
    def buyable(self):
        return bool(self._field_query('buyable'))

    @property
    def buying_price(self):
        return self._field_query('buying_price')

    @property
    def selling_price(self):
        return self._field_query('selling_price')
