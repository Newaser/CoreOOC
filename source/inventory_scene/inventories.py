from super.inventory import CardInventory, Card
from public.defaults import Window, Styles


class EquipmentInventory(CardInventory):
    def __init__(self):
        super(EquipmentInventory, self).__init__()

        # Category
        self.category = 'equipment'

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

        # Category
        self.category = 'material'

        # Init layout
        self.number = 16
        self.rows = 3
        self.max_column = 6
        self.margin = (0, 0)
        self.start_position = (666, Window.HEIGHT - 233)

        # Set card
        self.card = Card('查看', '出售')

        self.create_inventory(Styles.slot)


class BlueprintInventory(CardInventory):
    def __init__(self):
        super(BlueprintInventory, self).__init__()

        # Category
        self.category = 'blueprint'

        # Init layout
        self.number = 17
        self.rows = 3
        self.max_column = 6
        self.margin = (0, 0)
        self.start_position = (666, Window.HEIGHT - 233)

        # Set card
        self.card = Card('查看', '合成', '出售')

        self.create_inventory(Styles.slot)


class ChestInventory(CardInventory):
    def __init__(self):
        super(ChestInventory, self).__init__()

        # Category
        self.category = 'chest'

        # Init layout
        self.number = 18
        self.rows = 3
        self.max_column = 6
        self.margin = (0, 0)
        self.start_position = (666, Window.HEIGHT - 233)

        # Set card
        self.card = Card('查看', '拆开', '出售')

        self.create_inventory(Styles.slot)
