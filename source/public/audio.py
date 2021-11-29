from manager.audio_manager import JuniorPlayer as _JP
from manager.audio_manager import SeniorPlayer as _SP

# Sound resources
_sound_path = "../res/sound"
_sound_list = ['button_selected', 'button_activate']
sound = _JP(_sound_path, _sound_list)

# Music resources
_music_path = "../res/music"
_music_list = ['impassioned', 'mild']
music = _SP(_music_path, _music_list)
