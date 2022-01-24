from scipy.stats import binom

from db import db
from db.item import ItemQuery


class UnpackingQuery:
    """
    Query data about unpacking with a specific chest identified with 'chest_id' in DB.
    """

    def __init__(self, item_id):
        if not ItemQuery(item_id).category == 'chest':
            raise ValueError(f"Item identified with '{item_id}' is not a chest")

        self.chest_id = item_id

    def __treasure_triples(self):
        """A list of triples that records the treasures of the chest.

        Formed as::

            [(probability0, treasure_id0, amount0), (probability1, treasure_id1, amount1), ...]
        """
        sql = f"SELECT probability, treasure_id, amount " \
              "FROM unpacking " \
              f"WHERE chest_id = '{self.chest_id}'"

        return db.fetch(db.DEFAULT_CONNECT, sql)

    def experiment(self, n=1):
        """Perform a n-multiple Bernoulli Experiment of unpacking

        :param n: the multiple of the experiment
        :return: a dictionary {obtained_item_id: amount}
        """
        # the dictionary of item obtained
        obtained = {}

        # PERFORM the Bernoulli Experiment
        for p, treasure_id, amount in self.__treasure_triples():
            treasure_num = amount * binom.rvs(n, p)
            if treasure_num > 0:
                if treasure_id not in obtained.keys():
                    obtained[treasure_id] = treasure_num
                else:
                    obtained[treasure_id] += treasure_num

        return obtained
