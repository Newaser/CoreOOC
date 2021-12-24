from super.fight.phy_field import PhyField
from test_scene.player import Player
from public.defaults import Window
from public.image import Test
from public.stat import key_map_p1, key_map_p2


class TestLayer(PhyField):
    is_event_handler = True

    def __init__(self):
        super(TestLayer, self).__init__()

        # Add player1
        self.player1 = Player(Test.actor, key_map_p1)
        self.player1.unified_position = Window.WIDTH / 3, Window.HEIGHT / 2
        self.add(self.player1)

        # Add player2
        self.player2 = Player(Test.swiftness, key_map_p2)
        self.player2.unified_position = Window.WIDTH * 2 / 3, Window.HEIGHT / 2
        self.player2.phy.m = 1
        self.add(self.player2)
