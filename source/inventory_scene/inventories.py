from super.inventory import CardInventory, Card
from public.defaults import Window, Styles


class EquipmentInventory(CardInventory):
    def __init__(self):
        super(EquipmentInventory, self).__init__()

        # Init layout
        self.number = 15
        self.rows = 3
        self.max_column = 6
        self.margin = (0, 0)
        self.start_position = (666, Window.HEIGHT - 233)

        # Set card
        self.card = Card('查看', '装上', '出售')

        self.create_inventory(Styles.slot)


class MaterialInventory(CardInventory):
    def __init__(self):
        super(MaterialInventory, self).__init__()

        # Init layout
        self.number = 16
        self.rows = 3
        self.max_column = 6
        self.margin = (0, 0)
        self.start_position = (666, Window.HEIGHT - 233)

        # Set card
        self.card = Card('查看', '出售')

        self.create_inventory(Styles.slot)
