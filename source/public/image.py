from pyglet import resource
from pyglet.image import ImageGrid, Animation, load


class StartImage:
    """
    Load images concerning: Start Scene
    """
    resource.path.append("../res/image/GUI/start_scene")
    resource.reindex()

    try:
        background = resource.image("background.png")
        logo = resource.image("logo.png")
    except resource.ResourceNotFoundException as e:
        raise SystemExit(e)
