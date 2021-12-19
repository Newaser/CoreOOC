from .defaults import Settings
from manager.setting_manager import SettingManager


sm = SettingManager(Settings.DEFAULT_SETTINGS)
current_settings = sm.new_settings()

# Quotations
key_map = current_settings['key_map']
key_map_p1 = sm.split(current_settings, 'key_map_p1')
key_map_p2 = sm.split(current_settings, 'key_map_p2')
