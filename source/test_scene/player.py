from public.defaults import Player as DePlayer
from super.fight.actor import LivingActor


class Player(LivingActor):
    category = 'player'

    def __init__(self, image, player_keys):
        super(Player, self).__init__(image)

        self.max_HP = DePlayer.DEFAULT_HP

        self.player_keys = player_keys

    def on_key_press(self, symbol, _):
        if symbol in self.player_keys['UP']:
            self.phy.force('F_up', DePlayer.UP_PUSH)
        elif symbol in self.player_keys['DOWN']:
            self.phy.force('F_down', DePlayer.DOWN_PUSH)
        elif symbol in self.player_keys['LEFT']:
            self.phy.force('F_left', DePlayer.LEFT_PUSH)
        elif symbol in self.player_keys['RIGHT']:
            self.phy.force('F_right', DePlayer.RIGHT_PUSH)
        elif symbol in self.player_keys['SPEED']:
            # self.phy.motion_scale *= 2
            self.phy.v *= DePlayer.SPEED_MUL

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
