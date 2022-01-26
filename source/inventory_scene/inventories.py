from super.inventory.inventory import CardInventory, OptionCard
from public.defaults import Window, Styles


class EquipmentInventory(CardInventory):
    effects = Styles.INVENTORY_EFFECTS
    sounds = Styles.INVENTORY_SOUNDS

    def __init__(self):
        super(EquipmentInventory, self).__init__()

        # Category
        self.category = 'equipment'

        # Init layout
        self.number = 15
        self.max_column = 6
        self.spacing = (13, 13)
        self.start_position = (666, Window.HEIGHT - 233)

        # Set card
        self.card = OptionCard('查看', '装上', '出售', '全部出售')

        self.create_inventory()


class MaterialInventory(CardInventory):
    effects = Styles.INVENTORY_EFFECTS
    sounds = Styles.INVENTORY_SOUNDS

    def __init__(self):
        super(MaterialInventory, self).__init__()

        # Category
        self.category = 'material'

        # Init layout
        self.number = 16
        self.max_column = 6
        self.spacing = (13, 13)
        self.start_position = (666, Window.HEIGHT - 233)

        # Set card
        self.card = OptionCard('查看', '出售', '全部出售')

        self.create_inventory()


class BlueprintInventory(CardInventory):
    effects = Styles.INVENTORY_EFFECTS
    sounds = Styles.INVENTORY_SOUNDS

    def __init__(self):
        super(BlueprintInventory, self).__init__()

        # Category
        self.category = 'blueprint'

        # Init layout
        self.number = 17
        self.max_column = 6
        self.spacing = (13, 13)
        self.start_position = (666, Window.HEIGHT - 233)

        # Set card
        self.card = OptionCard('查看', '合成', '出售', '全部出售')

        self.create_inventory()


class ChestInventory(CardInventory):
    effects = Styles.INVENTORY_EFFECTS
    sounds = Styles.INVENTORY_SOUNDS

    def __init__(self):
        super(ChestInventory, self).__init__()

        # Category
        self.category = 'chest'

        # Init layout
        self.number = 18
        self.max_column = 6
        self.spacing = (13, 13)
        self.start_position = (666, Window.HEIGHT - 233)

        # Set card
        self.card = OptionCard('查看', '拆开', '全部拆开', '出售', '全部出售')

        self.create_inventory()
