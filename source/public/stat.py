"""
Statistics of the game
"""
from manager.recorder import Recorder
from manager.setting_manager import SettingManager
from manager.progress_manager import ProgressManager
from manager.item_manager import ItemManager


class Statistics:
    """
    Record statistics
    """
    # A Recorder records important game statistics
    recorder = Recorder()

    # Unimportant statistics
    #: If the main game has been started
    has_started = False

    #: the present player to equip/unequip equipments on the inventory
    present_player = 'player1'


# Statistics object
stat = Statistics()

# Managers
sm = SettingManager(stat.recorder.settings)
pm = ProgressManager(stat.recorder.progress)
im = ItemManager(stat.recorder.items, stat.recorder.airplane_equipments)


# Segments of Statistics

#: Key Maps
key_map = sm.settings['key_map']
key_map_p1 = sm.query('key_map_p1')
key_map_p2 = sm.query('key_map_p2')
