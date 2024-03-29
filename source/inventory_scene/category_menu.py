from cocos.layer import MultiplexLayer

from .inventories import *
from public.defaults import Window
from public.image import GUI
from public.transitions import black_field_transition
from super.menu.graphical_menus import GraphicalMenu, PicMenuItem


class CategoryMenu(GraphicalMenu):
    def __init__(self):
        super(CategoryMenu, self).__init__()

        # Set sounds & effects
        self.sounds['activated'] = 'shrill_page_slide'
        self.effects = Styles.CATEGORY_MENU_EFFECTS

        # Create menu item list
        self.items = []
        self.items.append(PicMenuItem(GUI.shield, self.on_equipment))
        self.items.append(PicMenuItem(GUI.iron_nuggets, self.on_material))
        self.items.append(PicMenuItem(GUI.blueprint, self.on_blueprint))
        self.items.append(PicMenuItem(GUI.chest, self.on_package))

        # About layout
        self.max_column = 4
        self.spacings = (15, 0)
        self.start_position = (676, Window.HEIGHT - 183)

        # About behavior
        self.default_activated = 0
        self.call_func_on_enter = False

        # Create the menu
        self.create_menu()

        # Add multi-inventories to the menu
        self.inventories = MultiplexLayer(
            EquipmentInventory(),
            MaterialInventory(),
            BlueprintInventory(),
            ChestInventory()
        )
        self.add(self.inventories)

    def on_enter(self):
        super(CategoryMenu, self).on_enter()

    def on_quit(self):
        black_field_transition()

    def on_equipment(self):
        self.inventories.switch_to(0)

    def on_material(self):
        self.inventories.switch_to(1)

    def on_blueprint(self):
        self.inventories.switch_to(2)

    def on_package(self):
        self.inventories.switch_to(3)
