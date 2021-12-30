"""
Self-defined actions.
For actions defined in this file:
    - If formed as func, it is the combination of actions defined in `cocos.actions`
    - If formed as class, it is new ones
"""

from cocos.actions import *
from cocos.euclid import Vector3


def thump(maxsize=1.05, cycle=1):
    """
    CocosNode thumps like a heart circularly in a specific cycle

    Example::

        sprite.do(thump())
    """
    scale = ScaleBy(maxsize, duration=cycle / 2)
    return Repeat(scale + Reverse(scale))


def stop_thump(duration=0):
    """
    Remedial work after a CocosNode stopped thumping

    Example::

        sprite.do(thump())
        sprite.stop()
        sprite.do(stop_thump())
    """
    return ScaleTo(1, duration)


def highlight(maxsize=1.05):
    """
    Scales a CocosNode by 1.05 in no time.

    Common Usage: Highlight texts

    Example::

        label.do(highlight())
    """
    return ScaleBy(maxsize, duration=0)


def stop_highlight():
    """
    Stop a CocosNode from highlighting

    Example::

        label.do(highlight())
        label.do(stop_highlight())
    """
    return ScaleTo(1, duration=0)


class FadeBy(IntervalAction):
    """Fades a `CocosNode` object by a multiple value by modifying it's opacity attribute.

    Example::

        action = FadeBy(0.5, 2)
        sprite.do(action)
    """
    def init(self, multiple, duration):
        """Init method.

        :Parameters:
            `multiple` : float
                The multiple of the alpha
            `duration` : float
                Seconds that it will take to fade
        """
        self.mul = multiple
        self.duration = duration

    def start(self):
        self.start_alpha = self.target.opacity
        self.end_alpha = self.start_alpha * self.mul

        if not 0 <= self.end_alpha <= 255:
            raise ValueError("The multiple of alpha is too big or too small")

    def update(self, t):
        self.target.opacity = self.start_alpha + (
            self.end_alpha - self.start_alpha) * t


class ShapeGraduateTo(IntervalAction):
    """
    Transform a Shape(or its border) from the
    original color to a new color in a specific time.

    Example::

        new_color = (255, 100, 255)
        action = ShapeGraduateTo(new_color, 2, 'border')
        shape.do(action)
    """
    def init(self, rgb, duration, obj='body'):
        self.rgb = Vector3(*rgb)
        self.duration = duration
        self.obj = obj

        if obj not in ['body', 'border']:
            raise ValueError('''
            The object of action "ShapeGraduateTo" must in 'body', 'border'
            ''')

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
    """
    Fades a Shape(or its border) to a specific alpha.It is an analogue of
    :class:`cocos.actions.interval_actions.FadeTo` in Shape CocosNode.

    Example::

        action = ShapeFadeTo(128, 2, 'border')
        shape.do(action)
    """
    def init(self, alpha, duration, obj='body'):
        self.alpha = alpha
        self.duration = duration
        self.obj = obj

        if obj not in ['body', 'border']:
            raise ValueError('''
            The object of action "ShapeFadeTo" must in 'body', 'border'
            ''')

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
    """
    Multiply a Shape(or its border)'s alpha by a specific multiple.

    Example::

        # Shape fade by half in 3 secs
        action = ShapeFadeBy(0.5, 3, 'border')
        shape.do(action)
    """
    def init(self, multiple, duration, obj='body'):
        self.multiple = multiple
        self.duration = duration
        self.obj = obj

        if obj not in ['body', 'border']:
            raise ValueError('''
            The object of action "ShapeFadeBy" must in 'body', 'border'
            ''')

    def start(self):
        self.start_alpha = {'body': self.target.opacity,
                            'border': self.target.border_opacity}[self.obj]
        self.end_alpha = int(self.start_alpha * self.multiple)

        if not 0 <= self.end_alpha <= 255:
            raise ValueError('''
            The multipled value of alpha out of range(0, 255)
            ''')

    def update(self, t):
        temp_alpha = self.start_alpha + (
            self.end_alpha - self.start_alpha) * t

        if self.obj == 'body':
            self.target.opacity = temp_alpha
        else:
            self.target.border_opacity = temp_alpha
