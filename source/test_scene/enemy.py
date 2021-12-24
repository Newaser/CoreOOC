from super.fight.actor import LivingActor


class Enemy(LivingActor):
    category = 'enemy'

    def __init__(self, image):
        super(Enemy, self).__init__(image)

        self.level = 1

        self.orbit = None

        self.generating_area = None
