from cocos.actions import *


def thump(maxsize=1.05, duration=0.5):
    scale = ScaleBy(maxsize, duration=duration)
    return Repeat(scale + Reverse(scale))


def stop_thump(duration=0):
    return ScaleTo(1, duration)