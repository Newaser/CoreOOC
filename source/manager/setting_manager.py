from copy import deepcopy
from public.defaults import Settings


class SettingManager:
    """Manage setting preferences with a given setting dictionary.
    """
    def __init__(self, settings):
        self.settings = settings

    def reset(self, sort_list=None):
        """Reset settings in batches
        """
        # Default: reset all settings
        if sort_list is None:
            sort_list = self.settings.keys()

        # Reset
        for sort in sort_list:
            self.settings[sort] = deepcopy(Settings.DEFAULT[sort])

    def query(self, keyword):
        """Query certain subset of settings by keyword
        """
        if keyword == 'key_map_p1':
            key_map = self.settings['key_map']
            return {
                "UP": key_map['battle_up_p1'],
                "DOWN": key_map['battle_down_p1'],
                "LEFT": key_map['battle_left_p1'],
                "RIGHT": key_map['battle_right_p1'],
                "ATTACK": key_map['attack_p1'],
                "SPEED": key_map['speed_p1'],
                "RESCUE": key_map['rescue_p1'],
                "SKILL_1": key_map['skill_1_p1'],
                "SKILL_2": key_map['skill_2_p1'],
                "SKILL_3": key_map['skill_3_p1'],
            }
        elif keyword == 'key_map_p2':
            key_map = self.settings['key_map']
            return {
                "UP": key_map['battle_up_p2'],
                "DOWN": key_map['battle_down_p2'],
                "LEFT": key_map['battle_left_p2'],
                "RIGHT": key_map['battle_right_p2'],
                "ATTACK": key_map['attack_p2'],
                "SPEED": key_map['speed_p2'],
                "RESCUE": key_map['rescue_p2'],
                "SKILL_1": key_map['skill_1_p2'],
                "SKILL_2": key_map['skill_2_p2'],
                "SKILL_3": key_map['skill_3_p2'],
            }

    def add_difficulty_by(self, rate):
        # TODO: Add difficulty by changing settings properly
        pass
