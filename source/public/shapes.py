from cocos.cocosnode import CocosNode
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

    def _set_color(self, rgb):
        self._rgb = rgb
        self._update_color()

    color = property(lambda self: self._rgb, _set_color)

    def _set_opacity(self, opacity):
        self._opacity = opacity
        self._update_color()

    opacity = property(lambda self: self._opacity, _set_opacity)


class _Rectangle(shapes.Rectangle):
    # TODO
    pass


class _BorderedRectangle(shapes.BorderedRectangle):
    def __init__(self, position, size, border_thickness=1, body_rgba=(255, 255, 255, 255),
                 border_rgba=(100, 100, 100, 255)):
        # Split opacity from RGB
        self._body_rgb = body_rgba[:3]
        self._border_rgb = border_rgba[:3]
        self._body_opacity = body_rgba[3]
        self._border_opacity = border_rgba[3]

        super().__init__(*position, *size, border_thickness, self._body_rgb, self._border_rgb)

        self._size = size
        self._anchor = self.x + self.width / 2, self.y + self.height / 2

    @property
    def size(self):
        return self._size

    @property
    def original_anchor(self):
        return self._anchor

    def _update_color(self):
        float_rgba = [*self._body_rgb, self._body_opacity] * 4 + \
                                      [*self._border_rgb, self._border_opacity] * 4

        self._vertex_list.colors[:] = [int(i) for i in float_rgba]

    def _set_body_color(self, rgb):
        self._body_rgb = rgb
        self._update_color()

    color = property(lambda self: self._body_rgb, _set_body_color)

    def _set_body_opacity(self, opacity):
        self._body_opacity = opacity
        self._update_color()
        
    opacity = property(lambda self: self._body_opacity, _set_body_opacity)

    def _set_border_color(self, rgb):
        self._border_rgb = rgb
        self._update_color()

    border_color = property(lambda self: self._border_rgb, _set_border_color)

    def _set_border_opacity(self, opacity):
        self._border_opacity = opacity
        self._update_color()

    border_opacity = property(lambda self: self._border_opacity, _set_border_opacity)


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
    'Triangle': _Triangle,
    'Star': _Star,
    'Polygon': _Polygon,
}

_bordered_dict = {
    'Rect': _BorderedRectangle,
    'Rectangle': _BorderedRectangle,
}


class Shape(CocosNode):
    def __init__(self, shape_name, *args, **kwargs):
        super().__init__()

        self.shape = _shape_dict[shape_name](*args, **kwargs)

        # Define Anchor
        self.transform_anchor = self.shape.transform_anchor
        self.anchor = self.transform_anchor

    def draw(self, *args, **kwargs):
        gl.glPushMatrix()
        self.transform()
        self.shape.draw()
        gl.glPopMatrix()

    def _set_color(self, rgb):
        self.shape.color = rgb

    color = property(lambda self: self.shape.color, _set_color)

    def _set_opacity(self, opacity):
        self.shape.opacity = opacity

    opacity = property(lambda self: self.shape.opacity, _set_opacity)


class BorderedShape(Shape):
    def __init__(self, shape_name, *args, **kwargs):
        super(Shape, self).__init__()

        self.shape = _bordered_dict[shape_name](*args, **kwargs)
        self.anchor = self.shape.original_anchor

    def _set_border_color(self, rgb):
        self.shape.border_color = rgb

    border_color = property(lambda self: self.shape.border_color, _set_border_color)

    def _set_border_opacity(self, opacity):
        self.shape.border_opacity = opacity

    border_opacity = property(lambda self: self.shape.border_opacity, _set_border_opacity)
