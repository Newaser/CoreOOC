from cocos.draw import *
from pyglet import gl
from pyglet import shapes


class _Arc(shapes.Arc):
    pass


class _Circle(shapes.Circle):
    # TODO
    pass


class _Ellipse(shapes.Ellipse):
    # TODO
    pass


class _Sector(shapes.Sector):
    pass


class _Line(shapes.Line):
    def __init__(self, start, end, thickness=1, rgba=(255, 255, 255, 255)):
        # Split opacity from RGB
        self._rgb = rgba[:3]
        self._opacity = rgba[3]

        super(_Line, self).__init__(*start, *end, thickness, self._rgb)

        self.transform_anchor = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2


class _Rectangle(shapes.Rectangle):
    # TODO
    pass


class _BorderedRectangle(shapes.BorderedRectangle):
    def __init__(self, position, size, border_thickness=1, body_rgba=(255, 255, 255, 255),
                 border_rgba=(100, 100, 100, 255)):
        # Split opacity from RGB
        self._body_rgb = body_rgba[:3]
        self._border_rgb = border_rgba[:3]
        self._opacity = body_rgba[3]
        self._border_opacity = border_rgba[3]

        super().__init__(*position, *size, border_thickness, self._body_rgb, self._border_rgb)

        self.transform_anchor = self.x + self.width / 2, self.y + self.height / 2

    def _update_color(self):
        self._vertex_list.colors[:] = [*self._rgb, self._opacity] * 4 + \
                                      [*self._brgb, self._border_opacity] * 4


class _Triangle(shapes.Triangle):
    # TODO
    pass


class _Star(shapes.Star):
    # TODO
    pass


class _Polygon(shapes.Polygon):
    pass


_shape_dict = {
    'Arc': _Arc,
    'Circle': _Circle,
    'Ellipse': _Ellipse,
    'Sector': _Sector,
    'Line': _Line,
    'Rect': _Rectangle,
    'Rectangle': _Rectangle,
    'Bordered Rect': _BorderedRectangle,
    'Bordered Rectangle': _BorderedRectangle,
    'Triangle': _Triangle,
    'Star': _Star,
    'Polygon': _Polygon,
}


class Shape(CocosNode):
    def __init__(self, shape_name, *args, **kwargs):
        super().__init__()

        self.shape = _shape_dict[shape_name](*args, **kwargs)
        self.anchor = self.shape.transform_anchor

    def draw(self, *args, **kwargs):
        gl.glPushMatrix()
        self.transform()
        self.shape.draw()
        gl.glPopMatrix()



