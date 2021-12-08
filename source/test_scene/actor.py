from cocos.sprite import Sprite

from super.physics import Physics2, Vector2, Rect
from public.defaults import Window
from public.image import Test


class Actor(Sprite):
    def __init__(self):
        super(Actor, self).__init__(Test.actor)

        self.position = Window.WIDTH / 2, Window.HEIGHT / 2

        self.phy = Physics2(m=1, x=Vector2(*self.position), drag_c=0.007)

        # Set the boundary
        self.phy.boundary = Rect(
            self.width / 2,
            self.height / 2,
            Window.WIDTH - self.width,
            Window.HEIGHT - self.height
        )
