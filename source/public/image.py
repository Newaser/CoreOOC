from pyglet import resource
from pyglet.image import ImageGrid, Animation, load


class GUI:
    """
    Load images concerning: GUI
    """
    resource.path.append("../res/image/GUI/")
    resource.reindex()

    try:
        background_0 = resource.image("background_0.png")
        blurred_background_0 = resource.image("blurred_background_0.png")
        background_1 = resource.image("background_1.png")
        logo = resource.image("logo.png")
        slot = resource.image("slot.png")
        shield = resource.image("shield.png")
        iron_nuggets = resource.image("iron_nuggets.png")
        blueprint = resource.image("blueprint.png")
        chest = resource.image("chest.png")

    except resource.ResourceNotFoundException as e:
        raise SystemExit(e)


class Items:
    resource.path.append("../res/image/items/")
    resource.reindex()

    try:
        _equipment_set = resource.image("equipments.png")
        _metal_set = resource.image("metals.png")
        _chest_set = resource.image("chests.png")
        equipments = ImageGrid(_equipment_set, 1, 5)
        metals = ImageGrid(_metal_set, 1, 6)
        chests = ImageGrid(_chest_set, 1, 4)
    except resource.ResourceNotFoundException as e:
        raise SystemExit(e)


class Test:
    resource.path.append("../res/image/test/")
    resource.reindex()

    actor = resource.image("actor.png")
    swiftness = resource.image("swiftness.png")
