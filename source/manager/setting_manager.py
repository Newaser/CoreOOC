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

    def add_difficulty_by(self):
        # TODO: Add difficulty by changing settings properly
        pass
