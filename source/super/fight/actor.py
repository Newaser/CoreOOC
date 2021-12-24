from copy import copy

from cocos.sprite import Sprite
from cocos.collision_model import AARectShape

from super.fight.physics import Physics2, Vector2, Rect
from public.defaults import Window


class Actor(Sprite):
    # Set default category
    category = 'other'

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

    def move(self, dt):
        self.phy.update(dt)
        self.unify_positions()

    def unify_positions(self, towards='phy'):
        """Unify positions of Physics & Screen & Collision towards one of them.
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

    unified_position = property(lambda self: tuple(self.phy.x[:]), _set_unified_position,
                                doc="Set positions of Physics & Screen & Collision in a row.")

    c_size = property(lambda self: (self.cshape.rx, self.cshape.ry), _set_c_size,
                      doc="The size of box collider")


class LivingActor(Actor):
    def __init__(self, image):
        super(LivingActor, self).__init__(image)

        self.__HP = 1
        self.__max_HP = 1

    def on_enter(self):
        super(LivingActor, self).on_enter()
        self.reset_HP()

    def __set_HP(self, points):
        if points <= 0:
            self.__HP = 0
            self.on_dead()
        elif points > self.__max_HP:
            self.__HP = self.__max_HP
        else:
            self.__HP = points

    HP = property(lambda self: self.__HP, __set_HP)

    def __set_max_HP(self, points):
        if points < 0:
            self.__max_HP = 0
        else:
            self.__max_HP = points

        if self.__HP > self.__max_HP:
            self.HP = self.__max_HP

    max_HP = property(lambda self: self.__max_HP, __set_max_HP)

    def reset_HP(self, points=None):
        if points is None:
            points = self.max_HP

        assert points >= 0
        self.max_HP = points
        self.HP = self.max_HP

    def heal(self, points):
        assert points >= 0

        self.HP += points

        self.on_heal()

    def damage(self, points):
        assert points >= 0

        self.HP -= points

        self.on_damage()

    def on_dead(self):
        pass

    def on_heal(self):
        pass

    def on_damage(self):
        pass
