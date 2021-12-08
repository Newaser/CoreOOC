from cocos.scene import Scene

from .test_layer import TestLayer


class TestScene(Scene):
    def __init__(self):
        super(TestScene, self).__init__()

        self.add(TestLayer())
        