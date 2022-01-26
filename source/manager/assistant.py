from collections import deque
from copy import copy

from cocos.director import director
from cocos.euclid import Vector2
from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.text import Label

from public.actions import *
from public.audio import sound
from public.defaults import Z, Window, Styles
from public.shapes import BorderedShape


class Assistant(object):
    """The assistant of the director, an instance of :class:`cocos.director.Director`
    """
    @classmethod
    def warn(cls, msg, duration=2):
        """Add a warning panel to current scene with a specific massage
        """
        # CREATE a warning panel fading in and out
        warning_panel = WarningPanel(msg)
        warning_panel.pass_by(duration)

        # ADD the panel to the current scene
        director.scene.add(warning_panel, z=Z.WARNING)

    @classmethod
    def notify(cls, tuple_list, sound_play=True):
        """Notify the receipt of items.

        :param tuple_list: list[(item_icon, amount), ...]
        :param sound_play: if play sound effect
        """
        # CREATE a notifier ADDED the RECEIPTS
        notifier = ReceiptNotifier(tuple_list, sound_play)

        # ADD the notifier to the current SCENE
        director.scene.add(notifier, z=Z.NOTICE)

        # RUN the notifier
        notifier.start_notifying()


class WarningPanel(Layer):
    """A panel throws a warning massage onto the screen
    """

    def __init__(self, msg=''):
        super(WarningPanel, self).__init__()

        # LAYOUT STUFF

        #: center of the massage Label
        self.massage_center = Window.WIDTH // 2, Window.HEIGHT // 6

        #: about the panel
        self.panel_size = 222, 100
        self.panel_bottom_left = tuple((Vector2(*self.massage_center) - Vector2(*self.panel_size) // 2)[:])

        #: text of massage
        self.massage_text = msg

        # COMPONENT STUFF

        #: a panel BorderedShape contains warning massage
        self.panel = None

        #: a massage Label
        self.massage = None

        # EXECUTIONS
        self._build()

    def _build(self):
        """Build components
        """
        # BUILD PANEL
        self.panel = BorderedShape(
            shape_name='Rect',
            position=self.panel_bottom_left,
            size=self.panel_size,
            **Styles.WARNING_PANEL_RECT,
        )

        # BUILD MASSAGE
        self.massage = Label(self.massage_text, **Styles.WARNING_FONT)
        self.massage.position = self.massage_center

        # ADD
        self.add(self.panel)
        self.add(self.massage)

    def pass_by(self, duration):
        """Fade in -> Stay -> Fade out -> Kill self
        """
        # allocate TIME
        proportions = 1, 5, 3
        time_vector = Vector3(*proportions) / sum(proportions) * duration

        # define pass by ACTION
        pass_by_action = FadeIn(time_vector[0]) + Delay(time_vector[1]) + FadeOut(time_vector[2])

        # DO actions
        self.panel.do(pass_by_action)
        self.massage.do(pass_by_action)
        self.do(Delay(duration) + CallFunc(self.kill))


class ReceiptNotifier(Layer):
    """Notify the receipt of items.
    List the item obtained grouped by category onto the screen.

    Appearance::
        -------------------------
        |                       |
        |   [item_icon1] × 1    |
        |   [item_icon2] × 3    |
        |   [item_icon3] × 1    |
        |                       |
        -------------------------
    """

    def __init__(self, receipt_tuples=None, sound_play=True):
        """:param receipt_tuples:
                a series of receipts formed as tuples: [(item_icon, amount)] * n
        """
        super(ReceiptNotifier, self).__init__()

        # LAYOUT STUFF

        #: about the line's background panels
        self.base_bg_bottom_left = Window.WIDTH * 0.85, 40
        self.bg_width = \
            Window.WIDTH - self.base_bg_bottom_left[0] + \
            Styles.RECEIPT_BG_RECT['border_thickness']
        self.bg_height = 70
        self.bg_size = self.bg_width, self.bg_height

        #: about the item icons
        self.icon_scale = 50 / 67
        self.base_icon_center = tuple((Vector2(*self.base_bg_bottom_left) +
                                       Vector2(45, self.bg_height / 2))[:])

        #: the center left of the first amount label
        self.base_label_center_left = tuple((Vector2(*self.base_bg_bottom_left) +
                                             Vector2(75, self.bg_height / 2))[:])

        #: a step of lines' single move
        self.step = 0, 90

        #: max lines to display at the same time
        self.max_line = 2

        #: multiple of line's single fade
        self.fade_mul = 0.5

        # FUNCTIONAL STUFF

        #: the period(secs) that the receipt lines update
        self.tick = 1

        #: count if secs exceeds one tick
        self.time_counter = 0.8

        #: if the sound plays
        self.sound_play = sound_play

        # COMPONENT STUFF

        #: a series of receipts formed as _Lines:
        self.receipt_lines = deque([])

        #: the lines on screen
        self.screen_lines = set()

        # EXECUTIONS

        #: build components
        self.add_receipts(receipt_tuples)

    def start_notifying(self):
        """Start to notify the player
        """
        #: update lines
        self.schedule(self._count)

    def pause_notifying(self):
        """Pause notifying the player
        """
        self.unschedule(self._count)

    def add_receipts(self, receipt_tuples):
        """Add receipts to the line list
        """
        if receipt_tuples is None:
            return

        # BUILD receipt LINES
        for icon, amount in receipt_tuples:
            if not isinstance(icon, Sprite):
                raise TypeError("Item icon must be a Sprite")

            # BUILD BACKGROUND
            background = BorderedShape(
                shape_name='Rect',
                position=self.base_bg_bottom_left,
                size=self.bg_size,
                **Styles.RECEIPT_BG_RECT,
            )

            # BUILD ICON
            icon.position = self.base_icon_center
            icon.do(ScaleTo(self.icon_scale, 0))

            # BUILD amount LABEL
            amount_label = Label('× ' + str(amount), **Styles.RECEIPT_FONT)
            amount_label.position = self.base_label_center_left

            # ADD a line
            new_line = self._Line(background, icon, amount_label)
            self.receipt_lines.append(new_line)

    def _add_line(self, line):
        """Add a receipt line onto the screen
        """
        for component in line.components:
            self.add(component)

        for component in [line.item_icon, line.amount_label]:
            component.do(throw_in())

        self.screen_lines.add(line)

    def _remove_line(self, line):
        """Remove a receipt line from the screen
        """
        for component in line.components:
            self.remove(component)

        self.screen_lines.remove(line)

    def _move_line(self, line):
        """Move a line up
        """
        for component in line.components:
            component.do(MoveBy(self.step, 0))

        line.row_order += 1

    def _fade_line(self, line):
        """Make a line more transparent
        """
        for component in line.components:
            component.do(FadeBy(self.fade_mul, 0))

    def _count(self, dt):
        """Count the secs and see if it exceeds one tick
        """
        # time elapse
        self.time_counter += dt

        # UPDATE lines and RECOUNT
        if self.time_counter >= self.tick:
            self._update()
            self.time_counter = 0

    def _update(self):
        """Fade out old lines, add new lines, update lines' vertical
        positions, and play sound.
        """
        # MOVE and FADE the old lines
        for line in self.screen_lines:
            self._move_line(line)
            self._fade_line(line)

        # ADD a new line to the screen
        try:
            new_line = self.receipt_lines.popleft()
        except IndexError:
            # if the queue empty and no on-screen lines
            if len(self.screen_lines) == 0:
                self.pause_notifying()
                self.kill()
                return
        else:
            # ADD a new line
            self._add_line(new_line)

            # play SOUND
            if self.sound_play:
                sound.play(Styles.NOTIFYING_SOUND)

        # REMOVE lines out of range
        for line in copy(self.screen_lines):
            if line.row_order > self.max_line:
                self._remove_line(line)

    class _Line(object):
        """A line indicates the information of one receipt of items
        """

        def __init__(self, background, icon, label, row=1):
            # COMPONENT STUFF

            self.background_panel = background

            self.item_icon = icon

            self.amount_label = label

            # FUNCTIONAL STUFF

            self.row_order = row

        @property
        def components(self):
            """Form the components as a list
            """
            return [self.background_panel, self.item_icon, self.amount_label]
