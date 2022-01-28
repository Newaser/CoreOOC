from db import db
from db.item import ItemQuery


class RecipeQuery:
    """
    Query data about recipes on blueprints with a specific 'blueprint_id'
    """

    def __init__(self, item_id):
        if not ItemQuery(item_id).category == 'blueprint':
            raise ValueError(f"Item identified with '{item_id}' is not a blueprint")

        self.blueprint_id = item_id

    @property
    def outcome_id(self):
        sql = f"SELECT outcome_id FROM recipe " \
              f"WHERE blueprint_id = '{self.blueprint_id}'"

        return db.fetch(db.DEFAULT_CONNECT, sql)[0][0]

    def get_material_dict(self):
        """
        The raw material dictionary of the recipe, formed as::

            {
            raw_material_id0: amount0,
            raw_material_id1: amount1,
            ...
            }
        """
        sql = f"SELECT raw_material_id, amount FROM recipe " \
              f"WHERE blueprint_id = '{self.blueprint_id}'"

        material_tuples = db.fetch(db.DEFAULT_CONNECT, sql)

        return {m_tuple[0]: m_tuple[1] for m_tuple in material_tuples}
