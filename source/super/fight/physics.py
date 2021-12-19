from cocos.director import director
from cocos.euclid import Vector2
from cocos.rect import Rect


class Physics2(object):
    def __init__(self, m, x, v, drag_c=0):

        # Basic physical quantities
        self._m = m
        self._x = x
        self._v = v
        self._a = Vector2()
        self._f = Vector2()

        # Memo: the latest variation of x & v
        self._last_dx = Vector2()
        self._last_dv = Vector2()

        # Limits
        self._max_v_norm = None
        self._max_a_norm = None

        self._x_boundary = Rect(0, 0, *director.get_window_size())

        # About External Force
        self._ex_force = {}
        # Coefficient of air drag
        self.drag_c = drag_c
        # Scale of motion
        self.motion_scale = 1

    def update(self, dt):
        """Update physical quantities as it elapsed 'dt' secs
        """
        self._update_drag()

        # Kinetics Formulas
        dv = self.a * dt
        dx = self.v * dt + 1/2 * self.a * dt ** 2

        self.v += dv
        self.x += dx * self.motion_scale

        self._last_dv = dv
        self._last_dx = dx * self.motion_scale

    def _update_drag(self):
        """Update the value of drags
        """
        # if abs(self.v) < 0.25:
        #     self.v = Vector2()

        try:
            f_value = - self.v.normalized() * self.drag_c * abs(self.v) ** 2
            self.reforce('air_drag', f_value)
        except OverflowError:
            raise OverflowError("v = " + str(self.v))

    def _set_m(self, m):
        if m > 0:
            self._m = m

    def _set_x(self, x):
        if self.boundary is not None:
            if not self.boundary.contains(*x[:]):
                if not self.boundary.left <= x[0] <= self.boundary.right:
                    if x[0] < self.boundary.left:
                        self._x[0] = self.boundary.left
                    else:
                        self._x[0] = self.boundary.right
                    self._v[0] = 0
                if not self.boundary.bottom <= x[1] <= self.boundary.top:
                    if x[1] < self.boundary.bottom:
                        self._x[1] = self.boundary.bottom
                    else:
                        self._x[1] = self.boundary.top
                    self._v[1] = 0
                return
        self._x = x

    def _set_v(self, v):
        if self.max_v is not None:
            if v > self.max_v:
                return
        self._v = v

    def _set_a(self, a):
        if self.max_a is not None:
            if a > self.max_a:
                return
        self._a = a
        self._f = self._m * self._a

    def _set_f(self, f):
        if self.max_a is not None:
            if f > self.m * self.max_a:
                return
        self._f = f
        self._a = self._f / self._m

    def _set_max_v_norm(self, max_v_norm):
        self._max_v_norm = max_v_norm

    def _set_max_a_norm(self, max_a_norm):
        self._max_a_norm = max_a_norm

    def _set_x_boundary(self, new_boundary):
        self._x_boundary = new_boundary

    m = property(lambda self: self._m, _set_m)

    x = property(lambda self: self._x, _set_x)

    v = property(lambda self: self._v, _set_v)

    a = property(lambda self: self._a, _set_a)

    f = property(lambda self: self._f, _set_f)

    last_dx = property(lambda self: self._last_dx)

    last_dv = property(lambda self: self._last_dv)

    max_v = property(lambda self: self._max_v_norm, _set_max_v_norm)

    max_a = property(lambda self: self._max_a_norm, _set_max_a_norm)

    boundary = property(lambda self: self._x_boundary, _set_x_boundary)

    def still(self):
        self.v = Vector2(0, 0)
        self.a = Vector2(0, 0)
        self._ex_force.clear()

    def force(self, force_id, value):
        assert isinstance(value, Vector2)

        if force_id in self._ex_force.keys():
            assert self._ex_force[force_id] == value
            return

        self._ex_force[force_id] = value
        self.f += value

    def release(self, force_id):
        if force_id in self._ex_force.keys():
            self.f -= self._ex_force[force_id]
            del self._ex_force[force_id]

    def reforce(self, force_id, value):
        self.release(force_id)
        self.force(force_id, value)

    def collide(self, other):
        assert isinstance(other, self.__class__)

        m1 = self.m
        m2 = other.m
        v1 = self.v
        v2 = other.v

        # Complete elastic collision formulas
        v1_ = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
        v2_ = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)

        self.v = v1_
        other.v = v2_

        # Undo the displacements
        self.x -= self.last_dx
        other.x -= other.last_dx
