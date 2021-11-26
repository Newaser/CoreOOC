from cocos.draw import *
from pyglet import gl
from pyglet.shapes import *


# class MyLine(Line):
#     def __init__(self, start, end, color, stroke_width=1):
#          self
#
#     def draw(self):
#         super().__init__(start, end, color, stroke_width)


class _ImprovedBorderedRectangle(BorderedRectangle):
    def __init__(self, x, y, width, height, border=1, body_rgba=(255, 255, 255, 255),
                 border_rgba=(100, 100, 100, 255), batch=None, group=None):
        # Split opacity from RGB
        self._body_rgb = body_rgba[:3]
        self._border_rgb = border_rgba[:3]
        self._opacity = body_rgba[3]
        self._border_opacity = border_rgba[3]

        super().__init__(x, y, width, height, border, self._body_rgb, self._border_rgb, batch, group)

        self.transform_anchor = self.x + self.width / 2, self.y + self.height / 2

    def _update_color(self):
        self._vertex_list.colors[:] = [*self._rgb, self._opacity] * 4 + \
                                      [*self._brgb, self._border_opacity] * 4

    def move(self):
        # TODO: Define a method 'move()' that implements: Delete the original graphic, and blit a new one
        pass

    def delete(self):
        super().delete()
        # TODO: Add some thing here to welcome the addition of method 'move()'
        pass


class Rectangle(CocosNode):
    def __init__(self, x, y, width, height, border=1, color=(255, 255, 255, 255),
                 border_color=(100, 100, 100, 255), batch=None, group=None):
        super().__init__()

        self.rect = _ImprovedBorderedRectangle(x, y, width, height, border, color, border_color, batch, group)
        self.anchor = self.rect.transform_anchor

    def draw(self, *args, **kwargs):
        gl.glPushMatrix()
        self.transform()
        self.rect.draw()
        gl.glPopMatrix()

