from cocos.layer import Layer

from public.shapes import Shape
from public.actions import *


class ShapeLayer(Layer):
    def __init__(self):
        super(ShapeLayer, self).__init__()

        # Rectangle Frame
        rect_frame = Shape(
            shape_name='Rect',
            position=(100, 100),
            size=(400, 400),
            border_thickness=10,
            body_rgba=(0, 0, 0, 0),
            border_rgba=(0, 0, 0, 230)
        )
        # rect_frame.do(thump())
        self.add(rect_frame)

        # A line
        a_line = Shape(
            shape_name='Line',
            start=(100, 100),
            end=(400, 500),
            thickness=3,
            rgba=(100, 150, 230, 255)
        )
        a_line.do(thump(2))
        self.add(a_line)
