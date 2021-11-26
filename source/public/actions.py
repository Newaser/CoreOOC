from cocos.actions import *


def thump(maxsize=1.05, cycle=1):
    scale = ScaleBy(maxsize, duration=cycle/2)
    return Repeat(scale + Reverse(scale))


def stop_thump(duration=0):
    return ScaleTo(1, duration)
