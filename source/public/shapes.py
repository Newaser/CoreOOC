from cocos.draw import *
from pyglet import gl
from pyglet import shapes


class _ImprovedLine(shapes.Line):
    def __init__(self, start, end, thickness=1, rgba=(255, 255, 255, 255)):
        # Split opacity from RGB
        self._rgb = rgba[:3]
        self._opacity = rgba[3]

        super(_ImprovedLine, self).__init__(*start, *end, thickness, self._rgb)

        self.transform_anchor = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2


class _ImprovedBorderedRectangle(shapes.BorderedRectangle):
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


_klass_dict = {
    'Line': _ImprovedLine,
    'Rect': _ImprovedBorderedRectangle,
    'Rectangle': _ImprovedBorderedRectangle,
}


class Shape(CocosNode):
    def __init__(self, shape_name, *args, **kwargs):
        super().__init__()

        self.shape = _klass_dict[shape_name](*args, **kwargs)
        self.anchor = self.shape.transform_anchor

    def draw(self, *args, **kwargs):
        gl.glPushMatrix()
        self.transform()
        self.shape.draw()
        gl.glPopMatrix()



