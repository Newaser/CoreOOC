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
        __coin_set = resource.image("coin_set.png")
        __blue_plane = resource.image("blue_plane.png")
        __red_plane = resource.image("red_plane.png")

    except resource.ResourceNotFoundException as e:
        raise SystemExit(e)

    coin_animation = Animation.from_image_sequence(ImageGrid(__coin_set, 4, 1), 0.1)

    DICT = {
        'blue_plane': __blue_plane,
        'red_plane': __red_plane,
    }


class Items:
    resource.path.append("../res/image/items/")
    resource.reindex()

    try:
        __equipment_set = resource.image("equipments.png")
        __blueprint_set = resource.image("blueprints.png")
        __chest_set = resource.image("chests.png")
        __ingot_set = resource.image("ingots.png")
        __coin_item = resource.image("coin.png")
    except resource.ResourceNotFoundException as e:
        raise SystemExit(e)

    DICT = {}
    equipments = ImageGrid(__equipment_set, 1, 5)
    blueprints = ImageGrid(__blueprint_set, 1, 5)
    chests = ImageGrid(__chest_set, 1, 4)
    ingots = ImageGrid(__ingot_set, 2, 3)

    DICT['C0'] = __coin_item
    for i in range(4):
        DICT['Ch' + str(i)] = chests[i]
    for i in range(5):
        DICT['Eq' + str(i)] = equipments[i]
        DICT['Bp' + str(i)] = blueprints[i]
    for i in range(6):
        DICT['MaM' + str(i)] = ingots[i]


class Test:
    resource.path.append("../res/image/test/")
    resource.reindex()

    actor = resource.image("actor.png")
    swiftness = resource.image("swiftness.png")
