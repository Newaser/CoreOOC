from copy import deepcopy


class SettingManager:
    def __init__(self, default_settings):
        self.default_settings = default_settings
        try:
            # TODO: Import the settings from the save file
            #
            # TODO: Reset key map when the save file is valid, apply the saved settings
            # if save_valid:
            #     self.settings = apply()
            pass
        except Exception as e:
            raise e

    def new_settings(self):
        return deepcopy(self.default_settings)

    def reset(self, settings, sort_list=None):
        if sort_list is None:
            for sort in settings.keys:
                settings[sort] = self.new_settings()[sort]
        else:
            for sort in sort_list:
                settings[sort] = self.new_settings()[sort]

    @staticmethod
    def split(settings, sort):
        if sort == 'key_map_p1':
            key_map = settings['key_map']
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
        elif sort == 'key_map_p2':
            key_map = settings['key_map']
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
        
    def add_difficulty_by(self):
        # TODO: Add difficulty by changing settings properly
        pass
