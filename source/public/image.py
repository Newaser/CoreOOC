from pyglet import resource
from pyglet.image import ImageGrid, Animation, load


class GUI:
    """
    Load images concerning: Start Scene
    """
    resource.path.append("../res/image/GUI/")
    resource.reindex()

    try:
        background_0 = resource.image("background_0.png")
        blurred_background_0 = resource.image("blurred_background_0.png")
        background_1 = resource.image("background_1.png")
        logo = resource.image("logo.png")
    except resource.ResourceNotFoundException as e:
        raise SystemExit(e)
