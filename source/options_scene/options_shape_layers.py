from cocos.layer import Layer
from public.shapes import BorderedShape


class MainPanelLayer(Layer):
    def __init__(self):
        super(MainPanelLayer, self).__init__()

        # Main panel & its rect wireframe
        self.body = BorderedShape(
            shape_name='Rect',
            position=(170, 105),
            size=(900, 510),
            border_thickness=5,
            body_rgba=(255, 228, 181, 211),
            border_rgba=(218, 165, 32, 211)
        )
        self.margin = 10
        self.wireframe = BorderedShape(
            shape_name='Rect',
            position=(170 + self.margin, 105 + self.margin),
            size=(900 - 2 * self.margin, 510 - 2 * self.margin),
            border_thickness=3,
            body_rgba=(0, 0, 0, 0),
            border_rgba=(218, 165, 32, 255),
        )
        self.add(self.body)
        self.add(self.wireframe)


class UpBarLayer(Layer):
    def __init__(self):
        super(UpBarLayer, self).__init__()

        # Add up bars
        for i in range(3):
            up_bar = BorderedShape(
                shape_name='Rect',
                position=(170 + i * 300, 615),
                size=(300, 45),
                border_thickness=6,
                body_rgba=(255, 228, 181, 211),
                border_rgba=(222, 184, 135, 211)
            )
            self.add(up_bar)
