from cocos.layer import Layer

from public.shapes import Shape
from public.actions import *


class OptionsShapeLayer(Layer):
    def __init__(self):
        super(OptionsShapeLayer, self).__init__()

        # Main panel & its rect wireframe
        main_panel = Shape(
            shape_name='Bordered Rect',
            position=(170, 105),
            size=(900, 510),
            border_thickness=5,
            body_rgba=(255, 255, 255, 255),
            border_rgba=(0, 0, 0, 255)
        )
        main_margin = 10
        main_wireframe = Shape(
            shape_name='Bordered Rect',
            position=(170 + main_margin, 105 + main_margin),
            size=(900 - 2 * main_margin, 510 - 2 * main_margin),
            border_thickness=3,
            body_rgba=(0, 0, 0, 0),
            border_rgba=(0, 0, 0, 255),
        )
        self.add(main_panel)
        self.add(main_wireframe)

        # Menu Item Frames
        menu_item_frames = []
        for i in range(3):
            frame = Shape(
                shape_name='Bordered Rect',
                position=(170 + i * 300, 615),
                size=(300, 45),
                border_thickness=6,
                body_rgba=(255, 255, 255, 255),
                border_rgba=(0, 0, 0, 255)
            )
            menu_item_frames.append(frame)
            self.add(frame)
