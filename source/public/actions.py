from cocos.actions import *
from cocos.euclid import Vector3


def thump(maxsize=1.05, cycle=1):
    scale = ScaleBy(maxsize, duration=cycle / 2)
    return Repeat(scale + Reverse(scale))


def stop_thump(duration=0):
    return ScaleTo(1, duration)


def highlight(maxsize=1.05):
    return ScaleBy(maxsize, duration=0)


def stop_highlight():
    return ScaleTo(1, duration=0)


class ShapeGraduateTo(IntervalAction):
    def init(self, rgb, duration, obj='body'):
        self.rgb = Vector3(*rgb)
        self.duration = duration
        self.obj = obj

        assert obj in ('body', 'border')

    def start(self):
        which = {'body': self.target.color,
                 'border': self.target.border_color}[self.obj]
        self.start_rgb = Vector3(*which)
        self.gradient = self.rgb - self.start_rgb

    def update(self, t):
        temp_rgb = tuple((self.start_rgb + self.gradient * t)[:])
        if self.obj == 'body':
            self.target.color = temp_rgb
        else:
            self.target.border_color = temp_rgb


class ShapeFadeTo(IntervalAction):
    def init(self, alpha, duration, obj='body'):
        self.alpha = alpha
        self.duration = duration
        self.obj = obj

        assert obj in ('body', 'border')

    def start(self):
        self.start_alpha = {'body': self.target.opacity,
                            'border': self.target.border_opacity}[self.obj]

    def update(self, t):
        temp_alpha = self.start_alpha + (
            self.alpha - self.start_alpha) * t

        if self.obj == 'body':
            self.target.opacity = temp_alpha
        else:
            self.target.border_opacity = temp_alpha


class ShapeFadeBy(IntervalAction):
    def init(self, times, duration, obj='body'):
        self.times = times
        self.duration = duration
        self.obj = obj

        assert obj in ('body', 'border')

    def start(self):
        self.start_alpha = {'body': self.target.opacity,
                            'border': self.target.border_opacity}[self.obj]
        self.end_alpha = int(self.obj * self.times)

        assert 0 <= self.end_alpha <= 255

    def update(self, t):
        temp_alpha = self.start_alpha + (
            self.end_alpha - self.start_alpha) * t

        if self.obj == 'body':
            self.target.opacity = temp_alpha
        else:
            self.target.border_opacity = temp_alpha
