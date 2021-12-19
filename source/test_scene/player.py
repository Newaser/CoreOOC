from public.defaults import Vectors
from super.fight.actor import Actor


class Player(Actor):
    def __init__(self, image, player_keys):
        super(Player, self).__init__(image)

        self.category = 'player'
        self.player_keys = player_keys

    def on_key_press(self, symbol, _):
        if symbol in self.player_keys['UP']:
            self.phy.force('F_up', Vectors.UP_PUSH)
        elif symbol in self.player_keys['DOWN']:
            self.phy.force('F_down', Vectors.DOWN_PUSH)
        elif symbol in self.player_keys['LEFT']:
            self.phy.force('F_left', Vectors.LEFT_PUSH)
        elif symbol in self.player_keys['RIGHT']:
            self.phy.force('F_right', Vectors.RIGHT_PUSH)
        elif symbol in self.player_keys['SPEED']:
            # self.phy.motion_scale *= 2
            self.phy.v *= Vectors.SPEED_MUL

    def on_key_release(self, symbol, _):
        if symbol in self.player_keys['UP']:
            self.phy.release('F_up')
        elif symbol in self.player_keys['DOWN']:
            self.phy.release('F_down')
        elif symbol in self.player_keys['LEFT']:
            self.phy.release('F_left')
        elif symbol in self.player_keys['RIGHT']:
            self.phy.release('F_right')
        elif symbol in self.player_keys['SPEED']:
            # self.phy.motion_scale *= 0.5
            pass
