from cocos.scene import Scene

from public.language import shift_language
from .test_layer import TestLayer


class TestScene(Scene):
    def __init__(self):
        super(TestScene, self).__init__()

        self.add(TestLayer())

    def on_enter(self):
        super(TestScene, self).on_enter()

        shift_language()
