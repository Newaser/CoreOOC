from public.defaults import Settings
from manager.setting_manager import SettingManager


sm = SettingManager(Settings.DEFAULT_SETTINGS)
current_settings = sm.new_settings()
