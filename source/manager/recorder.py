from copy import deepcopy

from public.defaults import Settings, Progress, SAVE_PATH
from db.item import get_formatted_item_dict


class Recorder:
    """
    Recorder records important game statistics data temporarily, and do I/O with
    external save files.
    'Important' game statistics data means that the data can be record to an external
    save file.
    Data in objects of :class:`Recorder` is temporary and volatile, so it is a
    good idea to save the local data of :class:`Recorder` to save files frequently.

    Save data is divided into 3 parts:
        1. Settings: records setting preference, which includes:
            - Video: if fullscreen,
            - Audio: music volume, sound volume
            - Key Map: control-keyboard mapping,
        2. Progress: records game progress, achievements, etc., which includes:
            - High Score: highest score of each level,
            - Accessible: if each level is accessible
        3. Items: number of items the player possesses

    I/O with save files by :meth:`read` and :meth:`write`. If the save file broken,
    :meth:`no_save` will be called.
    """

    def __init__(self):
        self.settings = {}

        self.progress = {}

        # Dictionary maps item_id with item number that the player possess
        self.items = {}

        self.read(SAVE_PATH)

    def __repr__(self):
        return str(self.settings) + "\n" + \
               str(self.progress) + "\n" + \
               str(self.items) + "\n"

    def __is_empty(self):
        """If all statistics empty
        """
        return not bool(self.settings) and \
            not bool(self.progress) and \
            not bool(self.items)

    def formatting(self):
        """Formatting the local data and save file
        """
        self.settings = deepcopy(Settings.DEFAULT)
        self.progress = deepcopy(Progress.DEFAULT)
        self.items = get_formatted_item_dict()

        self.write(SAVE_PATH)

    def read(self, path):
        """Read data from save files to local.
        If local data exists, it will be overwritten
        """
        try:
            with open(path, 'r') as save_file:
                content = save_file.read().split('\n')
        except FileNotFoundError:
            self.no_save()
            return

        # EXTRACT values from the content
        self.settings = eval(content[0])
        self.progress = eval(content[1])
        self.items = eval(content[2])

    def write(self, path):
        """Submit the local data to external save files in the form of String
        """
        with open(path, 'w') as save_file:
            save_file.write(self.__repr__())

    def no_save(self):
        """What to do if there's no save file
        """
        if self.__is_empty():
            self.formatting()
        else:
            # TODO: Give 2 choices when save file is broken:
            #   1. Overwrite the save file with the Recorder
            #   2. Formatting the Recorder and save file
            pass
