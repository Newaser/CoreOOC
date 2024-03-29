from db.item import ItemQuery
from inventory_scene.player_card import PlayerCard
from manager.assistant import Assistant
from public.audio import sound
from public.errors import ItemOverflowError, AlreadyDoneError, UnaffordableError
from public.events import emitter
from public.stat import im, stat
from super.inventory.inventory import CardInventory, OptionCard
from public.defaults import Window, Styles


class EquipmentInventory(CardInventory):
    effects = Styles.INVENTORY_EFFECTS
    sounds = Styles.INVENTORY_SOUNDS

    # Singleton
    player_card = None

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

        # BUILD
        self.create_inventory()
        self.create_player_card()

    def create_player_card(self):
        """Create the player card which displays the player's airplane
        """
        # SINGLETON
        if self.player_card is None:
            self.player_card = PlayerCard()

        # ADD the player's airplane card
        self.add(self.player_card)

    def on_equip(self):
        try:
            im.equip(stat.present_player, self.activated_item_id)
        except ItemOverflowError:
            Assistant.warn("装备槽已满！")
        except AlreadyDoneError:
            Assistant.warn("重复装备！")
        else:
            # UPDATE items
            self._update_items()

            # SOUND
            sound.play('equip')

            # INACTIVE slot, and EMIT EVENT
            self._inactivate_slot()
            emitter.finish_equip()

    def on_unequipped(self):
        """After an equipment is unequipped
        """
        self._update_items()


class MaterialInventory(CardInventory):
    effects = Styles.INVENTORY_EFFECTS
    sounds = Styles.INVENTORY_SOUNDS

    def __init__(self):
        super(MaterialInventory, self).__init__()

        # Category
        self.category = 'material'

        # Init layout
        self.number = 18
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
        self.number = 18
        self.max_column = 6
        self.spacing = (13, 13)
        self.start_position = (666, Window.HEIGHT - 233)

        # Set card
        self.card = OptionCard('查看', '合成', '出售', '全部出售')

        self.create_inventory()

    def on_forge(self):
        try:
            # FORAGE, NOTIFY and UPDATE
            still_have, outcome_id = im.forage(self.activated_item_id)
            Assistant.notify([(ItemQuery(outcome_id).get_sprite(), 1)])
            self._update_items()
            Assistant.update_money()

            # if the type of item sold out
            if not still_have:
                self._inactivate_slot()
                self.info_card.close()
        except UnaffordableError:
            Assistant.warn("原料不足！")


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

    def on_unpack(self, num):
        # UNPACK, NOTIFY and UPDATE
        still_have, tuple_list = im.unpack(self.activated_item_id, num)
        Assistant.notify(tuple_list)
        self._update_items()
        Assistant.update_money()

        # if the type of chest runs out
        if not still_have:
            self._inactivate_slot()
            self.info_card.close()

    def on_unpack_all(self):
        # '-1' means unpack all
        self.on_unpack(-1)
