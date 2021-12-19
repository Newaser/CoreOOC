from copy import copy

from cocos.sprite import Sprite
from cocos.collision_model import AARectShape

from super.fight.physics import Physics2, Vector2, Rect
from public.defaults import Window


class Actor(Sprite):
    def __init__(self, image):
        super(Actor, self).__init__(image)

        # Define physics and collision
        self.phy = Physics2(
            m=1,
            x=Vector2(),
            v=Vector2(),
            drag_c=0.007
        )
        self.cshape = AARectShape(Vector2(), 0, 0)

        # Set default move boundary
        self.phy.boundary = Rect(
            self.width / 2,
            self.height / 2,
            Window.WIDTH - self.width,
            Window.HEIGHT - self.height,
        )
        # Set default position
        self.unified_position = Window.WIDTH / 2, Window.HEIGHT / 2
        # Set default size of box collider
        self.c_size = 25, 25
        # Set default category
        self.category = 'other'

    def move(self, dt):
        self.phy.update(dt)
        self.unify_positions()

    def unify_positions(self, towards='phy'):
        """Update Order: phy_position -> screen_position -> c_position
        """
        if towards == 'phy':
            self.position = tuple(self.phy.x[:])
            self.cshape.center = copy(self.phy.x)
        elif towards == 'self':
            self.phy.x = Vector2(*self.position)
            self.cshape.center = Vector2(*self.position)
        elif towards == 'c':
            self.phy.x = copy(self.cshape.center)
            self.position = tuple(self.cshape.center[:])
        else:
            raise ValueError("Invalid value of 'towards' is given")

    def _set_unified_position(self, position):
        if not isinstance(position, Vector2):
            position = Vector2(*position)

        self.phy.x = position
        self.unify_positions()

    def _set_c_size(self, size):
        self._c_size = size
        self.cshape.rx = size[0]
        self.cshape.ry = size[1]

    unified_position = property(lambda self: tuple(self.phy.x[:]), _set_unified_position)

    c_size = property(lambda self: (self.cshape.rx, self.cshape.ry), _set_c_size)
